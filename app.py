"""Interfaz gráfica inicial del ejercicio C3-3."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.web_session import (
    create_student_session,
    normalize_student_code,
    restore_student_session,
)
from teoria_senales.domain.models import StepStatus
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.signal_processing.convolution import parse_numeric_sequence
from teoria_senales.storage.json_repository import JsonSessionRepository


SESSION_KEY = "c3_3_tracker"
HELP_KEY = "c3_3_step_1_help"
HELP_KEY_PREFIX = "c3_3_help_"
LEAVE_CONFIRMATION_KEY = "c3_3_leave_confirmation"
SESSION_PATH_KEY = "c3_3_session_path"
RECOVERY_PATH_KEY = "c3_3_recovery_path"
RECOVERY_CODE_KEY = "c3_3_recovery_code"
HEADER_IMAGE = SRC / "teoria_senales" / "assets" / "encabezado_institucional.png"
SESSION_DIRECTORY = Path(
    os.environ.get(
        "TEORIA_SENALES_SESSION_DIRECTORY",
        PROJECT_ROOT / "session_outputs",
    )
)


def save_active_session() -> Path:
    tracker = st.session_state[SESSION_KEY]
    repository = JsonSessionRepository(SESSION_DIRECTORY)
    path = repository.save(tracker.session)
    st.session_state[SESSION_PATH_KEY] = str(path)
    return path


def clear_recovery_state() -> None:
    st.session_state.pop(RECOVERY_PATH_KEY, None)
    st.session_state.pop(RECOVERY_CODE_KEY, None)


def activate_session(tracker, path: Path | None = None) -> None:
    st.session_state[SESSION_KEY] = tracker
    for step_id, step in tracker.session.steps.items():
        st.session_state[f"{HELP_KEY_PREFIX}{step_id}"] = bool(
            step.help_requests
        )
    st.session_state[HELP_KEY] = bool(
        tracker.session.steps["paso_1"].help_requests
    )
    st.session_state[LEAVE_CONFIRMATION_KEY] = False
    if path is None:
        save_active_session()
    else:
        st.session_state[SESSION_PATH_KEY] = str(path)
    clear_recovery_state()


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f5f7fa;
        }
        .block-container {
            max-width: 780px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        [data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid #dfe4ea;
            border-radius: 10px;
            padding: 1.4rem 1.4rem 0.5rem;
        }
        [data-testid="stFormSubmitButton"] button,
        .stButton button {
            border-radius: 6px;
            font-weight: 600;
        }
        .exercise-label {
            color: #17426f;
            font-size: 0.9rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }
        .sequence-value {
            background: #ffffff;
            border: 1px solid #dfe4ea;
            border-radius: 8px;
            color: #172b4d;
            font-size: 1.05rem;
            margin-bottom: 0.8rem;
            padding: 0.75rem 1rem;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_sequence(values: np.ndarray) -> str:
    samples = [int(value) if value.is_integer() else float(value) for value in values]
    return str(samples)


def create_signal_figure(values: np.ndarray, signal_name: str) -> plt.Figure:
    indices = np.arange(len(values))
    figure, axis = plt.subplots(figsize=(4.8, 2.8))
    markerline, stemlines, _ = axis.stem(indices, values, basefmt=" ")
    plt.setp(markerline, marker="o", markersize=7, color="#17426f")
    plt.setp(stemlines, linewidth=2, color="#17426f")

    lower_limit = min(-0.5, float(values.min()) - 0.5)
    upper_limit = max(0.5, float(values.max()) + 0.5)
    axis.axhline(0, color="#7b8794", linewidth=1)
    axis.set_xlim(-0.5, len(values) - 0.5)
    axis.set_ylim(lower_limit, upper_limit)
    axis.set_xticks(indices)
    axis.set_xlabel("Índice n")
    axis.set_ylabel("Amplitud")
    axis.set_title(f"Señal {signal_name}")
    axis.grid(axis="y", alpha=0.2)
    figure.tight_layout()
    return figure


def render_signal_card(values: np.ndarray, signal_name: str) -> None:
    st.markdown(
        f'<div class="sequence-value"><strong>{signal_name}</strong> = '
        f"{format_sequence(values)}</div>",
        unsafe_allow_html=True,
    )
    figure = create_signal_figure(values, signal_name)
    st.pyplot(figure, width="stretch")
    plt.close(figure)


def render_access_screen() -> None:
    st.markdown('<p class="exercise-label">Componente 3 · Ejercicio C3-3</p>', unsafe_allow_html=True)
    st.title("Convolución de señales discretas")
    st.write(
        "En este ejercicio desarrollarás una convolución lineal y comprobarás "
        "el resultado mediante DFT/FFT con dos longitudes de transformación."
    )

    if RECOVERY_PATH_KEY in st.session_state:
        render_recovery_choice()
        return

    with st.form("student_access", clear_on_submit=False):
        student_id = st.text_input(
            "Código estudiantil",
            placeholder="Ingresa tu código",
            help="El código permite identificar la sesión y el reporte del ejercicio.",
        )
        submitted = st.form_submit_button(
            "Iniciar ejercicio",
            type="primary",
            width="stretch",
        )

    if not submitted:
        return

    try:
        normalized_id = normalize_student_code(student_id)
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        pending_session = repository.find_latest_incomplete(
            normalized_id,
            "C3-3",
        )
        if pending_session is None:
            activate_session(create_student_session(normalized_id))
        else:
            _, path = pending_session
            st.session_state[RECOVERY_CODE_KEY] = normalized_id
            st.session_state[RECOVERY_PATH_KEY] = str(path)
    except ValueError as error:
        st.error(str(error))
        return

    st.rerun()


def render_recovery_choice() -> None:
    student_id = st.session_state[RECOVERY_CODE_KEY]
    st.info(
        f"Encontramos una sesión sin finalizar para el código {student_id}. "
        "Puedes continuarla o iniciar un nuevo intento."
    )
    continue_column, new_column = st.columns(2)
    with continue_column:
        continue_session = st.button(
            "Continuar sesión",
            type="primary",
            width="stretch",
        )
    with new_column:
        new_attempt = st.button("Iniciar nuevo intento", width="stretch")

    if continue_session:
        repository = JsonSessionRepository(SESSION_DIRECTORY)
        path = Path(st.session_state[RECOVERY_PATH_KEY])
        activate_session(
            restore_student_session(repository.load(path)),
            path,
        )
        st.rerun()
    elif new_attempt:
        activate_session(create_student_session(student_id))
        st.rerun()


def render_step_one(tracker) -> None:
    exercise = tracker.exercise
    step = tracker.session.steps["paso_1"]
    definition = exercise.get_step("paso_1")
    saved_values = (None, None, None)
    if step.attempts:
        last_answer = step.attempts[-1].answer
        if isinstance(last_answer, (list, tuple)) and len(last_answer) == 3:
            try:
                numeric_values = tuple(float(value) for value in last_answer)
                if all(
                    value >= 1 and value.is_integer()
                    for value in numeric_values
                ):
                    saved_values = tuple(int(value) for value in numeric_values)
            except (TypeError, ValueError):
                pass

    st.progress(0.2, text="Paso 1 de 5 · Reconocimiento de las señales")
    st.subheader("Señales de entrada")
    st.write(
        "Observa las muestras y sus índices. Las secuencias comienzan en "
        r"$n=0$."
    )

    left_column, right_column = st.columns(2)
    with left_column:
        render_signal_card(exercise.x, "x[n]")
    with right_column:
        render_signal_card(exercise.h, "h[n]")

    st.subheader("Identifica las longitudes")
    st.write(
        r"Determina $L_x$, $L_h$ y la longitud $L_y$ esperada para la "
        "convolución lineal."
    )

    completed = step.status == StepStatus.COMPLETED
    with st.form("step_one_answer"):
        lx_column, lh_column, ly_column = st.columns(3)
        with lx_column:
            lx = st.number_input(
                "Lx",
                min_value=1,
                step=1,
                value=saved_values[0],
                disabled=completed,
                placeholder="Longitud de x[n]",
            )
        with lh_column:
            lh = st.number_input(
                "Lh",
                min_value=1,
                step=1,
                value=saved_values[1],
                disabled=completed,
                placeholder="Longitud de h[n]",
            )
        with ly_column:
            ly = st.number_input(
                "Ly",
                min_value=1,
                step=1,
                value=saved_values[2],
                disabled=completed,
                placeholder="Longitud de y[n]",
            )
        submitted = st.form_submit_button(
            "Verificar respuesta",
            type="primary",
            width="stretch",
            disabled=completed,
        )

    if submitted and not completed:
        if None in (lx, lh, ly):
            st.warning("Completa las tres longitudes antes de verificar.")
        else:
            answer = [lx, lh, ly]
            correct = exercise.validate("paso_1", answer)
            attempt_number = len(step.attempts) + 1
            feedback = feedback_for_attempt(correct, attempt_number)
            tracker.register_attempt(
                "paso_1",
                answer,
                correct,
                feedback,
                definition.difficulty,
            )
            save_active_session()
            if correct:
                st.rerun()
            else:
                st.error(feedback)

    help_column, status_column = st.columns([1, 2])
    with help_column:
        if st.button("Ver orientación", width="stretch", disabled=completed):
            tracker.register_help("paso_1", definition.hint)
            st.session_state[HELP_KEY] = True
            save_active_session()
    with status_column:
        if completed:
            st.success("Paso 1 completado. El resultado quedó guardado en la sesión.")
        elif step.attempts:
            st.caption(f"Intentos registrados: {len(step.attempts)}")

    if st.session_state.get(HELP_KEY, False) and not completed:
        st.info(definition.hint)


def saved_sequence_answer(step) -> str:
    if not step.attempts:
        return ""

    answer = step.attempts[-1].answer
    parsed = parse_numeric_sequence(answer)
    if parsed is not None:
        return ", ".join(
            str(int(value)) if value.is_integer() else str(float(value))
            for value in parsed
        )
    return str(answer)


def render_step_two(tracker) -> None:
    exercise = tracker.exercise
    step = tracker.session.steps["paso_2"]
    definition = exercise.get_step("paso_2")
    completed = step.status == StepStatus.COMPLETED
    help_key = f"{HELP_KEY_PREFIX}paso_2"

    st.divider()
    st.progress(0.4, text="Paso 2 de 5 · Convolución lineal")
    st.subheader("Calcula la convolución lineal")
    st.write(
        r"Calcula cada muestra con $y[n]=\sum_k x[k]h[n-k]$. "
        "Conserva el orden de los índices desde n = 0."
    )
    st.caption(
        "Escribe las cinco muestras separadas por comas, espacios o punto y coma."
    )

    with st.form("step_two_answer"):
        answer = st.text_input(
            "Resultado de la convolución lineal",
            value=saved_sequence_answer(step),
            placeholder="Ejemplo de formato: 0, 1, 2, 3, 4",
            disabled=completed,
        )
        submitted = st.form_submit_button(
            "Verificar convolución lineal",
            type="primary",
            width="stretch",
            disabled=completed,
        )

    if submitted and not completed:
        if parse_numeric_sequence(answer) is None:
            st.warning(
                "Ingresa únicamente valores numéricos separados por comas, "
                "espacios o punto y coma."
            )
        else:
            correct = exercise.validate("paso_2", answer)
            attempt_number = len(step.attempts) + 1
            feedback = feedback_for_attempt(correct, attempt_number)
            tracker.register_attempt(
                "paso_2",
                answer,
                correct,
                feedback,
                definition.difficulty,
            )
            save_active_session()
            if correct:
                st.rerun()
            else:
                st.error(feedback)

    help_column, status_column = st.columns([1, 2])
    with help_column:
        if st.button(
            "Ver orientación del paso 2",
            width="stretch",
            disabled=completed,
        ):
            tracker.register_help("paso_2", definition.hint)
            st.session_state[help_key] = True
            save_active_session()
    with status_column:
        if completed:
            st.success(
                "Paso 2 completado. La convolución lineal quedó guardada."
            )
        elif step.attempts:
            st.caption(f"Intentos registrados: {len(step.attempts)}")

    if st.session_state.get(help_key, False) and not completed:
        st.info(definition.hint)

    if completed:
        st.markdown("#### Resultado comprobado")
        render_signal_card(
            np.asarray(exercise.expected_results["convolucion_lineal"]),
            "y[n]",
        )


def render_step_three(tracker) -> None:
    exercise = tracker.exercise
    step = tracker.session.steps["paso_3"]
    definition = exercise.get_step("paso_3")
    completed = step.status == StepStatus.COMPLETED
    help_key = f"{HELP_KEY_PREFIX}paso_3"

    st.divider()
    st.progress(0.6, text="Paso 3 de 5 · Verificación DFT/FFT con N = 3")
    st.subheader("Verifica el resultado con N = 3")
    st.write(
        r"Calcula $X[k]$ y $H[k]$ con tres puntos, multiplica ambos "
        r"espectros y aplica la transformada inversa."
    )
    st.caption(
        "Registra las tres muestras obtenidas en el dominio del tiempo."
    )

    with st.form("step_three_answer"):
        answer = st.text_input(
            "Resultado mediante DFT/FFT con N = 3",
            value=saved_sequence_answer(step),
            placeholder="Ejemplo de formato: 0, 1, 2",
            disabled=completed,
        )
        submitted = st.form_submit_button(
            "Verificar resultado con N = 3",
            type="primary",
            width="stretch",
            disabled=completed,
        )

    if submitted and not completed:
        if parse_numeric_sequence(answer) is None:
            st.warning(
                "Ingresa únicamente valores numéricos separados por comas, "
                "espacios o punto y coma."
            )
        else:
            correct = exercise.validate("paso_3", answer)
            attempt_number = len(step.attempts) + 1
            feedback = feedback_for_attempt(correct, attempt_number)
            tracker.register_attempt(
                "paso_3",
                answer,
                correct,
                feedback,
                definition.difficulty,
            )
            save_active_session()
            if correct:
                st.rerun()
            else:
                st.error(feedback)

    help_column, status_column = st.columns([1, 2])
    with help_column:
        if st.button(
            "Ver orientación del paso 3",
            width="stretch",
            disabled=completed,
        ):
            tracker.register_help("paso_3", definition.hint)
            st.session_state[help_key] = True
            save_active_session()
    with status_column:
        if completed:
            st.success(
                "Paso 3 completado. El resultado con N = 3 quedó guardado."
            )
        elif step.attempts:
            st.caption(f"Intentos registrados: {len(step.attempts)}")

    if st.session_state.get(help_key, False) and not completed:
        st.info(definition.hint)

    if completed:
        st.markdown("#### Resultado comprobado")
        render_signal_card(
            np.asarray(exercise.expected_results["resultado_N3"]),
            "y_N=3[n]",
        )
        st.caption(
            "Como N = 3 es menor que la longitud de la convolución lineal, "
            "este resultado presenta solapamiento circular."
        )


def render_step_four(tracker) -> None:
    exercise = tracker.exercise
    step = tracker.session.steps["paso_4"]
    definition = exercise.get_step("paso_4")
    completed = step.status == StepStatus.COMPLETED
    help_key = f"{HELP_KEY_PREFIX}paso_4"

    st.divider()
    st.progress(0.8, text="Paso 4 de 5 · Verificación DFT/FFT con N = 5")
    st.subheader("Verifica el resultado con N = 5")
    st.write(
        "Completa ambas señales con ceros hasta cinco muestras. Luego calcula "
        r"$X[k]$, $H[k]$, su producto y la transformada inversa."
    )
    st.caption(
        "Registra las cinco muestras obtenidas en el dominio del tiempo."
    )

    with st.form("step_four_answer"):
        answer = st.text_input(
            "Resultado mediante DFT/FFT con N = 5",
            value=saved_sequence_answer(step),
            placeholder="Ejemplo de formato: 0, 1, 2, 3, 4",
            disabled=completed,
        )
        submitted = st.form_submit_button(
            "Verificar resultado con N = 5",
            type="primary",
            width="stretch",
            disabled=completed,
        )

    if submitted and not completed:
        if parse_numeric_sequence(answer) is None:
            st.warning(
                "Ingresa únicamente valores numéricos separados por comas, "
                "espacios o punto y coma."
            )
        else:
            correct = exercise.validate("paso_4", answer)
            attempt_number = len(step.attempts) + 1
            feedback = feedback_for_attempt(correct, attempt_number)
            tracker.register_attempt(
                "paso_4",
                answer,
                correct,
                feedback,
                definition.difficulty,
            )
            save_active_session()
            if correct:
                st.rerun()
            else:
                st.error(feedback)

    help_column, status_column = st.columns([1, 2])
    with help_column:
        if st.button(
            "Ver orientación del paso 4",
            width="stretch",
            disabled=completed,
        ):
            tracker.register_help("paso_4", definition.hint)
            st.session_state[help_key] = True
            save_active_session()
    with status_column:
        if completed:
            st.success(
                "Paso 4 completado. El resultado con N = 5 quedó guardado."
            )
        elif step.attempts:
            st.caption(f"Intentos registrados: {len(step.attempts)}")

    if st.session_state.get(help_key, False) and not completed:
        st.info(definition.hint)

    if completed:
        st.markdown("#### Comparación de resultados")
        linear_column, fft_column = st.columns(2)
        with linear_column:
            render_signal_card(
                np.asarray(exercise.expected_results["convolucion_lineal"]),
                "y[n] lineal",
            )
        with fft_column:
            render_signal_card(
                np.asarray(exercise.expected_results["resultado_N5"]),
                "y_N=5[n]",
            )
        st.success(
            "Con N = 5 no hay solapamiento circular: el resultado coincide "
            "con la convolución lineal."
        )


def render_active_session() -> None:
    tracker = st.session_state[SESSION_KEY]
    session = tracker.session

    st.markdown(
        '<p class="exercise-label">Componente 3 · Ejercicio C3-3</p>',
        unsafe_allow_html=True,
    )
    st.title("Convolución de señales discretas")
    st.caption(f"Código estudiantil: {session.student_id}")
    render_step_one(tracker)
    if session.steps["paso_1"].status == StepStatus.COMPLETED:
        render_step_two(tracker)
    if session.steps["paso_2"].status == StepStatus.COMPLETED:
        render_step_three(tracker)
    if session.steps["paso_3"].status == StepStatus.COMPLETED:
        render_step_four(tracker)

    if not st.session_state.get(LEAVE_CONFIRMATION_KEY, False):
        if st.button("Volver al inicio"):
            st.session_state[LEAVE_CONFIRMATION_KEY] = True
            st.rerun()
        return

    st.warning(
        "La sesión se guardará antes de volver al inicio. "
        "¿Quieres salir del ejercicio?"
    )
    confirm_column, cancel_column = st.columns(2)
    with confirm_column:
        leave = st.button(
            "Guardar y volver al inicio",
            type="primary",
            width="stretch",
        )
    with cancel_column:
        cancel = st.button("Continuar ejercicio", width="stretch")

    if leave:
        save_active_session()
        for key in (
            SESSION_KEY,
            HELP_KEY,
            LEAVE_CONFIRMATION_KEY,
            SESSION_PATH_KEY,
        ):
            st.session_state.pop(key, None)
        for step_id in tracker.session.steps:
            st.session_state.pop(f"{HELP_KEY_PREFIX}{step_id}", None)
        st.rerun()
    elif cancel:
        st.session_state[LEAVE_CONFIRMATION_KEY] = False
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Ejercicio C3-3 | Teoría de Señales",
        page_icon="📈",
        layout="centered",
    )
    apply_styles()
    st.image(str(HEADER_IMAGE), width="stretch")

    if SESSION_KEY in st.session_state:
        render_active_session()
    else:
        render_access_screen()


if __name__ == "__main__":
    main()
