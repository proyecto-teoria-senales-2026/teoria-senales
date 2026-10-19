"""Definición técnica del ejercicio C1-4."""

from __future__ import annotations

from dataclasses import dataclass
from math import pi
from typing import Any

from teoria_senales.signal_processing.fourier_reconstruction import (
    exact_mean_square_error,
    gibbs_overshoot_ratio,
    reconstruct_rectangular_pulse,
)


@dataclass(frozen=True)
class FourierReconstructionStep:
    step_id: str
    title: str
    hint: str
    difficulty: str


class FourierReconstructionExercise:
    """Fuente única de fórmulas, resultados y criterios para C1-4."""

    exercise_id = "C1-4"
    title = "Reconstrucción de Fourier y fenómeno de Gibbs"
    rae_id = "RAE_C1"
    learning_result = (
        "Comparar la reconstrucción de una señal con diferentes números de "
        "armónicos y observar el efecto en la aproximación."
    )
    period = 2 * pi
    omega_0 = 1.0
    comparison_harmonics = (1, 5, 15)

    steps = (
        FourierReconstructionStep(
            "paso_1",
            "Localiza las discontinuidades y su valor de convergencia",
            "Los saltos del periodo principal están en ±π/2; allí la serie converge al promedio de los límites laterales.",
            "Identificación de saltos y aplicación del criterio de Dirichlet.",
        ),
        FourierReconstructionStep(
            "paso_2",
            "Reconstruye la señal con un armónico",
            "Evalúa S₁(t)=1/2+(2/π)cos(t) en t=0 y t=π/2.",
            "Evaluación de una suma parcial de Fourier.",
        ),
        FourierReconstructionStep(
            "paso_3",
            "Compara el error con 5 y 15 armónicos",
            "Usa Parseval: ECM_N=1/2-[a₀²/4+(1/2)Σ(aₙ²+bₙ²)].",
            "Cálculo e interpretación del error cuadrático medio.",
        ),
        FourierReconstructionStep(
            "paso_4",
            "Interpreta el fenómeno de Gibbs",
            "El sobreimpulso límite relativo al salto es G=Si(π)/π−1/2.",
            "Diferenciación entre convergencia global y sobreimpulso local.",
        ),
        FourierReconstructionStep(
            "paso_5", "Comprueba lo aprendido", "Relaciona armónicos, error, convergencia y Gibbs.", "Integración conceptual."
        ),
    )

    criteria_by_step = (
        ("C1_4_CR1", "Identifica discontinuidades y aplica el valor de convergencia de la serie.", ("paso_1",)),
        ("C1_4_CR2", "Reconstruye la señal y compara cuantitativamente el error al aumentar N.", ("paso_2", "paso_3")),
        ("C1_4_CR3", "Interpreta el fenómeno de Gibbs sin confundirlo con falta de convergencia global.", ("paso_4",)),
    )

    @property
    def expected_results(self) -> dict[str, float | list[float]]:
        ratio = gibbs_overshoot_ratio()
        values = reconstruct_rectangular_pulse([0.0, pi / 2], 1)
        return {
            "periodo_fundamental": self.period,
            "discontinuidades_periodo_principal": [-pi / 2, pi / 2],
            "valor_convergencia_en_salto": 0.5,
            "S1_en_cero": float(values[0]),
            "S1_en_pi_sobre_2": float(values[1]),
            "ECM_N5": exact_mean_square_error(5),
            "ECM_N15": exact_mean_square_error(15),
            "sobreimpulso_gibbs_porcentaje": 100 * ratio,
            "pico_limite_gibbs": 1 + ratio,
        }

    def validate(self, step_id: str, answer: Any) -> bool:
        try:
            values = tuple(float(value) for value in answer)
        except (TypeError, ValueError):
            return False
        results = self.expected_results
        expected_by_step = {
            "paso_1": (-pi / 2, pi / 2, 0.5),
            "paso_2": (float(results["S1_en_cero"]), float(results["S1_en_pi_sobre_2"])),
            "paso_3": (float(results["ECM_N5"]), float(results["ECM_N15"])),
            "paso_4": (float(results["sobreimpulso_gibbs_porcentaje"]), float(results["pico_limite_gibbs"])),
        }
        if step_id not in expected_by_step:
            raise ValueError(f"El paso {step_id!r} no tiene validación numérica automática.")
        expected = expected_by_step[step_id]
        return len(values) == len(expected) and all(
            abs(actual - target) <= 1e-3
            for actual, target in zip(values, expected, strict=True)
        )

    def get_step(self, step_id: str) -> FourierReconstructionStep:
        for step in self.steps:
            if step.step_id == step_id:
                return step
        raise KeyError(f"No existe el paso {step_id!r}.")
