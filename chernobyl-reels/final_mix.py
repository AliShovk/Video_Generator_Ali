#!/usr/bin/env python3
"""Финальный микс: подгонка реплик под сцены, без наложений."""
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

# сцена -> (файл, старт, следующий старт)
PLAN = [
    ("v1", 0.10, 5.00),
    ("v2", 5.15, 12.00),
    ("v3", 12.15, 19.00),
    ("v4", 19.15, 27.00),
    ("v5", 27.10, 35.00),
    ("v6", 35.15, 42.00),
    ("v7", 42.10, 47.00),
]

SHORT_V7 = "Февраль 2025-го. Арка повреждена. Восстановление идёт."


def ffdur(p: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True, check=True).stdout.strip())


def read48(p: Path) -> np.ndarray:
    tmp = OUT / "_tmp48.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(p), "-ar", str(SR), "-ac", "1", str(tmp)], check=True)
    with wave.open(str(tmp), "rb") as f:
        d = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32767
    return d


def save(p: Path, a: np.ndarray) -> None:
    a = np.clip(a, -1, 1)
    with wave.open(str(p), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def synth_v7() -> None:
    import torch
    torch.set_num_threads(4)
    from TTS.api import TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    wav = np.array(tts.tts(text=SHORT_V7, speaker_wav=REF, language="ru"), dtype=np.float32)
    raw = OUT / "v7_raw.wav"
    with wave.open(str(raw), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
        f.writeframes((np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes())
    chain = ("highpass=f=85,equalizer=f=2800:width_type=h:width=1200:g=2.5,"
             "equalizer=f=6800:width_type=h:width=2000:g=-3.5,"
             "acompressor=threshold=-18dB:ratio=3:attack=8:release=120:makeup=2")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                    "-filter:a", chain, "-ar", str(SR), "-ac", "1", str(OUT / "v7.wav")], check=True)


def main() -> None:
    synth_v7()
    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = (0.075 * np.sin(2 * np.pi * 46 * t) + 0.04 * np.sin(2 * np.pi * 69 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * t))
    report = []
    for name, start, nxt in PLAN:
        src = OUT / f"{name}.wav"
        d = ffdur(src)
        avail = nxt - start - 0.10
        if d > avail:
            tempo = min(1.35, d / avail)
            fast = OUT / f"{name}_fit.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                            "-filter:a", f"atempo={tempo:.3f}", "-ar", str(SR), "-ac", "1", str(fast)], check=True)
            a = read48(fast)
        else:
            a = read48(src)
        s = int(start * SR); e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        report.append({"line": name, "start": round(start, 2), "end": round(start + (e - s) / SR, 2)})
    save(OUT / "mix.wav", np.tanh(mix * 1.02))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(ROOT / "renders/chernobyl-reels.mp4"),
                    "-i", str(OUT / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-reels-voice.mp4")], check=True)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
