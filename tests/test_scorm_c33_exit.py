import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY = ROOT / "scorm" / "c3-3" / "activity.js"


class C33ExitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ACTIVITY.read_text(encoding="utf-8")

    def test_finish_saves_commits_and_finishes_in_that_order(self):
        handler = self.source.split('document.querySelector("#finish").onclick=()=>{', 1)[1]
        handler = handler.split("setTimeout", 1)[0]
        self.assertLess(handler.index("save();"), handler.index("runtime.commit();"))
        self.assertLess(handler.index("runtime.commit();"), handler.index("runtime.finish();"))

    def test_exit_uses_moodle_navigation_not_window_close(self):
        self.assertIn("window.top.location.assign(target)", self.source)
        self.assertIn("window.top.history.back()", self.source)
        self.assertNotIn("window.close()", self.source)

    def test_exit_can_return_to_activity_or_course(self):
        self.assertIn('/mod/scorm/view.php', self.source)
        self.assertIn('/course/view.php', self.source)
        self.assertIn('/mod/scorm/player.php', self.source)

    def test_button_prevents_duplicate_finish(self):
        self.assertIn('button.disabled=true', self.source)
        self.assertIn('Guardando y saliendo…', self.source)


if __name__ == "__main__":
    unittest.main()
