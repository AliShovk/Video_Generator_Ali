#!/usr/bin/env python3
"""Озвучка ролика «Мощность насоса»: Silero -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/pump-power")
OUT = ROOT / "out"

BLOCKS = [
    (0.60, ["Сколько мощности нужно, чтобы поднять воду?"]),
    (3.20, ["Пять метров — полбара и четверть лошадиной силы."]),
    (7.20, ["Десять метров — один бар и половина силы."]),
    (11.20, ["Двадцать метров — два бара и три четверти силы."]),
    (15.20, ["Сорок метров — четыре бара и полторы силы."]),
    (19.20, ["Восемьдесят метров — восемь баров и три лошадиные силы."]),
    (23.30, ["Каждые десять метров водяного столба — примерно один бар."]),
    (27.30, ["Для дома обычно хватает тридцати–шестидесяти литров в минуту."]),
]

n = Narrator(voice="eugene", lead=0.05, gap=0.10, delay_ms=600)
track = n.track(BLOCKS, total=36.0, out=OUT / "voice.wav")

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
