from __future__ import annotations

import re
from typing import Any

from app.agents.behavior import analyze_behavior
from app.agents.goal import plan_goals
from app.agents.guard import guard_response
from app.agents.nudge import generate_nudge
from app.agents.risk import assess_risk
from app.agents.scheme import discover_schemes
from app.models.schemas import ChatResponse, DigitalTwin
from app.services.llm import (
    build_agent_context,
    build_twin_context,
    generate_dynamic_response,
)
from app.services.market_data import fetch_market_context, is_market_query
from app.simulation.monte_carlo import generate_scenarios

CRISIS_KEYWORDS = [
    "can't pay", "suicide", "desperate", "debt trap", "help me",
    "बेचैन", "तंग", "आत्महत्या",
]

SIMULATION_KEYWORDS = [
    "should i", "what if", "loan", "borrow", "sip", "invest in",
    "buy a house", "afford", "worth it", "कर्ज", "ऋण", "save for",
]


def classify_intent(message: str) -> dict[str, Any]:
    msg = message.lower()
    is_crisis = any(k in msg for k in CRISIS_KEYWORDS)
    is_market = is_market_query(message)
    is_scheme = any(k in msg for k in ["scheme", "yojana", "benefit", "government", "pm-", "योजना"])
    is_simulation = (
        not is_market
        and any(k in msg for k in SIMULATION_KEYWORDS)
    )

    if is_crisis:
        return {"intent": "crisis", "agents": ["guard", "behavior", "risk"], "run_simulation": False}
    if is_market:
        return {"intent": "market", "agents": ["behavior", "risk", "guard"], "run_simulation": False}
    if is_simulation:
        return {"intent": "decision", "agents": ["behavior", "risk", "goal", "nudge", "scheme", "guard"], "run_simulation": True}
    if is_scheme:
        return {"intent": "scheme", "agents": ["scheme", "behavior", "guard"], "run_simulation": False}

    return {"intent": "general", "agents": ["behavior", "risk", "goal", "nudge", "scheme", "guard"], "run_simulation": False}


def _crisis_response(twin: DigitalTwin) -> str:
    name = twin.name.split()[0] if twin.name else "friend"
    return (
        f"{name}, I hear that you're going through a very difficult time. "
        "You are not alone. I'm connecting you with our human support partner "
        "who will reach out within 60 seconds. Please call **1800-599-0019** (iCall) "
        "or **9152987821** (Vandrevala Foundation) for immediate help. "
        "Your financial situation can improve — let's take this one step at a time."
    )


async def process_message(
    twin: DigitalTwin,
    message: str,
    voice_mode: bool = False,
    chat_history: list[dict] | None = None,
) -> ChatResponse:
    intent = classify_intent(message)
    agents_used = intent["agents"]

    if intent["intent"] == "crisis":
        guarded = guard_response(_crisis_response(twin), is_crisis=True)
        return ChatResponse(
            message=guarded["content"],
            agents_used=["guard"],
            disclaimer=guarded["disclaimer"],
        )

    behavior = analyze_behavior(twin)
    risk = assess_risk(twin)
    goal = plan_goals(twin, message)
    nudge = generate_nudge(twin, behavior, goal)
    schemes = discover_schemes(twin)

    scenarios = None
    if intent.get("run_simulation"):
        scenarios, _ = generate_scenarios(twin, message)

    market_context = fetch_market_context(message)
    if market_context and "market" not in agents_used:
        agents_used = agents_used + ["market_data"]

    twin_context = build_twin_context(twin)
    agent_context = build_agent_context(behavior, risk, goal, schemes, scenarios)

    response_text, provider = await generate_dynamic_response(
        message=message,
        twin_context=twin_context,
        agent_context=agent_context,
        market_context=market_context,
        chat_history=chat_history,
    )

    if provider != "fallback":
        agents_used.append(f"llm:{provider}")

    guarded = guard_response(response_text, is_crisis=False)

    audio_summary = None
    if voice_mode:
        summary_parts = [guarded["content"][:600]]
        if scenarios:
            summary_parts.append(
                f"Simulator summary: Best path has {scenarios[2].debt_trap_probability:.0%} debt trap risk. "
                f"{scenarios[2].nudge_action}"
            )
        audio_summary = " ".join(summary_parts)

    return ChatResponse(
        message=guarded["content"],
        agents_used=agents_used,
        scenarios=scenarios,
        nudge=nudge if intent["intent"] != "market" else None,
        schemes=schemes if intent["intent"] in ("scheme", "general") else None,
        disclaimer=guarded["disclaimer"],
        audio_summary=audio_summary,
    )
