from __future__ import annotations

from app.data.schemes_db import get_eligible_schemes
from app.models.schemas import DigitalTwin


def discover_schemes(twin: DigitalTwin) -> list[dict]:
    raw = get_eligible_schemes(twin)
    return [
        {
            "id": s["id"],
            "name": s["name"],
            "benefit_amount": s["benefit_amount"],
            "eligibility": s["eligibility"],
            "application_link": s["application_link"],
            "difficulty": s["difficulty"],
            "steps": s["steps"],
            "estimated_value": s["estimated_value"],
        }
        for s in raw
    ]
