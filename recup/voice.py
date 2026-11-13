#!/usr/bin/env python3
"""«Рекуператор» — озвучка ~35 с."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/recup")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Зимой мы проветриваем дом и вместе с воздухом выбрасываем тепло на улицу.",
    "Рекуператор возвращает до девяноста процентов этого тепла.",
    "Это приточно-вытяжная установка: два потока воздуха идут через один корпус.",
    "Внутри стоит теплообменник, где потоки идут навстречу друг другу.",
    "Но не смешиваются: тепло передаётся через стенки каналов.",
    "Вытяжка выходит холодной, а приток приходит уже тёплым.",
    "Летом всё наоборот: приток охлаждается, а жара уходит наружу.",
    "Ставят его на стену или в вентиляцию, плюс фильтры и слив конденсата.",
    "Итог: свежий воздух круглый год без потерь тепла.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=200)
starts, durs, t = [], [], 0.3
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.25

total = round(t + 0.4, 2)
json.dump(dict(total=total, starts=starts, durs=durs), open(ROOT / "timings.json", "w"), indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(total * SR), dtype=np.float32)
for i in range(len(LINES)):
    with wave.open(str(ROOT / f"p{i}.wav")) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(starts[i] * SR)
    e = min(len(mix), s + len(a))
    mix[s:e] += a[: e - s]
mix = mix / (float(np.max(np.abs(mix))) or 1.0) * 0.9
with wave.open(str(ROOT / "voice.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("total", total, starts)
