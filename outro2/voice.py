#!/usr/bin/env python3
"""Новая концовка: ссылка в шапке + «ГАЙД» в комментариях."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/outro2")
ROOT.mkdir(parents=True, exist_ok=True)

LINE = "Ссылка в шапке профиля. Или напишите гайд в комментариях."

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=200)
p = n.say(LINE, ROOT / "voice_raw.wav")
with wave.open(str(p)) as f:
    d = f.getnframes() / f.getframerate()

total = round(d + 0.9, 2)
json.dump(dict(total=total, dur=d), open(ROOT / "timings.json", "w"), indent=2)
print("voice", d, "total", total)
