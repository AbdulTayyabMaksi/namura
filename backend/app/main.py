from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.agents.orchestrator import process_message
from app.services.health_score import compute_financial_health_score
from app.database import get_db, init_db
from app.db_seed import seed_database
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    DigitalTwin,
    NudgeFeedback,
    OnboardingRequest,
    ScenarioBranch,
    SimulateRequest,
    SimulateResponse,
)
from app.simulation.monte_carlo import generate_scenarios
from app.store import twin_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="ArthSaathi 2.0 API",
    description="AI Financial Digital Twin — Multi-Agent Agentic AI System",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {
        "status": "healthy",
        "service": "arthsaathi-backend",
        "version": "2.0.0",
        "database": "postgresql",
        "db_status": db_status,
    }


@app.get("/api/v1/personas")
async def list_personas(db: Session = Depends(get_db)):
    return [
        {
            "id": t.user_id,
            "name": t.name,
            "occupation": t.context.occupation,
            "location": t.context.location,
            "language": t.context.language.value,
            "persona_id": t.persona_id.value if t.persona_id else None,
            "archetype": t.behavioral_archetype,
        }
        for t in twin_store.list_all(db)
    ]


@app.post("/api/v1/onboarding", response_model=DigitalTwin)
async def onboarding(req: OnboardingRequest, db: Session = Depends(get_db)):
    if req.persona_id:
        existing = twin_store.get(db, req.persona_id.value)
        if existing:
            return existing
    return twin_store.create_from_onboarding(db, req)


@app.get("/api/v1/twin/{user_id}", response_model=DigitalTwin)
async def get_twin(user_id: str, db: Session = Depends(get_db)):
    twin = twin_store.get(db, user_id)
    if not twin:
        raise HTTPException(404, "Digital Twin not found")
    return twin


@app.post("/api/v1/twin/{user_id}", response_model=DigitalTwin)
async def update_twin(user_id: str, updates: dict, db: Session = Depends(get_db)):
    twin = twin_store.update(db, user_id, updates)
    if not twin:
        raise HTTPException(404, "Digital Twin not found")
    return twin


@app.delete("/api/v1/twin/{user_id}")
async def delete_twin(user_id: str, db: Session = Depends(get_db)):
    if not twin_store.delete(db, user_id):
        raise HTTPException(404, "Digital Twin not found")
    return {"deleted": True, "user_id": user_id}


@app.get("/api/v1/twin/{user_id}/history")
async def twin_history(user_id: str, db: Session = Depends(get_db)):
    history = twin_store.get_history(db, user_id)
    if not history:
        raise HTTPException(404, "No history found")
    return [
        {"version": t.version, "updated_at": t.updated_at, "archetype": t.behavioral_archetype}
        for t in history
    ]


@app.get("/api/v1/chat/{user_id}/history")
async def chat_history(user_id: str, db: Session = Depends(get_db)):
    return twin_store.get_chat_history(db, user_id)


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    twin = twin_store.get(db, req.user_id)
    if not twin:
        raise HTTPException(404, "Digital Twin not found. Complete onboarding first.")

    history = twin_store.get_chat_history(db, req.user_id, limit=10)
    twin_store.save_chat_message(db, req.user_id, "user", req.message)
    skip_nudge = twin_store.has_nudge_today(db, req.user_id)
    response = await process_message(
        twin,
        req.message,
        req.voice_mode,
        chat_history=history,
        skip_nudge=skip_nudge,
    )
    twin_store.update(
        db,
        req.user_id,
        {
            "behavioral_archetype": twin.behavioral_archetype,
            "behavioral_score": min(1.0, twin.behavioral_score + 0.01),
        },
    )
    twin_store.save_chat_message(
        db,
        req.user_id,
        "assistant",
        response.message,
        metadata={
            "agents_used": response.agents_used,
            "has_scenarios": bool(response.scenarios),
            "has_nudge": bool(response.nudge),
        },
    )
    return response


@app.post("/api/v1/simulate", response_model=SimulateResponse)
async def simulate(req: SimulateRequest, db: Session = Depends(get_db)):
    twin = twin_store.get(db, req.user_id)
    if not twin:
        raise HTTPException(404, "Digital Twin not found")

    cached = twin_store.get_cached_simulation(db, req.user_id, req.question)
    if cached:
        return SimulateResponse(
            scenarios=[ScenarioBranch(**s) for s in cached["scenarios"]],
            computation_ms=cached["computation_ms"],
        )

    scenarios, elapsed = generate_scenarios(twin, req.question)
    result = {
        "scenarios": [s.model_dump() for s in scenarios],
        "computation_ms": elapsed,
    }
    twin_store.cache_simulation(db, req.user_id, req.question, result)
    return SimulateResponse(scenarios=scenarios, computation_ms=elapsed)


@app.get("/api/v1/twin/{user_id}/health-score")
async def health_score(user_id: str, db: Session = Depends(get_db)):
    twin = twin_store.get(db, user_id)
    if not twin:
        raise HTTPException(404, "Digital Twin not found")
    return compute_financial_health_score(twin)


@app.get("/api/v1/schemes/{user_id}")
async def get_schemes(user_id: str, db: Session = Depends(get_db)):
    twin = twin_store.get(db, user_id)
    if not twin:
        raise HTTPException(404, "Digital Twin not found")
    return twin_store.get_schemes_from_db(db, twin)


@app.post("/api/v1/nudge/feedback")
async def nudge_feedback(req: NudgeFeedback, db: Session = Depends(get_db)):
    twin_store.save_nudge_feedback(db, req.user_id, req.nudge_id, req.action)
    return {"received": True, "action": req.action, "nudge_id": req.nudge_id}


@app.post("/api/v1/voice/stt")
async def speech_to_text():
    return {"text": "", "note": "Use browser Web Speech API for demo STT"}


@app.post("/api/v1/voice/tts")
async def text_to_speech(body: dict):
    return {"audio_url": None, "text": body.get("text", ""), "note": "Use browser SpeechSynthesis for demo TTS"}


@app.post("/api/v1/webhook/whatsapp")
async def whatsapp_webhook(body: dict, db: Session = Depends(get_db)):
    message = body.get("message", body.get("text", ""))
    user_id = body.get("user_id", "rajesh")
    twin = twin_store.get(db, user_id)
    if not twin or not message:
        return {"reply": "Welcome to ArthSaathi! Send your financial question."}
    history = twin_store.get_chat_history(db, user_id, limit=10)
    response = await process_message(twin, message, chat_history=history)
    twin_store.save_chat_message(db, user_id, "user", message)
    twin_store.save_chat_message(db, user_id, "assistant", response.message)
    return {"reply": response.message, "scenarios": len(response.scenarios or [])}
