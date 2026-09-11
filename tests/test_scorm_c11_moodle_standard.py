import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY = ROOT / "scorm" / "c1-1" / "activity.js"


class C11MoodleStandardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ACTIVITY.read_text(encoding="utf-8")

    def test_fields_start_empty_and_use_neutral_placeholders(self):
        self.assertIn('saved[key] ?? ""', self.source)
        self.assertIn('"Escribe un valor"', self.source)
        self.assertIn('"Escribe los valores separados por comas"', self.source)
        self.assertIn('autocomplete="off"', self.source)

    def test_student_guide_is_available_before_and_during_activity(self):
        self.assertIn("Guía del estudiante C‑1‑1", self.source)
        self.assertIn('href="guia_estudiante_C-1-1.pdf"', self.source)
        self.assertIn("utiliza punto (.) como separador decimal", self.source)
        heading = self.source.split("function heading", 1)[1].split("function feedback", 1)[0]
        self.assertIn("Ver guía del estudiante", heading)

    def test_student_guide_is_declared_in_manifest(self):
        manifest = (ROOT / "scorm" / "c1-1" / "imsmanifest.xml").read_text(encoding="utf-8")
        self.assertIn('<file href="guia_estudiante_C-1-1.pdf"/>', manifest)

    def test_manifest_and_visible_title_identify_version_four(self):
        manifest = (ROOT / "scorm" / "c1-1" / "imsmanifest.xml").read_text(encoding="utf-8")
        index = (ROOT / "scorm" / "c1-1" / "index.html").read_text(encoding="utf-8")
        self.assertIn('identifier="TS_C1_1_V4_SCORM_12"', manifest)
        self.assertIn('version="4.0"', manifest)
        self.assertIn("<title>Teoría de Señales — C-1-1</title>", manifest)
        self.assertIn("<title>C-1-1 — Señales fundamentales de tiempo discreto</title>", manifest)
        self.assertIn("Componente 1 · Ejercicio C-1-1</p>", index)
        self.assertNotIn("Ejercicio C-1-1 V4", index)

    def test_student_guide_is_packaged_in_distribution_zip(self):
        package = ROOT / "scorm" / "dist" / "C-1-1_SCORM_1.2_V4_QA_AJUSTADO.zip"
        with zipfile.ZipFile(package) as archive:
            self.assertIn("guia_estudiante_C-1-1.pdf", archive.namelist())
            self.assertGreater(archive.getinfo("guia_estudiante_C-1-1.pdf").file_size, 0)

    def test_guided_attempts_are_recorded_in_moodle(self):
        self.assertIn("state.attempts[index] += 1", self.source)
        self.assertIn("runtime.recordInteraction", self.source)
        self.assertIn("runtime.recordObjective", self.source)
        self.assertIn("C1-1-G0", self.source)

    def test_finish_saves_commits_and_finishes_in_order(self):
        handler = self.source.split('document.querySelector("#finish").addEventListener("click", () => {', 1)[1]
        handler = handler.split("setTimeout", 1)[0]
        self.assertLess(handler.index("save();"), handler.index("runtime.commit();"))
        self.assertLess(handler.index("runtime.commit();"), handler.index("runtime.finish();"))

    def test_finish_returns_to_moodle_without_window_close(self):
        self.assertIn("window.top.location.assign(target)", self.source)
        self.assertIn("window.top.history.back()", self.source)
        self.assertIn("/mod/scorm/view.php", self.source)
        self.assertIn("/course/view.php", self.source)
        self.assertNotIn("window.close()", self.source)

    def test_score_scale_remains_zero_to_one_hundred(self):
        self.assertIn("const PASSING_SCORE = 60", self.source)
        self.assertIn("/ 100", self.source)


if __name__ == "__main__":
    unittest.main()
