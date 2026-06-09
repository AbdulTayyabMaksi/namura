from __future__ import annotations

import json
from typing import Any

import httpx

from app.config import settings

SYSTEM_PROMPT = """You are ArthSaathi 2.0 — an AI Financial Digital Twin assistant for Indian citizens.

Your role:
- Answer ANY financial question dynamically: personal finance, loans, savings, taxes, insurance, stocks, companies, mutual funds, crypto, real estate, government schemes, etc.
- Personalize answers using the user's Digital Twin profile and agent analysis provided below.
- When live market data is provided, use it in your answer with specific numbers.
- Explain complex topics in plain language suitable for the user's literacy level.
- For Indian users, default to INR (₹) and Indian context (SEBI, RBI, NSE, BSE, PM schemes).
- You may discuss companies, stocks, and market trends EDUCATIONALLY — explain what the data means.
- NEVER say "you should buy" or "you should sell" a specific stock/fund — that is SEBI-regulated investment advice.
- Instead say "factors to consider", "what the data suggests educationally", "consult a SEBI-registered advisor for decisions".
- If the user is in financial crisis, be empathetic and suggest human support.
- Give complete, thorough answers. Do not stop mid-sentence. Finish every section you start.
- Use markdown formatting: **bold** for key points, bullet lists where helpful.
- Respond in the user's preferred language when possible (language code provided in context).
"""


def _build_user_prompt(
    message: str,
    twin_context: str,
    agent_context: str,
    market_context: str,
    chat_history: list[dict],
) -> str:
    history_text = ""
    if chat_history:
        lines = [f"{m['role'].upper()}: {m['content'][:500]}" for m in chat_history[-6:]]
        history_text = "RECENT CONVERSATION:\n" + "\n".join(lines) + "\n\n"

    parts = [
        history_text,
        "USER DIGITAL TWIN PROFILE:",
        twin_context,
        "\nAGENT ANALYSIS:",
        agent_context or "No additional agent analysis.",
    ]
    if market_context:
        parts.extend(["\n", market_context])
    parts.extend(["\nUSER QUESTION:", message])
    return "\n".join(parts)


async def _call_openai(system: str, user: str) -> str | None:
    if not settings.openai_api_key:
        return None
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.llm_model_openai,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "temperature": 0.7,
                "max_tokens": 4096,
            },
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def _call_anthropic(system: str, user: str) -> str | None:
    if not settings.anthropic_api_key:
        return None
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.llm_model_anthropic,
                "max_tokens": 4096,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            },
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        return data["content"][0]["text"]


def _extract_google_text(data: dict) -> str | None:
    candidates = data.get("candidates") or []
    if not candidates:
        return None
    parts = candidates[0].get("content", {}).get("parts", [])
    texts = [p.get("text", "") for p in parts if p.get("text")]
    return "\n".join(texts).strip() if texts else None


async def _call_google(system: str, user: str) -> str | None:
    if not settings.google_api_key:
        return None
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{settings.llm_model_google}:generateContent",
            params={"key": settings.google_api_key},
            json={
                "system_instruction": {"parts": [{"text": system}]},
                "contents": [{"parts": [{"text": user}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 8192,
                },
            },
        )
        if resp.status_code != 200:
            return None
        return _extract_google_text(resp.json())


def _fallback_response(
    message: str,
    twin_context: str,
    agent_context: str,
    market_context: str,
) -> str:
    """Intelligent fallback when no LLM API key is configured."""
    name = twin_context.split("Name:")[1].split("\n")[0].strip() if "Name:" in twin_context else "there"

    parts = [f"Hello {name}! Here's what I can tell you about your question:\n"]

    if market_context:
        parts.append(market_context)
        parts.append(
            "\n**Educational note**: The data above is live market information. "
            "Past performance doesn't guarantee future returns. "
            "For investment decisions, consult a SEBI-registered investment advisor."
        )

    if agent_context and agent_context.strip() != "No additional agent analysis.":
        parts.append(f"\n**Your Financial Profile Insights**:\n{agent_context}")

    parts.append(
        f"\n**Regarding your question**: \"{message}\"\n\n"
        "I'm currently running in demo mode without an LLM API key. "
        "To get fully dynamic AI answers about any company, stock, or financial topic, "
        "add one of these to your `backend/.env` file:\n"
        "- `OPENAI_API_KEY=sk-...`\n"
        "- `ANTHROPIC_API_KEY=sk-ant-...`\n"
        "- `GOOGLE_API_KEY=...` (free at aistudio.google.com)\n\n"
        "With an API key enabled, I can answer any financial question dynamically — "
        "stock analysis, company comparisons, tax planning, loan decisions, and more."
    )

    return "\n".join(parts)


async def generate_dynamic_response(
    message: str,
    twin_context: str,
    agent_context: str,
    market_context: str = "",
    chat_history: list[dict] | None = None,
) -> tuple[str, str]:
    """Returns (response_text, provider_used)."""
    user_prompt = _build_user_prompt(
        message, twin_context, agent_context, market_context, chat_history or []
    )

    for provider, fn in [
        ("openai", _call_openai),
        ("anthropic", _call_anthropic),
        ("google", _call_google),
    ]:
        result = await fn(SYSTEM_PROMPT, user_prompt)
        if result:
            return result, provider

    return _fallback_response(message, twin_context, agent_context, market_context), "fallback"


def build_twin_context(twin) -> str:
    avg_income = (twin.income.range_min + twin.income.range_max) / 2
    return f"""Name: {twin.name}
Occupation: {twin.context.occupation}
Location: {twin.context.location}
Language: {twin.context.language.value}
Income: ₹{twin.income.range_min:,.0f} – ₹{twin.income.range_max:,.0f} ({twin.income.frequency})
Avg Income: ₹{avg_income:,.0f}
Monthly Expenses: ₹{twin.expenditure.recurring_commitments + twin.expenditure.discretionary_spend:,.0f}
Total Debt: ₹{twin.debt.total_debt:,.0f}
Monthly EMI: ₹{twin.debt.monthly_emi:,.0f}
Behavioral Archetype: {twin.behavioral_archetype}
Risk Appetite: {twin.risk.risk_appetite}
Shock Resilience: {twin.risk.shock_resilience:.0%}
Disability Flags: {', '.join(twin.context.disability_flags) or 'None'}"""


def build_agent_context(
    behavior: dict,
    risk: dict,
    goal: dict,
    schemes: list,
    scenarios: list | None,
) -> str:
    parts = []

    if behavior:
        parts.append(
            f"Behavior Agent: Archetype={behavior.get('archetype')}, "
            f"Score={behavior.get('score', 0):.0%}. "
            f"Insight: {behavior.get('insight')}. "
            f"Risks: {', '.join(behavior.get('top_risks', []))}"
        )

    if risk:
        parts.append(
            f"Risk Agent: Debt trap probability={risk.get('debt_trap_probability', 0):.0%} (18mo). "
            f"{risk.get('narrative')}"
        )

    if goal:
        parts.append(f"Goal Agent: {goal.get('summary')}")

    if schemes:
        scheme_names = ", ".join(s.get("name", "") for s in schemes[:5])
        parts.append(f"Scheme Agent: Eligible for {len(schemes)} schemes including {scheme_names}")

    if scenarios:
        parts.append(
            f"Simulator: 3 paths computed. "
            f"Path A debt trap={scenarios[0].debt_trap_probability:.0%}, "
            f"Path B={scenarios[1].debt_trap_probability:.0%}, "
            f"Path C (best)={scenarios[2].debt_trap_probability:.0%}"
        )

    return "\n".join(parts) if parts else ""
