#!/usr/bin/env python3
"""Голос (Piper) + субтитры (SRT) для конвейера."""
from __future__ import annotations

import json
import subprocess
import wave
from pathlib import Path

import re

import numpy as np

from numru import ru_number

MODEL = "/root/tts-venv/piper/ru_denis.onnx"
FALLBACK = "/root/tts-venv/piper/ru_denis.onnx"
SR = 48000
CHAIN = ("highpass=f=85,equalizer=f=240:width_type=h:width=200:g=1.8,"
         "equalizer=f=3000:width_type=h:width=1400:g=2.2,"
         "equalizer=f=7000:width_type=h:width=2200:g=-3.5,"
         "acompressor=threshold=-20dB:ratio=3:attack=6:release=150:makeup=3,"
         "alimiter=limit=0.94")


def wav_dur(p: Path) -> float:
    with wave.open(str(p), "rb") as f:
        return f.getnframes() / f.getframerate()


def read48(p: Path) -> np.ndarray:
    tmp = p.parent / "_tmp48.wav"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(p),
                    "-ar", str(SR), "-ac", "1", str(tmp)], check=True)
    with wave.open(str(tmp), "rb") as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32767


def save(p: Path, a: np.ndarray) -> None:
    a = np.clip(a, -1, 1)
    with wave.open(str(p), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def piper(text: str, out_wav: Path, model: str, length_scale: float = 1.0) -> None:
    subprocess.run(["/root/tts-venv/bin/python", "-m", "piper", "--model", model,
                    "--length_scale", str(length_scale), "--output_file", str(out_wav)],
                   input=text.encode(), check=True, cwd="/root/tts-venv/piper",
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def digits_to_words(text: str) -> str:
    def repl(m):
        raw = m.group(0).replace(" ", "").replace("\u00a0", "")
        return ru_number(int(raw)) if raw.isdigit() else m.group(0)
    return re.sub(r"\d[\d\s]{0,12}", repl, text)


_SILERO = None


def _silero():
    global _SILERO
    if _SILERO is None:
        import torch
        torch.set_num_threads(6)
        model, _ = torch.hub.load('snakers4/silero-models', 'silero_tts', language='ru',
                                  speaker='v4_ru', trust_repo=True)
        _SILERO = model
    return _SILERO


def synth_silero(text: str, speaker: str = "aidar") -> np.ndarray:
    model = _silero()
    parts = []
    for i, ph in enumerate([p.strip() for p in text.replace("—", "-").split(".") if p.strip()]):
        a = model.apply_tts(text=ph + ".", speaker=speaker, sample_rate=SR,
                            put_accent=True, put_yo=True).numpy().astype(np.float32)
        idx = np.where(np.abs(a) > 0.008)[0]
        if len(idx):
            a = a[max(0, idx[0] - 150): min(len(a), idx[-1] + 3500)]
        parts.append(a)
        parts.append(np.zeros(int(0.2 * SR), dtype=np.float32))
    return np.concatenate(parts) if parts else np.zeros(int(0.5 * SR), dtype=np.float32)


def synth_scene(text: str, tmpdir: Path, tag: str) -> np.ndarray:
    text = digits_to_words(text)
    try:
        return synth_silero(text)
    except Exception as exc:  # noqa: BLE001
        print(f"[voice] silero недоступен ({exc}); piper")
    model = MODEL if Path(MODEL).exists() else FALLBACK
    phrases = [p.strip() for p in text.replace("—", "-").split(".") if p.strip()]
    chunks: list[np.ndarray] = []
    for i, ph in enumerate(phrases):
        raw = tmpdir / f"{tag}_{i}.wav"
        piper(ph + ".", raw, model)
        a = read48(raw)
        idx = np.where(np.abs(a) > 0.008)[0]
        if len(idx):
            a = a[max(0, idx[0] - 150): min(len(a), idx[-1] + 3000)]
        chunks.append(a)
        if i < len(phrases) - 1:
            chunks.append(np.zeros(int(0.2 * SR), dtype=np.float32))
    return np.concatenate(chunks) if chunks else np.zeros(int(0.5 * SR), dtype=np.float32)


def build_voice(scenes: list[dict], out: Path) -> tuple[Path, list[dict]]:
    tmp = out / "voice_parts"
    tmp.mkdir(exist_ok=True)
    total = sum(s["duration"] for s in scenes)
    mix = np.zeros(int(total * SR), dtype=np.float32)
    start = 0.0
    timing = []
    for sc in scenes:
        a = synth_scene(sc["narration"], tmp, sc["id"])
        d = len(a) / SR
        avail = sc["duration"] - 0.25
        if d > avail:
            tmp_in = tmp / f"{sc['id']}_in.wav"
            tmp_out = tmp / f"{sc['id']}_fit.wav"
            save(tmp_in, a)
            subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp_in),
                            "-filter:a", f"atempo={min(1.3, d/avail):.3f}", "-ar", str(SR), "-ac", "1", str(tmp_out)], check=True)
            a = read48(tmp_out)
            d = len(a) / SR
        s = int((start + 0.15) * SR)
        e = min(len(mix), s + len(a))
        mix[s:e] += a[: e - s]
        timing.append({"id": sc["id"], "start": round(start + 0.15, 2), "end": round(start + 0.15 + (e - s) / SR, 2),
                       "text": sc["narration"]})
        start += sc["duration"]

    voice = out / "voice.wav"
    save(voice, np.tanh(mix * 1.02))
    (out / "timings.json").write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding="utf-8")
    return voice, timing


def fmt_ts(sec: float) -> str:
    h = int(sec // 3600); m = int((sec % 3600) // 60); s = sec % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def build_srt(timing: list[dict], out: Path) -> Path:
    lines = []
    idx = 1
    for item in timing:
        words = item["text"].split()
        chunks = []
        cur: list[str] = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) >= 42:
                chunks.append(" ".join(cur)); cur = []
        if cur:
            chunks.append(" ".join(cur))
        span = max(0.8, (item["end"] - item["start"]) / max(1, len(chunks)))
        t0 = item["start"]
        for c in chunks:
            t1 = min(item["end"], t0 + span)
            lines.append(f"{idx}\n{fmt_ts(t0)} --> {fmt_ts(t1)}\n{c}\n")
            idx += 1
            t0 = t1
    path = out / "subtitles.srt"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
