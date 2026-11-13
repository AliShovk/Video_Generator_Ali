#!/usr/bin/env python3
"""Визуальный агент: техническая 2D-инфографика 1080×1920 (SVG + GSAP)."""
from __future__ import annotations

import math
from pathlib import Path

BG = "#050b12"
INK = "#e8eef4"
CYAN = "#6fd3f2"
ORANGE = "#ff7a1a"
STEEL1, STEEL2, STEEL3 = "#dfe9f2", "#7f95a4", "#2d3b46"
MUTED = "#7f93a3"

DEFS = f"""
<defs>
  <linearGradient id="steel" x1="0" y1="0" x2="0.25" y2="1">
    <stop offset="0" stop-color="{STEEL1}"/><stop offset="0.45" stop-color="{STEEL2}"/><stop offset="1" stop-color="{STEEL3}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity="0.95"/>
  </linearGradient>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{ORANGE}" stop-opacity="0.55"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="grid" width="90" height="90" patternUnits="userSpaceOnUse">
    <path d="M 90 0 L 0 0 0 90" fill="none" stroke="#0e1e2a" stroke-width="1"/>
  </pattern>
  <filter id="soft"><feGaussianBlur stdDeviation="16"/></filter>
</defs>
"""


def svg(body: str) -> str:
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            f'{DEFS}<rect width="1080" height="1920" fill="{BG}"/>'
            f'<rect width="1080" height="1920" fill="url(#grid)"/>{body}</svg>')


def t(x, y, s, size=28, color=INK, anchor="start", mono=True, op=1.0, weight="500"):
    fam = "JetBrains Mono, monospace" if mono else "Inter, sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="1.5" text-anchor="{anchor}" opacity="{op}">{s}</text>')


def dim_h(x1, x2, y, label):
    return (f'<g class="dim"><line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{CYAN}" stroke-width="2"/>'
            f'<line x1="{x1}" y1="{y-14}" x2="{x1}" y2="{y+14}" stroke="{CYAN}" stroke-width="2"/>'
            f'<line x1="{x2}" y1="{y-14}" x2="{x2}" y2="{y+14}" stroke="{CYAN}" stroke-width="2"/>'
            f'<polygon points="{x1+8},{y} {x1+26},{y-5} {x1+26},{y+5}" fill="{CYAN}"/>'
            f'<polygon points="{x2-8},{y} {x2-26},{y-5} {x2-26},{y+5}" fill="{CYAN}"/>'
            + t((x1 + x2) / 2, y - 20, label, 30, CYAN, "middle") + '</g>')


def dim_v(y1, y2, x, label):
    return (f'<g class="dim"><line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{CYAN}" stroke-width="2"/>'
            f'<line x1="{x-14}" y1="{y1}" x2="{x+14}" y2="{y1}" stroke="{CYAN}" stroke-width="2"/>'
            f'<line x1="{x-14}" y1="{y2}" x2="{x+14}" y2="{y2}" stroke="{CYAN}" stroke-width="2"/>'
            f'<g transform="translate({x+36} {(y1+y2)/2}) rotate(90)">{t(0, 0, label, 30, CYAN, "middle")}</g></g>')


def arch(cx, base, span, height, thick=54, ribs=26, opacity=1.0, ident=""):
    rx, ry = span / 2, height
    x0, x1 = cx - rx, cx + rx
    irx, iry = rx - thick, ry - thick * 0.92
    body = (f"M {x0} {base} A {rx} {ry} 0 0 1 {x1} {base} "
            f"L {cx+irx} {base} A {irx} {iry} 0 0 0 {cx-irx} {base} Z")
    out = [f'<g id="{ident}" opacity="{opacity}">',
           f'<path d="{body}" fill="url(#steel)"/>']
    for i in range(1, ribs):
        a = math.pi * i / ribs
        ox, oy = cx - rx * math.cos(a), base - ry * math.sin(a)
        ix, iy = cx - irx * math.cos(a), base - iry * math.sin(a)
        out.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#101820" stroke-width="3" opacity="0.55"/>')
    for i in range(ribs):
        a1 = math.pi * i / ribs
        a2 = math.pi * (i + 0.5) / ribs
        out.append(f'<line x1="{cx-rx*math.cos(a1):.1f}" y1="{base-ry*math.sin(a1):.1f}" '
                   f'x2="{cx-irx*math.cos(a2):.1f}" y2="{base-iry*math.sin(a2):.1f}" stroke="#1b2732" stroke-width="2" opacity="0.45"/>')
    out.append(f'<path d="M {x0} {base} A {rx} {ry} 0 0 1 {x1} {base}" fill="none" stroke="#eaf4fb" stroke-width="2.5" opacity="0.6"/>')
    out.append('</g>')
    return "".join(out)


def block(x, y, w=300, h=200):
    return (f'<g><rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#1a232b" stroke="#3c4a55" stroke-width="3"/>'
            f'<rect x="{x+w*0.12}" y="{y-h-52}" width="{w*0.3}" height="52" fill="#232d35"/>'
            f'<rect x="{x+w*0.55}" y="{y-h-30}" width="{w*0.24}" height="30" fill="#232d35"/>'
            f'<rect x="{x+18}" y="{y-h+22}" width="{w-36}" height="10" fill="{ORANGE}" opacity="0.35"/></g>')


def ground(y):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="#080f14"/>'
            f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#31414c" stroke-width="3"/>')


def scene_hero(d: dict) -> str:
    b = [ground(1330), block(150, 1330, 280, 180)]
    b.append(f'<ellipse cx="540" cy="1310" rx="500" ry="60" fill="#000" opacity="0.5" filter="url(#soft)"/>')
    b.append(f'<g id="hero-arch">{arch(560, 1330, 740, 610, 56, 28)}</g>')
    b.append(f'<ellipse cx="560" cy="1080" rx="290" ry="240" fill="url(#glow)" opacity="0.25" filter="url(#soft)"/>')
    for x in (250, 860):
        b.append(f'<rect x="{x}" y="1300" width="70" height="26" rx="4" fill="#2b3944"/>'
                 f'<circle cx="{x+14}" cy="1328" r="9" fill="#101820"/><circle cx="{x+56}" cy="1328" r="9" fill="#101820"/>')
    return "".join(b)


def scene_section(d: dict) -> str:
    b = [ground(1360)]
    b.append(arch(540, 1360, 740, 610, 54, 22, ident="sec-arch"))
    # стрелки нагрузки по дуге
    for i, (x, y) in enumerate([(230, 1340), (340, 1060), (540, 850), (740, 1060), (850, 1340)]):
        b.append(f'<g class="load"><line x1="{x}" y1="{y}" x2="{x}" y2="{y+90}" stroke="{ORANGE}" stroke-width="5"/>'
                 f'<polygon points="{x},{y+110} {x-10},{y+86} {x+10},{y+86}" fill="{ORANGE}"/></g>')
    b.append(t(540, 720, "НАГРУЗКА → КАРКАС → ОПОРЫ", 26, MUTED, "middle"))
    return "".join(b)


def scene_dimensions(d: dict) -> str:
    span = d.get("span", 257); height = d.get("height", 108); length = d.get("length", 162)
    b = [ground(1270)]
    b.append(arch(540, 1270, 760, 620, 58, 26, ident="dim-arch"))
    b.append(dim_h(160, 920, 1160, f"{span} м — пролёт"))
    b.append(dim_v(1270, 650, 990, f"{height} м"))
    b.append(t(540, 1110, f"длина — {length} м", 26, MUTED, "middle"))
    return "".join(b)


def scene_detail(d: dict) -> str:
    b = [f'<rect x="0" y="1300" width="1080" height="620" fill="#0d1317"/>',
         f'<rect x="0" y="1290" width="1080" height="16" fill="{STEEL2}"/>']
    for x in range(20, 1080, 110):
        b.append(f'<rect x="{x}" y="1280" width="58" height="10" fill="#93a4b1" opacity="0.7"/>')
    b.append(f'<rect x="210" y="1190" width="660" height="76" rx="6" fill="url(#steel)" stroke="#c8d8e4" stroke-width="3"/>')
    b.append('<g id="jacks">')
    for x in (330, 540, 750):
        b.append(f'<rect x="{x-62}" y="1266" width="124" height="110" fill="#1d2a33" stroke="{CYAN}" stroke-width="3"/>')
        b.append(f'<rect class="piston" x="{x-12}" y="1190" width="24" height="80" rx="6" fill="{ORANGE}"/>')
        b.append(f'<circle cx="{x}" cy="1320" r="6" fill="{CYAN}"/>')
    b.append('</g>')
    b.append(f'<path id="hyd" d="M 392 1376 L 688 1376" stroke="{CYAN}" stroke-width="18" fill="none" stroke-linecap="round" opacity="0.6"/>')
    b.append(t(540, 1105, "224 ДОМКРАТА · СИНХРОННО", 30, CYAN, "middle"))
    return "".join(b)


def scene_move(d: dict) -> str:
    b = [ground(1320), block(780, 1320, 250, 180)]
    b.append(f'<rect x="0" y="1306" width="1080" height="18" fill="{STEEL2}"/>')
    b.append(f'<g id="move-arch">{arch(300, 1320, 500, 400, 42, 20)}</g>')
    for i in range(4):
        b.append(f'<line x1="{60+i*14}" y1="{1240+i*40}" x2="{190+i*10}" y2="{1240+i*40}" stroke="{CYAN}" stroke-width="5" opacity="0.35"/>')
    b.append(t(540, 1050, "327 МЕТРОВ", 34, INK, "middle"))
    return "".join(b)


def scene_note(d: dict) -> str:
    b = [f'<rect width="1080" height="1920" fill="#070d12"/>']
    b.append(f'<rect x="120" y="560" width="840" height="700" fill="#0e1a22" stroke="#2a3d4a" stroke-width="4"/>')
    for i in range(0, 9):
        b.append(f'<line x1="{120+i*105}" y1="560" x2="{120+i*105}" y2="1260" stroke="#16242e" stroke-width="2"/>')
    b.append(f'<path id="crack" d="M 470 640 L 560 760 L 500 860 L 610 980" stroke="{ORANGE}" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="700" stroke-dashoffset="700"/>')
    b.append(f'<circle id="warn" cx="620" cy="700" r="46" fill="{ORANGE}" opacity="0.9"/>')
    b.append(t(620, 720, "!", 54, "#08111a", "middle", weight="700"))
    b.append(t(540, 1420, "ФЕВРАЛЬ 2025", 40, ORANGE, "middle"))
    return "".join(b)


BUILDERS = {"hero": scene_hero, "section": scene_section, "dimensions": scene_dimensions,
            "detail": scene_detail, "move": scene_move, "note": scene_note}

CAPTION = {"hero": "Построили в стороне — и передвинули целиком",
           "section": "Нагрузка идёт по каркасу к опорам",
           "dimensions": "Габариты арки",
           "detail": "Гидравлика толкает опоры по рельсам",
           "move": "Перемещение на 327 метров",
           "note": "Оболочка повреждена, восстановление не завершено"}

CHIP = {"hero": "Чернобыль · 2016", "section": "Принцип", "dimensions": "Размеры",
        "detail": "Механизм", "move": "Перемещение", "note": "2025"}

ANIM = {
    "hero": 'tl.fromTo("#hero-arch",{y:70,opacity:0},{y:0,opacity:1,duration:1.2,ease:"power2.out"},0.2);',
    "section": 'tl.fromTo(".load",{opacity:0,y:-20},{opacity:1,y:0,duration:0.5,stagger:0.35},0.6);',
    "dimensions": 'tl.fromTo(".dim",{opacity:0},{opacity:1,duration:0.5,stagger:0.4},0.5);',
    "detail": 'tl.to(".piston",{y:-12,duration:0.45,yoyo:true,repeat:7,stagger:0.12,ease:"sine.inOut"},0.4);',
    "move": 'tl.fromTo("#move-arch",{x:0},{x:400,duration:8.2,ease:"power1.inOut"},0.5);',
    "note": 'tl.to("#crack",{strokeDashoffset:0,duration:1.4,ease:"power2.out"},0.5);tl.to("#warn",{opacity:0.35,duration:0.5,yoyo:true,repeat:6},1.2);',
}


def page(scene: dict, index: int) -> str:
    kind = scene["kind"]
    dur = scene["duration"]
    body = svg(BUILDERS[kind](scene.get("dims", {})))
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{BG}; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
    .chip {{ position:absolute; left:48px; top:118px; border:1px solid rgba(111,211,242,.45);
      color:{CYAN}; font:500 27px/1 "JetBrains Mono",monospace; letter-spacing:.18em;
      text-transform:uppercase; padding:11px 16px; background:rgba(6,12,18,.65); }}
    .foot {{ position:absolute; left:48px; right:48px; bottom:420px; font:700 48px/1.12 "Oswald",sans-serif;
      text-transform:uppercase; color:{INK}; text-shadow:0 4px 18px rgba(0,0,0,.85); }}
    .foot::before {{ content:""; display:block; width:70px; height:4px; background:{ORANGE}; margin-bottom:14px; }}
  </style>
  <div id="root" data-composition-id="{scene['id']}" data-width="1080" data-height="1920">
    <div class="clip" id="{scene['id']}-clip" data-start="0" data-duration="{dur}">
      <div id="{scene['id']}-in">
        {body}
        <div class="chip">{CHIP[kind]}</div>
        <div class="foot">{CAPTION[kind]}</div>
      </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{scene['id']} .world", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {dur}, ease: "none" }}, 0);
    {ANIM[kind]}
    window.__timelines["{scene['id']}"] = tl;
  </script>
</template>
"""


def build_project(out: Path, scenes: list[dict], dims: dict) -> Path:
    proj = out / "render"
    comps = proj / "compositions"
    comps.mkdir(parents=True, exist_ok=True)
    start = 0
    hosts = []
    for sc in scenes:
        sc = dict(sc)
        sc["dims"] = dims
        (comps / f"{sc['id']}.html").write_text(page(sc, 0), encoding="utf-8")
        hosts.append(f'<div id="{sc["id"]}" class="scene" data-composition-id="{sc["id"]}" '
                     f'data-composition-src="compositions/{sc["id"]}.html" data-start="{start}" '
                     f'data-duration="{sc["duration"]}" data-track-index="{len(hosts)+1}" '
                     f'data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
        start += sc["duration"]
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{BG}}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
</body></html>"""
    (proj / "index.html").write_text(html, encoding="utf-8")
    (proj / "hyperframes.json").write_text(Path("/root/video-gen/fireplace/hyperframes.json").read_text(encoding="utf-8"), encoding="utf-8")
    return proj
