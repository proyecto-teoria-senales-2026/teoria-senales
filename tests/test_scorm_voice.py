from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ACTIVITY = ROOT / "scorm" / "c3-3" / "activity.js"


class ScormVoiceLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ACTIVITY.read_text(encoding="utf-8")

    def test_microphone_and_contingency_are_available(self):
        self.assertIn("getUserMedia", self.source)
        self.assertIn("MediaRecorder", self.source)
        self.assertIn('type=\\"file\\"', self.source)
        self.assertIn('accept=\\"audio/*\\"', self.source)

    def test_voice_step_is_mandatory_but_ungraded(self):
        self.assertIn("Paso obligatorio · sin puntaje", self.source)
        self.assertIn('id=\\"continue-evaluation\\" disabled', self.source)
        self.assertIn("if(!state.voice?.completed)", self.source)
        self.assertIn("weighting:0", self.source)
        self.assertIn("He leído y comprendido", self.source)
        self.assertNotIn("autorizo su procesamiento temporal", self.source)
        self.assertNotIn("Este laboratorio es opcional", self.source)
        self.assertNotIn("continúa sin grabar", self.source)

    def test_audio_is_not_persisted(self):
        self.assertIn("rawAudioStored:false", self.source)
        self.assertIn("el audio no fue almacenado", self.source)
        self.assertNotIn("reader.readAsDataURL", self.source)

    def test_voice_processing_contract(self):
        self.assertIn("VOICE_SAMPLE_RATE=16000", self.source)
        self.assertIn("VOICE_MAX_SECONDS=5", self.source)
        self.assertIn("function impulseResponse()", self.source)
        self.assertIn("convolveVoice", self.source)
        self.assertIn("wavBlob", self.source)

    def test_three_views_and_exploration_controls_exist(self):
        self.assertIn('id=\\"voice-waveform-original\\"', self.source)
        self.assertIn('id=\\"voice-waveform-processed\\"', self.source)
        self.assertIn('id=\\"voice-waveform-combined\\"', self.source)
        self.assertIn('id=\\"voice-gain\\"', self.source)
        self.assertIn('id=\\"voice-delay\\"', self.source)
        self.assertIn('id=\\"voice-decay\\"', self.source)
        self.assertIn('id=\\"voice-time\\"', self.source)


if __name__ == "__main__":
    unittest.main()
