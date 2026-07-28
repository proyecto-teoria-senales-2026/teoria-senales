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
class EvaluationQuestionRecord:
    question_id: str
    answer: Any
    correct: bool
    points_earned: int
    points_possible: int
    criterion_ids: tuple[str, ...]
    rae_id: str


@dataclass
class EvaluationCriterionRecord:
    criterion_id: str
    question_ids: tuple[str, ...]
    achieved: bool
    evidence: str


@dataclass
class EvaluationRecord:
    points_earned: int
    points_possible: int
    grade: float
    questions: list[EvaluationQuestionRecord]
    criteria: list[EvaluationCriterionRecord]
    completed_at: str = field(default_factory=current_time)


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
    evaluation: EvaluationRecord | None = None
    criteria: list[CriterionRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convierte la sesión a una estructura lista para guardar como JSON."""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SessionRecord:
        """Reconstruye una sesión previamente guardada."""

        steps = {
            step_id: StepRecord(
                step_id=step_data["step_id"],
                title=step_data["title"],
                status=StepStatus(step_data.get("status", StepStatus.NOT_STARTED)),
                attempts=[
                    AttemptRecord(**attempt)
                    for attempt in step_data.get("attempts", [])
                ],
                help_requests=list(step_data.get("help_requests", [])),
                corrections=step_data.get("corrections", 0),
                difficulties=list(step_data.get("difficulties", [])),
            )
            for step_id, step_data in data.get("steps", {}).items()
        }
        criteria = [
            CriterionRecord(
                criterion_id=criterion["criterion_id"],
                description=criterion["description"],
                status=CriterionStatus(criterion["status"]),
                evidence=criterion["evidence"],
            )
            for criterion in data.get("criteria", [])
        ]

        evaluation_data = data.get("evaluation")
        evaluation = None
        if evaluation_data is not None:
            evaluation = EvaluationRecord(
                points_earned=evaluation_data["points_earned"],
                points_possible=evaluation_data["points_possible"],
                grade=evaluation_data["grade"],
                questions=[
                    EvaluationQuestionRecord(
                        question_id=question["question_id"],
                        answer=question["answer"],
                        correct=question["correct"],
                        points_earned=question["points_earned"],
                        points_possible=question["points_possible"],
                        criterion_ids=tuple(question["criterion_ids"]),
                        rae_id=question["rae_id"],
                    )
                    for question in evaluation_data.get("questions", [])
                ],
                criteria=[
                    EvaluationCriterionRecord(
                        criterion_id=criterion["criterion_id"],
                        question_ids=tuple(criterion["question_ids"]),
                        achieved=criterion["achieved"],
                        evidence=criterion["evidence"],
                    )
                    for criterion in evaluation_data.get("criteria", [])
                ],
                completed_at=evaluation_data["completed_at"],
            )

        return cls(
            session_id=data["session_id"],
            student_name=data["student_name"],
            student_id=data["student_id"],
            exercise_id=data["exercise_id"],
            exercise_title=data["exercise_title"],
            started_at=data["started_at"],
            finished_at=data.get("finished_at"),
            steps=steps,
            results=dict(data.get("results", {})),
            interpretation_answers=dict(data.get("interpretation_answers", {})),
            conclusion=data.get("conclusion", ""),
            evaluation=evaluation,
            criteria=criteria,
        )
