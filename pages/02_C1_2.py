"""Interfaz guiada del ejercicio C1-2."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.web_session import (
    create_exercise_session,
    normalize_student_code,
    restore_exercise_session,
)
from teoria_senales.domain.models import StepStatus
from teoria_senales.evaluation.autograding import QuestionType
from teoria_senales.evaluation.c1_2_question_bank import (
    evaluate_c1_2,
    select_c1_2_questions,
)
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.reports.pdf_report import (
    generate_pdf_report_bytes,
    report_filename,
    report_verification_code,
)
from teoria_senales.storage.json_repository import JsonSessionRepository


SESSION_KEY = "c1_2_tracker"
SESSION_PATH_KEY = "c1_2_session_path"
RECOVERY_PATH_KEY = "c1_2_recovery_path"
RECOVERY_CODE_KEY = "c1_2_recovery_code"
LEAVE_CONFIRMATION_KEY = "c1_2_leave_confirmation"
GUIDED_STEP_IDS = ("paso_1", "paso_2", "paso_3", "paso_4")
SESSION_DIRECTORY = Path(
    os.environ.get("TEORIA_SENALES_SESSION_DIRECTORY", PROJECT_ROOT / "session_outputs")
)
HEADER_IMAGE = SRC / "teoria_senales" / "assets" / "encabezado_institucional.png"
STUDENT_GUIDE_PDF = PROJECT_ROOT / "docs" / "guias" / "Guia_del_estudiante_C-1-2.pdf"


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #f5f7fa; }
        .block-container { max-width: 820px; padding-top: 4.5rem; padding-bottom: 3rem; }
        [data-testid="stForm"] {
            background: #ffffff; border: 1px solid #dfe4ea;
            border-radius: 10px; padding: 1.4rem 1.4rem 0.6rem;
        }
        .exercise-label {
            color: #17426f; font-size: 0.9rem; font-weight: 700;
            letter-spacing: 0.03em; margin-bottom: 0.25rem; text-transform: uppercase;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_active_session() -> Path:
    tracker = st.session_state[SESSION_KEY]
    path = JsonSessionRepository(SESSION_DIRECTORY).save(tracker.session)
    st.session_state[SESSION_PATH_KEY] = str(path)
    return path


def activate_session(tracker, path: Path | None = None) -> None:
    st.session_state[SESSION_KEY] = tracker
    st.session_state[LEAVE_CONFIRMATION_KEY] = False
    if path is None:
        save_active_session()
    else:
        st.session_state[SESSION_PATH_KEY] = str(path)
    st.session_state.pop(RECOVERY_PATH_KEY, None)
    st.session_state.pop(RECOVERY_CODE_KEY, None)


def render_student_guide() -> None:
    with st.expander("Guía del estudiante C-1-2", expanded=False):
        st.markdown(
            """
            Reconoce y relaciona cinco características de las señales discretas:
            paridad, periodicidad, duración, energía y potencia.

            1. Clasifica dos secuencias como pares o impares.
            2. Determina el periodo de una senoidal y reconoce una señal aperiódica.
            3. Calcula la energía y la potencia media de una secuencia finita.
            4. Calcula la potencia de una señal periódica.
            5. Responde tres preguntas de selección múltiple y dos de verdadero/falso.
            """
        )
        st.latex(r"x[n]=x[-n]\quad\text{(par)}")
        st.latex(r"x[n]=-x[-n]\quad\text{(impar)}")
        st.latex(r"x[n+N_0]=x[n]")
        st.latex(r"E_x=\sum_{n=-\infty}^{\infty}|x[n]|^2")
        st.latex(r"P_x=\frac{1}{N_0}\sum_{n=0}^{N_0-1}|x[n]|^2")
        if STUDENT_GUIDE_PDF.is_file():
            st.download_button(
                "Descargar guía completa en PDF",
                data=STUDENT_GUIDE_PDF.read_bytes(),
                file_name=STUDENT_GUIDE_PDF.name,
                mime="application/pdf",
                key="download_c1_2_student_guide",
            )


def render_access_screen() -> None:
    st.markdown('<p class="exercise-label">Componente 1 · Ejercicio C-1-2</p>', unsafe_allow_html=True)
    st.title("Características de las señales discretas")
    st.write("Relaciona paridad, periodicidad, duración, energía y potencia mediante un recorrido guiado.")
    render_student_guide()
    if RECOVERY_PATH_KEY in st.session_state:
        render_recovery_choice()
        return
    with st.form("c1_2_access"):
        student_id = st.text_input("Código estudiantil")
        submitted = st.form_submit_button("Iniciar ejercicio C-1-2", type="primary", width="stretch")
    if not submitted:
        return
    try:
        normalized = normalize_student_code(student_id)
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        pending = repository.find_latest_incomplete(normalized, "C1-2")
        if pending is None:
            activate_session(create_exercise_session(normalized, "C1-2"))
        else:
            _, path = pending
            st.session_state[RECOVERY_CODE_KEY] = normalized
            st.session_state[RECOVERY_PATH_KEY] = str(path)
    except ValueError as error:
        st.error(str(error))
        return
    st.rerun()


def render_recovery_choice() -> None:
    student_id = st.session_state[RECOVERY_CODE_KEY]
    st.info(f"Encontramos una sesión C-1-2 sin finalizar para {student_id}.")
    left, right = st.columns(2)
    with left:
        continue_session = st.button("Continuar sesión", type="primary", width="stretch")
    with right:
        new_attempt = st.button("Iniciar nuevo intento", width="stretch")
    if continue_session:
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        path = Path(st.session_state[RECOVERY_PATH_KEY])
        activate_session(restore_exercise_session(repository.load(path)), path)
        st.rerun()
    if new_attempt:
        activate_session(create_exercise_session(student_id, "C1-2"))
        st.rerun()


def register_step_answer(tracker, step_id: str, answer: list[float]) -> None:
    definition = tracker.exercise.get_step(step_id)
    step = tracker.session.steps[step_id]
    correct = tracker.exercise.validate(step_id, answer)
    feedback = feedback_for_attempt(correct, len(step.attempts) + 1)
    tracker.register_attempt(step_id, answer, correct, feedback, definition.difficulty)
    save_active_session()
    if correct:
        st.rerun()
    st.error(feedback)


def render_help(tracker, step_id: str) -> None:
    step = tracker.session.steps[step_id]
    definition = tracker.exercise.get_step(step_id)
    completed = step.status == StepStatus.COMPLETED
    if st.button(
        f"Ver orientación del paso {step_id[-1]}",
        key=f"c1_2_help_{step_id}",
        disabled=completed or bool(step.help_requests),
    ):
        tracker.register_help(step_id, definition.hint)
        save_active_session()
        st.rerun()
    if step.help_requests and not completed:
        st.info(step.help_requests[-1])


def render_step_one(tracker) -> None:
    step = tracker.session.steps["paso_1"]
    completed = step.status == StepStatus.COMPLETED
    exercise = tracker.exercise
    st.progress(0.2, text="Paso 1 de 5 · Paridad")
    st.subheader("Clasifica señales pares e impares")
    st.table({
        "n": list(exercise.parity_indices),
        "x1[n]": list(exercise.even_signal),
        "x2[n]": list(exercise.odd_signal),
    })
    with st.form("c1_2_step_1"):
        first = st.radio("Clasificación de x1[n]", ("Par", "Impar", "Ninguna"), index=None, disabled=completed)
        second = st.radio("Clasificación de x2[n]", ("Par", "Impar", "Ninguna"), index=None, disabled=completed)
        submitted = st.form_submit_button("Verificar paridad", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (first, second):
            st.warning("Clasifica las dos señales antes de verificar.")
        else:
            codes = {"Par": 0.0, "Impar": 1.0, "Ninguna": 2.0}
            register_step_answer(tracker, "paso_1", [codes[first], codes[second]])
    render_help(tracker, "paso_1")


def render_step_two(tracker) -> None:
    step = tracker.session.steps["paso_2"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.4, text="Paso 2 de 5 · Periodicidad y duración")
    st.subheader("Reconoce periodicidad y duración")
    st.write("Para x[n] = cos((π/2)n), un periodo contiene las muestras [1, 0, -1, 0].")
    with st.form("c1_2_step_2"):
        period = st.number_input("Periodo fundamental N0", min_value=1, value=None, disabled=completed)
        exponential = st.radio("x[n] = (1/2)^n u[n] es:", ("Periódica", "Aperiódica"), index=None, disabled=completed)
        duration = st.radio("La senoidal periódica tiene duración:", ("Finita", "Infinita"), index=None, disabled=completed)
        submitted = st.form_submit_button("Verificar periodicidad", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (period, exponential, duration):
            st.warning("Completa las tres respuestas antes de verificar.")
        else:
            register_step_answer(tracker, "paso_2", [period, 0 if exponential == "Aperiódica" else 1, 1 if duration == "Infinita" else 0])
    render_help(tracker, "paso_2")


def render_step_three(tracker) -> None:
    step = tracker.session.steps["paso_3"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.6, text="Paso 3 de 5 · Energía")
    st.subheader("Calcula la energía de una secuencia finita")
    st.write("Usa x[n] = {1, -1, 2}, extendida con ceros fuera de sus tres muestras.")
    st.latex(r"E_x=|1|^2+|-1|^2+|2|^2")
    with st.form("c1_2_step_3"):
        energy = st.number_input("Energía Ex", value=None, disabled=completed)
        power = st.number_input("Potencia media Px", value=None, disabled=completed)
        submitted = st.form_submit_button("Verificar energía", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (energy, power):
            st.warning("Completa energía y potencia antes de verificar.")
        else:
            register_step_answer(tracker, "paso_3", [energy, power])
    render_help(tracker, "paso_3")


def render_step_four(tracker) -> None:
    step = tracker.session.steps["paso_4"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.8, text="Paso 4 de 5 · Potencia")
    st.subheader("Calcula la potencia de una señal periódica")
    st.write("Usa un periodo de x[n] = cos((π/2)n): [1, 0, -1, 0].")
    st.latex(r"P_x=\frac{1}{4}\sum_{n=0}^{3}|x[n]|^2")
    with st.form("c1_2_step_4"):
        power = st.number_input("Potencia media Px", value=None, disabled=completed)
        energy = st.radio("La energía total es:", ("Finita", "Infinita"), index=None, disabled=completed)
        duration = st.radio("La duración es:", ("Finita", "Infinita"), index=None, disabled=completed)
        submitted = st.form_submit_button("Verificar potencia", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (power, energy, duration):
            st.warning("Completa las tres respuestas antes de verificar.")
        else:
            register_step_answer(tracker, "paso_4", [power, 1 if energy == "Infinita" else 0, 1 if duration == "Infinita" else 0])
    render_help(tracker, "paso_4")


def render_evaluation(tracker) -> None:
    session = tracker.session
    st.progress(1.0, text="Paso 5 de 5 · Evaluación final")
    if session.evaluation is not None:
        evaluation = session.evaluation
        st.success(f"Evaluación completada: {evaluation.points_earned}/{evaluation.points_possible} puntos · Nota {evaluation.grade:.2f}".replace(".", ","))
        st.code(f"Código de verificación: {report_verification_code(session)}", language=None)
        st.download_button("Descargar reporte docente PDF", data=generate_pdf_report_bytes(session), file_name=report_filename(session), mime="application/pdf", type="primary", width="stretch")
        return
    st.subheader("Comprueba lo aprendido")
    questions = select_c1_2_questions(session.session_id)
    answers: dict[str, object] = {}
    with st.form("c1_2_final_evaluation"):
        for question in questions:
            st.markdown(f"**{question.question_id}**  \n{question.prompt}")
            if question.question_type is QuestionType.MULTIPLE_CHOICE:
                labels = tuple(f"{code.upper()}. {text}" for code, text in question.options)
                selected = st.radio(f"Selecciona una respuesta en {question.question_id}", labels, index=None, key=f"c1_2_eval_{question.question_id}")
                answers[question.question_id] = selected[0].casefold() if selected else None
            else:
                selected = st.radio(f"Selecciona una respuesta en {question.question_id}", ("Verdadero", "Falso"), index=None, horizontal=True, key=f"c1_2_eval_{question.question_id}")
                answers[question.question_id] = selected == "Verdadero" if selected else None
        submitted = st.form_submit_button("Calificar evaluación", type="primary", width="stretch")
    if submitted:
        missing = [question_id for question_id, answer in answers.items() if answer is None]
        if missing:
            st.warning(f"Responde todas las preguntas antes de calificar: {', '.join(missing)}.")
            return
        result = evaluate_c1_2(questions, answers)
        tracker.record_evaluation(result)
        tracker.complete(tracker.exercise.expected_results)
        save_active_session()
        st.rerun()


def render_active_session() -> None:
    tracker = st.session_state[SESSION_KEY]
    session = tracker.session
    st.markdown('<p class="exercise-label">Componente 1 · Ejercicio C-1-2</p>', unsafe_allow_html=True)
    st.title("Características de las señales discretas")
    st.caption(f"Código estudiantil: {session.student_id}")
    render_student_guide()
    active_step = next((step_id for step_id in GUIDED_STEP_IDS if session.steps[step_id].status != StepStatus.COMPLETED), None)
    if active_step is None:
        render_evaluation(tracker)
    else:
        renderers = {"paso_1": render_step_one, "paso_2": render_step_two, "paso_3": render_step_three, "paso_4": render_step_four}
        renderers[active_step](tracker)
    if not st.session_state.get(LEAVE_CONFIRMATION_KEY, False):
        if st.button("Guardar y volver al inicio", key="c1_2_return"):
            st.session_state[LEAVE_CONFIRMATION_KEY] = True
            st.rerun()
        return
    st.warning("¿Quieres guardar la sesión y salir del ejercicio C-1-2?")
    left, right = st.columns(2)
    with left:
        leave = st.button("Sí, guardar y salir", type="primary", width="stretch")
    with right:
        cancel = st.button("Continuar ejercicio", width="stretch")
    if leave:
        save_active_session()
        for key in (SESSION_KEY, SESSION_PATH_KEY, LEAVE_CONFIRMATION_KEY):
            st.session_state.pop(key, None)
        st.rerun()
    if cancel:
        st.session_state[LEAVE_CONFIRMATION_KEY] = False
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="Ejercicio C-1-2 | Teoría de Señales", page_icon="📊", layout="centered")
    apply_styles()
    if HEADER_IMAGE.is_file():
        st.image(str(HEADER_IMAGE), width="stretch")
    if SESSION_KEY in st.session_state:
        render_active_session()
    else:
        render_access_screen()


if __name__ == "__main__":
    main()
