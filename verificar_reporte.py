"""Punto de entrada del verificador docente de reportes PDF."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.reports.pdf_verifier import verify_pdf_against_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verifica un reporte PDF contra su sesión JSON original."
    )
    parser.add_argument("pdf", type=Path, help="Ruta del reporte PDF recibido.")
    parser.add_argument(
        "--sessions",
        type=Path,
        default=PROJECT_ROOT / "session_outputs",
        help="Carpeta que contiene los registros JSON originales.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        pdf_data = args.pdf.read_bytes()
    except OSError as error:
        print(f"NO VERIFICABLE: {error}")
        return 2

    result = verify_pdf_against_repository(pdf_data, args.sessions)
    print(result.status)
    for detail in result.details:
        print(f"- {detail}")
    if result.session_id:
        print(f"- Sesión: {result.session_id}")
        print(f"- Estudiante: {result.student_id}")
        print(f"- Ejercicio: {result.exercise_id}")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
