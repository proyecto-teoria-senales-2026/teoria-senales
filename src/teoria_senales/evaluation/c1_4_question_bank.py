"""Banco y selección reproducible de preguntas para C1-4."""

from __future__ import annotations

import random
from collections.abc import Hashable

from teoria_senales.evaluation.autograding import EvaluationResult, QuestionDefinition, QuestionType, evaluate_questions


def _mcq(number, prompt, expected, options, criterion):
    return QuestionDefinition(f"C1-4-P{number:02d}", QuestionType.MULTIPLE_CHOICE, prompt, 1, (criterion,), "RAE_C1", expected, options)


def _true_false(number, prompt, expected, criterion):
    return QuestionDefinition(f"C1-4-P{number:02d}", QuestionType.TRUE_FALSE, prompt, 1, (criterion,), "RAE_C1", expected)


C1_4_QUESTION_BANK = (
    _mcq(1, "¿Qué representa N en la suma parcial S_N(t) de C-1-4?", "b", (("a", "El periodo"), ("b", "El mayor orden armónico incluido"), ("c", "La amplitud"), ("d", "El número de saltos")), "C1_4_CR2"),
    _mcq(2, "¿Dónde están los saltos del periodo principal del pulso?", "c", (("a", "0 y π"), ("b", "±π"), ("c", "±π/2"), ("d", "±2π")), "C1_4_CR1"),
    _mcq(3, "¿A qué valor converge la serie exactamente en un salto 0↔1?", "a", (("a", "0,5"), ("b", "0"), ("c", "1"), ("d", "1,5")), "C1_4_CR1"),
    _mcq(4, "¿Qué ocurre con el ECM al pasar de N=5 a N=15?", "d", (("a", "Aumenta"), ("b", "No cambia"), ("c", "Se vuelve negativo"), ("d", "Disminuye")), "C1_4_CR2"),
    _mcq(5, "¿Qué relación permite calcular el ECM sin muestrear la señal?", "b", (("a", "Nyquist"), ("b", "Parseval"), ("c", "Convolución"), ("d", "Escalado temporal")), "C1_4_CR2"),
    _mcq(6, "¿Cuál es aproximadamente el sobreimpulso límite de Gibbs relativo al salto?", "c", (("a", "0 %"), ("b", "5 %"), ("c", "8,95 %"), ("d", "50 %")), "C1_4_CR3"),
    _mcq(7, "Al aumentar N, ¿cómo cambia la zona de oscilación cercana al salto?", "a", (("a", "Se hace más estrecha"), ("b", "Ocupa todo el periodo"), ("c", "Desaparece para N=15"), ("d", "Se vuelve constante")), "C1_4_CR3"),
    _mcq(8, "¿Cuál expresión corresponde a S₁(t)?", "d", (("a", "cos(t)"), ("b", "1/2"), ("c", "1+(2/π)sen(t)"), ("d", "1/2+(2/π)cos(t)")), "C1_4_CR2"),
    _mcq(9, "¿Qué significa convergencia global en este ejercicio?", "b", (("a", "Que no existen oscilaciones"), ("b", "Que el error promedio disminuye al aumentar N"), ("c", "Que cada suma parcial es idéntica"), ("d", "Que el pico siempre vale 1")), "C1_4_CR3"),
    _true_false(10, "Agregar armónicos mejora la aproximación temporal global.", True, "C1_4_CR2"),
    _true_false(11, "En una discontinuidad, la serie converge al promedio de los límites laterales.", True, "C1_4_CR1"),
    _true_false(12, "El fenómeno de Gibbs demuestra que la serie de Fourier no converge en ningún punto.", False, "C1_4_CR3"),
    _true_false(13, "El sobreimpulso límite de Gibbs es cercano al 8,95 % del tamaño del salto.", True, "C1_4_CR3"),
    _true_false(14, "El ECM puede calcularse a partir de la energía no capturada por los coeficientes incluidos.", True, "C1_4_CR2"),
    _true_false(15, "Para este pulso, los armónicos pares aportan coeficientes aₙ distintos de cero.", False, "C1_4_CR2"),
)


def select_c1_4_questions(seed: Hashable):
    generator = random.Random(str(seed))
    multiple_choice = [q for q in C1_4_QUESTION_BANK if q.question_type is QuestionType.MULTIPLE_CHOICE]
    true_false = [q for q in C1_4_QUESTION_BANK if q.question_type is QuestionType.TRUE_FALSE]
    selected = generator.sample(multiple_choice, 3) + generator.sample(true_false, 2)
    generator.shuffle(selected)
    return tuple(selected)


def evaluate_c1_4(questions, answers) -> EvaluationResult:
    return evaluate_questions(questions, answers)
