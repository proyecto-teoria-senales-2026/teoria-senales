"""Verificación local de reportes contra el registro JSON original."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader

from teoria_senales.domain.models import SessionRecord
from teoria_senales.domain.nomenclature import visible_exercise_id
from teoria_senales.reports.pdf_report import (
    pdf_content_hash,
    report_content_hash,
    report_verification_code,
)
from teoria_senales.storage.json_repository import JsonSessionRepository, safe_name


@dataclass(frozen=True)
class VerificationResult:
    valid: bool
    status: str
    details: tuple[str, ...]
    session_id: str | None = None
    student_id: str | None = None
    exercise_id: str | None = None


def _metadata(pdf_data: bytes) -> dict[str, str]:
    reader = PdfReader(BytesIO(pdf_data))
    if reader.is_encrypted and reader.decrypt("") == 0:
        raise ValueError("El PDF no se puede abrir con la clave esperada.")
    return {str(key): str(value) for key, value in (reader.metadata or {}).items()}


def verify_pdf_against_session(
    pdf_data: bytes,
    session: SessionRecord,
) -> VerificationResult:
    """Comprueba metadatos y contenido visible contra una sesión finalizada."""

    details: list[str] = []
    try:
        metadata = _metadata(pdf_data)
        actual_content_hash = pdf_content_hash(pdf_data)
        expected_content_hash = report_content_hash(session)
    except Exception as error:
        return VerificationResult(False, "ALTERADO O NO VÁLIDO", (str(error),))

    expected = {
        "/TSVerificationCode": report_verification_code(session),
        "/TSSessionID": session.session_id,
        "/TSStudentID": session.student_id,
        "/TSExerciseID": visible_exercise_id(session.exercise_id),
        "/TSContentSHA256": expected_content_hash,
    }
    for key, expected_value in expected.items():
        actual_value = metadata.get(key)
        if actual_value != expected_value:
            details.append(
                f"Metadato {key} no coincide: esperado {expected_value!r}, recibido {actual_value!r}."
            )

    embedded_hash = metadata.get("/TSContentSHA256")
    if actual_content_hash != embedded_hash:
        details.append("La huella del contenido visible no coincide con la incorporada en el PDF.")
    if actual_content_hash != expected_content_hash:
        details.append("El contenido visible no coincide con el reporte reconstruido desde la sesión original.")

    valid = not details
    return VerificationResult(
        valid,
        "VÁLIDO" if valid else "ALTERADO O NO VÁLIDO",
        tuple(details) if details else ("Metadatos, código y contenido coinciden con la sesión original.",),
        session_id=session.session_id,
        student_id=session.student_id,
        exercise_id=visible_exercise_id(session.exercise_id),
    )


def find_session_for_pdf(
    pdf_data: bytes,
    sessions_directory: str | Path,
) -> tuple[SessionRecord, Path]:
    """Localiza el JSON original a partir del identificador incluido en el PDF."""

    metadata = _metadata(pdf_data)
    session_id = metadata.get("/TSSessionID")
    if not session_id:
        raise ValueError("El PDF no contiene el identificador de sesión requerido.")

    repository = JsonSessionRepository(sessions_directory)
    matches = list(repository.output_directory.glob(f"*_{safe_name(session_id)}.json"))
    exact: list[tuple[SessionRecord, Path]] = []
    for path in matches:
        try:
            session = repository.load(path)
        except Exception:
            continue
        if session.session_id == session_id:
            exact.append((session, path))
    if len(exact) != 1:
        raise ValueError(
            "No se encontró un único registro JSON original para la sesión del PDF."
        )
    return exact[0]


def verify_pdf_against_repository(
    pdf_data: bytes,
    sessions_directory: str | Path,
) -> VerificationResult:
    try:
        session, _ = find_session_for_pdf(pdf_data, sessions_directory)
    except Exception as error:
        return VerificationResult(False, "NO VERIFICABLE", (str(error),))
    return verify_pdf_against_session(pdf_data, session)
