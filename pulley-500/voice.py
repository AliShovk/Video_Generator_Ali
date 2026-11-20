#!/usr/bin/env python3
"""Озвучка ролика pulley-500: Silero через локальный TTS-мост -> out/voice.wav."""
import sys, wave, json
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/pulley-500")
OUT = ROOT / "out"

BLOCKS = [
    (1.30, ["Пятьсот килограммов. Какая сила нужна?"]),
    (4.15, ["Вес делят два нижних блока: по двести пятьдесят."]),
    (8.15, ["Каждый подвижный блок делит силу ещё вдвое: сто двадцать пять."]),
    (12.15, ["И ещё раз: шестьдесят две с половиной."]),
    (16.15, ["Тянем верёвку вниз — блок идёт вверх."]),
    (22.15, ["Ответ: шестьдесят две целых пять десятых килограмма на верёвку."]),
    (26.30, ["Это шестьсот тринадцать ньютонов. Но верёвку вытянуть в восемь раз больше."]),
]

n = Narrator(voice="eugene", lead=0.05, gap=0.10, delay_ms=600)
track = n.track(BLOCKS, total=34.0, out=OUT / "voice.wav")

# длительности фраз — проверить, что ничего не наезжает
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
