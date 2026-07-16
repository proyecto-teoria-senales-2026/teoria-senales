"""Configuración y reglas del ejercicio aprobado de convolución."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from teoria_senales.signal_processing.convolution import (
    frequency_domain_convolution,
    linear_convolution,
    minimum_transform_length,
    values_match,
)


@dataclass(frozen=True)
class StepDefinition:
    step_id: str
    title: str
    hint: str
    difficulty: str


class ConvolutionPilot:
    """Mantiene en un solo lugar los datos y validaciones del piloto."""

    exercise_id = "C3-3"
    title = "Convolución lineal de señales discretas y verificación mediante DFT/FFT"
    x = np.asarray([1.0, 2.0, 1.0])
    h = np.asarray([1.0, -1.0, 2.0])

    steps = (
        StepDefinition(
            "paso_1",
            "Reconocimiento de las señales",
            "Usa L_y = L_x + L_h - 1 y verifica primero la longitud de cada secuencia.",
            "Identificación de índices y longitudes de secuencias finitas.",
        ),
        StepDefinition(
            "paso_2",
            "Cálculo de la convolución lineal",
            "Organiza los productos muestra por muestra para cada valor de n.",
            "Cálculo y desplazamiento de muestras en la suma de convolución.",
        ),
        StepDefinition(
            "paso_3",
            "Verificación con DFT/FFT para N = 3",
            "Compara N con L_x + L_h - 1 y considera el solapamiento circular.",
            "Interpretación de la convolución circular cuando N es insuficiente.",
        ),
        StepDefinition(
            "paso_4",
            "Verificación con DFT/FFT para N = 5",
            "Completa las dos secuencias con ceros hasta alcanzar cinco muestras.",
            "Uso del relleno con ceros para obtener la convolución lineal mediante DFT.",
        ),
        StepDefinition(
            "paso_5",
            "Comparación e interpretación",
            "Relaciona la longitud N con el tipo de convolución obtenido.",
            "Relación entre convolución temporal y multiplicación espectral.",
        ),
    )

    @property
    def expected_results(self) -> dict[str, list[float] | int]:
        return {
            "Lx": len(self.x),
            "Lh": len(self.h),
            "Ly": minimum_transform_length(self.x, self.h),
            "convolucion_lineal": linear_convolution(self.x, self.h).tolist(),
            "resultado_N3": frequency_domain_convolution(self.x, self.h, 3).tolist(),
            "resultado_N5": frequency_domain_convolution(self.x, self.h, 5).tolist(),
        }

    def validate(self, step_id: str, answer: Any) -> bool:
        expected = self.expected_results
        if step_id == "paso_1":
            try:
                values = [float(value) for value in answer]
            except (TypeError, ValueError):
                return False
            if len(values) != 3 or not all(value.is_integer() for value in values):
                return False
            lx, lh, ly = (int(value) for value in values)
            return (lx, lh, ly) == (expected["Lx"], expected["Lh"], expected["Ly"])
        if step_id == "paso_2":
            return values_match(answer, expected["convolucion_lineal"])
        if step_id == "paso_3":
            return values_match(answer, expected["resultado_N3"])
        if step_id == "paso_4":
            return values_match(answer, expected["resultado_N5"])
        raise ValueError(f"El paso {step_id!r} no tiene validación numérica automática.")

    def get_step(self, step_id: str) -> StepDefinition:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(f"No existe el paso {step_id!r}.")
