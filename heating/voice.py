#!/usr/bin/env python3
"""«Почему радиатор холодный» — озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/heating")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Котёл работает, труба горячая, а батарея холодная. Разбираем пять причин по порядку.",
    "Сначала посмотрим, как система устроена. Котёл греет воду, насос толкает её по трубе, радиатор отдаёт тепло, обратка возвращает воду назад.",
    "Первая причина: воздух. Он собирается вверху радиатора и не даёт воде пройти. Открой кран Маевского и спусти воздух, пока не пойдёт вода.",
    "Вторая: насос стоит на минимальной скорости. Вода не доходит до дальних радиаторов. Переключи насос на вторую или третью скорость.",
    "Третья: разбалансировка. Ближний радиатор забирает весь поток, дальнему не остаётся. Прикрой ближние краны и открой дальний.",
    "Четвёртая: грязь и ил. Они оседают в батарее и в фильтре, проход сужается. Промой радиатор и почисти фильтр перед насосом.",
    "Пятая: низкое давление. Манометр показывает меньше нормы, вода не поднимается на верхние этажи. Проверь подпитку и утечки.",
    "Проверь по порядку: воздух, насос, балансировка, грязь, давление. В девяти случаях этого хватает.",
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
