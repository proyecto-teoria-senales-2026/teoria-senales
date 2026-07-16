"""Modelos de datos para registrar una sesión de aprendizaje."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from zoneinfo import ZoneInfo


BOGOTA = ZoneInfo("America/Bogota")


def current_time() -> str:
    """Devuelve una marca de tiempo ISO 8601 en la zona horaria del proyecto."""

    return datetime.now(BOGOTA).isoformat(timespec="seconds")


class StepStatus(str, Enum):
    NOT_STARTED = "no_iniciado"
    IN_PROGRESS = "en_proceso"
    COMPLETED = "completado"
    TEACHER_REVIEW = "revision_docente"


class CriterionStatus(str, Enum):
    ACHIEVED = "alcanzado"
    NEEDS_REINFORCEMENT = "requiere_refuerzo"
    TEACHER_REVIEW = "revision_docente"


@dataclass
class AttemptRecord:
    number: int
    answer: Any
    correct: bool | None
    feedback: str
    timestamp: str = field(default_factory=current_time)


@dataclass
class StepRecord:
    step_id: str
    title: str
    status: StepStatus = StepStatus.NOT_STARTED
    attempts: list[AttemptRecord] = field(default_factory=list)
    help_requests: list[str] = field(default_factory=list)
    corrections: int = 0
    difficulties: list[str] = field(default_factory=list)


@dataclass
class CriterionRecord:
    criterion_id: str
    description: str
    status: CriterionStatus
    evidence: str


@dataclass
class SessionRecord:
    session_id: str
    student_name: str
    student_id: str
    exercise_id: str
    exercise_title: str
    started_at: str = field(default_factory=current_time)
    finished_at: str | None = None
    steps: dict[str, StepRecord] = field(default_factory=dict)
    results: dict[str, Any] = field(default_factory=dict)
    interpretation_answers: dict[str, str] = field(default_factory=dict)
    conclusion: str = ""
    criteria: list[CriterionRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convierte la sesión a una estructura lista para guardar como JSON."""

        return asdict(self)
