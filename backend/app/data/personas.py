from app.models.schemas import (
    ContextualProfile,
    DebtProfile,
    DigitalTwin,
    ExpenditureProfile,
    GoalProfile,
    IncomeProfile,
    Language,
    PersonaId,
    RiskProfile,
)

PERSONAS: dict[str, DigitalTwin] = {
    "priya": DigitalTwin(
        user_id="priya",
        persona_id=PersonaId.PRIYA,
        name="Priya Sharma",
        income=IncomeProfile(
            sources=["Teaching salary"],
            frequency="monthly",
            range_min=32000,
            range_max=38000,
            variability_index=0.1,
            historical=[35000, 35500, 34800, 35200, 35000],
        ),
        expenditure=ExpenditureProfile(
            categories={"rent": 12000, "groceries": 5000, "transport": 2000, "utilities": 1500},
            recurring_commitments=20500,
            discretionary_spend=8000,
        ),
        debt=DebtProfile(loans=[], total_debt=0, predatory_risk_score=0.1),
        goals=GoalProfile(
            short_term=[{"name": "Emergency fund", "target": 100000, "deadline": "12 months"}],
            medium_term=[{"name": "Child education", "target": 500000, "deadline": "5 years"}],
        ),
        risk=RiskProfile(risk_appetite="conservative", shock_resilience=0.6),
        context=ContextualProfile(
            location="Thane, Maharashtra",
            language=Language.MARATHI,
            occupation="School Teacher",
            literacy_level="high",
        ),
        behavioral_archetype="anxious",
        behavioral_score=0.65,
    ),
    "rajesh": DigitalTwin(
        user_id="rajesh",
        persona_id=PersonaId.RAJESH,
        name="Rajesh Kumar",
        income=IncomeProfile(
            sources=["Gig delivery", "Part-time driving"],
            frequency="daily",
            range_min=15000,
            range_max=40000,
            variability_index=0.75,
            historical=[22000, 18000, 35000, 15000, 28000, 32000, 16000],
        ),
        expenditure=ExpenditureProfile(
            categories={"rent": 8000, "food": 6000, "fuel": 4000, "family": 5000},
            recurring_commitments=8000,
            discretionary_spend=12000,
            impulse_triggers=["festival spending", "loan app ads"],
        ),
        debt=DebtProfile(
            loans=[{"type": "personal", "amount": 25000, "rate": 24, "emi": 2800}],
            total_debt=25000,
            predatory_risk_score=0.68,
            monthly_emi=2800,
        ),
        goals=GoalProfile(
            short_term=[{"name": "Emergency fund", "target": 30000, "deadline": "6 months"}],
        ),
        risk=RiskProfile(risk_appetite="low", fraud_vulnerability=0.7, shock_resilience=0.25),
        context=ContextualProfile(
            location="Mumbai, Maharashtra",
            language=Language.HINDI,
            occupation="Gig Worker",
            literacy_level="medium",
        ),
        behavioral_archetype="impulsive",
        behavioral_score=0.35,
    ),
    "kisan": DigitalTwin(
        user_id="kisan",
        persona_id=PersonaId.KISAN,
        name="Ramesh Gowda",
        income=IncomeProfile(
            sources=["Crop sales", "Dairy"],
            frequency="seasonal",
            range_min=8000,
            range_max=45000,
            variability_index=0.9,
            historical=[12000, 8000, 42000, 15000, 38000, 10000],
        ),
        expenditure=ExpenditureProfile(
            categories={"seeds": 15000, "fertilizer": 12000, "labour": 20000, "family": 8000},
            recurring_commitments=5000,
            discretionary_spend=3000,
        ),
        debt=DebtProfile(
            loans=[{"type": "informal", "amount": 50000, "rate": 36, "emi": 0}],
            total_debt=50000,
            predatory_risk_score=0.55,
        ),
        goals=GoalProfile(
            medium_term=[{"name": "Irrigation pump", "target": 80000, "deadline": "2 years"}],
        ),
        risk=RiskProfile(risk_appetite="very_low", shock_resilience=0.3),
        context=ContextualProfile(
            location="Mandya, Karnataka",
            language=Language.KANNADA,
            occupation="Farmer (3 acres)",
            literacy_level="low",
            seasonal_calendar=["Kharif: Jun-Oct", "Rabi: Nov-Mar"],
        ),
        behavioral_archetype="passive",
        behavioral_score=0.45,
    ),
    "divya": DigitalTwin(
        user_id="divya",
        persona_id=PersonaId.DIVYA,
        name="Divya Patil",
        income=IncomeProfile(
            sources=["Government job"],
            frequency="monthly",
            range_min=23000,
            range_max=27000,
            variability_index=0.05,
            historical=[25000, 25200, 24800, 25000],
        ),
        expenditure=ExpenditureProfile(
            categories={"rent": 6000, "groceries": 4000, "transport": 1500, "medical": 2000},
            recurring_commitments=13500,
            discretionary_spend=5000,
        ),
        debt=DebtProfile(loans=[], total_debt=0),
        goals=GoalProfile(
            long_term=[{"name": "Own home", "target": 2000000, "deadline": "15 years"}],
        ),
        risk=RiskProfile(risk_appetite="moderate", shock_resilience=0.55),
        context=ContextualProfile(
            location="Pune, Maharashtra",
            language=Language.MARATHI,
            occupation="Clerk",
            literacy_level="high",
            disability_flags=["visual_impairment"],
        ),
        behavioral_archetype="disciplined",
        behavioral_score=0.78,
    ),
}


def get_persona(user_id: str) -> DigitalTwin | None:
    return PERSONAS.get(user_id)
