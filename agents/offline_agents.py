from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from pde_tools.report import format_console_report
from pde_tools.solvers import run_pde_experiment


@dataclass
class ExperimentPlan:
    pde: str
    parameters: dict[str, Any]
    rationale: str


class PlannerAgent:
    """Small deterministic planner for the offline demo.

    The ADK version in `agents/numerical_pde_agent/agent.py` uses an LLM,
    but this class lets the capstone demo run without API keys.
    """

    DEFAULTS = {
        "heat": {"alpha": 1.0, "nx": 101, "dt": 1e-5, "T": 0.01},
        "wave": {"c": 1.0, "nx": 201, "dt": 0.0025, "T": 0.25},
        "advection": {"c": 1.0, "nx": 200, "dt": 0.002, "T": 0.2},
    }

    def plan(self, user_request: str) -> ExperimentPlan:
        text = user_request.lower()

        if "wave" in text:
            pde = "wave"
        elif "advection" in text or "transport" in text:
            pde = "advection"
        else:
            pde = "heat"

        params = dict(self.DEFAULTS[pde])

        # Minimal extraction for demo purposes.
        for key in ("alpha", "c", "dt", "T", "nx"):
            pattern = rf"{key}\\s*=\\s*([0-9.eE+-]+)"
            match = re.search(pattern, user_request)
            if match:
                raw = match.group(1)
                params[key] = int(raw) if key == "nx" else float(raw)

        return ExperimentPlan(
            pde=pde,
            parameters=params,
            rationale=f"Selected the {pde} solver and safe default parameters when values were not supplied.",
        )


class SolverAgent:
    """Executes only the controlled PDE solver tool."""

    def solve(self, plan: ExperimentPlan) -> dict[str, Any]:
        return run_pde_experiment(plan.pde, **plan.parameters)


class EvaluatorAgent:
    """Evaluates numerical reliability using stability and relative L2 error."""

    def evaluate(self, result: dict[str, Any]) -> dict[str, Any]:
        err = result["relative_l2_error"]
        if result["pde"] == "advection":
            passed = err < 3e-2
        else:
            passed = err < 1e-3
        return {
            "passed": passed,
            "relative_l2_error": err,
            "message": "Evaluation passed." if passed else "Evaluation did not meet the MVP threshold.",
        }


class ReporterAgent:
    """Formats the final human-readable response."""

    def report(self, plan: ExperimentPlan, result: dict[str, Any], evaluation: dict[str, Any]) -> str:
        return (
            f"Planner rationale: {plan.rationale}\\n"
            f"Evaluation: {evaluation['message']}\\n\\n"
            + format_console_report(result)
        )


def run_offline_agent(user_request: str) -> str:
    planner = PlannerAgent()
    solver = SolverAgent()
    evaluator = EvaluatorAgent()
    reporter = ReporterAgent()

    plan = planner.plan(user_request)
    result = solver.solve(plan)
    evaluation = evaluator.evaluate(result)
    return reporter.report(plan, result, evaluation)
