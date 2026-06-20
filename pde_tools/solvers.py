from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from .policy import (
    PolicyViolation,
    ensure_int_bounds,
    ensure_numeric_bounds,
    ensure_supported_pde,
    safe_output_path,
)


@dataclass
class SolverResult:
    pde: str
    method: str
    parameters: dict[str, float | int | str]
    relative_l2_error: float
    stability_condition: str
    stable: bool
    plot_path: str
    csv_path: str
    report_path: str
    interpretation: str


def _relative_l2(numerical: np.ndarray, exact: np.ndarray) -> float:
    denominator = np.linalg.norm(exact)
    if denominator == 0:
        return float(np.linalg.norm(numerical - exact))
    return float(np.linalg.norm(numerical - exact) / denominator)


def _save_plot(
    x: np.ndarray,
    numerical: np.ndarray,
    exact: np.ndarray,
    title: str,
    filename: str,
) -> str:
    path = safe_output_path(filename)
    plt.figure()
    plt.plot(x, numerical, label="Numerical")
    plt.plot(x, exact, "--", label="Exact")
    plt.xlabel("x")
    plt.ylabel("u")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()
    return str(path)


def _save_csv(x: np.ndarray, numerical: np.ndarray, exact: np.ndarray, filename: str) -> str:
    path = safe_output_path(filename)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["x", "numerical", "exact", "absolute_error"])
        for xi, ui, ei in zip(x, numerical, exact):
            writer.writerow([float(xi), float(ui), float(ei), float(abs(ui - ei))])
    return str(path)


def _write_report(result: SolverResult) -> str:
    path = safe_output_path(f"{result.pde}_report.md")
    lines = [
        f"# {result.pde.title()} Equation Experiment Report",
        "",
        f"**Method:** {result.method}",
        "",
        "## Parameters",
        "",
    ]
    for key, value in result.parameters.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(
        [
            "",
            "## Stability",
            "",
            f"- Stable: `{result.stable}`",
            f"- Condition: `{result.stability_condition}`",
            "",
            "## Error",
            "",
            f"- Relative L2 error: `{result.relative_l2_error:.6e}`",
            "",
            "## Artifacts",
            "",
            f"- Plot: `{result.plot_path}`",
            f"- CSV: `{result.csv_path}`",
            "",
            "## Interpretation",
            "",
            result.interpretation,
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def solve_heat_equation(
    alpha: float = 1.0,
    nx: int = 101,
    dt: float = 1e-5,
    T: float = 0.01,
) -> SolverResult:
    alpha = ensure_numeric_bounds("alpha", alpha, 1e-8, 100.0)
    nx = ensure_int_bounds("nx", nx, 11, 5000)
    dt = ensure_numeric_bounds("dt", dt, 1e-10, 1.0)
    T = ensure_numeric_bounds("T", T, 1e-10, 10.0)

    x = np.linspace(0.0, 1.0, nx)
    dx = x[1] - x[0]
    stability_limit = dx**2 / (2.0 * alpha)
    if dt > stability_limit:
        raise PolicyViolation(
            f"Unstable heat-equation time step: dt={dt:.3e}, "
            f"but explicit Euler requires dt <= dx^2/(2 alpha) = {stability_limit:.3e}."
        )

    nt = int(np.ceil(T / dt))
    dt = T / nt
    r = alpha * dt / dx**2

    u = np.sin(np.pi * x)
    u[0] = 0.0
    u[-1] = 0.0

    for _ in range(nt):
        u_new = u.copy()
        u_new[1:-1] = u[1:-1] + r * (u[2:] - 2.0 * u[1:-1] + u[:-2])
        u_new[0] = 0.0
        u_new[-1] = 0.0
        u = u_new

    exact = np.exp(-alpha * np.pi**2 * T) * np.sin(np.pi * x)
    err = _relative_l2(u, exact)
    plot = _save_plot(x, u, exact, "1D Heat Equation", "heat_solution.png")
    csv_path = _save_csv(x, u, exact, "heat_solution.csv")

    result = SolverResult(
        pde="heat",
        method="explicit Euler in time, centered finite differences in space",
        parameters={
            "alpha": alpha,
            "nx": nx,
            "dx": float(dx),
            "dt": float(dt),
            "T": T,
            "nt": nt,
            "cfl_like_ratio": float(r),
        },
        relative_l2_error=err,
        stability_condition=f"dt <= dx^2/(2 alpha) = {stability_limit:.3e}",
        stable=True,
        plot_path=plot,
        csv_path=csv_path,
        report_path="",
        interpretation=(
            "The numerical solution is compared against the exact decaying sine mode. "
            "Because the time step satisfies the explicit heat-equation stability condition, "
            "the method remains stable and the relative L2 error is small for the chosen grid."
        ),
    )
    result.report_path = _write_report(result)
    return result


def solve_wave_equation(
    c: float = 1.0,
    nx: int = 201,
    dt: float = 0.0025,
    T: float = 0.25,
) -> SolverResult:
    c = ensure_numeric_bounds("c", c, 1e-8, 100.0)
    nx = ensure_int_bounds("nx", nx, 11, 5000)
    dt = ensure_numeric_bounds("dt", dt, 1e-10, 1.0)
    T = ensure_numeric_bounds("T", T, 1e-10, 10.0)

    x = np.linspace(0.0, 1.0, nx)
    dx = x[1] - x[0]
    cfl = c * dt / dx
    if cfl > 1.0:
        raise PolicyViolation(
            f"Unstable wave-equation time step: c*dt/dx={cfl:.3e}, but stability requires c*dt/dx <= 1."
        )

    nt = int(np.ceil(T / dt))
    dt = T / nt
    r = c * dt / dx

    u0 = np.sin(np.pi * x)
    u0[0] = 0.0
    u0[-1] = 0.0

    u_prev = u0.copy()
    u = u0.copy()
    u[1:-1] = u0[1:-1] + 0.5 * r**2 * (u0[2:] - 2.0 * u0[1:-1] + u0[:-2])
    u[0] = 0.0
    u[-1] = 0.0

    for _ in range(1, nt):
        u_next = u.copy()
        u_next[1:-1] = (
            2.0 * u[1:-1]
            - u_prev[1:-1]
            + r**2 * (u[2:] - 2.0 * u[1:-1] + u[:-2])
        )
        u_next[0] = 0.0
        u_next[-1] = 0.0
        u_prev, u = u, u_next

    exact = np.cos(c * np.pi * T) * np.sin(np.pi * x)
    err = _relative_l2(u, exact)
    plot = _save_plot(x, u, exact, "1D Wave Equation", "wave_solution.png")
    csv_path = _save_csv(x, u, exact, "wave_solution.csv")

    result = SolverResult(
        pde="wave",
        method="second-order centered finite differences in time and space",
        parameters={
            "c": c,
            "nx": nx,
            "dx": float(dx),
            "dt": float(dt),
            "T": T,
            "nt": nt,
            "cfl": float(r),
        },
        relative_l2_error=err,
        stability_condition="c*dt/dx <= 1",
        stable=True,
        plot_path=plot,
        csv_path=csv_path,
        report_path="",
        interpretation=(
            "The wave solution is compared against the exact standing-wave solution. "
            "The CFL condition is satisfied, so the finite-difference wave solver remains stable."
        ),
    )
    result.report_path = _write_report(result)
    return result


def solve_advection_equation(
    c: float = 1.0,
    nx: int = 200,
    dt: float = 0.002,
    T: float = 0.2,
) -> SolverResult:
    c = ensure_numeric_bounds("c", c, -100.0, 100.0)
    if c == 0:
        raise PolicyViolation("c must be nonzero for the advection experiment.")
    nx = ensure_int_bounds("nx", nx, 20, 10000)
    dt = ensure_numeric_bounds("dt", dt, 1e-10, 1.0)
    T = ensure_numeric_bounds("T", T, 1e-10, 10.0)

    x = np.linspace(0.0, 1.0, nx, endpoint=False)
    dx = 1.0 / nx
    cfl = abs(c) * dt / dx
    if cfl > 1.0:
        raise PolicyViolation(
            f"Unstable advection time step: |c|*dt/dx={cfl:.3e}, but upwind requires |c|*dt/dx <= 1."
        )

    nt = int(np.ceil(T / dt))
    dt = T / nt
    r = c * dt / dx

    u = np.sin(2.0 * np.pi * x)

    for _ in range(nt):
        if c > 0:
            u = u - r * (u - np.roll(u, 1))
        else:
            u = u - r * (np.roll(u, -1) - u)

    exact = np.sin(2.0 * np.pi * ((x - c * T) % 1.0))
    err = _relative_l2(u, exact)
    plot = _save_plot(x, u, exact, "1D Linear Advection Equation", "advection_solution.png")
    csv_path = _save_csv(x, u, exact, "advection_solution.csv")

    result = SolverResult(
        pde="advection",
        method="first-order upwind finite difference method with periodic boundary conditions",
        parameters={
            "c": c,
            "nx": nx,
            "dx": float(dx),
            "dt": float(dt),
            "T": T,
            "nt": nt,
            "cfl": float(abs(r)),
        },
        relative_l2_error=err,
        stability_condition="|c|*dt/dx <= 1",
        stable=True,
        plot_path=plot,
        csv_path=csv_path,
        report_path="",
        interpretation=(
            "The upwind method transports the sine wave around the periodic domain. "
            "The method is stable under the CFL condition, but it is first order and therefore introduces numerical diffusion."
        ),
    )
    result.report_path = _write_report(result)
    return result


def result_to_dict(result: SolverResult) -> dict[str, Any]:
    return {
        "pde": result.pde,
        "method": result.method,
        "parameters": result.parameters,
        "relative_l2_error": result.relative_l2_error,
        "stability_condition": result.stability_condition,
        "stable": result.stable,
        "plot_path": result.plot_path,
        "csv_path": result.csv_path,
        "report_path": result.report_path,
        "interpretation": result.interpretation,
    }


def run_pde_experiment(pde: str, **kwargs: Any) -> dict[str, Any]:
    pde = ensure_supported_pde(pde)

    if pde == "heat":
        allowed = {"alpha", "nx", "dt", "T"}
        params = {key: value for key, value in kwargs.items() if key in allowed and value is not None}
        return result_to_dict(solve_heat_equation(**params))

    if pde == "wave":
        allowed = {"c", "nx", "dt", "T"}
        params = {key: value for key, value in kwargs.items() if key in allowed and value is not None}
        return result_to_dict(solve_wave_equation(**params))

    if pde == "advection":
        allowed = {"c", "nx", "dt", "T"}
        params = {key: value for key, value in kwargs.items() if key in allowed and value is not None}
        return result_to_dict(solve_advection_equation(**params))

    raise PolicyViolation(f"Unsupported PDE '{pde}'.")
