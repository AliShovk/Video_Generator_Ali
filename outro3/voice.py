#!/usr/bin/env python3
"""Озвучка концовки: мягкая обрезка старта, чтобы не съедало «Хотите»."""
import json
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator
import numpy as np

ROOT = Path("/root/video-gen/outro3")
SR = 48000
PARTS = [
    "Хотите делать такие ролики?",
    "Ссылка в шапке профиля. Или напишите гайд в комментариях.",
]

n = Narrator(voice="eugene")


def synth(text: str, out: Path) -> None:
    out.write_bytes(n._post(n._prep(text)))
    raw = out
    tmp = out.with_suffix(".trim.wav")
    # мягкая обрезка: порог −60 дБ и старт 30 мс, чтобы не срезать согласную
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
        "-af", ("silenceremove=start_periods=1:start_duration=0.03:start_threshold=-60dB,"
                "areverse,silenceremove=start_periods=1:start_duration=0.03:start_threshold=-60dB,areverse"),
        "-ar", str(SR), "-ac", "1", str(tmp),
    ], check=True)

    with wave.open(str(tmp)) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    rms = float(np.sqrt((a ** 2).mean())) or 1e-6
    gain = (10 ** (-17 / 20)) / rms
    peak = float(np.max(np.abs(a)) * gain) or 1.0
    if peak > 0.89:
        gain *= 0.89 / peak
    a = np.clip(a * gain, -1, 1)
    with wave.open(str(out), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())
    tmp.unlink(missing_ok=True)


files = []
for i, text in enumerate(PARTS):
    p = ROOT / f"seg{i}.wav"
    synth(text, p)
    files.append(str(p))

subprocess.run([
    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
    "-i", files[0], "-i", files[1],
    "-filter_complex", "[0:a]apad=pad_dur=0.3[a0];[a0][1:a]concat=n=2:v=0:a=1[out]",
    "-map", "[out]", "-ar", "48000", "-ac", "1", str(ROOT / "voice_raw.wav"),
], check=True)

with wave.open(str(ROOT / "voice_raw.wav")) as f:
    d = f.getnframes() / f.getframerate()

json.dump(dict(total=round(d + 0.9, 2), dur=d), open(ROOT / "timings.json", "w"), indent=2)
print("voice", round(d, 2), "total", round(d + 0.9, 2))
