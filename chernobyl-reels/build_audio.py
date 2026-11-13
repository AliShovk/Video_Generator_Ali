#!/usr/bin/env python3
"""Reels-озвучка: чистый референс, обработка голоса, микс, луфнорм I=-14."""
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl-reels")
OUT = ROOT / "voice"
OUT.mkdir(exist_ok=True)
VIDEO = ROOT / "renders/chernobyl-reels.mp4"
SR = 48000
TOTAL = 47.0
REF = "/tmp/ref_clean.wav"

LINES = [
    ("v1", 0.25, 4.2, "36 тысяч тонн. Арку собрали в стороне — и передвинули."),
    ("v2", 5.25, 6.4, "Высота — 108 метров, пролёт — 257, длина — 162."),
    ("v3", 12.25, 6.4, "Над разрушенным реактором собирать было слишком опасно."),
    ("v4", 19.25, 7.4, "224 гидравлических домкрата поставили арку на рельсы."),
    ("v5", 27.25, 7.4, "327 метров. Две недели в ноябре 2016-го."),
    ("v6", 35.25, 6.4, "Арка накрыла четвёртый блок. Срок службы — 100 лет."),
    ("v7", 42.25, 4.4, "Но в феврале 2025-го её повредили. Восстановление идёт."),
]


def dur(path: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True, check=True).stdout.strip())


def save_wav(path: Path, audio: np.ndarray) -> None:
    a = np.clip(audio, -1, 1)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as f:
        data = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32767
        sr, ch = f.getframerate(), f.getnchannels()
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        data = np.interp(np.linspace(0, len(data) - 1, int(len(data) * SR / sr)), np.arange(len(data)), data).astype(np.float32)
    return data


def bed(total: float) -> np.ndarray:
    n = int(total * SR)
    t = np.arange(n) / SR
    low = 0.075 * np.sin(2 * np.pi * 46 * t) + 0.04 * np.sin(2 * np.pi * 69 * t)
    return low * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * t))


def main() -> None:
    import torch
    torch.set_num_threads(4)
    from TTS.api import TTS

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    mix = bed(TOTAL)
    for name, start, cap, text in LINES:
        wav = np.array(tts.tts(text=text, speaker_wav=REF, language="ru"), dtype=np.float32)
        raw = OUT / f"{name}_raw.wav"
        with wave.open(str(raw), "wb") as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000)
            f.writeframes((np.clip(wav, -1, 1) * 32767).astype(np.int16).tobytes())

        # обработка: срез низа, присутствие, де-эссер, компрессор
        proc = OUT / f"{name}.wav"
        chain = ("highpass=f=85,equalizer=f=2800:width_type=h:width=1200:g=2.5,"
                 "equalizer=f=6800:width_type=h:width=2000:g=-3.5,"
                 "acompressor=threshold=-18dB:ratio=3:attack=8:release=120:makeup=2")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(raw),
                        "-filter:a", chain, "-ar", str(SR), "-ac", "1", str(proc)], check=True)
        a = read_wav(proc)
        d = len(a) / SR
        if d > cap:
            tempo = min(1.15, d / cap)
            fast = OUT / f"{name}_t.wav"
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(proc),
                            "-filter:a", f"atempo={tempo:.3f}", "-ar", str(SR), "-ac", "1", str(fast)], check=True)
            a = read_wav(fast)
            d = len(a) / SR
        s = int(start * SR)
        e = min(len(mix), s + len(a))
        mix[s:e] += 1.0 * a[: e - s]
        print(f"{name}: {d:.2f}s / cap {cap}", flush=True)

    save_wav(OUT / "mix.wav", np.tanh(mix * 1.02))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(VIDEO), "-i", str(OUT / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9", "-shortest", str(ROOT / "renders/chernobyl-reels-voice.mp4")], check=True)
    print("готово", dur(ROOT / "renders/chernobyl-reels-voice.mp4"))


if __name__ == "__main__":
    main()
