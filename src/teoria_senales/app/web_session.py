"""Creación de la sesión usada por la interfaz gráfica."""

from __future__ import annotations

import re

from teoria_senales.domain.models import SessionRecord
from teoria_senales.exercises.convolution_pilot import ConvolutionPilot
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
    """Inicia una sesión del C3-3 a partir del código estudiantil."""

    normalized_id = normalize_student_code(student_id)
    return SessionTracker(
        student_name="Estudiante",
        student_id=normalized_id,
        exercise=ConvolutionPilot(),
    )


def restore_student_session(session: SessionRecord) -> SessionTracker:
    """Reconstruye el seguimiento de una sesión guardada del C3-3."""

    return SessionTracker.from_session(session, ConvolutionPilot())
