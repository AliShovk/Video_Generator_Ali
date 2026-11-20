#!/usr/bin/env python3
"""Озвучка ролика «Закон Ома»: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/ohm-law")
OUT = ROOT / "out"

BLOCKS = [
    (0.70, ["Закон Ома связывает напряжение, ток и сопротивление."]),
    (4.50, ["Вольт толкает заряды через проводник."]),
    (7.60, ["Ампер — это ток: сколько заряда проходит за секунду."]),
    (11.40, ["Ом мешает: это сопротивление проводника."]),
    (14.40, ["Ток равен напряжению, делённому на сопротивление."]),
    (18.00, ["Двенадцать вольт на четыре ома — три ампера."]),
    (21.40, ["Больше сопротивление — меньше ток. При том же напряжении."]),
    (25.00, ["Запомни: ток равен напряжению, делённому на сопротивление."]),
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
