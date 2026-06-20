from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from pde_tools.solvers import run_pde_experiment

mcp = FastMCP("Numerical PDE Experiment MCP", json_response=True)


@mcp.tool()
def run_pde_experiment_tool(
    pde: str,
    alpha: float | None = None,
    c: float | None = None,
    nx: int | None = None,
    dt: float | None = None,
    T: float | None = None,
) -> dict[str, Any]:
    """Run a controlled numerical PDE experiment.

    Supported PDE values:
    - heat
    - wave
    - advection

    This tool does not execute arbitrary Python. It dispatches only to reviewed finite-difference solvers.
    """
    params = {"alpha": alpha, "c": c, "nx": nx, "dt": dt, "T": T}
    return run_pde_experiment(pde, **params)


if __name__ == "__main__":
    # Stdio is convenient for local IDE/agent integration.
    # For production, use streamable-http behind a governed gateway.
    mcp.run(transport="stdio")
