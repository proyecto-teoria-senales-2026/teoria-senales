"""Cálculos de convolución usados por el ejercicio piloto."""

from __future__ import annotations

import re
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray


NUMERIC_TOLERANCE = 1e-6


def linear_convolution(x: ArrayLike, h: ArrayLike) -> NDArray[np.float64]:
    """Calcula la convolución lineal de dos secuencias finitas."""

    return np.convolve(np.asarray(x, dtype=float), np.asarray(h, dtype=float))


def frequency_domain_convolution(
    x: ArrayLike, h: ArrayLike, transform_length: int
) -> NDArray[np.float64]:
    """Calcula IFFT(FFT(x, N)·FFT(h, N)) para una longitud N dada."""

    if transform_length <= 0:
        raise ValueError("La longitud de transformación debe ser positiva.")

    x_array = np.asarray(x, dtype=float)
    h_array = np.asarray(h, dtype=float)
    if transform_length < max(len(x_array), len(h_array)):
        raise ValueError("N no puede ser menor que la longitud de las secuencias.")

    spectrum_product = np.fft.fft(x_array, transform_length) * np.fft.fft(
        h_array, transform_length
    )
    result = np.fft.ifft(spectrum_product)
    return np.real_if_close(result, tol=1000).real


def minimum_transform_length(x: ArrayLike, h: ArrayLike) -> int:
    """Devuelve la longitud mínima para evitar solapamiento circular."""

    return len(np.asarray(x)) + len(np.asarray(h)) - 1


def parse_numeric_sequence(value: Any) -> NDArray[np.float64] | None:
    """Convierte una respuesta común en una secuencia numérica válida."""

    if isinstance(value, str):
        normalized = value.strip()
        for bracket in "[](){}":
            normalized = normalized.replace(bracket, " ")
        value = [
            token
            for token in re.split(r"[,;\s]+", normalized)
            if token
        ]

    try:
        values = np.asarray(value, dtype=float)
    except (TypeError, ValueError):
        return None

    if (
        values.ndim != 1
        or values.size == 0
        or not np.all(np.isfinite(values))
    ):
        return None
    return values


def values_match(
    answer: Any,
    expected: ArrayLike,
    tolerance: float = NUMERIC_TOLERANCE,
) -> bool:
    """Compara dos secuencias considerando longitud y tolerancia numérica."""

    answer_array = parse_numeric_sequence(answer)
    expected_array = np.asarray(expected, dtype=float)
    return (
        answer_array is not None
        and answer_array.shape == expected_array.shape
        and bool(
            np.allclose(
                answer_array,
                expected_array,
                atol=tolerance,
                rtol=0.0,
            )
        )
    )
