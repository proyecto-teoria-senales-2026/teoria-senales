"""Cálculos para la serie trigonométrica de Fourier del ejercicio C1-3."""

from __future__ import annotations

from math import pi

import numpy as np
from numpy.typing import ArrayLike


NUMERIC_TOLERANCE = 1e-9


def rectangular_pulse_coefficients(
    harmonics: int,
    *,
    amplitude: float = 1.0,
    period: float = 2 * pi,
    half_width: float = pi / 2,
) -> tuple[float, np.ndarray, np.ndarray]:
    """Calcula a0, an y bn para un pulso rectangular par y periódico.

    Se usa la convención
    x(t) = a0/2 + sum(an cos(n*w0*t) + bn sin(n*w0*t)).
    En un periodo centrado en cero, x(t)=amplitude para |t|<=half_width
    y x(t)=0 fuera del pulso.
    """

    if not isinstance(harmonics, int) or isinstance(harmonics, bool) or harmonics < 1:
        raise ValueError("El número de armónicos debe ser un entero positivo.")
    if not np.isfinite(amplitude):
        raise ValueError("La amplitud debe ser finita.")
    if not np.isfinite(period) or period <= 0:
        raise ValueError("El periodo debe ser finito y positivo.")
    if not np.isfinite(half_width) or half_width <= 0 or 2 * half_width > period:
        raise ValueError("El semiancho debe ser positivo y no superar medio periodo.")

    omega_0 = 2 * pi / period
    a0 = 4 * amplitude * half_width / period
    orders = np.arange(1, harmonics + 1, dtype=float)
    an = (
        4
        * amplitude
        * np.sin(orders * omega_0 * half_width)
        / (period * orders * omega_0)
    )
    bn = np.zeros_like(an)
    an[np.abs(an) <= NUMERIC_TOLERANCE] = 0.0
    return float(a0), an, bn


def harmonic_amplitude_phase(
    an: ArrayLike,
    bn: ArrayLike,
) -> tuple[np.ndarray, np.ndarray]:
    """Convierte an y bn a A_n cos(n*w0*t + phi_n)."""

    cosine = np.asarray(an, dtype=float)
    sine = np.asarray(bn, dtype=float)
    if cosine.ndim != 1 or sine.ndim != 1 or cosine.shape != sine.shape:
        raise ValueError("an y bn deben ser vectores unidimensionales del mismo tamaño.")
    if cosine.size == 0 or not np.all(np.isfinite(cosine)) or not np.all(np.isfinite(sine)):
        raise ValueError("Los coeficientes deben ser vectores finitos no vacíos.")

    amplitudes = np.hypot(cosine, sine)
    phases = np.arctan2(-sine, cosine)
    phases[np.isclose(phases, -pi, atol=NUMERIC_TOLERANCE)] = pi
    phases[amplitudes <= NUMERIC_TOLERANCE] = np.nan
    return amplitudes, phases


def reconstruct_trigonometric_series(
    time: ArrayLike,
    a0: float,
    an: ArrayLike,
    bn: ArrayLike,
    *,
    omega_0: float,
) -> np.ndarray:
    """Evalúa una suma trigonométrica finita usando coeficientes calculados."""

    samples = np.asarray(time, dtype=float)
    cosine = np.asarray(an, dtype=float)
    sine = np.asarray(bn, dtype=float)
    if samples.ndim != 1 or samples.size == 0 or not np.all(np.isfinite(samples)):
        raise ValueError("El vector de tiempo debe ser unidimensional, finito y no vacío.")
    if cosine.ndim != 1 or sine.ndim != 1 or cosine.shape != sine.shape:
        raise ValueError("an y bn deben tener el mismo tamaño.")
    if cosine.size == 0 or not np.all(np.isfinite(cosine)) or not np.all(np.isfinite(sine)):
        raise ValueError("Los coeficientes deben ser finitos y no vacíos.")
    if not np.isfinite(a0) or not np.isfinite(omega_0) or omega_0 <= 0:
        raise ValueError("a0 debe ser finito y omega_0 debe ser finita y positiva.")

    orders = np.arange(1, cosine.size + 1, dtype=float)[:, None]
    angles = orders * omega_0 * samples[None, :]
    harmonic_terms = cosine[:, None] * np.cos(angles) + sine[:, None] * np.sin(angles)
    return a0 / 2 + np.sum(harmonic_terms, axis=0)

