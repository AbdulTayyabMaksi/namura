from __future__ import annotations

from datetime import datetime

from app.models.schemas import DigitalTwin

NUDGE_TEMPLATES = {
    "impulsive": "Set aside ₹{amount} today before any spending — your future self will thank you.",
    "disciplined": "Great habits! Increase your SIP by ₹{amount}/month to reach goals 4 months earlier.",
    "anxious": "One small step: transfer ₹{amount} to a separate savings jar today. No big decisions needed.",
    "passive": "Enable auto-save of ₹{amount}/day — takes 2 minutes, works while you sleep.",
}


def generate_nudge(twin: DigitalTwin, behavior: dict | None = None, goal: dict | None = None) -> dict:
    archetype = twin.behavioral_archetype
    avg_income = (twin.income.range_min + twin.income.range_max) / 2

    if avg_income < 20000:
        amount = 50
    elif avg_income < 40000:
        amount = 120
    else:
        amount = 200

    template = NUDGE_TEMPLATES.get(archetype, NUDGE_TEMPLATES["passive"])
    message = template.format(amount=amount)

    action = f"Open your UPI app → Set daily auto-debit of ₹{amount} to savings"
    timing = "Best sent day after income credit"

    return {
        "id": f"nudge-{datetime.utcnow().strftime('%Y%m%d')}",
        "message": message,
        "amount": amount,
        "action": action,
        "timing": timing,
        "archetype": archetype,
        "principle": "implementation_intention",
    }
