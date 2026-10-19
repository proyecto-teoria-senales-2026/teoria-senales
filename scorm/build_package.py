"""Genera paquetes SCORM 1.2 con una estructura uniforme y verificable.

Uso:
    python scorm/build_package.py c1-1
    python scorm/build_package.py c1-2
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
REQUIRED_FILES = (
    "imsmanifest.xml",
    "index.html",
    "styles.css",
    "activity.js",
    "scorm12-runtime.js",
)


def build(exercise: str) -> Path:
    source = ROOT / exercise
    if not source.is_dir():
        raise ValueError(f"No existe el ejercicio SCORM: {exercise}")

    missing = [name for name in REQUIRED_FILES if not (source / name).is_file()]
    if missing:
        raise ValueError(f"Faltan archivos requeridos: {', '.join(missing)}")

    DIST.mkdir(exist_ok=True)
    output = DIST / f"{exercise.upper().replace('-', '-')}_SCORM_1.2.zip"

    # El modo 'w' reemplaza solamente este ZIP con un paquete nuevo y completo.
    # No usa borrado de carpetas ni modifica otros ejercicios.
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name in REQUIRED_FILES:
            package.write(source / name, arcname=name)

    with zipfile.ZipFile(output) as package:
        names = set(package.namelist())
        if names != set(REQUIRED_FILES):
            raise RuntimeError("El ZIP no tiene la estructura SCORM esperada.")
        bad = package.testzip()
        if bad is not None:
            raise RuntimeError(f"El archivo comprimido está dañado: {bad}")
    return output


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Indica el ejercicio, por ejemplo: c1-1")
    print(build(sys.argv[1]))


if __name__ == "__main__":
    main()
