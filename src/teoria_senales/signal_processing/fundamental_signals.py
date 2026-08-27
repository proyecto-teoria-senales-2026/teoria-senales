"""Generación determinista de señales fundamentales de tiempo discreto."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import pi

import numpy as np
from numpy.typing import NDArray


class FundamentalSignalKind(str, Enum):
    IMPULSE = "impulso_unitario"
    STEP = "escalon_unitario"
    RAMP = "rampa_unitaria"
    EXPONENTIAL = "exponencial"
    SINUSOIDAL = "senoidal"


@dataclass(frozen=True)
class DiscreteSignal:
    indices: NDArray[np.int64]
    samples: NDArray[np.float64]
    symbol: str = "x[n]"


def discrete_indices(start: int, end: int) -> NDArray[np.int64]:
    """Construye un intervalo entero inclusivo y acotado para la interfaz."""

    if start > end:
        raise ValueError("El índice inicial no puede ser mayor que el índice final.")
    if end - start > 200:
        raise ValueError("El intervalo admite máximo 201 muestras.")
    return np.arange(start, end + 1, dtype=np.int64)


def generate_fundamental_signal(
    kind: FundamentalSignalKind | str,
    start: int,
    end: int,
    *,
    amplitude: float = 1.0,
    exponential_base: float = 0.5,
    causal: bool = False,
    angular_frequency: float = pi / 2,
    phase: float = 0.0,
) -> DiscreteSignal:
    """Genera una señal fundamental usando siempre el índice visible ``n``."""

    try:
        signal_kind = FundamentalSignalKind(kind)
    except ValueError as error:
        raise ValueError(f"Tipo de señal no soportado: {kind!r}.") from error

    n = discrete_indices(start, end)
    if signal_kind is FundamentalSignalKind.IMPULSE:
        samples = amplitude * (n == 0).astype(float)
    elif signal_kind is FundamentalSignalKind.STEP:
        samples = amplitude * (n >= 0).astype(float)
    elif signal_kind is FundamentalSignalKind.RAMP:
        samples = amplitude * np.where(n >= 0, n, 0).astype(float)
    elif signal_kind is FundamentalSignalKind.EXPONENTIAL:
        if exponential_base <= 0:
            raise ValueError("La base de la exponencial debe ser mayor que cero.")
        samples = amplitude * np.power(exponential_base, n.astype(float))
        if causal:
            samples = np.where(n >= 0, samples, 0.0)
    else:
        if angular_frequency <= 0:
            raise ValueError("La frecuencia angular debe ser mayor que cero.")
        samples = amplitude * np.sin(angular_frequency * n + phase)

    return DiscreteSignal(indices=n, samples=np.asarray(samples, dtype=float))


def sinusoidal_period_samples(
    angular_frequency: float,
    *,
    max_denominator: int = 10_000,
    tolerance: float = 1e-10,
) -> int | None:
    """Obtiene el periodo fundamental cuando ``omega/(2*pi)`` es racional."""

    if angular_frequency <= 0:
        raise ValueError("La frecuencia angular debe ser mayor que cero.")
    ratio = angular_frequency / (2 * pi)
    fraction = Fraction(ratio).limit_denominator(max_denominator)
    if abs(float(fraction) - ratio) > tolerance:
        return None
    return fraction.denominator
