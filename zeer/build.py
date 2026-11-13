#!/usr/bin/env python3
"""«Глиняный холодильник» — 8 сцен, винтажный постер."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/zeer")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

PAPER = "#f4e7c9"; PAPER_D = "#e3d2ad"
INK = "#3a2a1c"; INK2 = "#6b5236"
CLAY = "#c1703f"; CLAY_D = "#9c5228"; CLAY_L = "#d98e5c"
SAND = "#e0c08a"; SAND_D = "#c9a468"
GREEN = "#6d8b4a"; GREEN_D = "#4f6b32"
RED = "#b4402f"; RED_D = "#8c2f22"
BLUE = "#6fa3bf"; CREAM = "#f7efd9"
YEL = "#d9a13b"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl", italic=False, family="Nunito, Arial"):
    it = ' font-style="italic"' if italic else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{w}"{it} '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def paper(seed=1):
    r = random.Random(seed)
    sp = "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.8,2.4):.1f}" '
                 f'fill="#8a6a3a" opacity="{r.uniform(0.03,0.1):.2f}"/>' for _ in range(220))
    return (f'<rect width="1080" height="1920" fill="{PAPER}"/>{sp}'
            f'<rect x="0" y="0" width="1080" height="1920" fill="none" stroke="{PAPER_D}" stroke-width="26"/>'
            f'<rect x="26" y="26" width="1028" height="1868" fill="none" stroke="#b89a66" stroke-width="2" opacity="0.5"/>')


def ribbon(cx, cy, w, h, text, sub=""):
    b = [f'<g class="rib"><path d="M {cx-w/2-40} {cy} l 40 -{h/2} l 0 {h} z" fill="{CLAY_D}"/>'
         f'<path d="M {cx+w/2+40} {cy} l -40 -{h/2} l 0 {h} z" fill="{CLAY_D}"/>'
         f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="8" fill="{CLAY}"/>'
         f'<text x="{cx}" y="{cy+12}" font-family="Nunito" font-size="{h*0.44:.0f}" font-weight="900" fill="{CREAM}" '
         f'text-anchor="middle" letter-spacing="2">{text}</text>']
    if sub:
        b.append(f'<text x="{cx}" y="{cy+h/2+40}" font-family="Nunito" font-size="26" font-weight="800" font-style="italic" '
                 f'fill="{INK2}" text-anchor="middle">{sub}</text>')
    b.append('</g>')
    return "".join(b)


def pot(cx, by, w=360, h=300, cls="pot", inner=False, sand=False, water=False):
    """Глиняный горшок с орнаментальной полосой."""
    b = [f'<g class="{cls}">']
    top = by - h * 0.86
    b.append(f'<path d="M {cx-w/2} {by} q {-14} {-h*0.55} {w*0.12} {-h*0.9} q {w*0.38} {-h*0.16} {w*0.76} 0 '
             f'q {w*0.12} {-h*0.35} 0 {0} q {0} 0 0 0" fill="none"/>')
    b.append(f'<path d="M {cx-w/2} {by} q 0 {-h*0.86} {w/2} {-h*0.86} q {w/2} 0 {w/2} {h*0.86} z" fill="{CLAY}" stroke="{CLAY_D}" stroke-width="5"/>')
    b.append(f'<ellipse cx="{cx}" cy="{top}" rx="{w/2}" ry="{w*0.10}" fill="{CLAY_L}" stroke="{CLAY_D}" stroke-width="5"/>')
    b.append(f'<ellipse cx="{cx}" cy="{top}" rx="{w*0.38}" ry="{w*0.10}" fill="#5b3a22" opacity="0.55"/>')
    # орнамент
    yy = by - h * 0.32
    b.append(f'<rect x="{cx-w*0.44}" y="{yy}" width="{w*0.88}" height="{h*0.10}" fill="{CLAY_D}" opacity="0.35"/>')
    for k in range(5):
        px = cx - w * 0.34 + k * w * 0.17
        b.append(f'<path d="M {px} {yy+h*0.05} l {w*0.05} {-h*0.03} l {w*0.05} {h*0.03}" stroke="{CREAM}" stroke-width="4" fill="none" opacity="0.8"/>')
    b.append('</g>')
    return "".join(b)


def arrows_out(cx, cy, n=5, cls="ev"):
    b = [f'<g class="{cls}">']
    for i in range(n):
        a = math.radians(-150 + i * 40)
        x1, y1 = cx + 190 * math.cos(a), cy + 170 * math.sin(a)
        x2, y2 = cx + 300 * math.cos(a), cy + 300 * math.sin(a)
        b.append(f'<path class="ar{i}" d="M {x1:.0f} {y1:.0f} L {x2:.0f} {y2:.0f}" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>')
        b.append(f'<path d="M {x2-18*math.cos(a):.0f} {y2-18*math.sin(a):.0f} l {-14*math.sin(a):.0f} {14*math.cos(a):.0f} '
                 f'l {28*math.sin(a):.0f} {-28*math.cos(a):.0f}" fill="none" stroke="{BLUE}" stroke-width="9" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def veg(x, y, cls="vg"):
    b = [f'<g class="{cls}">']
    # капуста
    b.append(f'<circle cx="{x}" cy="{y}" r="52" fill="{GREEN}" stroke="{GREEN_D}" stroke-width="4"/>')
    for r in (38, 24):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{GREEN_D}" stroke-width="3" opacity="0.7"/>')
    # помидор
    b.append(f'<circle cx="{x+86}" cy="{y+26}" r="40" fill="{RED}" stroke="{RED_D}" stroke-width="4"/>')
    b.append(f'<path d="M {x+86} {y-14} l -10 12 l 20 0 z" fill="{GREEN_D}"/>')
    # перец
    b.append(f'<path d="M {x-84} {y+30} q -18 40 6 62 q 22 14 34 -8 q 8 -34 -8 -54 z" fill="{YEL}" stroke="#a87a20" stroke-width="4"/>')
    # сыр
    b.append(f'<path d="M {x-30} {y+96} l 110 0 l -104 46 l 0 -46 z" fill="#f0dfae" stroke="#c2a76a" stroke-width="4"/>')
    b.append(f'<circle cx="{x+20}" cy="{y+120}" r="6" fill="#c2a76a" opacity="0.7"/>')
    b.append('</g>')
    return "".join(b)


def thermo(x, y, h=300, cls="th"):
    return (f'<g class="{cls}"><rect x="{x-16}" y="{y-h}" width="32" height="{h}" rx="16" fill="{CREAM}" stroke="{INK2}" stroke-width="4"/>'
            f'<circle cx="{x}" cy="{y+22}" r="34" fill="{CREAM}" stroke="{INK2}" stroke-width="4"/>'
            f'<circle cx="{x}" cy="{y+22}" r="22" fill="{BLUE}"/>'
            f'<rect class="merc" x="{x-7}" y="{y-h*0.45:.0f}" width="14" height="{h*0.45+20:.0f}" rx="7" fill="{BLUE}"/></g>')


def step_badge(x, y, n, cls="bd"):
    return (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="34" fill="{RED}"/>'
            f'<text x="{x}" y="{y+14}" font-family="Nunito" font-size="40" font-weight="900" fill="{CREAM}" text-anchor="middle">{n}</text></g>')


def label(x, y, s, size=22, cls="lb", col=INK):
    w = len(s) * size * 0.58 + 26
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="6" fill="{CREAM}" opacity="0.9"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [paper(1)]
    b.append(ribbon(540, 190, 780, 120, "ГЛИНЯНЫЙ ХОЛОДИЛЬНИК", "два горшка, песок и вода"))
    b.append(pot(280, 1150, 440, 360, "p1o"))
    b.append(pot(800, 1100, 270, 260, "p1i"))
    b.append(f'<path class="sand1" d="M 500 1190 q 70 -70 140 0 q 30 26 -70 30 q -100 -4 -70 -30 z" fill="{SAND}" stroke="{SAND_D}" stroke-width="4"/>')
    b.append(f'<path d="M 660 1250 q 40 -18 80 -6" stroke="{INK2}" stroke-width="5" fill="none" stroke-dasharray="10 8"/>')
    b.append(label(470, 1250, "1,5–2 см песка", 22, "lb1"))
    b.append(label(575, 860, "2 ГОРШКА", 22, "lb2"))
    b.append(t(540, 1600, "без электричества", 28, INK2, "middle", 700, italic=True))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [paper(2)]
    b.append(step_badge(120, 300, 1))
    b.append(t(180, 315, "СБОРКА", 46, INK))
    b.append(pot(540, 1320, 480, 420, "p2o"))
    b.append(pot(540, 1120, 300, 300, "p2i"))
    b.append(f'<g class="sandpour"><path d="M 700 720 q 20 90 -10 160" stroke="{SAND_D}" stroke-width="26" fill="none" opacity="0.9"/>'
             f'<circle cx="700" cy="700" r="40" fill="{SAND}" stroke="{SAND_D}" stroke-width="4"/></g>')
    b.append(arrows_out(540, 1250, 0, "e0"))
    b.append(label(700, 940, "ПЕСОК", 24, "lb2"))
    b.append(label(120, 1420, "ГОРШКИ БЕЗ ГЛАЗУРИ", 22, "lb3"))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [paper(3)]
    b.append(step_badge(120, 300, 2))
    b.append(t(180, 315, "ПРОМОЧИТЬ", 46, INK))
    b.append(pot(540, 1320, 480, 420, "p3o", water=True))
    b.append(pot(540, 1120, 300, 300, "p3i"))
    b.append(f'<g class="pour"><path d="M 700 700 q 30 110 -6 200" stroke="{BLUE}" stroke-width="16" fill="none" opacity="0.85"/></g>')
    b.append(f'<g class="cloth"><path d="M 380 1090 q 160 -50 320 0 l 0 40 q -160 40 -320 0 z" fill="#cfc3a4" stroke="{INK2}" stroke-width="4"/>'
             f'<path d="M 380 1102 q 160 -40 320 0" stroke="#b9ab8a" stroke-width="3" fill="none"/></g>')
    b.append(label(740, 1180, "МОКРАЯ ТКАНЬ", 20, "lb4"))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [paper(4)]
    b.append(t(60, 260, "КАК ЭТО РАБОТАЕТ", 44, INK))
    b.append(pot(540, 1380, 400, 400, "p4o", water=True))
    b.append(pot(540, 1180, 260, 280, "p4i"))
    b.append(arrows_out(540, 1180, 5, "ev4"))
    b.append(t(540, 640, "ИСПАРЕНИЕ", 40, BLUE, "middle", 900, ls=3))
    b.append(t(540, 700, "вода уходит с наружной стенки", 24, INK2, "middle", 700, italic=True))
    b.append(label(120, 1560, "ЗАБИРАЕТ ТЕПЛО", 22, "lb5"))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [paper(5)]
    b.append(pot(420, 1480, 470, 470, "p5o"))
    b.append(f'<circle cx="820" cy="900" r="190" fill="{CREAM}" stroke="{INK2}" stroke-width="4"/>')
    b.append(veg(820, 900, "v5"))
    b.append(f'<path d="M 690 1100 q -90 90 -140 200" stroke="{INK2}" stroke-width="5" fill="none" stroke-dasharray="10 8"/>')
    b.append(thermo(940, 1300, 260, "th5"))
    b.append(t(60, 280, "ВНУТРИ ПРОХЛАДНО", 40, INK))
    b.append(t(60, 340, "овощи, зелень, сыр", 24, INK2, w=700, italic=True))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [paper(6)]
    b.append(t(60, 280, "НА СКОЛЬКО ХОЛОДНЕЕ", 40, INK))
    b.append(thermo(300, 900, 520, "th6"))
    b.append(t(360, 520, "−10…−15 °C", 56, BLUE, "start", 900))
    b.append(t(360, 600, "от температуры воздуха", 26, INK2, w=700, italic=True))
    b.append(f'<rect x="160" y="1200" width="760" height="330" rx="18" fill="{CREAM}" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(540, 1290, "ЧЕМ СУШЕ ВОЗДУХ —", 30, INK, "middle", 800))
    b.append(t(540, 1345, "ТЕМ СИЛЬНЕЕ ХОЛОД", 30, RED, "middle", 900))
    b.append(t(540, 1430, "во влажном климате работает хуже", 24, INK2, "middle", 700, italic=True))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [paper(7)]
    b.append(f'<rect x="120" y="520" width="840" height="560" rx="16" fill="#e8d9b6" stroke="{INK2}" stroke-width="3"/>')
    # решётка навеса
    for i in range(8):
        b.append(f'<path d="M 120 {540+i*18} l 840 0" stroke="{INK2}" stroke-width="3" opacity="0.5"/>')
    b.append(pot(540, 1180, 380, 380, "p7o"))
    b.append(arrows_out(540, 1000, 3, "ev7"))
    b.append(t(60, 340, "ГДЕ СТАВИТЬ", 44, INK))
    b.append(t(64, 410, "тень, сквозняк, сухой воздух", 26, INK2, w=700, italic=True))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [paper(8)]
    b.append(ribbon(540, 240, 700, 110, "ГЛИНА · ПЕСОК · ВОДА"))
    b.append(pot(380, 1200, 300, 320, "p8a"))
    b.append(f'<circle cx="700" cy="760" r="70" fill="{SAND}" stroke="{SAND_D}" stroke-width="5"/>')
    b.append(f'<path d="M 700 830 l -30 60 l 60 0 z" fill="{SAND_D}" opacity="0.7"/>')
    b.append(f'<path d="M 640 1080 q 60 -40 130 -60" stroke="{BLUE}" stroke-width="14" fill="none"/>')
    b.append(t(540, 1560, "БОЛЬШЕ НИЧЕГО НЕ НУЖНО", 34, INK, "middle", 900))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".rib", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.7}, 0.05);'
    'tl.fromTo(".p1o", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.3);'
    'tl.fromTo(".p1i", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.55);'
    'tl.fromTo(".sand1", {opacity:0}, {opacity:1, duration:0.5}, 0.7);'
    'tl.fromTo(".lb1, .lb2", {opacity:0}, {opacity:1, duration:0.4, stagger:0.15}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".bd", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}, 0.1);'
    'tl.fromTo(".p2o", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.fromTo(".p2i", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.4);'
    'tl.to(".sandpour", {y:120, opacity:0.2, duration:1.4, repeat:-1, ease:"sine.in"}, 0.6);'
    'tl.fromTo(".lb2, .lb3", {opacity:0}, {opacity:1, duration:0.4, stagger:0.2}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".bd", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.4, ease:"back.out(2)"}, 0.1);'
    'tl.fromTo(".p3o", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.fromTo(".cloth", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.5}, 0.5);'
    'tl.to(".pour", {opacity:0.2, duration:0.9, yoyo:true, repeat:-1}, 0.6);'
    'tl.fromTo(".lb4", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".p4o, .p4i", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.1);'
    'tl.fromTo(".ev4", {opacity:0}, {opacity:1, duration:0.6}, 0.4);'
    'tl.to(".ar0, .ar1, .ar2, .ar3, .ar4", {y:-26, opacity:0.15, duration:1.4, stagger:0.15, repeat:-1, ease:"sine.out"}, 0.8);'
    'tl.fromTo(".hl, .lb5", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".p5o", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".v5", {opacity:0, scale:0.9, transformOrigin:"820px 900px"}, {opacity:1, scale:1, duration:0.6}, 0.5);'
    'tl.fromTo(".th5", {opacity:0, x:20}, {opacity:1, x:0, duration:0.5}, 0.7);'
    'tl.to(".merc", {scaleY:0.7, transformOrigin:"880px 1150px", duration:1.6, ease:"sine.out"}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".th6", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.to(".merc", {scaleY:0.8, transformOrigin:"300px 900px", duration:1.8, ease:"sine.out"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".p7o", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".ev7", {opacity:0}, {opacity:1, duration:0.6}, 0.4);'
    'tl.to(".ar0, .ar1, .ar2", {y:-20, opacity:0.2, duration:1.3, stagger:0.15, repeat:-1, ease:"sine.out"}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".rib", {opacity:0, y:-16}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".p8a", {opacity:0}, {opacity:1, duration:0.6}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
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
<link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,700;0,800;0,900;1,700;1,800&display=swap" rel="stylesheet">
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
