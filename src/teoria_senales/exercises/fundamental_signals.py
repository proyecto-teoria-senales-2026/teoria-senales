"""Definición técnica inicial del ejercicio C1-1."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Any

from teoria_senales.signal_processing.fundamental_signals import (
    DiscreteSignal,
    FundamentalSignalKind,
    generate_fundamental_signal,
    sinusoidal_period_samples,
)


@dataclass(frozen=True)
class FundamentalSignalExample:
    name: str
    notation: str
    signal: DiscreteSignal


@dataclass(frozen=True)
class FundamentalSignalStep:
    step_id: str
    title: str
    hint: str
    difficulty: str


class FundamentalSignalsExercise:
    """Fuente única de valores para C1-1, sus guías y su evaluación."""

    exercise_id = "C1-1"
    title = "Representación de señales fundamentales de tiempo discreto"
    rae_id = "RAE_C1"
    learning_result = (
        "Identificar y representar señales fundamentales de tiempo discreto: "
        "impulso unitario, escalón unitario, rampa, exponencial y senoidal."
    )
    index_start = -4
    index_end = 6
    steps = (
        FundamentalSignalStep(
            "paso_1",
            "Reconocimiento de las señales fundamentales",
            "Ubica primero n = 0. El impulso solo vale 1 en ese índice; "
            "el escalón cambia de 0 a 1 y la rampa comienza en 0.",
            "Identificación de impulso, escalón y rampa en tiempo discreto.",
        ),
        FundamentalSignalStep(
            "paso_2",
            "Lectura de muestras y amplitud",
            "Evalúa cada expresión en el índice solicitado antes de "
            "aplicar el factor de amplitud.",
            "Lectura de muestras y efecto del escalamiento de amplitud.",
        ),
        FundamentalSignalStep(
            "paso_3",
            "Comportamiento de la señal exponencial",
            "Para x[n] = (1/2)^n u[n], calcula primero (1/2)^0u[0] y "
            "(1/2)^2u[2]. "
            "Compara ambos valores para describir su comportamiento.",
            "Cálculo e interpretación de una exponencial discreta causal y decreciente.",
        ),
        FundamentalSignalStep(
            "paso_4",
            "Periodo y muestras de la señal senoidal",
            "El periodo N₀ cumple ω₀N₀ = 2πk. Para ω₀ = π/2, "
            "busca el menor entero positivo N₀.",
            "Relación entre frecuencia angular, periodo y muestras senoidales.",
        ),
        FundamentalSignalStep(
            "paso_5",
            "Evaluación automática",
            "Relaciona cada expresión con su representación y sus parámetros.",
            "Integración conceptual de las señales fundamentales.",
        ),
    )
    criteria_by_step = (
        (
            "C1_1_CR1",
            "Identifica y diferencia impulso, escalón, rampa, exponencial y senoidal, y reconoce su duración.",
            ("paso_1",),
        ),
        (
            "C1_1_CR2",
            "Calcula muestras y reconoce el efecto de la amplitud y la base exponencial.",
            ("paso_2", "paso_3"),
        ),
        (
            "C1_1_CR3",
            "Relaciona frecuencia angular, periodo y representación temporal x[n].",
            ("paso_4",),
        ),
    )

    def examples(self) -> tuple[FundamentalSignalExample, ...]:
        start, end = self.index_start, self.index_end
        return (
            FundamentalSignalExample(
                "Impulso unitario",
                "δ[n]",
                generate_fundamental_signal(
                    FundamentalSignalKind.IMPULSE, start, end
                ),
            ),
            FundamentalSignalExample(
                "Escalón unitario",
                "u[n]",
                generate_fundamental_signal(
                    FundamentalSignalKind.STEP, start, end
                ),
            ),
            FundamentalSignalExample(
                "Rampa unitaria",
                "r[n] = n·u[n]",
                generate_fundamental_signal(
                    FundamentalSignalKind.RAMP, start, end
                ),
            ),
            FundamentalSignalExample(
                "Exponencial discreta",
                "x[n] = (1/2)^n u[n]",
                generate_fundamental_signal(
                    FundamentalSignalKind.EXPONENTIAL,
                    start,
                    end,
                    exponential_base=0.5,
                    causal=True,
                ),
            ),
            FundamentalSignalExample(
                "Señal senoidal",
                "x[n] = sin((π/2)n)",
                generate_fundamental_signal(
                    FundamentalSignalKind.SINUSOIDAL,
                    start,
                    end,
                    angular_frequency=pi / 2,
                ),
            ),
        )

    @property
    def expected_results(self) -> dict[str, float | int]:
        impulse = generate_fundamental_signal(
            FundamentalSignalKind.IMPULSE, -1, 0
        )
        step = generate_fundamental_signal(
            FundamentalSignalKind.STEP, -1, 4
        )
        ramp = generate_fundamental_signal(
            FundamentalSignalKind.RAMP, 0, 3
        )
        exponential = generate_fundamental_signal(
            FundamentalSignalKind.EXPONENTIAL,
            0,
            2,
            exponential_base=0.5,
            causal=True,
        )
        return {
            "impulso_en_n_0": float(impulse.samples[-1]),
            "escalon_en_n_menos_1": float(step.samples[0]),
            "escalon_en_n_0": float(step.samples[1]),
            "escalon_en_n_4": float(step.samples[-1]),
            "rampa_en_n_3": float(ramp.samples[-1]),
            "exponencial_en_n_0": float(exponential.samples[0]),
            "exponencial_en_n_2": float(exponential.samples[-1]),
            "periodo_senoidal": sinusoidal_period_samples(pi / 2) or 0,
        }

    def validate(self, step_id: str, answer: Any) -> bool:
        try:
            values = tuple(float(value) for value in answer)
        except (TypeError, ValueError):
            return False

        results = self.expected_results
        sinusoidal = generate_fundamental_signal(
            FundamentalSignalKind.SINUSOIDAL,
            0,
            4,
            angular_frequency=pi / 2,
        )
        expected_by_step = {
            "paso_1": (
                results["impulso_en_n_0"],
                results["escalon_en_n_menos_1"],
                results["rampa_en_n_3"],
            ),
            "paso_2": (
                3 * results["impulso_en_n_0"],
                2 * results["escalon_en_n_4"],
                results["rampa_en_n_3"],
            ),
            "paso_3": (
                results["exponencial_en_n_0"],
                results["exponencial_en_n_2"],
                0.0,
            ),
            "paso_4": (
                results["periodo_senoidal"],
                *tuple(float(value) for value in sinusoidal.samples),
            ),
        }
        if step_id not in expected_by_step:
            raise ValueError(
                f"El paso {step_id!r} no tiene validación numérica automática."
            )
        expected = expected_by_step[step_id]
        return len(values) == len(expected) and all(
            abs(actual - target) <= 1e-9
            for actual, target in zip(values, expected, strict=True)
        )

    def get_step(self, step_id: str) -> FundamentalSignalStep:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(f"No existe el paso {step_id!r}.")
