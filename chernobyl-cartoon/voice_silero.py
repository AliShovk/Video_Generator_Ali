#!/usr/bin/env python3
"""Женский голос Silero (baya): фразовый синтез, паузы, студийная обработка."""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-cartoon")
OUT = ROOT / "voice_silero"
OUT.mkdir(exist_ok=True)
SR = 48000
TOTAL = 47.0

LINES = [
    ("v1", 0.15, 5.00, ["Тридцать шесть тысяч тонн.", "Собрали в стороне —", "и передвинули."]),
    ("v2", 5.15, 12.00, ["Высота — сто восемь метров.", "Пролёт — двести пятьдесят семь.", "Длина — сто шестьдесят два."]),
    ("v3", 12.15, 19.00, ["Над разрушенным реактором", "собирать было слишком опасно."]),
    ("v4", 19.15, 27.00, ["Двести двадцать четыре домкрата", "двигали её вперёд."]),
    ("v5", 27.10, 35.00, ["Триста двадцать семь метров.", "Две недели,", "ноябрь две тысячи шестнадцатого."]),
    ("v6", 35.15, 42.00, ["Арка накрыла четвёртый блок.", "Рассчитана на сто лет."]),
    ("v7", 42.10, 47.00, ["В двадцать пятом году", "конструкцию повредили.", "Восстановление идёт."]),
]

CHAIN = ("highpass=f=80,"
         "equalizer=f=220:width_type=h:width=180:g=1.8,"
         "equalizer=f=3000:width_type=h:width=1400:g=1.6,"
         "equalizer=f=7000:width_type=h:width=2200:g=-3,"
         "acompressor=threshold=-20dB:ratio=3:attack=6:release=150:makeup=3,"
         "alimiter=limit=0.94")


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
    import torch
    torch.set_num_threads(6)
    model, _ = torch.hub.load('snakers4/silero-models', 'silero_tts', language='ru', speaker='v4_ru', trust_repo=True)

    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = 0.04 * np.sin(2 * np.pi * 52 * t) * (0.65 + 0.35 * np.sin(2 * np.pi * 0.05 * t))
    report = []

    for name, start, nxt, phrases in LINES:
        chunks = []
        for i, ph in enumerate(phrases):
            audio = model.apply_tts(text=ph, speaker="baya", sample_rate=SR, put_accent=True, put_yo=True)
            a = audio.numpy().astype(np.float32)
            idx = np.where(np.abs(a) > 0.008)[0]
            if len(idx):
                a = a[max(0, idx[0] - 120): idx[-1] + 4000]
            chunks.append(a)
            if i < len(phrases) - 1:
                chunks.append(np.zeros(int(0.22 * SR), dtype=np.float32))
        line = np.concatenate(chunks)
        raw = OUT / f"{name}_raw.wav"
        save(raw, line)

        proc = OUT / f"{name}.wav"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                        "-filter:a", CHAIN, "-ar", str(SR), "-ac", "1", str(proc)], check=True)

        d = len(read48(proc)) / SR
        avail = nxt - start - 0.15
        if d > avail:
            fit = OUT / f"{name}_fit.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(proc),
                            "-filter:a", f"atempo={min(1.3, d/avail):.3f}", "-ar", str(SR), "-ac", "1", str(fit)], check=True)
            a = read48(fit)
        elif d < avail * 0.78:
            slow = OUT / f"{name}_slow.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(proc),
                            "-filter:a", f"atempo={max(0.88, d/(avail*0.88)):.3f}", "-ar", str(SR), "-ac", "1", str(slow)], check=True)
            a = read48(slow)
        else:
            a = read48(proc)
        s = int(start * SR); e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        report.append({"line": name, "start": start, "end": round(start + (e - s) / SR, 2)})

    save(OUT / "mix.wav", np.tanh(mix * 1.05))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(ROOT / "renders/chernobyl-cartoon-v2.mp4"), "-i", str(OUT / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-cartoon-final.mp4")], check=True)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
