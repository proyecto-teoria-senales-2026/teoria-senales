"""Preguntas y reglas de calificación automática para el ejercicio C-3-3."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from teoria_senales.exercises.convolution_pilot import ConvolutionPilot
from teoria_senales.signal_processing.convolution import (
    NUMERIC_TOLERANCE,
    values_match,
)


class QuestionType(str, Enum):
    """Formatos autocalificables aprobados para el piloto."""

    NUMERIC = "numerica"
    MULTIPLE_CHOICE = "seleccion_multiple"
    TRUE_FALSE = "verdadero_falso"


@dataclass(frozen=True)
class QuestionDefinition:
    """Configuración editable de una pregunta calificable."""

    question_id: str
    question_type: QuestionType
    prompt: str
    points: int
    criterion_ids: tuple[str, ...]
    rae_id: str
    expected_answer: Any
    options: tuple[tuple[str, str], ...] = ()
    tolerance: float = NUMERIC_TOLERANCE


@dataclass(frozen=True)
class QuestionResult:
    """Resultado obtenido por el estudiante en una pregunta."""

    question_id: str
    criterion_ids: tuple[str, ...]
    rae_id: str
    points_possible: int
    points_earned: int
    correct: bool
    answer: Any


@dataclass(frozen=True)
class EvaluationResult:
    """Resumen completo de la evaluación automática."""

    questions: tuple[QuestionResult, ...]
    points_earned: int
    points_possible: int
    grade: float


def _build_c3_3_questions() -> tuple[QuestionDefinition, ...]:
    exercise = ConvolutionPilot()
    results = exercise.expected_results
    x_values = exercise.x.astype(int).tolist()
    h_values = exercise.h.astype(int).tolist()

    return (
        QuestionDefinition(
            question_id="C3-3-P01",
            question_type=QuestionType.NUMERIC,
            prompt=(
                f"Ingresa, en este orden, L_x, L_h y L_y para x[n] = {x_values} "
                f"y h[n] = {h_values}."
            ),
            points=3,
            criterion_ids=("C3_3_CR1",),
            rae_id="RAE_C3",
            expected_answer=(
                results["Lx"],
                results["Lh"],
                results["Ly"],
            ),
        ),
        QuestionDefinition(
            question_id="C3-3-P02",
            question_type=QuestionType.NUMERIC,
            prompt=(
                f"Ingresa la convolución lineal y[n] de x[n] = {x_values} "
                f"y h[n] = {h_values}."
            ),
            points=3,
            criterion_ids=("C3_3_CR2",),
            rae_id="RAE_C3",
            expected_answer=tuple(results["convolucion_lineal"]),
        ),
        QuestionDefinition(
            question_id="C3-3-P03",
            question_type=QuestionType.NUMERIC,
            prompt="Ingresa el resultado obtenido mediante DFT/FFT para N = 3.",
            points=3,
            criterion_ids=("C3_3_CR3",),
            rae_id="RAE_C3",
            expected_answer=tuple(results["resultado_N3"]),
        ),
        QuestionDefinition(
            question_id="C3-3-P04",
            question_type=QuestionType.NUMERIC,
            prompt="Ingresa el resultado obtenido mediante DFT/FFT para N = 5.",
            points=3,
            criterion_ids=("C3_3_CR4",),
            rae_id="RAE_C3",
            expected_answer=tuple(results["resultado_N5"]),
        ),
        QuestionDefinition(
            question_id="C3-3-P05",
            question_type=QuestionType.MULTIPLE_CHOICE,
            prompt=(
                "¿Qué explica correctamente la diferencia entre los resultados "
                "obtenidos con N = 3 y N = 5?"
            ),
            points=2,
            criterion_ids=("C3_3_CR5",),
            rae_id="RAE_C3",
            expected_answer="c",
            options=(
                (
                    "a",
                    "N = 3 reproduce la convolución lineal y N = 5 produce "
                    "convolución circular.",
                ),
                (
                    "b",
                    "Los dos valores de N producen siempre el mismo resultado, "
                    "sin importar la longitud de las señales.",
                ),
                (
                    "c",
                    "N = 3 produce convolución circular porque la longitud es "
                    "insuficiente; N = 5, con relleno de ceros, reproduce la "
                    "convolución lineal.",
                ),
                (
                    "d",
                    "El relleno de ceros cambia los valores originales de las "
                    "señales y por eso los resultados son diferentes.",
                ),
            ),
        ),
        QuestionDefinition(
            question_id="C3-3-P06",
            question_type=QuestionType.MULTIPLE_CHOICE,
            prompt=(
                "¿Cuál es la función del relleno con ceros al verificar la "
                "convolución lineal mediante DFT/FFT?"
            ),
            points=2,
            criterion_ids=("C3_3_CR5",),
            rae_id="RAE_C3",
            expected_answer="b",
            options=(
                (
                    "a",
                    "Modificar las amplitudes originales para que ambas "
                    "señales tengan los mismos valores.",
                ),
                (
                    "b",
                    "Completar las secuencias hasta una longitud N igual o "
                    "mayor que L_x + L_h - 1 para evitar el solapamiento circular.",
                ),
                (
                    "c",
                    "Aumentar la frecuencia de muestreo de las señales antes "
                    "de calcular la DFT.",
                ),
                (
                    "d",
                    "Eliminar la transformada inversa del procedimiento de "
                    "verificación.",
                ),
            ),
        ),
        QuestionDefinition(
            question_id="C3-3-P07",
            question_type=QuestionType.TRUE_FALSE,
            prompt=(
                "La convolución circular obtenida con N = 3 conserva las cinco "
                "muestras de la convolución lineal sin superposición."
            ),
            points=1,
            criterion_ids=("C3_3_CR6",),
            rae_id="RAE_C3",
            expected_answer=False,
        ),
        QuestionDefinition(
            question_id="C3-3-P08",
            question_type=QuestionType.TRUE_FALSE,
            prompt=(
                "La convolución en el tiempo puede verificarse multiplicando las "
                "DFT de las señales y aplicando la transformada inversa, siempre "
                "que la longitud N sea suficiente."
            ),
            points=1,
            criterion_ids=("C3_3_CR6",),
            rae_id="RAE_C3",
            expected_answer=True,
        ),
    )


C3_3_QUESTIONS = _build_c3_3_questions()


def get_c3_3_questions() -> tuple[QuestionDefinition, ...]:
    """Devuelve la configuración vigente de las ocho preguntas del C-3-3."""

    return C3_3_QUESTIONS


def _parse_boolean(answer: Any) -> bool | None:
    if isinstance(answer, bool):
        return answer
    if isinstance(answer, str):
        normalized = answer.strip().casefold()
        if normalized in {"verdadero", "v", "true"}:
            return True
        if normalized in {"falso", "f", "false"}:
            return False
    return None


def _is_correct(question: QuestionDefinition, answer: Any) -> bool:
    if question.question_type == QuestionType.NUMERIC:
        return values_match(
            answer,
            question.expected_answer,
            tolerance=question.tolerance,
        )
    if question.question_type == QuestionType.MULTIPLE_CHOICE:
        return (
            isinstance(answer, str)
            and answer.strip().casefold()
            == str(question.expected_answer).strip().casefold()
        )
    if question.question_type == QuestionType.TRUE_FALSE:
        return _parse_boolean(answer) is question.expected_answer
    raise ValueError(f"Formato de pregunta no soportado: {question.question_type!r}.")


def evaluate_questions(
    questions: tuple[QuestionDefinition, ...],
    answers: dict[str, Any],
) -> EvaluationResult:
    """Califica cualquier selección de preguntas con la escala común 0,0–5,0."""

    if not questions:
        raise ValueError("La evaluación debe incluir al menos una pregunta.")
    configured_ids = {question.question_id for question in questions}
    unknown_ids = set(answers) - configured_ids
    if unknown_ids:
        unknown = ", ".join(sorted(unknown_ids))
        raise ValueError(f"Se recibieron preguntas no configuradas: {unknown}.")

    results: list[QuestionResult] = []
    for question in questions:
        answer = answers.get(question.question_id)
        correct = _is_correct(question, answer)
        results.append(
            QuestionResult(
                question_id=question.question_id,
                criterion_ids=question.criterion_ids,
                rae_id=question.rae_id,
                points_possible=question.points,
                points_earned=question.points if correct else 0,
                correct=correct,
                answer=answer,
            )
        )

    points_possible = sum(question.points for question in questions)
    if points_possible <= 0:
        raise ValueError("El puntaje total de la evaluación debe ser positivo.")
    points_earned = sum(result.points_earned for result in results)
    grade = round(points_earned / points_possible * 5.0, 2)
    return EvaluationResult(
        questions=tuple(results),
        points_earned=points_earned,
        points_possible=points_possible,
        grade=grade,
    )


def evaluate_c3_3(answers: dict[str, Any]) -> EvaluationResult:
    """Califica las ocho respuestas del C-3-3 sobre 18 puntos y nota 0,0–5,0."""

    return evaluate_questions(C3_3_QUESTIONS, answers)
