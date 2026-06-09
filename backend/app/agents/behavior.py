from __future__ import annotations

from app.models.schemas import DigitalTwin

ARCHETYPE_INSIGHTS = {
    "impulsive": "You tend to spend during income peaks. Setting aside money on payday helps.",
    "disciplined": "Strong savings habits detected. Consider optimizing for higher returns.",
    "anxious": "Financial anxiety may lead to avoiding decisions. Small steps build confidence.",
    "passive": "Limited active financial management. Automated savings could help significantly.",
}


def analyze_behavior(twin: DigitalTwin) -> dict:
    archetype = twin.behavioral_archetype
    triggers = twin.expenditure.impulse_triggers
    variability = twin.income.variability_index

    risks = []
    if variability > 0.5:
        risks.append("High income variability makes budgeting challenging")
    if twin.debt.predatory_risk_score > 0.5:
        risks.append("Elevated exposure to predatory lending products")
    if twin.expenditure.discretionary_spend > twin.income.range_max * 0.3:
        risks.append("Discretionary spending exceeds recommended 30% threshold")

    positives = []
    if twin.behavioral_score > 0.6:
        positives.append("Consistent financial tracking behavior")
    if twin.debt.total_debt == 0:
        positives.append("Debt-free status — strong foundation")

    return {
        "archetype": archetype,
        "score": twin.behavioral_score,
        "insight": ARCHETYPE_INSIGHTS.get(archetype, "Building your financial profile."),
        "top_risks": risks[:3] or ["No major behavioral risks detected"],
        "positive_habits": positives[:2] or ["Starting your financial journey"],
        "impulse_triggers": triggers,
    }
