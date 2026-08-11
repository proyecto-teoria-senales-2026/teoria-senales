"""Convenciones visibles compartidas por todos los ejercicios."""

from __future__ import annotations

import re
from collections.abc import Iterable


VISIBLE_SYMBOLS = {
    "input_signal": "x[n]",
    "impulse_response": "h[n]",
    "output_signal": "y[n]",
    "sample_index": "n",
    "summation_index": "m",
    "input_length": "L_x",
    "impulse_response_length": "L_h",
    "output_length": "L_y",
    "transform_length": "N",
    "fundamental_period": "T₀",
    "fundamental_angular_frequency": "ω₀",
}

_FORBIDDEN_VISIBLE_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9_])Lx(?![A-Za-z0-9_])"),
    re.compile(r"(?<![A-Za-z0-9_])Lh(?![A-Za-z0-9_])"),
    re.compile(r"(?<![A-Za-z0-9_])Ly(?![A-Za-z0-9_])"),
)


def inconsistent_visible_symbols(texts: Iterable[str]) -> tuple[str, ...]:
    """Devuelve expresiones visibles que incumplen la convención aprobada."""

    findings: list[str] = []
    for text in texts:
        for pattern in _FORBIDDEN_VISIBLE_PATTERNS:
            findings.extend(match.group(0) for match in pattern.finditer(text))
    return tuple(findings)


def visible_exercise_id(exercise_id: str) -> str:
    """Aplica la forma visible acordada sin alterar identificadores internos."""

    match = re.fullmatch(r"C(\d+)-(\d+)", exercise_id)
    if match:
        return f"C-{match.group(1)}-{match.group(2)}"
    return exercise_id
