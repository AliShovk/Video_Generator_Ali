#!/usr/bin/env python3
"""«Виды обогревателей» — озвучка (10 фраз)."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/heaters")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Четыре обогревателя — четыре разных принципа. Разбираем, какой куда.",
    "Конвектор. Тонкая панель на стену: воздух проходит через рёбра и поднимается вверх. Тихо, но греет постепенно.",
    "Масляный радиатор. Секции с маслом: греется долго и остывает долго. Тяжёлый, зато тепло мягкое.",
    "Вентиляторный. Мотор и спираль: горячий воздух дует сразу. Быстро, но шумит и сушит воздух.",
    "Инфракрасный. Греет не воздух, а предметы и людей. Как солнце. Хорош на веранде и в гараже.",
    "Керамическая башня. Керамика внутри, поток мягче, есть поворот. Для спальни и детской.",
    "Сравним по трём параметрам: скорость нагрева, шум и расход.",
    "Мощность считают так: сто ватт на квадратный метр при потолке до трёх метров.",
    "Для ванной — защита от брызг. Для дома — защита от опрокидывания и термостат.",
    "Спальня — конвектор. Ванная — с защитой от брызг. Гараж — инфракрасный. Быстро — вентилятор.",
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
