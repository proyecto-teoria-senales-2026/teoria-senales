"""Creación de la sesión usada por la interfaz gráfica."""

from __future__ import annotations

import re

from teoria_senales.domain.models import SessionRecord
from teoria_senales.exercises.convolution_pilot import ConvolutionPilot
from teoria_senales.exercises.fundamental_signals import FundamentalSignalsExercise
from teoria_senales.exercises.fourier_series import FourierSeriesExercise
from teoria_senales.exercises.fourier_reconstruction import FourierReconstructionExercise
from teoria_senales.exercises.signal_characteristics import SignalCharacteristicsExercise
from teoria_senales.tracking.session_tracker import SessionTracker


MAX_STUDENT_CODE_LENGTH = 40
STUDENT_CODE_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def normalize_student_code(student_id: str) -> str:
    """Valida el código con reglas técnicas, no con un formato institucional."""

    normalized_id = student_id.strip()
    if not normalized_id:
        raise ValueError("Ingresa el código estudiantil para iniciar el ejercicio.")
    if len(normalized_id) > MAX_STUDENT_CODE_LENGTH:
        raise ValueError(
            f"El código estudiantil admite máximo {MAX_STUDENT_CODE_LENGTH} caracteres."
        )
    if (
        not STUDENT_CODE_PATTERN.fullmatch(normalized_id)
        or not any(character.isalnum() for character in normalized_id)
    ):
        raise ValueError(
            "Usa únicamente letras, números, guion (-) o guion bajo (_)."
        )
    return normalized_id


def create_student_session(student_id: str) -> SessionTracker:
    """Inicia una sesión de C-3-3 a partir del código estudiantil."""

    return create_exercise_session(student_id, "C3-3")


def restore_student_session(session: SessionRecord) -> SessionTracker:
    """Reconstruye el seguimiento de una sesión guardada de C-3-3."""

    return restore_exercise_session(session)


def exercise_for_id(exercise_id: str):
    exercises = {
        "C1-1": FundamentalSignalsExercise,
        "C1-2": SignalCharacteristicsExercise,
        "C1-3": FourierSeriesExercise,
        "C1-4": FourierReconstructionExercise,
        "C3-3": ConvolutionPilot,
    }
    try:
        return exercises[exercise_id]()
    except KeyError as error:
        raise ValueError(f"Ejercicio no soportado: {exercise_id}.") from error


def create_exercise_session(student_id: str, exercise_id: str) -> SessionTracker:
    normalized_id = normalize_student_code(student_id)
    return SessionTracker(
        student_name="Estudiante",
        student_id=normalized_id,
        exercise=exercise_for_id(exercise_id),
    )


def restore_exercise_session(session: SessionRecord) -> SessionTracker:
    return SessionTracker.from_session(
        session,
        exercise_for_id(session.exercise_id),
    )
