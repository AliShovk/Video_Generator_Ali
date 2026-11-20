#!/usr/bin/env python3
"""Озвучка «Кузница»: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/forge")
OUT = ROOT / "out"

BLOCKS = [
    (0.40, ["Это выглядит как удары. На самом деле — это форма."]),
    (5.00, ["Металл не становится прочным сам."]),
    (8.00, ["Его греют, бьют и остужают."]),
    (11.00, ["Каждый удар убирает лишнее."]),
    (14.00, ["Пятнадцать ударов — и форма готова."]),
    (19.00, ["Резкое охлаждение делает металл твёрдым."]),
    (22.60, ["Клинок не появляется сразу. Он появляется из сотни ударов."]),
    (26.40, ["Тебя не ломают. Тебя куют."]),
]

n = Narrator(voice="eugene", lead=0.05, gap=0.10, delay_ms=600)
track = n.track(BLOCKS, total=33.0, out=OUT / "voice.wav")

info = []
for i, (start, phrases) in enumerate(BLOCKS):
    p = OUT / "narr" / f"{i}_0.wav"
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    info.append({"start": start, "dur": round(d, 2), "end": round(start + d, 2), "text": phrases[0]})
json.dump(info, open(OUT / "voice_lines.json", "w"), ensure_ascii=False, indent=2)
for x in info:
    print(f"{x['start']:>5.2f} → {x['end']:>5.2f}  {x['text']}")
print("voice:", track)
