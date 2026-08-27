"""Almacenamiento local y auditable para la primera versión del piloto."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path

from teoria_senales.domain.models import SessionRecord


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return cleaned.strip("_") or "sesion"


class JsonSessionRepository:
    def __init__(self, output_directory: str | Path) -> None:
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def path_for(self, session: SessionRecord) -> Path:
        filename = (
            f"sesion_{safe_name(session.student_id)}_{session.exercise_id}_"
            f"{session.session_id}.json"
        )
        return self.output_directory / filename

    def save(self, session: SessionRecord) -> Path:
        destination = self.path_for(session)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.output_directory,
                prefix=f".{destination.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    session.to_dict(),
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                )
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            os.replace(temporary_path, destination)
        except Exception:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise
        return destination

    def load(self, source: str | Path) -> SessionRecord:
        data = json.loads(Path(source).read_text(encoding="utf-8"))
        return SessionRecord.from_dict(data)

    def find_latest_incomplete(
        self,
        student_id: str,
        exercise_id: str,
    ) -> tuple[SessionRecord, Path] | None:
        pattern = f"sesion_{safe_name(student_id)}_{exercise_id}_*.json"
        matches: list[tuple[SessionRecord, Path]] = []

        for path in self.output_directory.glob(pattern):
            try:
                session = self.load(path)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                continue
            if (
                session.student_id == student_id
                and session.exercise_id == exercise_id
                and session.finished_at is None
            ):
                matches.append((session, path))

        if not matches:
            return None
        return max(
            matches,
            key=lambda item: (
                item[0].started_at,
                item[1].stat().st_mtime_ns,
            ),
        )
