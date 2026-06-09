from __future__ import annotations

from datetime import datetime, timedelta
import hashlib
import uuid

from sqlalchemy.orm import Session

from app.data.schemes_db import get_eligible_schemes
from app.models.db_models import (
    ChatMessageRecord,
    DigitalTwinRecord,
    GovernmentSchemeRecord,
    NudgeFeedbackRecord,
    SimulationCacheRecord,
    TwinHistoryRecord,
)
from app.models.schemas import (
    ContextualProfile,
    DigitalTwin,
    IncomeProfile,
    OnboardingRequest,
)


def _record_to_twin(record: DigitalTwinRecord) -> DigitalTwin:
    return DigitalTwin(**record.profile)


class TwinStore:
    def get(self, db: Session, user_id: str) -> DigitalTwin | None:
        record = db.get(DigitalTwinRecord, user_id)
        return _record_to_twin(record) if record else None

    def list_all(self, db: Session) -> list[DigitalTwin]:
        records = db.query(DigitalTwinRecord).all()
        return [_record_to_twin(r) for r in records]

    def create_from_onboarding(self, db: Session, req: OnboardingRequest) -> DigitalTwin:
        user_id = req.persona_id.value if req.persona_id else str(uuid.uuid4())[:8]
        twin = DigitalTwin(
            user_id=user_id,
            persona_id=req.persona_id,
            name=req.name,
            income=IncomeProfile(
                sources=[req.occupation],
                frequency=req.income_frequency,
                range_min=req.income_min,
                range_max=req.income_max,
                variability_index=0.3,
            ),
            context=ContextualProfile(
                location=req.location,
                language=req.language,
                occupation=req.occupation,
            ),
        )
        profile = twin.model_dump(mode="json")
        record = DigitalTwinRecord(user_id=user_id, profile=profile, version=1)
        db.add(record)
        db.add(TwinHistoryRecord(user_id=user_id, profile=profile, version=1))
        db.commit()
        db.refresh(record)
        return twin

    def update(self, db: Session, user_id: str, updates: dict) -> DigitalTwin | None:
        record = db.get(DigitalTwinRecord, user_id)
        if not record:
            return None

        twin = _record_to_twin(record)
        data = twin.model_dump(mode="json")
        for key, val in updates.items():
            if key in data and val is not None:
                data[key] = val
        data["version"] = record.version + 1
        data["updated_at"] = datetime.utcnow().isoformat()

        record.profile = data
        record.version = data["version"]
        record.updated_at = datetime.utcnow()
        db.add(TwinHistoryRecord(user_id=user_id, profile=data, version=record.version))
        db.commit()
        db.refresh(record)
        return _record_to_twin(record)

    def delete(self, db: Session, user_id: str) -> bool:
        record = db.get(DigitalTwinRecord, user_id)
        if not record:
            return False
        db.delete(record)
        db.commit()
        return True

    def get_history(self, db: Session, user_id: str) -> list[DigitalTwin]:
        records = (
            db.query(TwinHistoryRecord)
            .filter(TwinHistoryRecord.user_id == user_id)
            .order_by(TwinHistoryRecord.version)
            .all()
        )
        return [DigitalTwin(**r.profile) for r in records]

    def save_chat_message(
        self,
        db: Session,
        user_id: str,
        role: str,
        content: str,
        metadata: dict | None = None,
    ) -> None:
        db.add(
            ChatMessageRecord(
                user_id=user_id,
                role=role,
                content=content,
                metadata_=metadata,
            )
        )
        db.commit()

    def get_chat_history(self, db: Session, user_id: str, limit: int = 50) -> list[dict]:
        records = (
            db.query(ChatMessageRecord)
            .filter(ChatMessageRecord.user_id == user_id)
            .order_by(ChatMessageRecord.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "role": r.role,
                "content": r.content,
                "metadata": r.metadata_,
                "created_at": r.created_at.isoformat(),
            }
            for r in reversed(records)
        ]

    def has_nudge_today(self, db: Session, user_id: str) -> bool:
        since = datetime.utcnow() - timedelta(hours=24)
        recent = (
            db.query(ChatMessageRecord)
            .filter(
                ChatMessageRecord.user_id == user_id,
                ChatMessageRecord.role == "assistant",
                ChatMessageRecord.created_at >= since,
            )
            .all()
        )
        for r in recent:
            if r.metadata_ and r.metadata_.get("has_nudge"):
                return True
        return False

    def save_nudge_feedback(
        self, db: Session, user_id: str, nudge_id: str, action: str
    ) -> None:
        db.add(
            NudgeFeedbackRecord(user_id=user_id, nudge_id=nudge_id, action=action)
        )
        db.commit()

    def get_schemes_from_db(self, db: Session, twin: DigitalTwin) -> list[dict]:
        all_schemes = db.query(GovernmentSchemeRecord).all()
        if not all_schemes:
            return get_eligible_schemes(twin)
        eligible_ids = {s["id"] for s in get_eligible_schemes(twin)}
        return [s.data for s in all_schemes if s.id in eligible_ids]

    def get_cached_simulation(
        self, db: Session, user_id: str, question: str
    ) -> dict | None:
        qhash = hashlib.sha256(question.encode()).hexdigest()[:16]
        record = (
            db.query(SimulationCacheRecord)
            .filter(
                SimulationCacheRecord.user_id == user_id,
                SimulationCacheRecord.question_hash == qhash,
            )
            .order_by(SimulationCacheRecord.created_at.desc())
            .first()
        )
        return record.result if record else None

    def cache_simulation(
        self, db: Session, user_id: str, question: str, result: dict
    ) -> None:
        qhash = hashlib.sha256(question.encode()).hexdigest()[:16]
        db.add(
            SimulationCacheRecord(
                user_id=user_id,
                question_hash=qhash,
                result=result,
            )
        )
        db.commit()


twin_store = TwinStore()
