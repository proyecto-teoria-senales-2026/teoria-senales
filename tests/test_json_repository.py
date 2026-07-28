"""Pruebas del guardado seguro de las sesiones JSON."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from teoria_senales.app.web_session import create_student_session
from teoria_senales.storage.json_repository import JsonSessionRepository


class JsonSessionRepositoryTests(unittest.TestCase):
    def test_interrupted_save_preserves_previous_file(self) -> None:
        tracker = create_student_session("GUARDADO-001")

        with tempfile.TemporaryDirectory() as temporary_directory:
            repository = JsonSessionRepository(temporary_directory)
            destination = repository.save(tracker.session)
            previous_content = destination.read_text(encoding="utf-8")
            tracker.session.student_name = "Cambio pendiente"

            with patch(
                "teoria_senales.storage.json_repository.os.replace",
                side_effect=OSError("interrupción simulada"),
            ):
                with self.assertRaisesRegex(OSError, "interrupción simulada"):
                    repository.save(tracker.session)

            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                previous_content,
            )
            self.assertEqual(
                list(Path(temporary_directory).glob("*.tmp")),
                [],
            )


if __name__ == "__main__":
    unittest.main()
