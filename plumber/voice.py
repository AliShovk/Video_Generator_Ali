#!/usr/bin/env python3
"""«Что делает сантехник?» — озвучка по сетке."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/plumber")
ROOT.mkdir(parents=True, exist_ok=True)

INTRO = "Что делает сантехник?"
ITEMS = [
    "Ищет неисправность: осматривает трубы и сантехнику.",
    "Ремонтирует краны: меняет прокладки и картриджи.",
    "Устраняет протечки: находит место и заделывает.",
    "Устанавливает оборудование: раковины, душевые, бойлеры.",
    "Соединяет трубы: фитинги, резьба, герметик.",
    "Проверяет результат: вода не капает, всё сухо.",
]
FLOW = "Осмотрел, нашёл, починил, проверил — так работает мастер."

n = Narrator(voice="eugene", lead=0.0, gap=0.12, delay_ms=150)

clips = []


def say(text, name):
    p = n.say(text, ROOT / f"{name}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    return p, d


p_intro, d_intro = say(INTRO, "intro")
clips.append((p_intro, d_intro, 0.3))

p_flow, d_flow = say(FLOW, "flow")

GRID = [3.0, 6.2, 9.4, 12.6, 15.8, 19.0]
for i, it in enumerate(ITEMS):
    p, d = say(it, f"i{i}")
    clips.append((p, d, GRID[i]))

flow_start = 22.3
clips.append((p_flow, d_flow, flow_start))

total = 25.4
json.dump(dict(total=total, grid=GRID, flow=flow_start), open(ROOT / "timings.json", "w"), indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(total * SR), dtype=np.float32)
for path, d, st in clips:
    with wave.open(str(path)) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(st * SR)
    e = min(len(mix), s + len(a))
    if e > s:
        mix[s:e] += a[: e - s]
mix = mix / (float(np.max(np.abs(mix))) or 1.0) * 0.9
with wave.open(str(ROOT / "voice.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("total", total, "grid", GRID, "flow", flow_start, "flow_dur", round(d_flow, 2))
