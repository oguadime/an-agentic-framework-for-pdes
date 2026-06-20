# Advection Equation Experiment Report

**Method:** first-order upwind finite difference method with periodic boundary conditions

## Parameters

- `c`: `1.0`
- `nx`: `200`
- `dx`: `0.005`
- `dt`: `0.002`
- `T`: `0.2`
- `nt`: `100`
- `cfl`: `0.4`

## Stability

- Stable: `True`
- Condition: `|c|*dt/dx <= 1`

## Error

- Relative L2 error: `1.177412e-02`

## Artifacts

- Plot: `/Users/emmanuel/Downloads/numerical-pde-agent/outputs/advection_solution.png`
- CSV: `/Users/emmanuel/Downloads/numerical-pde-agent/outputs/advection_solution.csv`

## Interpretation

The upwind method transports the sine wave around the periodic domain. The method is stable under the CFL condition, but it is first order and therefore introduces numerical diffusion.
