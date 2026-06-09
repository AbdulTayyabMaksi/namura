from __future__ import annotations

import time
from typing import Any

import numpy as np

from app.models.schemas import DigitalTwin, ScenarioBranch


def _avg_income(twin: DigitalTwin) -> float:
    return (twin.income.range_min + twin.income.range_max) / 2


def run_monte_carlo(
    income_mean: float,
    income_std: float,
    monthly_expense: float,
    debt: float,
    monthly_emi: float,
    months: int,
    n_simulations: int = 1000,
    daily_save: float = 0,
    extra_emi: float = 0,
) -> dict[str, Any]:
    rng = np.random.default_rng(42)
    savings = np.zeros(n_simulations)
    debt_remaining = np.full(n_simulations, debt)
    debt_trap_count = 0

    for _ in range(months):
        income = rng.normal(income_mean, income_std, n_simulations)
        income = np.maximum(income, income_mean * 0.3)
        net = income - monthly_expense - monthly_emi - extra_emi + daily_save * 30

        broke = (savings + net) < 0
        debt_trap_count += int(np.sum(broke & (debt_remaining > 0)))

        savings = savings + net
        debt_remaining = np.maximum(debt_remaining - np.maximum(net * 0.3, 0), 0)

    debt_trap_prob = min(0.95, debt_trap_count / (n_simulations * months) * 12)

    return {
        "savings_mean": float(np.mean(savings)),
        "savings_p25": float(np.percentile(savings, 25)),
        "savings_p75": float(np.percentile(savings, 75)),
        "debt_trap_probability": round(debt_trap_prob, 2),
        "trajectory": [
            float(np.mean(savings) * (i + 1) / months) for i in range(min(months, 12))
        ],
    }


def generate_scenarios(twin: DigitalTwin, question: str = "") -> tuple[list[ScenarioBranch], int]:
    start = time.time()
    income = _avg_income(twin)
    income_std = income * twin.income.variability_index
    expense = twin.expenditure.recurring_commitments + twin.expenditure.discretionary_spend * 0.6
    debt = twin.debt.total_debt
    emi = twin.debt.monthly_emi

    pessimistic = run_monte_carlo(
        income_mean=income * 0.85,
        income_std=income_std * 1.2,
        monthly_expense=expense * 1.1,
        debt=debt + 50000,
        monthly_emi=emi + 4200,
        months=36,
        daily_save=0,
    )

    status_quo = run_monte_carlo(
        income_mean=income,
        income_std=income_std,
        monthly_expense=expense,
        debt=debt,
        monthly_emi=emi,
        months=36,
        daily_save=0,
    )

    optimistic = run_monte_carlo(
        income_mean=income * 1.05,
        income_std=income_std * 0.8,
        monthly_expense=expense * 0.95,
        debt=max(0, debt - 20000),
        monthly_emi=max(0, emi - 500),
        months=36,
        daily_save=120,
    )

    scenarios = [
        ScenarioBranch(
            label="Path A — Risky Choice",
            path_type="pessimistic",
            description="Taking a high-interest loan or continuing risky spending",
            month_6={
                "savings": max(0, pessimistic["savings_mean"] * 0.15),
                "debt_burden": debt + 25000,
                "emergency_fund": 0,
                "emi_pressure": emi + 4200,
            },
            month_12={
                "savings": max(0, pessimistic["savings_mean"] * 0.3),
                "debt_trap_probability": pessimistic["debt_trap_probability"],
                "net_worth": pessimistic["savings_mean"] - debt,
            },
            month_36={
                "savings": pessimistic["savings_mean"],
                "debt_trap_probability": min(0.95, pessimistic["debt_trap_probability"] + 0.15),
                "goal_probability": 0.12,
            },
            debt_trap_probability=pessimistic["debt_trap_probability"],
            savings_trajectory=pessimistic["trajectory"],
            goal_impact="Goals likely delayed by 3+ years",
            nudge_action="Avoid this loan. See Path C for a safer alternative.",
            color="#ef4444",
        ),
        ScenarioBranch(
            label="Path B — Continue As-Is",
            path_type="status_quo",
            description="No changes to current financial habits",
            month_6={
                "savings": max(0, status_quo["savings_mean"] * 0.2),
                "debt_burden": debt,
                "emergency_fund": max(0, status_quo["savings_mean"] * 0.1),
            },
            month_12={
                "savings": status_quo["savings_mean"] * 0.4,
                "debt_trap_probability": status_quo["debt_trap_probability"],
                "net_worth": status_quo["savings_mean"] - debt,
            },
            month_36={
                "savings": status_quo["savings_mean"],
                "debt_trap_probability": status_quo["debt_trap_probability"],
                "goal_probability": 0.35,
            },
            debt_trap_probability=status_quo["debt_trap_probability"],
            savings_trajectory=status_quo["trajectory"],
            goal_impact="Slow progress — goals achievable but delayed",
            nudge_action="You need a plan. Small daily changes can shift your trajectory.",
            color="#eab308",
        ),
        ScenarioBranch(
            label="Path C — Smart Change",
            path_type="optimistic",
            description="Save ₹120/day, avoid predatory loans, build emergency fund",
            month_6={
                "savings": optimistic["savings_mean"] * 0.25,
                "debt_burden": max(0, debt - 10000),
                "emergency_fund": 21600,
            },
            month_12={
                "savings": optimistic["savings_mean"] * 0.5,
                "debt_trap_probability": optimistic["debt_trap_probability"],
                "net_worth": optimistic["savings_mean"],
            },
            month_36={
                "savings": optimistic["savings_mean"],
                "debt_trap_probability": optimistic["debt_trap_probability"],
                "goal_probability": 0.78,
            },
            debt_trap_probability=optimistic["debt_trap_probability"],
            savings_trajectory=optimistic["trajectory"],
            goal_impact="Goals on track — emergency fund built in 6 months",
            nudge_action="Start ₹120/day auto-save. Takes 2 minutes to set up.",
            color="#22c55e",
        ),
    ]

    elapsed = int((time.time() - start) * 1000)
    return scenarios, elapsed
