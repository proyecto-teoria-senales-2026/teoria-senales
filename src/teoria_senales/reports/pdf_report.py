"""Generador del reporte de seguimiento por estudiante y ejercicio."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import matplotlib
import reportlab

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from teoria_senales.domain.models import SessionRecord
from teoria_senales.storage.json_repository import safe_name


NAVY = colors.HexColor("#233F6B")
BLUE = colors.HexColor("#3568A8")
LIGHT_BLUE = colors.HexColor("#EAF1F8")
LIGHT_GRAY = colors.HexColor("#F3F4F6")
REGULAR_FONT = "Vera"
BOLD_FONT = "Vera-Bold"
HEADER_IMAGE = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "encabezado_institucional.png"
)


def _register_fonts() -> None:
    """Incrusta una tipografía estable para conservar el diseño del PDF."""

    fonts_directory = Path(reportlab.__file__).resolve().parent / "fonts"
    if REGULAR_FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(REGULAR_FONT, fonts_directory / "Vera.ttf"))
    if BOLD_FONT not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(BOLD_FONT, fonts_directory / "VeraBd.ttf"))
    pdfmetrics.registerFontFamily(
        REGULAR_FONT,
        normal=REGULAR_FONT,
        bold=BOLD_FONT,
        italic=REGULAR_FONT,
        boldItalic=BOLD_FONT,
    )


def _display_status(value: str) -> str:
    labels = {
        "no_iniciado": "No iniciado",
        "en_proceso": "En proceso",
        "completado": "Completado",
        "revision_docente": "Revisión docente",
        "alcanzado": "Alcanzado",
        "requiere_refuerzo": "Requiere refuerzo",
    }
    return labels.get(value, value.replace("_", " ").capitalize())


def _format_sequence(values: object) -> str:
    if not isinstance(values, list):
        return str(values)
    formatted: list[str] = []
    for value in values:
        number = float(value)
        formatted.append(str(int(number)) if number.is_integer() else f"{number:.4g}")
    return "{" + ", ".join(formatted) + "}"


def _format_answer(value: object) -> str:
    if isinstance(value, bool):
        return "Verdadero" if value else "Falso"
    if isinstance(value, list):
        return _format_sequence(value)
    return str(value)


def _format_date(value: str) -> str:
    date_part = value[:10]
    try:
        year, month, day = date_part.split("-")
    except ValueError:
        return date_part
    return f"{day}/{month}/{year}"


def _results_figure(session: SessionRecord) -> BytesIO:
    linear = session.results.get("convolucion_lineal", [])
    n3 = session.results.get("resultado_N3", [])
    n5 = session.results.get("resultado_N5", [])
    figure, axes = plt.subplots(3, 1, figsize=(7.0, 5.3), constrained_layout=True)
    for axis, values, title in zip(
        axes,
        (linear, n3, n5),
        ("Convolución lineal", "Verificación con N = 3", "Verificación con N = 5"),
    ):
        indices = list(range(len(values)))
        axis.stem(indices, values, basefmt=" ")
        axis.set_title(title, fontsize=9)
        axis.set_xlabel("n", fontsize=8)
        axis.set_ylabel("Amplitud", fontsize=8)
        axis.set_xticks(indices)
        axis.grid(alpha=0.25)
        axis.tick_params(labelsize=8)
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=160, bbox_inches="tight")
    plt.close(figure)
    buffer.seek(0)
    return buffer


def generate_pdf_report(session: SessionRecord, output_directory: str | Path) -> Path:
    _register_fonts()
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = f"reporte_{safe_name(session.student_id)}_{session.exercise_id}.pdf"
    destination = output_path / filename

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName=BOLD_FONT,
            fontSize=17,
            leading=21,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontName=BOLD_FONT,
            fontSize=11,
            leading=14,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ExerciseTitle",
            parent=styles["Heading3"],
            fontName=BOLD_FONT,
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.black,
            spaceAfter=8,
        )
    )
    styles["BodyText"].fontName = REGULAR_FONT
    styles["BodyText"].fontSize = 9.2
    styles["BodyText"].leading = 12.3

    document = SimpleDocTemplate(
        str(destination),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=3.1 * cm,
        bottomMargin=1.5 * cm,
        title=f"Reporte de seguimiento - {session.exercise_id}",
        author="Proyecto Teoría de Señales",
    )

    story: list[object] = [
        Paragraph("Reporte de seguimiento del ejercicio", styles["ReportTitle"]),
        Paragraph(session.exercise_title, styles["ExerciseTitle"]),
        Spacer(1, 8),
    ]

    identity_data = [
        ["Estudiante", session.student_name, "Identificación", session.student_id],
        ["Ejercicio", session.exercise_id, "Fecha", _format_date(session.finished_at or session.started_at)],
        ["Sesión", session.session_id[:8], "Estado", "Finalizada" if session.finished_at else "En curso"],
    ]
    identity_table = Table(identity_data, colWidths=[2.2 * cm, 5.6 * cm, 2.2 * cm, 5.6 * cm])
    identity_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                ("BACKGROUND", (2, 0), (2, -1), LIGHT_BLUE),
                ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                ("TEXTCOLOR", (2, 0), (2, -1), NAVY),
                ("FONTNAME", (0, 0), (0, -1), BOLD_FONT),
                ("FONTNAME", (2, 0), (2, -1), BOLD_FONT),
                ("FONTNAME", (0, 0), (-1, -1), REGULAR_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B7C6D8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([identity_table, Paragraph("Seguimiento por paso", styles["Section"])])

    step_rows = [["Paso", "Intentos", "Correcciones", "Ayudas", "Estado"]]
    for step in session.steps.values():
        step_rows.append(
            [
                Paragraph(step.title, styles["BodyText"]),
                str(len(step.attempts)),
                str(step.corrections),
                str(len(step.help_requests)),
                _display_status(step.status.value),
            ]
        )
    step_table = Table(step_rows, colWidths=[8.1 * cm, 1.8 * cm, 2.1 * cm, 1.6 * cm, 2.6 * cm], repeatRows=1)
    step_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("FONTNAME", (0, 1), (-1, -1), REGULAR_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("FONTSIZE", (0, 0), (-1, 0), 7.2),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C6CDD6")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.extend([step_table, Paragraph("Resultados registrados", styles["Section"])])

    result_rows = [["Resultado", "Valor"]]
    result_rows.append(
        [
            "Longitudes identificadas",
            (
                f"Lx = {session.results.get('Lx', '-')}, "
                f"Lh = {session.results.get('Lh', '-')}, "
                f"Ly = {session.results.get('Ly', '-')}"
            ),
        ]
    )
    for key, label in (
        ("convolucion_lineal", "Convolución lineal"),
        ("resultado_N3", "Resultado con N = 3"),
        ("resultado_N5", "Resultado con N = 5"),
    ):
        result_rows.append([label, _format_sequence(session.results.get(key, []))])
    result_table = Table(result_rows, colWidths=[6.0 * cm, 10.2 * cm], repeatRows=1)
    result_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("FONTNAME", (0, 1), (-1, -1), REGULAR_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C6CDD6")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    chart = Image(_results_figure(session), width=15.5 * cm, height=8.7 * cm)
    story.extend([result_table, Spacer(1, 8), chart, PageBreak()])

    story.append(Paragraph("Evaluación automática", styles["Section"]))
    if session.evaluation is not None:
        evaluation_summary = Table(
            [
                [
                    "Puntaje",
                    (
                        f"{session.evaluation.points_earned}/"
                        f"{session.evaluation.points_possible}"
                    ),
                    "Nota",
                    f"{session.evaluation.grade:.2f}".replace(".", ","),
                ]
            ],
            colWidths=[2.3 * cm, 3.3 * cm, 2.3 * cm, 3.3 * cm],
        )
        evaluation_summary.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                    ("BACKGROUND", (2, 0), (2, -1), LIGHT_BLUE),
                    ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                    ("TEXTCOLOR", (2, 0), (2, -1), NAVY),
                    ("FONTNAME", (0, 0), (-1, -1), REGULAR_FONT),
                    ("FONTNAME", (0, 0), (0, -1), BOLD_FONT),
                    ("FONTNAME", (2, 0), (2, -1), BOLD_FONT),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C6CDD6")),
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        question_rows = [["Pregunta", "Respuesta", "Resultado", "Puntaje", "Criterio"]]
        for question in session.evaluation.questions:
            question_rows.append(
                [
                    question.question_id,
                    Paragraph(_format_answer(question.answer), styles["BodyText"]),
                    "Correcta" if question.correct else "Incorrecta",
                    f"{question.points_earned}/{question.points_possible}",
                    ", ".join(question.criterion_ids),
                ]
            )
        question_table = Table(
            question_rows,
            colWidths=[2.0 * cm, 5.6 * cm, 2.4 * cm, 2.1 * cm, 4.1 * cm],
            repeatRows=1,
        )
        question_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                    ("FONTNAME", (0, 1), (-1, -1), REGULAR_FONT),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("ALIGN", (0, 1), (0, -1), "CENTER"),
                    ("ALIGN", (2, 1), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C6CDD6")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.extend([evaluation_summary, Spacer(1, 7), question_table])
    else:
        story.append(Paragraph("Evaluación pendiente.", styles["BodyText"]))

    story.append(Paragraph("Criterios de revisión", styles["Section"]))

    criteria_rows = [["Criterio", "Estado", "Evidencia"]]
    for criterion in session.criteria:
        criteria_rows.append(
            [
                Paragraph(criterion.description, styles["BodyText"]),
                _display_status(criterion.status.value),
                Paragraph(criterion.evidence, styles["BodyText"]),
            ]
        )
    criteria_table = Table(criteria_rows, colWidths=[8.4 * cm, 2.8 * cm, 5.0 * cm], repeatRows=1)
    criteria_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("FONTNAME", (0, 1), (-1, -1), REGULAR_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C6CDD6")),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(criteria_table)

    reinforcement = []
    for step in session.steps.values():
        if step.corrections or step.help_requests:
            reinforcement.extend(step.difficulties)
    story.append(Paragraph("Aspectos que pueden requerir refuerzo", styles["Section"]))
    if reinforcement:
        for item in dict.fromkeys(reinforcement):
            story.append(Paragraph(f"- {item}", styles["BodyText"]))
    else:
        story.append(
            Paragraph(
                "No se registraron correcciones ni solicitudes de ayuda en los pasos con validación automática.",
                styles["BodyText"],
            )
        )

    def add_page_chrome(canvas: object, doc: object) -> None:
        canvas.saveState()
        header_height = A4[0] * 108 / 838
        canvas.drawImage(
            str(HEADER_IMAGE),
            0,
            A4[1] - header_height,
            width=A4[0],
            height=header_height,
            preserveAspectRatio=False,
            mask="auto",
        )
        canvas.setFont(REGULAR_FONT, 7.5)
        canvas.setFillColor(colors.HexColor("#667085"))
        canvas.drawString(1.7 * cm, 0.8 * cm, "Proyecto Teoría de Señales")
        canvas.drawRightString(A4[0] - 1.7 * cm, 0.8 * cm, f"Página {doc.page}")
        canvas.restoreState()

    document.build(story, onFirstPage=add_page_chrome, onLaterPages=add_page_chrome)
    return destination
