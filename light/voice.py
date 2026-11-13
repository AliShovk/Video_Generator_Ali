#!/usr/bin/env python3
"""«Разводка освещения» — озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/light")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Свет мигает, выключатель щёлкает, а в щитке стоит не тот автомат. Разбираем разводку освещения по правилам.",
    "Схема простая: щиток, автомат, кабель, выключатель, светильник. И обратно — ноль и земля.",
    "Главное правило: выключатель разрывает фазу, а не ноль. Иначе светильник выключен, а провод под напряжением.",
    "Освещение — отдельная группа. Кабель полтора миллиметра, автомат десять ампер, до двух киловатт.",
    "Люстра на два режима — два провода от выключателя и две группы ламп.",
    "Длинный коридор — проходные выключатели: включил у входа, выключил у другой двери.",
    "Соединения только клеммами в коробке. Скрутки и медь с алюминием — это нагрев и пожар.",
    "В ванной и на улице — влагозащищённые светильники и УЗО на тридцать миллиампер.",
    "Проверь: фаза на выключателе, автомат десять ампер, клеммы, УЗО, отдельная группа.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=250)
starts, durs, t = [], [], 0.25
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.28

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
