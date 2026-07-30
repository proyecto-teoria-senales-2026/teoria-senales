"""Generación del reporte docente corto por sesión."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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
        "alcanzado": "Alcanzado",
        "requiere_refuerzo": "Requiere refuerzo",
        "revision_docente": "Revisión docente",
    }
    return labels.get(value, value.replace("_", " ").capitalize())


def _format_date(value: str) -> str:
    date_part = value[:10]
    try:
        year, month, day = date_part.split("-")
    except ValueError:
        return date_part
    return f"{day}/{month}/{year}"


def _rae_id(session: SessionRecord) -> str:
    if session.evaluation is None:
        return "-"
    rae_ids = dict.fromkeys(
        question.rae_id for question in session.evaluation.questions
    )
    return ", ".join(rae_ids) or "-"


def _questions_by_criterion(session: SessionRecord) -> dict[str, str]:
    if session.evaluation is None:
        return {}
    return {
        criterion.criterion_id: ", ".join(criterion.question_ids)
        for criterion in session.evaluation.criteria
    }


def report_filename(session: SessionRecord) -> str:
    session_code = safe_name(session.session_id)
    return (
        f"reporte_docente_{safe_name(session.student_id)}_"
        f"{safe_name(session.exercise_id)}_{session_code}.pdf"
    )


def _build_report(session: SessionRecord, destination: str | BytesIO) -> None:
    if session.evaluation is None or session.finished_at is None:
        raise ValueError(
            "El reporte docente solo está disponible al finalizar la evaluación."
        )

    _register_fonts()
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
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ExerciseTitle",
            parent=styles["Heading3"],
            fontName=REGULAR_FONT,
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.black,
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
            spaceBefore=11,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableText",
            parent=styles["BodyText"],
            fontName=REGULAR_FONT,
            fontSize=7.7,
            leading=10,
        )
    )

    document = SimpleDocTemplate(
        destination,
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=3.1 * cm,
        bottomMargin=1.5 * cm,
        title=f"Reporte docente - {session.exercise_id}",
        author="Proyecto Teoría de Señales",
    )

    identity_data = [
        ["Código estudiantil", session.student_id],
        ["Código de sesión", session.session_id],
        ["Ejercicio", f"{session.exercise_id} - {session.exercise_title}"],
        ["RAE", _rae_id(session)],
        ["Fecha de finalización", _format_date(session.finished_at)],
    ]
    identity_table = Table(identity_data, colWidths=[4.1 * cm, 12.1 * cm])
    identity_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                ("FONTNAME", (0, 0), (0, -1), BOLD_FONT),
                ("FONTNAME", (1, 0), (1, -1), REGULAR_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 8.3),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B7C6D8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    achieved_count = sum(
        criterion.status.value == "alcanzado" for criterion in session.criteria
    )
    summary_data = [
        ["Puntaje", "Nota final", "Criterios alcanzados"],
        [
            (
                f"{session.evaluation.points_earned}/"
                f"{session.evaluation.points_possible}"
            ),
            f"{session.evaluation.grade:.2f}".replace(".", ","),
            f"{achieved_count} de {len(session.criteria)}",
        ],
    ]
    summary_table = Table(summary_data, colWidths=[5.4 * cm] * 3)
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("FONTNAME", (0, 1), (-1, 1), BOLD_FONT),
                ("FONTSIZE", (0, 0), (-1, 0), 8.5),
                ("FONTSIZE", (0, 1), (-1, 1), 12),
                ("TEXTCOLOR", (0, 1), (-1, 1), NAVY),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B7C6D8")),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    questions_by_criterion = _questions_by_criterion(session)
    criterion_rows = [["Criterio", "Descripción", "Preguntas", "Resultado"]]
    for criterion in session.criteria:
        criterion_rows.append(
            [
                criterion.criterion_id,
                Paragraph(criterion.description, styles["TableText"]),
                questions_by_criterion.get(criterion.criterion_id, "-"),
                _display_status(criterion.status.value),
            ]
        )
    criteria_table = Table(
        criterion_rows,
        colWidths=[1.5 * cm, 9.3 * cm, 2.2 * cm, 3.2 * cm],
        repeatRows=1,
    )
    criteria_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), BOLD_FONT),
                ("FONTNAME", (0, 1), (-1, -1), REGULAR_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 7.7),
                ("ALIGN", (0, 1), (0, -1), "CENTER"),
                ("ALIGN", (2, 1), (-1, -1), "CENTER"),
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

    story = [
        Paragraph("Reporte docente del ejercicio", styles["ReportTitle"]),
        Paragraph(session.exercise_title, styles["ExerciseTitle"]),
        identity_table,
        Paragraph("Resultado de la evaluación", styles["Section"]),
        summary_table,
        Paragraph("Resultado por criterio", styles["Section"]),
        criteria_table,
        Spacer(1, 6),
    ]

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
        canvas.drawRightString(
            A4[0] - 1.7 * cm,
            0.8 * cm,
            f"Página {doc.page}",
        )
        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_page_chrome,
        onLaterPages=add_page_chrome,
    )


def generate_pdf_report_bytes(session: SessionRecord) -> bytes:
    buffer = BytesIO()
    _build_report(session, buffer)
    return buffer.getvalue()


def generate_pdf_report(
    session: SessionRecord,
    output_directory: str | Path,
) -> Path:
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    destination = output_path / report_filename(session)
    destination.write_bytes(generate_pdf_report_bytes(session))
    return destination
