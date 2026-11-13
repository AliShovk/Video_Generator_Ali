#!/usr/bin/env python3
"""«5 ошибок, из-за которых плитка отваливается» — озвучка и тайминги."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/tile-errors")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Плитка отпала не потому, что клей плохой. Вот пять причин, по которым она держится до первого хлопка.",
    "Первая: нет грунтовки. Клей ушёл в стену и не схватился с плиткой.",
    "Вторая: нет зазора. Плитка упирается в соседнюю и отрывается при нагреве.",
    "Третья: клей нанесли плюхами. Под плиткой пустота, и она лопается от удара.",
    "Четвёртая: гребёнка не по размеру плитки. На большой плите шесть миллиметров клея мало.",
    "Пятая: нет гидроизоляции в мокрой зоне. Вода идёт под клей и рвёт его изнутри.",
    "Проверь все пять — и плитка простоит дольше ремонта.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.18, delay_ms=250)
starts, durs, t = [], [], 0.25
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.25

total = round(t + 0.5, 2)
json.dump(dict(total=total, starts=starts, durs=durs), open(ROOT / "timings.json", "w"), indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(total * SR), dtype=np.float32)
for i in range(len(LINES)):
    with wave.open(str(ROOT / f"p{i}.wav")) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(starts[i] * SR)
    mix[s:s + len(a)] += a
peak = float(np.max(np.abs(mix))) or 1.0
mix = mix / peak * 0.9
with wave.open(str(ROOT / "voice.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("total", total)
for i in range(len(LINES)):
    print(i, starts[i], durs[i])
