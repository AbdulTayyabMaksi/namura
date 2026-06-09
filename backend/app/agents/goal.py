from __future__ import annotations

from app.models.schemas import DigitalTwin


def plan_goals(twin: DigitalTwin, message: str = "") -> dict:
    all_goals = (
        twin.goals.short_term + twin.goals.medium_term + twin.goals.long_term
    )
    avg_income = (twin.income.range_min + twin.income.range_max) / 2
    monthly_savings_capacity = max(0, avg_income * 0.15 - twin.debt.monthly_emi)

    milestones = []
    for goal in all_goals:
        target = goal.get("target", 0)
        deadline = goal.get("deadline", "unknown")
        months = _parse_deadline(deadline)
        monthly_needed = target / max(months, 1)
        achievable = monthly_needed <= monthly_savings_capacity * 1.5

        milestones.append({
            "name": goal.get("name", "Goal"),
            "target": target,
            "monthly_needed": round(monthly_needed),
            "achievable": achievable,
            "probability": 0.78 if achievable else 0.25,
            "alternative": (
                f"Extend deadline by {int(months * 0.5)} months"
                if not achievable
                else "On track with current savings rate"
            ),
        })

    if not milestones:
        milestones.append({
            "name": "Emergency Fund",
            "target": avg_income * 3,
            "monthly_needed": round(avg_income * 0.1),
            "achievable": True,
            "probability": 0.65,
            "alternative": "Start with ₹100/day for 6 months",
        })

    return {
        "milestones": milestones,
        "monthly_savings_capacity": round(monthly_savings_capacity),
        "summary": (
            f"You have {len(milestones)} active goal(s). "
            f"Monthly savings capacity: ₹{monthly_savings_capacity:,.0f}. "
            + (
                f"Primary goal '{milestones[0]['name']}' is "
                f"{'on track' if milestones[0]['achievable'] else 'needs adjustment'}."
            )
        ),
    }


def _parse_deadline(deadline: str) -> int:
    deadline = deadline.lower()
    if "month" in deadline:
        try:
            return int("".join(c for c in deadline.split()[0] if c.isdigit()) or "12")
        except ValueError:
            return 12
    if "year" in deadline:
        try:
            years = int("".join(c for c in deadline if c.isdigit()) or "1")
            return years * 12
        except ValueError:
            return 12
    return 24
