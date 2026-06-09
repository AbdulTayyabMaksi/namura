from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    MARATHI = "mr"
    KANNADA = "kn"
    TAMIL = "ta"
    TELUGU = "te"
    BENGALI = "bn"
    GUJARATI = "gu"
    PUNJABI = "pa"
    MALAYALAM = "ml"


class PersonaId(str, Enum):
    PRIYA = "priya"
    RAJESH = "rajesh"
    KISAN = "kisan"
    DIVYA = "divya"


class IncomeProfile(BaseModel):
    sources: list[str] = []
    frequency: str = "monthly"
    range_min: float = 0
    range_max: float = 0
    variability_index: float = 0.3
    historical: list[float] = []


class ExpenditureProfile(BaseModel):
    categories: dict[str, float] = {}
    recurring_commitments: float = 0
    discretionary_spend: float = 0
    impulse_triggers: list[str] = []


class DebtProfile(BaseModel):
    loans: list[dict[str, Any]] = []
    total_debt: float = 0
    predatory_risk_score: float = 0
    monthly_emi: float = 0


class GoalProfile(BaseModel):
    short_term: list[dict[str, Any]] = []
    medium_term: list[dict[str, Any]] = []
    long_term: list[dict[str, Any]] = []


class RiskProfile(BaseModel):
    risk_appetite: str = "moderate"
    fraud_vulnerability: float = 0.3
    insurance_gaps: list[str] = []
    shock_resilience: float = 0.5


class ContextualProfile(BaseModel):
    location: str = ""
    language: Language = Language.ENGLISH
    literacy_level: str = "medium"
    disability_flags: list[str] = []
    occupation: str = ""
    seasonal_calendar: list[str] = []


class DigitalTwin(BaseModel):
    user_id: str
    persona_id: Optional[PersonaId] = None
    name: str = ""
    income: IncomeProfile = Field(default_factory=IncomeProfile)
    expenditure: ExpenditureProfile = Field(default_factory=ExpenditureProfile)
    debt: DebtProfile = Field(default_factory=DebtProfile)
    goals: GoalProfile = Field(default_factory=GoalProfile)
    risk: RiskProfile = Field(default_factory=RiskProfile)
    context: ContextualProfile = Field(default_factory=ContextualProfile)
    behavioral_archetype: str = "passive"
    behavioral_score: float = 0.5
    version: int = 1
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    user_id: str
    message: str
    language: Language = Language.ENGLISH
    voice_mode: bool = False
    low_data_mode: bool = False


class AgentOutput(BaseModel):
    agent_id: str
    content: str
    confidence: float = 0.85
    citations: list[str] = []
    warnings: list[str] = []


class ScenarioBranch(BaseModel):
    label: str
    path_type: str
    description: str
    month_6: dict[str, Any]
    month_12: dict[str, Any]
    month_36: dict[str, Any]
    debt_trap_probability: float
    savings_trajectory: list[float]
    goal_impact: str
    nudge_action: str
    color: str


class ChatResponse(BaseModel):
    message: str
    agents_used: list[str] = []
    scenarios: Optional[list[ScenarioBranch]] = None
    nudge: Optional[dict[str, Any]] = None
    schemes: Optional[list[dict[str, Any]]] = None
    disclaimer: str = "This is educational information, not regulated financial advice."
    audio_summary: Optional[str] = None


class SimulateRequest(BaseModel):
    user_id: str
    question: str
    horizon_months: int = 36


class SimulateResponse(BaseModel):
    scenarios: list[ScenarioBranch]
    computation_ms: int


class SchemeItem(BaseModel):
    id: str
    name: str
    benefit_amount: str
    eligibility: str
    application_link: str
    difficulty: int
    steps: list[str]
    estimated_value: float


class NudgeFeedback(BaseModel):
    user_id: str
    nudge_id: str
    action: str


class OnboardingRequest(BaseModel):
    name: str
    occupation: str
    location: str
    language: Language
    income_min: float
    income_max: float
    income_frequency: str
    persona_id: Optional[PersonaId] = None
