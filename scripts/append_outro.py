#!/usr/bin/env python3
"""Приклеить концовку (QR-карточку) к готовому ролику.

usage: append_outro.py input.mp4 [output.mp4]
Результат всегда 1080x1920, 30 fps, H.264 + AAC.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/root/video-gen")
OUTRO = ROOT / "assets/outro/outro.mp4"
W, H, FPS = 1080, 1920, 30


def probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def has_audio(info: dict) -> bool:
    return any(s.get("codec_type") == "audio" for s in info.get("streams", []))


def duration(info: dict) -> float:
    return float(info["format"]["duration"])


def build(src: Path, dst: Path) -> None:
    src_has_a = has_audio(probe(src))
    outro_has_a = has_audio(probe(OUTRO))

    # нормализуем обе части к одному формату и склеиваем
    norm = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={FPS}"
    )
    parts, labels = [], []
    for i, path in enumerate((src, OUTRO)):
        parts.append(f"[{i}:v]{norm}[v{i}]")
    for i, (path, ok) in enumerate(((src, src_has_a), (OUTRO, outro_has_a))):
        if ok:
            parts.append(f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a{i}]")
        else:
            d = duration(probe(path))
            parts.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d}[a{i}]")
    # concat ждёт пары [v][a] в порядке частей
    for i in range(2):
        labels.append(f"[v{i}][a{i}]")

    filt = ";".join(parts) + ";" + "".join(labels) + "concat=n=2:v=1:a=1[v][a]"

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src), "-i", str(OUTRO),
        "-filter_complex", filt,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-profile:v", "main", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-aspect", "9:16", str(dst),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_name(src.stem + "-outro.mp4")
    build(src, dst)
    info = probe(dst)
    print(f"ok: {dst} | {duration(info):.2f}s | {W}x{H}")


if __name__ == "__main__":
    main()
