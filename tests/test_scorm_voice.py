from pathlib import Path
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scorm" / "c3-3"
PACKAGE = ROOT / "scorm" / "dist" / "C3-3_SCORM_1.2.zip"
REQUIRED = {
    "imsmanifest.xml",
    "index.html",
    "styles.css",
    "activity.js",
    "scorm12-runtime.js",
}


class ScormVoicePilotTests(unittest.TestCase):
    def test_c3_3_scorm_contains_microphone_lab(self):
        activity = (SOURCE / "activity.js").read_text(encoding="utf-8")
        for expected in (
            "navigator.mediaDevices",
            "getUserMedia",
            "MediaRecorder",
            "VOICE_SAMPLE_RATE=16000",
            "VOICE_MAX_SECONDS=5",
            "VOICE_FILTER=[1,-1,2]",
            "rawAudioStored:false",
            "Laboratorio piloto de voz",
            "Decisión que debe discutirse con los tutores",
        ):
            self.assertIn(expected, activity)

    def test_voice_lab_does_not_change_the_grade(self):
        activity = (SOURCE / "activity.js").read_text(encoding="utf-8")
        self.assertIn("const PASSING_SCORE=3", activity)
        self.assertIn("weighting:0", activity)
        self.assertIn("El laboratorio de voz no agrega ni resta puntos", activity)
        self.assertNotIn("state.points+=1", activity)

    def test_voice_audio_is_not_stored_in_package_or_suspend_data(self):
        activity = (SOURCE / "activity.js").read_text(encoding="utf-8")
        self.assertNotIn("state.voice.audio", activity)
        self.assertNotIn("base64Audio", activity)
        with ZipFile(PACKAGE) as package:
            self.assertFalse(
                any(name.lower().endswith((".wav", ".mp3", ".ogg", ".webm")) for name in package.namelist())
            )

    def test_regenerated_zip_matches_c3_3_source(self):
        with ZipFile(PACKAGE) as package:
            self.assertIsNone(package.testzip())
            self.assertEqual(set(package.namelist()), REQUIRED)
            for name in REQUIRED:
                self.assertEqual(package.read(name), (SOURCE / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
