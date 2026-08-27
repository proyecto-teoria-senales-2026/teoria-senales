from io import BytesIO
import unittest
import wave

import numpy as np

from teoria_senales.signal_processing.voice import (
    VOICE_SAMPLE_RATE,
    VoiceProcessingError,
    analyze_voice,
)


def make_wav(samples: np.ndarray, sample_rate: int = VOICE_SAMPLE_RATE) -> bytes:
    pcm = np.round(np.clip(samples, -1, 1) * 32767).astype("<i2")
    buffer = BytesIO()
    with wave.open(buffer, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(pcm.tobytes())
    return buffer.getvalue()


class VoiceProcessingTests(unittest.TestCase):
    def test_voice_is_convolved_with_c3_3_impulse_response(self):
        samples = np.asarray([0.0, 0.5, -0.25, 0.25], dtype=np.float64)
        analysis = analyze_voice(make_wav(samples))
        self.assertEqual(analysis.sample_rate, VOICE_SAMPLE_RATE)
        self.assertEqual(analysis.sample_count, 4)
        self.assertEqual(analysis.convolved.size, 6)
        np.testing.assert_allclose(
            analysis.convolved,
            np.convolve(analysis.original, [1.0, -1.0, 2.0]),
        )
        self.assertTrue(analysis.original_wav.startswith(b"RIFF"))
        self.assertTrue(analysis.convolved_wav.startswith(b"RIFF"))

    def test_voice_is_limited_to_five_seconds(self):
        samples = np.zeros(VOICE_SAMPLE_RATE * 6, dtype=np.float64)
        analysis = analyze_voice(make_wav(samples))
        self.assertTrue(analysis.truncated)
        self.assertEqual(analysis.sample_count, VOICE_SAMPLE_RATE * 5)
        self.assertEqual(analysis.duration_seconds, 5.0)

    def test_empty_or_invalid_audio_is_rejected(self):
        with self.assertRaises(VoiceProcessingError):
            analyze_voice(b"not-a-wav")


if __name__ == "__main__":
    unittest.main()
