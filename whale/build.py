#!/usr/bin/env python3
"""«Кит в Тайнане» — 8 сцен, комикс-поп."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/whale")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

PAPER = "#fdf3dc"
INK = "#141414"
CYAN = "#1fb6c9"
MAG = "#e6397f"
YEL = "#ffcf3f"
RED = "#e63946"
GREY = "#8fa3b0"
WHALE = "#4a5b6b"


def t(x, y, s, size=48, col=INK, anchor="start", w=900, ls=0, cls="hl", rot=0, stroke=None):
    st = f' stroke="{stroke}" stroke-width="12" paint-order="stroke" stroke-linejoin="round"' if stroke else ""
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}"{st}{tr}>{s}</text>')


def burst(cx, cy, r, pts=14, col=YEL, cls="burst", inner=0.62):
    p = []
    for i in range(pts * 2):
        a = math.pi * i / pts
        rr = r if i % 2 == 0 else r * inner
        p.append(f"{cx + rr*math.cos(a):.0f},{cy + rr*math.sin(a):.0f}")
    return (f'<g class="{cls}"><polygon points="{" ".join(p)}" fill="{col}" stroke="{INK}" stroke-width="8"/>'
            f'<polygon points="{" ".join(p)}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.35" transform="rotate(6 {cx} {cy})"/></g>')


def halftone(cx, cy, r, col=INK, op=0.25, n=9):
    out = [f'<g class="ht" opacity="{op}">']
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x, y = cx + i * 34, cy + j * 34
            d = math.hypot(x - cx, y - cy)
            if 0 < d < r:
                out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{max(1.5, 7*(1-d/r)):.1f}" fill="{col}"/>')
    out.append('</g>')
    return "".join(out)


def splash(cx, cy, r, col=RED, cls="spl", n=12):
    rnd = random.Random(int(cx + cy))
    p = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r * (1 + rnd.uniform(-0.25, 0.35)) if i % 2 == 0 else r * 0.55
        p.append(f"{cx + rr*math.cos(a):.0f},{cy + rr*math.sin(a):.0f}")
    return f'<g class="{cls}"><polygon points="{" ".join(p)}" fill="{col}"/></g>'


def whale(x, y, s=1.0, cls="wh", col=WHALE, belly=True, blown=False):
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x-190*s} {y} q 20 -120 190 -120 q 170 0 190 120 q 20 110 -190 110 q -210 0 -190 -110 z" fill="{col}" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<path d="M {x-190*s} {y} q -90 -60 -120 -130 q 90 20 120 90" fill="{col}" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<path d="M {x-180*s} {y+30*s} q 180 80 360 0" stroke="{INK}" stroke-width="6" fill="none" opacity="0.5"/>')
    if belly:
        b.append(f'<path d="M {x-150*s} {y+40*s} q 150 60 300 0 q -40 70 -150 70 q -110 0 -150 -70 z" fill="#dfe9ee" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<circle cx="{x-110*s}" cy="{y-40*s}" r="{10*s}" fill="{INK}"/>')
    b.append(f'<path d="M {x-150*s} {y-10*s} q 30 16 60 0" stroke="{INK}" stroke-width="5" fill="none"/>')
    return "".join(b) + '</g>'


def truck(x, y, s=1.0, cls="tr"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{300*s}" height="{120*s}" rx="10" fill="{CYAN}" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="{x+300*s}" y="{y+30*s}" width="{110*s}" height="{90*s}" rx="10" fill="{MAG}" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="{x+314*s}" y="{y+46*s}" width="{70*s}" height="{40*s}" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{x+70*s}" cy="{y+140*s}" r="{34*s}" fill="{INK}"/><circle cx="{x+70*s}" cy="{y+140*s}" r="{13*s}" fill="{GREY}"/>'
            f'<circle cx="{x+330*s}" cy="{y+140*s}" r="{34*s}" fill="{INK}"/><circle cx="{x+330*s}" cy="{y+140*s}" r="{13*s}" fill="{GREY}"/></g>')


def person(x, y, s=1.0, col=INK, shirt=CYAN, cls="p", shock=False):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x-18*s}" y="{y-90*s}" width="{36*s}" height="{80*s}" rx="{14*s}" fill="{shirt}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<rect x="{x-16*s}" y="{y-14*s}" width="{12*s}" height="{46*s}" fill="{INK}"/>')
    b.append(f'<rect x="{x+4*s}" y="{y-14*s}" width="{12*s}" height="{46*s}" fill="{INK}"/>')
    b.append(f'<circle cx="{x}" cy="{y-120*s}" r="{26*s}" fill="#f6d6b8" stroke="{INK}" stroke-width="6"/>')
    if shock:
        b.append(f'<circle cx="{x-9*s}" cy="{y-126*s}" r="{4.5*s}" fill="{INK}"/>')
        b.append(f'<circle cx="{x+9*s}" cy="{y-126*s}" r="{4.5*s}" fill="{INK}"/>')
        b.append(f'<ellipse cx="{x}" cy="{y-108*s}" rx="{7*s}" ry="{9*s}" fill="{INK}"/>')
        b.append(f'<path d="M {x-30*s} {y-150*s} l -16 -22 M {x+30*s} {y-150*s} l 16 -22" stroke="{INK}" stroke-width="5"/>')
    else:
        b.append(f'<circle cx="{x-8*s}" cy="{y-126*s}" r="{4*s}" fill="{INK}"/>')
        b.append(f'<circle cx="{x+8*s}" cy="{y-126*s}" r="{4*s}" fill="{INK}"/>')
        b.append(f'<path d="M {x-8*s} {y-110*s} q {8*s} {6*s} {16*s} 0" stroke="{INK}" stroke-width="4" fill="none"/>')
    b.append('</g>')
    return "".join(b)


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', halftone(860, 380, 420, INK, 0.12)]
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="none" stroke="{INK}" stroke-width="16"/>')
    b.append(burst(760, 380, 260, 16, YEL, "b1"))
    b.append(t(760, 350, "50", 130, INK, "middle", 900))
    b.append(t(760, 430, "ТОНН", 56, INK, "middle", 900))
    b.append(truck(280, 1210, 1.05, "tr1"))
    b.append(whale(450, 1150, 1.25, "wh1"))
    b.append(t(60, 640, "КИТ", 100, INK, ls=2))
    b.append(t(60, 740, "ВЗОРВАЛСЯ", 100, RED, ls=1))
    b.append(t(60, 820, "на улице города", 32, INK, w=700))
    b.append(t(60, 1700, "Тайнань · 2004", 30, INK, w=800))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{CYAN}"/>', halftone(240, 1500, 380, INK, 0.12)]
    b.append(f'<rect x="60" y="420" width="960" height="1060" fill="{PAPER}" stroke="{INK}" stroke-width="12"/>')
    # кран
    b.append(f'<rect x="700" y="470" width="26" height="620" fill="{YEL}" stroke="{INK}" stroke-width="7"/>')
    b.append(f'<rect x="560" y="470" width="300" height="24" fill="{YEL}" stroke="{INK}" stroke-width="7"/>')
    b.append(f'<path d="M 600 494 l 0 160" stroke="{INK}" stroke-width="6"/>')
    b.append(whale(600, 780, 1.0, "wh2"))
    b.append(truck(330, 1120, 0.95, "tr2"))
    b.append(t(540, 360, "ГРУЗЯТ НА ГРУЗОВИК", 46, INK, "middle", 900))
    b.append(t(540, 1560, "ТАЙВАНЬ · 2004", 34, PAPER, "middle", 900, ls=2))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{YEL}"/>']
    for i, (x, w, h, c) in enumerate(((60, 240, 520, MAG), (330, 220, 420, CYAN), (580, 260, 560, MAG), (870, 180, 380, CYAN))):
        b.append(f'<rect x="{x}" y="{1150-h}" width="{w}" height="{h}" fill="{c}" stroke="{INK}" stroke-width="8"/>')
        for k in range(3):
            b.append(f'<rect x="{x+30}" y="{1150-h+50+k*70}" width="{w-60}" height="34" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="0" y="1150" width="1080" height="770" fill="{GREY}" stroke="{INK}" stroke-width="10"/>')
    b.append(f'<path d="M 60 1230 l 960 0" stroke="{PAPER}" stroke-width="8" stroke-dasharray="40 34"/>')
    b.append(truck(300, 1080, 1.0, "tr3"))
    b.append(whale(560, 1010, 1.35, "wh3"))
    b.append(person(120, 1300, 1.0, INK, CYAN, "p3a", True))
    b.append(person(940, 1300, 1.0, INK, MAG, "p3b", True))
    b.append(t(60, 240, "ЧЕРЕЗ ЦЕНТР", 64, INK, ls=1))
    b.append(t(60, 320, "ТАЙНАНЯ", 64, RED, ls=1))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{MAG}"/>']
    b.append(f'<circle cx="540" cy="1000" r="460" fill="{PAPER}" stroke="{INK}" stroke-width="12"/>')
    b.append(whale(540, 1000, 2.0, "wh4"))
    # стрелки давления
    for i, (x, y, a) in enumerate(((180, 760, -30), (900, 760, 30), (200, 1200, 30), (880, 1200, -30))):
        b.append(f'<g class="ar{i}"><path d="M {x} {y} l {60 if x<540 else -60} {30 if y<1000 else -30}" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>'
                 f'<path d="M {x+60 if x<540 else x-60} {y+30 if y<1000 else y-30} l {-4 if x<540 else 4} {-26}" stroke="{RED}" stroke-width="10"/></g>')
    b.append(t(540, 260, "ДАВЛЕНИЕ", 74, PAPER, "middle", 900, ls=2))
    b.append(t(540, 340, "как в мяче", 30, INK, "middle", 800))
    b.append(t(540, 1640, "разложение + жара", 34, INK, "middle", 800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{YEL}"/>']
    b.append(splash(540, 900, 470, RED, "sp1", 14))
    b.append(burst(540, 900, 330, 18, YEL, "b5"))
    b.append(t(540, 870, "БАМ!", 150, RED, "middle", 900, rot=-6))
    b.append(t(540, 960, "не шутка", 30, INK, "middle", 800))
    # брызги
    for i, (x, y, r) in enumerate(((150, 520, 60), (900, 480, 46), (200, 1400, 54), (880, 1440, 70), (540, 300, 40))):
        b.append(f'<g class="d{i}">{splash(x, y, r, MAG, "sp", 10)}</g>')
    b.append(t(60, 220, "ВНУТРЕННОСТИ", 40, INK))
    b.append(t(60, 1720, "по машинам и людям", 30, INK, w=800))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', halftone(540, 960, 460, RED, 0.18)]
    b.append(f'<rect x="60" y="380" width="960" height="1160" fill="{PAPER}" stroke="{INK}" stroke-width="12"/>')
    b.append(person(300, 1300, 1.6, INK, CYAN, "p6a", True))
    b.append(person(760, 1300, 1.6, INK, MAG, "p6b", True))
    b.append(f'<path d="M 200 1180 q 40 -40 80 0 M 700 1180 q 40 -40 80 0" stroke="{RED}" stroke-width="8" fill="none"/>')
    b.append(t(540, 800, "ПОГИБШИХ", 76, INK, "middle", 900))
    b.append(t(540, 890, "НЕТ", 96, RED, "middle", 900, ls=6))
    b.append(t(540, 1640, "обошлось", 30, INK, "middle", 800))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{CYAN}"/>']
    b.append(f'<rect x="0" y="1120" width="1080" height="800" fill="{GREY}" stroke="{INK}" stroke-width="10"/>')
    b.append(f'<path d="M 120 1200 q 200 -30 400 0 q 200 30 400 0" stroke="{PAPER}" stroke-width="10" fill="none"/>')
    # мойщики
    b.append(person(260, 1180, 1.35, INK, YEL, "p7a"))
    b.append(person(800, 1180, 1.35, INK, YEL, "p7b"))
    b.append(f'<path class="hose" d="M 330 1120 q 120 80 220 30" stroke="{MAG}" stroke-width="12" fill="none"/>')
    b.append(f'<path class="hose2" d="M 700 1120 q -100 70 -200 30" stroke="{MAG}" stroke-width="12" fill="none"/>')
    b.append(t(540, 260, "ОТМЫВАЛИ", 76, PAPER, "middle", 900))
    b.append(t(540, 350, "СУТКИ", 96, INK, "middle", 900, ls=4))
    b.append(t(540, 1660, "кварталы целиком", 30, PAPER, "middle", 800))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', halftone(540, 900, 420, INK, 0.1)]
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="none" stroke="{INK}" stroke-width="16"/>')
    # три иконки
    for i, (cx, col, label) in enumerate(((230, YEL, "ЖАРА"), (540, CYAN, "ГАЗ"), (850, MAG, "ДАВЛЕНИЕ"))):
        b.append(f'<g class="ic{i}"><circle cx="{cx}" cy="780" r="110" fill="{col}" stroke="{INK}" stroke-width="10"/>'
                 f'<text x="{cx}" y="{940}" font-family="Nunito" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">{label}</text></g>')
    b.append(t(385, 830, "+", 80, INK, "middle", 900))
    b.append(t(695, 830, "=", 80, INK, "middle", 900))
    b.append(t(540, 360, "ПОЧЕМУ", 64, INK, "middle", 900))
    b.append(t(540, 1210, "БОМБА", 96, RED, "middle", 900, ls=4))
    b.append(t(540, 1320, "тайваньский кит · 2004", 28, INK, "middle", 700))
    b.append(t(540, 1700, "Reuters · архив 2004", 26, INK, "middle", 700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".tr1", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.05);'
    'tl.fromTo(".wh1", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.5}, 0.35);'
    'tl.fromTo(".b1", {opacity:0, scale:0.7}, {opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}, 0.05);'
    'tl.fromTo(".hl", {opacity:0, y:14}, {opacity:1, y:0, duration:0.35, stagger:0.08}, 0);'
    'tl.to(".wh1", {y:-8, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);',
    'tl.fromTo(".wh2", {opacity:0, y:-60}, {opacity:1, y:0, duration:0.8, ease:"power2.out"}, 0.1);'
    'tl.fromTo(".tr2", {opacity:0, x:40}, {opacity:1, x:0, duration:0.6}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".tr3", {opacity:0, x:-80}, {opacity:1, x:0, duration:0.8}, 0.05);'
    'tl.fromTo(".wh3", {opacity:0}, {opacity:1, duration:0.5}, 0.4);'
    'tl.fromTo(".p3a, .p3b", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 0.6);'
    'tl.to(".wh3", {y:-10, duration:0.5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".wh4", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.7, ease:"back.out(1.4)"}, 0.05);'
    'tl.to(".wh4", {scale:1.03, duration:0.8, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".ar0, .ar1, .ar2, .ar3", {opacity:0}, {opacity:1, duration:0.4, stagger:0.12}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".sp1", {opacity:0, scale:0.3}, {opacity:1, scale:1, duration:0.45, ease:"back.out(2.2)"}, 0.05);'
    'tl.fromTo(".b5", {opacity:0, scale:0.5}, {opacity:1, scale:1, duration:0.4, ease:"back.out(3)"}, 0.1);'
    'tl.fromTo(".d0, .d1, .d2, .d3, .d4", {opacity:0, y:20}, {opacity:1, y:0, duration:0.3, stagger:0.08}, 0.3);'
    'tl.fromTo(".hl", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}, 0.25);',
    'tl.fromTo(".p6a", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.5}, 0.1);'
    'tl.fromTo(".p6b", {opacity:0, x:30}, {opacity:1, x:0, duration:0.5}, 0.3);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.15}, 0.2);',
    'tl.fromTo(".p7a, .p7b", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.1);'
    'tl.fromTo(".hose, .hose2", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.12}, 0.1);',
    'tl.fromTo(".ic0", {opacity:0, y:20}, {opacity:1, y:0, duration:0.45}, 0.1);'
    'tl.fromTo(".ic1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.45}, 0.3);'
    'tl.fromTo(".ic2", {opacity:0, y:20}, {opacity:1, y:0, duration:0.45}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.12}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{PAPER}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
