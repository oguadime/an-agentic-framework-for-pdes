from __future__ import annotations

from typing import Any


def format_console_report(result: dict[str, Any]) -> str:
    params = "\n".join(f"  - {k}: {v}" for k, v in result["parameters"].items())
    return f"""PDE experiment completed.

PDE: {result['pde']}
Method: {result['method']}

Parameters:
{params}

Stability:
  - stable: {result['stable']}
  - condition: {result['stability_condition']}

Relative L2 error: {result['relative_l2_error']:.6e}

Artifacts:
  - plot: {result['plot_path']}
  - csv: {result['csv_path']}
  - report: {result['report_path']}

Interpretation:
{result['interpretation']}
"""
