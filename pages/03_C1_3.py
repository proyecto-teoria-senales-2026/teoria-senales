"""Interfaz guiada del ejercicio C1-3."""

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

from teoria_senales.app.web_session import (
    create_exercise_session,
    normalize_student_code,
    restore_exercise_session,
)
from teoria_senales.domain.models import StepStatus
from teoria_senales.evaluation.autograding import QuestionType
from teoria_senales.evaluation.c1_3_question_bank import (
    evaluate_c1_3,
    select_c1_3_questions,
)
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.reports.pdf_report import (
    generate_pdf_report_bytes,
    report_filename,
    report_verification_code,
)
from teoria_senales.signal_processing.fourier_series import (
    harmonic_amplitude_phase,
    reconstruct_trigonometric_series,
)
from teoria_senales.storage.json_repository import JsonSessionRepository


SESSION_KEY = "c1_3_tracker"
SESSION_PATH_KEY = "c1_3_session_path"
RECOVERY_PATH_KEY = "c1_3_recovery_path"
RECOVERY_CODE_KEY = "c1_3_recovery_code"
LEAVE_CONFIRMATION_KEY = "c1_3_leave_confirmation"
GUIDED_STEP_IDS = ("paso_1", "paso_2", "paso_3", "paso_4")
SESSION_DIRECTORY = Path(
    os.environ.get("TEORIA_SENALES_SESSION_DIRECTORY", PROJECT_ROOT / "session_outputs")
)
HEADER_IMAGE = SRC / "teoria_senales" / "assets" / "encabezado_institucional.png"
STUDENT_GUIDE_PDF = PROJECT_ROOT / "docs" / "guias" / "Guia_del_estudiante_C-1-3.pdf"


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background: #f5f7fa; }
        .block-container { max-width: 860px; padding-top: 4.5rem; padding-bottom: 3rem; }
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
    with st.expander("Guía del estudiante C-1-3", expanded=False):
        st.markdown(
            """
            Calcula la serie trigonométrica de Fourier de un pulso rectangular par,
            periódico y de amplitud 1.

            1. Identifica el periodo y la frecuencia angular fundamental.
            2. Calcula el término constante y usa la simetría de la señal.
            3. Obtén los coeficientes de los primeros armónicos.
            4. Interpreta los espectros de amplitud y fase.
            5. Responde tres preguntas de selección múltiple y dos de verdadero/falso.
            """
        )
        st.latex(r"x(t)=\frac{a_0}{2}+\sum_{n=1}^{\infty}[a_n\cos(n\omega_0t)+b_n\sin(n\omega_0t)]")
        st.latex(r"\omega_0=\frac{2\pi}{T_0},\quad a_n=\frac{2}{\pi n}\sin\left(\frac{n\pi}{2}\right),\quad b_n=0")
        if STUDENT_GUIDE_PDF.is_file():
            st.download_button(
                "Descargar guía completa en PDF",
                data=STUDENT_GUIDE_PDF.read_bytes(),
                file_name=STUDENT_GUIDE_PDF.name,
                mime="application/pdf",
                key="download_c1_3_student_guide",
            )


def render_access_screen() -> None:
    st.markdown('<p class="exercise-label">Componente 1 · Ejercicio C-1-3</p>', unsafe_allow_html=True)
    st.title("Coeficientes y espectro de la serie de Fourier")
    st.write("Calcula los coeficientes trigonométricos de una señal periódica e interpreta sus armónicos.")
    render_student_guide()
    if RECOVERY_PATH_KEY in st.session_state:
        render_recovery_choice()
        return
    with st.form("c1_3_access"):
        student_id = st.text_input("Código estudiantil")
        submitted = st.form_submit_button("Iniciar ejercicio C-1-3", type="primary", width="stretch")
    if not submitted:
        return
    try:
        normalized = normalize_student_code(student_id)
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        pending = repository.find_latest_incomplete(normalized, "C1-3")
        if pending is None:
            activate_session(create_exercise_session(normalized, "C1-3"))
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
    st.info(f"Encontramos una sesión C-1-3 sin finalizar para {student_id}.")
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
        activate_session(create_exercise_session(student_id, "C1-3"))
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
        key=f"c1_3_help_{step_id}",
        disabled=completed or bool(step.help_requests),
    ):
        tracker.register_help(step_id, definition.hint)
        save_active_session()
        st.rerun()
    if step.help_requests and not completed:
        st.info(step.help_requests[-1])


def render_reference_signal() -> None:
    st.write("En un periodo -π ≤ t < π, la señal vale 1 para |t| ≤ π/2 y 0 en el resto.")
    st.latex(r"x(t)=\begin{cases}1,& |t|\leq \pi/2\\0,& \pi/2<|t|<\pi\end{cases},\qquad x(t+2\pi)=x(t)")


def render_step_one(tracker) -> None:
    completed = tracker.session.steps["paso_1"].status == StepStatus.COMPLETED
    st.progress(0.2, text="Paso 1 de 5 · Periodo y frecuencia fundamental")
    st.subheader("Identifica el periodo y la frecuencia fundamental")
    render_reference_signal()
    st.latex(r"\omega_0=\frac{2\pi}{T_0}")
    with st.form("c1_3_step_1"):
        period = st.number_input("Periodo fundamental T₀", value=None, disabled=completed)
        omega = st.number_input("Frecuencia angular fundamental ω₀", value=None, disabled=completed)
        submitted = st.form_submit_button("Verificar periodo y frecuencia", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (period, omega):
            st.warning("Completa los dos valores antes de verificar.")
        else:
            register_step_answer(tracker, "paso_1", [period, omega])
    render_help(tracker, "paso_1")


def render_step_two(tracker) -> None:
    completed = tracker.session.steps["paso_2"].status == StepStatus.COMPLETED
    st.progress(0.4, text="Paso 2 de 5 · Término constante y simetría")
    st.subheader("Calcula el término constante y reconoce la simetría")
    st.latex(r"a_0=\frac{2}{T_0}\int_{T_0}x(t)\,dt,\qquad \text{valor medio}=\frac{a_0}{2}")
    st.write("La señal es par: x(t) = x(-t). Por ello, los términos seno se anulan.")
    with st.form("c1_3_step_2"):
        a0 = st.number_input("Coeficiente a₀", value=None, disabled=completed)
        mean = st.number_input("Valor medio a₀/2", value=None, disabled=completed)
        b1 = st.number_input("Coeficiente b₁", value=None, disabled=completed)
        submitted = st.form_submit_button("Verificar término constante", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (a0, mean, b1):
            st.warning("Completa los tres valores antes de verificar.")
        else:
            register_step_answer(tracker, "paso_2", [a0, mean, b1])
    render_help(tracker, "paso_2")


def render_step_three(tracker) -> None:
    completed = tracker.session.steps["paso_3"].status == StepStatus.COMPLETED
    st.progress(0.6, text="Paso 3 de 5 · Coeficientes armónicos")
    st.subheader("Calcula los coeficientes de los armónicos")
    st.latex(r"a_n=\frac{2}{\pi n}\sin\left(\frac{n\pi}{2}\right),\qquad b_n=0")
    with st.form("c1_3_step_3"):
        a1 = st.number_input("Coeficiente a₁", value=None, format="%.6f", disabled=completed)
        a2 = st.number_input("Coeficiente a₂", value=None, format="%.6f", disabled=completed)
        a3 = st.number_input("Coeficiente a₃", value=None, format="%.6f", disabled=completed)
        submitted = st.form_submit_button("Verificar coeficientes", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (a1, a2, a3):
            st.warning("Completa los tres coeficientes antes de verificar.")
        else:
            register_step_answer(tracker, "paso_3", [a1, a2, a3])
    render_help(tracker, "paso_3")


def create_spectrum_figure(tracker) -> plt.Figure:
    _, an, bn = tracker.exercise.coefficients
    amplitudes, phases = harmonic_amplitude_phase(an, bn)
    orders = np.arange(1, len(an) + 1)
    visible_phases = np.nan_to_num(phases, nan=0.0)
    figure, axes = plt.subplots(2, 1, figsize=(6.2, 4.6), sharex=True)
    markerline, stemlines, _ = axes[0].stem(orders, amplitudes, basefmt=" ")
    plt.setp(markerline, marker="o", color="#17426f")
    plt.setp(stemlines, color="#17426f", linewidth=2)
    axes[0].set_ylabel("Aₙ")
    axes[0].set_title("Espectro de amplitud")
    markerline, stemlines, _ = axes[1].stem(orders, visible_phases, basefmt=" ")
    plt.setp(markerline, marker="o", color="#3568a8")
    plt.setp(stemlines, color="#3568a8", linewidth=2)
    axes[1].set_ylabel("φₙ [rad]")
    axes[1].set_xlabel("Armónico n")
    axes[1].set_title("Espectro de fase; fase 0 mostrada en armónicos nulos")
    for axis in axes:
        axis.grid(axis="y", alpha=0.25)
        axis.set_xticks(orders)
    figure.tight_layout()
    return figure


def create_reconstruction_figure(tracker) -> plt.Figure:
    a0, an, bn = tracker.exercise.coefficients
    time = np.linspace(-pi, pi, 600, endpoint=False)
    original = (np.abs(time) <= pi / 2).astype(float)
    reconstruction = reconstruct_trigonometric_series(time, a0, an, bn, omega_0=tracker.exercise.omega_0)
    figure, axis = plt.subplots(figsize=(6.2, 3.0))
    axis.plot(time, original, label="x(t)", color="#6b7280", linewidth=2)
    axis.plot(time, reconstruction, label="Suma con 5 armónicos", color="#17426f", linewidth=2)
    axis.set_xlabel("t")
    axis.set_ylabel("Amplitud")
    axis.set_xticks([-pi, -pi / 2, 0, pi / 2, pi], ["-π", "-π/2", "0", "π/2", "π"])
    axis.grid(alpha=0.2)
    axis.legend()
    figure.tight_layout()
    return figure


def render_step_four(tracker) -> None:
    completed = tracker.session.steps["paso_4"].status == StepStatus.COMPLETED
    st.progress(0.8, text="Paso 4 de 5 · Espectros")
    st.subheader("Interpreta los espectros de amplitud y fase")
    st.latex(r"A_n=\sqrt{a_n^2+b_n^2},\qquad \varphi_n=\operatorname{atan2}(-b_n,a_n)")
    spectrum = create_spectrum_figure(tracker)
    st.pyplot(spectrum, width="stretch")
    plt.close(spectrum)
    with st.form("c1_3_step_4"):
        amplitude_1 = st.number_input("Amplitud A₁", value=None, format="%.6f", disabled=completed)
        phase_1 = st.number_input("Fase φ₁ [rad]", value=None, format="%.6f", disabled=completed)
        amplitude_3 = st.number_input("Amplitud A₃", value=None, format="%.6f", disabled=completed)
        phase_3 = st.number_input("Fase φ₃ [rad]", value=None, format="%.6f", disabled=completed)
        submitted = st.form_submit_button("Verificar espectros", type="primary", width="stretch", disabled=completed)
    if submitted:
        if None in (amplitude_1, phase_1, amplitude_3, phase_3):
            st.warning("Completa las cuatro lecturas antes de verificar.")
        else:
            register_step_answer(tracker, "paso_4", [amplitude_1, phase_1, amplitude_3, phase_3])
    render_help(tracker, "paso_4")


def render_evaluation(tracker) -> None:
    session = tracker.session
    st.progress(1.0, text="Paso 5 de 5 · Evaluación final")
    if session.evaluation is not None:
        evaluation = session.evaluation
        st.success(f"Evaluación completada: {evaluation.points_earned}/{evaluation.points_possible} puntos · Nota {evaluation.grade:.2f}".replace(".", ","))
        reconstruction = create_reconstruction_figure(tracker)
        st.pyplot(reconstruction, width="stretch")
        plt.close(reconstruction)
        st.code(f"Código de verificación: {report_verification_code(session)}", language=None)
        st.download_button("Descargar reporte docente PDF", data=generate_pdf_report_bytes(session), file_name=report_filename(session), mime="application/pdf", type="primary", width="stretch")
        return
    st.subheader("Comprueba lo aprendido")
    questions = select_c1_3_questions(session.session_id)
    answers: dict[str, object] = {}
    with st.form("c1_3_final_evaluation"):
        for question in questions:
            st.markdown(f"**{question.question_id}**  \n{question.prompt}")
            if question.question_type is QuestionType.MULTIPLE_CHOICE:
                labels = tuple(f"{code.upper()}. {text}" for code, text in question.options)
                selected = st.radio(f"Selecciona una respuesta en {question.question_id}", labels, index=None, key=f"c1_3_eval_{question.question_id}")
                answers[question.question_id] = selected[0].casefold() if selected else None
            else:
                selected = st.radio(f"Selecciona una respuesta en {question.question_id}", ("Verdadero", "Falso"), index=None, horizontal=True, key=f"c1_3_eval_{question.question_id}")
                answers[question.question_id] = selected == "Verdadero" if selected else None
        submitted = st.form_submit_button("Calificar evaluación", type="primary", width="stretch")
    if submitted:
        missing = [question_id for question_id, answer in answers.items() if answer is None]
        if missing:
            st.warning(f"Responde todas las preguntas antes de calificar: {', '.join(missing)}.")
            return
        result = evaluate_c1_3(questions, answers)
        tracker.record_evaluation(result)
        tracker.complete(tracker.exercise.expected_results)
        save_active_session()
        st.rerun()


def render_active_session() -> None:
    tracker = st.session_state[SESSION_KEY]
    session = tracker.session
    st.markdown('<p class="exercise-label">Componente 1 · Ejercicio C-1-3</p>', unsafe_allow_html=True)
    st.title("Coeficientes y espectro de la serie de Fourier")
    st.caption(f"Código estudiantil: {session.student_id}")
    render_student_guide()
    active_step = next((step_id for step_id in GUIDED_STEP_IDS if session.steps[step_id].status != StepStatus.COMPLETED), None)
    if active_step is None:
        render_evaluation(tracker)
    else:
        renderers = {"paso_1": render_step_one, "paso_2": render_step_two, "paso_3": render_step_three, "paso_4": render_step_four}
        renderers[active_step](tracker)
    if not st.session_state.get(LEAVE_CONFIRMATION_KEY, False):
        if st.button("Guardar y volver al inicio", key="c1_3_return"):
            st.session_state[LEAVE_CONFIRMATION_KEY] = True
            st.rerun()
        return
    st.warning("¿Quieres guardar la sesión y salir del ejercicio C-1-3?")
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
    st.set_page_config(page_title="Ejercicio C-1-3 | Teoría de Señales", page_icon="📈", layout="centered")
    apply_styles()
    if HEADER_IMAGE.is_file():
        st.image(str(HEADER_IMAGE), width="stretch")
    if SESSION_KEY in st.session_state:
        render_active_session()
    else:
        render_access_screen()


if __name__ == "__main__":
    main()
