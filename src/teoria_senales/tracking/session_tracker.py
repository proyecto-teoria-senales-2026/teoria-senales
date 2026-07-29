"""Servicio de seguimiento del trabajo realizado por el estudiante."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import uuid4

from teoria_senales.domain.models import (
    AttemptRecord,
    CriterionRecord,
    CriterionStatus,
    EvaluationCriterionRecord,
    EvaluationQuestionRecord,
    EvaluationRecord,
    SessionRecord,
    StepRecord,
    StepStatus,
    current_time,
)

if TYPE_CHECKING:
    from teoria_senales.evaluation.autograding import EvaluationResult


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

    @classmethod
    def from_session(cls, session: SessionRecord, exercise: Any) -> SessionTracker:
        """Continúa una sesión guardada con el ejercicio que le corresponde."""

        if session.exercise_id != exercise.exercise_id:
            raise ValueError("La sesión guardada no corresponde al ejercicio solicitado.")
        tracker = cls.__new__(cls)
        tracker.exercise = exercise
        tracker.session = session
        return tracker

    def register_attempt(
        self,
        step_id: str,
        answer: Any,
        correct: bool,
        feedback: str,
        difficulty: str,
    ) -> AttemptRecord:
        step = self.session.steps[step_id]
        if step.status == StepStatus.COMPLETED:
            return step.attempts[-1]

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
        if help_text in step.help_requests:
            return
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

    def record_evaluation(self, result: EvaluationResult) -> EvaluationRecord:
        """Guarda respuestas, puntaje y evidencia por criterio en la sesión."""

        if self.session.evaluation is not None:
            return self.session.evaluation

        question_records = [
            EvaluationQuestionRecord(
                question_id=question.question_id,
                answer=question.answer,
                correct=question.correct,
                points_earned=question.points_earned,
                points_possible=question.points_possible,
                criterion_ids=question.criterion_ids,
                rae_id=question.rae_id,
            )
            for question in result.questions
        ]
        criterion_records = self._group_evaluation_by_criterion(question_records)
        evaluation = EvaluationRecord(
            points_earned=result.points_earned,
            points_possible=result.points_possible,
            grade=result.grade,
            questions=question_records,
            criteria=criterion_records,
        )
        self.session.evaluation = evaluation
        step = self.session.steps["paso_5"]
        step.attempts.append(
            AttemptRecord(
                number=1,
                answer={
                    question.question_id: question.answer
                    for question in result.questions
                },
                correct=all(question.correct for question in result.questions),
                feedback=(
                    "Evaluación automática completada: "
                    f"{result.points_earned}/{result.points_possible} puntos."
                ),
            )
        )
        step.status = StepStatus.COMPLETED
        return evaluation

    def complete(self, results: dict[str, Any]) -> SessionRecord:
        self.session.results = results
        self.session.finished_at = current_time()
        self.session.criteria = self._evaluate_criteria()
        return self.session

    @staticmethod
    def _group_evaluation_by_criterion(
        questions: list[EvaluationQuestionRecord],
    ) -> list[EvaluationCriterionRecord]:
        criterion_ids = dict.fromkeys(
            criterion_id
            for question in questions
            for criterion_id in question.criterion_ids
        )
        records: list[EvaluationCriterionRecord] = []
        for criterion_id in criterion_ids:
            related = [
                question
                for question in questions
                if criterion_id in question.criterion_ids
            ]
            evidence = "; ".join(
                (
                    f"{question.question_id}: "
                    f"{question.points_earned}/{question.points_possible} puntos"
                )
                for question in related
            )
            records.append(
                EvaluationCriterionRecord(
                    criterion_id=criterion_id,
                    question_ids=tuple(
                        question.question_id for question in related
                    ),
                    achieved=all(question.correct for question in related),
                    evidence=evidence,
                )
            )
        return records

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
                "Obtiene el resultado mediante DFT/FFT para N = 3.",
                ("paso_3",),
            ),
            (
                "CR4",
                "Obtiene el resultado mediante DFT/FFT para N = 5.",
                ("paso_4",),
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

        records.extend(self._interpretation_criteria())
        return self._apply_evaluation_results(records)

    @staticmethod
    def _interpretation_criteria() -> list[CriterionRecord]:
        return [
            CriterionRecord(
                "CR5",
                "Compara los resultados y reconoce la función del relleno con ceros.",
                CriterionStatus.TEACHER_REVIEW,
                "Respuestas de comparación registradas en el Paso 5.",
            ),
            CriterionRecord(
                "CR6",
                "Reconoce la convolución circular y relaciona tiempo y frecuencia.",
                CriterionStatus.TEACHER_REVIEW,
                "Respuestas conceptuales registradas en el Paso 5.",
            ),
        ]

    def _apply_evaluation_results(
        self,
        criteria: list[CriterionRecord],
    ) -> list[CriterionRecord]:
        if self.session.evaluation is None:
            return criteria

        evaluation_by_criterion = {
            record.criterion_id: record
            for record in self.session.evaluation.criteria
        }
        for criterion in criteria:
            evaluation = evaluation_by_criterion.get(criterion.criterion_id)
            if evaluation is None:
                continue
            criterion.status = (
                CriterionStatus.ACHIEVED
                if evaluation.achieved
                else CriterionStatus.NEEDS_REINFORCEMENT
            )
            criterion.evidence = f"Evaluación automática: {evaluation.evidence}."
        return criteria
