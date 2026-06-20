import pytest

from pde_tools.policy import PolicyViolation
from pde_tools.solvers import run_pde_experiment


def test_heat_equation_error_is_small():
    result = run_pde_experiment("heat", alpha=1.0, nx=101, dt=1e-5, T=0.01)
    assert result["relative_l2_error"] < 1e-3
    assert result["stable"] is True


def test_wave_equation_error_is_small():
    result = run_pde_experiment("wave", c=1.0, nx=201, dt=0.0025, T=0.25)
    assert result["relative_l2_error"] < 1e-3
    assert result["stable"] is True


def test_advection_equation_error_is_reasonable_for_upwind():
    result = run_pde_experiment("advection", c=1.0, nx=200, dt=0.002, T=0.2)
    assert result["relative_l2_error"] < 3e-2
    assert result["stable"] is True


def test_heat_equation_rejects_unstable_dt():
    with pytest.raises(PolicyViolation):
        run_pde_experiment("heat", alpha=1.0, nx=101, dt=1.0, T=0.01)


def test_unknown_pde_is_rejected():
    with pytest.raises(PolicyViolation):
        run_pde_experiment("burgers", nx=101, dt=1e-4, T=0.01)
