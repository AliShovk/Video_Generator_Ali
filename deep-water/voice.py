#!/usr/bin/env python3
"""Озвучка «Глубинный полив»: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/deep-water")
OUT = ROOT / "out"

BLOCKS = [
    (0.40, ["Дерево поливают не под ствол. А в трубу рядом."]),
    (2.90, ["Копаешь яму шестьдесят сантиметров. Узкую и глубокую."]),
    (7.20, ["Сажаешь саженец. Корневой ком остаётся внизу."]),
    (11.40, ["Рядом ставишь перфорированную трубу. Пятьдесят сантиметров."]),
    (15.60, ["Засыпаешь её гравием. Канал не заплывает землёй."]),
    (19.80, ["Льёшь воду прямо в трубу."]),
    (23.60, ["Влага уходит к корням. Корни тянутся вниз."]),
    (27.20, ["Вода на пятьдесят сантиметров ниже. И дерево переживает засуху."]),
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
