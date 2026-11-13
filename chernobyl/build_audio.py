#!/usr/bin/env python3
"""Озвучка «Чернобыльская арка»: XTTS-клон + индустриальный фон."""
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path("/root/video-gen/chernobyl")
OUT = ROOT / "voice"
OUT.mkdir(exist_ok=True)
VIDEO = ROOT / "renders/chernobyl.mp4"
SR = 48000
TOTAL = 60.0
REF = "/tmp/ref_audio_ref.wav"

LINES = [
    ("v1", 0.30, 4.4, "Тридцать шесть тысяч тонн. Собрали в стороне — и передвинули."),
    ("v2", 5.30, 7.4, "Высота — сто восемь метров, длина — сто шестьдесят два, пролёт — двести пятьдесят семь."),
    ("v3", 13.30, 9.4, "Собирать над разрушенным реактором было слишком опасно. Арку собрали в трёхстах метрах."),
    ("v4", 23.30, 11.4, "Конструкцию поставили на направляющие. Двести двадцать четыре гидравлических домкрата толкали её вперёд."),
    ("v5", 35.30, 10.4, "Триста двадцать семь метров. Две недели в ноябре две тысячи шестнадцатого."),
    ("v6", 46.30, 7.4, "Арка накрыла четвёртый блок. Расчётный срок службы — сто лет."),
    ("v7", 54.30, 5.4, "Но в феврале двадцать пятого она получила повреждения. Восстановление ещё не завершено."),
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


def bed(total: float = 60.0) -> np.ndarray:
    n = int(total * SR)
    t = np.arange(n) / SR
    low = 0.10 * np.sin(2 * np.pi * 44 * t) + 0.05 * np.sin(2 * np.pi * 66 * t)
    low *= 0.7 + 0.3 * np.sin(2 * np.pi * 0.07 * t)
    return low


def main() -> None:
    import torch
    torch.set_num_threads(4)
    from TTS.api import TTS

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    mix = bed(TOTAL)
    for name, start, cap, text in LINES:
        wav = np.array(tts.tts(text=text, speaker_wav=REF, language="ru"), dtype=np.float32)
        tmp = OUT / f"{name}_raw.wav"
        arr = (np.clip(wav, -1, 1) * 32767).astype(np.int16)
        with wave.open(str(tmp), "wb") as f:
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(24000); f.writeframes(arr.tobytes())
        a = read_wav(tmp)
        d = len(a) / SR
        if d > cap:
            tempo = min(1.18, d / cap)
            save_wav(OUT / f"{name}_t.wav", a)
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(OUT / f"{name}_t.wav"),
                            "-filter:a", f"atempo={tempo:.3f}", "-ar", str(SR), "-ac", "1", str(OUT / f"{name}.wav")], check=True)
            a = read_wav(OUT / f"{name}.wav")
            d = len(a) / SR
        else:
            save_wav(OUT / f"{name}.wav", a)
        s = int(start * SR)
        e = min(len(mix), s + len(a))
        mix[s:e] += 0.95 * a[: e - s]
        print(f"{name}: {d:.2f}s / cap {cap}", flush=True)

    save_wav(OUT / "mix.wav", np.tanh(mix * 1.05))
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(VIDEO), "-i", str(OUT / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-shortest", str(ROOT / "renders/chernobyl-voice.mp4")], check=True)
    print("готово", dur(ROOT / "renders/chernobyl-voice.mp4"))


if __name__ == "__main__":
    main()
