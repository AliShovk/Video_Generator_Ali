#!/usr/bin/env python3
"""«Фундамент на склоне: cut / fill» — 8 сцен, скетч-стиль."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/slope")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

PAPER = "#f4ede0"
INK = "#2b2b2b"
EARTH = "#cfa877"
EARTH_D = "#b98c55"
CONC = "#cfd8dc"
CONC_D = "#9aa7ae"
GREEN = "#7fa063"
RED = "#d2452f"
OK = "#3f9d4a"
SKY = "#eaf1f4"


def S(d, w=7, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, op=1.0, cls="fillshape"):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}"/>'


def txt(x, y, s, size=54, col=INK, anchor="start", cls="hl", font="Nunito, Arial"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def hand(x, y, s, size=72, col=INK, anchor="middle", rot=-4):
    return (f'<text class="hand" x="{x}" y="{y}" font-family="Caveat, Nunito, cursive" font-size="{size}" '
            f'font-weight="700" fill="{col}" text-anchor="{anchor}" transform="rotate({rot} {x} {y})">{s}</text>')


def grain(seed=7, n=200):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.6):.1f}" '
                   f'fill="#8a7f6a" opacity="{r.uniform(0.04,0.12):.2f}"/>' for _ in range(n))


def slope(y0=760, y1=1440):
    return f"M 0 {y0} L 1080 {y1} L 1080 1920 L 0 1920 Z"


def tree(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M 0 0 L 0 -120" stroke="#6b4a2a" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M 0 -70 L -50 -120 M 0 -90 L 48 -140" stroke="#6b4a2a" stroke-width="10" stroke-linecap="round"/>'
            f'<ellipse cx="-30" cy="-190" rx="78" ry="58" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="60" cy="-210" rx="66" ry="50" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="10" cy="-255" rx="72" ry="54" fill="{GREEN}" stroke="{INK}" stroke-width="5"/>'
            f'</g>')


def person(x, y, s=1.0, cls="person"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="-96" r="20" fill="#f0c9a0" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M -20 -76 L 20 -76 L 24 -14 L -24 -14 Z" fill="#f5d94e" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M -18 -14 L -18 22 M 18 -14 L 18 22" stroke="{INK}" stroke-width="9"/>'
            f'<path d="M -24 -70 L -40 -30 M 24 -70 L 40 -30" stroke="{INK}" stroke-width="7"/></g>')


def foundation(x, top, w=120, h=260, foot=True, cls="fnd"):
    foot_w = w + 110
    f = (f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{CONC}" stroke="{INK}" stroke-width="6"/>')
    if foot:
        f += (f'<rect x="{x - 55}" y="{top + h - 60}" width="{foot_w}" height="70" fill="{CONC}" '
              f'stroke="{INK}" stroke-width="6"/>')
    return f'<g class="{cls}">{f}</g>'


def house(x, y, w=300, h=190):
    return (f'<g><path d="M {x} {y} l {w/2} -110 l {w/2} 110 Z" fill="#5a5f63" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#efe6d4" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="{x+40}" y="{y+50}" width="70" height="70" fill="{SKY}" stroke="{INK}" stroke-width="4"/>'
            f'<rect x="{x+180}" y="{y+40}" width="60" height="150" fill="#8a6a4a" stroke="{INK}" stroke-width="4"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(1)]
    b.append(F(slope(700, 1420), EARTH))
    b.append(S("M 0 700 L 1080 1420", 9, INK))
    b.append(F(slope(700, 1420), EARTH))
    b.append(tree(180, 820, 0.85))
    b.append(house(520, 950, 320, 200))
    b.append(hand(90, 330, "дом на склоне", 92, INK, "start"))
    b.append(txt(70, 1720, "ОДНА ОШИБКА — И ОН ПОЕДЕТ", 40, RED))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(2)]
    b.append(F(slope(700, 1420), EARTH))
    b.append(S("M 0 700 L 1080 1420", 9))
    # срез: вырезаем клин
    b.append(F("M 300 950 L 300 1290 L 900 1290 L 900 1330 L 300 1330 Z", PAPER))
    b.append(S("M 300 950 L 300 1290", 9))
    b.append(S("M 300 1290 L 1000 1290", 9))
    b.append(S("M 300 950 L 1000 1290", 5, INK, "draw", 'stroke-dasharray="14 12"'))
    b.append(foundation(330, 900, 130, 320))
    b.append(person(640, 1240, 1.1))
    b.append(hand(760, 800, "CUT", 92, INK, "middle", -6))
    b.append(S("M 700 830 q -40 90 -90 130", 5))
    b.append('<g class="cross2"><path d="M 840 900 l 120 120 M 960 900 l -120 120" stroke="#d2452f" stroke-width="22" stroke-linecap="round"/></g>')
    b.append(txt(70, 1720, "ГЛУБОКИЙ СРЕЗ + ОДНА ОПОРА", 38, RED))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(3)]
    b.append(F(slope(700, 1420), EARTH))
    b.append(S("M 0 700 L 1080 1420", 8))
    b.append(f'<g class="tilt3"><rect x="250" y="860" width="130" height="430" fill="{CONC}" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="195" y="1230" width="240" height="70" fill="{CONC}" stroke="{INK}" stroke-width="6"/></g>')
    for i in range(4):
        b.append(f'<path class="slide3" d="M {420 + i*120} 1180 q 60 90 120 140" stroke="{RED}" stroke-width="9" fill="none" opacity="0.9"/>')
        b.append(f'<path d="M {540 + i*120} 1320 l -16 -34 l 34 6 z" fill="{RED}"/>')
    b.append(txt(70, 420, "ГРУНТ СПОЛЗАЕТ", 52, RED))
    b.append(txt(70, 500, "ОПОРА БЕЗ УПОРА", 40, INK))
    b.append(txt(70, 1720, "КРЕН · ТРЕЩИНЫ · ПЕРЕКОС", 34, INK))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(4)]
    b.append(F(slope(700, 1420), EARTH))
    b.append(S("M 0 700 L 1080 1420", 9))
    b.append(F("M 200 820 L 800 820 L 800 1233 L 200 833 Z", EARTH_D, 0.85))
    for i in range(9):
        b.append(f'<path d="M {230 + i*64} 838 L {250 + i*64} 1215" stroke="#8a6a3a" stroke-width="3" opacity="0.5"/>')
    b.append(foundation(200, 820, 110, 260, True, "f4a"))
    b.append(foundation(450, 900, 110, 300, True, "f4b"))
    b.append(foundation(700, 1000, 110, 330, True, "f4c"))
    b.append(house(190, 590, 620, 230))
    b.append('<g class="ok4"><path d="M 820 860 l 60 70 l 110 -140" stroke="#3f9d4a" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    b.append(txt(70, 1720, "СТУПЕНЧАТЫЙ ФУНДАМЕНТ", 40, OK))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(5)]
    b.append(F(slope(700, 1420), EARTH))
    b.append(S("M 0 700 L 1080 1420", 9))
    b.append(foundation(200, 820, 100, 260, True, "f5a"))
    b.append(foundation(470, 950, 100, 300, True, "f5b"))
    b.append(F("M 470 950 L 1000 950 L 1000 1400 L 470 1400 Z", EARTH_D, 0.9))
    for yy in range(965, 1400, 26):
        b.append(S(f"M 480 {yy} L 990 {yy}", 3, "#8a6a3a"))
    b.append(hand(230, 830, "CUT", 88, INK, "middle", -8))
    b.append(S("M 250 860 q 10 60 -10 90", 5))
    b.append(hand(760, 1080, "FILL", 88, INK, "middle", 5))
    b.append(S("M 760 1120 q -20 50 -40 70", 5))
    b.append(txt(70, 1720, "СРЕЗ СВЕРХУ · ПОДСЫПКА СНИЗУ", 34))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(6)]
    b.append(F(slope(760, 1420), EARTH))
    b.append(S("M 0 760 L 1080 1420", 9))
    # карьер под подсыпку
    b.append(F("M 170 980 L 910 980 L 910 1560 L 170 1560 Z", "#a97f4c"))
    b.append(S("M 170 980 L 910 980 L 910 1560 L 170 1560 Z", 6))
    cols = ["#c9a878", "#bd9260", "#c9a878", "#bd9260", "#c9a878", "#bd9260"]
    for i, yy in enumerate(range(980, 1560, 96)):
        b.append(f'<rect class="layer6" x="172" y="{yy}" width="736" height="94" fill="{cols[i%6]}" opacity="0"/>')
        b.append(f'<path class="layer6" d="M 176 {yy} L 906 {yy}" stroke="#8a6a3a" stroke-width="4" opacity="0"/>')
    b.append(f'<g class="plate6"><rect x="330" y="880" width="420" height="44" rx="6" fill="#9aa7ae" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="490" y="800" width="100" height="86" fill="#6f7a80" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 330 830 L 330 872 M 750 830 L 750 872" stroke="{RED}" stroke-width="7"/></g>')
    b.append(hand(780, 800, "20 см", 74, RED, "start", 5))
    b.append(S("M 300 1000 L 300 1060 M 260 1000 L 260 1060 M 260 1030 L 300 1030", 4, INK))
    b.append(txt(70, 340, "ТРАМБОВКА СЛОЯМИ", 46))
    b.append(txt(70, 410, "не толще 20 сантиметров", 30, "#6b5a44"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(7)]
    b.append(F(slope(760, 1420), EARTH))
    b.append(S("M 0 760 L 1080 1420", 9))
    b.append(foundation(420, 980, 120, 300))
    b.append(F("M 300 1290 L 520 1290 L 520 1400 L 300 1400 Z", "#b9c0c4", 0.95))
    b.append(S("M 300 1290 L 520 1290", 5))
    for i in range(6):
        b.append(f'<circle cx="{320 + i*32}" cy="{1330 + (i%2)*30}" r="11" fill="#8f979b" stroke="{INK}" stroke-width="3"/>')
    b.append('<path class="frost7" d="M 0 1180 q 540 260 1080 240" stroke="#4da3ff" stroke-width="6" stroke-dasharray="16 12" fill="none"/>')
    b.append(txt(60, 1140, "ГЛУБИНА ПРОМЕРЗАНИЯ", 28, "#2f6fa8"))
    b.append(F("M 640 1130 L 960 1180 L 960 1235 L 640 1185 Z", "#d8cbb4", 0.95))
    b.append(S("M 640 1130 L 960 1180 L 960 1235 L 640 1185 Z", 4))
    b.append(txt(660, 1120, "ОТМОСТКА", 26, "#6b5a44"))
    b.append(hand(700, 900, "дренаж", 76, "#2f6fa8", "start", -3))
    b.append(txt(70, 1720, "НИЖЕ ПРОМЕРЗАНИЯ + ВОДА ОТВЕДЕНА", 30))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(8)]
    b.append(F(slope(700, 1420), EARTH))
    b.append(S("M 0 700 L 1080 1420", 9))
    b.append(F("M 180 820 L 780 820 L 780 1220 L 180 833 Z", EARTH_D, 0.85))
    for i in range(9):
        b.append(f'<path d="M {210 + i*62} 838 L {230 + i*62} 1200" stroke="#8a6a3a" stroke-width="3" opacity="0.5"/>')
    b.append(foundation(180, 820, 105, 250, True, "f8a"))
    b.append(foundation(420, 900, 105, 300, True, "f8b"))
    b.append(foundation(660, 1000, 105, 330, True, "f8c"))
    b.append(house(170, 590, 620, 230))
    b.append('<g class="ok8"><path d="M 800 1020 l 60 70 l 110 -140" stroke="#3f9d4a" stroke-width="24" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>')
    b.append(hand(540, 1620, "стоит десятилетиями", 80, INK, "middle", -3))
    b.append(txt(70, 1740, "СТУПЕНИ · ТРАМБОВКА · ГЕОЛОГИЯ", 28, "#6b5a44"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:1.1, stagger:0.12, ease:"none"}, 0.1);'
    'tl.to(".fillshape", {opacity:1, duration:0.7, stagger:0.15}, 0.2);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.08, ease:"none"}, 0.1);'
    'tl.to(".fillshape", {opacity:1, duration:0.5, stagger:0.08}, 0.2);'
    'tl.fromTo(".cross2", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 1.2);',
    'tl.fromTo(".tilt3", {rotation:0, transformOrigin:"50% 100%"}, {rotation:5, duration:2.2, ease:"sine.inOut"}, 0.3);'
    'tl.to(".slide3", {y:60, opacity:0.5, duration:1.2, stagger:0.15, repeat:2, ease:"power1.inOut"}, 0.4);',
    'tl.fromTo(".f4a", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"back.out(2)"}, 0.2);'
    'tl.fromTo(".f4b", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"back.out(2)"}, 0.7);'
    'tl.fromTo(".f4c", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"back.out(2)"}, 1.2);'
    'tl.fromTo(".fillshape", {opacity:0}, {opacity:0.85, duration:0.8}, 1.6);'
    'tl.fromTo(".ok4", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 2.2);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.7, stagger:0.05}, 0.1);'
    'tl.to(".fillshape", {opacity:0.9, duration:0.6}, 0.3);'
    'tl.fromTo(".hand", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.4}, 0.8);',
    'tl.to(".layer6", {opacity:1, duration:0.4, stagger:0.25}, 0.3);'
    'tl.fromTo(".plate6", {y:-120, opacity:0}, {y:0, opacity:1, duration:0.7, ease:"power2.out"}, 0.6);'
    'tl.to(".plate6", {y:26, duration:0.5, yoyo:true, repeat:2, ease:"power1.inOut"}, 1.6);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.1}, 0.1);'
    'tl.to(".fillshape", {opacity:0.95, duration:0.6, stagger:0.1}, 0.3);'
    'tl.to(".frost7", {opacity:0.35, duration:0.7, yoyo:true, repeat:3}, 0.8);',
    'tl.fromTo(".f8a", {y:-70, opacity:0}, {y:0, opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".f8b", {y:-70, opacity:0}, {y:0, opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".f8c", {y:-70, opacity:0}, {y:0, opacity:1, duration:0.5}, 0.9);'
    'tl.fromTo(".ok8", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 1.4);'
    'tl.fromTo(".hand", {opacity:0}, {opacity:1, duration:0.8}, 2.0);',
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.04, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:18 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.08 }}, 0.05);
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
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
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
