#!/usr/bin/env python3
"""«Тёплый пол» — озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/warmfloor")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Пол холодный, а счёт за отопление растёт. Разбираем тёплый пол по слоям и показываем, где его делают неправильно.",
    "Пирог снизу вверх: плита, утеплитель, труба в стяжке, плитка. Уберёшь утеплитель — будешь греть подвал.",
    "Шаг трубы — десять-пятнадцать сантиметров. У окон и дверей десять, в середине комнаты можно пятнадцать.",
    "Каждый контур — отдельная петля от коллектора. Длина петли не больше восьмидесяти-ста метров, иначе дальний конец не прогреется.",
    "Ошибка первая: нет демпферной ленты по стенам. Стяжка упирается в стены и трескается.",
    "Ошибка вторая: шаг тридцать сантиметров. Пол получается полосатый: тепло, холодно, тепло.",
    "Термостат ставим на высоте метра, а датчик — в стяжку, в гофру, чтобы его можно было заменить.",
    "И запуск: первый прогрев по пять градусов в день. Резко нельзя, стяжка треснет.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.16, delay_ms=250)
starts, durs, t = [], [], 0.25
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.22

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
