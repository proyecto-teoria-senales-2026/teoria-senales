"""Punto de entrada del prototipo de convolución."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.pilot_cli import run_demo, run_interactive


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Piloto del ejercicio guiado de convolución para Teoría de Señales."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Genera una sesión de demostración sin solicitar entradas por consola.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(PROJECT_ROOT / "demo_outputs"),
        help="Carpeta en la que se guardan la sesión JSON y el reporte PDF.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    runner = run_demo if args.demo else run_interactive
    json_path, pdf_path = runner(args.output_dir)
    print("\nSesión registrada correctamente.")
    print(f"Datos de la sesión: {json_path}")
    print(f"Reporte para el docente: {pdf_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
