#!/usr/bin/env python3
"""«Кондиционер из глиняных трубок» — 8 сцен."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/clayac")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

INK = "#2b2b2b"
TERRA = "#bf6a3e"
TERRA_D = "#a0532d"
TERRA_W = "#8d4526"
FRAME = "#8b979f"
WATER = "#4da3ff"
HOT = "#d2452f"
COOL = "#2f8fd8"
OK = "#3f9d4a"
CREAM = "#f6e3c8"


def S(d, w=7, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def txt(x, y, s, size=52, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def bg(warm=True):
    return (f'<defs><linearGradient id="bgg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{"#f6a94e" if warm else "#9fd3ee"}"/>'
            f'<stop offset="1" stop-color="{"#f7d79a" if warm else "#e6f3fa"}"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#bgg)"/>')


def pipe(x, y, r=40, wet=0.0, cls="pipe"):
    inner = TERRA_W if wet > 0.5 else "#6d3a20"
    return (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="{r}" fill="{TERRA}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.55:.0f}" fill="{inner}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.55:.0f}" fill="none" stroke="{TERRA_D}" stroke-width="6"/></g>')


def unit(y0=780, rows=7, wet=0.0, cols=6, x0=252, dy=100, dx=106, r=40, frame=True, tray=True, cls="unit"):
    b = []
    if frame:
        b.append(f'<g class="frameG"><rect x="196" y="{y0-86}" width="688" height="{rows*dy+96}" fill="none" stroke="{FRAME}" stroke-width="16"/>'
                 f'<path d="M 214 {y0+rows*dy+10} l 0 60 M 866 {y0+rows*dy+10} l 0 60" stroke="{FRAME}" stroke-width="18"/></g>')
    for ry in range(rows):
        for c in range(cols):
            b.append(pipe(x0 + c*dx, y0 + ry*dy, r, wet, f"pipe p{ry}_{c}"))
    if tray:
        ty = y0 + rows*dy + 10
        b.append(f'<g class="trayG"><rect x="196" y="{ty}" width="688" height="80" rx="10" fill="#cfd8dc" stroke="{INK}" stroke-width="6"/>'
                 f'<rect x="212" y="{ty+26}" width="656" height="42" rx="8" fill="{WATER}" opacity="0.85"/></g>')
    return "".join(b)


def manifold(y=690, x0=252, cols=6, dx=106, cls="manG"):
    b = [f'<g class="{cls}"><rect x="{x0-70}" y="{y-26}" width="{(cols-1)*dx+140}" height="46" rx="22" fill="{FRAME}" stroke="{INK}" stroke-width="5"/>']
    for c in range(cols):
        b.append(f'<path d="M {x0 + c*dx} {y+20} l 0 26" stroke="{WATER}" stroke-width="9"/>')
        b.append(f'<circle cx="{x0 + c*dx}" cy="{y+56}" r="9" fill="{WATER}"/>')
    b.append('</g>')
    return "".join(b)


def arrow(x1, y1, x2, y2, col, w=14, cls="arrow"):
    return (f'<g class="{cls}"><path d="M {x1} {y1} L {x2} {y2}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="M {x2} {y2} l -26 -12 l 4 26 z" fill="{col}"/></g>')


def thermo(x, y, frac=0.8, col=HOT, label="", cls="th"):
    h = 260
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="46" height="{h}" rx="23" fill="#fdf6ec" stroke="{INK}" stroke-width="5"/>'
            f'<rect class="thFill" x="{x+8}" y="{y + h*(1-frac) + 8}" width="30" height="{h*frac-16}" rx="15" fill="{col}"/>'
            f'<circle cx="{x+23}" cy="{y+h+26}" r="28" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            f'<text x="{x+23}" y="{y+h+96}" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{INK}" '
            f'text-anchor="middle">{label}</text></g>')


def steam(x, y, cls="steam"):
    return (f'<path class="{cls}" d="M {x} {y} q -18 -26 0 -46 q 18 -20 0 -44" stroke="#ffffff" stroke-width="7" fill="none" opacity="0.9"/>')


# ---------------------------------------------------------------- s1
def s1():
    b = [bg(True)]
    b.append(f'<circle cx="200" cy="330" r="110" fill="#f4d35e" stroke="{INK}" stroke-width="6"/>')
    for i in range(8):
        a = i * 0.785
        import math
        b.append(f'<path d="M {200 + 130*math.cos(a):.0f} {330 + 130*math.sin(a):.0f} '
                 f'L {200 + 175*math.cos(a):.0f} {330 + 175*math.sin(a):.0f}" stroke="{INK}" stroke-width="7"/>')
    b.append(unit(900, 5, 0.0, 5, 320, 96, 112, 38, True, True, "u1"))
    b.append(txt(60, 620, "КОНДИЦИОНЕР", 58, INK))
    b.append(txt(60, 690, "БЕЗ РОЗЕТКИ", 58, HOT))
    b.append(txt(60, 760, "глина · вода · ветер", 30, "#7a4a26"))
    b.append(txt(60, 1760, "0 КВТ · 0 ХЛАДАГЕНТА", 28, "#7a4a26"))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [bg(True)]
    b.append(f'<circle cx="540" cy="900" r="250" fill="{TERRA}" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<circle cx="540" cy="900" r="140" fill="#6d3a20"/>')
    b.append(f'<circle cx="540" cy="900" r="140" fill="none" stroke="{TERRA_D}" stroke-width="8"/>')
    b.append(f'<path class="drop2" d="M 540 560 q 40 60 0 96 q -40 -36 0 -96 z" fill="{WATER}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path class="air2" d="M 120 900 l 220 0" stroke="{HOT}" stroke-width="16"/>')
    b.append(f'<path class="air2b" d="M 960 860 l -220 0" stroke="{COOL}" stroke-width="16"/>')
    b.append(txt(60, 300, "ИСПАРЕНИЕ", 58))
    b.append(txt(60, 368, "вода забирает тепло", 30, "#7a4a26"))
    b.append(txt(60, 1500, "ЧЕМ СУШЕ ВОЗДУХ — ТЕМ СИЛЬНЕЕ ЭФФЕКТ", 26, "#7a4a26"))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [bg(False)]
    b.append(unit(780, 6, 0.0, 6, 252, 100, 106, 40, True, True, "u3"))
    b.append(manifold(690, 252, 6, 106, "m3"))
    b.append(txt(60, 300, "КОНСТРУКЦИЯ", 54))
    b.append(txt(60, 366, "каркас · трубки · вода · поддон", 27, "#28506b"))
    b.append(txt(60, 1720, "ГЛИНА ВПИТЫВАЕТ ВОДУ И ОТДАЁТ ЕЁ ВОЗДУХУ", 24, "#28506b"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [bg(False)]
    b.append(unit(780, 6, 0.75, 6, 252, 100, 106, 40, True, True, "u4"))
    b.append(manifold(690, 252, 6, 106, "m4"))
    for c in range(6):
        for k in range(3):
            b.append(f'<circle class="drip4" cx="{252 + c*106}" cy="{800 + k*120}" r="9" fill="{WATER}"/>')
    b.append(txt(60, 300, "ТРУБКИ ВЛАЖНЫЕ", 50))
    b.append(txt(60, 366, "вода капает сверху вниз", 27, "#28506b"))
    b.append(txt(60, 1720, "ЛИШНЯЯ ВОДА УХОДИТ В ПОДДОН", 24, "#28506b"))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [bg(True)]
    b.append(unit(820, 6, 0.7, 6, 252, 100, 106, 40, True, False, "u5"))
    for i in range(3):
        b.append(arrow(60, 900 + i*140, 320, 900 + i*140, HOT, 16, f"a5{i}"))
    b.append(txt(60, 330, "ВХОДИТ ГОРЯЧИЙ", 46))
    b.append(txt(60, 396, "сухой воздух", 30, "#7a4a26"))
    b.append(thermo(930, 620, 0.92, HOT, "+38°"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [bg(True)]
    b.append(unit(820, 6, 0.8, 6, 252, 100, 106, 40, True, False, "u6"))
    for i in range(9):
        x = 300 + (i % 3) * 200
        y = 900 + (i // 3) * 150
        b.append(steam(x, y, "st6"))
    b.append(txt(60, 330, "ВОДА ИСПАРЯЕТСЯ", 48))
    b.append(txt(60, 396, "и забирает тепло", 30, "#7a4a26"))
    b.append(thermo(930, 700, 0.55, COOL, "+26°"))
    b.append(arrow(60, 1000, 250, 1000, HOT, 15, "a6in"))
    b.append(arrow(820, 1180, 1010, 1180, COOL, 15, "a6out"))
    b.append(txt(60, 1720, "ЭТО И ЕСТЬ ОХЛАЖДЕНИЕ", 28, "#7a4a26"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [bg(False)]
    b.append(unit(780, 6, 0.5, 6, 252, 100, 106, 40, True, True, "u7"))
    for i in range(3):
        b.append(arrow(760, 900 + i*130, 1010, 900 + i*130, COOL, 16, f"a7{i}"))
    b.append(f'<path class="pump7" d="M 900 1600 q 160 -60 20 -300 q -80 -140 -60 -420" stroke="{COOL}" stroke-width="10" '
             f'fill="none" stroke-dasharray="18 14"/>')
    b.append(txt(60, 330, "ВЫХОДИТ ХОЛОДНЫЙ", 44))
    b.append(txt(60, 396, "на 5–10 градусов ниже", 28, "#28506b"))
    b.append(txt(60, 1760, "ПОДДОН → НАСОС → СНОВА НАВЕРХ", 26, "#28506b"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [bg(False)]
    b.append(f'<g><rect x="120" y="620" width="360" height="360" rx="24" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
             f'<path class="hum8" d="M 300 900 q 90 -120 0 -220 q -90 100 0 220 z" fill="{COOL}" opacity="0.8" stroke="{INK}" stroke-width="5"/>'
             f'<text x="300" y="1020" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">сухо</text></g>')
    b.append(f'<g><rect x="600" y="620" width="360" height="360" rx="24" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M 780 900 q 90 -120 0 -220 q -90 100 0 220 z" fill="#9aa3aa" opacity="0.6" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 700 700 l 160 160 M 860 700 l -160 160" stroke="{HOT}" stroke-width="14"/>'
             f'<text x="780" y="1020" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">влажно</text></g>')
    b.append(txt(60, 320, "ГДЕ РАБОТАЕТ", 54))
    b.append(txt(60, 1500, "СУХОЙ КЛИМАТ — ДА", 40, OK))
    b.append(txt(60, 1570, "ВЛАЖНЫЙ — ПОЧТИ НЕТ", 40, HOT))
    b.append(txt(60, 1700, "ЭФФЕКТ: −5…−10 °C НА ВЫХОДЕ", 28, "#28506b"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.08}, 0.1);'
    'tl.fromTo(".u1", {opacity:0, y:40}, {opacity:1, y:0, duration:0.9}, 0.2);',
    'tl.fromTo(".drop2", {y:-80, opacity:0}, {y:0, opacity:1, duration:0.7, ease:"power2.in"}, 0.2);'
    'tl.fromTo(".air2", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.8}, 0.6);'
    'tl.fromTo(".air2b", {scaleX:0, transformOrigin:"100% 50%"}, {scaleX:1, duration:0.8}, 0.9);',
    'tl.fromTo(".pipe", {scale:0, opacity:0, transformOrigin:"50% 50%"}, {scale:1, opacity:1, duration:0.35, stagger:0.02, ease:"back.out(2)"}, 0.15);'
    'tl.fromTo(".frameG", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".trayG", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5}, 0.9);'
    'tl.fromTo(".manG", {opacity:0, y:-30}, {opacity:1, y:0, duration:0.5}, 1.1);',
    'tl.to(".drip4", {y:150, opacity:0.2, duration:1.0, stagger:0.06, repeat:7, ease:"power1.in"}, 0.2);'
    'tl.to(".pipe", {opacity:0.6, duration:0.4}, 0.1);',
    'tl.to(".a50, .a51, .a52", {x:40, opacity:0.5, duration:0.7, stagger:0.15, yoyo:true, repeat:6}, 0.2);'
    'tl.to(".thFill", {attr:{"height":200}, duration:0.8}, 0.2);',
    'tl.fromTo(".st6", {opacity:0, y:30}, {opacity:1, y:-60, duration:1.2, stagger:0.1, repeat:3, ease:"sine.out"}, 0.2);'
    'tl.to(".thFill", {y:"+=160", duration:1.4, ease:"power2.out"}, 0.3);',
    'tl.to(".a70, .a71, .a72", {x:-30, opacity:0.6, duration:0.7, stagger:0.15, yoyo:true, repeat:6}, 0.2);'
    'tl.to(".pump7", {strokeDashoffset:-160, duration:1.6, repeat:5, ease:"none"}, 0.3);',
    'tl.fromTo(".hum8", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.8}, 0.3);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.7}, 0.1);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.03, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
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
