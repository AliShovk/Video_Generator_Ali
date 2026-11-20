#!/usr/bin/env python3
"""Озвучка «Стройка»: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/wall")
OUT = ROOT / "out"

BLOCKS = [
    (0.40, ["Ты не видишь результата. А он уже есть."]),
    (3.30, ["Стена не появляется сразу."]),
    (6.60, ["Сначала фундамент. Потом кирпич за кирпичом."]),
    (10.40, ["Кто-то носит, кто-то кладёт, кто-то поднимает."]),
    (14.40, ["Никто не видит целого — каждый видит свой кирпич."]),
    (18.60, ["Но стена растёт. Каждый день."]),
    (22.40, ["И однажды она закрывает горизонт."]),
    (26.50, ["Ты не строишь стену. Ты строишь то, что за ней."]),
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
