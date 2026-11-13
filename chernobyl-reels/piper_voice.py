#!/usr/bin/env python3
"""Озвучка Piper (ru_RU-denis): чистый синтез без артефактов, подгонка под сцены."""
import json
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-reels")
OUT = ROOT / "voice_piper"
OUT.mkdir(exist_ok=True)
MODEL = Path("/root/tts-venv/piper/ru_denis.onnx")
SR = 48000
TOTAL = 47.0

LINES = [
    ("v1", 0.10, 5.00, "Тридцать шесть тысяч тонн. Собрали в стороне — и передвинули.", 1.0),
    ("v2", 5.15, 12.00, "Высота — сто восемь метров. Пролёт — двести пятьдесят семь. Длина — сто шестьдесят два.", 0.98),
    ("v3", 12.15, 19.00, "Над разрушенным реактором собирать было слишком опасно.", 1.0),
    ("v4", 19.15, 27.00, "Двести двадцать четыре гидравлических домкрата поставили арку на рельсы.", 0.98),
    ("v5", 27.10, 35.00, "Триста двадцать семь метров. Две недели в ноябре две тысячи шестнадцатого.", 0.98),
    ("v6", 35.15, 42.00, "Арка накрыла четвёртый блок. Срок службы — сто лет.", 1.0),
    ("v7", 42.10, 47.00, "Февраль две тысячи двадцать пятого. Арка повреждена. Восстановление идёт.", 0.97),
]

CHAIN = ("highpass=f=80,equalizer=f=250:width_type=h:width=300:g=-1.5,"
         "equalizer=f=3000:width_type=h:width=1400:g=2.2,"
         "equalizer=f=7000:width_type=h:width=2200:g=-3,"
         "acompressor=threshold=-20dB:ratio=3.2:attack=6:release=140:makeup=3,"
         "alimiter=limit=0.95")


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


def synth(text: str, name: str, length_scale: float) -> Path:
    txt = OUT / f"{name}.txt"
    txt.write_text(text, encoding="utf-8")
    raw = OUT / f"{name}_raw.wav"
    subprocess.run(["/root/tts-venv/bin/python", "-m", "piper", "--model", str(MODEL),
                    "--length_scale", str(length_scale), "--output_file", str(raw)],
                   input=text.encode(), check=True, cwd="/root/tts-venv/piper",
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc = OUT / f"{name}.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                    "-filter:a", CHAIN, "-ar", str(SR), "-ac", "1", str(proc)], check=True)
    return proc


def main() -> None:
    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = (0.07 * np.sin(2 * np.pi * 46 * t) + 0.038 * np.sin(2 * np.pi * 69 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * t))
    report = []
    for name, start, nxt, text, ls in LINES:
        proc = synth(text, name, ls)
        d = ffdur(proc)
        avail = nxt - start - 0.15
        # подгоняем темп речи под окно сцены: без длинных пауз, но и без спешки
        if d < avail * 0.82:
            ls2 = min(1.32, ls * (avail * 0.92) / d)
            proc = synth(text, name, ls2)
            d = ffdur(proc)
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
        report.append({"line": name, "start": start, "end": round(start + (e - s) / SR, 2)})
    save(OUT / "mix.wav", np.tanh(mix * 1.02))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(ROOT / "renders/chernobyl-reels.mp4"),
                    "-i", str(OUT / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-reels-piper.mp4")], check=True)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
