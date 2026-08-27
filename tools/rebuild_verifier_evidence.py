"""Regenera la pareja de evidencia válida/alterada del verificador."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import sys

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.reports.pdf_report import generate_pdf_report_bytes
from teoria_senales.storage.json_repository import JsonSessionRepository


EVIDENCE = ROOT / "docs" / "evidencias" / "verificacion"
SESSION_FILE = EVIDENCE / "sesion_DEMO-VERIFICACION_C3-3_DEMO-VERIFICACION-C3-3.json"
VALID_REPORT = EVIDENCE / "reporte_original_valido_C-3-3.pdf"
ALTERED_REPORT = EVIDENCE / "reporte_copia_alterada_C-3-3.pdf"


def _altered_copy(pdf_data: bytes) -> bytes:
    reader = PdfReader(BytesIO(pdf_data))
    if reader.is_encrypted and reader.decrypt("") == 0:
        raise ValueError("No se pudo abrir el reporte original protegido.")

    overlay_buffer = BytesIO()
    overlay = canvas.Canvas(overlay_buffer, pagesize=A4)
    overlay.setFillColor(HexColor("#A61B1B"))
    overlay.setFont("Helvetica-Bold", 10)
    overlay.drawString(48, 42, "COPIA ALTERADA PARA COMPROBAR EL VERIFICADOR")
    overlay.save()
    overlay_buffer.seek(0)

    first_page = reader.pages[0]
    first_page.merge_page(PdfReader(overlay_buffer).pages[0], over=True)
    writer = PdfWriter()
    writer.add_page(first_page)
    for page in reader.pages[1:]:
        writer.add_page(page)
    writer.add_metadata(dict(reader.metadata or {}))
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def main() -> int:
    repository = JsonSessionRepository(EVIDENCE)
    session = repository.load(SESSION_FILE)
    valid_data = generate_pdf_report_bytes(session)
    VALID_REPORT.write_bytes(valid_data)
    ALTERED_REPORT.write_bytes(_altered_copy(valid_data))
    print(f"Actualizado: {VALID_REPORT.relative_to(ROOT)}")
    print(f"Actualizado: {ALTERED_REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
