import unittest

from teoria_senales.app.web_session import exercise_for_id, normalize_student_code
from teoria_senales.domain.nomenclature import inconsistent_visible_symbols, visible_exercise_id
from teoria_senales.evaluation.autograding import evaluate_c3_3, get_c3_3_questions
from teoria_senales.evaluation.c1_1_question_bank import select_c1_1_questions
from teoria_senales.evaluation.c1_2_question_bank import select_c1_2_questions
from teoria_senales.evaluation.c1_3_question_bank import select_c1_3_questions
from teoria_senales.evaluation.c1_4_question_bank import select_c1_4_questions


class NomenclatureTests(unittest.TestCase):
    def test_visible_ids(self):
        for internal, visible in {
            "C1-1": "C-1-1",
            "C1-2": "C-1-2",
            "C1-3": "C-1-3",
            "C1-4": "C-1-4",
            "C3-3": "C-3-3",
        }.items():
            with self.subTest(internal=internal):
                self.assertEqual(visible_exercise_id(internal), visible)

    def test_visible_symbols(self):
        self.assertEqual(inconsistent_visible_symbols(["L_x, L_h y L_y"]), ())
        self.assertEqual(inconsistent_visible_symbols(["Lx, Lh y Ly"]), ("Lx", "Lh", "Ly"))

    def test_student_code_is_normalized(self):
        self.assertEqual(normalize_student_code("  2026-01_A  "), "2026-01_A")

    def test_invalid_student_code_is_rejected(self):
        for value in ("", "código con espacios", "***"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_student_code(value)

    def test_supported_exercises(self):
        for exercise_id in ("C1-1", "C1-2", "C1-3", "C1-4", "C3-3"):
            with self.subTest(exercise_id=exercise_id):
                self.assertEqual(exercise_for_id(exercise_id).exercise_id, exercise_id)


class QuestionBankTests(unittest.TestCase):
    def test_each_component_one_bank_selects_five(self):
        selectors = (
            select_c1_1_questions,
            select_c1_2_questions,
            select_c1_3_questions,
            select_c1_4_questions,
        )
        for selector in selectors:
            with self.subTest(selector=selector.__name__):
                self.assertEqual(len(selector("session-seed")), 5)

    def test_selection_is_reproducible(self):
        first = [q.question_id for q in select_c1_1_questions("same")]
        second = [q.question_id for q in select_c1_1_questions("same")]
        self.assertEqual(first, second)

    def test_selected_question_ids_follow_convention(self):
        for prefix, selector in (
            ("C1-1-P", select_c1_1_questions),
            ("C1-2-P", select_c1_2_questions),
            ("C1-3-P", select_c1_3_questions),
            ("C1-4-P", select_c1_4_questions),
        ):
            with self.subTest(prefix=prefix):
                self.assertTrue(all(q.question_id.startswith(prefix) for q in selector("qa")))

    def test_c3_3_has_eight_questions(self):
        questions = get_c3_3_questions()
        self.assertEqual(len(questions), 8)
        self.assertEqual([q.question_id for q in questions], [f"C3-3-P{i:02d}" for i in range(1, 9)])

    def test_c3_3_perfect_score(self):
        result = evaluate_c3_3(
            {
                "C3-3-P01": [3, 3, 5],
                "C3-3-P02": [1, 1, 1, 3, 2],
                "C3-3-P03": [4, 3, 1],
                "C3-3-P04": [1, 1, 1, 3, 2],
                "C3-3-P05": "c",
                "C3-3-P06": "b",
                "C3-3-P07": False,
                "C3-3-P08": True,
            }
        )
        self.assertEqual(result.points_earned, result.points_possible)


if __name__ == "__main__":
    unittest.main()
