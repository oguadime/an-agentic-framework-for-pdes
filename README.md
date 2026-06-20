# Numerical PDE Experiment Agent

A capstone project for Kaggle's **AI Agents: Intensive Vibe Coding Capstone Project (2026)**.

This project builds a small but production-minded AI agent system for running verified numerical PDE experiments. It is designed for the **Freestyle** track, with a real-world scientific-computing use case.

## What it does

The agent takes a natural-language PDE experiment request, plans the experiment, runs a controlled solver, checks stability and error, saves a plot/report, and explains the result.

Current supported PDEs:

- 1D heat equation with zero Dirichlet boundary conditions
- 1D wave equation with zero Dirichlet boundary conditions
- 1D linear advection equation with periodic boundary conditions

The MVP is deliberately scoped to PDEs with known exact solutions, so the system can evaluate numerical error.

## Course concepts demonstrated

1. **Agent / multi-agent design**
   - Offline deterministic agent workflow in `agents/offline_agents.py`
   - ADK-compatible multi-agent definition in `agents/numerical_pde_agent/agent.py`
   - Planner, solver, evaluator, and reporter responsibilities are separated.

2. **MCP server**
   - `mcp_server/pde_mcp_server.py` exposes `run_pde_experiment` as a controlled tool.

3. **Agent skill**
   - `.agent/skills/pde-experiment/SKILL.md` teaches the agent how to run PDE experiments.

4. **Security and evaluation**
   - No arbitrary code execution.
   - Strict policy checks in `pde_tools/policy.py`.
   - Stability conditions are enforced before simulation.
   - Unit tests in `evals/test_pde_solvers.py`.

5. **Spec-driven development**
   - The implementation follows `specs/pde_agent_mvp.md`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python demo.py
pytest -q
```

Expected result:

- terminal report with relative L2 errors
- plots in `outputs/`
- markdown reports in `outputs/`

## ADK setup

The deterministic demo does not require an API key. To run the ADK agent, install dependencies and set your Gemini API key:

```bash
pip install google-adk
cp .env.example .env
# edit .env and add your GOOGLE_API_KEY
```

Then run from the parent directory that contains the `agents/` folder:

```bash
adk run numerical_pde_agent
```

or

```bash
adk web --port 8000
```

Depending on your local ADK version, you may need to run this from inside the `agents/` directory:

```bash
cd agents
adk run numerical_pde_agent
```

## MCP server

Install MCP extras:

```bash
pip install "mcp[cli]"
```

Run the local MCP server:

```bash
python mcp_server/pde_mcp_server.py
```

The server exposes a controlled `run_pde_experiment` tool. The tool does not run arbitrary user code. It only dispatches to vetted solver functions.

## Example prompts

```text
Run a heat equation experiment with alpha=1, nx=101, dt=1e-5, T=0.01.
```

```text
Run a wave equation experiment with c=1, nx=201, dt=0.0025, T=0.25.
```

```text
Run an advection experiment with c=1, nx=200, dt=0.002, T=0.2.
```

## Repository structure

```text
numerical-pde-agent/
├── README.md
├── requirements.txt
├── .env.example
├── specs/
│   └── pde_agent_mvp.md
├── .agents/
│   └── AGENTS.md
├── .agent/
│   └── skills/
│       └── pde-experiment/
│           └── SKILL.md
├── pde_tools/
│   ├── __init__.py
│   ├── solvers.py
│   ├── policy.py
│   └── report.py
├── agents/
│   ├── offline_agents.py
│   └── numerical_pde_agent/
│       ├── __init__.py
│       └── agent.py
├── mcp_server/
│   └── pde_mcp_server.py
├── evals/
│   └── test_pde_solvers.py
├── docs/
│   ├── AgenticPDE.png
│   └── local_run_results.txt
├── outputs/
│   └── .gitkeep
└── demo.py
```

## Safety note

This is a scientific-computing agent. The key safety choice is that the agent cannot execute arbitrary generated Python. It calls bounded, reviewed solver functions through a narrow interface. This keeps the demo useful while reducing the risk of rogue tool use.
