"""Interfaz guiada del ejercicio C1-1."""

from __future__ import annotations

import os
import sys
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
from teoria_senales.evaluation.c1_1_question_bank import (
    evaluate_c1_1,
    select_c1_1_questions,
)
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.reports.pdf_report import (
    generate_pdf_report_bytes,
    report_filename,
    report_verification_code,
)
from teoria_senales.storage.json_repository import JsonSessionRepository


SESSION_KEY = "c1_1_tracker"
SESSION_PATH_KEY = "c1_1_session_path"
RECOVERY_PATH_KEY = "c1_1_recovery_path"
RECOVERY_CODE_KEY = "c1_1_recovery_code"
LEAVE_CONFIRMATION_KEY = "c1_1_leave_confirmation"
GUIDED_STEP_IDS = ("paso_1", "paso_2", "paso_3", "paso_4")
SESSION_DIRECTORY = Path(
    os.environ.get(
        "TEORIA_SENALES_SESSION_DIRECTORY",
        PROJECT_ROOT / "session_outputs",
    )
)
HEADER_IMAGE = SRC / "teoria_senales" / "assets" / "encabezado_institucional.png"
STUDENT_GUIDE_PDF = PROJECT_ROOT / "docs" / "guias" / "Guia_del_estudiante_C-1-1.pdf"


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
    with st.expander("Guía del estudiante C-1-1", expanded=False):
        st.markdown(
            r"""
            #### 1. Información general

            Ejercicio individual guiado sobre la representación de señales
            fundamentales de tiempo discreto.

            #### 2. Resultado de Aprendizaje Esperado

            Identificar y representar matemáticamente señales comunes utilizadas
            en ingeniería mediante series de Fourier, dibujando el espectro de
            frecuencias, relacionando con aplicaciones reales y reconocer la
            importancia de comparar los resultados teóricos con experimentales y
            de simulación.

            #### 3. Conocimientos previos

            - Índice entero de tiempo discreto y lectura de una secuencia.
            - Potencias, seno y multiplicación por escalares.
            - Amplitud, frecuencia angular, periodo y duración.
            - Lectura de gráficas de tallos.

            #### 4. Lectura de apoyo

            Oppenheim y Schafer, *Discrete-Time Signal Processing*: señales
            discretas, secuencias fundamentales y periodicidad.

            #### 5. Enunciado

            Observa las representaciones numéricas y gráficas del impulso
            unitario, el escalón unitario, la rampa, una exponencial y una
            senoidal. Identifica sus valores característicos, analiza la amplitud,
            reconoce su duración y relaciona la frecuencia angular de la senoidal
            con su periodo.

            #### 6. Desarrollo de la actividad

            1. Reconoce impulso, escalón y rampa.
            2. Calcula el efecto de la amplitud.
            3. Interpreta la señal exponencial.
            4. Halla el periodo de la señal senoidal.
            5. Comprueba lo aprendido.

            #### 7. Producto esperado

            Al finalizar, descarga el reporte con el código estudiantil, el
            ejercicio, el puntaje, la nota, los resultados por criterio y el
            código de verificación.

            #### 8. Criterios de evaluación

            - Identifica y diferencia las cinco señales fundamentales.
            - Calcula muestras y reconoce amplitud, base exponencial y duración.
            - Relaciona frecuencia angular, periodo y representación temporal.

            **Nomenclatura**

            $n$: índice entero; $x[n]$: señal; $\delta[n]$: impulso unitario;
            $u[n]$: escalón unitario; $r[n]$: rampa; $A$: amplitud;
            $\omega_0$: frecuencia angular; $N_0$: periodo en muestras.
            """
        )
        st.latex(r"r[n] = n\,u[n]")
        st.latex(r"x[n] = \left(\frac{1}{2}\right)^n u[n]")
        st.latex(r"x[n] = \sin\left(\frac{\pi}{2}n\right)")
        st.latex(r"x[n+N_0]=x[n],\qquad \omega_0N_0=2\pi k")
        st.latex(r"\mathrm{Nota}=\frac{\mathrm{puntos\ obtenidos}}{\mathrm{puntos\ posibles}}\times 5{,}0")
        if STUDENT_GUIDE_PDF.is_file():
            st.download_button(
                "Descargar guía completa en PDF",
                data=STUDENT_GUIDE_PDF.read_bytes(),
                file_name=STUDENT_GUIDE_PDF.name,
                mime="application/pdf",
                key="download_c1_1_student_guide",
            )


def create_signal_figure(indices: np.ndarray, samples: np.ndarray, title: str):
    figure, axis = plt.subplots(figsize=(5.4, 2.7))
    markerline, stemlines, _ = axis.stem(indices, samples, basefmt=" ")
    plt.setp(markerline, marker="o", markersize=6, color="#17426f")
    plt.setp(stemlines, linewidth=2, color="#17426f")
    axis.axhline(0, color="#7b8794", linewidth=1)
    axis.set_xlabel("Índice n")
    axis.set_ylabel("Amplitud")
    axis.set_title(title)
    axis.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    return figure


def render_examples(exercise, names: tuple[str, ...] | None = None) -> None:
    examples = exercise.examples()
    if names is not None:
        examples = tuple(example for example in examples if example.name in names)
    for example in examples:
        st.markdown(f"**{example.name}:** ${example.notation}$")
        figure = create_signal_figure(
            example.signal.indices,
            example.signal.samples,
            example.name,
        )
        st.pyplot(figure, width="stretch")
        plt.close(figure)


def render_access_screen() -> None:
    st.markdown(
        '<p class="exercise-label">Componente 1 · Ejercicio C-1-1</p>',
        unsafe_allow_html=True,
    )
    st.title("Señales fundamentales de tiempo discreto")
    st.write(
        "Reconoce y representa impulso, escalón, rampa, exponencial y "
        "senoidal mediante un recorrido guiado."
    )
    render_student_guide()

    if RECOVERY_PATH_KEY in st.session_state:
        render_recovery_choice()
        return

    with st.form("c1_1_access"):
        student_id = st.text_input(
            "Código estudiantil",
            help="El código identifica la sesión y el reporte del ejercicio.",
        )
        submitted = st.form_submit_button(
            "Iniciar ejercicio C-1-1", type="primary", width="stretch"
        )
    if not submitted:
        return

    try:
        normalized = normalize_student_code(student_id)
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        pending = repository.find_latest_incomplete(normalized, "C1-1")
        if pending is None:
            activate_session(create_exercise_session(normalized, "C1-1"))
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
    st.info(
        f"Encontramos una sesión C-1-1 sin finalizar para {student_id}. "
        "Puedes continuarla o iniciar un nuevo intento."
    )
    continue_column, new_column = st.columns(2)
    with continue_column:
        continue_session = st.button(
            "Continuar sesión", type="primary", width="stretch"
        )
    with new_column:
        new_attempt = st.button("Iniciar nuevo intento", width="stretch")
    if continue_session:
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        path = Path(st.session_state[RECOVERY_PATH_KEY])
        activate_session(restore_exercise_session(repository.load(path)), path)
        st.rerun()
    elif new_attempt:
        activate_session(create_exercise_session(student_id, "C1-1"))
        st.rerun()


def register_step_answer(tracker, step_id: str, answer: list[float]) -> None:
    definition = tracker.exercise.get_step(step_id)
    step = tracker.session.steps[step_id]
    correct = tracker.exercise.validate(step_id, answer)
    feedback = feedback_for_attempt(correct, len(step.attempts) + 1)
    tracker.register_attempt(
        step_id,
        answer,
        correct,
        feedback,
        definition.difficulty,
    )
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
        key=f"help_{step_id}",
        disabled=completed or bool(step.help_requests),
    ):
        tracker.register_help(step_id, definition.hint)
        save_active_session()
        st.rerun()
    if step.help_requests and not completed:
        st.info(step.help_requests[-1])
    if step.attempts and not completed:
        count = len(step.attempts)
        st.caption(f"{count} {'intento registrado' if count == 1 else 'intentos registrados'}")


def render_step_one(tracker) -> None:
    step = tracker.session.steps["paso_1"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.2, text="Paso 1 de 5 · Reconocimiento")
    st.subheader("Reconoce impulso, escalón y rampa")
    render_examples(
        tracker.exercise,
        ("Impulso unitario", "Escalón unitario", "Rampa unitaria"),
    )
    st.write("Lee en las gráficas los valores solicitados.")
    with st.form("c1_1_step_1"):
        columns = st.columns(3)
        with columns[0]:
            impulse = st.number_input("δ[0]", value=None, disabled=completed)
        with columns[1]:
            step_value = st.number_input("u[-1]", value=None, disabled=completed)
        with columns[2]:
            ramp = st.number_input("r[3]", value=None, disabled=completed)
        submitted = st.form_submit_button(
            "Verificar reconocimiento", type="primary", width="stretch", disabled=completed
        )
    if submitted:
        if None in (impulse, step_value, ramp):
            st.warning("Completa los tres valores antes de verificar.")
        else:
            register_step_answer(tracker, "paso_1", [impulse, step_value, ramp])
    render_help(tracker, "paso_1")


def render_step_two(tracker) -> None:
    step = tracker.session.steps["paso_2"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.4, text="Paso 2 de 5 · Muestras y amplitud")
    st.subheader("Calcula el efecto de la amplitud")
    st.write(
        "Evalúa las expresiones en el índice indicado. El factor que "
        "multiplica la señal modifica su amplitud."
    )
    with st.form("c1_1_step_2"):
        columns = st.columns(3)
        with columns[0]:
            impulse = st.number_input("3δ[0]", value=None, disabled=completed)
        with columns[1]:
            step_value = st.number_input("2u[4]", value=None, disabled=completed)
        with columns[2]:
            ramp = st.number_input("r[3]", value=None, disabled=completed)
        submitted = st.form_submit_button(
            "Verificar muestras", type="primary", width="stretch", disabled=completed
        )
    if submitted:
        if None in (impulse, step_value, ramp):
            st.warning("Completa los tres valores antes de verificar.")
        else:
            register_step_answer(tracker, "paso_2", [impulse, step_value, ramp])
    render_help(tracker, "paso_2")


def render_step_three(tracker) -> None:
    step = tracker.session.steps["paso_3"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.6, text="Paso 3 de 5 · Exponencial discreta")
    st.subheader("Interpreta x[n] = (1/2)^n u[n]")
    render_examples(tracker.exercise, ("Exponencial discreta",))
    with st.form("c1_1_step_3"):
        left, middle = st.columns(2)
        with left:
            x_zero = st.number_input("x[0]", value=None, disabled=completed)
        with middle:
            x_two = st.number_input("x[2]", value=None, disabled=completed)
        behavior = st.radio(
            "Cuando n aumenta, la señal:",
            ("Disminuye hacia cero", "Permanece constante", "Crece sin límite"),
            index=None,
            disabled=completed,
        )
        submitted = st.form_submit_button(
            "Verificar exponencial", type="primary", width="stretch", disabled=completed
        )
    if submitted:
        if None in (x_zero, x_two, behavior):
            st.warning("Completa los valores y selecciona el comportamiento.")
        else:
            behavior_code = 0 if behavior == "Disminuye hacia cero" else 1
            register_step_answer(tracker, "paso_3", [x_zero, x_two, behavior_code])
    render_help(tracker, "paso_3")


def parse_sequence(value: str) -> list[float] | None:
    normalized = value.replace(";", " ").replace(",", " ").split()
    try:
        return [float(item) for item in normalized]
    except ValueError:
        return None


def render_step_four(tracker) -> None:
    step = tracker.session.steps["paso_4"]
    completed = step.status == StepStatus.COMPLETED
    st.progress(0.8, text="Paso 4 de 5 · Señal senoidal")
    st.subheader("Halla el periodo de x[n] = sin((π/2)n)")
    render_examples(tracker.exercise, ("Señal senoidal",))
    with st.form("c1_1_step_4"):
        period = st.number_input("Periodo N₀ en muestras", min_value=1, value=None, disabled=completed)
        samples = st.text_input(
            "Muestras x[0], x[1], x[2], x[3], x[4]",
            placeholder="Ejemplo: 0, 1, 0, -1, 0",
            disabled=completed,
        )
        submitted = st.form_submit_button(
            "Verificar periodo y muestras", type="primary", width="stretch", disabled=completed
        )
    if submitted:
        parsed = parse_sequence(samples)
        if period is None or parsed is None or len(parsed) != 5:
            st.warning("Ingresa el periodo y exactamente cinco muestras numéricas.")
        else:
            register_step_answer(tracker, "paso_4", [period, *parsed])
    render_help(tracker, "paso_4")


def render_evaluation(tracker) -> None:
    session = tracker.session
    st.progress(1.0, text="Paso 5 de 5 · Evaluación final")
    if session.evaluation is not None:
        evaluation = session.evaluation
        st.success(
            f"Evaluación completada: {evaluation.points_earned}/"
            f"{evaluation.points_possible} puntos · Nota "
            f"{evaluation.grade:.2f}".replace(".", ",")
        )
        st.code(
            f"Código de verificación: {report_verification_code(session)}",
            language=None,
        )
        st.download_button(
            "Descargar reporte docente PDF",
            data=generate_pdf_report_bytes(session),
            file_name=report_filename(session),
            mime="application/pdf",
            type="primary",
            width="stretch",
        )
        return

    st.subheader("Comprueba lo aprendido")
    st.write(
        "Responde cinco preguntas seleccionadas aleatoriamente del banco de "
        "C-1-1: tres de selección múltiple y dos de verdadero/falso."
    )
    questions = select_c1_1_questions(session.session_id)
    answers: dict[str, object] = {}
    with st.form("c1_1_final_evaluation"):
        for question in questions:
            st.markdown(f"**{question.question_id}**  \n{question.prompt}")
            if question.question_type is QuestionType.MULTIPLE_CHOICE:
                labels = tuple(
                    f"{code.upper()}. {text}" for code, text in question.options
                )
                selected = st.radio(
                    f"Selecciona una respuesta en {question.question_id}",
                    labels,
                    index=None,
                    key=f"c1_eval_{question.question_id}",
                )
                answers[question.question_id] = (
                    selected[0].casefold() if selected else None
                )
            else:
                selected = st.radio(
                    f"Selecciona una respuesta en {question.question_id}",
                    ("Verdadero", "Falso"),
                    index=None,
                    horizontal=True,
                    key=f"c1_eval_{question.question_id}",
                )
                answers[question.question_id] = (
                    selected == "Verdadero" if selected else None
                )
        submitted = st.form_submit_button(
            "Calificar evaluación", type="primary", width="stretch"
        )
    if submitted:
        missing = [question_id for question_id, answer in answers.items() if answer is None]
        if missing:
            st.warning(f"Responde todas las preguntas antes de calificar: {', '.join(missing)}.")
            return
        result = evaluate_c1_1(questions, answers)
        tracker.record_evaluation(result)
        tracker.complete(tracker.exercise.expected_results)
        save_active_session()
        st.rerun()


def render_active_session() -> None:
    tracker = st.session_state[SESSION_KEY]
    session = tracker.session
    st.markdown(
        '<p class="exercise-label">Componente 1 · Ejercicio C-1-1</p>',
        unsafe_allow_html=True,
    )
    st.title("Señales fundamentales de tiempo discreto")
    st.caption(f"Código estudiantil: {session.student_id}")
    render_student_guide()

    active_step = next(
        (
            step_id
            for step_id in GUIDED_STEP_IDS
            if session.steps[step_id].status != StepStatus.COMPLETED
        ),
        None,
    )
    if active_step is None:
        render_evaluation(tracker)
    else:
        completed_count = GUIDED_STEP_IDS.index(active_step)
        if completed_count:
            st.success(f"{completed_count} de 4 pasos guiados completados.")
        renderers = {
            "paso_1": render_step_one,
            "paso_2": render_step_two,
            "paso_3": render_step_three,
            "paso_4": render_step_four,
        }
        renderers[active_step](tracker)

    if not st.session_state.get(LEAVE_CONFIRMATION_KEY, False):
        if st.button("Guardar y volver al inicio", key="c1_return"):
            st.session_state[LEAVE_CONFIRMATION_KEY] = True
            st.rerun()
        return
    st.warning("¿Quieres guardar la sesión y salir del ejercicio C-1-1?")
    confirm_column, cancel_column = st.columns(2)
    with confirm_column:
        leave = st.button("Sí, guardar y salir", type="primary", width="stretch")
    with cancel_column:
        cancel = st.button("Continuar ejercicio", width="stretch")
    if leave:
        save_active_session()
        for key in (SESSION_KEY, SESSION_PATH_KEY, LEAVE_CONFIRMATION_KEY):
            st.session_state.pop(key, None)
        st.rerun()
    elif cancel:
        st.session_state[LEAVE_CONFIRMATION_KEY] = False
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Ejercicio C-1-1 | Teoría de Señales",
        page_icon="📈",
        layout="centered",
    )
    apply_styles()
    if HEADER_IMAGE.is_file():
        st.image(str(HEADER_IMAGE), width="stretch")
    if SESSION_KEY in st.session_state:
        render_active_session()
    else:
        render_access_screen()


if __name__ == "__main__":
    main()
