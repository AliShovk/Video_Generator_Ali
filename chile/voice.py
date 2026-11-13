#!/usr/bin/env python3
"""Озвучка «33» (Чили, 2010): 8 фраз + тайминги."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/chile")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Тридцать три человека. Семьсот метров под землёй. Шестьдесят девять дней. Никто не знал, живы ли они. Связи с поверхностью не было.",
    "Пятого августа две тысячи десятого года в шахте Сан-Хосе обрушился верхний уровень. Выход завалило камнем. Тридцать три шахтёра успели уйти вглубь.",
    "Тридцать три человека в убежище размером с комнату. Еды на три дня. Связи нет. Воду делили по глотку.",
    "Семнадцать дней бурили в пустоту. Ни одного сигнала снизу. Семьи жили у ворот в палатках.",
    "Двадцать второго августа бур пробил выработку. Внутри нашли записку: мы живы, все тридцать три.",
    "Тринадцатого октября подняли первого. Флоренсио Авалос провёл под землёй шестьдесят девять дней. Наверху загорелся сигнальный фонарь.",
    "Последним поднялся старший смены Луис Урсуа. Все тридцать три вернулись домой.",
    "Шестьдесят девять дней. Тридцать три человека. Ни одного потерянного.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.12, delay_ms=250)
starts, durs, t = [], [], 0.25
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.25

total = round(t + 0.6, 2)
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
