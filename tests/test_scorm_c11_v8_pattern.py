import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY = ROOT / "scorm" / "c1-1" / "activity.js"


class C11V8PatternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ACTIVITY.read_text(encoding="utf-8")

    def test_uses_zero_to_one_hundred_and_twenty_point_rubric(self):
        self.assertIn("const PASSING_SCORE = 60", self.source)
        self.assertIn("guidedPoints: [0, 0, 0, 0]", self.source)
        self.assertIn("pasos guiados: hasta 12 puntos", self.source)
        self.assertIn("selección múltiple: 6 puntos", self.source)
        self.assertIn("verdadero/falso: 2 puntos", self.source)
        self.assertIn("(state.points / 20) * 100", self.source)

    def test_guided_attempts_are_scored_and_reported(self):
        self.assertIn("state.attempts[index] += 1", self.source)
        self.assertIn("state.attempts[index] === 1 ? 3 : 2", self.source)
        self.assertIn("runtime.recordInteraction", self.source)
        self.assertIn("runtime.recordObjective", self.source)

    def test_initial_controls_do_not_expose_answers(self):
        self.assertIn('placeholder="${key === "samples" ? "Escribe los valores separados por comas" : "Escribe un valor"}"', self.source)
        evaluation = self.source.split("function renderEvaluation()", 1)[1].split("function gradeEvaluation", 1)[0]
        self.assertNotIn(" checked", evaluation)

    def test_finish_saves_commits_finishes_and_leaves_moodle_player(self):
        handler = self.source.split('document.querySelector("#finish").addEventListener("click", () => {', 1)[1]
        handler = handler.split("setTimeout", 1)[0]
        self.assertLess(handler.index("save();"), handler.index("runtime.commit();"))
        self.assertLess(handler.index("runtime.commit();"), handler.index("runtime.finish();"))
        self.assertIn("window.top.location.assign(target)", self.source)
        self.assertIn("window.top.history.back()", self.source)
        self.assertNotIn("window.close()", self.source)

    def test_voice_is_not_added_to_component_one(self):
        self.assertNotIn("getUserMedia", self.source)
        self.assertNotIn("Grabar voz", self.source)


if __name__ == "__main__":
    unittest.main()
