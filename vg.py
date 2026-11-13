#!/usr/bin/env python3
"""vg — единая команда для видеогенератора /root/video-gen.

  vg list                     список проектов
  vg voice  <name>            синтез озвучки (Silero) -> timings.json, voice.wav
  vg build  <name>            сборка HTML-сцен
  vg render <name> [quality]   рендер HyperFrames -> render.mp4
  vg final  <name>            сведение звука + концовка -> <name>-final.mp4
  vg make   <name>            voice + build + render + final одной командой
  vg new    <name> [--from solarfence]   копия проекта как шаблон
  vg push                     залить исходники в GitHub (AliShovk/Video_Generator_Ali)
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/root/video-gen")
PY = "/usr/local/lib/hermes-agent/venv/bin/python"
OUTRO = ROOT / "assets/outro/outro.mp4"
APPEND = ROOT / "scripts/append_outro.py"


def proj(name: str) -> Path:
    p = ROOT / name
    if not p.is_dir():
        sys.exit(f"нет проекта: {p}")
    return p


def run(cmd, cwd=None):
    print("+", " ".join(cmd))
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if r.returncode != 0:
        sys.exit(f"команда упала ({r.returncode}): {' '.join(cmd)}")


def cmd_list():
    rows = []
    for p in sorted(ROOT.iterdir()):
        if (p / "build.py").exists():
            mp4 = next(iter(sorted(ROOT.glob(f"{p.name}*-final.mp4"))), None)
            rows.append((p.name, "final" if mp4 else ("render" if (p / "render.mp4").exists() else "src")))
    print(f"проектов: {len(rows)}")
    for n, st in rows:
        print(f"  {n:<16} {st}")


def cmd_voice(name):
    p = proj(name)
    if not (p / "voice.py").exists():
        sys.exit("нет voice.py")
    run([PY, "voice.py"], cwd=p)


def cmd_build(name):
    p = proj(name)
    run([PY, "build.py"], cwd=p)


def cmd_render(name, quality="high"):
    p = proj(name)
    run(["node", "../node_modules/hyperframes/bin/hyperframes.mjs", "render",
         "-o", "render.mp4", "--quality", quality], cwd=p)


def cmd_final(name):
    p = proj(name)
    render, voice = p / "render.mp4", p / "voice.wav"
    if not render.exists():
        sys.exit("нет render.mp4 — сначала vg render")
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(render)]).strip())
    tmp = p / "_main.mp4"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(render)]
    if voice.exists():
        cmd += ["-i", str(voice), "-filter_complex", "[1:a]loudnorm=I=-16:TP=-1.5:LRA=11[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-c:v", "libx264", "-profile:v", "main", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.2f}", "-movflags", "+faststart",
            "-aspect", "9:16", str(tmp)]
    run(cmd)
    out = ROOT / f"{name}-final.mp4"
    run([PY, str(APPEND), str(tmp), str(out)])
    tmp.unlink(missing_ok=True)
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,display_aspect_ratio", "-of", "csv=p=0", str(out)]).decode().strip()
    print(f"готово: {out} | {probe}")


def cmd_make(name):
    cmd_voice(name)
    cmd_build(name)
    cmd_render(name)
    cmd_final(name)


def cmd_new(name, src="solarfence"):
    dst = ROOT / name
    if dst.exists():
        sys.exit(f"уже существует: {dst}")
    shutil.copytree(proj(src), dst, ignore=shutil.ignore_patterns(
        "render.mp4", "*.wav", "__pycache__", "compositions", "timings.json"))
    print(f"создан {dst} из {src}")
    print("дальше: правь voice.py + build.py, затем vg make", name)


MIRROR = Path("/root/.video-gen-mirror")
REMOTE = "git@github.com:AliShovk/Video_Generator_Ali.git"


def cmd_push(msg=None):
    """Синхронизирует исходники в зеркало и пушит в GitHub."""
    if not (MIRROR / ".git").exists():
        if MIRROR.exists():
            shutil.rmtree(MIRROR)
        run(["git", "clone", REMOTE, str(MIRROR)])
    run(["rsync", "-a", "--delete",
         "--exclude", ".git/", "--exclude", "node_modules/", "--exclude", "browsers/", "--exclude", "__pycache__/",
         "--exclude", ".hyperframes/", "--exclude", "*.wav", "--exclude", "*.mp4", "--exclude", "*.log",
         f"{ROOT}/", f"{MIRROR}/"])
    for f in ("outro.mp4", "outro-old.mp4"):
        src = ROOT / "assets/outro" / f
        if src.exists():
            shutil.copy2(src, MIRROR / "assets/outro" / f)
    run(["git", "add", "-A"], cwd=MIRROR)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=MIRROR)
    if diff.returncode == 0:
        print("нет изменений — всё уже в GitHub")
        return
    import datetime
    text = msg or f"Обновление видеогенератора {datetime.datetime.now():%d.%m.%Y %H:%M}"
    run(["git", "-c", "user.name=AliShovk", "-c", "user.email=alishovk@users.noreply.github.com",
         "commit", "-q", "-m", text], cwd=MIRROR)
    run(["git", "push", "origin", "HEAD:main"], cwd=MIRROR)
    print("запушено:", subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=MIRROR).decode().strip())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    c = sys.argv[1]
    args = sys.argv[2:]
    if c == "list":
        cmd_list()
    elif c == "voice":
        cmd_voice(args[0])
    elif c == "build":
        cmd_build(args[0])
    elif c == "render":
        cmd_render(args[0], args[1] if len(args) > 1 else "high")
    elif c == "final":
        cmd_final(args[0])
    elif c == "make":
        cmd_make(args[0])
    elif c == "new":
        cmd_new(args[0], args[2] if len(args) > 2 and args[1] == "--from" else "solarfence")
    elif c == "push":
        cmd_push(args[0] if args else None)
    else:
        print(__doc__)
