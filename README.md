# ArthSaathi 2.0 — AI Financial Digital Twin

Multi-agent Agentic AI system that creates a living **Financial Digital Twin** for every Indian citizen. Built for Nomura KakushIN 10.0 Financial Literacy & Agentic AI Hackathon.

## Features

- **Dynamic AI Chat (Gemini/OpenAI/Anthropic)** — Ask any financial question; live stock data via yfinance
- **6-Agent Architecture** — Behavior, Risk, Goal, Nudge, Scheme Discovery & Safety Guard agents
- **Financial Health Score** — A–D grade with personalized action recommendations
- **52+ Government Schemes** — Central + state schemes with eligibility matching
- **Mandi Crop Prices** — Agricultural price data for Kisan persona
- **DPDPA Privacy Panel** — Export or delete all your data
- **Markdown Chat** — Rich formatted AI responses with scheme chips inline
- **Future Self Simulator** — 1,000 Monte Carlo simulations across 3 parallel timelines
- **Digital Twin Panel** — 6-dimensional radar chart with interactive 3D visualization
- **4 Demo Personas** — Priya (Teacher), Rajesh (Gig Worker), Kisan (Farmer), Divya (Visual Impairment)
- **Government Scheme Discovery** — 70+ schemes with eligibility matching
- **Voice-First UI** — Web Speech API STT/TTS, voice-only mode for accessibility
- **10 Indian Languages** — Language selector with vernacular support
- **Low Data Mode** — Compressed responses for rural connectivity
- **SEBI Compliance** — Guard Agent filters investment advice

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| 3D UI | Three.js, React Three Fiber, Drei |
| Charts | Recharts, D3.js |
| State | Zustand, TanStack React Query |
| Animations | Framer Motion |
| Backend | FastAPI (Python 3.11) |
| Simulation | NumPy, SciPy, Pandas (Monte Carlo) |
| Agents | LangGraph-style orchestrator (6 agents) |
| Database | PostgreSQL 16 + pgvector (sole data store) |

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 16 with pgvector extension (or Docker)

### 1. PostgreSQL

```bash
docker compose up postgres -d
# Or use a local PostgreSQL instance with:
# CREATE DATABASE arthsaathi;
# CREATE EXTENSION vector;
```

### 2. Backend

```bash
cd backend
cp .env.example .env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

App: http://localhost:3000

### 4. Docker (Full Stack)

```bash
docker-compose up --build
```

## Project Structure

```
namura/
├── frontend/          # Next.js 14 web app with 3D UI
│   ├── src/
│   │   ├── app/           # Pages (landing, dashboard)
│   │   ├── components/    # 3D, chat, twin, schemes, etc.
│   │   ├── lib/           # API client, store, utils
│   │   └── types/         # TypeScript definitions
├── backend/           # FastAPI multi-agent backend
│   ├── app/
│   │   ├── agents/        # 6 AI agents + orchestrator
│   │   ├── simulation/    # Monte Carlo engine
│   │   ├── data/          # Personas & schemes DB
│   │   └── main.py        # API endpoints
└── docker-compose.yml
```

## PostgreSQL Schema

All data is stored exclusively in PostgreSQL 16 (with pgvector extension):

| Table | Purpose |
|-------|---------|
| `digital_twins` | User Digital Twin profiles (JSONB) |
| `twin_history` | Versioned twin snapshots |
| `government_schemes` | Scheme knowledge base (70+ schemes) |
| `chat_messages` | Conversation history per user |
| `nudge_feedback` | Nudge action tracking (acted/snoozed/dismissed) |
| `simulation_cache` | Cached Monte Carlo simulation results |

Tables are auto-created on backend startup. Demo personas and schemes are seeded automatically.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/chat` | POST | Multi-agent chat processing |
| `/api/v1/twin/{user_id}` | GET | Fetch Digital Twin |
| `/api/v1/simulate` | POST | Run Future Scenario Simulator |
| `/api/v1/schemes/{user_id}` | GET | Discover eligible schemes |
| `/api/v1/onboarding` | POST | Create new Digital Twin |
| `/api/v1/nudge/feedback` | POST | Nudge action feedback |

## Demo Personas

| Persona | Profile | Key Feature |
|---------|---------|-------------|
| Priya | Teacher, Thane, ₹35K/mo | Product explainer + Marathi voice |
| Rajesh | Gig Worker, Mumbai | Debt risk + irregular income |
| Kisan | Farmer, Karnataka | Scheme discovery + mandi prices |
| Divya | Visual Impairment, Pune | Voice-only + disability schemes |

## Environment Variables

```env
# Backend (optional for full LLM integration)
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
BHASHINI_API_KEY=your_key
DATABASE_URL=postgresql+psycopg://arthsaathi:arthsaathi@localhost:5432/arthsaathi

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Disclaimer

This application provides **educational information only** — not regulated financial advice. All outputs pass through the Safety & Compliance Guard Agent per SEBI guidelines.
