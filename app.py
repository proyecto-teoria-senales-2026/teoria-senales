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
from teoria_senales.evaluation.autograding import (
    QuestionType,
    evaluate_c3_3,
    get_c3_3_questions,
)
from teoria_senales.feedback.progressive import feedback_for_attempt
from teoria_senales.reports.pdf_report import (
    generate_pdf_report_bytes,
    report_filename,
    report_verification_code,
)
from teoria_senales.signal_processing.convolution import parse_numeric_sequence
from teoria_senales.signal_processing.explorer import explore_signals
from teoria_senales.storage.json_repository import JsonSessionRepository


SESSION_KEY = "c3_3_tracker"
HELP_KEY = "c3_3_step_1_help"
HELP_KEY_PREFIX = "c3_3_help_"
LEAVE_CONFIRMATION_KEY = "c3_3_leave_confirmation"
SESSION_PATH_KEY = "c3_3_session_path"
RECOVERY_PATH_KEY = "c3_3_recovery_path"
RECOVERY_CODE_KEY = "c3_3_recovery_code"
EVALUATION_STARTED_KEY = "c3_3_evaluation_started"
EVALUATION_REVIEW_KEY = "c3_3_evaluation_review"
EVALUATION_DRAFT_KEY = "c3_3_evaluation_draft"
GUIDED_STEP_IDS = ("paso_1", "paso_2", "paso_3", "paso_4")
STEP_TITLES = {
    "paso_1": "Reconocimiento de las señales",
    "paso_2": "Convolución lineal",
    "paso_3": "Verificación DFT/FFT con N = 3",
    "paso_4": "Verificación DFT/FFT con N = 5",
}
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


def start_final_evaluation() -> None:
    st.session_state[EVALUATION_STARTED_KEY] = True


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
    st.session_state[EVALUATION_STARTED_KEY] = (
        tracker.session.evaluation is not None
    )
    st.session_state[EVALUATION_REVIEW_KEY] = False
    st.session_state.pop(EVALUATION_DRAFT_KEY, None)
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
            padding-top: 5rem;
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


def format_attempt_count(count: int) -> str:
    label = "intento registrado" if count == 1 else "intentos registrados"
    return f"{count} {label}"


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


def render_signal_explorer() -> None:
    st.divider()
    st.subheader("Explorador de señales")
    st.write(
        "Prueba otras secuencias discretas y observa cómo cambia la "
        "convolución. Este espacio no modifica la sesión ni la calificación."
    )

    with st.form("signal_explorer"):
        x_column, h_column = st.columns(2)
        with x_column:
            x_value = st.text_input(
                "Muestras de x[n]",
                value="1, 2, 1",
                help="Ingresa entre 2 y 8 valores separados por comas.",
            )
        with h_column:
            h_value = st.text_input(
                "Muestras de h[n]",
                value="1, -1, 2",
                help="Ingresa entre 2 y 8 valores separados por comas.",
            )
        transform_length = st.number_input(
            "Longitud de transformación N",
            min_value=2,
            max_value=15,
            value=5,
            step=1,
        )
        generated = st.form_submit_button(
            "Generar y comparar",
            type="primary",
            width="stretch",
        )

    if not generated:
        st.caption(
            "Elige las muestras y una longitud N para generar la comparación."
        )
        return

    try:
        exploration = explore_signals(
            x_value,
            h_value,
            int(transform_length),
        )
    except ValueError as error:
        st.warning(str(error))
        return

    input_x_column, input_h_column = st.columns(2)
    with input_x_column:
        render_signal_card(exploration.x, "x[n] explorada")
    with input_h_column:
        render_signal_card(exploration.h, "h[n] explorada")

    st.markdown("#### Comparación de resultados")
    linear_column, frequency_column = st.columns(2)
    with linear_column:
        render_signal_card(
            exploration.linear_result,
            "Convolución lineal",
        )
    with frequency_column:
        render_signal_card(
            exploration.frequency_result,
            f"Resultado con N = {exploration.transform_length}",
        )

    if exploration.has_circular_overlap:
        st.warning(
            f"N = {exploration.transform_length} es menor que la longitud "
            f"mínima {exploration.minimum_length}. El resultado presenta "
            "solapamiento circular."
        )
    else:
        st.success(
            f"N = {exploration.transform_length} alcanza la longitud mínima "
            f"{exploration.minimum_length}. El resultado frecuencial conserva "
            "la convolución lineal."
        )


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
    help_requested = bool(step.help_requests)
    with st.form("step_one_answer"):
        lx_column, lh_column, ly_column = st.columns(3)
        with lx_column:
            lx = st.number_input(
                r"$L_x$",
                min_value=1,
                step=1,
                value=saved_values[0],
                disabled=completed,
                placeholder="Longitud de x[n]",
            )
        with lh_column:
            lh = st.number_input(
                r"$L_h$",
                min_value=1,
                step=1,
                value=saved_values[1],
                disabled=completed,
                placeholder="Longitud de h[n]",
            )
        with ly_column:
            ly = st.number_input(
                r"$L_y$",
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
        if st.button(
            "Ver orientación",
            width="stretch",
            disabled=completed or help_requested,
        ):
            tracker.register_help("paso_1", definition.hint)
            st.session_state[HELP_KEY] = True
            save_active_session()
            st.rerun()
    with status_column:
        if completed:
            st.success("Paso 1 completado. El resultado quedó guardado en la sesión.")
        elif step.attempts:
            st.caption(format_attempt_count(len(step.attempts)))

    if (
        st.session_state.get(HELP_KEY, False) or help_requested
    ) and not completed:
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


def render_completed_step_summary(
    tracker,
    step_id: str,
    reveal_result: bool,
) -> None:
    step = tracker.session.steps[step_id]
    step_number = GUIDED_STEP_IDS.index(step_id) + 1
    title = STEP_TITLES[step_id]

    with st.expander(f"Paso {step_number} · {title} · completado"):
        st.caption(format_attempt_count(len(step.attempts)))
        if step.help_requests:
            st.caption("Orientación consultada")

        if not reveal_result:
            st.write(
                "El detalle del resultado se mostrará al finalizar la evaluación."
            )
            return

        if step_id == "paso_1":
            answer = step.attempts[-1].answer
            if isinstance(answer, (list, tuple)) and len(answer) == 3:
                lx, lh, ly = (int(float(value)) for value in answer)
                st.markdown(
                    rf"$L_x={lx}$, $L_h={lh}$ y $L_y={ly}$."
                )
        elif step_id == "paso_2":
            st.write(f"Resultado: {saved_sequence_answer(step)}")
        elif step_id == "paso_3":
            st.write(f"Resultado con N = 3: {saved_sequence_answer(step)}")
            st.caption(
                "La longitud N = 3 produce solapamiento circular."
            )
        elif step_id == "paso_4":
            st.write(f"Resultado con N = 5: {saved_sequence_answer(step)}")
            st.caption(
                "Con N = 5, el resultado coincide con la convolución lineal."
            )


def render_completed_step_summaries(
    tracker,
    step_ids: tuple[str, ...],
    reveal_results: bool,
) -> None:
    for step_id in step_ids:
        render_completed_step_summary(tracker, step_id, reveal_results)


def render_step_two(tracker) -> None:
    exercise = tracker.exercise
    step = tracker.session.steps["paso_2"]
    definition = exercise.get_step("paso_2")
    completed = step.status == StepStatus.COMPLETED
    help_key = f"{HELP_KEY_PREFIX}paso_2"
    help_requested = bool(step.help_requests)

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
            disabled=completed or help_requested,
        ):
            tracker.register_help("paso_2", definition.hint)
            st.session_state[help_key] = True
            save_active_session()
            st.rerun()
    with status_column:
        if completed:
            st.success(
                "Paso 2 completado. La convolución lineal quedó guardada."
            )
        elif step.attempts:
            st.caption(format_attempt_count(len(step.attempts)))

    if (
        st.session_state.get(help_key, False) or help_requested
    ) and not completed:
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
    help_requested = bool(step.help_requests)

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
            "Resultado temporal mediante DFT/FFT con N = 3",
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
            disabled=completed or help_requested,
        ):
            tracker.register_help("paso_3", definition.hint)
            st.session_state[help_key] = True
            save_active_session()
            st.rerun()
    with status_column:
        if completed:
            st.success(
                "Paso 3 completado. El resultado con N = 3 quedó guardado."
            )
        elif step.attempts:
            st.caption(format_attempt_count(len(step.attempts)))

    if (
        st.session_state.get(help_key, False) or help_requested
    ) and not completed:
        st.info(definition.hint)

    if completed:
        st.markdown("#### Resultado comprobado")
        render_signal_card(
            np.asarray(exercise.expected_results["resultado_N3"]),
            "y[n] para N = 3",
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
    help_requested = bool(step.help_requests)

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
            "Resultado temporal mediante DFT/FFT con N = 5",
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
            disabled=completed or help_requested,
        ):
            tracker.register_help("paso_4", definition.hint)
            st.session_state[help_key] = True
            save_active_session()
            st.rerun()
    with status_column:
        if completed:
            st.success(
                "Paso 4 completado. El resultado con N = 5 quedó guardado."
            )
        elif step.attempts:
            st.caption(format_attempt_count(len(step.attempts)))

    if (
        st.session_state.get(help_key, False) or help_requested
    ) and not completed:
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
                "y[n] para N = 5",
            )
        st.success(
            "Con N = 5 no hay solapamiento circular: el resultado coincide "
            "con la convolución lineal."
        )


def render_step_four_result(tracker) -> None:
    exercise = tracker.exercise

    st.divider()
    st.progress(0.8, text="Paso 4 de 5 · Resultado verificado")
    st.subheader("Comparación de resultados")
    linear_column, fft_column = st.columns(2)
    with linear_column:
        render_signal_card(
            np.asarray(exercise.expected_results["convolucion_lineal"]),
            "Convolución lineal y[n]",
        )
    with fft_column:
        render_signal_card(
            np.asarray(exercise.expected_results["resultado_N5"]),
            "Resultado y[n] para N = 5",
        )
    st.success(
        "Con N = 5 no hay solapamiento circular: el resultado coincide "
        "con la convolución lineal."
    )
    st.write(
        "El recorrido guiado está completo. Al iniciar la evaluación, "
        "los resultados anteriores quedarán ocultos hasta el envío final."
    )
    st.button(
        "Iniciar evaluación",
        key="start_final_evaluation",
        on_click=start_final_evaluation,
        type="primary",
        width="stretch",
    )


def format_grade(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def render_evaluation_summary(session) -> None:
    evaluation = session.evaluation
    if evaluation is None:
        return

    st.success("Evaluación finalizada. Las respuestas quedaron guardadas.")
    points_column, grade_column = st.columns(2)
    with points_column:
        st.metric(
            "Puntaje",
            f"{evaluation.points_earned}/{evaluation.points_possible}",
        )
    with grade_column:
        st.metric("Nota final", format_grade(evaluation.grade))

    st.markdown("#### Resultado por pregunta")
    question_rows = [
        "| Pregunta | Resultado | Puntos |",
        "|---|---|---:|",
    ]
    for result in evaluation.questions:
        question_rows.append(
            "| "
            f"{result.question_id} | "
            f"{'Correcta' if result.correct else 'Por reforzar'} | "
            f"{result.points_earned}/{result.points_possible} |"
        )
    st.markdown("\n".join(question_rows))

    st.markdown("#### Resultado por criterio")
    criterion_rows = [
        "| Criterio | Resultado |",
        "|---|---|",
    ]
    for criterion in session.criteria:
        status = (
            "Alcanzado"
            if criterion.status.value == "alcanzado"
            else "Requiere refuerzo"
        )
        criterion_rows.append(
            f"| {criterion.criterion_id} | {status} |"
        )
    st.markdown("\n".join(criterion_rows))

    st.download_button(
        "Descargar reporte docente protegido",
        data=generate_pdf_report_bytes(session),
        file_name=report_filename(session),
        mime="application/pdf",
        type="primary",
        width="stretch",
    )
    st.caption(
        "Código de verificación: "
        f"`{report_verification_code(session)}`. El docente puede compararlo "
        "con el registro original de la sesión."
    )
    render_signal_explorer()


def render_evaluation_review(
    tracker,
    option_labels: dict[str, dict[str, str]],
) -> None:
    exercise = tracker.exercise
    draft = st.session_state.get(EVALUATION_DRAFT_KEY)
    if not draft:
        st.session_state[EVALUATION_REVIEW_KEY] = False
        st.rerun()

    st.subheader("Revisa tus respuestas")
    st.write(
        "La evaluación se calificará cuando confirmes el envío. "
        "Todavía puedes volver y corregir una respuesta."
    )
    rows = [
        "| Pregunta | Respuesta registrada |",
        "|---|---|",
    ]
    for question in get_c3_3_questions():
        answer = draft[question.question_id]
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            displayed_answer = option_labels[question.question_id][answer]
        elif question.question_type == QuestionType.TRUE_FALSE:
            displayed_answer = "Verdadero" if answer else "Falso"
        else:
            displayed_answer = answer
        rows.append(f"| {question.question_id} | {displayed_answer} |")
    st.markdown("\n".join(rows))

    edit_column, confirm_column = st.columns(2)
    with edit_column:
        edit = st.button(
            "Volver a editar",
            key="evaluation_edit",
            width="stretch",
        )
    with confirm_column:
        confirm = st.button(
            "Confirmar y calificar",
            key="evaluation_confirm",
            type="primary",
            width="stretch",
        )

    if edit:
        st.session_state[EVALUATION_REVIEW_KEY] = False
        st.rerun()
    if confirm:
        evaluation = evaluate_c3_3(draft)
        tracker.record_evaluation(evaluation)
        tracker.complete(exercise.expected_results)
        save_active_session()
        st.session_state[EVALUATION_REVIEW_KEY] = False
        st.session_state.pop(EVALUATION_DRAFT_KEY, None)
        st.rerun()


def render_step_five(tracker) -> None:
    session = tracker.session

    st.divider()
    st.progress(1.0, text="Paso 5 de 5 · Evaluación final")
    if session.evaluation is not None:
        render_evaluation_summary(session)
        return

    questions = get_c3_3_questions()
    option_labels = {
        question.question_id: {
            code: f"{code.upper()}. {text}"
            for code, text in question.options
        }
        for question in questions
        if question.question_type == QuestionType.MULTIPLE_CHOICE
    }
    option_codes = {
        question_id: {
            label: code
            for code, label in labels.items()
        }
        for question_id, labels in option_labels.items()
    }

    if st.session_state.get(EVALUATION_REVIEW_KEY, False):
        render_evaluation_review(tracker, option_labels)
        return

    st.subheader("Compara e interpreta los resultados")
    st.write(
        "Responde las ocho preguntas. El puntaje total es de 18 puntos "
        "y la nota se calcula en una escala de 0,0 a 5,0."
    )
    st.caption(
        "Antes del envío final podrás revisar las ocho respuestas."
    )

    draft = st.session_state.get(EVALUATION_DRAFT_KEY, {})
    form_answers: dict[str, object] = {}

    form_placeholder = st.empty()
    with form_placeholder.form("final_evaluation"):
        for question in questions:
            point_label = "punto" if question.points == 1 else "puntos"
            st.markdown(
                f"**{question.question_id} · {question.points} "
                f"{point_label}**  \n{question.prompt}"
            )
            if question.question_type == QuestionType.NUMERIC:
                expected_length = len(question.expected_answer)
                form_answers[question.question_id] = st.text_input(
                    f"Respuesta numérica {question.question_id}",
                    value=draft.get(question.question_id, ""),
                    placeholder=f"Escribe {expected_length} valores",
                    key=f"evaluation_{question.question_id}",
                )
            elif question.question_type == QuestionType.MULTIPLE_CHOICE:
                labels = option_labels[question.question_id]
                options = tuple(labels.values())
                saved_label = labels.get(draft.get(question.question_id))
                selected_index = (
                    options.index(saved_label)
                    if saved_label in options
                    else None
                )
                form_answers[question.question_id] = st.radio(
                    f"Selecciona una respuesta en {question.question_id}",
                    options,
                    index=selected_index,
                    key=f"evaluation_{question.question_id}",
                )
            else:
                options = ("Verdadero", "Falso")
                saved_answer = draft.get(question.question_id)
                selected_index = (
                    0 if saved_answer is True
                    else 1 if saved_answer is False
                    else None
                )
                form_answers[question.question_id] = st.radio(
                    f"Selecciona una respuesta en {question.question_id}",
                    options,
                    index=selected_index,
                    horizontal=True,
                    key=f"evaluation_{question.question_id}",
                )

        submitted = st.form_submit_button(
            "Revisar respuestas",
            type="primary",
            width="stretch",
        )

    if submitted:
        invalid_numeric = [
            question.question_id
            for question in questions
            if question.question_type == QuestionType.NUMERIC
            and parse_numeric_sequence(form_answers[question.question_id]) is None
        ]
        if invalid_numeric:
            st.warning(
                f"Completa {', '.join(invalid_numeric)} únicamente con valores "
                "numéricos separados "
                "por comas, espacios o punto y coma."
            )
            return
        unselected = [
            question.question_id
            for question in questions
            if question.question_type != QuestionType.NUMERIC
            and form_answers[question.question_id] is None
        ]
        if unselected:
            st.warning(
                f"Selecciona una respuesta en {', '.join(unselected)} "
                "antes de calificar."
            )
            return

        evaluation_draft: dict[str, object] = {}
        for question in questions:
            answer = form_answers[question.question_id]
            if question.question_type == QuestionType.NUMERIC:
                evaluation_draft[question.question_id] = answer.strip()
            elif question.question_type == QuestionType.MULTIPLE_CHOICE:
                evaluation_draft[question.question_id] = option_codes[
                    question.question_id
                ][answer]
            else:
                evaluation_draft[question.question_id] = answer == "Verdadero"
        st.session_state[EVALUATION_DRAFT_KEY] = evaluation_draft
        st.session_state[EVALUATION_REVIEW_KEY] = True
        form_placeholder.empty()
        render_evaluation_review(tracker, option_labels)


def render_active_session() -> None:
    tracker = st.session_state[SESSION_KEY]
    session = tracker.session

    st.markdown(
        '<p class="exercise-label">Componente 3 · Ejercicio C3-3</p>',
        unsafe_allow_html=True,
    )
    st.title("Convolución de señales discretas")
    st.caption(f"Código estudiantil: {session.student_id}")

    active_step = next(
        (
            step_id
            for step_id in GUIDED_STEP_IDS
            if session.steps[step_id].status != StepStatus.COMPLETED
        ),
        None,
    )
    if active_step is None:
        if (
            session.evaluation is None
            and not st.session_state.get(EVALUATION_STARTED_KEY, False)
        ):
            active_view = "paso_4_resultado"
        else:
            active_view = "paso_5"
    else:
        active_view = active_step

    if active_view in GUIDED_STEP_IDS:
        active_index = GUIDED_STEP_IDS.index(active_view)
        summary_ids = tuple(
            step_id
            for step_id in GUIDED_STEP_IDS[:active_index]
            if session.steps[step_id].status == StepStatus.COMPLETED
        )
    elif active_view == "paso_4_resultado":
        summary_ids = GUIDED_STEP_IDS[:3]
    else:
        summary_ids = GUIDED_STEP_IDS

    render_completed_step_summaries(
        tracker,
        summary_ids,
        reveal_results=(
            active_view != "paso_5" or session.evaluation is not None
        ),
    )

    renderers = {
        "paso_1": render_step_one,
        "paso_2": render_step_two,
        "paso_3": render_step_three,
        "paso_4": render_step_four,
        "paso_4_resultado": render_step_four_result,
        "paso_5": render_step_five,
    }
    renderers[active_view](tracker)

    if not st.session_state.get(LEAVE_CONFIRMATION_KEY, False):
        if st.button("Volver al inicio", key="return_to_start"):
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
            key="confirm_return_to_start",
            type="primary",
            width="stretch",
        )
    with cancel_column:
        cancel = st.button(
            "Continuar ejercicio",
            key="cancel_return_to_start",
            width="stretch",
        )

    if leave:
        save_active_session()
        for key in (
            SESSION_KEY,
            HELP_KEY,
            LEAVE_CONFIRMATION_KEY,
            SESSION_PATH_KEY,
            EVALUATION_STARTED_KEY,
            EVALUATION_REVIEW_KEY,
            EVALUATION_DRAFT_KEY,
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
    if HEADER_IMAGE.is_file():
        st.image(str(HEADER_IMAGE), width="stretch")

    if SESSION_KEY in st.session_state:
        render_active_session()
    else:
        render_access_screen()


if __name__ == "__main__":
    main()
