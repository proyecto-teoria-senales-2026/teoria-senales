"""Almacenamiento local y auditable para la primera versión del piloto."""

from __future__ import annotations

import json
import re
from pathlib import Path

from teoria_senales.domain.models import SessionRecord


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return cleaned.strip("_") or "sesion"


class JsonSessionRepository:
    def __init__(self, output_directory: str | Path) -> None:
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def save(self, session: SessionRecord) -> Path:
        filename = f"sesion_{safe_name(session.student_id)}_{session.exercise_id}.json"
        destination = self.output_directory / filename
        destination.write_text(
            json.dumps(session.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return destination
