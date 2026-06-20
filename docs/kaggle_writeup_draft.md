# Numerical PDE Experiment Agent

## Subtitle

A safe multi-agent scientific-computing assistant for verified finite-difference PDE experiments.

## Track

Freestyle

## Problem

Numerical PDE experiments are common in scientific computing, but they are easy to set up incorrectly. A student or researcher may choose an unstable time step, compare against no reference solution, forget boundary conditions, or generate a plot that looks plausible but is numerically wrong. This project builds an agentic assistant that helps users run small PDE experiments while enforcing stability checks and producing error metrics.

## Solution

The Numerical PDE Experiment Agent accepts natural-language requests such as:

> Run a heat equation experiment with alpha=1, nx=101, dt=1e-5, T=0.01.

The system plans the experiment, runs a controlled solver, compares the numerical result against an exact solution, saves a plot and CSV file, and produces a short scientific report. The current MVP supports:

- 1D heat equation
- 1D wave equation
- 1D linear advection equation

These PDEs were selected because they have known exact solutions, making evaluation concrete.

## Why Agents?

A single script can solve one PDE, but an agentic system can coordinate the full workflow: understand the request, select the proper solver, enforce numerical stability, generate artifacts, evaluate error, and explain the result. The agent pattern also makes the system extensible. Future agents can add convergence studies, PINN baselines, Fourier methods, or LaTeX report generation.

## Architecture

The project uses four logical agents:

1. Planner Agent: identifies the PDE, parameters, method, and defaults.
2. Solver Agent: calls controlled PDE solver tools.
3. Evaluator Agent: checks stability and relative L2 error.
4. Reporter Agent: formats the final explanation and artifacts.

The repository also includes an ADK-compatible multi-agent definition and an MCP server exposing the PDE experiment as a controlled tool.

## Course Concepts Demonstrated

1. Multi-agent system with ADK-compatible code.
2. MCP server exposing a numerical PDE experiment tool.
3. Agent skill using a `SKILL.md` workflow for PDE experiments.
4. Security guardrails through policy checks, stability enforcement, and no arbitrary code execution.
5. Evaluation through reproducible tests and exact-solution error metrics.

## Technical Implementation

The numerical core uses finite differences:

- Heat equation: explicit Euler in time and centered finite differences in space.
- Wave equation: second-order centered finite differences in time and space.
- Advection equation: first-order upwind method with periodic boundary conditions.

Each solver checks the relevant stability condition before running. The output includes a plot, CSV file, markdown report, and relative L2 error.

## Safety and Reliability

The agent does not run arbitrary user-provided Python. It only dispatches to reviewed solver functions. The policy layer rejects unsupported PDEs, out-of-range parameters, unstable time steps, and unsafe output paths. The test suite verifies error thresholds and rejection behavior.

## Results

The MVP produces small relative L2 errors for the heat and wave equations and a reasonable first-order error for the advection equation. The generated plots visually confirm agreement between numerical and exact solutions.

## How to Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo.py
pytest -q
```

## Future Work

Future extensions include convergence studies, nonlinear PDEs, spectral solvers, finite-element modules, PINN comparisons, and report export to LaTeX.
