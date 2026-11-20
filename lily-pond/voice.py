#!/usr/bin/env python3
"""Озвучка «Кувшинка»: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/lily-pond")
OUT = ROOT / "out"

BLOCKS = [
    (0.50, ["За день до результата это выглядит как провал."]),
    (3.40, ["Лилия удваивается каждый день."]),
    (6.20, ["Двадцатый день — почти ничего."]),
    (10.20, ["Двадцать пятый — три процента пруда."]),
    (13.20, ["Двадцать седьмой — двенадцать. Двадцать восьмой — четверть."]),
    (18.20, ["Двадцать девятый — половина пруда."]),
    (22.20, ["А на тридцатый — весь пруд."]),
    (26.20, ["Если кажется, что ты стоишь на месте — возможно, ты на двадцать девятом дне."]),
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
