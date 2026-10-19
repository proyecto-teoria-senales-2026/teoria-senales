from pathlib import Path
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scorm" / "c2-1"
PACKAGE = ROOT / "scorm" / "dist" / "C-2-1_SCORM_1.2_V2_QA.zip"


class C21V2StandardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.activity = (SOURCE / "activity.js").read_text(encoding="utf-8")
        cls.manifest = (SOURCE / "imsmanifest.xml").read_text(encoding="utf-8")
        cls.index = (SOURCE / "index.html").read_text(encoding="utf-8")

    def test_four_guided_steps_and_twenty_point_rubric(self):
        self.assertIn("guidedPoints: [0, 0, 0, 0]", self.activity)
        self.assertIn("state.attempts[index] === 1 ? 3 : 2", self.activity)
        self.assertIn("const weighting = type === \"tf\" ? 1 : 2", self.activity)
        self.assertIn("(state.points / 20) * 100", self.activity)

    def test_score_scale_is_zero_to_one_hundred(self):
        self.assertIn("const PASSING_SCORE = 60", self.activity)
        self.assertIn("score: state.score", self.activity)
        self.assertIn("/ 100", self.activity)
        self.assertNotIn("nota se calcula sobre 5,0", self.activity)

    def test_guide_is_available_before_and_during_activity(self):
        self.assertGreaterEqual(self.activity.count("guia_estudiante_C-2-1.pdf"), 2)
        self.assertIn('<file href="guia_estudiante_C-2-1.pdf"/>', self.manifest)

    def test_fields_start_empty_and_decimal_notice_is_visible(self):
        self.assertIn('value="${saved[key] ?? ""}"', self.activity)
        self.assertIn("utiliza punto (.) como separador decimal. Ejemplo: 1.5", self.activity)

    def test_version_is_internal_only(self):
        self.assertIn('identifier="TS_C2_1_V2_SCORM_12"', self.manifest)
        self.assertIn('version="2.0"', self.manifest)
        self.assertNotIn("C-2-1 V2", self.index)
        self.assertNotIn("C-2-1 V2", self.manifest)

    def test_finish_uses_approved_moodle_exit_flow(self):
        save_at = self.activity.index("save();", self.activity.index('button.textContent = "Guardando y saliendo…"'))
        commit_at = self.activity.index("runtime.commit();", save_at)
        finish_at = self.activity.index("runtime.finish();", commit_at)
        self.assertLess(save_at, commit_at)
        self.assertLess(commit_at, finish_at)
        self.assertIn("leaveScormPlayer()", self.activity)

    def test_question_bank_is_randomized_by_type(self):
        self.assertEqual(self.activity.count('["C2-1-P'), 15)
        self.assertIn('filter((question) => question[1] === "mc")', self.activity)
        self.assertIn('filter((question) => question[1] === "tf")', self.activity)

    def test_distribution_zip_contains_required_files(self):
        self.assertTrue(PACKAGE.exists())
        with zipfile.ZipFile(PACKAGE) as archive:
            names = set(archive.namelist())
        self.assertEqual(names, {"imsmanifest.xml", "index.html", "styles.css", "activity.js", "scorm12-runtime.js", "guia_estudiante_C-2-1.pdf"})


if __name__ == "__main__":
    unittest.main()
