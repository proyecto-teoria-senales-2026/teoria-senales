"""Procesamiento temporal de voz para el piloto del ejercicio C-3-3."""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import wave

import numpy as np
from numpy.typing import NDArray


VOICE_SAMPLE_RATE = 16_000
VOICE_MAX_DURATION_SECONDS = 5.0
VOICE_IMPULSE_RESPONSE = np.asarray([1.0, -1.0, 2.0], dtype=np.float64)


class VoiceProcessingError(ValueError):
    """Indica que una grabación no puede procesarse de forma segura."""


@dataclass(frozen=True)
class VoiceAnalysis:
    sample_rate: int
    duration_seconds: float
    sample_count: int
    truncated: bool
    original: NDArray[np.float64]
    convolved: NDArray[np.float64]
    original_wav: bytes
    convolved_wav: bytes


def _pcm_to_float(raw: bytes, sample_width: int) -> NDArray[np.float64]:
    if sample_width == 1:
        return (np.frombuffer(raw, dtype=np.uint8).astype(np.float64) - 128.0) / 128.0
    if sample_width == 2:
        return np.frombuffer(raw, dtype="<i2").astype(np.float64) / 32768.0
    if sample_width == 4:
        return np.frombuffer(raw, dtype="<i4").astype(np.float64) / 2147483648.0
    raise VoiceProcessingError(
        "La grabación usa un formato de audio no compatible. Intenta grabarla nuevamente."
    )


def _encode_wav(samples: NDArray[np.float64], sample_rate: int) -> bytes:
    values = np.asarray(samples, dtype=np.float64)
    peak = float(np.max(np.abs(values))) if values.size else 0.0
    if peak > 0.98:
        values = values * (0.98 / peak)
    pcm = np.round(np.clip(values, -1.0, 1.0) * 32767.0).astype("<i2")

    buffer = BytesIO()
    with wave.open(buffer, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(pcm.tobytes())
    return buffer.getvalue()


def analyze_voice(
    wav_data: bytes,
    *,
    max_duration_seconds: float = VOICE_MAX_DURATION_SECONDS,
) -> VoiceAnalysis:
    """Decodifica, limita y convoluciona una grabación WAV sin guardarla."""

    try:
        with wave.open(BytesIO(wav_data), "rb") as source:
            channels = source.getnchannels()
            sample_width = source.getsampwidth()
            sample_rate = source.getframerate()
            frame_count = source.getnframes()
            raw = source.readframes(frame_count)
    except (EOFError, wave.Error) as error:
        raise VoiceProcessingError(
            "No fue posible leer la grabación. Intenta grabarla nuevamente."
        ) from error

    if sample_rate <= 0 or channels <= 0:
        raise VoiceProcessingError("La grabación no contiene parámetros de audio válidos.")

    samples = _pcm_to_float(raw, sample_width)
    if channels > 1:
        usable = samples[: samples.size - (samples.size % channels)]
        samples = usable.reshape(-1, channels).mean(axis=1)

    if samples.size == 0:
        raise VoiceProcessingError("La grabación está vacía.")

    maximum_samples = max(1, int(round(sample_rate * max_duration_seconds)))
    truncated = samples.size > maximum_samples
    samples = np.asarray(samples[:maximum_samples], dtype=np.float64)
    samples = samples - float(np.mean(samples))

    convolved = np.convolve(samples, VOICE_IMPULSE_RESPONSE, mode="full")
    duration = samples.size / sample_rate

    return VoiceAnalysis(
        sample_rate=sample_rate,
        duration_seconds=duration,
        sample_count=int(samples.size),
        truncated=truncated,
        original=samples,
        convolved=convolved,
        original_wav=_encode_wav(samples, sample_rate),
        convolved_wav=_encode_wav(convolved, sample_rate),
    )
