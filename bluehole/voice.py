#!/usr/bin/env python3
"""«Бушменская дыра» — озвучка, 60 секунд."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/bluehole")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Он нырнул, чтобы достать тело. И остался рядом с ним навсегда.",
    "Южная Африка. Озеро в скале уходит вниз на двести восемьдесят три метра.",
    "Это глубже, чем стоэтажный дом.",
    "В тысяча девятьсот девяносто четвёртом здесь погиб Деон Дрейер. Ему было двадцать.",
    "Он всплывал с пятидесяти метров и не добрался до поверхности.",
    "Тело осталось в пещере, на глубине двухсот семидесяти метров.",
    "Десять лет никто не мог его достать.",
    "Глубина не прощает ошибок: там нет света и нет второго шанса.",
    "В две тысячи пятом австралийский пилот Дэйв Шоу решил попробовать.",
    "Год подготовки: ребризер, газовые смеси, команда поддержки.",
    "Спуск занимает двадцать пять минут. Подъём — много часов.",
    "Он нашёл тело и начал поднимать его к свету.",
    "На глубине его запутал страховочный трос.",
    "Луч фонаря ещё двигался, потом замер.",
    "Камера на шлеме записала последние минуты.",
    "Двенадцатого января подняли обоих.",
    "Фильм об этом называется «Дэйв не вернётся».",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=200)
starts, durs, t = [], [], 0.2
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.6

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
