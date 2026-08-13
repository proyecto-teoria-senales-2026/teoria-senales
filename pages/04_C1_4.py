"""Interfaz guiada del ejercicio C1-4."""

from __future__ import annotations

import os
import sys
from math import pi
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.web_session import create_exercise_session, normalize_student_code, restore_exercise_session
from teoria_senales.domain.models import StepStatus
from teoria_senales.evaluation.autograding import QuestionType
from teoria_senales.evaluation.c1_4_question_bank import evaluate_c1_4, select_c1_4_questions
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.reports.pdf_report import generate_pdf_report_bytes, report_filename, report_verification_code
from teoria_senales.signal_processing.fourier_reconstruction import reconstruct_rectangular_pulse, rectangular_periodic_signal
from teoria_senales.storage.json_repository import JsonSessionRepository


SESSION_KEY = "c1_4_tracker"
SESSION_PATH_KEY = "c1_4_session_path"
RECOVERY_PATH_KEY = "c1_4_recovery_path"
RECOVERY_CODE_KEY = "c1_4_recovery_code"
LEAVE_CONFIRMATION_KEY = "c1_4_leave_confirmation"
GUIDED_STEP_IDS = ("paso_1", "paso_2", "paso_3", "paso_4")
SESSION_DIRECTORY = Path(os.environ.get("TEORIA_SENALES_SESSION_DIRECTORY", PROJECT_ROOT / "session_outputs"))
HEADER_IMAGE = SRC / "teoria_senales" / "assets" / "encabezado_institucional.png"
STUDENT_GUIDE_PDF = PROJECT_ROOT / "docs" / "guias" / "Guia_del_estudiante_C-1-4.pdf"


def apply_styles() -> None:
    st.markdown("""
    <style>
    .stApp { background: #f5f7fa; }
    .block-container { max-width: 860px; padding-top: 4.5rem; padding-bottom: 3rem; }
    [data-testid="stForm"] { background:#fff; border:1px solid #dfe4ea; border-radius:10px; padding:1.4rem 1.4rem .6rem; }
    .exercise-label { color:#17426f; font-size:.9rem; font-weight:700; letter-spacing:.03em; text-transform:uppercase; }
    </style>
    """, unsafe_allow_html=True)


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
    with st.expander("Guía del estudiante C-1-4", expanded=False):
        st.markdown("""
        Compara la reconstrucción del pulso rectangular usado en C-1-3.

        1. Localiza los saltos y determina el valor de convergencia.
        2. Evalúa la suma parcial con un armónico.
        3. Compara las reconstrucciones para N = 1, 5 y 15 y calcula el error para N = 5 y N = 15.
        4. Interpreta el fenómeno de Gibbs.
        5. Responde tres preguntas de selección múltiple y dos de verdadero/falso.
        """)
        st.latex(r"S_N(t)=\frac{a_0}{2}+\sum_{n=1}^{N}[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]")
        st.latex(r"\mathrm{ECM}_N=\frac12-\left[\frac{a_0^2}{4}+\frac12\sum_{n=1}^{N}(a_n^2+b_n^2)\right]")
        if STUDENT_GUIDE_PDF.is_file():
            st.download_button("Descargar guía completa en PDF", STUDENT_GUIDE_PDF.read_bytes(), STUDENT_GUIDE_PDF.name, "application/pdf", key="download_c1_4_student_guide")


def render_access_screen() -> None:
    st.markdown('<p class="exercise-label">Componente 1 · Ejercicio C-1-4</p>', unsafe_allow_html=True)
    st.title("Reconstrucción de Fourier y fenómeno de Gibbs")
    st.write("Compara sumas parciales, mide la convergencia e interpreta las oscilaciones cercanas a los saltos.")
    render_student_guide()
    if RECOVERY_PATH_KEY in st.session_state:
        render_recovery_choice()
        return
    with st.form("c1_4_access"):
        student_id = st.text_input("Código estudiantil")
        submitted = st.form_submit_button("Iniciar ejercicio C-1-4", type="primary", width="stretch")
    if not submitted:
        return
    try:
        normalized = normalize_student_code(student_id)
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        pending = repository.find_latest_incomplete(normalized, "C1-4")
        if pending is None:
            activate_session(create_exercise_session(normalized, "C1-4"))
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
    st.info(f"Encontramos una sesión C-1-4 sin finalizar para {student_id}.")
    left, right = st.columns(2)
    if left.button("Continuar sesión", type="primary", width="stretch"):
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        path = Path(st.session_state[RECOVERY_PATH_KEY])
        activate_session(restore_exercise_session(repository.load(path)), path)
        st.rerun()
    if right.button("Iniciar nuevo intento", width="stretch"):
        activate_session(create_exercise_session(student_id, "C1-4"))
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
    if st.button(f"Ver orientación del paso {step_id[-1]}", key=f"c1_4_help_{step_id}", disabled=step.status == StepStatus.COMPLETED or bool(step.help_requests)):
        tracker.register_help(step_id, definition.hint)
        save_active_session()
        st.rerun()
    if step.help_requests and step.status != StepStatus.COMPLETED:
        st.info(step.help_requests[-1])


def create_comparison_figure() -> plt.Figure:
    time = np.linspace(-pi, pi, 1200, endpoint=False)
    figure, axes = plt.subplots(3, 1, figsize=(7, 7.2), sharex=True)
    original = rectangular_periodic_signal(time)
    for axis, harmonics in zip(axes, (1, 5, 15), strict=True):
        axis.plot(time, original, color="#9ca3af", linewidth=2, label="x(t)")
        axis.plot(time, reconstruct_rectangular_pulse(time, harmonics), color="#17426f", linewidth=1.8, label=f"S_{harmonics}(t)")
        axis.axvline(-pi / 2, color="#d97706", alpha=.35)
        axis.axvline(pi / 2, color="#d97706", alpha=.35)
        axis.set_ylabel("Amplitud")
        axis.grid(alpha=.2)
        axis.legend(loc="upper right")
    axes[-1].set_xticks([-pi, -pi/2, 0, pi/2, pi], ["-π", "-π/2", "0", "π/2", "π"])
    axes[-1].set_xlabel("t")
    figure.tight_layout()
    return figure


def render_step_one(tracker) -> None:
    completed = tracker.session.steps["paso_1"].status == StepStatus.COMPLETED
    st.progress(.2, text="Paso 1 de 5 · Discontinuidades y convergencia")
    st.subheader("Localiza las discontinuidades y su valor de convergencia")
    st.latex(r"S_N(t_s)\to\frac{x(t_s^-)+x(t_s^+)}{2}")
    with st.form("c1_4_step_1"):
        left = st.number_input("Salto izquierdo t [rad]", value=None, format="%.6f", disabled=completed)
        right = st.number_input("Salto derecho t [rad]", value=None, format="%.6f", disabled=completed)
        midpoint = st.number_input("Valor de convergencia en el salto", value=None, format="%.6f", disabled=completed)
        submitted = st.form_submit_button("Verificar discontinuidades", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (left, right, midpoint): st.warning("Completa los tres valores antes de verificar.")
        else: register_step_answer(tracker, "paso_1", [left, right, midpoint])
    render_help(tracker, "paso_1")


def render_step_two(tracker) -> None:
    completed = tracker.session.steps["paso_2"].status == StepStatus.COMPLETED
    st.progress(.4, text="Paso 2 de 5 · Reconstrucción con N = 1")
    st.subheader("Reconstruye la señal con un armónico")
    st.latex(r"S_1(t)=\frac12+\frac{2}{\pi}\cos(t)")
    with st.form("c1_4_step_2"):
        center = st.number_input("S₁(0)", value=None, format="%.6f", disabled=completed)
        edge = st.number_input("S₁(π/2)", value=None, format="%.6f", disabled=completed)
        submitted = st.form_submit_button("Verificar suma parcial", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (center, edge): st.warning("Completa los dos valores antes de verificar.")
        else: register_step_answer(tracker, "paso_2", [center, edge])
    render_help(tracker, "paso_2")


def render_step_three(tracker) -> None:
    completed = tracker.session.steps["paso_3"].status == StepStatus.COMPLETED
    st.progress(.6, text="Paso 3 de 5 · Comparación del error")
    st.subheader("Compara el error con 5 y 15 armónicos")
    figure = create_comparison_figure()
    st.pyplot(figure, width="stretch")
    plt.close(figure)
    st.latex(r"\mathrm{ECM}_N=\frac12-\left[\frac{a_0^2}{4}+\frac12\sum_{n=1}^{N}(a_n^2+b_n^2)\right]")
    with st.form("c1_4_step_3"):
        mse5 = st.number_input("ECM para N = 5", value=None, format="%.6f", disabled=completed)
        mse15 = st.number_input("ECM para N = 15", value=None, format="%.6f", disabled=completed)
        submitted = st.form_submit_button("Verificar errores", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (mse5, mse15): st.warning("Completa los dos errores antes de verificar.")
        else: register_step_answer(tracker, "paso_3", [mse5, mse15])
    render_help(tracker, "paso_3")


def render_step_four(tracker) -> None:
    completed = tracker.session.steps["paso_4"].status == StepStatus.COMPLETED
    st.progress(.8, text="Paso 4 de 5 · Fenómeno de Gibbs")
    st.subheader("Interpreta el fenómeno de Gibbs")
    st.latex(r"G=\frac{\mathrm{Si}(\pi)}{\pi}-\frac12,\qquad \mathrm{Si}(\pi)=\int_0^\pi\frac{\sin u}{u}\,du")
    st.write("Expresa G como porcentaje del salto y calcula el pico límite superior 1 + G.")
    with st.form("c1_4_step_4"):
        percent = st.number_input("Sobreimpulso límite [%]", value=None, format="%.6f", disabled=completed)
        peak = st.number_input("Pico límite superior", value=None, format="%.6f", disabled=completed)
        submitted = st.form_submit_button("Verificar Gibbs", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (percent, peak): st.warning("Completa los dos valores antes de verificar.")
        else: register_step_answer(tracker, "paso_4", [percent, peak])
    render_help(tracker, "paso_4")


def render_evaluation(tracker) -> None:
    session = tracker.session
    st.progress(1.0, text="Paso 5 de 5 · Evaluación final")
    if session.evaluation is not None:
        evaluation = session.evaluation
        st.success(f"Evaluación completada: {evaluation.points_earned}/{evaluation.points_possible} puntos · Nota {evaluation.grade:.2f}".replace(".", ","))
        st.code(f"Código de verificación: {report_verification_code(session)}", language=None)
        st.download_button("Descargar reporte docente PDF", generate_pdf_report_bytes(session), report_filename(session), "application/pdf", type="primary", width="stretch")
        return
    st.subheader("Comprueba lo aprendido")
    questions = select_c1_4_questions(session.session_id)
    answers: dict[str, object] = {}
    with st.form("c1_4_final_evaluation"):
        for question in questions:
            st.markdown(f"**{question.question_id}**  \n{question.prompt}")
            if question.question_type is QuestionType.MULTIPLE_CHOICE:
                labels = tuple(f"{code.upper()}. {text}" for code, text in question.options)
                selected = st.radio(f"Selecciona una respuesta en {question.question_id}", labels, index=None, key=f"c1_4_eval_{question.question_id}")
                answers[question.question_id] = selected[0].casefold() if selected else None
            else:
                selected = st.radio(f"Selecciona una respuesta en {question.question_id}", ("Verdadero", "Falso"), index=None, horizontal=True, key=f"c1_4_eval_{question.question_id}")
                answers[question.question_id] = selected == "Verdadero" if selected else None
        submitted = st.form_submit_button("Calificar evaluación", type="primary", width="stretch")
    if submitted:
        missing = [question_id for question_id, answer in answers.items() if answer is None]
        if missing:
            st.warning(f"Responde todas las preguntas antes de calificar: {', '.join(missing)}.")
            return
        tracker.record_evaluation(evaluate_c1_4(questions, answers))
        tracker.complete(tracker.exercise.expected_results)
        save_active_session()
        st.rerun()


def render_active_session() -> None:
    tracker = st.session_state[SESSION_KEY]
    st.markdown('<p class="exercise-label">Componente 1 · Ejercicio C-1-4</p>', unsafe_allow_html=True)
    st.title("Reconstrucción de Fourier y fenómeno de Gibbs")
    st.caption(f"Código estudiantil: {tracker.session.student_id}")
    render_student_guide()
    active = next((step_id for step_id in GUIDED_STEP_IDS if tracker.session.steps[step_id].status != StepStatus.COMPLETED), None)
    if active is None:
        render_evaluation(tracker)
    else:
        {"paso_1": render_step_one, "paso_2": render_step_two, "paso_3": render_step_three, "paso_4": render_step_four}[active](tracker)
    if st.button("Guardar y volver al inicio", key="c1_4_return"):
        save_active_session()
        st.session_state.pop(SESSION_KEY, None)
        st.rerun()


def main() -> None:
    st.set_page_config(page_title="C-1-4 · Reconstrucción de Fourier", page_icon="📈", layout="centered")
    apply_styles()
    if HEADER_IMAGE.is_file():
        st.image(str(HEADER_IMAGE), width="stretch")
    if SESSION_KEY in st.session_state:
        render_active_session()
    else:
        render_access_screen()


if __name__ == "__main__":
    main()
