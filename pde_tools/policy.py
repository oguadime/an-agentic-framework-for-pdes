from __future__ import annotations

from pathlib import Path
from typing import Any

ALLOWED_PDES = {"heat", "wave", "advection"}
OUTPUT_DIR = Path("outputs").resolve()


class PolicyViolation(ValueError):
    """Raised when a proposed PDE experiment violates safety or scope policy."""


def ensure_supported_pde(pde: str) -> str:
    normalized = pde.strip().lower()
    aliases = {
        "heat equation": "heat",
        "diffusion": "heat",
        "diffusion equation": "heat",
        "wave equation": "wave",
        "linear advection": "advection",
        "advection equation": "advection",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in ALLOWED_PDES:
        raise PolicyViolation(
            f"Unsupported PDE '{pde}'. Supported PDEs are: {sorted(ALLOWED_PDES)}."
        )
    return normalized


def ensure_numeric_bounds(name: str, value: Any, lower: float, upper: float) -> float:
    try:
        numeric = float(value)
    except Exception as exc:
        raise PolicyViolation(f"{name} must be numeric.") from exc

    if not (lower <= numeric <= upper):
        raise PolicyViolation(f"{name}={numeric} is outside allowed range [{lower}, {upper}].")
    return numeric


def ensure_int_bounds(name: str, value: Any, lower: int, upper: int) -> int:
    try:
        numeric = int(value)
    except Exception as exc:
        raise PolicyViolation(f"{name} must be an integer.") from exc

    if not (lower <= numeric <= upper):
        raise PolicyViolation(f"{name}={numeric} is outside allowed range [{lower}, {upper}].")
    return numeric


def safe_output_path(filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    candidate = (OUTPUT_DIR / filename).resolve()
    if not str(candidate).startswith(str(OUTPUT_DIR)):
        raise PolicyViolation("Output path must stay inside outputs/.")
    return candidate
