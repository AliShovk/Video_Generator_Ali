#!/usr/bin/env python3
"""«Как замешать бетон» — 8 сцен, инфографика."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/concrete")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#eef1f3"
INK = "#23272b"
CEM = "#b9bfc4"
SAND = "#e8c766"
GRAV = "#8f9aa2"
WATER = "#4da3ff"
RED = "#cf3a2a"
OK = "#3f9d4a"
WHITE = "#ffffff"


def S(d, w=7, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, op=1.0, cls="fillshape", stroke=INK, sw=6):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=54, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def bucket(x, y, col, num="", label="", s=1.0, cls="bkt"):
    """Ведро: трапеция + ручка."""
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M -70 -130 L 70 -130 L 54 0 L -54 0 Z" fill="{col}" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="-130" rx="70" ry="18" fill="{WHITE}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M -70 -130 q 0 -58 70 -58 q 70 0 70 58" fill="none" stroke="{INK}" stroke-width="7"/>'
            f'<text x="0" y="-58" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{INK}" '
            f'text-anchor="middle" opacity="0.75">{num}</text></g>')


def grain(seed, n=140):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.5):.1f}" '
                   f'fill="#9aa3aa" opacity="{r.uniform(0.04,0.1):.2f}"/>' for _ in range(n))


def slab(x, y, w, h, col=CEM, cls="slab"):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}" stroke="{INK}" stroke-width="6"/>'


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(1)]
    b.append(slab(110, 1180, 860, 240, "#c9ced2"))
    b.append(f'<path class="crack1" d="M 380 1180 l 40 80 l -30 60 l 60 100" stroke="{RED}" stroke-width="9" fill="none"/>')
    b.append(f'<path d="M 700 1180 l -30 70 l 40 60" stroke="{RED}" stroke-width="7" fill="none"/>')
    b.append(bucket(760, 1080, WATER, "", "", 0.9, "pour1"))
    b.append(f'<path class="spill1" d="M 700 1060 q -40 60 -20 120" stroke="{WATER}" stroke-width="14" fill="none"/>')
    b.append(txt(80, 330, "БЕТОН СЛАБЫЙ", 62, INK))
    b.append(txt(80, 410, "ПОТОМУ ЧТО ВОДА НА ГЛАЗ", 32, RED))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(2)]
    b.append(txt(80, 260, "ЧЕТЫРЕ ЧАСТИ", 58))
    items = [("1", "ЦЕМЕНТ", CEM), ("2", "ПЕСОК", SAND), ("3", "ЩЕБЕНЬ", GRAV), ("4", "ВОДА", WATER)]
    for i, (num, name, col) in enumerate(items):
        x = 155 + i * 255
        b.append(bucket(x, 1010, col, num, name, 1.12, f"b2{i}"))
        b.append(txt(x, 1120, name, 30, INK, "middle", "hl"))
        if i < 3:
            b.append(f'<path class="arrow2" d="M {x+105} 920 l 62 0 M {x+152} 903 l 22 17 l -22 17" stroke="{INK}" stroke-width="7" fill="none"/>')
    b.append(txt(80, 1400, "объём, не вес", 30, "#5c666e"))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(3)]
    b.append(txt(80, 250, "ПРОПОРЦИЯ 1 : 2 : 4", 50))
    parts = [("1", CEM, 180, 0.95), ("2", SAND, 470, 1.18), ("4", GRAV, 790, 1.42)]
    for num, col, x, s in parts:
        b.append(bucket(x, 1060, col, num, "", s, f"b3{num}"))
    b.append(txt(180, 1190, "ЦЕМЕНТ", 30, INK, "middle"))
    b.append(txt(470, 1230, "ПЕСОК", 30, INK, "middle"))
    b.append(txt(790, 1290, "ЩЕБЕНЬ", 30, INK, "middle"))
    b.append(txt(540, 1450, "+ вода 0,5 от цемента", 36, "#2f6fa8", "middle"))
    b.append(txt(80, 1620, "М200–М300 ДЛЯ СТЯЖКИ И ФУНДАМЕНТА", 24, "#5c666e"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(4)]
    b.append(F("M 90 1330 q 160 -300 430 -280 q 260 20 370 280 z", CEM, 0.95, "pile4"))
    b.append(F("M 480 1360 q 100 -220 280 -205 q 190 15 250 205 z", SAND, 0.9, "pile4b"))
    # лопата
    b.append(f'<g class="shovel4" transform="translate(60 250)"><path d="M 760 640 L 640 940" stroke="#8a6a3a" stroke-width="16" stroke-linecap="round"/>'
             f'<path d="M 600 930 q 60 -30 100 30 q -30 70 -100 40 z" fill="#b9bfc4" stroke="{INK}" stroke-width="6"/></g>')
    b.append(txt(80, 260, "СНАЧАЛА СУХОЕ", 56))
    b.append(txt(80, 330, "цемент + песок, потом щебень", 30, "#5c666e"))
    b.append(txt(80, 1640, "ВОДУ ПОКА НЕ ЛЬЁМ", 34, RED))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(5)]
    b.append(F("M 90 1360 q 240 -300 470 -280 q 300 20 390 280 z", "#b0a08a", 0.95, "mix5"))
    b.append(f'<path class="hose5" d="M 1080 540 q -300 70 -460 220" stroke="#2e8b57" stroke-width="20" fill="none"/>')
    b.append(f'<path class="water5" d="M 620 760 q 30 180 -20 330" stroke="{WATER}" stroke-width="20" fill="none"/>')
    for i in range(5):
        b.append(f'<circle class="drop5" cx="{600 + i*14}" cy="{1090 + i*18}" r="12" fill="{WATER}"/>')
    b.append(txt(80, 260, "ВОДА — ПОСТЕПЕННО", 48))
    b.append(txt(80, 330, "не всю сразу", 30, "#5c666e"))
    b.append(f'<ellipse cx="600" cy="1100" rx="46" ry="14" fill="{WATER}" opacity="0.5"/>')
    b.append(txt(80, 1640, "СУХАЯ СМЕСЬ → ВЛАЖНАЯ → ОДНОРОДНАЯ", 24, "#5c666e"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(6)]
    b.append(f'<rect x="110" y="620" width="860" height="640" rx="24" fill="#b6b3ac" stroke="{INK}" stroke-width="8"/>')
    r = random.Random(11)
    for i in range(120):
        b.append(f'<circle class="agg6" cx="{r.uniform(130,950):.0f}" cy="{r.uniform(640,1240):.0f}" '
                 f'r="{r.uniform(6,18):.0f}" fill="#8f9aa2" opacity="0.75"/>')
    b.append('<g class="ok6"><path d="M 700 1400 l 46 54 l 92 -120" stroke="#3f9d4a" stroke-width="22" fill="none" stroke-linecap="round"/></g>')
    b.append(txt(80, 320, "ОДНОРОДНО", 58))
    b.append(txt(80, 390, "цвет одинаковый · комков нет", 28, "#5c666e"))
    b.append(txt(80, 1700, "СУХИХ КАРМАНОВ ОСТАТЬСЯ НЕ ДОЛЖНО", 26, "#5c666e"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(7)]
    b.append(txt(80, 260, "ВОДА / ЦЕМЕНТ = 0,5", 46))
    b.append(txt(80, 330, "по весу", 26, "#5c666e"))
    bars = [("0,4", 0.95, "#3f9d4a"), ("0,5", 0.85, "#3f9d4a"), ("0,6", 0.65, "#e0a12a"), ("0,7", 0.5, RED)]
    for i, (lab, h, col) in enumerate(bars):
        x = 150 + i * 210
        hh = 520 * h
        b.append(f'<rect class="bar7" x="{x}" y="{1200 - hh}" width="120" height="{hh}" rx="8" fill="{col}" stroke="{INK}" stroke-width="5"/>')
        b.append(txt(x + 60, 1260, lab, 30, INK, "middle"))
    b.append(txt(80, 1400, "БОЛЬШЕ ВОДЫ — НИЖЕ ПРОЧНОСТЬ", 28, RED))
    b.append(txt(80, 1500, "лишняя вода испаряется и оставляет поры", 24, "#5c666e"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(8)]
    b.append(slab(110, 1080, 860, 200, "#c9ced2"))
    b.append(f'<rect class="film8" x="110" y="1040" width="860" height="60" rx="10" fill="#bfe3f5" opacity="0.85" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<g class="cal8"><rect x="640" y="420" width="330" height="330" rx="18" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>'
             f'<rect x="640" y="420" width="330" height="80" rx="18" fill="{RED}" stroke="{INK}" stroke-width="7"/>'
             f'<text x="805" y="600" font-family="Nunito, Arial" font-size="90" font-weight="900" fill="{INK}" text-anchor="middle">7</text>'
             f'<text x="805" y="700" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#5c666e" text-anchor="middle">дней</text></g>')
    b.append(txt(80, 300, "УХОД", 58))
    b.append(txt(80, 370, "накрыть плёнкой, не сушить", 28, "#5c666e"))
    b.append(txt(80, 1480, "7 ДНЕЙ — НАБОР, 28 — ПРОЕКТНАЯ", 28, "#2f6fa8"))
    b.append(txt(80, 1600, "ПОЛИВАТЬ ВОДОЙ ПЕРВЫЕ СУТКИ", 26, "#5c666e"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.1}, 0.1);'
    'tl.to(".fillshape", {opacity:1, duration:0.5, stagger:0.1}, 0.2);'
    'tl.to(".crack1", {opacity:0.4, duration:0.4, yoyo:true, repeat:4}, 0.6);'
    'tl.fromTo(".pour1", {rotation:-20, transformOrigin:"50% 0%"}, {rotation:0, duration:0.8}, 0.3);'
    'tl.to(".spill1", {opacity:0.5, duration:0.5, yoyo:true, repeat:3}, 0.6);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.6, stagger:0.08}, 0.1);'
    'tl.fromTo(".bkt", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.5, stagger:0.25, ease:"back.out(2)"}, 0.2);'
    'tl.fromTo(".arrow2", {opacity:0}, {opacity:1, duration:0.3, stagger:0.2}, 0.8);',
    'tl.fromTo(".bkt", {scale:0.4, opacity:0}, {scale:1, opacity:1, duration:0.5, stagger:0.3, ease:"back.out(2)"}, 0.2);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.6, stagger:0.1}, 0.3);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.1}, 0.1);'
    'tl.to(".fillshape", {opacity:1, duration:0.6}, 0.2);'
    'tl.fromTo(".shovel4", {rotation:18, transformOrigin:"70% 80%"}, {rotation:-14, duration:1.0, yoyo:true, repeat:2, ease:"sine.inOut"}, 0.3);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8}, 0.1);'
    'tl.to(".fillshape", {opacity:1, duration:0.6}, 0.2);'
    'tl.to(".drop5", {y:220, opacity:0, duration:0.9, stagger:0.12, repeat:3, ease:"power1.in"}, 0.3);'
    'tl.fromTo(".hose5", {opacity:0}, {opacity:1, duration:0.6}, 0.1);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8}, 0.1);'
    'tl.fromTo(".agg6", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, stagger:0.005, ease:"power1.out"}, 0.3);'
    'tl.fromTo(".ok6", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 1.6);',
    'tl.fromTo(".bar7", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.6, stagger:0.2, ease:"power2.out"}, 0.2);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.6, stagger:0.08}, 0.1);',
    'tl.fromTo(".film8", {scaleX:0.2, transformOrigin:"0% 50%"}, {scaleX:1, duration:1.0, ease:"power2.out"}, 0.3);'
    'tl.fromTo(".cal8", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.6, ease:"back.out(2)"}, 0.6);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.6}, 0.1);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.03, duration:{dur}, ease:"none" }}, 0);
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
