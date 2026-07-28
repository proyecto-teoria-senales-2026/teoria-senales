"""Pruebas del primer acceso desde la interfaz Streamlit."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    from streamlit.testing.v1 import AppTest
except ModuleNotFoundError:
    AppTest = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(AppTest is None, "Streamlit no está instalado.")
class StreamlitAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.environment = patch.dict(
            os.environ,
            {
                "TEORIA_SENALES_SESSION_DIRECTORY": (
                    self.temporary_directory.name
                )
            },
        )
        self.environment.start()

    def tearDown(self) -> None:
        self.environment.stop()
        self.temporary_directory.cleanup()

    def create_app(self) -> AppTest:
        app = AppTest.from_file(str(PROJECT_ROOT / "app.py"))
        app.run(timeout=10)
        self.assertFalse(app.exception)
        return app

    @staticmethod
    def find_button(app: AppTest, label: str):
        return next(button for button in app.button if button.label == label)

    def test_student_can_start_a_session(self) -> None:
        app = self.create_app()

        self.assertEqual(app.text_input[0].label, "Código estudiantil")
        self.assertEqual(app.button[0].label, "Iniciar ejercicio")

        app.text_input[0].set_value("202600123")
        app.button[0].click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertEqual(
            [number_input.label for number_input in app.number_input],
            ["Lx", "Lh", "Ly"],
        )
        self.assertIn("Verificar respuesta", [button.label for button in app.button])
        self.assertIn("Ver orientación", [button.label for button in app.button])
        self.assertIn("Volver al inicio", [button.label for button in app.button])
        self.assertTrue(
            any("x[n]" in markdown.value for markdown in app.markdown)
        )
        self.assertTrue(
            any("h[n]" in markdown.value for markdown in app.markdown)
        )
        tracker = app.session_state["c3_3_tracker"]
        session_path = Path(app.session_state["c3_3_session_path"])
        self.assertTrue(session_path.exists())
        self.assertEqual(
            session_path.parent,
            Path(self.temporary_directory.name),
        )
        self.assertIn(tracker.session.session_id, session_path.name)

    def test_empty_code_does_not_create_a_session(self) -> None:
        app = self.create_app()

        app.text_input[0].set_value("   ")
        app.button[0].click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertIn("código estudiantil", app.error[0].value)

    def test_invalid_code_shows_a_clear_message(self) -> None:
        app = self.create_app()

        app.text_input[0].set_value("2026/001")
        app.button[0].click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertIn("letras, números", app.error[0].value)

    def test_first_step_registers_a_correct_answer(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("202600123")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertTrue(
            any("Paso 1 completado" in message.value for message in app.success)
        )
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_1"]
        self.assertEqual(len(step.attempts), 1)
        self.assertTrue(step.attempts[0].correct)

    def test_incomplete_answer_is_not_registered(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("202600123")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertIn("tres longitudes", app.warning[0].value)
        tracker = app.session_state["c3_3_tracker"]
        self.assertEqual(len(tracker.session.steps["paso_1"].attempts), 0)

    def test_first_step_keeps_help_and_retry_in_the_session(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("202600123")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(4)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_1"]
        self.assertFalse(step.attempts[0].correct)
        self.assertEqual(step.corrections, 1)

        self.find_button(app, "Ver orientación").click()
        app.run(timeout=10)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_1"]
        self.assertEqual(len(step.help_requests), 1)
        self.assertTrue(any("L_y" in info.value for info in app.info))

        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_1"]
        self.assertEqual(len(step.attempts), 2)
        self.assertTrue(step.attempts[-1].correct)

    def test_return_to_start_requires_confirmation(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("SALIDA-001")
        app.button[0].click()
        app.run(timeout=10)

        self.find_button(app, "Volver al inicio").click()
        app.run(timeout=10)

        self.assertIn("c3_3_tracker", app.session_state)
        self.assertTrue(
            any(
                "La sesión se guardará" in warning.value
                for warning in app.warning
            )
        )
        self.assertIn(
            "Guardar y volver al inicio",
            [button.label for button in app.button],
        )
        self.assertIn(
            "Continuar ejercicio",
            [button.label for button in app.button],
        )

        self.find_button(app, "Continuar ejercicio").click()
        app.run(timeout=10)
        self.assertIn("c3_3_tracker", app.session_state)
        self.assertIn("Volver al inicio", [button.label for button in app.button])

    def test_confirmed_exit_saves_before_returning_to_start(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("SALIDA-002")
        app.button[0].click()
        app.run(timeout=10)
        session_path = Path(app.session_state["c3_3_session_path"])

        self.find_button(app, "Volver al inicio").click()
        app.run(timeout=10)
        self.find_button(app, "Guardar y volver al inicio").click()
        app.run(timeout=10)

        self.assertNotIn("c3_3_tracker", app.session_state)
        self.assertEqual(app.text_input[0].label, "Código estudiantil")
        self.assertTrue(session_path.exists())

    def test_incomplete_session_can_be_recovered(self) -> None:
        first_app = self.create_app()
        first_app.text_input[0].set_value("RECUPERAR-001")
        first_app.button[0].click()
        first_app.run(timeout=10)
        first_app.number_input[0].set_value(3)
        first_app.number_input[1].set_value(3)
        first_app.number_input[2].set_value(4)
        self.find_button(first_app, "Verificar respuesta").click()
        first_app.run(timeout=10)

        original_tracker = first_app.session_state["c3_3_tracker"]
        original_id = original_tracker.session.session_id

        recovered_app = self.create_app()
        recovered_app.text_input[0].set_value("RECUPERAR-001")
        recovered_app.button[0].click()
        recovered_app.run(timeout=10)

        self.assertIn(
            "Continuar sesión",
            [button.label for button in recovered_app.button],
        )
        self.assertIn(
            "Iniciar nuevo intento",
            [button.label for button in recovered_app.button],
        )

        self.find_button(recovered_app, "Continuar sesión").click()
        recovered_app.run(timeout=10)
        tracker = recovered_app.session_state["c3_3_tracker"]

        self.assertEqual(tracker.session.session_id, original_id)
        self.assertEqual(len(tracker.session.steps["paso_1"].attempts), 1)
        self.assertFalse(tracker.session.steps["paso_1"].attempts[0].correct)

    def test_completed_step_shows_recovered_answers(self) -> None:
        first_app = self.create_app()
        first_app.text_input[0].set_value("RECUPERAR-VALORES")
        first_app.button[0].click()
        first_app.run(timeout=10)
        first_app.number_input[0].set_value(3)
        first_app.number_input[1].set_value(3)
        first_app.number_input[2].set_value(5)
        self.find_button(first_app, "Verificar respuesta").click()
        first_app.run(timeout=10)

        recovered_app = self.create_app()
        recovered_app.text_input[0].set_value("RECUPERAR-VALORES")
        recovered_app.button[0].click()
        recovered_app.run(timeout=10)
        self.find_button(recovered_app, "Continuar sesión").click()
        recovered_app.run(timeout=10)

        self.assertFalse(recovered_app.exception)
        self.assertEqual(
            [number_input.value for number_input in recovered_app.number_input],
            [3, 3, 5],
        )
        self.assertTrue(
            all(number_input.disabled for number_input in recovered_app.number_input)
        )

    def test_student_can_start_a_new_attempt_instead_of_recovering(self) -> None:
        first_app = self.create_app()
        first_app.text_input[0].set_value("RECUPERAR-002")
        first_app.button[0].click()
        first_app.run(timeout=10)
        original_id = first_app.session_state["c3_3_tracker"].session.session_id

        new_app = self.create_app()
        new_app.text_input[0].set_value("RECUPERAR-002")
        new_app.button[0].click()
        new_app.run(timeout=10)
        self.find_button(new_app, "Iniciar nuevo intento").click()
        new_app.run(timeout=10)
        new_id = new_app.session_state["c3_3_tracker"].session.session_id

        self.assertNotEqual(new_id, original_id)


if __name__ == "__main__":
    unittest.main()
