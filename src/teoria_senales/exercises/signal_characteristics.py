"""Definición técnica del ejercicio C1-2."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi
from typing import Any

from teoria_senales.signal_processing.signal_characteristics import (
    is_even_sequence,
    is_odd_sequence,
    periodic_average_power,
    signal_energy,
)


@dataclass(frozen=True)
class SignalCharacteristicStep:
    step_id: str
    title: str
    hint: str
    difficulty: str


class SignalCharacteristicsExercise:
    """Fuente única de fórmulas, señales y resultados para C1-2."""

    exercise_id = "C1-2"
    title = "Características de las señales discretas"
    rae_id = "RAE_C1"
    learning_result = (
        "Reconocer y relacionar paridad, periodicidad, energía, potencia y "
        "duración en señales discretas."
    )
    parity_indices = (-2, -1, 0, 1, 2)
    even_signal = (1.0, 2.0, 3.0, 2.0, 1.0)
    odd_signal = (-2.0, -1.0, 0.0, 1.0, 2.0)
    finite_energy_signal = (1.0, -1.0, 2.0)
    sinusoidal_period = tuple(cos((pi / 2) * n) for n in range(4))

    steps = (
        SignalCharacteristicStep(
            "paso_1",
            "Clasifica señales pares e impares",
            "Compara las muestras ubicadas en n y -n. Una señal par conserva "
            "el valor; una señal impar cambia el signo y cumple x[0] = 0.",
            "Aplicación de x[n] = x[-n] y x[n] = -x[-n].",
        ),
        SignalCharacteristicStep(
            "paso_2",
            "Reconoce periodicidad y duración",
            "Busca el menor entero positivo N0 que cumpla x[n + N0] = x[n]. "
            "Una exponencial causal decreciente no repite sus muestras.",
            "Diferenciación entre señales periódicas, aperiódicas y su duración.",
        ),
        SignalCharacteristicStep(
            "paso_3",
            "Calcula la energía de una secuencia finita",
            "Eleva al cuadrado la magnitud de cada muestra y suma los "
            "resultados. Una secuencia finita extendida con ceros tiene potencia media cero.",
            "Cálculo de energía y potencia de una señal de duración finita.",
        ),
        SignalCharacteristicStep(
            "paso_4",
            "Calcula la potencia de una señal periódica",
            "Calcula el promedio de |x[n]|² sobre un periodo completo. Una "
            "señal periódica no nula tiene energía infinita.",
            "Cálculo de potencia media y clasificación energética de una señal periódica.",
        ),
        SignalCharacteristicStep(
            "paso_5",
            "Comprueba lo aprendido",
            "Relaciona cada característica con su definición y su fórmula.",
            "Integración conceptual de las características de señales discretas.",
        ),
    )

    criteria_by_step = (
        (
            "C1_2_CR1",
            "Clasifica señales pares e impares y reconoce su duración.",
            ("paso_1",),
        ),
        (
            "C1_2_CR2",
            "Determina la periodicidad y el periodo fundamental de señales discretas.",
            ("paso_2",),
        ),
        (
            "C1_2_CR3",
            "Calcula e interpreta energía y potencia de señales discretas.",
            ("paso_3", "paso_4"),
        ),
    )

    @property
    def expected_results(self) -> dict[str, float | int | bool]:
        return {
            "primera_senal_es_par": is_even_sequence(self.even_signal),
            "segunda_senal_es_impar": is_odd_sequence(self.odd_signal),
            "periodo_senoidal": len(self.sinusoidal_period),
            "exponencial_causal_es_periodica": False,
            "energia_secuencia_finita": signal_energy(self.finite_energy_signal),
            "potencia_secuencia_finita": 0.0,
            "potencia_senoidal_periodica": periodic_average_power(
                self.sinusoidal_period
            ),
            "energia_senoidal_periodica_infinita": True,
        }

    def validate(self, step_id: str, answer: Any) -> bool:
        try:
            values = tuple(float(value) for value in answer)
        except (TypeError, ValueError):
            return False

        results = self.expected_results
        expected_by_step = {
            "paso_1": (0.0, 1.0),
            "paso_2": (
                float(results["periodo_senoidal"]),
                0.0,
                1.0,
            ),
            "paso_3": (
                float(results["energia_secuencia_finita"]),
                float(results["potencia_secuencia_finita"]),
            ),
            "paso_4": (
                float(results["potencia_senoidal_periodica"]),
                1.0,
                1.0,
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

    def get_step(self, step_id: str) -> SignalCharacteristicStep:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(f"No existe el paso {step_id!r}.")
