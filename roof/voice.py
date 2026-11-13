#!/usr/bin/env python3
"""Озвучка «Утепление кровли» по фразам из spec.py."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/roof")
ROOT.mkdir(parents=True, exist_ok=True)

from spec import PHRASES

n = Narrator(voice="eugene", lead=0.0, gap=0.22, delay_ms=250)
starts, durs, t = [], [], 0.25
for i, ph in enumerate(PHRASES):
    p = n.say(ph["text"], ROOT / f'{ph["id"]}.wav')
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.30

total = round(t + 0.6, 2)
json.dump(dict(total=total, items=[dict(id=ph["id"], scene=ph["scene"], start=starts[i], dur=durs[i])
                                   for i, ph in enumerate(PHRASES)]),
          open(ROOT / "timings.json", "w"), ensure_ascii=False, indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(total * SR), dtype=np.float32)
for i in range(len(PHRASES)):
    with wave.open(str(ROOT / f'{PHRASES[i]["id"]}.wav')) as f:
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
for i, ph in enumerate(PHRASES):
    print(ph["id"], starts[i], durs[i])
