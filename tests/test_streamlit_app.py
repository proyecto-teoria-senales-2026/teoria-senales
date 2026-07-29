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

    @staticmethod
    def find_text_input(app: AppTest, label: str):
        return next(
            text_input
            for text_input in app.text_input
            if text_input.label == label
        )

    def advance_to_final_evaluation(self, app: AppTest) -> None:
        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        self.find_text_input(
            app,
            "Resultado de la convolución lineal",
        ).set_value("1 1 1 3 2")
        self.find_button(app, "Verificar convolución lineal").click()
        app.run(timeout=10)

        self.find_text_input(
            app,
            "Resultado temporal mediante DFT/FFT con N = 3",
        ).set_value("4 3 1")
        self.find_button(app, "Verificar resultado con N = 3").click()
        app.run(timeout=10)

        self.find_text_input(
            app,
            "Resultado temporal mediante DFT/FFT con N = 5",
        ).set_value("1 1 1 3 2")
        self.find_button(app, "Verificar resultado con N = 5").click()
        app.run(timeout=10)
        self.find_button(app, "Iniciar evaluación").click()
        app.run(timeout=10)

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
            [r"$L_x$", r"$L_h$", r"$L_y$"],
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
            any(
                "Paso 1" in expander.label and "completado" in expander.label
                for expander in app.expander
            )
        )
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_1"]
        self.assertEqual(len(step.attempts), 1)
        self.assertTrue(step.attempts[0].correct)
        self.assertNotIn(
            "Verificar respuesta",
            [button.label for button in app.button],
        )
        self.assertEqual(
            len(
                app.session_state["c3_3_tracker"]
                .session.steps["paso_1"]
                .attempts
            ),
            1,
        )

    def test_completed_steps_are_compact_and_only_current_step_is_editable(
        self,
    ) -> None:
        app = self.create_app()
        app.text_input[0].set_value("FLUJO-COMPACTO")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        self.assertEqual(len(app.expander), 1)
        self.assertIn("Paso 1", app.expander[0].label)
        self.assertEqual(len(app.number_input), 0)
        self.assertEqual(
            [text_input.label for text_input in app.text_input],
            ["Resultado de la convolución lineal"],
        )
        self.assertNotIn(
            "Verificar respuesta",
            [button.label for button in app.button],
        )

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
        self.assertTrue(
            self.find_button(app, "Ver orientación").disabled
        )

        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_1"]
        self.assertEqual(len(step.attempts), 2)
        self.assertTrue(step.attempts[-1].correct)

    def test_second_step_registers_attempts_help_and_correct_result(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("PASO2-001")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        self.assertEqual(
            [text_input.label for text_input in app.text_input],
            ["Resultado de la convolución lineal"],
        )
        app.text_input[0].set_value("1, 1, 1, 3, 0")
        self.find_button(app, "Verificar convolución lineal").click()
        app.run(timeout=10)

        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_2"]
        self.assertEqual(len(step.attempts), 1)
        self.assertFalse(step.attempts[0].correct)
        self.assertEqual(step.corrections, 1)

        self.find_button(app, "Ver orientación del paso 2").click()
        app.run(timeout=10)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_2"]
        self.assertEqual(len(step.help_requests), 1)
        self.assertTrue(
            any(
                "productos muestra por muestra" in info.value
                for info in app.info
            )
        )

        app.text_input[0].set_value("[1; 1; 1; 3; 2]")
        self.find_button(app, "Verificar convolución lineal").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_2"]
        self.assertEqual(len(step.attempts), 2)
        self.assertTrue(step.attempts[-1].correct)
        self.assertTrue(
            any(
                "Paso 2" in expander.label and "completado" in expander.label
                for expander in app.expander
            )
        )
        self.assertTrue(
            any(
                "Resultado: 1, 1, 1, 3, 2" in markdown.value
                for markdown in app.markdown
            )
        )
        self.assertNotIn(
            "Verificar convolución lineal",
            [button.label for button in app.button],
        )
        self.assertEqual(
            len(
                app.session_state["c3_3_tracker"]
                .session.steps["paso_2"]
                .attempts
            ),
            2,
        )

    def test_second_step_rejects_non_numeric_text_without_registering_it(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("PASO2-TEXTO")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        app.text_input[0].set_value("abc")
        self.find_button(app, "Verificar convolución lineal").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertTrue(
            any("únicamente valores numéricos" in warning.value for warning in app.warning)
        )
        tracker = app.session_state["c3_3_tracker"]
        self.assertEqual(len(tracker.session.steps["paso_2"].attempts), 0)

    def test_third_step_registers_fft_result_and_circular_warning(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("PASO3-001")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        app.text_input[-1].set_value("1 1 1 3 2")
        self.find_button(app, "Verificar convolución lineal").click()
        app.run(timeout=10)

        self.assertEqual(
            app.text_input[-1].label,
            "Resultado temporal mediante DFT/FFT con N = 3",
        )
        app.text_input[-1].set_value("4, 3, 0")
        self.find_button(app, "Verificar resultado con N = 3").click()
        app.run(timeout=10)

        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_3"]
        self.assertEqual(len(step.attempts), 1)
        self.assertFalse(step.attempts[0].correct)

        self.find_button(app, "Ver orientación del paso 3").click()
        app.run(timeout=10)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_3"]
        self.assertEqual(len(step.help_requests), 1)
        self.assertTrue(
            any("solapamiento circular" in info.value for info in app.info)
        )

        app.text_input[-1].set_value("(4; 3; 1)")
        self.find_button(app, "Verificar resultado con N = 3").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_3"]
        self.assertEqual(len(step.attempts), 2)
        self.assertTrue(step.attempts[-1].correct)
        self.assertTrue(
            any(
                "Paso 3" in expander.label and "completado" in expander.label
                for expander in app.expander
            )
        )
        self.assertTrue(
            any("solapamiento circular" in caption.value for caption in app.caption)
        )
        self.assertNotIn(
            "Verificar resultado con N = 3",
            [button.label for button in app.button],
        )
        self.assertEqual(
            len(
                app.session_state["c3_3_tracker"]
                .session.steps["paso_3"]
                .attempts
            ),
            2,
        )

    def test_fourth_step_confirms_zero_padding_result(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("PASO4-001")
        app.button[0].click()
        app.run(timeout=10)

        app.number_input[0].set_value(3)
        app.number_input[1].set_value(3)
        app.number_input[2].set_value(5)
        self.find_button(app, "Verificar respuesta").click()
        app.run(timeout=10)

        app.text_input[-1].set_value("1 1 1 3 2")
        self.find_button(app, "Verificar convolución lineal").click()
        app.run(timeout=10)
        app.text_input[-1].set_value("4 3 1")
        self.find_button(app, "Verificar resultado con N = 3").click()
        app.run(timeout=10)

        self.assertEqual(
            app.text_input[-1].label,
            "Resultado temporal mediante DFT/FFT con N = 5",
        )
        app.text_input[-1].set_value("1, 1, 1, 3, 0")
        self.find_button(app, "Verificar resultado con N = 5").click()
        app.run(timeout=10)

        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_4"]
        self.assertEqual(len(step.attempts), 1)
        self.assertFalse(step.attempts[0].correct)

        self.find_button(app, "Ver orientación del paso 4").click()
        app.run(timeout=10)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_4"]
        self.assertEqual(len(step.help_requests), 1)
        self.assertTrue(
            any("cinco muestras" in info.value for info in app.info)
        )

        app.text_input[-1].set_value("{1; 1; 1; 3; 2}")
        self.find_button(app, "Verificar resultado con N = 5").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        tracker = app.session_state["c3_3_tracker"]
        step = tracker.session.steps["paso_4"]
        self.assertEqual(len(step.attempts), 2)
        self.assertTrue(step.attempts[-1].correct)
        self.assertTrue(
            any(
                "coincide con la convolución lineal" in message.value
                for message in app.success
            )
        )
        self.assertIn(
            "Iniciar evaluación",
            [button.label for button in app.button],
        )
        self.assertNotIn(
            "Verificar resultado con N = 5",
            [button.label for button in app.button],
        )
        self.assertEqual(
            len(
                app.session_state["c3_3_tracker"]
                .session.steps["paso_4"]
                .attempts
            ),
            2,
        )

    def test_recovery_restores_the_guided_steps(self) -> None:
        first_app = self.create_app()
        first_app.text_input[0].set_value("RECUPERAR-GUIADO")
        first_app.button[0].click()
        first_app.run(timeout=10)

        first_app.number_input[0].set_value(3)
        first_app.number_input[1].set_value(3)
        first_app.number_input[2].set_value(5)
        self.find_button(first_app, "Verificar respuesta").click()
        first_app.run(timeout=10)

        first_app.text_input[-1].set_value("1 1 1 3 2")
        self.find_button(first_app, "Verificar convolución lineal").click()
        first_app.run(timeout=10)

        first_app.text_input[-1].set_value("4 3 0")
        self.find_button(first_app, "Verificar resultado con N = 3").click()
        first_app.run(timeout=10)
        self.find_button(first_app, "Ver orientación del paso 3").click()
        first_app.run(timeout=10)
        first_app.text_input[-1].set_value("4 3 1")
        self.find_button(first_app, "Verificar resultado con N = 3").click()
        first_app.run(timeout=10)

        first_app.text_input[-1].set_value("1 1 1 3 2")
        self.find_button(first_app, "Verificar resultado con N = 5").click()
        first_app.run(timeout=10)
        original_id = first_app.session_state["c3_3_tracker"].session.session_id

        recovered_app = self.create_app()
        recovered_app.text_input[0].set_value("RECUPERAR-GUIADO")
        recovered_app.button[0].click()
        recovered_app.run(timeout=10)
        self.find_button(recovered_app, "Continuar sesión").click()
        recovered_app.run(timeout=10)

        self.assertFalse(recovered_app.exception)
        tracker = recovered_app.session_state["c3_3_tracker"]
        self.assertEqual(tracker.session.session_id, original_id)
        self.assertEqual(len(recovered_app.text_input), 0)
        self.assertEqual(len(recovered_app.expander), 3)
        self.assertIn(
            "Iniciar evaluación",
            [button.label for button in recovered_app.button],
        )
        for step_id in ("paso_2", "paso_3", "paso_4"):
            answer = tracker.session.steps[step_id].attempts[-1].answer
            self.assertTrue(tracker.exercise.validate(step_id, answer))
        self.assertEqual(
            len(tracker.session.steps["paso_3"].attempts),
            2,
        )
        self.assertEqual(
            len(tracker.session.steps["paso_3"].help_requests),
            1,
        )

    def test_final_evaluation_requires_all_four_answers(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("EVALUACION-INCOMPLETA")
        app.button[0].click()
        app.run(timeout=10)
        self.advance_to_final_evaluation(app)

        self.find_button(app, "Calificar evaluación").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertTrue(
            any("Completa P1 y P2" in warning.value for warning in app.warning)
        )
        tracker = app.session_state["c3_3_tracker"]
        self.assertIsNone(tracker.session.evaluation)
        self.assertEqual(
            len(tracker.session.steps["paso_5"].attempts),
            0,
        )

    def test_evaluation_hides_guided_results_and_waits_for_confirmation(
        self,
    ) -> None:
        app = self.create_app()
        app.text_input[0].set_value("EVALUACION-REVISION")
        app.button[0].click()
        app.run(timeout=10)
        self.advance_to_final_evaluation(app)

        self.assertEqual(len(app.expander), 4)
        self.assertEqual(
            [text_input.label for text_input in app.text_input],
            ["Respuesta numérica P1", "Respuesta numérica P2"],
        )
        visible_text = "\n".join(
            element.value
            for collection in (
                app.markdown,
                app.caption,
                app.info,
                app.success,
            )
            for element in collection
        )
        self.assertNotIn("Resultado: 1, 1, 1, 3, 2", visible_text)
        self.assertNotIn("solapamiento circular", visible_text)
        self.assertNotIn(
            "el resultado coincide con la convolución lineal",
            visible_text,
        )

        self.find_text_input(app, "Respuesta numérica P1").set_value(
            "1, 1, 1, 3, 2"
        )
        self.find_text_input(app, "Respuesta numérica P2").set_value("4, 3, 1")
        app.radio[0].set_value(
            next(option for option in app.radio[0].options if option.startswith("C."))
        )
        app.radio[1].set_value("Verdadero")
        self.find_button(app, "Calificar evaluación").click()
        app.run(timeout=10)

        self.assertIsNone(
            app.session_state["c3_3_tracker"].session.evaluation
        )
        self.assertIn(
            "Volver a editar",
            [button.label for button in app.button],
        )
        self.assertIn(
            "Confirmar y calificar",
            [button.label for button in app.button],
        )
        self.find_button(app, "Volver a editar").click()
        app.run(timeout=10)
        self.assertEqual(
            [
                self.find_text_input(app, "Respuesta numérica P1").value,
                self.find_text_input(app, "Respuesta numérica P2").value,
            ],
            ["1, 1, 1, 3, 2", "4, 3, 1"],
        )

    def test_final_evaluation_requires_both_selected_answers(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("EVALUACION-SELECCIONES")
        app.button[0].click()
        app.run(timeout=10)
        self.advance_to_final_evaluation(app)

        self.find_text_input(app, "Respuesta numérica P1").set_value(
            "1, 1, 1, 3, 2"
        )
        self.find_text_input(app, "Respuesta numérica P2").set_value("4, 3, 1")
        self.find_button(app, "Calificar evaluación").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        self.assertTrue(
            any(
                "Selecciona una respuesta en P3 y P4" in warning.value
                for warning in app.warning
            )
        )
        tracker = app.session_state["c3_3_tracker"]
        self.assertIsNone(tracker.session.evaluation)
        self.assertIsNone(tracker.session.finished_at)

    def test_final_evaluation_calculates_grade_and_finishes_session(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("EVALUACION-COMPLETA")
        app.button[0].click()
        app.run(timeout=10)
        self.advance_to_final_evaluation(app)

        self.find_text_input(app, "Respuesta numérica P1").set_value(
            "1, 1, 1, 3, 2"
        )
        self.find_text_input(app, "Respuesta numérica P2").set_value("4, 3, 1")
        app.radio[0].set_value(
            next(option for option in app.radio[0].options if option.startswith("C."))
        )
        app.radio[1].set_value("Verdadero")
        self.find_button(app, "Calificar evaluación").click()
        app.run(timeout=10)

        self.assertIsNone(
            app.session_state["c3_3_tracker"].session.evaluation
        )
        self.assertIn(
            "Confirmar y calificar",
            [button.label for button in app.button],
        )
        self.find_button(app, "Confirmar y calificar").click()
        app.run(timeout=10)

        self.assertFalse(app.exception)
        tracker = app.session_state["c3_3_tracker"]
        evaluation = tracker.session.evaluation
        self.assertIsNotNone(evaluation)
        self.assertEqual(evaluation.points_earned, 9)
        self.assertEqual(evaluation.points_possible, 9)
        self.assertEqual(evaluation.grade, 5.0)
        self.assertIsNotNone(tracker.session.finished_at)
        self.assertEqual(
            tracker.session.steps["paso_5"].status.value,
            "completado",
        )
        self.assertEqual(len(tracker.session.steps["paso_5"].attempts), 1)
        self.assertTrue(
            any(
                "Evaluación finalizada" in success.value
                for success in app.success
            )
        )
        self.assertNotIn(
            "Calificar evaluación",
            [button.label for button in app.button],
        )
        self.assertEqual(
            len(
                app.session_state["c3_3_tracker"]
                .session.steps["paso_5"]
                .attempts
            ),
            1,
        )

    def test_final_evaluation_applies_proportional_grade(self) -> None:
        app = self.create_app()
        app.text_input[0].set_value("EVALUACION-PARCIAL")
        app.button[0].click()
        app.run(timeout=10)
        self.advance_to_final_evaluation(app)

        self.find_text_input(app, "Respuesta numérica P1").set_value(
            "1, 1, 1, 3, 2"
        )
        self.find_text_input(app, "Respuesta numérica P2").set_value("4, 3, 0")
        app.radio[0].set_value(
            next(option for option in app.radio[0].options if option.startswith("C."))
        )
        app.radio[1].set_value("Falso")
        self.find_button(app, "Calificar evaluación").click()
        app.run(timeout=10)
        self.find_button(app, "Confirmar y calificar").click()
        app.run(timeout=10)

        evaluation = app.session_state["c3_3_tracker"].session.evaluation
        self.assertEqual(evaluation.points_earned, 5)
        self.assertEqual(evaluation.grade, 2.78)
        self.assertEqual(
            [question.points_earned for question in evaluation.questions],
            [3, 0, 2, 0],
        )

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
        self.assertEqual(len(recovered_app.number_input), 0)
        self.assertEqual(len(recovered_app.expander), 1)
        self.assertIn("Paso 1", recovered_app.expander[0].label)
        self.assertTrue(
            any(
                "$L_x=3$" in markdown.value
                and "$L_h=3$" in markdown.value
                and "$L_y=5$" in markdown.value
                for markdown in recovered_app.markdown
            )
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
