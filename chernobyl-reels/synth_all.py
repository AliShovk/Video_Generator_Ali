#!/usr/bin/env python3
"""Переозвучка: числа словами, мягкие параметры XTTS, подгонка под сцены."""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-reels")
OUT = ROOT / "voice"
SR = 48000
TOTAL = 47.0
REF = "/tmp/ref_clean.wav"

LINES = [
    ("v1", 0.10, 5.00, "Тридцать шесть тысяч тонн. Собрали в стороне — и передвинули."),
    ("v2", 5.15, 12.00, "Высота — сто восемь метров. Пролёт — двести пятьдесят семь. Длина — сто шестьдесят два."),
    ("v3", 12.15, 19.00, "Над разрушенным реактором собирать было слишком опасно."),
    ("v4", 19.15, 27.00, "Двести двадцать четыре гидравлических домкрата поставили арку на рельсы."),
    ("v5", 27.10, 35.00, "Триста двадцать семь метров. Две недели в ноябре две тысячи шестнадцатого."),
    ("v6", 35.15, 42.00, "Арка накрыла четвёртый блок. Срок службы — сто лет."),
    ("v7", 42.10, 47.00, "Февраль две тысячи двадцать пятого. Арка повреждена. Восстановление идёт."),
]

CHAIN = ("highpass=f=85,equalizer=f=2800:width_type=h:width=1200:g=2.5,"
         "equalizer=f=6800:width_type=h:width=2000:g=-3.5,"
         "acompressor=threshold=-18dB:ratio=3:attack=8:release=120:makeup=2")


def ffdur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout.strip())


def read48(p: Path) -> np.ndarray:
    tmp = OUT / "_tmp48.wav"
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
    from TTS.api import TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = (0.07 * np.sin(2 * np.pi * 46 * t) + 0.038 * np.sin(2 * np.pi * 69 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * t))
    report = []

    for name, start, nxt, text in LINES:
        wav = np.array(tts.tts(text=text, speaker_wav=REF, language="ru", speed=0.95,
                               temperature=0.6, repetition_penalty=6.0, top_p=0.8), dtype=np.float32)
        raw = OUT / f"{name}_raw.wav"
        with wave.open(str(raw), "wb") as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
            f.writeframes((np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes())
        proc = OUT / f"{name}.wav"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                        "-filter:a", CHAIN, "-ar", str(SR), "-ac", "1", str(proc)], check=True)

        d = ffdur(proc)
        avail = nxt - start - 0.10
        if d > avail:
            tempo = min(1.3, d / avail)
            fit = OUT / f"{name}_fit.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(proc),
                            "-filter:a", f"atempo={tempo:.3f}", "-ar", str(SR), "-ac", "1", str(fit)], check=True)
            a = read48(fit)
        else:
            a = read48(proc)
        s = int(start * SR); e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        report.append({"line": name, "dur": round((e - s) / SR, 2), "start": start, "end": round(start + (e - s) / SR, 2)})

    save(OUT / "mix.wav", np.tanh(mix * 1.02))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(ROOT / "renders/chernobyl-reels.mp4"),
                    "-i", str(OUT / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-reels-voice.mp4")], check=True)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
