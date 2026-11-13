#!/usr/bin/env python3
"""Правка двух реплик + пересборка микса без полного пересинтеза."""
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-reels")
OUT = ROOT / "voice"
VIDEO = ROOT / "renders/chernobyl-reels.mp4"
SR = 48000
TOTAL = 47.0
REF = "/tmp/ref_clean.wav"

LINES = [
    ("v1", 0.20, 4.5, "36 тысяч тонн. Собрали в стороне — и передвинули."),
    ("v2", 5.25, 6.4, None),
    ("v3", 12.25, 6.4, None),
    ("v4", 19.25, 7.4, None),
    ("v5", 27.10, 7.6, None),
    ("v6", 35.25, 6.4, None),
    ("v7", 42.20, 4.6, "В феврале 2025-го её повредили. Восстановление идёт."),
]


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as f:
        data = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32767
        sr, ch = f.getframerate(), f.getnchannels()
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        data = np.interp(np.linspace(0, len(data) - 1, int(len(data) * SR / sr)), np.arange(len(data)), data).astype(np.float32)
    return data


def save_wav(path: Path, audio: np.ndarray) -> None:
    a = np.clip(audio, -1, 1)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def synth(text: str, name: str) -> np.ndarray:
    import torch
    torch.set_num_threads(4)
    from TTS.api import TTS
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    wav = np.array(tts.tts(text=text, speaker_wav=REF, language="ru"), dtype=np.float32)
    raw = OUT / f"{name}_raw.wav"
    with wave.open(str(raw), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
        f.writeframes((np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes())
    chain = ("highpass=f=85,equalizer=f=2800:width_type=h:width=1200:g=2.5,"
             "equalizer=f=6800:width_type=h:width=2000:g=-3.5,"
             "acompressor=threshold=-18dB:ratio=3:attack=8:release=120:makeup=2")
    proc = OUT / f"{name}.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                    "-filter:a", chain, "-ar", str(SR), "-ac", "1", str(proc)], check=True)
    return read_wav(proc)


def main() -> None:
    n = int(TOTAL * SR)
    t = np.arange(n) / SR
    mix = (0.075 * np.sin(2 * np.pi * 46 * t) + 0.04 * np.sin(2 * np.pi * 69 * t)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * t))

    for name, start, cap, text in LINES:
        if text:
            a = synth(text, name)
        else:
            a = read_wav(OUT / f"{name}.wav")
        d = len(a) / SR
        if d > cap:
            fast = OUT / f"{name}_t.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(OUT / f"{name}.wav"),
                            "-filter:a", f"atempo={min(1.15, d / cap):.3f}", "-ar", str(SR), "-ac", "1", str(fast)], check=True)
            a = read_wav(fast)
            d = len(a) / SR
        s = int(start * SR)
        e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        print(f"{name}: {d:.2f}s / cap {cap}", flush=True)

    save_wav(OUT / "mix.wav", np.tanh(mix * 1.02))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(VIDEO), "-i", str(OUT / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-reels-voice.mp4")], check=True)
    print("готово")


if __name__ == "__main__":
    main()
