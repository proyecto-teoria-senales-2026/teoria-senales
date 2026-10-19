from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ("c1-1", "c1-2", "c1-3", "c1-4", "c2-1", "c2-2", "c2-3", "c2-4", "c3-3")


class ScormScoreScaleTests(unittest.TestCase):
    def test_all_packages_use_zero_to_one_hundred(self):
        for package in PACKAGES:
            source = (ROOT / "scorm" / package / "activity.js").read_text(encoding="utf-8")
            with self.subTest(package=package):
                self.assertRegex(source, r"PASSING_SCORE\s*=\s*60")
                self.assertIn("/ 100", source)

    def test_all_runtimes_declare_maximum_one_hundred(self):
        for package in PACKAGES:
            source = (ROOT / "scorm" / package / "scorm12-runtime.js").read_text(encoding="utf-8")
            with self.subTest(package=package):
                self.assertIn("maximumScore = 100", source)
                self.assertIn("passingScore = 60", source)


if __name__ == "__main__":
    unittest.main()
