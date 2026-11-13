#!/usr/bin/env python3
"""«Как рисуется дом» — озвучка под этапы скетча (30 с)."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/sketch")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Сначала — общие габариты и линия земли.",
    "Дальше контур: треугольник, стена и скруглённый объём.",
    "Окна, двери и перила — тонкой линией.",
    "Теперь цвет: дерево, стекло, крыша.",
    "Дерево, кусты и тень — и рисунок оживает.",
    "Тридцать секунд — и дом готов.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=200)
FIXED = [0.6, 5.2, 9.8, 14.2, 18.8, 25.4]
starts, durs = [], []
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(FIXED[i])
    durs.append(round(d, 3))

json.dump(dict(total=30.0, starts=starts, durs=durs), open(ROOT / "timings.json", "w"), indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(30.0 * SR), dtype=np.float32)
for i in range(len(LINES)):
    with wave.open(str(ROOT / f"p{i}.wav")) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(starts[i] * SR)
    e = min(len(mix), s + len(a))
    mix[s:e] += a[: e - s]
peak = float(np.max(np.abs(mix))) or 1.0
mix = mix / peak * 0.85
with wave.open(str(ROOT / "voice.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("starts", starts)
