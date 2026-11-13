#!/usr/bin/env python3
"""Правка трёх реплик Piper и пересборка финального микса."""
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-reels")
OUT = ROOT / "voice_piper"
MODEL = "/root/tts-venv/piper/ru_denis.onnx"
SR = 48000
TOTAL = 47.0

FIX = {
    "v4": "Двести двадцать четыре гидравлических домкрата двигали её вперёд.",
    "v6": "Арка накрыла четвёртый блок. Она рассчитана на сто лет.",
    "v7": "В двадцать пятом году конструкцию повредили. Восстановление идёт.",
}
PLAN = {
    "v1": (0.10, 5.00), "v2": (5.15, 12.00), "v3": (12.15, 19.00),
    "v4": (19.15, 27.00), "v5": (27.10, 35.00), "v6": (35.15, 42.00), "v7": (42.10, 47.00),
}
CHAIN = ("highpass=f=80,equalizer=f=250:width_type=h:width=300:g=-1.5,"
         "equalizer=f=3000:width_type=h:width=1400:g=2.2,"
         "equalizer=f=7000:width_type=h:width=2200:g=-3,"
         "acompressor=threshold=-20dB:ratio=3.2:attack=6:release=140:makeup=3,"
         "alimiter=limit=0.95")


def synth(text: str, name: str, length_scale: float = 1.0) -> Path:
    raw = OUT / f"{name}_raw.wav"
    subprocess.run(["/root/tts-venv/bin/python", "-m", "piper", "--model", MODEL,
                    "--length_scale", str(length_scale), "--output_file", str(raw)],
                   input=text.encode(), check=True, cwd="/root/tts-venv/piper",
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc = OUT / f"{name}.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                    "-filter:a", CHAIN, "-ar", str(SR), "-ac", "1", str(proc)], check=True)
    return proc


def ffdur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout.strip())


def read48(p: Path) -> np.ndarray:
    tmp = OUT / "_t48.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(p), "-ar", str(SR), "-ac", "1", str(tmp)], check=True)
    with wave.open(str(tmp), "rb") as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32767


def save(p: Path, a: np.ndarray) -> None:
    a = np.clip(a, -1, 1)
    with wave.open(str(p), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def main() -> None:
    for name, text in FIX.items():
        start, nxt = PLAN[name]
        proc = synth(text, name)
        d = ffdur(proc)
        avail = nxt - start - 0.15
        if d < avail * 0.82:
            proc = synth(text, name, min(1.32, (avail * 0.92) / d))
        print(name, round(ffdur(proc), 2))

    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = (0.07 * np.sin(2 * np.pi * 46 * t) + 0.038 * np.sin(2 * np.pi * 69 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * t))
    for name, (start, nxt) in PLAN.items():
        a = read48(OUT / f"{name}.wav")
        s = int(start * SR); e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        print(name, "->", round(start + (e - s) / SR, 2))
    save(OUT / "mix.wav", np.tanh(mix * 1.02))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(ROOT / "renders/chernobyl-reels.mp4"),
                    "-i", str(OUT / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-reels-final.mp4")], check=True)
    print("готово")


if __name__ == "__main__":
    main()
