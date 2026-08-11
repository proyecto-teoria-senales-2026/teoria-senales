"""Cálculo de características de señales discretas."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def _as_real_samples(values: ArrayLike) -> np.ndarray:
    samples = np.asarray(values, dtype=float)
    if samples.ndim != 1 or samples.size == 0:
        raise ValueError("La señal debe ser una secuencia numérica no vacía.")
    if not np.all(np.isfinite(samples)):
        raise ValueError("Las muestras de la señal deben ser finitas.")
    return samples


def is_even_sequence(values: ArrayLike, *, tolerance: float = 1e-9) -> bool:
    """Verifica x[n] = x[-n] en una secuencia ordenada de -M a M."""

    samples = _as_real_samples(values)
    if samples.size % 2 == 0:
        raise ValueError("La verificación de paridad requiere un índice central n = 0.")
    return bool(np.allclose(samples, samples[::-1], atol=tolerance, rtol=0.0))


def is_odd_sequence(values: ArrayLike, *, tolerance: float = 1e-9) -> bool:
    """Verifica x[n] = -x[-n] en una secuencia ordenada de -M a M."""

    samples = _as_real_samples(values)
    if samples.size % 2 == 0:
        raise ValueError("La verificación de paridad requiere un índice central n = 0.")
    return bool(np.allclose(samples, -samples[::-1], atol=tolerance, rtol=0.0))


def signal_energy(values: ArrayLike) -> float:
    """Calcula E_x = suma de |x[n]|² para una secuencia finita."""

    samples = _as_real_samples(values)
    return float(np.sum(np.abs(samples) ** 2))


def periodic_average_power(one_period: ArrayLike) -> float:
    """Calcula P_x = (1/N0) suma de |x[n]|² en un periodo."""

    samples = _as_real_samples(one_period)
    return float(np.mean(np.abs(samples) ** 2))
