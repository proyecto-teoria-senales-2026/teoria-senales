"""Pruebas de la sesión que inicia la interfaz gráfica."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.web_session import create_student_session


class WebSessionTests(unittest.TestCase):
    def test_student_code_is_required(self) -> None:
        with self.assertRaisesRegex(ValueError, "código estudiantil"):
            create_student_session("   ")

    def test_session_uses_the_entered_code_and_c3_3(self) -> None:
        tracker = create_student_session(" 202600123 ")
        session = tracker.session

        self.assertEqual(session.student_id, "202600123")
        self.assertEqual(session.exercise_id, "C3-3")
        self.assertEqual(len(session.steps), 5)
        self.assertIsNone(session.evaluation)

    def test_student_code_has_a_safe_technical_length(self) -> None:
        with self.assertRaisesRegex(ValueError, "máximo 40"):
            create_student_session("A" * 41)

    def test_student_code_rejects_unsafe_characters(self) -> None:
        with self.assertRaisesRegex(ValueError, "letras, números"):
            create_student_session("2026/001")
        with self.assertRaisesRegex(ValueError, "letras, números"):
            create_student_session("---")

    def test_student_code_accepts_common_safe_separators(self) -> None:
        tracker = create_student_session("ING-2026_001")
        self.assertEqual(tracker.session.student_id, "ING-2026_001")


if __name__ == "__main__":
    unittest.main()
