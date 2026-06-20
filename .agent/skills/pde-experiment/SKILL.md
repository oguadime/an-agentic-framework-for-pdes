---
name: pde-experiment
description: |
  Use this skill when the user asks to run, analyze, compare, plot, or explain numerical PDE experiments.
  Trigger on requests involving heat equation, wave equation, advection equation, diffusion, finite differences, stability, convergence, exact solution comparison, or relative L2 error.
  Do NOT use for general coding questions, unrelated machine learning tasks, or arbitrary shell execution.
---

# PDE Experiment Skill

When a user asks for a numerical PDE experiment:

1. Identify the PDE, domain, boundary conditions, initial condition, numerical method, and final time.
2. If the request is missing critical parameters, use safe defaults only for the MVP PDEs:
   - heat: `alpha=1`, `nx=101`, `dt=1e-5`, `T=0.01`
   - wave: `c=1`, `nx=201`, `dt=0.0025`, `T=0.25`
   - advection: `c=1`, `nx=200`, `dt=0.002`, `T=0.2`
3. Prefer controlled tools from `pde_tools` or the MCP server. Never create and run arbitrary user code.
4. Check the stability condition before running the solver.
5. Run the experiment.
6. Report:
   - PDE
   - numerical method
   - parameters
   - stability condition
   - relative L2 error
   - plot path
   - short scientific interpretation
7. If the computation is unstable or outside the allowed policy bounds, reject it and suggest safer parameters.
