#!/usr/bin/env python3
"""Голос для мультяшной версии: фразовый синтез, паузы, студийная обработка."""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-cartoon")
OUT = ROOT / "voice"
OUT.mkdir(exist_ok=True)
MODEL = "/root/tts-venv/piper/ru_irina.onnx"
SR = 48000
TOTAL = 47.0

# (id, старт, конец окна, [фразы], скорость)
LINES = [
    ("v1", 0.15, 5.00, ["Тридцать шесть тысяч тонн.", "Собрали в стороне —", "и передвинули."], 1.02),
    ("v2", 5.15, 12.00, ["Высота — сто восемь метров.", "Пролёт — двести пятьдесят семь.", "Длина — сто шестьдесят два."], 1.0),
    ("v3", 12.15, 19.00, ["Над разрушенным реактором", "собирать было слишком опасно."], 1.0),
    ("v4", 19.15, 27.00, ["Двести двадцать четыре домкрата", "двигали её вперёд."], 1.0),
    ("v5", 27.10, 35.00, ["Триста двадцать семь метров.", "Две недели,", "ноябрь две тысячи шестнадцатого."], 1.0),
    ("v6", 35.15, 42.00, ["Арка накрыла четвёртый блок.", "Рассчитана на сто лет."], 1.0),
    ("v7", 42.10, 47.00, ["В двадцать пятом году", "конструкцию повредили.", "Восстановление идёт."], 1.0),
]

CHAIN = ("highpass=f=75,"
         "equalizer=f=200:width_type=h:width=180:g=2.0,"
         "equalizer=f=3000:width_type=h:width=1400:g=1.8,"
         "equalizer=f=7200:width_type=h:width=2200:g=-4,"
         "acompressor=threshold=-20dB:ratio=3.2:attack=6:release=150:makeup=3,"
         "aecho=0.9:0.85:22:0.075,"
         "alimiter=limit=0.94")


def synth_phrase(text: str, tag: str, speed: float) -> np.ndarray:
    raw = OUT / f"_{tag}.wav"
    subprocess.run(["/root/tts-venv/bin/python", "-m", "piper", "--model", MODEL,
                    "--length_scale", f"{1.0 / speed:.3f}", "--output_file", str(raw)],
                   input=text.encode(), check=True, cwd="/root/tts-venv/piper",
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(str(raw), "rb") as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32767
        sr = f.getframerate()
    if sr != 24000:
        a = np.interp(np.linspace(0, len(a) - 1, int(len(a) * 24000 / sr)), np.arange(len(a)), a).astype(np.float32)
    return a


def trim(a: np.ndarray, thr=0.008) -> np.ndarray:
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0:
        return a
    lo, hi = max(0, idx[0] - 200), min(len(a), idx[-1] + 3000)
    return a[lo:hi]


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
    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = 0.045 * np.sin(2 * np.pi * 52 * t) * (0.65 + 0.35 * np.sin(2 * np.pi * 0.05 * t))
    report = []

    for name, start, nxt, phrases, speed in LINES:
        gap = np.zeros(int(0.24 * 24000), dtype=np.float32)
        chunks = []
        for i, ph in enumerate(phrases):
            chunks.append(trim(synth_phrase(ph, f"{name}_{i}", speed)))
            if i < len(phrases) - 1:
                chunks.append(gap)
        a24 = np.concatenate(chunks)
        raw = OUT / f"{name}_raw.wav"
        with wave.open(str(raw), "wb") as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
            f.writeframes((np.clip(a24, -1, 1) * 32767).astype(np.int16).tobytes())

        proc = OUT / f"{name}.wav"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                        "-filter:a", CHAIN, "-ar", str(SR), "-ac", "1", str(proc)], check=True)

        d = len(read48(proc)) / SR
        avail = nxt - start - 0.15
        if d > avail:
            fit = OUT / f"{name}_fit.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(proc),
                            "-filter:a", f"atempo={min(1.32, d/avail):.3f}", "-ar", str(SR), "-ac", "1", str(fit)], check=True)
            a = read48(fit)
        else:
            a = read48(proc)
        s = int(start * SR); e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        report.append({"line": name, "start": start, "end": round(start + (e - s) / SR, 2)})

    save(OUT / "mix.wav", np.tanh(mix * 1.05))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(ROOT / "renders/chernobyl-cartoon.mp4"), "-i", str(OUT / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-cartoon-voice.mp4")], check=True)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
