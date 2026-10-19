"""Banco y selección reproducible de preguntas para C1-2."""

from __future__ import annotations

import random
from collections.abc import Hashable

from teoria_senales.evaluation.autograding import (
    EvaluationResult,
    QuestionDefinition,
    QuestionType,
    evaluate_questions,
)
from teoria_senales.exercises.signal_characteristics import (
    SignalCharacteristicsExercise,
)


def _mcq(number, prompt, expected, options, criterion):
    return QuestionDefinition(
        question_id=f"C1-2-P{number:02d}",
        question_type=QuestionType.MULTIPLE_CHOICE,
        prompt=prompt,
        points=1,
        criterion_ids=(criterion,),
        rae_id="RAE_C1",
        expected_answer=expected,
        options=options,
    )


def _true_false(number, prompt, expected, criterion):
    return QuestionDefinition(
        question_id=f"C1-2-P{number:02d}",
        question_type=QuestionType.TRUE_FALSE,
        prompt=prompt,
        points=1,
        criterion_ids=(criterion,),
        rae_id="RAE_C1",
        expected_answer=expected,
    )


_RESULTS = SignalCharacteristicsExercise().expected_results

C1_2_QUESTION_BANK = (
    _mcq(1, "¿Qué condición define una señal par?", "b", (("a", "x[n] = -x[-n]"), ("b", "x[n] = x[-n]"), ("c", "x[n + 1] = 0"), ("d", "x[n] = n")), "C1_2_CR1"),
    _mcq(2, "¿Qué condición define una señal impar?", "a", (("a", "x[n] = -x[-n]"), ("b", "x[n] = x[-n]"), ("c", "x[n] = 1"), ("d", "x[n + N0] = x[n]")), "C1_2_CR1"),
    _mcq(3, "¿Cuál debe ser el valor de x[0] en una señal impar?", "c", (("a", "1"), ("b", "-1"), ("c", "0"), ("d", "N0")), "C1_2_CR1"),
    _mcq(4, "¿Cuál es el periodo fundamental de x[n] = cos((pi/2)n)?", "d", (("a", "1"), ("b", "2"), ("c", "3"), ("d", str(_RESULTS["periodo_senoidal"]))), "C1_2_CR2"),
    _mcq(5, "¿Qué condición debe cumplir una señal periódica?", "b", (("a", "x[n] = 0 para todo n"), ("b", "x[n + N0] = x[n] para algún entero positivo N0"), ("c", "Su energía siempre es finita"), ("d", "Debe ser impar")), "C1_2_CR2"),
    _mcq(6, "¿Cómo se clasifica x[n] = (1/2)^n u[n] respecto a la periodicidad?", "c", (("a", "Periódica con N0 = 2"), ("b", "Periódica con N0 = 4"), ("c", "Aperiódica"), ("d", "Impar")), "C1_2_CR2"),
    _mcq(7, "¿Cuál es la energía de la secuencia finita {1, -1, 2}?", "d", (("a", "0"), ("b", "2"), ("c", "4"), ("d", str(int(_RESULTS["energia_secuencia_finita"]))),), "C1_2_CR3"),
    _mcq(8, "¿Cuál es la potencia media de la señal periódica con un periodo {1, 0, -1, 0}?", "b", (("a", "0"), ("b", "0,5"), ("c", "1"), ("d", "2")), "C1_2_CR3"),
    _mcq(9, "¿Qué expresión calcula la energía de una señal discreta?", "a", (("a", "La suma de |x[n]|^2"), ("b", "El máximo de x[n]"), ("c", "El periodo dividido entre dos"), ("d", "La suma de los índices n")), "C1_2_CR3"),
    _true_false(10, "Una señal par cumple x[n] = x[-n].", True, "C1_2_CR1"),
    _true_false(11, "Toda señal discreta es par o impar.", False, "C1_2_CR1"),
    _true_false(12, "El periodo fundamental es el menor entero positivo N0 que satisface x[n + N0] = x[n].", True, "C1_2_CR2"),
    _true_false(13, "La exponencial causal x[n] = (1/2)^n u[n] es periódica.", False, "C1_2_CR2"),
    _true_false(14, "Una secuencia de duración finita y energía finita tiene potencia media cero cuando se extiende con ceros.", True, "C1_2_CR3"),
    _true_false(15, "Una señal periódica no nula tiene energía infinita y potencia media finita.", True, "C1_2_CR3"),
)


def select_c1_2_questions(seed: Hashable) -> tuple[QuestionDefinition, ...]:
    generator = random.Random(str(seed))
    multiple_choice = [q for q in C1_2_QUESTION_BANK if q.question_type is QuestionType.MULTIPLE_CHOICE]
    true_false = [q for q in C1_2_QUESTION_BANK if q.question_type is QuestionType.TRUE_FALSE]
    selected = generator.sample(multiple_choice, 3) + generator.sample(true_false, 2)
    generator.shuffle(selected)
    return tuple(selected)


def evaluate_c1_2(questions, answers) -> EvaluationResult:
    return evaluate_questions(questions, answers)
