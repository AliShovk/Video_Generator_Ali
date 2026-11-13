#!/usr/bin/env python3
"""Озвучка «Гравитация исчезла на 10 секунд» — Silero baya."""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/mirrors")
OUT = ROOT / "voice"
OUT.mkdir(exist_ok=True)
SR = 48000
TOTAL = 60.0

LINES = [
    ("v1", 0.40, 10.00, ["Ты видишь в боковом зеркале свою дверь?", "Значит машину рядом ты не видишь."]),
    ("v2", 10.30, 18.00, ["Перестроился — удар в бок.", "Штраф и виноват в аварии ты."]),
    ("v3", 18.30, 30.00, ["Слева догоняет машина.", "В заднем зеркале она есть.", "Потом уходит вбок — и исчезает."]),
    ("v4", 30.30, 40.00, ["Боковое зеркало смотрит назад,", "а не в слепую зону."]),
    ("v5", 40.30, 52.00, ["Наклони голову к стеклу", "и разверни зеркало так,", "чтобы край кузова был едва виден."]),
    ("v6", 52.30, 59.60, ["Слепая зона перекрыта.", "Проверь оба зеркала."]),
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
    mix = 0.035 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.06 * t))
    report = []

    for name, start, nxt, phrases in LINES:
        chunks = []
        for i, ph in enumerate(phrases):
            audio = model.apply_tts(text=ph, speaker="aidar", sample_rate=SR, put_accent=True, put_yo=True)
            a = audio.numpy().astype(np.float32)
            idx = np.where(np.abs(a) > 0.008)[0]
            if len(idx):
                a = a[max(0, idx[0] - 120): idx[-1] + 4000]
            chunks.append(a)
            if i < len(phrases) - 1:
                chunks.append(np.zeros(int(0.2 * SR), dtype=np.float32))
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
        elif d < avail * 0.75:
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
                    "-i", str(ROOT / "renders/mirrors.mp4"), "-i", str(OUT / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/mirrors-voice.mp4")], check=True)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
