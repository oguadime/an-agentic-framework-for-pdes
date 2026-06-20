# Wave Equation Experiment Report

**Method:** second-order centered finite differences in time and space

## Parameters

- `c`: `1.0`
- `nx`: `201`
- `dx`: `0.005`
- `dt`: `0.0025`
- `T`: `0.25`
- `nt`: `100`
- `cfl`: `0.5`

## Stability

- Stable: `True`
- Condition: `c*dt/dx <= 1`

## Error

- Relative L2 error: `6.055918e-06`

## Artifacts

- Plot: `/Users/emmanuel/Downloads/numerical-pde-agent/outputs/wave_solution.png`
- CSV: `/Users/emmanuel/Downloads/numerical-pde-agent/outputs/wave_solution.csv`

## Interpretation

The wave solution is compared against the exact standing-wave solution. The CFL condition is satisfied, so the finite-difference wave solver remains stable.
