#!/usr/bin/env python3
"""«12 применений WD-40» — пофразная озвучка для точной синхронизации."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/wd40")
ROOT.mkdir(parents=True, exist_ok=True)

INTRO = "Двенадцать применений WD-40."
ITEMS = [
    "Унитаз.", "Обувь.", "Молния.", "Хром.", "Ножницы.", "Жвачка.",
    "Наклейки.", "Карандаш.", "Кольцо.", "Замок.", "Смола.", "Петли.",
]
OUTRO = "Незаменимый помощник в каждом доме."

n = Narrator(voice="eugene", lead=0.0, gap=0.12, delay_ms=150)

clips = []


def say(text, name):
    p = n.say(text, ROOT / f"{name}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    return p, d


p_intro, d_intro = say(INTRO, "intro")
clips.append((p_intro, d_intro, 0.4))
icon_times = []
GRID_START, STEP = 3.0, 1.55
for i, it in enumerate(ITEMS):
    p, d = say(it, f"i{i}")
    st = GRID_START + i * STEP
    clips.append((p, d, st))
    icon_times.append(round(st, 3))

p_out, d_out = say(OUTRO, "outro")
outro_start = GRID_START + 12 * STEP + 0.5
clips.append((p_out, d_out, outro_start))

total = round(outro_start + d_out + 0.8, 2)
json.dump(dict(total=total, icon_times=icon_times, outro=round(outro_start, 3),
               intro=0.4, items=ITEMS), open(ROOT / "timings.json", "w"), indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(total * SR), dtype=np.float32)
for path, d, st in clips:
    with wave.open(str(path)) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(st * SR)
    e = min(len(mix), s + len(a))
    mix[s:e] += a[: e - s]
mix = mix / (float(np.max(np.abs(mix))) or 1.0) * 0.9
with wave.open(str(ROOT / "voice.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("total", total)
print("icons", icon_times)
print("outro", round(outro_start, 3))
