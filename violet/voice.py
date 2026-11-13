#!/usr/bin/env python3
"""«Вайолет Джессоп» — озвучка, 60 секунд."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/violet")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Три корабля. Три катастрофы. И одна женщина на всех трёх.",
    "Её звали Вайолет Джессоп, и она работала стюардессой на лайнерах.",
    "В тысяча девятьсот одиннадцатом году она вышла в море на «Олимпике».",
    "Лайнер столкнулся с крейсером и получил пробоину.",
    "Обошлось без жертв: судно вернулось в порт своим ходом.",
    "Через год Вайолет устроилась на «Титаник».",
    "Это был самый большой корабль в мире.",
    "Ночью лайнер задел айсберг.",
    "Через два часа сорок минут «Титаник» ушёл под воду.",
    "Погибли тысяча четыреста девяносто шесть человек.",
    "Вайолет села в шлюпку номер шестнадцать, с чужим ребёнком на руках.",
    "Она так и не узнала, выжили ли его родители.",
    "В тысяча девятьсот шестнадцатом она оказалась на «Британике».",
    "Судно подорвалось на немецкой мине в Средиземном море.",
    "Тридцать шлюпок спустили за полчаса, вчетверо быстрее, чем на «Титанике».",
    "Вайолет снова оказалась в шлюпке.",
    "Она ходила в море до самой пенсии.",
    "И умерла в глубокой старости, в тысяча девятьсот семьдесят первом году.",
    "Три корабля. Одна жизнь.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=200)
starts, durs, t = [], [], 0.3
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.26

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

print("total", total)
print("starts", starts)
