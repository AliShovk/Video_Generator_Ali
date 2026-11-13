import sys
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

n = Narrator(voice="eugene")
blocks = [
    (0.4, ["Эйфелева башня становится выше", "на пятнадцать сантиметров.", "Каждый день."]),
    (11.3, ["Металл нагревается на солнце", "и расширяется.", "Летом вершина гуляет вверх и вниз."]),
    (22.3, ["Днём она выше, ночью ниже.", "Это видно по зазорам в конструкции."]),
    (33.3, ["А ещё металл ржавеет.", "Поэтому башню красят каждые семь лет."]),
]
mix = n.track(blocks, total=42.0, out=Path("renders/voice_eugene.wav"))
final = n.mux("renders/eiffel.mp4", mix, "renders/eiffel-eugene.mp4")
print("ok", final.stat().st_size)
