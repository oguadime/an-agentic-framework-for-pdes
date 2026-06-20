# Heat Equation Experiment Report

**Method:** explicit Euler in time, centered finite differences in space

## Parameters

- `alpha`: `1.0`
- `nx`: `101`
- `dx`: `0.01`
- `dt`: `1e-05`
- `T`: `0.01`
- `nt`: `1000`
- `cfl_like_ratio`: `0.1`

## Stability

- Stable: `True`
- Condition: `dt <= dx^2/(2 alpha) = 5.000e-05`

## Error

- Relative L2 error: `3.247189e-06`

## Artifacts

- Plot: `/Users/emmanuel/Downloads/numerical-pde-agent/outputs/heat_solution.png`
- CSV: `/Users/emmanuel/Downloads/numerical-pde-agent/outputs/heat_solution.csv`

## Interpretation

The numerical solution is compared against the exact decaying sine mode. Because the time step satisfies the explicit heat-equation stability condition, the method remains stable and the relative L2 error is small for the chosen grid.
