#!/usr/bin/env python3
"""Озвучка анекдота: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/joke-memory")
OUT = ROOT / "out"

BLOCKS = [
    (0.60, ["Анекдот, который всегда заходит."]),
    (3.60, ["Пациент у врача."]),
    (6.10, ["Доктор, у меня провалы в памяти."]),
    (10.40, ["И давно?"]),
    (13.20, ["Что давно?"]),
    (17.20, ["Подписывайся, будет ещё."]),
]

n = Narrator(voice="eugene", lead=0.05, gap=0.10, delay_ms=600)
track = n.track(BLOCKS, total=21.0, out=OUT / "voice.wav")

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
