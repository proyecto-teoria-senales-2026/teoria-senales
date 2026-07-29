"""Pruebas del núcleo numérico y del seguimiento del piloto."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.pilot_cli import run_demo
from teoria_senales.evaluation.autograding import evaluate_c3_3
from teoria_senales.exercises.convolution_pilot import ConvolutionPilot
from teoria_senales.signal_processing.convolution import (
    frequency_domain_convolution,
    linear_convolution,
    minimum_transform_length,
)
from teoria_senales.storage.json_repository import JsonSessionRepository
from teoria_senales.tracking.session_tracker import SessionTracker


def correct_evaluation_answers() -> dict[str, object]:
    return {
        "P1": [3, 3, 5],
        "P2": [1, 1, 1, 3, 2],
        "P3": [4, 3, 1],
        "P4": [1, 1, 1, 3, 2],
        "P5": "c",
        "P6": "b",
        "P7": False,
        "P8": True,
    }


class ConvolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.exercise = ConvolutionPilot()

    def test_approved_reference_values(self) -> None:
        self.assertEqual(linear_convolution(self.exercise.x, self.exercise.h).tolist(), [1, 1, 1, 3, 2])
        self.assertEqual(
            frequency_domain_convolution(self.exercise.x, self.exercise.h, 3).round(10).tolist(),
            [4, 3, 1],
        )
        self.assertEqual(
            frequency_domain_convolution(self.exercise.x, self.exercise.h, 5).round(10).tolist(),
            [1, 1, 1, 3, 2],
        )
        self.assertEqual(minimum_transform_length(self.exercise.x, self.exercise.h), 5)

    def test_validations_reject_incorrect_lengths(self) -> None:
        self.assertFalse(self.exercise.validate("paso_1", [3, 3, 4]))
        self.assertFalse(self.exercise.validate("paso_1", [3.2, 3, 5]))
        self.assertTrue(self.exercise.validate("paso_1", [3, 3, 5]))

    def test_numeric_steps_reject_invalid_text_without_failing(self) -> None:
        for step_id in ("paso_2", "paso_3", "paso_4"):
            with self.subTest(step_id=step_id):
                self.assertFalse(self.exercise.validate(step_id, "abc"))
                self.assertFalse(self.exercise.validate(step_id, "1, dos, 3"))
                self.assertFalse(self.exercise.validate(step_id, "   "))

    def test_numeric_steps_accept_common_sequence_formats(self) -> None:
        accepted_answers = {
            "paso_2": "[1, 1, 1, 3, 2]",
            "paso_3": "(4; 3; 1)",
            "paso_4": "1 1 1 3 2",
        }

        for step_id, answer in accepted_answers.items():
            with self.subTest(step_id=step_id, answer=answer):
                self.assertTrue(self.exercise.validate(step_id, answer))

    def test_numeric_steps_and_evaluation_use_the_same_tolerance(self) -> None:
        accepted_answer = "4.0000005, 3, 1"
        rejected_answer = "4.000002, 3, 1"

        self.assertTrue(self.exercise.validate("paso_3", accepted_answer))
        self.assertFalse(self.exercise.validate("paso_3", rejected_answer))
        self.assertTrue(
            evaluate_c3_3({"P3": accepted_answer}).questions[2].correct
        )
        self.assertFalse(
            evaluate_c3_3({"P3": rejected_answer}).questions[2].correct
        )

    def test_completed_step_does_not_register_a_duplicate_attempt(self) -> None:
        tracker = SessionTracker("Ana", "EST-003", self.exercise)
        definition = self.exercise.get_step("paso_2")
        first_attempt = tracker.register_attempt(
            "paso_2",
            "1, 1, 1, 3, 2",
            True,
            "Respuesta correcta.",
            definition.difficulty,
        )
        repeated_attempt = tracker.register_attempt(
            "paso_2",
            "1, 1, 1, 3, 2",
            True,
            "Respuesta correcta.",
            definition.difficulty,
        )

        self.assertIs(repeated_attempt, first_attempt)
        self.assertEqual(len(tracker.session.steps["paso_2"].attempts), 1)

    def test_same_orientation_is_registered_only_once(self) -> None:
        tracker = SessionTracker("Ana", "EST-004", self.exercise)
        hint = self.exercise.get_step("paso_3").hint

        tracker.register_help("paso_3", hint)
        tracker.register_help("paso_3", hint)

        step = tracker.session.steps["paso_3"]
        self.assertEqual(step.help_requests, [hint])
        self.assertEqual(step.status.value, "en_proceso")

    def test_demo_generates_structured_session_and_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            json_path, pdf_path = run_demo(temporary_directory)
            self.assertTrue(json_path.exists())
            self.assertTrue(pdf_path.exists())
            self.assertGreater(pdf_path.stat().st_size, 5_000)
            session_data = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(session_data["evaluation"]["points_earned"], 18)
            self.assertEqual(session_data["evaluation"]["points_possible"], 18)
            self.assertEqual(session_data["evaluation"]["grade"], 5.0)
            self.assertEqual(len(session_data["evaluation"]["questions"]), 8)
            self.assertNotIn("interpretation_answers", session_data)
            self.assertNotIn("conclusion", session_data)

    def test_incorrect_p5_does_not_change_cr3_or_cr4(self) -> None:
        tracker = SessionTracker("Ana", "EST-001", self.exercise)
        result = evaluate_c3_3(
            {
                "P1": [3, 3, 5],
                "P2": [1, 1, 1, 3, 2],
                "P3": [4, 3, 1],
                "P4": [1, 1, 1, 3, 2],
                "P5": "a",
                "P6": "b",
                "P7": False,
                "P8": True,
            }
        )
        tracker.record_evaluation(result)
        session = tracker.complete(self.exercise.expected_results)

        with tempfile.TemporaryDirectory() as temporary_directory:
            json_path = JsonSessionRepository(temporary_directory).save(session)
            session_data = json.loads(json_path.read_text(encoding="utf-8"))

        evaluation = session_data["evaluation"]
        self.assertEqual(evaluation["points_earned"], 16)
        self.assertEqual(evaluation["points_possible"], 18)
        self.assertEqual(evaluation["grade"], 4.44)
        self.assertEqual(
            [question["points_earned"] for question in evaluation["questions"]],
            [3, 3, 3, 3, 0, 2, 1, 1],
        )
        self.assertEqual(
            [criterion["criterion_id"] for criterion in evaluation["criteria"]],
            ["CR1", "CR2", "CR3", "CR4", "CR5", "CR6"],
        )
        criteria_evaluation = {
            criterion["criterion_id"]: criterion
            for criterion in evaluation["criteria"]
        }
        self.assertEqual(
            criteria_evaluation["CR3"]["question_ids"],
            ["P3"],
        )
        self.assertEqual(
            criteria_evaluation["CR4"]["question_ids"],
            ["P4"],
        )
        self.assertEqual(
            criteria_evaluation["CR5"]["question_ids"],
            ["P5", "P6"],
        )

        criteria = {
            criterion["criterion_id"]: criterion
            for criterion in session_data["criteria"]
        }
        self.assertEqual(criteria["CR2"]["status"], "alcanzado")
        self.assertEqual(criteria["CR3"]["status"], "alcanzado")
        self.assertEqual(criteria["CR4"]["status"], "alcanzado")
        self.assertEqual(criteria["CR5"]["status"], "requiere_refuerzo")
        self.assertEqual(criteria["CR6"]["status"], "alcanzado")
        self.assertEqual(
            session_data["steps"]["paso_5"]["status"],
            "completado",
        )
        self.assertEqual(
            len(session_data["steps"]["paso_5"]["attempts"]),
            1,
        )
        self.assertIsNotNone(session_data["finished_at"])

    def test_evaluation_completes_step_five_without_duplicate_records(self) -> None:
        tracker = SessionTracker("Ana", "EST-005", self.exercise)
        result = evaluate_c3_3(correct_evaluation_answers())

        first_record = tracker.record_evaluation(result)
        second_record = tracker.record_evaluation(result)
        step = tracker.session.steps["paso_5"]

        self.assertIs(second_record, first_record)
        self.assertEqual(step.status.value, "completado")
        self.assertEqual(len(step.attempts), 1)
        self.assertEqual(
            step.attempts[0].feedback,
            "Evaluación automática completada: 18/18 puntos.",
        )

    def test_repeated_student_code_creates_separate_session_files(self) -> None:
        first_tracker = SessionTracker("Ana", "EST-001", self.exercise)
        second_tracker = SessionTracker("Ana", "EST-001", self.exercise)

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = JsonSessionRepository(temporary_directory)
            first_path = repository.save(first_tracker.session)
            second_path = repository.save(second_tracker.session)

            self.assertNotEqual(first_path, second_path)
            self.assertTrue(first_path.exists())
            self.assertTrue(second_path.exists())
            self.assertIn(first_tracker.session.session_id, first_path.name)
            self.assertIn(second_tracker.session.session_id, second_path.name)

    def test_latest_incomplete_session_is_recovered(self) -> None:
        first_tracker = SessionTracker("Ana", "EST-002", self.exercise)
        second_tracker = SessionTracker("Ana", "EST-002", self.exercise)
        first_tracker.session.started_at = "2026-07-28T10:00:00-05:00"
        second_tracker.session.started_at = "2026-07-28T10:01:00-05:00"

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = JsonSessionRepository(temporary_directory)
            repository.save(first_tracker.session)
            expected_path = repository.save(second_tracker.session)
            recovered = repository.find_latest_incomplete("EST-002", "C3-3")

            self.assertIsNotNone(recovered)
            recovered_session, recovered_path = recovered
            self.assertEqual(
                recovered_session.session_id,
                second_tracker.session.session_id,
            )
            self.assertEqual(recovered_path, expected_path)

    def test_completed_evaluation_is_not_recovered_as_incomplete(self) -> None:
        tracker = SessionTracker("Ana", "EST-006", self.exercise)
        tracker.record_evaluation(
            evaluate_c3_3(correct_evaluation_answers())
        )
        tracker.complete(self.exercise.expected_results)

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = JsonSessionRepository(temporary_directory)
            repository.save(tracker.session)
            recovered = repository.find_latest_incomplete("EST-006", "C3-3")

        self.assertIsNone(recovered)


if __name__ == "__main__":
    unittest.main()
