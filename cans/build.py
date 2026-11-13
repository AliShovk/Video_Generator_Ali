#!/usr/bin/env python3
"""«Две жестянки» — 7 сцен, светлая иллюстрация."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/cans")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG1 = "#f1f6e9"; BG2 = "#e3efd6"
INK = "#2f3a2a"; INK2 = "#5f6f56"
GRASS = "#7fae5a"; GRASS_D = "#5d8a3f"
SOIL = "#8a5a35"; SOIL_D = "#6b4327"
METAL = "#b9c0c2"; METAL_D = "#8a9295"; RUST = "#b06a3a"
WOOD = "#c19a63"; WOOD_D = "#96703f"
BUG = "#3a3f33"; RED = "#c0392b"; BLUE = "#4c8fb5"; NET = "#dfe9ef"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def bg(seed=1):
    r = random.Random(seed)
    blades = "".join(f'<path d="M {r.uniform(0,1080):.0f} {r.uniform(380,520):.0f} l {r.uniform(-8,8):.0f} -{r.uniform(14,30):.0f}" '
                     f'stroke="{GRASS_D}" stroke-width="3" opacity="0.5"/>' for _ in range(80))
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#eef7fb"/><stop offset="1" stop-color="#e9f4de"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sky)"/>'
            f'<path d="M 0 520 q 270 -30 540 0 t 540 0 l 0 1400 l -1080 0 z" fill="{GRASS}"/>'
            f'{blades}')


def soil(y=900, h=700, cls="sl"):
    r = random.Random(9)
    dots = "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(y+20,y+h):.0f}" r="{r.uniform(2,5):.0f}" '
                   f'fill="{SOIL_D}" opacity="{r.uniform(0.2,0.5):.2f}"/>' for _ in range(120))
    return (f'<g class="{cls}"><rect x="0" y="{y}" width="1080" height="{h}" fill="{SOIL}"/>'
            f'<path d="M 0 {y} q 270 -18 540 0 t 540 0" stroke="{GRASS_D}" stroke-width="14" fill="none"/>{dots}</g>')


def can(x, y, w=150, h=210, cls="cn"):
    """Жестянка: корпус, ободки, ржавчина."""
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{METAL}" stroke="{METAL_D}" stroke-width="4"/>')
    b.append(f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="{w*0.16}" fill="#cfd6d8" stroke="{METAL_D}" stroke-width="4"/>')
    b.append(f'<ellipse cx="{x+w/2}" cy="{y+6}" rx="{w/2-12}" ry="{w*0.12}" fill="#8d979a" opacity="0.6"/>')
    for k in (0.32, 0.62):
        b.append(f'<path d="M {x} {y+h*k:.0f} l {w} 0" stroke="{METAL_D}" stroke-width="6" opacity="0.8"/>')
    b.append(f'<path d="M {x+26} {y+40} q 10 40 0 80" stroke="{RUST}" stroke-width="9" opacity="0.55" fill="none"/>')
    b.append(f'<path d="M {x+w-40} {y+110} q -8 40 4 70" stroke="{RUST}" stroke-width="7" opacity="0.45" fill="none"/>')
    b.append('</g>')
    return "".join(b)


def stake(x, y, h=300, cls="stk"):
    return (f'<g class="{cls}"><path d="M {x-22} {y} l 44 0 l 0 {-h} l -44 0 z" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="4"/>'
            f'<path d="M {x} {y-h} l 0 {-40} l 0 40 l -22 40 l 0 -40 z" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="4"/>'
            f'<path d="M {x-10} {y-h*0.4} q 20 10 20 40" stroke="{WOOD_D}" stroke-width="3" fill="none" opacity="0.6"/></g>')


def bug(x, y, s=1.0, cls="bg1", col=BUG):
    b = [f'<g class="{cls}" transform="translate({x} {y}) scale({s})">']
    b.append(f'<ellipse cx="0" cy="0" rx="16" ry="9" fill="{col}"/>')
    b.append(f'<ellipse cx="-14" cy="-2" rx="7" ry="6" fill="{col}"/>')
    b.append(f'<path d="M -6 -10 q 10 -14 18 -2 M 4 -10 q 10 -12 16 0" stroke="#cfe3ef" stroke-width="3" fill="none" opacity="0.9"/>')
    b.append(f'<path d="M 6 2 l 16 4 M 6 -2 l 16 -4" stroke="{col}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def field(cx, cy, rx=260, ry=150, col=BLUE, cls="fd"):
    b = [f'<g class="{cls}">']
    for k in (1.0, 0.72, 0.45):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*k:.0f}" ry="{ry*k:.0f}" fill="none" stroke="{col}" stroke-width="4" '
                 f'stroke-dasharray="12 12" opacity="0.75"/>')
    b.append('</g>')
    return "".join(b)


def stamp(text, x, y, cls="stp", col=RED, size=90, rot=-8):
    w = len(text) * size * 0.62
    return (f'<g class="{cls}" transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-w/2}" y="{y-size*0.75}" width="{w:.0f}" height="{size*1.4:.0f}" rx="10" fill="none" stroke="{col}" stroke-width="12" opacity="0.9"/>'
            f'<text x="{x}" y="{y+size*0.32}" font-family="Nunito" font-size="{size}" font-weight="900" fill="{col}" '
            f'text-anchor="middle" letter-spacing="6">{text}</text></g>')


def label(x, y, s, size=22, cls="lb", col=INK):
    w = len(s) * size * 0.58 + 26
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="8" fill="#ffffff" opacity="0.92"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(1)]
    b.append(stake(540, 1050, 430, "st1"))
    b.append(can(250, 800, 230, 320, "c1"))
    b.append(can(600, 800, 230, 320, "c1b"))
    b.append(bug(180, 560, 1.2, "b1a"))
    b.append(bug(900, 520, 1.1, "b1b"))
    b.append(bug(760, 420, 0.9, "b1c"))
    b.append(t(60, 200, "ДВЕ ЖЕСТЯНКИ", 52, INK))
    b.append(t(60, 268, "и комары не подлетают?", 40, GRASS_D))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg(2), soil(900, 700, "sl2")]
    b.append(stake(540, 1060, 430, "st2"))
    b.append(can(220, 900, 240, 330, "c2"))
    b.append(can(620, 900, 240, 330, "c2b"))
    # камни
    for i, px in enumerate((240, 300, 360, 640, 700, 760)):
        b.append(f'<ellipse cx="{px}" cy="1180" rx="26" ry="16" fill="#a8a8a0" stroke="#8a8a82" stroke-width="2"/>')
    b.append(label(120, 700, "ЖЕСТЯНКИ В ЗЕМЛЮ", 20, "lb1"))
    b.append(label(680, 700, "КОЛЫШЕК МЕЖДУ", 20, "lb2"))
    b.append(t(60, 220, "КАК ДЕЛАЮТ", 44, INK))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(3)]
    b.append(field(540, 900, 400, 250, BLUE, "fd3"))
    b.append(stake(540, 1000, 280, "st3"))
    b.append(can(240, 820, 220, 300, "c3"))
    b.append(can(620, 820, 220, 300, "c3b"))
    b.append(bug(150, 700, 1.3, "b3a"))
    b.append(bug(930, 760, 1.2, "b3b"))
    b.append(f'<path d="M 200 720 q 80 -40 70 -120" stroke="{RED}" stroke-width="5" fill="none" stroke-dasharray="10 8"/>')
    b.append(label(120, 560, "«ЗАЩИТНОЕ ПОЛЕ»", 22, "lb3", RED))
    b.append(t(60, 220, "ЧТО ОБЕЩАЮТ", 44, INK))
    b.append(t(60, 286, "насекомые обходят грядку", 26, INK2, w=700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg(4)]
    b.append(field(540, 880, 320, 200, "#9aa8ad", "fd4"))
    b.append(can(230, 760, 230, 320, "c4"))
    b.append(can(620, 760, 230, 320, "c4b"))
    b.append(stamp("МИФ", 540, 900, "stp4", RED, 130, -10))
    b.append(t(60, 240, "ПРОВЕРЯЕМ", 44, INK))
    b.append(t(64, 306, "никакого поля нет", 30, RED, w=800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg(5)]
    # два примера: заряд и магнит
    b.append(f'<circle cx="300" cy="760" r="90" fill="#f2d36a" stroke="#c9a53a" stroke-width="4"/>')
    b.append(t(300, 786, "+", 70, "#6b4c11", "middle", 900))
    for k in (130, 180, 230):
        b.append(f'<circle cx="300" cy="760" r="{k}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="10 12" opacity="0.7"/>')
    b.append(t(300, 660, "ЭЛЕКТРИЧЕСКОЕ", 20, BLUE, "middle", 800))
    b.append(f'<rect x="640" y="690" width="130" height="140" rx="8" fill="{RED}" stroke="#8c2f22" stroke-width="4"/>')
    b.append(f'<rect x="640" y="690" width="65" height="140" rx="8" fill="#4a6a9a" stroke="#33507a" stroke-width="4"/>')
    b.append(t(705, 880, "МАГНИТНОЕ", 20, "#4a6a9a", "middle", 800))
    for k in (170, 220):
        b.append(f'<path d="M {705-k} 760 q {k} -110 {2*k} 0" fill="none" stroke="#4a6a9a" stroke-width="3" stroke-dasharray="10 12" opacity="0.7"/>')
    b.append(t(60, 220, "ДЛЯ ПОЛЯ НУЖЕН ЗАРЯД", 34, INK))
    b.append(t(60, 276, "или магнит. У жестянки — ни того, ни другого.", 22, INK2, w=700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(6)]
    b.append(f'<circle cx="540" cy="900" r="290" fill="#f6ddc6" stroke="#d9b391" stroke-width="4"/>')
    b.append(f'<circle cx="470" cy="760" r="18" fill="{INK}"/><circle cx="610" cy="760" r="18" fill="{INK}"/>')
    b.append(f'<path d="M 470 880 q 70 46 140 0" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    b.append(bug(760, 700, 1.4, "b6a"))
    b.append(bug(320, 660, 1.2, "b6b"))
    b.append(f'<path d="M 760 760 q -60 60 -140 60" stroke="{RED}" stroke-width="4" fill="none" stroke-dasharray="10 8"/>')
    b.append(t(60, 240, "КОМАРАМ НУЖЕН ЗАПАХ И ТЕПЛО", 30, INK))
    b.append(t(60, 300, "жёстянка им не мешает", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg(7)]
    # сетка
    b.append(f'<g class="net"><rect x="120" y="620" width="840" height="520" rx="16" fill="{NET}" opacity="0.55" stroke="#9fb2bc" stroke-width="4"/>')
    for i in range(14):
        b.append(f'<path d="M {140+i*60} 640 l 0 480" stroke="#aebfc8" stroke-width="2" opacity="0.8"/>')
    for k in range(8):
        b.append(f'<path d="M 140 {650+k*60} l 800 0" stroke="#aebfc8" stroke-width="2" opacity="0.8"/>')
    b.append('</g>')
    b.append(t(60, 250, "РАБОТАЕТ ДРУГОЕ", 44, INK))
    b.append(t(60, 320, "сетка", 34, GRASS_D, w=800))
    b.append(t(60, 375, "сухо · тень · репеллент", 26, INK2, w=700))
    b.append(label(140, 1220, "КОЛЫШЕК — ПРОСТО КОЛЫШЕК", 22, "lb7"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7]
ANIM = [
    'tl.fromTo(".st1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".c1", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.3);'
    'tl.fromTo(".c1b", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.5);'
    'tl.fromTo(".b1a, .b1b, .b1c", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.7);'
    'tl.to(".b1a, .b1b, .b1c", {x:20, y:-14, duration:1.6, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".stk", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".c2, .c2b", {opacity:0, y:-40}, {opacity:1, y:0, duration:0.7, stagger:0.2}, 0.3);'
    'tl.fromTo(".lb1, .lb2", {opacity:0}, {opacity:1, duration:0.4, stagger:0.2}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".fd3", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.8}, 0.1);'
    'tl.fromTo(".c3, .c3b, .st3", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.3);'
    'tl.fromTo(".b3a, .b3b", {opacity:0}, {opacity:1, duration:0.5, stagger:0.2}, 0.7);'
    'tl.to(".b3a, .b3b", {x:-18, duration:1.4, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl, .lb3", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".c4, .c4b", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.1);'
    'tl.fromTo(".fd4", {opacity:0}, {opacity:0.5, duration:0.6}, 0.3);'
    'tl.fromTo(".stp4", {opacity:0, scale:1.6}, {opacity:1, scale:1, duration:0.4, ease:"power4.out"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);'
    'tl.to(".b6a, .b6b", {x:16, y:-10, duration:1.4, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.5);',
    'tl.fromTo(".net", {opacity:0, y:16}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".hl, .lb7", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG1}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    {anim}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, fn in enumerate(SCENES):
        sid = f"s{i+1}"
        st, dur = B[i]
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur, ANIM[i]), encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("ok", TOTAL, B)


if __name__ == "__main__":
    build()
