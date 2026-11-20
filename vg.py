#!/usr/bin/env python3
"""vg — единая команда для видеогенератора /root/video-gen.

  vg list                     список проектов
  vg voice  <name>            синтез озвучки (Silero) -> timings.json, voice.wav
  vg build  <name>            сборка HTML-сцен
  vg render <name> [quality]   рендер HyperFrames -> render.mp4
  vg final  <name> [--reels]  сведение звука + концовка -> <name>-final.mp4
                              --reels: без 5,8 с концовки, громкость -14 LUFS (Instagram)
  vg make   <name> [--reels]  voice + build + render + final одной командой
  vg meta   <name>            подпись, UTM-ссылка, проверка хука -> <name>/instagram.md
  vg new    <name> [--from solarfence]   копия проекта как шаблон
  vg studio new <name> [--format 9:16] [--from demo]   рисованный ролик (Animation Studio)
  vg studio list | song | make | render | outro <name>  второй движок: кадры кодом + музыка кодом
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


def cmd_final(name, reels=False):
    p = proj(name)
    render, voice = p / "render.mp4", p / "voice.wav"
    if not render.exists():
        sys.exit("нет render.mp4 — сначала vg render")
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(render)]).strip())
    tmp = p / "_main.mp4"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(render)]
    if voice.exists():
        cmd += ["-i", str(voice), "-filter_complex", f"[1:a]loudnorm=I={-14 if reels else -16}:TP=-1.5:LRA=11[a]",
                "-map", "0:v", "-map", "[a]"]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-c:v", "libx264", "-profile:v", "main", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.2f}", "-movflags", "+faststart",
            "-aspect", "9:16", str(tmp)]
    run(cmd)
    out = ROOT / f"{name}-final.mp4"
    if reels:
        tmp.replace(out)
    else:
        run([PY, str(APPEND), str(tmp), str(out)])
        tmp.unlink(missing_ok=True)
    probe = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,display_aspect_ratio", "-of", "csv=p=0", str(out)]).decode().strip()
    print(f"готово: {out} | {probe}")


def cmd_make(name, reels=False):
    cmd_voice(name)
    cmd_build(name)
    cmd_render(name)
    cmd_final(name, reels)
    if reels:
        cmd_meta(name)


def cmd_meta(name):
    run([PY, str(ROOT / "scripts/reels_meta.py"), str(proj(name))])


def cmd_new(name, src="solarfence"):
    dst = ROOT / name
    if dst.exists():
        sys.exit(f"уже существует: {dst}")
    shutil.copytree(proj(src), dst, ignore=shutil.ignore_patterns(
        "render.mp4", "*.wav", "__pycache__", "compositions", "timings.json"))
    print(f"создан {dst} из {src}")
    print("дальше: правь voice.py + build.py, затем vg make", name)


# ---------- Animation Studio (второй движок: рисованные ролики + синтезированная музыка) ----------
STUDIO = ROOT / "engines/animation-studio"


def studio_proj(name: str) -> Path:
    p = ROOT / name
    if not (p / "score.js").exists():
        sys.exit(f"нет studio-проекта: {p} — создай: vg studio new {name}")
    return p


def cmd_studio_list():
    rows = []
    for p in sorted(ROOT.iterdir()):
        if (p / "score.js").exists():
            out = list((p / "out").glob("*.mp4")) if (p / "out").is_dir() else []
            rows.append((p.name, "video" if any(o.stat().st_size > 100_000 for o in out) else "src"))
    print(f"studio-проектов: {len(rows)}")
    for n, st in rows:
        print(f"  {n:<20} {st}")


def cmd_studio_new(name, extra=None):
    dst = ROOT / name
    if dst.exists():
        sys.exit(f"уже существует: {dst}")
    run(["node", str(STUDIO / "scripts/new-project.js"), str(dst)] + (extra or []))


def cmd_studio_song(name):
    p = studio_proj(name)
    run(["node", "song.js"], cwd=p)


def cmd_studio_render(name, rest):
    p = studio_proj(name)
    run(["node", "engine/render.js"] + rest, cwd=p)


def cmd_studio_make(name, draft=False):
    p = studio_proj(name)
    cmd_studio_song(name)
    run(["node", "engine/render.js", "video"] + (["--draft"] if draft else []), cwd=p)
    run(["node", "engine/render.js", "mux"] + (["--draft"] if draft else []), cwd=p)


def cmd_studio_outro(name):
    """Приклеивает утверждённую концовку MasterHacks к готовому studio-ролику (9:16)."""
    p = studio_proj(name)
    vids = sorted((p / "out").glob("*.mp4"), key=lambda x: x.stat().st_mtime, reverse=True)
    vids = [v for v in vids if not v.name.startswith("clip_")]
    if not vids:
        sys.exit("нет готового mp4 в out/ — сначала vg studio make")
    src = vids[0]
    out = ROOT / f"{name}-final.mp4"
    run([PY, str(APPEND), str(src), str(out)])
    print(f"готово: {out}")


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
        cmd_final(args[0], "--reels" in args)
    elif c == "make":
        cmd_make(args[0], "--reels" in args)
    elif c == "meta":
        cmd_meta(args[0])
    elif c == "new":
        cmd_new(args[0], args[2] if len(args) > 2 and args[1] == "--from" else "solarfence")
    elif c == "studio":
        if not args:
            print("vg studio new <name> [--format 9:16] [--from <demo>]\n"
                  "vg studio list\n"
                  "vg studio song <name>\n"
                  "vg studio make <name> [--draft]\n"
                  "vg studio render <name> <engine-команда> [...]\n"
                  "vg studio outro <name>")
        else:
            sub, rest = args[0], args[1:]
            if sub == "list":
                cmd_studio_list()
            elif sub == "new":
                cmd_studio_new(rest[0], rest[1:])
            elif sub == "song":
                cmd_studio_song(rest[0])
            elif sub == "make":
                cmd_studio_make(rest[0], "--draft" in rest)
            elif sub == "outro":
                cmd_studio_outro(rest[0])
            elif sub == "render":
                cmd_studio_render(rest[0], rest[1:])
            else:
                print("неизвестная studio-команда:", sub)
    elif c == "push":
        cmd_push(args[0] if args else None)
    else:
        print(__doc__)
