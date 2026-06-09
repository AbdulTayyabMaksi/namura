from __future__ import annotations

from app.models.schemas import DigitalTwin
from app.simulation.monte_carlo import run_monte_carlo, _avg_income


def assess_risk(twin: DigitalTwin) -> dict:
    income = _avg_income(twin)
    expense = twin.expenditure.recurring_commitments + twin.expenditure.discretionary_spend * 0.6

    result_18 = run_monte_carlo(
        income_mean=income,
        income_std=income * twin.income.variability_index,
        monthly_expense=expense,
        debt=twin.debt.total_debt,
        monthly_emi=twin.debt.monthly_emi,
        months=18,
    )

    result_36 = run_monte_carlo(
        income_mean=income,
        income_std=income * twin.income.variability_index,
        monthly_expense=expense,
        debt=twin.debt.total_debt,
        monthly_emi=twin.debt.monthly_emi,
        months=36,
    )

    if result_18["debt_trap_probability"] > 0.6:
        narrative = "High risk — immediate action recommended to avoid debt spiral."
    elif result_18["debt_trap_probability"] > 0.3:
        narrative = "Moderate risk — small changes now can prevent future problems."
    else:
        narrative = "Low risk trajectory — focus on building wealth and achieving goals."

    return {
        "debt_trap_probability": result_18["debt_trap_probability"],
        "debt_trap_36m": result_36["debt_trap_probability"],
        "income_shock_resilience": twin.risk.shock_resilience,
        "fraud_vulnerability": twin.risk.fraud_vulnerability,
        "narrative": narrative,
        "early_warnings": _early_warnings(twin, result_18),
    }


def _early_warnings(twin: DigitalTwin, result: dict) -> list[str]:
    warnings = []
    if result["debt_trap_probability"] > 0.5:
        warnings.append("⚠️ Debt trap risk exceeds 50% — consider debt restructuring")
    if twin.debt.predatory_risk_score > 0.5:
        warnings.append("⚠️ Predatory loan exposure detected — avoid new high-interest loans")
    if twin.risk.shock_resilience < 0.4:
        warnings.append("⚠️ Low financial shock resilience — build emergency fund urgently")
    return warnings
