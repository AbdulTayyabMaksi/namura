from __future__ import annotations

from app.models.schemas import DigitalTwin


def compute_financial_health_score(twin: DigitalTwin) -> dict:
    avg_income = (twin.income.range_min + twin.income.range_max) / 2
    expense = twin.expenditure.recurring_commitments + twin.expenditure.discretionary_spend

    income_score = min(100, (avg_income / 50000) * 40)
    savings_rate = max(0, (avg_income - expense) / max(avg_income, 1))
    savings_score = min(30, savings_rate * 100)
    debt_ratio = twin.debt.total_debt / max(avg_income * 12, 1)
    debt_score = max(0, 20 - debt_ratio * 20)
    behavior_score = twin.behavioral_score * 10
    resilience_score = twin.risk.shock_resilience * 10

    total = round(income_score + savings_score + debt_score + behavior_score + resilience_score)

    if total >= 75:
        grade, label = "A", "Strong financial health"
    elif total >= 55:
        grade, label = "B", "Moderate — room to improve"
    elif total >= 35:
        grade, label = "C", "At risk — action needed"
    else:
        grade, label = "D", "Critical — urgent intervention"

    return {
        "score": min(100, total),
        "grade": grade,
        "label": label,
        "breakdown": {
            "income_stability": round(income_score),
            "savings_capacity": round(savings_score),
            "debt_health": round(debt_score),
            "behavior": round(behavior_score),
            "resilience": round(resilience_score),
        },
        "top_action": _top_action(twin, total),
    }


def _top_action(twin: DigitalTwin, score: int) -> str:
    if twin.debt.predatory_risk_score > 0.5:
        return "Avoid new high-interest loans and build ₹100/day emergency fund"
    if score < 40:
        return "Start tracking daily expenses and apply for PMJDY if no bank account"
    if twin.income.variability_index > 0.5:
        return "Set aside 20% of income on every payment day before spending"
    return "Continue current habits and explore government schemes for extra benefits"
