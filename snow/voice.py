#!/usr/bin/env python3
"""«Снег-утеплитель» — озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/snow")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Ты убираешь снег от фундамента. А надо наоборот.",
    "Снег почти на девяносто процентов состоит из воздуха. Поэтому он держит тепло лучше многих утеплителей.",
    "Смотри: снаружи минус двадцать, а под сугробом у фундамента около нуля.",
    "Убери снег — и грунт промёрзнет глубже. Вода в трубах и отмостка пострадают первыми.",
    "Поэтому снег не разгребают, а наоборот — накидывают на отмостку и вокруг труб.",
    "Но есть правило: не закрывай продухи подпола и вентиляцию. Иначе получишь сырость и плесень.",
    "И не наваливай сугроб выше уровня пола первого этажа — нагрузка на стены ни к чему.",
    "Снег у фундамента — бесплатный утеплитель. Просто не мешай ему работать.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.18, delay_ms=250)
starts, durs, t = [], [], 0.25
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.26

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
