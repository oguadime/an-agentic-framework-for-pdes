# Project Agent Instructions

You are working on a numerical PDE experiment agent.

Follow these rules:

1. Prefer the existing solver tools in `pde_tools/` over writing new numerical code.
2. Do not execute arbitrary user-provided Python.
3. Keep edits small and surgical.
4. Add or update tests when changing solver behavior.
5. Write outputs only to `outputs/`.
6. Always report the PDE, method, stability condition, parameters, plot path, and relative L2 error.
7. If a user asks for an unsupported PDE, ask for clarification or state that the current MVP supports heat, wave, and advection only.
