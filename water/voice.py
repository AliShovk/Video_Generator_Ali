#!/usr/bin/env python3
"""«5 ошибок, из-за которых падает напор» — озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/water")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Из крана течёт тонкая струйка, а насос работает. Вот пять причин, куда ушёл напор.",
    "Первая: труба слишком тонкая. Шестнадцать миллиметров на весь дом — это мало.",
    "Вторая: много поворотов. Каждое колено отнимает давление.",
    "Третья: нет гидроаккумулятора. Насос включается на каждый стакан воды.",
    "Четвёртая: забитый фильтр. Картридж не меняли полгода.",
    "Пятая: воздушная пробка. Труба идёт горбом, воздух стоит вверху.",
    "Проверь эти пять точек — и напор вернётся без замены насоса.",
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
