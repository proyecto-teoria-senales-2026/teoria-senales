"""Limpia el encabezado y normaliza los metadatos de las guías PDF."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "docs" / "guias"
HEADER = ROOT / "src" / "teoria_senales" / "assets" / "encabezado_institucional.png"
AUTHORS = "Juan Esteban Rengifo Segura; Julián Felipe Montaña Aguilar"


def _header_overlay() -> object:
    buffer = BytesIO()
    page = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    header_height = width * 161 / 876
    page.setFillColorRGB(1, 1, 1)
    page.rect(0, height - header_height, width, header_height, stroke=0, fill=1)
    page.drawImage(
        str(HEADER),
        0,
        height - header_height,
        width=width,
        height=header_height,
        preserveAspectRatio=False,
        mask="auto",
    )
    # El PDF maestro conserva un punto residual en el borde izquierdo, dentro
    # de la franja inferior del encabezado. La máscara se dibuja sobre la
    # imagen, en las coordenadas reales del punto, sin cubrir la línea azul.
    page.setFillColorRGB(1, 1, 1)
    page.rect(0, height - header_height, 12, 10, stroke=0, fill=1)
    page.save()
    buffer.seek(0)
    return PdfReader(buffer).pages[0]


def rebuild(path: Path) -> None:
    reader = PdfReader(path)
    overlay = _header_overlay()
    writer = PdfWriter()
    for source_page in reader.pages:
        source_page.merge_page(overlay, over=True)
        writer.add_page(source_page)
    metadata = dict(reader.metadata or {})
    metadata.update(
        {
            "/Author": AUTHORS,
            "/Creator": "Proyecto Teoría de Señales",
            "/Producer": "Proyecto Teoría de Señales",
        }
    )
    writer.add_metadata(metadata)
    temporary = path.with_suffix(".tmp.pdf")
    with temporary.open("wb") as stream:
        writer.write(stream)
    temporary.replace(path)


def main() -> int:
    if not HEADER.is_file():
        raise FileNotFoundError(f"No existe el encabezado institucional: {HEADER}")
    guides = sorted(GUIDES.glob("Guia_del_estudiante_C-*.pdf"))
    if len(guides) != 5:
        raise RuntimeError(f"Se esperaban 5 guías y se encontraron {len(guides)}")
    for guide in guides:
        rebuild(guide)
        print(f"Actualizada: {guide.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
