from __future__ import annotations

from typing import Any

from google.adk.agents.llm_agent import Agent

from pde_tools.solvers import run_pde_experiment

MODEL = "gemini-flash-latest"


def run_heat_equation(alpha: float = 1.0, nx: int = 101, dt: float = 1e-5, T: float = 0.01) -> dict[str, Any]:
    "Run a verified 1D heat equation experiment and return plot/error/report artifacts."
    return run_pde_experiment("heat", alpha=alpha, nx=nx, dt=dt, T=T)


def run_wave_equation(c: float = 1.0, nx: int = 201, dt: float = 0.0025, T: float = 0.25) -> dict[str, Any]:
    "Run a verified 1D wave equation experiment and return plot/error/report artifacts."
    return run_pde_experiment("wave", c=c, nx=nx, dt=dt, T=T)


def run_advection_equation(c: float = 1.0, nx: int = 200, dt: float = 0.002, T: float = 0.2) -> dict[str, Any]:
    "Run a verified 1D linear advection experiment and return plot/error/report artifacts."
    return run_pde_experiment("advection", c=c, nx=nx, dt=dt, T=T)


planner_agent = Agent(
    name="pde_planner_agent",
    model=MODEL,
    description="Plans safe numerical PDE experiments from user requests.",
    instruction="""
You are the planner for a numerical PDE experiment system.
Identify the PDE, parameters, method, boundary conditions, and exact solution comparison.
Current MVP supports heat, wave, and linear advection equations.
If information is missing, choose the documented MVP defaults and state them.
Do not propose arbitrary code execution.
""",
)

solver_agent = Agent(
    name="pde_solver_agent",
    model=MODEL,
    description="Runs controlled PDE solver tools.",
    instruction="""
You are the solver agent.
Use only the provided solver tools. Do not write or execute arbitrary code.
Before calling a tool, verify that the parameters are within the supported MVP scope.
After running the tool, return the plot path, report path, and relative L2 error.
""",
    tools=[run_heat_equation, run_wave_equation, run_advection_equation],
)

evaluator_agent = Agent(
    name="pde_evaluator_agent",
    model=MODEL,
    description="Evaluates PDE experiment stability, error, and scientific interpretation.",
    instruction="""
You are the evaluator agent.
Check the reported stability condition, relative L2 error, and whether the method matches the PDE.
For heat and wave experiments, an MVP relative L2 error below 1e-3 is strong.
For advection, an MVP relative L2 error below 3e-2 is acceptable because the first-order upwind method is diffusive.
Explain any instability or large error clearly.
""",
)

root_agent = Agent(
    name="numerical_pde_orchestrator",
    model=MODEL,
    description="A multi-agent numerical PDE experiment assistant.",
    instruction="""
You orchestrate a numerical PDE experiment workflow.

Workflow:
1. Delegate planning to the planner agent.
2. Use the solver agent and its controlled tools to run the experiment.
3. Delegate quality assessment to the evaluator agent.
4. Return a concise report with PDE, method, parameters, stability condition, relative L2 error, plot path, and interpretation.

Never run arbitrary user code. If the user requests an unsupported PDE, explain that the current MVP supports heat, wave, and advection.
""",
    sub_agents=[planner_agent, solver_agent, evaluator_agent],
)
