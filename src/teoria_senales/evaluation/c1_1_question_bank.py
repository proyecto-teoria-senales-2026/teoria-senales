"""Banco inicial y selección aleatoria reproducible para C1-1."""

from __future__ import annotations

import random
from collections.abc import Hashable

from teoria_senales.evaluation.autograding import (
    EvaluationResult,
    QuestionDefinition,
    QuestionType,
    evaluate_questions,
)


def _mcq(
    number: int,
    prompt: str,
    expected: str,
    options: tuple[tuple[str, str], ...],
    criterion: str,
) -> QuestionDefinition:
    return QuestionDefinition(
        question_id=f"C1-1-P{number:02d}",
        question_type=QuestionType.MULTIPLE_CHOICE,
        prompt=prompt,
        points=1,
        criterion_ids=(criterion,),
        rae_id="RAE_C1",
        expected_answer=expected,
        options=options,
    )


def _true_false(
    number: int,
    prompt: str,
    expected: bool,
    criterion: str,
) -> QuestionDefinition:
    return QuestionDefinition(
        question_id=f"C1-1-P{number:02d}",
        question_type=QuestionType.TRUE_FALSE,
        prompt=prompt,
        points=1,
        criterion_ids=(criterion,),
        rae_id="RAE_C1",
        expected_answer=expected,
    )


C1_1_QUESTION_BANK = (
    _mcq(
        1,
        "¿En qué índice vale 1 el impulso unitario δ[n]?",
        "b",
        (("a", "n = -1"), ("b", "n = 0"), ("c", "n = 1"), ("d", "En todos los índices")),
        "C1_1_CR1",
    ),
    _mcq(
        2,
        "¿Cuál es el valor del escalón unitario u[n] para n < 0?",
        "a",
        (("a", "0"), ("b", "1"), ("c", "n"), ("d", "-1")),
        "C1_1_CR1",
    ),
    _mcq(
        3,
        "¿Qué expresión representa la rampa unitaria discreta?",
        "c",
        (("a", "δ[n]"), ("b", "u[n - 1]"), ("c", "n·u[n]"), ("d", "cos(n)")),
        "C1_1_CR1",
    ),
    _mcq(
        4,
        "Si x[n] = 3δ[n], ¿cuál es x[0]?",
        "d",
        (("a", "0"), ("b", "1"), ("c", "2"), ("d", "3")),
        "C1_1_CR2",
    ),
    _mcq(
        5,
        "Si x[n] = 2u[n], ¿cuál es x[4]?",
        "c",
        (("a", "0"), ("b", "1"), ("c", "2"), ("d", "4")),
        "C1_1_CR2",
    ),
    _mcq(
        6,
        "Si x[n] = r[n], ¿cuál es x[3]?",
        "d",
        (("a", "0"), ("b", "1"), ("c", "2"), ("d", "3")),
        "C1_1_CR2",
    ),
    _mcq(
        7,
        "¿Cuál es el periodo de x[n] = sin((π/2)n)?",
        "b",
        (("a", "2 muestras"), ("b", "4 muestras"), ("c", "π muestras"), ("d", "No es periódica")),
        "C1_1_CR3",
    ),
    _mcq(
        8,
        "¿Qué parámetro controla el valor máximo de una señal senoidal?",
        "a",
        (("a", "La amplitud"), ("b", "El índice inicial"), ("c", "La duración del archivo"), ("d", "El nombre de la señal")),
        "C1_1_CR3",
    ),
    _mcq(
        9,
        "¿Qué sucede con x[n] = (1/2)^n u[n] cuando n aumenta desde n = 0?",
        "c",
        (("a", "Crece sin límite"), ("b", "Permanece constante"), ("c", "Disminuye hacia cero"), ("d", "Alterna entre 1 y -1")),
        "C1_1_CR2",
    ),
    _true_false(10, "El impulso unitario δ[n] vale cero para todo n distinto de cero.", True, "C1_1_CR1"),
    _true_false(11, "El escalón unitario u[n] vale cero en n = 0.", False, "C1_1_CR1"),
    _true_false(12, "La rampa unitaria r[n] es cero para n < 0.", True, "C1_1_CR2"),
    _true_false(13, "Multiplicar una señal por 2 duplica su amplitud.", True, "C1_1_CR2"),
    _true_false(14, "Toda señal senoidal de tiempo discreto es periódica para cualquier frecuencia angular.", False, "C1_1_CR3"),
    _true_false(
        15,
        "El impulso unitario δ[n] tiene duración finita porque solo es distinto de cero en n = 0.",
        True,
        "C1_1_CR1",
    ),
)


def select_c1_1_questions(seed: Hashable) -> tuple[QuestionDefinition, ...]:
    """Selecciona tres preguntas de opción múltiple y dos de V/F por sesión."""

    generator = random.Random(str(seed))
    multiple_choice = [
        question
        for question in C1_1_QUESTION_BANK
        if question.question_type is QuestionType.MULTIPLE_CHOICE
    ]
    true_false = [
        question
        for question in C1_1_QUESTION_BANK
        if question.question_type is QuestionType.TRUE_FALSE
    ]
    selected = generator.sample(multiple_choice, 3) + generator.sample(true_false, 2)
    generator.shuffle(selected)
    return tuple(selected)


def evaluate_c1_1(
    questions: tuple[QuestionDefinition, ...],
    answers: dict[str, object],
) -> EvaluationResult:
    return evaluate_questions(questions, answers)
