"""Cálculos del explorador visual de señales discretas."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from teoria_senales.signal_processing.convolution import (
    frequency_domain_convolution,
    linear_convolution,
    minimum_transform_length,
    parse_numeric_sequence,
)


MIN_SEQUENCE_LENGTH = 2
MAX_SEQUENCE_LENGTH = 8


@dataclass(frozen=True)
class SignalExploration:
    x: NDArray[np.float64]
    h: NDArray[np.float64]
    linear_result: NDArray[np.float64]
    frequency_result: NDArray[np.float64]
    transform_length: int
    minimum_length: int

    @property
    def has_circular_overlap(self) -> bool:
        return self.transform_length < self.minimum_length


def parse_explorer_sequence(value: str, signal_name: str) -> NDArray[np.float64]:
    """Valida una secuencia corta para la exploración visual."""

    sequence = parse_numeric_sequence(value)
    if sequence is None:
        raise ValueError(
            f"Ingresa valores numéricos válidos para {signal_name}."
        )
    if not MIN_SEQUENCE_LENGTH <= len(sequence) <= MAX_SEQUENCE_LENGTH:
        raise ValueError(
            f"{signal_name} debe tener entre {MIN_SEQUENCE_LENGTH} y "
            f"{MAX_SEQUENCE_LENGTH} muestras."
        )
    return sequence


def explore_signals(
    x_value: str,
    h_value: str,
    transform_length: int,
) -> SignalExploration:
    """Genera los resultados temporal y frecuencial de dos señales."""

    x = parse_explorer_sequence(x_value, "x[n]")
    h = parse_explorer_sequence(h_value, "h[n]")
    minimum_length = minimum_transform_length(x, h)
    smallest_input = max(len(x), len(h))
    if transform_length < smallest_input:
        raise ValueError(
            f"N debe ser mayor o igual que {smallest_input} para estas señales."
        )

    return SignalExploration(
        x=x,
        h=h,
        linear_result=linear_convolution(x, h),
        frequency_result=frequency_domain_convolution(
            x,
            h,
            transform_length,
        ),
        transform_length=transform_length,
        minimum_length=minimum_length,
    )
