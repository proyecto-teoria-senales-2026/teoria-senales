"""Preguntas y reglas de calificación automática para el piloto C3-3."""

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
            question_id="P1",
            question_type=QuestionType.NUMERIC,
            prompt=(
                f"Ingresa la convolución lineal y[n] de x[n] = {x_values} "
                f"y h[n] = {h_values}."
            ),
            points=3,
            criterion_ids=("CR2",),
            rae_id="RAE_C3",
            expected_answer=tuple(results["convolucion_lineal"]),
        ),
        QuestionDefinition(
            question_id="P2",
            question_type=QuestionType.NUMERIC,
            prompt="Ingresa el resultado obtenido mediante DFT/FFT para N = 3.",
            points=3,
            criterion_ids=("CR3",),
            rae_id="RAE_C3",
            expected_answer=tuple(results["resultado_N3"]),
        ),
        QuestionDefinition(
            question_id="P3",
            question_type=QuestionType.MULTIPLE_CHOICE,
            prompt=(
                "¿Qué explica correctamente la diferencia entre los resultados "
                "obtenidos con N = 3 y N = 5?"
            ),
            points=2,
            criterion_ids=("CR3", "CR4", "CR5"),
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
            question_id="P4",
            question_type=QuestionType.TRUE_FALSE,
            prompt=(
                "La convolución en el tiempo puede verificarse multiplicando las "
                "DFT de las señales y aplicando la transformada inversa, siempre "
                "que la longitud N sea suficiente."
            ),
            points=1,
            criterion_ids=("CR6",),
            rae_id="RAE_C3",
            expected_answer=True,
        ),
    )


C3_3_QUESTIONS = _build_c3_3_questions()


def get_c3_3_questions() -> tuple[QuestionDefinition, ...]:
    """Devuelve la configuración vigente de las cuatro preguntas del C3-3."""

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


def evaluate_c3_3(answers: dict[str, Any]) -> EvaluationResult:
    """Califica las cuatro respuestas del C3-3 sobre 9 puntos y nota 0,0–5,0."""

    configured_ids = {question.question_id for question in C3_3_QUESTIONS}
    unknown_ids = set(answers) - configured_ids
    if unknown_ids:
        unknown = ", ".join(sorted(unknown_ids))
        raise ValueError(f"Se recibieron preguntas no configuradas: {unknown}.")

    results: list[QuestionResult] = []
    for question in C3_3_QUESTIONS:
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

    points_possible = sum(question.points for question in C3_3_QUESTIONS)
    points_earned = sum(result.points_earned for result in results)
    grade = round(points_earned / points_possible * 5.0, 2)
    return EvaluationResult(
        questions=tuple(results),
        points_earned=points_earned,
        points_possible=points_possible,
        grade=grade,
    )
