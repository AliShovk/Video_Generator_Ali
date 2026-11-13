#!/usr/bin/env python3
"""ENGINEERING EXPLAINER GENERATOR — оркестратор конвейера.

Использование:
    python3 pipeline.py briefs/chernobyl.json [--skip-render]

Артефакты в out/<slug>/:
    research.md, engineering.md, script.md, storyboard.json, factcheck.json,
    assets/ (render/), voice.wav, subtitles.srt, final.mp4, sources.md, manifest.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import agents
import visual
import voice as vc

ROOT = Path(__file__).resolve().parent
HF = ROOT.parent / "node_modules" / "hyperframes" / "bin" / "hyperframes.mjs"


def log(stage: str, msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {stage:<12} {msg}", flush=True)


def render(project: Path) -> Path:
    out = project / "renders"
    out.mkdir(exist_ok=True)
    mp4 = out / "explainer.mp4"
    log("render", "HyperFrames: сборка кадров")
    subprocess.run(["node", str(HF), "render", "-o", str(mp4), "--quality", "high"],
                   cwd=project, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return mp4


def mux(video: Path, audio: Path, srt: Path, out: Path) -> Path:
    final = out / "final.mp4"
    log("edit", "FFmpeg: видео + голос + субтитры")
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(video), "-i", str(audio), "-i", str(srt),
                    "-map", "0:v", "-map", "1:a", "-map", "2:s",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=9",
                    "-c:s", "mov_text", "-metadata:s:s:0", "language=rus",
                    str(final)], check=True)
    return final


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--skip-render", action="store_true")
    args = ap.parse_args()

    brief = agents.Brief.load(Path(args.brief))
    out = ROOT / "out" / brief.slug
    out.mkdir(parents=True, exist_ok=True)
    assets = out / "assets"
    assets.mkdir(exist_ok=True)

    log("research", f"{brief.slug}: {len(brief.facts)} фактов")
    (out / "research.md").write_text(agents.research(brief), encoding="utf-8")

    log("engineering", "принцип, нагрузки, механизмы")
    (out / "engineering.md").write_text(agents.engineering(brief), encoding="utf-8")

    log("script", "текст диктора")
    script_md, lines = agents.script(brief)
    (out / "script.md").write_text(script_md, encoding="utf-8")

    log("storyboard", "сцены и ракурсы")
    scenes = agents.storyboard(brief, lines)
    (out / "storyboard.json").write_text(json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8")

    log("factcheck", "сверка чисел с research.md")
    fc = agents.factcheck(brief, lines, scenes)
    (out / "factcheck.json").write_text(json.dumps(fc, ensure_ascii=False, indent=2), encoding="utf-8")
    if not fc["ok"]:
        log("factcheck", "ОТКАЗ: " + "; ".join(f"{p['scene']}:{p['reason']}" for p in fc["problems"]))
        return 2
    log("factcheck", f"ок, {fc['duration_s']} с, чисел: {len(fc['checked_numbers'])}")

    log("visual", "SVG-слои и сцены")
    project = visual.build_project(out, scenes, brief.dims)
    shutil.copytree(project / "compositions", assets / "compositions", dirs_exist_ok=True)
    (assets / "storyboard.json").write_text(json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8")

    log("voice", "Piper: озвучка по сценам")
    wav, timing = vc.build_voice(scenes, out)
    srt = vc.build_srt(timing, out)

    if args.skip_render:
        log("render", "пропущено (--skip-render)")
        final = None
    else:
        mp4 = render(project)
        final = mux(mp4, wav, srt, out)
        log("done", f"{final} · {final.stat().st_size/1e6:.1f} МБ")

    (out / "sources.md").write_text(
        "# Sources\n\n" + "\n".join(f"- {s}" for s in brief.sources) +
        "\n\n## Проверенные утверждения\n\n" +
        "\n".join(f"- {f.claim} — {f.source}" for f in brief.facts) + "\n", encoding="utf-8")

    manifest = {
        "slug": brief.slug,
        "artifacts": sorted(p.name for p in out.glob("*") if p.is_file()),
        "duration_s": fc["duration_s"],
        "scenes": len(scenes),
        "voice": "piper",
        "renderer": "hyperframes",
        "final": str(final) if final else None,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    log("manifest", ", ".join(manifest["artifacts"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
