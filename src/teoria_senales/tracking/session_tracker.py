"""Servicio de seguimiento del trabajo realizado por el estudiante."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from teoria_senales.domain.models import (
    AttemptRecord,
    CriterionRecord,
    CriterionStatus,
    SessionRecord,
    StepRecord,
    StepStatus,
    current_time,
)


class SessionTracker:
    def __init__(self, student_name: str, student_id: str, exercise: Any) -> None:
        self.exercise = exercise
        self.session = SessionRecord(
            session_id=str(uuid4()),
            student_name=student_name.strip() or "Estudiante de prueba",
            student_id=student_id.strip() or "SIN-ID",
            exercise_id=exercise.exercise_id,
            exercise_title=exercise.title,
            steps={
                step.step_id: StepRecord(step_id=step.step_id, title=step.title)
                for step in exercise.steps
            },
        )

    def register_attempt(
        self,
        step_id: str,
        answer: Any,
        correct: bool,
        feedback: str,
        difficulty: str,
    ) -> AttemptRecord:
        step = self.session.steps[step_id]
        attempt = AttemptRecord(
            number=len(step.attempts) + 1,
            answer=answer,
            correct=correct,
            feedback=feedback,
        )
        step.attempts.append(attempt)
        if correct:
            step.status = StepStatus.COMPLETED
        else:
            step.status = StepStatus.IN_PROGRESS
            step.corrections += 1
            if difficulty not in step.difficulties:
                step.difficulties.append(difficulty)
        return attempt

    def register_help(self, step_id: str, help_text: str) -> None:
        step = self.session.steps[step_id]
        step.help_requests.append(help_text)
        if step.status == StepStatus.NOT_STARTED:
            step.status = StepStatus.IN_PROGRESS

    def record_interpretation(self, answers: dict[str, str], conclusion: str) -> None:
        self.session.interpretation_answers = answers
        self.session.conclusion = conclusion
        step = self.session.steps["paso_5"]
        step.attempts.append(
            AttemptRecord(
                number=len(step.attempts) + 1,
                answer={"respuestas": answers, "conclusion": conclusion},
                correct=None,
                feedback="Respuestas registradas para revisión docente.",
            )
        )
        step.status = StepStatus.TEACHER_REVIEW

    def complete(self, results: dict[str, Any]) -> SessionRecord:
        self.session.results = results
        self.session.finished_at = current_time()
        self.session.criteria = self._evaluate_criteria()
        return self.session

    def _evaluate_criteria(self) -> list[CriterionRecord]:
        criteria_by_step = (
            (
                "CR1",
                "Identifica correctamente las longitudes de las señales.",
                ("paso_1",),
            ),
            (
                "CR2",
                "Calcula la convolución lineal en el dominio del tiempo.",
                ("paso_2",),
            ),
            (
                "CR3",
                "Compara los resultados obtenidos con N = 3 y N = 5.",
                ("paso_3", "paso_4"),
            ),
        )
        records: list[CriterionRecord] = []
        for criterion_id, description, step_ids in criteria_by_step:
            steps = [self.session.steps[step_id] for step_id in step_ids]
            achieved = all(step.status == StepStatus.COMPLETED for step in steps)
            status = (
                CriterionStatus.ACHIEVED
                if achieved
                else CriterionStatus.NEEDS_REINFORCEMENT
            )
            attempt_count = sum(len(step.attempts) for step in steps)
            step_label = "Paso asociado" if len(steps) == 1 else "Pasos asociados"
            completed_label = "completado" if len(steps) == 1 else "completados"
            attempt_label = "intento" if attempt_count == 1 else "intentos"
            evidence = (
                f"{step_label} {completed_label} en {attempt_count} {attempt_label}."
                if achieved
                else "Quedó pendiente completar uno o más pasos asociados."
            )
            records.append(CriterionRecord(criterion_id, description, status, evidence))

        records.extend(
            [
                CriterionRecord(
                    "CR4",
                    "Reconoce el efecto de la convolución circular.",
                    CriterionStatus.TEACHER_REVIEW,
                    "Respuesta sobre el caso N = 3 registrada en el Paso 5.",
                ),
                CriterionRecord(
                    "CR5",
                    "Explica la función del relleno con ceros al verificar la convolución lineal.",
                    CriterionStatus.TEACHER_REVIEW,
                    "Respuesta de interpretación registrada en el Paso 5.",
                ),
                CriterionRecord(
                    "CR6",
                    "Relaciona la convolución temporal con la multiplicación espectral.",
                    CriterionStatus.TEACHER_REVIEW,
                    "Respuesta de interpretación y conclusión registradas en el Paso 5.",
                ),
            ]
        )
        return records
