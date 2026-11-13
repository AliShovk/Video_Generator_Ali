#!/usr/bin/env python3
"""«Уклон канализации» — озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/sewer")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Вода стоит в унитазе, а из трапа пахнет. Чаще всего виноват уклон трубы.",
    "Уклон — это перепад высоты на метр трубы. Для канализации он считается в сантиметрах на метр, а не «на глаз».",
    "Запомни три цифры. Труба пятьдесят миллиметров — три с половиной сантиметра на метр. Сто десять — два сантиметра. Сто шестьдесят — восемь миллиметров.",
    "Если уклон меньше нормы, вода течёт медленно, ил оседает на дне и труба зарастает. Это главная причина засоров.",
    "Если уклон больше нормы — вода убегает, а твёрдое остаётся. И ещё шум, срыв сифонов и запах.",
    "Повороты делай плавно: два отвода по сорок пять градусов вместо одного девяноста. На длинных участках ставь ревизию.",
    "И не забудь вентиляцию стояка. Без неё вода уходит с бульканьем, а запах тянет в квартиру.",
    "Проверь уклон уровнем, собери на 45-х отводах, поставь ревизию и вентиляцию — и канализация будет тихой.",
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
