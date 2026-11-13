#!/usr/bin/env python3
"""«Тайга» — ремейк референса, озвучка."""
import json
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

ROOT = Path("/root/video-gen/taiga")
ROOT.mkdir(parents=True, exist_ok=True)

LINES = [
    "Если поезд встал посреди тайги, а на улице минус сорок — не выходите из вагона.",
    "Вы сидите в самом тёплом месте на сто километров вокруг.",
    "Но только если не совершите одну фатальную ошибку.",
    "Контактная сеть обесточена. Электровоз — мёртвый кусок железа.",
    "Первый порыв Дениса — дойти по шпалам до станции. Не надо.",
    "До станции сорок километров. Это десять часов по шпалам.",
    "А переохлаждение наступит через два.",
    "А в вагоне есть то, о чём забыли все пассажиры.",
    "Первое — котёл. В нерабочем тамбуре стоит угольный котёл.",
    "Ему не нужно электричество. Угля в ящике под вагоном — на трое суток.",
    "Второе — вода. Без отопления трубы замёрзнут через три часа и лопнут.",
    "Денис набирает кипяток во все бутылки и сливает систему, пока не поздно.",
    "Третье — люди. Каждый человек греет воздух, как стоваттная лампа.",
    "Всех пассажиров собирают в один вагон, а тамбур заклеивают одеялами.",
    "Проводница сверяет список. По билетам — сто девяносто два человека.",
    "В вагоне — сто девяносто один.",
    "Кто-то сошёл в Чите, — машет она рукой.",
    "Тепла и кипятка хватит на трое суток.",
    "Но была одна проблема.",
    "Ночью Денис выходит в тамбур подбросить угля.",
    "И видит дым над хвостом поезда.",
    "Все сто девяносто один здесь, в этом вагоне.",
    "Но в последнем вагоне кто-то топит котёл.",
    "Денис гасит фонарь и прижимается к стеклу.",
    "В окне пятнадцатого вагона стоит человек. И смотрит прямо на него.",
    "Секунда — и силуэт исчезает под окном.",
    "Он не испугался. Он прячется.",
    "Сто девяносто два не сошёл в Чите. И он знает о нас.",
    "Продолжение следует.",
]

n = Narrator(voice="eugene", lead=0.0, gap=0.2, delay_ms=200)
starts, durs, t = [], [], 0.4
for i, text in enumerate(LINES):
    p = n.say(text, ROOT / f"p{i}.wav")
    with wave.open(str(p)) as f:
        d = f.getnframes() / f.getframerate()
    starts.append(round(t, 3))
    durs.append(round(d, 3))
    t += d + 0.85

total = round(t + 0.6, 2)
json.dump(dict(total=total, starts=starts, durs=durs), open(ROOT / "timings.json", "w"), indent=2)

import numpy as np
SR = 48000
mix = np.zeros(int(total * SR), dtype=np.float32)
for i in range(len(LINES)):
    with wave.open(str(ROOT / f"p{i}.wav")) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    s = int(starts[i] * SR)
    e = min(len(mix), s + len(a))
    mix[s:e] += a[: e - s]
mix = mix / (float(np.max(np.abs(mix))) or 1.0) * 0.9
with wave.open(str(ROOT / "voice.wav"), "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(SR)
    f.writeframes((mix * 32767).astype(np.int16).tobytes())

print("total", total, starts)
