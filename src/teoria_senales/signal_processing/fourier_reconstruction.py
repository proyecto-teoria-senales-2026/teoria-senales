"""Reconstrucción y convergencia de la serie de Fourier para C1-4."""

from __future__ import annotations

from math import pi

import numpy as np
from numpy.typing import ArrayLike

from teoria_senales.signal_processing.fourier_series import (
    reconstruct_trigonometric_series,
    rectangular_pulse_coefficients,
)


def rectangular_periodic_signal(time: ArrayLike) -> np.ndarray:
    """Evalúa el pulso 0/1, de periodo 2π, usando 0,5 en los saltos."""

    samples = np.asarray(time, dtype=float)
    if samples.ndim != 1 or samples.size == 0 or not np.all(np.isfinite(samples)):
        raise ValueError("El vector de tiempo debe ser unidimensional, finito y no vacío.")
    wrapped = (samples + pi) % (2 * pi) - pi
    distance = np.abs(wrapped)
    signal = (distance < pi / 2).astype(float)
    signal[np.isclose(distance, pi / 2, atol=1e-12)] = 0.5
    return signal


def reconstruct_rectangular_pulse(time: ArrayLike, harmonics: int) -> np.ndarray:
    """Calcula la suma parcial S_N(t), donde N es el mayor orden armónico."""

    a0, an, bn = rectangular_pulse_coefficients(harmonics)
    return reconstruct_trigonometric_series(time, a0, an, bn, omega_0=1.0)


def exact_mean_square_error(harmonics: int) -> float:
    """Obtiene el ECM periódico de S_N mediante Parseval, sin muestreo."""

    a0, an, bn = rectangular_pulse_coefficients(harmonics)
    original_mean_square = 0.5
    captured_mean_square = a0**2 / 4 + 0.5 * float(np.sum(an**2 + bn**2))
    return max(0.0, original_mean_square - captured_mean_square)


def gibbs_overshoot_ratio(integration_points: int = 200_001) -> float:
    """Calcula G = Si(π)/π - 1/2, razón límite del sobreimpulso de Gibbs."""

    if not isinstance(integration_points, int) or integration_points < 1001:
        raise ValueError("Se requieren al menos 1001 puntos de integración.")
    variable = np.linspace(0.0, pi, integration_points)
    integrand = np.ones_like(variable)
    integrand[1:] = np.sin(variable[1:]) / variable[1:]
    sine_integral = float(np.trapezoid(integrand, variable))
    return sine_integral / pi - 0.5


def reconstruction_metrics(harmonics: int) -> dict[str, float]:
    """Resume error global y referencia límite del fenómeno de Gibbs."""

    ratio = gibbs_overshoot_ratio()
    return {
        "harmonics": float(harmonics),
        "mean_square_error": exact_mean_square_error(harmonics),
        "gibbs_overshoot_ratio": ratio,
        "gibbs_overshoot_percent": 100 * ratio,
        "gibbs_limiting_peak": 1 + ratio,
    }
