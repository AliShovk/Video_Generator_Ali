#!/usr/bin/env python3
"""Синтез озвучки по фразам + тайминги для синхронизации анимации."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

from story import PHRASES

ROOT = Path("/root/video-gen/molasses")
OUT = ROOT / "renders"
OUT.mkdir(parents=True, exist_ok=True)
VOICE_DIR = OUT / "phrases"
VOICE_DIR.mkdir(exist_ok=True)

GAP = 0.10
LEAD = 0.20

n = Narrator(voice="eugene", lead=0.0, gap=GAP, delay_ms=250)

t = LEAD
timings = []
for ph in PHRASES:
    p = n.say(ph["text"], VOICE_DIR / f'{ph["id"]}.wav')
    with wave.open(str(p)) as f:
        dur = f.getnframes() / f.getframerate()
    timings.append(dict(id=ph["id"], scene=ph["scene"], start=round(t, 3), dur=round(dur, 3)))
    t += dur + GAP

total = round(t + 0.4, 3)
json.dump(dict(total=total, phrases=timings), open(ROOT / "timings.json", "w"), ensure_ascii=False, indent=2)

# сборка дорожки
from narrator import SR
import numpy as np

mix = np.zeros(int(total * SR), dtype=np.float32)
for item in timings:
    with wave.open(str(VOICE_DIR / f'{item["id"]}.wav')) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(item["start"] * SR)
    mix[s:s + len(a)] += a

peak = float(np.max(np.abs(mix))) or 1.0
mix = mix / peak * 0.9
with wave.open(str(OUT / "voice_timed.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("total", total, "фраз", len(timings))
for it in timings:
    print(f'{it["id"]} {it["scene"]} {it["start"]:6.2f} +{it["dur"]:.2f}')
