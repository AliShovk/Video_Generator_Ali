#!/usr/bin/env python3
"""«Солнечный дистиллятор» — 9 сцен, тёплая иллюстрация."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/still")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

SAND = "#efd9a8"; SAND_D = "#d9ba7f"
INK = "#3d3226"; INK2 = "#6f5f4a"
GLASS = "#cfe9f3"; GLASS_D = "#8db9c9"
WOOD = "#b07a45"; WOOD_D = "#82552a"
STONE = "#b9b0a4"; STONE_D = "#8d8375"
DIRTY = "#8a6a3c"; CLEAN = "#5fb6d9"
SUN = "#f2b33d"; SUN_D = "#d9911f"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def title(x, y, s, size=36, cls="hl", col=INK):
    w = len(s) * size * 0.60 + 32
    return (f'<g class="{cls}"><rect x="{x-12}" y="{y-size*1.1:.0f}" width="{w:.0f}" height="{size*1.6:.0f}" rx="{size*0.3:.0f}" '
            f'fill="#fffaf0" opacity="0.9"/>'
            f'<text x="{x}" y="{y}" font-family="Nunito" font-size="{size}" font-weight="900" fill="{col}" letter-spacing="1">{s}</text></g>')


def bg(seed=1):
    r = random.Random(seed)
    grains = "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(700,1900):.0f}" r="{r.uniform(1,3):.1f}" '
                     f'fill="{SAND_D}" opacity="{r.uniform(0.15,0.4):.2f}"/>' for _ in range(160))
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#fdf4dd"/><stop offset="1" stop-color="#f7e6c2"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sky)"/>'
            f'<path d="M 0 1500 q 260 -90 540 -20 q 280 70 540 -30 l 0 470 l -1080 0 z" fill="{SAND}"/>{grains}')


def sun(cx=180, cy=330, r=95, cls="sun"):
    b = [f'<g class="{cls}">']
    for i in range(12):
        a = math.radians(i * 30)
        b.append(f'<path d="M {cx+r*1.25*math.cos(a):.0f} {cy+r*1.25*math.sin(a):.0f} l {40*math.cos(a):.0f} {40*math.sin(a):.0f}" '
                 f'stroke="{SUN_D}" stroke-width="8" stroke-linecap="round" opacity="0.75"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>')
    b.append(f'<circle cx="{cx-r*0.3:.0f}" cy="{cy-r*0.3:.0f}" r="{r*0.45:.0f}" fill="#ffd97a" opacity="0.55"/>')
    b.append('</g>')
    return "".join(b)


def stones(x, y, w=620, h=230, cls="st"):
    b = [f'<g class="{cls}">']
    rows = 3
    for row in range(rows):
        yy = y + h - (row + 1) * (h / rows)
        n = 5 + row
        bw = w / n
        for i in range(n):
            px = x + i * bw + (bw * 0.5 if row % 2 else 0) - 6
            b.append(f'<rect x="{px:.0f}" y="{yy:.0f}" width="{bw-12:.0f}" height="{h/rows-8:.0f}" rx="14" '
                     f'fill="{STONE}" stroke="{STONE_D}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def still(cx=540, by=1280, w=620, h=360, cls="still", water=DIRTY, glass=True, drop=True):
    """Дистиллятор: лоток, купол, жёлоб."""
    apex_x, apex_y = cx, by - h - 120
    left, right = cx - w / 2, cx + w / 2
    b = [f'<g class="{cls}">']
    b.append(stones(cx - w / 2 - 40, by, w + 80, 230, f"{cls}s"))
    # лоток
    b.append(f'<rect x="{left}" y="{by-60}" width="{w}" height="70" rx="10" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="5"/>')
    b.append(f'<rect x="{left+16}" y="{by-52}" width="{w-32}" height="46" rx="8" fill="{water}"/>')
    b.append(f'<path d="M {left+30} {by-44} q 60 -10 120 0" stroke="#ffffff" stroke-width="3" fill="none" opacity="0.25"/>')
    if glass:
        b.append(f'<path d="M {left} {by-62} L {apex_x} {apex_y} L {right} {by-62} Z" fill="{GLASS}" opacity="0.45" stroke="{GLASS_D}" stroke-width="5"/>')
        b.append(f'<path d="M {left+8} {by-70} L {apex_x} {apex_y+14} L {apex_x-40} {by-70} Z" fill="#ffffff" opacity="0.35"/>')
        b.append(f'<path d="M {right} {by-62} L {apex_x} {apex_y}" stroke="{GLASS_D}" stroke-width="4"/>')
    # жёлоб
    b.append(f'<path d="M {right-80} {by-96} l 0 60 l 46 0 l 0 -60" fill="none" stroke="{WOOD_D}" stroke-width="10"/>')
    b.append(f'<path d="M {right-70} {by-40} l 0 40" stroke="{CLEAN}" stroke-width="7" stroke-dasharray="6 8"/>')
    b.append('</g>')
    return "".join(b)


def pot(cx, by, s=1.0, cls="pot", level=0.4):
    b = [f'<g class="{cls}"><g transform="translate({cx} {by}) scale({s})">']
    b.append(f'<path d="M -60 -70 q 0 70 14 92 q 46 16 92 0 q 14 -22 14 -92 z" fill="#c07a4a" stroke="#8f5530" stroke-width="4"/>')
    b.append(f'<rect x="-58" y="-80" width="116" height="18" rx="8" fill="#a9663c" stroke="#8f5530" stroke-width="3"/>')
    b.append(f'<rect class="plevel" x="-46" y="{-70*level:.0f}" width="92" height="{70*level:.0f}" fill="{CLEAN}" opacity="0.75"/>')
    b.append('</g></g>')
    return "".join(b)


def arrows_up(x, y, n=4, cls="ev"):
    b = [f'<g class="{cls}">']
    for i in range(n):
        px = x + i * 60
        b.append(f'<path class="a{i}" d="M {px} {y} l 0 -70" stroke="#e8a04a" stroke-width="7" stroke-linecap="round"/>')
        b.append(f'<path d="M {px-16} {y-56} l 16 -20 l 16 20" fill="none" stroke="#e8a04a" stroke-width="7" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def drops(x, y, n=6, cls="dr"):
    b = [f'<g class="{cls}">']
    for i in range(n):
        px = x + i * 46
        py = y + (i % 3) * 26
        b.append(f'<path class="d{i}" d="M {px} {py} q 8 12 0 20 q -8 -8 0 -20 z" fill="{CLEAN}" opacity="0.9"/>')
    b.append('</g>')
    return "".join(b)


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(1)]
    b.append(sun(900, 300, 100, "sun1"))
    b.append(still(540, 1300, 620, 360, "st1"))
    b.append(pot(880, 1520, 1.0, "pot1", 0.45))
    b.append(title(60, 190, "СОЛНЕЧНЫЙ ДИСТИЛЛЯТОР", 32))
    b.append(t(64, 250, "грязная вода + солнце = питьевая", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg(2)]
    b.append(f'<path d="M 200 900 q 340 -60 680 0 l 0 300 l -680 0 z" fill="{SAND_D}" opacity="0.6"/>')
    b.append(f'<rect x="230" y="880" width="620" height="220" rx="18" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="5"/>')
    b.append(f'<rect x="250" y="900" width="580" height="180" rx="12" fill="{DIRTY}"/>')
    b.append(f'<path d="M 270 960 q 140 -16 280 0" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.2"/>')
    b.append(title(60, 190, "ЛОТОК С ГРЯЗНОЙ ВОДОЙ", 30))
    b.append(t(64, 250, "яма или поддон", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(3), sun(900, 300, 90, "sun3")]
    b.append(still(540, 1300, 620, 400, "st3"))
    b.append(f'<path class="glint" d="M 300 1100 l 120 -160" stroke="#ffffff" stroke-width="6" opacity="0.5"/>')
    b.append(title(60, 190, "ПРОЗРАЧНЫЙ КУПОЛ", 34))
    b.append(t(64, 250, "стекло или плёнка", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg(4), sun(900, 310, 105, "sun4")]
    b.append(still(540, 1300, 620, 380, "st4"))
    b.append(arrows_up(400, 1150, 4, "ev4"))
    b.append(title(60, 190, "ИСПАРЕНИЕ", 40))
    b.append(t(64, 252, "солнце нагревает воду", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg(5)]
    b.append(still(540, 1300, 620, 380, "st5"))
    b.append(drops(560, 900, 6, "dr5"))
    b.append(title(60, 190, "КОНДЕНСАЦИЯ", 40))
    b.append(t(64, 252, "пар оседает на холодном стекле", 22, INK2, w=700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(6)]
    b.append(still(540, 1300, 620, 380, "st6"))
    b.append(pot(880, 1520, 1.05, "pot6", 0.55))
    b.append(f'<circle class="drip0" cx="820" cy="1240" r="8" fill="{CLEAN}"/>')
    b.append(f'<circle class="drip1" cx="820" cy="1300" r="7" fill="{CLEAN}"/>')
    b.append(f'<circle class="drip2" cx="820" cy="1360" r="9" fill="{CLEAN}"/>')
    b.append(title(60, 190, "СТЕКАЕТ В ЁМКОСТЬ", 32))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg(7)]
    b.append(still(540, 1300, 620, 380, "st7"))
    b.append(f'<path d="M 300 1240 q 240 40 480 0" stroke="#6b5334" stroke-width="8" fill="none" opacity="0.7"/>')
    b.append(f'<circle cx="360" cy="1256" r="10" fill="#6b5334" opacity="0.7"/>')
    b.append(f'<circle cx="430" cy="1264" r="7" fill="#6b5334" opacity="0.6"/>')
    b.append(title(60, 190, "ВНИЗУ — ГРЯЗЬ И СОЛЬ", 32))
    b.append(t(64, 250, "они остаются на дне", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [bg(8), sun(880, 320, 90, "sun8")]
    b.append(pot(430, 1450, 2.2, "pot8", 0.75))
    b.append(t(760, 1180, "3–5", 96, CLEAN, "middle", 900))
    b.append(t(760, 1250, "ЛИТРОВ В ДЕНЬ", 26, INK, "middle", 800))
    b.append(title(60, 190, "СКОЛЬКО ВОДЫ", 38))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [bg(9), sun(540, 520, 150, "sun9")]
    b.append(still(540, 1320, 560, 320, "st9"))
    b.append(title(60, 190, "ТОЛЬКО СОЛНЦЕ", 40))
    b.append(t(64, 252, "ни фильтра, ни электричества", 24, INK2, w=700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".st1", {opacity:0, y:24}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".sun1", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.6, ease:"back.out(1.5)"}, 0.2);'
    'tl.to(".sun1", {rotate:14, transformOrigin:"170px 320px", duration:8, repeat:-1, ease:"none"}, 0.5);'
    'tl.fromTo(".pot1", {opacity:0, x:20}, {opacity:1, x:0, duration:0.5}, 0.7);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".st3", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.to(".glint", {opacity:0.1, duration:1.2, yoyo:true, repeat:-1}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".st4", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".ev4", {opacity:0}, {opacity:1, duration:0.6}, 0.3);'
    'tl.to(".a0, .a1, .a2, .a3", {y:-40, opacity:0.2, duration:1.2, stagger:0.18, repeat:-1, ease:"sine.out"}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".st5", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".dr5", {opacity:0}, {opacity:1, duration:0.6}, 0.3);'
    'tl.to(".d0, .d1, .d2, .d3, .d4, .d5", {y:120, opacity:0, duration:1.8, stagger:0.2, repeat:-1, ease:"sine.in"}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".st6", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".pot6", {opacity:0, x:20}, {opacity:1, x:0, duration:0.5}, 0.3);'
    'tl.to(".drip0", {y:120, opacity:0, duration:1.1, repeat:-1}, 0.5);'
    'tl.to(".drip1", {y:120, opacity:0, duration:1.1, repeat:-1}, 0.9);'
    'tl.to(".drip2", {y:120, opacity:0, duration:1.1, repeat:-1}, 1.3);'
    'tl.fromTo(".plevel", {scaleY:0.6, transformOrigin:"540px 1450px"}, {scaleY:1, duration:2, ease:"sine.out"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".st7", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".pot8", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.to(".plevel", {scaleY:1.15, transformOrigin:"430px 1450px", duration:2, ease:"sine.out"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".st9", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".sun9", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.6}, 0.2);'
    'tl.to(".sun9", {rotate:12, transformOrigin:"540px 520px", duration:8, repeat:-1, ease:"none"}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SAND}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
