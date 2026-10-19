"""Definición técnica del ejercicio C1-3."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Any

from teoria_senales.signal_processing.fourier_series import (
    harmonic_amplitude_phase,
    rectangular_pulse_coefficients,
)


@dataclass(frozen=True)
class FourierSeriesStep:
    step_id: str
    title: str
    hint: str
    difficulty: str


class FourierSeriesExercise:
    """Fuente única de señal, fórmulas y resultados para C1-3."""

    exercise_id = "C1-3"
    title = "Coeficientes y espectro de la serie de Fourier"
    rae_id = "RAE_C1"
    learning_result = (
        "Calcular los coeficientes de la serie trigonométrica de Fourier de "
        "una señal periódica y visualizar sus espectros de amplitud y fase."
    )
    amplitude = 1.0
    period = 2 * pi
    half_width = pi / 2
    omega_0 = 2 * pi / period
    harmonics = 5

    steps = (
        FourierSeriesStep(
            "paso_1",
            "Identifica el periodo y la frecuencia fundamental",
            "La señal se repite cada 2π. Usa ω₀ = 2π/T₀.",
            "Identificación de T₀ y cálculo de ω₀.",
        ),
        FourierSeriesStep(
            "paso_2",
            "Calcula el término constante y reconoce la simetría",
            "Usa a₀ = (2/T₀)∫x(t)dt. Como x(t) es par, todos los coeficientes bₙ son cero.",
            "Cálculo de a₀, valor medio y efecto de la simetría par.",
        ),
        FourierSeriesStep(
            "paso_3",
            "Calcula los coeficientes de los armónicos",
            "Para este pulso, aₙ = (2/(πn))sen(nπ/2). Evalúa n = 1, 2 y 3.",
            "Sustitución de n en la expresión analítica de aₙ.",
        ),
        FourierSeriesStep(
            "paso_4",
            "Interpreta los espectros de amplitud y fase",
            "Usa Aₙ = √(aₙ²+bₙ²) y φₙ = atan2(-bₙ,aₙ). Un aₙ negativo produce fase π.",
            "Conversión de coeficientes trigonométricos a amplitud y fase.",
        ),
        FourierSeriesStep(
            "paso_5",
            "Comprueba lo aprendido",
            "Relaciona la señal, sus coeficientes y sus espectros.",
            "Integración conceptual de la serie trigonométrica de Fourier.",
        ),
    )

    criteria_by_step = (
        (
            "C1_3_CR1",
            "Identifica el periodo fundamental y formula la serie trigonométrica de Fourier.",
            ("paso_1",),
        ),
        (
            "C1_3_CR2",
            "Calcula a₀, aₙ y bₙ a partir de la señal periódica y su simetría.",
            ("paso_2", "paso_3"),
        ),
        (
            "C1_3_CR3",
            "Interpreta los armónicos en los espectros de amplitud y fase.",
            ("paso_4",),
        ),
    )

    @property
    def coefficients(self) -> tuple[float, tuple[float, ...], tuple[float, ...]]:
        a0, an, bn = rectangular_pulse_coefficients(
            self.harmonics,
            amplitude=self.amplitude,
            period=self.period,
            half_width=self.half_width,
        )
        return a0, tuple(float(value) for value in an), tuple(float(value) for value in bn)

    @property
    def expected_results(self) -> dict[str, float | list[float]]:
        a0, an, bn = self.coefficients
        amplitudes, phases = harmonic_amplitude_phase(an, bn)
        return {
            "periodo_fundamental": self.period,
            "frecuencia_angular_fundamental": self.omega_0,
            "a0": a0,
            "valor_medio": a0 / 2,
            "an": list(an),
            "bn": list(bn),
            "amplitudes": [float(value) for value in amplitudes],
            "fases": [None if value != value else float(value) for value in phases],
        }

    def validate(self, step_id: str, answer: Any) -> bool:
        try:
            values = tuple(float(value) for value in answer)
        except (TypeError, ValueError):
            return False

        results = self.expected_results
        expected_by_step = {
            "paso_1": (
                float(results["periodo_fundamental"]),
                float(results["frecuencia_angular_fundamental"]),
            ),
            "paso_2": (
                float(results["a0"]),
                float(results["valor_medio"]),
                0.0,
            ),
            "paso_3": (
                float(results["an"][0]),
                float(results["an"][1]),
                float(results["an"][2]),
            ),
            "paso_4": (
                float(results["amplitudes"][0]),
                float(results["fases"][0]),
                float(results["amplitudes"][2]),
                float(results["fases"][2]),
            ),
        }
        if step_id not in expected_by_step:
            raise ValueError(f"El paso {step_id!r} no tiene validación numérica automática.")
        expected = expected_by_step[step_id]
        return len(values) == len(expected) and all(
            abs(actual - target) <= 1e-3
            for actual, target in zip(values, expected, strict=True)
        )

    def get_step(self, step_id: str) -> FourierSeriesStep:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(f"No existe el paso {step_id!r}.")

