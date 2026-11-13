#!/usr/bin/env python3
"""«Турбина в водостоке» — 8 сцен, тушь и акварель."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/rainpower")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

PAPER = "#fbf6ea"; PAPER_D = "#eadfc6"
INK = "#3a3733"; INK2 = "#6b655c"
WALL = "#efe8d8"; WALL_D = "#d8cfba"
ROOF = "#d9c3a0"; ROOF_D = "#b49c76"
BRICK = "#ddd8cc"; BRICK_D = "#b7b1a3"
WATER = "#a8c9dc"; WATER_D = "#6f9cb5"
METAL = "#c9cdc9"; METAL_D = "#8d938f"
LAMP = "#f0c25c"; LAMP_D = "#c9993a"
HOT = "#c0703f"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def paper(seed=1):
    r = random.Random(seed)
    sp = "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.7,2):.1f}" '
                 f'fill="#8a7a55" opacity="{r.uniform(0.03,0.09):.2f}"/>' for _ in range(200))
    return (f'<rect width="1080" height="1920" fill="{PAPER}"/>{sp}'
            f'<rect x="20" y="20" width="1040" height="1880" fill="none" stroke="{PAPER_D}" stroke-width="3"/>')


def siding(x, y, w, h, cls="sd"):
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WALL}" stroke="{INK}" stroke-width="3"/>']
    rows = int(h / 44)
    for i in range(rows):
        yy = y + 30 + i * 44
        b.append(f'<path d="M {x} {yy} l {w} 0" stroke="{WALL_D}" stroke-width="4"/>')
        b.append(f'<path d="M {x} {yy+4} l {w} 0" stroke="#ffffff" stroke-width="2" opacity="0.6"/>')
    b.append('</g>')
    return "".join(b)


def roof_edge(x, y, w, cls="rf"):
    return (f'<g class="{cls}"><path d="M {x-30} {y} L {x+w+30} {y} L {x+w+10} {y-46} L {x-10} {y-46} Z" fill="{ROOF}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {x-30} {y} L {x+w+30} {y}" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M {x+20} {y-40} l 0 36 M {x+80} {y-40} l 0 36 M {x+140} {y-40} l 0 36" stroke="{ROOF_D}" stroke-width="2" opacity="0.6"/></g>')


def gutter(x, y, w=340, cls="gt"):
    """Жёлоб и труба вниз."""
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x} {y} l {w} 0 l -14 34 l {-w+28} 0 z" fill="{METAL}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path d="M {x+w-10} {y+6} q 26 30 8 60 l -34 130 l -40 0 l 34 -140 q 8 -34 32 -50z" fill="{METAL}" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def turbine(cx, cy, r=90, cls="tb", angle=0):
    b = [f'<g class="{cls}">']
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r+22}" fill="{METAL}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r+22}" fill="{WATER}" opacity="0.35"/>')
    b.append(f'<g class="wheel" style="transform-box: fill-box; transform-origin: 50% 50%;"><g transform="rotate({angle} {cx} {cy})">')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#e9e4d6" stroke="{INK}" stroke-width="4"/>')
    for i in range(10):
        a = math.radians(i * 36)
        b.append(f'<path d="M {cx} {cy} L {cx + r*math.cos(a):.0f} {cy + r*math.sin(a):.0f}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<circle cx="{cx + r*0.62*math.cos(a):.0f}" cy="{cy + r*0.62*math.sin(a):.0f}" r="{r*0.16:.0f}" '
                 f'fill="{METAL}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.2:.0f}" fill="{METAL_D}" stroke="{INK}" stroke-width="3"/>')
    b.append('</g></g></g>')
    return "".join(b)


def puddle(cx, cy, rx=190, ry=60, cls="pd"):
    return (f'<g class="{cls}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WATER}" opacity="0.5" stroke="{WATER_D}" stroke-width="3"/>'
            f'<ellipse cx="{cx-30}" cy="{cy-10}" rx="{rx*0.4:.0f}" ry="{ry*0.3:.0f}" fill="#ffffff" opacity="0.35"/></g>')


def water_jet(x1, y1, x2, y2, cls="jet", w=22):
    return (f'<g class="{cls}"><path d="M {x1} {y1} q {10} {(y2-y1)*0.5:.0f} {x2-x1} {y2-y1}" stroke="{WATER}" stroke-width="{w}" fill="none" '
            f'stroke-linecap="round" opacity="0.85"/>'
            f'<path d="M {x1} {y1} q {10} {(y2-y1)*0.5:.0f} {x2-x1} {y2-y1}" stroke="#ffffff" stroke-width="{w*0.35:.0f}" fill="none" opacity="0.5"/></g>')


def lamp(x, y, cls="lp"):
    return (f'<g class="{cls}"><path d="M {x} {y} l 0 -40" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M {x-26} {y-40} q 26 -34 52 0 z" fill="{METAL}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x}" cy="{y+18}" r="26" fill="{LAMP}" opacity="0.85"/>'
            f'<circle cx="{x}" cy="{y+18}" r="44" fill="{LAMP}" opacity="0.22"/>'
            f'<path d="M {x-26} {y-40} l 52 0" stroke="{INK}" stroke-width="3"/></g>')


def label(x, y, s, size=22, cls="lb", col=INK, wash=None):
    w = len(s) * size * 0.58 + 26
    bg = wash or "#fffdf6"
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="6" fill="{bg}" opacity="0.92" stroke="{INK2}" stroke-width="1.5"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


def rain(n=26, seed=3, cls="rn"):
    r = random.Random(seed)
    out = [f'<g class="{cls}">']
    for i in range(n):
        x, y = r.uniform(60, 1020), r.uniform(140, 900)
        out.append(f'<path class="r{i}" d="M {x:.0f} {y:.0f} l -8 34" stroke="{WATER_D}" stroke-width="3" opacity="0.5" stroke-linecap="round"/>')
    out.append('</g>')
    return "".join(out)


# ---------------------------------------------------------------- 1
def s1():
    b = [paper(1), rain(22, 2)]
    b.append(siding(560, 520, 460, 780, "sd1"))
    b.append('<rect x="0" y="1300" width="1080" height="620" fill="#e7e2d0"/>')
    b.append(f'<path d="M 0 1300 l 1080 0" stroke="{INK}" stroke-width="4"/>')
    b.append(roof_edge(150, 520, 880, "rf1"))
    b.append(gutter(300, 560, 380, "gt1"))
    b.append(water_jet(596, 720, 600, 1300, "j1", 26))
    b.append(puddle(600, 1350, 240, 70, "pd1"))
    b.append(t(60, 180, "ВОДОСТОК", 56, INK))
    b.append(t(60, 246, "может не только сливать", 34, INK2))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [paper(2), rain(16, 4)]
    b.append(siding(560, 480, 460, 820, "sd2"))
    b.append('<rect x="0" y="1300" width="1080" height="620" fill="#e7e2d0"/>')
    b.append(f'<path d="M 0 1300 l 1080 0" stroke="{INK}" stroke-width="4"/>')
    b.append(roof_edge(150, 480, 880, "rf2"))
    b.append(gutter(300, 520, 380, "gt2"))
    b.append(water_jet(596, 680, 600, 1300, "j2", 26))
    b.append(puddle(640, 1360, 270, 84, "pd2"))
    b.append(f'<path d="M 900 1430 q -140 40 -260 0" stroke="{HOT}" stroke-width="5" fill="none" stroke-dasharray="12 10"/>')
    b.append(label(120, 1480, "ЛУЖА У ФУНДАМЕНТА", 22, "lb1"))
    b.append(t(60, 180, "СЕЙЧАС ТАК", 44, INK))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [paper(3)]
    b.append(siding(560, 460, 460, 1000, "sd3"))
    b.append(roof_edge(150, 460, 880, "rf3"))
    b.append(gutter(300, 500, 380, "gt3"))
    b.append(f'<rect x="520" y="760" width="120" height="260" rx="18" fill="{METAL}" stroke="{INK}" stroke-width="4"/>')
    b.append(turbine(580, 890, 64, "tb3"))
    b.append(water_jet(596, 700, 580, 800, "j3", 20))
    b.append(f'<path d="M 580 1010 l 0 150" stroke="{WATER}" stroke-width="18" opacity="0.6"/>')
    b.append(label(700, 820, "КОРПУС С ТУРБИНОЙ", 20, "lb2"))
    b.append(t(60, 180, "ВМЕСТО КОЛЕНА", 40, INK))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [paper(4)]
    b.append(f'<circle cx="540" cy="900" r="300" fill="{WATER}" opacity="0.12"/>')
    b.append(turbine(540, 900, 190, "tb4"))
    b.append(water_jet(300, 640, 470, 820, "j4", 26))
    b.append(label(700, 1180, "МИКРО-ПЕЛТОН", 22, "lb3"))
    b.append(t(60, 200, "ВОДА КРУТИТ КОЛЕСО", 36, INK))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [paper(5)]
    b.append(f'<rect x="200" y="760" width="220" height="240" rx="16" fill="{METAL}" stroke="{INK}" stroke-width="4"/>')
    b.append(t(310, 890, "ГЕН", 44, INK, "middle", 900))
    b.append(f'<path d="M 420 880 q 160 -40 240 20" stroke="{INK}" stroke-width="4" fill="none"/>')
    b.append(lamp(720, 900, "lp5"))
    b.append(t(60, 220, "ПРОВОД → СВЕТ", 42, INK))
    b.append(label(200, 1080, "АККУМУЛЯТОР И ЛАМПА", 20, "lb4"))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [paper(6)]
    b.append(f'<rect x="120" y="620" width="380" height="240" rx="14" fill="{WALL}" stroke="{INK}" stroke-width="3"/>')
    b.append(t(310, 700, "КРЫША", 26, INK, "middle", 800))
    b.append(t(310, 800, "100 м²", 56, INK, "middle", 900))
    b.append(f'<path d="M 540 740 l 80 0" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="650" y="620" width="300" height="240" rx="14" fill="{WATER}" opacity="0.3" stroke="{INK}" stroke-width="3"/>')
    b.append(t(800, 700, "ДОЖДЬ", 26, INK, "middle", 800))
    b.append(t(800, 800, "10 мм", 56, WATER_D, "middle", 900))
    b.append(f'<path d="M 460 960 q 60 60 120 0" stroke="{INK}" stroke-width="4" fill="none"/>')
    b.append(t(540, 1080, "≈ 1000 Л ВОДЫ", 52, INK, "middle", 900))
    b.append(t(60, 220, "СКОЛЬКО ЭТО", 42, INK))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [paper(7)]
    b.append(siding(560, 460, 460, 1000, "sd7"))
    b.append(roof_edge(150, 460, 880, "rf7"))
    b.append(gutter(300, 500, 380, "gt7"))
    b.append(f'<rect x="520" y="760" width="120" height="240" rx="18" fill="{METAL}" stroke="{INK}" stroke-width="4"/>')
    b.append(turbine(580, 880, 58, "tb7"))
    b.append(f'<path d="M 580 1000 q 120 90 240 60" stroke="{WATER}" stroke-width="16" fill="none" opacity="0.7"/>')
    b.append(f'<path d="M 760 1040 l 90 40" stroke="{INK}" stroke-width="4" stroke-dasharray="10 8"/>')
    b.append(label(780, 1100, "В СТОРОНУ ОТ ДОМА", 20, "lb5"))
    b.append(t(60, 180, "ФУНДАМЕНТ СУХОЙ", 40, INK))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [paper(8)]
    b.append(turbine(540, 760, 150, "tb8"))
    b.append(lamp(840, 700, "lp8"))
    b.append(t(540, 1120, "ДЕСЯТКИ ВАТТ", 54, INK, "middle", 900))
    b.append(t(540, 1190, "только пока идёт дождь", 26, INK2, "middle", 700))
    b.append(t(540, 1500, "но вода уходит от фундамента", 28, WATER_D, "middle", 800))
    b.append(t(540, 1560, "а свет — бесплатно", 28, INK, "middle", 800))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".sd1, .rf1", {opacity:0, y:16}, {opacity:1, y:0, duration:0.7, stagger:0.1}, 0.1);'
    'tl.fromTo(".gt1", {opacity:0}, {opacity:1, duration:0.5}, 0.4);'
    'tl.fromTo(".j1", {opacity:0}, {opacity:1, duration:0.6}, 0.6);'
    'tl.to(".j1", {opacity:0.55, duration:0.7, yoyo:true, repeat:-1}, 1.0);'
    'tl.fromTo(".pd1", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6}, 0.7);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".sd2, .rf2, .gt2", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.1);'
    'tl.to(".j2", {opacity:0.55, duration:0.7, yoyo:true, repeat:-1}, 0.5);'
    'tl.to(".pd2", {scaleX:1.12, transformOrigin:"600px 1280px", duration:1.6, ease:"sine.out"}, 0.6);'
    'tl.fromTo(".lb1", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".sd3, .rf3, .gt3", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.1);'
    'tl.fromTo(".tb3", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.6, ease:"back.out(1.6)"}, 0.5);'
    'tl.to(".tb3", {scale:1.03, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".lb2", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".tb4", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.7}, 0.1);'
    'tl.to(".tb4", {scale:1.02, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.5);'
    'tl.fromTo(".j4", {opacity:0}, {opacity:1, duration:0.6}, 0.4);'
    'tl.fromTo(".lb3", {opacity:0}, {opacity:1, duration:0.4}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".lp5", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6}, 0.2);'
    'tl.to(".lp5", {opacity:0.75, duration:0.8, yoyo:true, repeat:-1}, 0.8);'
    'tl.fromTo(".lb4", {opacity:0}, {opacity:1, duration:0.4}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".sd7, .rf7, .gt7", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.1);'
    'tl.to(".tb7", {scale:1.03, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.6);'
    'tl.fromTo(".lb5", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".tb8", {opacity:0, scale:0.92}, {opacity:1, scale:1, duration:0.6}, 0.1);'
    'tl.to(".tb8", {scale:1.02, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.6);'
    'tl.fromTo(".lp8", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.2);',
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
