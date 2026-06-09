"""Core backend tests for ArthSaathi 2.0."""
from __future__ import annotations

import pytest

from app.agents.guard import guard_response
from app.agents.orchestrator import classify_intent
from app.data.personas import PERSONAS
from app.data.schemes_db import SCHEMES, get_eligible_schemes
from app.services.health_score import compute_financial_health_score
from app.services.market_data import _extract_tickers, is_market_query
from app.services.mandi_prices import is_mandi_query, fetch_mandi_context
from app.simulation.monte_carlo import generate_scenarios


def test_scheme_count_meets_blueprint():
    assert len(SCHEMES) >= 50


def test_personas_loaded():
    assert len(PERSONAS) == 4
    assert "rajesh" in PERSONAS
    assert "kisan" in PERSONAS


def test_market_query_detection():
    assert is_market_query("What is TCS stock price?")
    assert not is_market_query("What is my debt risk?")


def test_mandi_query_detection():
    assert is_mandi_query("What is wheat mandi price today?")
    ctx = fetch_mandi_context("wheat price in mandi")
    assert "Wheat" in ctx


def test_mrf_ticker_extraction():
    tickers = _extract_tickers("Compare MRF vs TCS stocks")
    assert any("MRF" in t for t in tickers)


def test_intent_market_not_simulation():
    intent = classify_intent("Compare MRF vs TCS stocks for investing")
    assert intent["intent"] == "market"
    assert intent["run_simulation"] is False


def test_intent_loan_triggers_simulation():
    intent = classify_intent("Should I take a 50000 loan?")
    assert intent["intent"] == "decision"
    assert intent["run_simulation"] is True


def test_guard_allows_educational_stock_content():
    result = guard_response("Reliance is trading at INR 1269. The P/E ratio is 21.")
    assert "educational information" in result["content"].lower()
    assert result["approved"]


def test_guard_softens_direct_advice():
    result = guard_response("You should definitely buy this stock now.")
    assert "SEBI" in result["content"] or "educational" in result["content"].lower()


def test_health_score_range():
    twin = PERSONAS["priya"]
    score = compute_financial_health_score(twin)
    assert 0 <= score["score"] <= 100
    assert score["grade"] in ("A", "B", "C", "D")


def test_monte_carlo_generates_three_scenarios():
    twin = PERSONAS["rajesh"]
    scenarios, elapsed = generate_scenarios(twin, "loan decision")
    assert len(scenarios) == 3
    assert elapsed >= 0
    assert scenarios[0].debt_trap_probability >= scenarios[2].debt_trap_probability


def test_scheme_eligibility_kisan():
    schemes = get_eligible_schemes(PERSONAS["kisan"])
    names = [s["name"] for s in schemes]
    assert any("PM-KISAN" in n or "Kisan" in n for n in names)


def test_scheme_eligibility_divya_disability():
    schemes = get_eligible_schemes(PERSONAS["divya"])
    assert any(s.get("requires_disability") for s in schemes if "Disability" in s["name"] or "RPwD" in s["name"] or "Accessible" in s["name"])
