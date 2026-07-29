"""Flujo provisional por consola para demostrar el ejercicio completo."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from teoria_senales.evaluation.autograding import (
    QuestionType,
    evaluate_c3_3,
    get_c3_3_questions,
)
from teoria_senales.exercises.convolution_pilot import ConvolutionPilot
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.reports.pdf_report import generate_pdf_report
from teoria_senales.storage.json_repository import JsonSessionRepository
from teoria_senales.tracking.session_tracker import SessionTracker


def parse_numbers(raw_value: str) -> list[float]:
    tokens = raw_value.replace(";", ",").split(",")
    return [float(token.strip()) for token in tokens if token.strip()]


def _run_validated_step(
    tracker: SessionTracker,
    exercise: ConvolutionPilot,
    step_id: str,
    prompt: str,
    parser: Callable[[str], Any],
) -> None:
    definition = exercise.get_step(step_id)
    print(f"\n{definition.title}")
    while True:
        raw = input(f"{prompt}\nEscribe 'ayuda' para consultar una orientación: ").strip()
        if raw.lower() == "ayuda":
            tracker.register_help(step_id, definition.hint)
            print(f"Ayuda: {definition.hint}")
            continue
        try:
            answer = parser(raw)
        except ValueError:
            answer = raw
        correct = exercise.validate(step_id, answer)
        attempt_number = len(tracker.session.steps[step_id].attempts) + 1
        feedback = feedback_for_attempt(correct, attempt_number)
        tracker.register_attempt(
            step_id,
            answer,
            correct,
            feedback,
            definition.difficulty,
        )
        print(feedback)
        if correct:
            break


def _read_evaluation_answers() -> dict[str, Any]:
    print("\nEvaluación automática")
    print("Responde las ocho preguntas. El puntaje total es de 18 puntos.")
    answers: dict[str, Any] = {}
    for question in get_c3_3_questions():
        point_label = "punto" if question.points == 1 else "puntos"
        print(
            f"\n{question.question_id}. {question.prompt} "
            f"({question.points} {point_label})"
        )
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            for option_id, option_text in question.options:
                print(f"  {option_id}) {option_text}")
        elif question.question_type == QuestionType.TRUE_FALSE:
            print("  Escribe verdadero o falso.")

        raw_answer = input("> ").strip()
        if question.question_type == QuestionType.NUMERIC:
            try:
                answers[question.question_id] = parse_numbers(raw_answer)
            except ValueError:
                answers[question.question_id] = raw_answer
        else:
            answers[question.question_id] = raw_answer
    return answers


def run_interactive(output_directory: str | Path) -> tuple[Path, Path]:
    exercise = ConvolutionPilot()
    print("Prototipo del ejercicio guiado de convolución")
    print(f"x[n] = {exercise.x.astype(int).tolist()}")
    print(f"h[n] = {exercise.h.astype(int).tolist()}")
    student_name = input("Nombre del estudiante: ")
    student_id = input("Identificación: ")
    tracker = SessionTracker(student_name, student_id, exercise)

    _run_validated_step(
        tracker,
        exercise,
        "paso_1",
        "Ingresa Lx, Lh y Ly separados por comas.",
        parse_numbers,
    )
    _run_validated_step(
        tracker,
        exercise,
        "paso_2",
        "Ingresa la convolución lineal, separando las muestras por comas.",
        parse_numbers,
    )
    _run_validated_step(
        tracker,
        exercise,
        "paso_3",
        "Ingresa el resultado obtenido mediante DFT/FFT para N = 3.",
        parse_numbers,
    )
    _run_validated_step(
        tracker,
        exercise,
        "paso_4",
        "Ingresa el resultado obtenido mediante DFT/FFT para N = 5.",
        parse_numbers,
    )

    evaluation = evaluate_c3_3(_read_evaluation_answers())
    tracker.record_evaluation(evaluation)
    grade_text = f"{evaluation.grade:.2f}".replace(".", ",")
    print(
        "\nResultado: "
        f"{evaluation.points_earned}/{evaluation.points_possible} puntos, "
        f"nota {grade_text}."
    )
    session = tracker.complete(exercise.expected_results)
    repository = JsonSessionRepository(output_directory)
    json_path = repository.save(session)
    pdf_path = generate_pdf_report(session, output_directory)
    return json_path, pdf_path


def run_demo(output_directory: str | Path) -> tuple[Path, Path]:
    """Genera una sesión reproducible para mostrar el funcionamiento del piloto."""

    exercise = ConvolutionPilot()
    tracker = SessionTracker("Estudiante de demostración", "DEMO-001", exercise)

    scripted_attempts = {
        "paso_1": [([3, 3, 4], False), ([3, 3, 5], True)],
        "paso_2": [([1, 1, 1, 3, 2], True)],
        "paso_3": [([1, 1, 1], False), ([4, 3, 1], True)],
        "paso_4": [([1, 1, 1, 3, 2], True)],
    }
    tracker.register_help("paso_1", exercise.get_step("paso_1").hint)
    tracker.register_help("paso_3", exercise.get_step("paso_3").hint)
    for step_id, attempts in scripted_attempts.items():
        definition = exercise.get_step(step_id)
        for answer, expected_correct in attempts:
            correct = exercise.validate(step_id, answer)
            if correct != expected_correct:
                raise RuntimeError("La sesión de demostración no coincide con las validaciones.")
            attempt_number = len(tracker.session.steps[step_id].attempts) + 1
            tracker.register_attempt(
                step_id,
                answer,
                correct,
                feedback_for_attempt(correct, attempt_number),
                definition.difficulty,
            )

    evaluation = evaluate_c3_3(
        {
            "P1": [3, 3, 5],
            "P2": [1, 1, 1, 3, 2],
            "P3": [4, 3, 1],
            "P4": [1, 1, 1, 3, 2],
            "P5": "c",
            "P6": "b",
            "P7": False,
            "P8": True,
        }
    )
    tracker.record_evaluation(evaluation)
    session = tracker.complete(exercise.expected_results)
    repository = JsonSessionRepository(output_directory)
    return repository.save(session), generate_pdf_report(session, output_directory)
