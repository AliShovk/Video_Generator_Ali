#!/usr/bin/env python3
"""«Вода из тумана» — 8 сцен, плоская иллюстрация."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/fog")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

SKY = "#cfe6f2"
HILL = "#b9c98a"
HILL_D = "#9fb46f"
INK = "#2b2b2b"
WOOD = "#a9763f"
MESH = "#8f9aa2"
WATER = "#4da3ff"
SUN = "#f2c14e"
GREEN = "#5b9e4a"
TANK = "#5f7d8c"

DEFS = """<defs>
<pattern id="meshP" width="26" height="26" patternUnits="userSpaceOnUse">
  <path d="M 0 0 L 26 0 M 0 0 L 0 26" stroke="#6f7a82" stroke-width="3" opacity="0.85"/>
</pattern>
<linearGradient id="waterG" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#7fc3ff"/><stop offset="1" stop-color="#3f8fd8"/>
</linearGradient>
</defs>"""


def S(d, w=7, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, op=1.0, cls="fillshape", stroke="none", sw=0):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke != "none" else ""
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}"{st}/>'


def txt(x, y, s, size=54, col=INK, anchor="start", cls="hl", weight=900):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{weight}" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def hills(y=1150):
    return (f'<path d="M 0 {y+160} Q 180 {y-70} 380 {y+40} Q 560 {y+150} 720 {y+20} Q 900 {y-110} 1080 {y+60} '
            f'L 1080 1920 L 0 1920 Z" fill="{HILL}" stroke="{INK}" stroke-width="6"/>')


def fog(cx, cy, w=900, op=0.9, cls="fog"):
    return (f'<g class="{cls}" opacity="{op}"><ellipse cx="{cx}" cy="{cy}" rx="{w*0.5}" ry="90" fill="#ffffff"/>'
            f'<ellipse cx="{cx-w*0.22}" cy="{cy+30}" rx="{w*0.3}" ry="70" fill="#ffffff"/>'
            f'<ellipse cx="{cx+w*0.2}" cy="{cy+26}" rx="{w*0.32}" ry="78" fill="#ffffff"/>'
            f'<ellipse cx="{cx+w*0.05}" cy="{cy-40}" rx="{w*0.26}" ry="64" fill="#ffffff"/></g>')


def meshPanel(x, y, w, h):
    return (f'<g class="meshG"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#meshP)" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{WOOD}" stroke-width="14"/></g>')


def post(x, ytop, ybot):
    return f'<rect class="postG" x="{x-16}" y="{ytop}" width="32" height="{ybot-ytop}" fill="{WOOD}" stroke="{INK}" stroke-width="6"/>'


def trough(x, y, w):
    return (f'<g class="troughG"><path d="M {x} {y} l {w} 0 l -18 56 l {-w+36} 0 z" fill="#9fb8c8" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M {x+22} {y-8} l {w-44} 0" stroke="{WATER}" stroke-width="10"/></g>')


def tank(x, y, w, h, level=0.0, cls="tankG"):
    inner = h - 24
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="46" fill="{TANK}" stroke="{INK}" stroke-width="7"/>'
            f'<clipPath id="tk{int(x)}"><rect x="{x+8}" y="{y+8}" width="{w-16}" height="{h-16}" rx="40"/></clipPath>'
            f'<g clip-path="url(#tk{int(x)})"><rect class="tankFill" x="{x+8}" y="{y + h - 8 - inner*level}" '
            f'width="{w-16}" height="{inner*level}" fill="url(#waterG)"/></g>'
            f'<rect x="{x-14}" y="{y-18}" width="{w+28}" height="30" rx="10" fill="{TANK}" stroke="{INK}" stroke-width="6"/></g>')


def plant(x, y, s=1.0, cls="plantG"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M 0 0 L 0 -50" stroke="{GREEN}" stroke-width="8"/>'
            f'<ellipse cx="-22" cy="-58" rx="24" ry="14" fill="{GREEN}" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="22" cy="-58" rx="24" ry="14" fill="{GREEN}" stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="0" cy="-72" r="16" fill="#e8734a" stroke="{INK}" stroke-width="4"/></g>')


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>']
    b.append(f'<circle cx="880" cy="300" r="90" fill="{SUN}" stroke="{INK}" stroke-width="6"/>')
    b.append(hills(1150))
    b.append(f'<path d="M 120 1500 q 120 -40 240 0 M 600 1620 q 140 -30 280 0" stroke="{INK}" stroke-width="4" fill="none" opacity="0.4"/>')
    b.append(f'<g opacity="0.9"><rect x="640" y="1180" width="120" height="80" fill="#e8dcc4" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 620 1180 L 700 1120 L 780 1180 Z" fill="#c0603f" stroke="{INK}" stroke-width="5"/></g>')
    b.append(txt(70, 300, "ВОДА ИЗ ТУМАНА", 58, INK))
    b.append(txt(70, 380, "ТАМ, ГДЕ НЕТ ДОЖДЯ", 30, "#5c666e"))
    b.append(txt(70, 1740, "ПРОСТО СЕТКА И ВЕТЕР", 30, "#5c666e"))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>']
    b.append(hills(1120))
    b.append(post(180, 780, 1500))
    b.append(post(860, 780, 1500))
    b.append(meshPanel(196, 800, 648, 520))
    b.append(fog(540, 880, 1100, 0.95, "fog2"))
    b.append(txt(70, 300, "ТУМАН = ВОДА", 56))
    b.append(txt(70, 370, "мелкие капли в воздухе", 28, "#5c666e"))
    b.append(txt(70, 1740, "ВЕТЕР НЕСЁТ ИХ ЧЕРЕЗ СЕТКУ", 26, "#5c666e"))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="#e9f2f7"/>']
    # крупная сетка
    for i in range(9):
        b.append(f'<line class="thread3" x1="{120 + i*100}" y1="560" x2="{120 + i*100}" y2="1400" stroke="{MESH}" stroke-width="7"/>')
    for j in range(7):
        b.append(f'<line class="thread3" x1="120" y1="{560 + j*140}" x2="920" y2="{560 + j*140}" stroke="{MESH}" stroke-width="7"/>')
    r = random.Random(3)
    for i in range(18):
        b.append(f'<circle class="drop3" cx="{r.uniform(140,900):.0f}" cy="{r.uniform(580,1380):.0f}" '
                 f'r="{r.uniform(8,18):.0f}" fill="{WATER}" opacity="0.95"/>')
    b.append(f'<path class="wind3" d="M 40 480 q 300 -60 600 0" stroke="{INK}" stroke-width="6" fill="none" stroke-dasharray="14 12"/>')
    b.append(txt(70, 300, "КАПЛИ ЦЕПЛЯЮТСЯ", 50))
    b.append(txt(70, 1640, "ячейка около 1 см", 30, "#5c666e"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>']
    b.append(hills(1240))
    b.append(post(170, 640, 1560))
    b.append(post(870, 640, 1560))
    b.append(meshPanel(186, 660, 668, 560))
    b.append(f'<path class="guy4" d="M 170 660 L 60 1520 M 870 660 L 990 1520" stroke="{INK}" stroke-width="5" fill="none"/>')
    b.append(trough(150, 1290, 790))
    b.append(txt(60, 300, "КОНСТРУКЦИЯ", 54))
    b.append(txt(60, 360, "две стойки · сетка · жёлоб", 28, "#5c666e"))
    b.append(txt(300, 1430, "ЖЁЛОБ", 28, INK))
    b.append(txt(760, 640, "СЕТКА", 28, INK, "end"))
    b.append(txt(70, 1740, "РАСТЯЖКИ ДЕРЖАТ ОТ ВЕТРА", 24, "#5c666e"))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="#eef5f9"/>']
    b.append(meshPanel(200, 420, 680, 520))
    b.append(trough(160, 980, 780))
    for i in range(8):
        x = 260 + i * 80
        b.append(f'<circle class="drip5" cx="{x}" cy="{900 - (i%3)*40}" r="14" fill="{WATER}"/>')
        b.append(f'<path class="run5" d="M {x} 940 l 0 40" stroke="{WATER}" stroke-width="9" stroke-linecap="round"/>')
    b.append(f'<rect class="water5" x="180" y="1000" width="740" height="26" fill="{WATER}" opacity="0.9"/>')
    b.append(txt(60, 300, "СТЕКАЮТ В ЖЁЛОБ", 50))
    b.append(txt(60, 1560, "МЕЛКИЕ КАПЛИ → КРУПНЫЕ → ВОДА", 26, "#5c666e"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>', hills(1300)]
    b.append(trough(90, 520, 520))
    b.append(f'<path class="pipe6" d="M 350 590 L 350 780 L 470 780" stroke="{MESH}" stroke-width="26" fill="none"/>')
    # фильтры
    b.append(f'<g class="filt6"><rect x="450" y="700" width="90" height="180" rx="18" fill="#dfe7ec" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="560" y="700" width="90" height="180" rx="18" fill="#dfe7ec" stroke="{INK}" stroke-width="6"/>'
             f'<text x="495" y="940" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{INK}" text-anchor="middle">фильтры</text></g>')
    b.append(f'<path class="pipe6b" d="M 650 790 L 760 790 L 760 900" stroke="{MESH}" stroke-width="24" fill="none"/>')
    b.append(tank(640, 900, 330, 400, 0.35, "tank6"))
    b.append(txt(60, 300, "ФИЛЬТРЫ И БАК", 52))
    b.append(txt(60, 1640, "МУСОР И ПЕСОК — В ФИЛЬТРАХ", 24, "#5c666e"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>', hills(1420)]
    b.append(tank(120, 700, 300, 360, 0.75, "tank7"))
    b.append(f'<path class="pipe7" d="M 420 880 L 560 880" stroke="{MESH}" stroke-width="22" fill="none"/>')
    b.append(f'<g class="tap7"><rect x="556" y="836" width="66" height="76" rx="10" fill="{MESH}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 622 862 l 44 0 q 18 0 18 18 l 0 34" fill="none" stroke="{MESH}" stroke-width="18" stroke-linecap="round"/>'
             f'<path d="M 574 806 l 30 0" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g>')
    b.append(f'<path class="jet7" d="M 684 918 l 0 82" stroke="{WATER}" stroke-width="13"/>')
    b.append(f'<g class="cup7"><path d="M 646 1000 l 76 0 l -10 92 l -56 0 z" fill="#eaf6ff" stroke="{INK}" stroke-width="5"/></g>')
    b.append(f'<rect x="700" y="1400" width="340" height="70" rx="10" fill="#7a5a3a" stroke="{INK}" stroke-width="5"/>')
    for i, x in enumerate((770, 880, 990)):
        b.append(plant(x, 1420, 1.5, f"p7{i}"))
        b.append(f'<path class="drip7" d="M {x} 1300 l 0 30" stroke="{WATER}" stroke-width="10" stroke-dasharray="6 14"/>')
    b.append(txt(60, 300, "ПИТЬЁ И ПОЛИВ", 54))
    b.append(txt(60, 1680, "БЕЗ НАСОСА — САМОТЁКОМ", 26, "#5c666e"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>', hills(1250)]
    b.append(meshPanel(140, 700, 420, 380))
    b.append(f'<path class="flow8" d="M 350 1080 l 0 120" stroke="{WATER}" stroke-width="26" stroke-linecap="round"/>')
    b.append(tank(620, 780, 340, 380, 0.7, "tank8"))
    b.append(txt(80, 380, "40 м²", 96, INK))
    b.append(txt(80, 470, "сетки", 34, "#5c666e"))
    b.append(txt(80, 620, "до 300 л", 88, "#2f6fa8"))
    b.append(txt(80, 700, "в сутки", 34, "#5c666e"))
    b.append(txt(80, 1660, "НО ТОЛЬКО ТАМ, ГДЕ ТУМАН РЕГУЛЯРНЫЙ", 26, "#8a4a2f"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.1}, 0.1);'
    'tl.fromTo(".hl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.1);',
    'tl.fromTo(".fog", {x:-260, opacity:0}, {x:20, opacity:0.95, duration:1.6, ease:"sine.out"}, 0.2);'
    'tl.fromTo(".meshG", {opacity:0, scaleY:0.6, transformOrigin:"50% 100%"}, {opacity:1, scaleY:1, duration:1.0}, 0.3);'
    'tl.to(".postG", {attr:{"stroke-width":6}, duration:0.2}, 0.2);',
    'tl.fromTo(".drop3", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, stagger:0.06, ease:"back.out(2)"}, 0.2);'
    'tl.to(".wind3", {x:60, opacity:0.5, duration:1.4, yoyo:true, repeat:1}, 0.1);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.9, stagger:0.12}, 0.1);'
    'tl.fromTo(".meshG", {opacity:0}, {opacity:1, duration:0.8}, 0.3);'
    'tl.fromTo(".troughG", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"back.out(2)"}, 0.8);',
    'tl.fromTo(".drip5", {y:-120, opacity:0}, {y:0, opacity:1, duration:0.7, stagger:0.12, ease:"power2.in"}, 0.2);'
    'tl.fromTo(".water5", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.9, ease:"power2.out"}, 1.1);',
    'tl.fromTo(".filt6", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6}, 0.4);'
    'tl.fromTo(".tankFill", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.4, ease:"power2.out"}, 0.9);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.7, stagger:0.1}, 0.1);',
    'tl.fromTo(".tankFill", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.2}, 0.3);'
    'tl.to(".jet7", {opacity:0.4, duration:0.5, yoyo:true, repeat:4}, 1.2);'
    'tl.fromTo(".plantG", {scale:0.6, opacity:0}, {scale:1, opacity:1, duration:0.5, stagger:0.2}, 1.0);',
    'tl.fromTo(".flow8", {scaleY:0, transformOrigin:"50% 0%"}, {scaleY:1, duration:0.8}, 0.3);'
    'tl.fromTo(".tank8 .tankFill", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.4}, 0.6);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.7}, 0.1);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SKY}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">{svg(''.join(body))}</div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.03, duration:{dur}, ease:"none" }}, 0);
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
