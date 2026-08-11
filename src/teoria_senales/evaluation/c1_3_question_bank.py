"""Banco y selección reproducible de preguntas para C1-3."""

from __future__ import annotations

import random
from collections.abc import Hashable

from teoria_senales.evaluation.autograding import (
    EvaluationResult,
    QuestionDefinition,
    QuestionType,
    evaluate_questions,
)


def _mcq(number, prompt, expected, options, criterion):
    return QuestionDefinition(
        question_id=f"C1-3-P{number:02d}",
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
        question_id=f"C1-3-P{number:02d}",
        question_type=QuestionType.TRUE_FALSE,
        prompt=prompt,
        points=1,
        criterion_ids=(criterion,),
        rae_id="RAE_C1",
        expected_answer=expected,
    )


C1_3_QUESTION_BANK = (
    _mcq(1, "¿Cuál es la forma de la serie trigonométrica usada en C-1-3?", "b", (("a", "x(t)=a₀+Σaₙsen(nω₀t)"), ("b", "x(t)=a₀/2+Σ[aₙcos(nω₀t)+bₙsen(nω₀t)]"), ("c", "x(t)=Σbₙ"), ("d", "x(t)=a₀/2")), "C1_3_CR1"),
    _mcq(2, "Si T₀ = 2π, ¿cuál es ω₀ = 2π/T₀?", "a", (("a", "1 rad/s"), ("b", "2 rad/s"), ("c", "π rad/s"), ("d", "2π rad/s")), "C1_3_CR1"),
    _mcq(3, "¿Qué integral calcula a₀ con la convención usada?", "c", (("a", "(1/T₀)∫x(t)dt"), ("b", "∫x²(t)dt"), ("c", "(2/T₀)∫x(t)dt"), ("d", "(2/T₀)∫x(t)sen(ω₀t)dt")), "C1_3_CR2"),
    _mcq(4, "Como el pulso rectangular de C-1-3 es par, ¿qué ocurre con bₙ?", "d", (("a", "bₙ=1"), ("b", "bₙ=aₙ"), ("c", "bₙ=-aₙ"), ("d", "bₙ=0 para todo n")), "C1_3_CR2"),
    _mcq(5, "Para aₙ=(2/(πn))sen(nπ/2), ¿cuánto vale a₁?", "b", (("a", "0"), ("b", "2/π"), ("c", "1/π"), ("d", "-2/π")), "C1_3_CR2"),
    _mcq(6, "Para aₙ=(2/(πn))sen(nπ/2), ¿cuánto vale a₂?", "a", (("a", "0"), ("b", "1/π"), ("c", "2/π"), ("d", "-2/(3π)")), "C1_3_CR2"),
    _mcq(7, "¿Cuál es la amplitud del armónico n?", "c", (("a", "aₙ+bₙ"), ("b", "aₙ-bₙ"), ("c", "√(aₙ²+bₙ²)"), ("d", "atan2(-bₙ,aₙ)")), "C1_3_CR3"),
    _mcq(8, "Si b₃=0 y a₃<0, ¿cuál es la fase del tercer armónico en la convención usada?", "d", (("a", "0"), ("b", "π/2"), ("c", "-π/2"), ("d", "π")), "C1_3_CR3"),
    _mcq(9, "¿Qué representa a₀/2 en la serie trigonométrica?", "a", (("a", "El valor medio o componente continua"), ("b", "La frecuencia fundamental"), ("c", "La fase del primer armónico"), ("d", "El periodo fundamental")), "C1_3_CR1"),
    _true_false(10, "La frecuencia angular fundamental cumple ω₀=2π/T₀.", True, "C1_3_CR1"),
    _true_false(11, "En la convención usada, el término constante de la serie es a₀/2.", True, "C1_3_CR1"),
    _true_false(12, "Una señal par puede tener coeficientes bₙ distintos de cero en su serie trigonométrica real.", False, "C1_3_CR2"),
    _true_false(13, "Para el pulso de C-1-3, los armónicos pares tienen aₙ=0.", True, "C1_3_CR2"),
    _true_false(14, "La amplitud Aₙ puede ser negativa.", False, "C1_3_CR3"),
    _true_false(15, "La fase de un armónico con amplitud cero no aporta información física y se considera indefinida.", True, "C1_3_CR3"),
)


def select_c1_3_questions(seed: Hashable) -> tuple[QuestionDefinition, ...]:
    generator = random.Random(str(seed))
    multiple_choice = [q for q in C1_3_QUESTION_BANK if q.question_type is QuestionType.MULTIPLE_CHOICE]
    true_false = [q for q in C1_3_QUESTION_BANK if q.question_type is QuestionType.TRUE_FALSE]
    selected = generator.sample(multiple_choice, 3) + generator.sample(true_false, 2)
    generator.shuffle(selected)
    return tuple(selected)


def evaluate_c1_3(questions, answers) -> EvaluationResult:
    return evaluate_questions(questions, answers)

