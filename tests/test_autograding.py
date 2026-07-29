"""Pruebas de la evaluación automática propuesta para el C3-3."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.evaluation.autograding import (
    QuestionType,
    evaluate_c3_3,
    get_c3_3_questions,
)
from teoria_senales.exercises.convolution_pilot import ConvolutionPilot


class C33AutogradingTests(unittest.TestCase):
    def test_question_configuration_has_eight_questions_and_eighteen_points(
        self,
    ) -> None:
        questions = get_c3_3_questions()

        self.assertEqual(len(questions), 8)
        self.assertEqual(sum(question.points for question in questions), 18)
        self.assertEqual(
            [question.question_type for question in questions],
            [
                QuestionType.NUMERIC,
                QuestionType.NUMERIC,
                QuestionType.NUMERIC,
                QuestionType.NUMERIC,
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.MULTIPLE_CHOICE,
                QuestionType.TRUE_FALSE,
                QuestionType.TRUE_FALSE,
            ],
        )
        self.assertEqual(
            [question.points for question in questions],
            [3, 3, 3, 3, 2, 2, 1, 1],
        )
        self.assertEqual(
            [question.criterion_ids for question in questions],
            [
                ("CR1",),
                ("CR2",),
                ("CR3",),
                ("CR4",),
                ("CR3", "CR4", "CR5"),
                ("CR5",),
                ("CR6",),
                ("CR6",),
            ],
        )
        self.assertTrue(all(question.rae_id == "RAE_C3" for question in questions))

    def test_all_correct_answers_produce_grade_five(self) -> None:
        result = evaluate_c3_3(
            {
                "P1": [3, 3, 5],
                "P2": [1, 1, 1, 3, 2],
                "P3": [4, 3, 1],
                "P4": [1, 1, 1, 3, 2],
                "P5": "C",
                "P6": "B",
                "P7": "Falso",
                "P8": "Verdadero",
            }
        )

        self.assertEqual(result.points_earned, 18)
        self.assertEqual(result.points_possible, 18)
        self.assertEqual(result.grade, 5.0)
        self.assertTrue(all(question.correct for question in result.questions))

    def test_numeric_answers_accept_common_sequence_formats(self) -> None:
        accepted_formats = (
            "[1, 1, 1, 3, 2]",
            "(1; 1; 1; 3; 2)",
            "1 1 1 3 2",
        )

        for answer in accepted_formats:
            with self.subTest(answer=answer):
                result = evaluate_c3_3({"P2": answer})
                self.assertTrue(result.questions[1].correct)

    def test_invalid_numeric_text_is_graded_incorrect_without_failing(self) -> None:
        result = evaluate_c3_3(
            {
                "P2": "abc",
                "P3": "4, tres, 1",
            }
        )

        self.assertFalse(result.questions[1].correct)
        self.assertFalse(result.questions[2].correct)
        self.assertEqual(result.points_earned, 0)
        self.assertEqual(result.grade, 0.0)

    def test_numeric_answers_come_from_the_exercise_configuration(self) -> None:
        exercise = ConvolutionPilot()
        questions = get_c3_3_questions()

        self.assertEqual(
            questions[0].expected_answer,
            (
                exercise.expected_results["Lx"],
                exercise.expected_results["Lh"],
                exercise.expected_results["Ly"],
            ),
        )
        self.assertEqual(
            questions[1].expected_answer,
            tuple(exercise.expected_results["convolucion_lineal"]),
        )
        self.assertEqual(
            questions[2].expected_answer,
            tuple(exercise.expected_results["resultado_N3"]),
        )
        self.assertEqual(
            questions[3].expected_answer,
            tuple(exercise.expected_results["resultado_N5"]),
        )
        self.assertIn(str(exercise.x.astype(int).tolist()), questions[1].prompt)
        self.assertIn(str(exercise.h.astype(int).tolist()), questions[1].prompt)

    def test_partial_answers_produce_proportional_grade(self) -> None:
        result = evaluate_c3_3(
            {
                "P1": [3, 3, 5],
                "P2": "1, 1, 1, 3, 2",
                "P3": [4, 3, 0],
                "P4": [1, 1, 1, 3, 0],
                "P5": "c",
                "P6": "a",
                "P7": False,
                "P8": False,
            }
        )

        self.assertEqual(result.points_earned, 9)
        self.assertEqual(result.grade, 2.5)
        self.assertEqual(
            [question.points_earned for question in result.questions],
            [3, 3, 0, 0, 2, 0, 1, 0],
        )

    def test_missing_or_incorrect_answers_produce_grade_zero(self) -> None:
        result = evaluate_c3_3(
            {
                "P1": [1, 1],
                "P5": "a",
                "P6": "d",
                "P7": "Verdadero",
                "P8": "Falso",
            }
        )

        self.assertEqual(result.points_earned, 0)
        self.assertEqual(result.grade, 0.0)
        self.assertFalse(any(question.correct for question in result.questions))

    def test_unknown_question_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "P9"):
            evaluate_c3_3({"P9": "respuesta"})


if __name__ == "__main__":
    unittest.main()
