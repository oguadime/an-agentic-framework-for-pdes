# Numerical PDE Experiment Agent MVP Spec

## Goal

Build an agentic numerical PDE assistant that can run small, verified PDE experiments and explain the results.

The system should accept a user request, identify the PDE experiment, run a safe numerical solver, compute error against a known exact solution, save a plot, and generate a concise report.

## Supported PDEs

### 1D heat equation

\[
u_t = \alpha u_{xx}, \quad x \in [0,1], \quad t \in [0,T].
\]

Boundary conditions:

\[
u(0,t)=0,\quad u(1,t)=0.
\]

Initial condition:

\[
u(x,0)=\sin(\pi x).
\]

Exact solution:

\[
u(x,t)=e^{-\alpha \pi^2 t}\sin(\pi x).
\]

Numerical method:

- second-order centered finite difference in space
- explicit Euler in time

Stability condition:

\[
\Delta t \leq \frac{\Delta x^2}{2\alpha}.
\]

### 1D wave equation

\[
u_{tt}=c^2u_{xx}, \quad x\in[0,1].
\]

Boundary conditions:

\[
u(0,t)=0,\quad u(1,t)=0.
\]

Initial displacement:

\[
u(x,0)=\sin(\pi x).
\]

Initial velocity:

\[
u_t(x,0)=0.
\]

Exact solution:

\[
u(x,t)=\cos(c\pi t)\sin(\pi x).
\]

Numerical method:

- centered finite difference in space
- leapfrog / second-order centered time stepping

Stability condition:

\[
c\Delta t/\Delta x \leq 1.
\]

### 1D linear advection equation

\[
u_t + c u_x = 0, \quad x\in[0,1],
\]

with periodic boundary conditions and

\[
u(x,0)=\sin(2\pi x).
\]

Exact solution:

\[
u(x,t)=\sin(2\pi(x-ct)).
\]

Numerical method:

- first-order upwind finite difference method

Stability condition:

\[
|c|\Delta t/\Delta x \leq 1.
\]

## Agent workflow

1. Planner identifies PDE, parameters, and missing information.
2. Solver calls a controlled solver function.
3. Evaluator checks stability, relative L2 error, and numerical behavior.
4. Reporter writes a short result explanation and saves artifacts.

## Safety requirements

- The system must not execute arbitrary user-provided code.
- The system must reject unsupported PDE names.
- The system must enforce parameter bounds.
- The system must enforce stability conditions unless the code is explicitly modified by a developer.
- Outputs must be written only to the local `outputs/` directory.

## Success criteria

- `python demo.py` completes successfully.
- `pytest -q` passes.
- The heat equation error is below `1e-3`.
- The wave equation error is below `1e-3` for the provided stable default.
- The advection error is below `3e-2` for the provided stable default.
- Unstable time steps are rejected.
