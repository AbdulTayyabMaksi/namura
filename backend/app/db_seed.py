from __future__ import annotations

from sqlalchemy.orm import Session

from app.data.personas import PERSONAS
from app.data.schemes_db import SCHEMES
from app.models.db_models import DigitalTwinRecord, GovernmentSchemeRecord, TwinHistoryRecord


def seed_database(db: Session) -> None:
    _seed_personas(db)
    _seed_schemes(db)
    db.commit()


def _seed_personas(db: Session) -> None:
    for user_id, twin in PERSONAS.items():
        existing = db.get(DigitalTwinRecord, user_id)
        if existing:
            continue
        profile = twin.model_dump(mode="json")
        record = DigitalTwinRecord(
            user_id=user_id,
            profile=profile,
            version=twin.version,
        )
        db.add(record)
        db.add(
            TwinHistoryRecord(
                user_id=user_id,
                profile=profile,
                version=twin.version,
            )
        )


def _seed_schemes(db: Session) -> None:
    for scheme in SCHEMES:
        if db.get(GovernmentSchemeRecord, scheme["id"]):
            continue
        db.add(
            GovernmentSchemeRecord(
                id=scheme["id"],
                name=scheme["name"],
                data=scheme,
            )
        )
