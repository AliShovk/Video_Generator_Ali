#!/usr/bin/env python3
"""«Солнечный забор» — 9 сцен, яркая иллюстрация."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/solarfence")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

SKY1 = "#ffe9c9"; SKY2 = "#cfe9f7"
INK = "#2f3a44"; INK2 = "#5f6f7a"
GRASS = "#7fbf5a"; GRASS_D = "#569237"
WOOD = "#a9764a"; WOOD_D = "#7d5330"; WOOD_L = "#c99a6a"
PANEL = "#20456f"; PANEL_L = "#3f78a8"; PANEL_D = "#132c47"
SUN = "#ffb03a"; SUN_D = "#e58a1c"
HOUSE = "#f7efdd"; HOUSE_D = "#d9cdb4"
ROOF = "#c96a4a"; ROOF_D = "#a14f33"
WARM = "#ffd98a"; CYAN = "#7fe3f0"; YEL = "#ffd23f"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def flowers(r):
    out = []
    for i in range(11):
        x, y = r.uniform(50, 1030), r.uniform(1360, 1860)
        c = "#ff8fa3" if i % 2 else "#ffd166"
        for k in range(5):
            a = math.radians(k * 72)
            out.append(f'<circle cx="{x+13*math.cos(a):.0f}" cy="{y+13*math.sin(a):.0f}" r="7" fill="{c}" opacity="0.95"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#fff3cf"/>')
    return "".join(out)


def bg(seed=1):
    r = random.Random(seed)
    tufts = "".join(f'<path d="M {r.uniform(0,1080):.0f} {r.uniform(1280,1900):.0f} l {r.uniform(-14,14):.0f} -{r.uniform(18,34):.0f}" '
                    f'stroke="{GRASS_D}" stroke-width="4" stroke-linecap="round" opacity="0.55"/>' for _ in range(90))
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{SKY1}"/><stop offset="0.55" stop-color="{SKY2}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sky)"/>'
            f'<rect x="0" y="1260" width="1080" height="660" fill="{GRASS}"/>'
            f'<path d="M 0 1700 q 300 -40 540 0 t 540 0 l 0 220 l -1080 0 z" fill="{GRASS_D}" opacity="0.25"/>'
            + flowers(r) + tufts)



def sun(cx=880, cy=300, r=95, cls="sun"):
    b = [f'<g class="{cls}">']
    for i in range(12):
        a = math.radians(i * 30)
        b.append(f'<path class="ray{i}" d="M {cx+r*1.3*math.cos(a):.0f} {cy+r*1.3*math.sin(a):.0f} '
                 f'l {46*math.cos(a):.0f} {46*math.sin(a):.0f}" stroke="{SUN_D}" stroke-width="9" stroke-linecap="round" opacity="0.8"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>')
    b.append(f'<circle cx="{cx-r*0.28:.0f}" cy="{cy-r*0.28:.0f}" r="{r*0.4:.0f}" fill="#ffd27a" opacity="0.7"/>')
    b.append('</g>')
    return "".join(b)


def fence_wood(x=60, y=1240, n=9, w=110, h=330, cls="fw"):
    b = [f'<g class="{cls}">']
    for i in range(n):
        px = x + i * w
        b.append(f'<rect x="{px}" y="{y-h}" width="{w-14}" height="{h}" rx="6" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="4"/>')
        for k in range(3):
            b.append(f'<path d="M {px+18+k*26} {y-h+20} q 6 {h*0.4} 0 {h-40}" stroke="{WOOD_D}" stroke-width="3" fill="none" opacity="0.45"/>')
        b.append(f'<path d="M {px} {y-h*0.72:.0f} l {w-14} 0" stroke="{WOOD_D}" stroke-width="8" opacity="0.55"/>')
        b.append(f'<path d="M {px} {y-h*0.25:.0f} l {w-14} 0" stroke="{WOOD_D}" stroke-width="8" opacity="0.55"/>')
    b.append('</g>')
    return "".join(b)


def fence_panels(x=90, y=1240, n=5, w=170, h=380, cls="fp", glint=True):
    b = [f'<g class="{cls}">']
    for i in range(n):
        px = x + i * w
        b.append(f'<rect x="{px}" y="{y-h}" width="26" height="{h+20}" rx="6" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="4"/>')
        b.append(f'<rect x="{px+26}" y="{y-h+18}" width="{w-40}" height="{h-46}" rx="6" fill="{PANEL}" stroke="{PANEL_D}" stroke-width="4"/>')
        # сетка ячеек
        for cx in range(1, 5):
            b.append(f'<path d="M {px+26+(w-40)*cx/4:.0f} {y-h+18} l 0 {h-46}" stroke="{PANEL_L}" stroke-width="2" opacity="0.7"/>')
        for cy in range(1, 6):
            b.append(f'<path d="M {px+26} {y-h+18+(h-46)*cy/6:.0f} l {w-40} 0" stroke="{PANEL_L}" stroke-width="2" opacity="0.7"/>')
        b.append(f'<path d="M {px+26} {y-h+18} l {w-40} 0 l 0 26 l {-w+40} 0 z" fill="{CYAN}" opacity="0.18"/>')
        if glint:
            b.append(f'<path class="gl{i}" d="M {px+40} {y-h+40} l 46 0 l -26 {h-90} l -46 0 z" fill="#ffffff" opacity="0.0"/>')
    b.append(f'<rect x="{x}" y="{y-h-16}" width="{n*w}" height="18" rx="6" fill="{WOOD_L}" stroke="{WOOD_D}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def house(x=740, y=1250, w=320, h=300, cls="hs"):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{HOUSE}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M {x-30} {y-h} L {x+w/2} {y-h-110} L {x+w+30} {y-h} Z" fill="{ROOF}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M {x-30} {y-h} L {x+w+30} {y-h}" stroke="{INK}" stroke-width="4"/>')
    # окна
    b.append(f'<rect class="win1" x="{x+34}" y="{y-h+60}" width="86" height="80" rx="6" fill="{WARM}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<rect class="win2" x="{x+180}" y="{y-h+60}" width="86" height="80" rx="6" fill="#cfe3ee" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<rect x="{x+120}" y="{y-120}" width="{w-180}" height="120" rx="6" fill="{HOUSE_D}" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def conduit(pts, cls="cd"):
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    return (f'<g class="{cls}"><path d="{d}" stroke="#9aa4ab" stroke-width="18" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="#c9d3d8" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.8"/></g>')


def dots(pts, n=5, cls="dt"):
    """Жёлтые «искры» энергии вдоль трассы."""
    out = [f'<g class="{cls}">']
    x0, y0 = pts[-1]
    for i in range(n):
        out.append(f'<circle class="e{i}" cx="{x0}" cy="{y0}" r="9" fill="{YEL}" opacity="0.95"/>')
    out.append('</g>')
    return "".join(out)


def weeds(x, y, cls="wd"):
    b = [f'<g class="{cls}">']
    for i in range(7):
        px = x + i * 26
        b.append(f'<path class="w{i}" d="M {px} {y} q 8 -40 2 -70" stroke="{GRASS_D}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def label(x, y, s, size=22, cls="lb", col=INK):
    w = len(s) * size * 0.58 + 26
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="8" fill="#ffffff" opacity="0.92" stroke="{INK2}" stroke-width="1.5"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(1), sun(880, 290, 95, "sun1")]
    b.append(fence_panels(70, 1250, 5, 170, 400, "fp1"))
    b.append(house(760, 1250, 300, 290, "hs1"))
    b.append(conduit([(520, 1300), (700, 1340), (760, 1290)], "cd1"))
    b.append(t(60, 190, "ЗАБОР-", 64, INK))
    b.append(t(60, 262, "ЭЛЕКТРОСТАНЦИЯ", 52, "#1f6f8b"))
    b.append(t(64, 330, "приватность + энергия", 28, INK2, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg(2)]
    b.append(fence_wood(60, 1300, 9, 115, 380, "fw2"))
    b.append(label(200, 760, "ТОЛЬКО ПРИВАТНОСТЬ", 22, "lb1"))
    b.append(t(60, 200, "ОБЫЧНЫЙ ЗАБОР", 44, INK))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(3)]
    b.append(fence_wood(40, 1300, 10, 110, 380, "fw3"))
    b.append(weeds(120, 1310, "wd3"))
    b.append(f'<g class="brush"><rect x="820" y="900" width="70" height="24" rx="8" fill="{WOOD_D}"/>'
             f'<rect x="870" y="890" width="60" height="44" rx="10" fill="#8fbf6a"/></g>')
    b.append(f'<path class="paint" d="M 780 960 q -60 90 -120 120" stroke="#8fbf6a" stroke-width="16" fill="none" opacity="0"/>')
    b.append(label(140, 760, "КРАСИТЬ КАЖДЫЙ ГОД", 22, "lb2"))
    b.append(t(60, 200, "ЗАНИМАЕТ МЕСТО", 42, INK))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg(4)]
    b.append(fence_panels(90, 1300, 5, 175, 430, "fp4"))
    b.append(label(150, 720, "ПАНЕЛИ НА ТЕХ ЖЕ СТОЛБАХ", 20, "lb3"))
    b.append(t(60, 200, "ТЕ ЖЕ МЕТРЫ", 44, INK))
    b.append(t(60, 262, "другая работа", 30, "#1f6f8b", w=800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg(5), sun(540, 560, 120, "sun5")]
    b.append(fence_panels(120, 1400, 3, 240, 420, "fp5"))
    for i, (x1, y1) in enumerate(((420, 760), (520, 800), (640, 780))):
        b.append(f'<path class="arr{i}" d="M {x1} {y1} l 0 180" stroke="{YEL}" stroke-width="9" stroke-linecap="round"/>')
        b.append(f'<path d="M {x1-18} {y1+156} l 18 28 l 18 -28" fill="none" stroke="{YEL}" stroke-width="9" stroke-linecap="round"/>')
    b.append(t(60, 200, "СВЕТ С ДВУХ СТОРОН", 40, INK))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(6)]
    b.append(fence_panels(50, 1300, 4, 175, 420, "fp6"))
    b.append(house(700, 1300, 320, 300, "hs6"))
    b.append(conduit([(450, 1330), (640, 1370), (720, 1320)], "cd6"))
    b.append(dots([(450, 1330), (720, 1320)], 5, "dt6"))
    b.append(t(60, 200, "КАБЕЛЬ В ДОМ", 44, INK))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg(7)]
    b.append(house(300, 1300, 480, 420, "hs7"))
    # иконки приборов
    b.append(f'<g class="ap1"><circle cx="360" cy="720" r="56" fill="{WARM}" stroke="{INK}" stroke-width="4"/></g>')
    b.append(f'<g class="ap2"><rect x="480" y="670" width="110" height="110" rx="12" fill="#eaf3f8" stroke="{INK}" stroke-width="4"/>'
             f'<circle cx="535" cy="725" r="30" fill="#9fc4d8" stroke="{INK}" stroke-width="3"/></g>')
    b.append(f'<g class="ap3"><path d="M 680 780 q 40 -90 80 0 z" fill="#e8e2d2" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="690" y="780" width="60" height="26" rx="8" fill="#c9c2b0" stroke="{INK}" stroke-width="3"/></g>')
    b.append(t(60, 220, "СВЕТ · СТИРКА · ЧАЙНИК", 34, INK))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [bg(8)]
    b.append(fence_panels(90, 1250, 5, 175, 400, "fp8"))
    b.append(f'<circle cx="800" cy="700" r="150" fill="#ffffff" opacity="0.75" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(800, 660, "10 М", 56, INK, "middle", 900))
    b.append(t(800, 730, "ЗАБОРА", 24, INK2, "middle", 800))
    b.append(t(800, 820, "= 2–3 кВт·ч", 30, "#1f6f8b", "middle", 900))
    b.append(t(60, 200, "СКОЛЬКО ЭТО ДАЁТ", 38, INK))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [bg(9), sun(880, 300, 90, "sun9")]
    b.append(fence_panels(80, 1280, 5, 175, 410, "fp9"))
    b.append(house(760, 1280, 300, 290, "hs9"))
    b.append(t(60, 260, "ПРИВАТНОСТЬ", 56, INK))
    b.append(t(60, 330, "+ ЭНЕРГИЯ", 56, "#1f6f8b"))
    b.append(t(64, 400, "на одних и тех же метрах", 26, INK2, w=700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".sun1", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.6}, 0.1);'
    'tl.to(".sun1", {rotate:20, transformOrigin:"880px 290px", duration:10, repeat:-1, ease:"none"}, 0.4);'
    'tl.fromTo(".fp1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.3);'
    'tl.fromTo(".hs1", {opacity:0, x:20}, {opacity:1, x:0, duration:0.6}, 0.6);'
    'tl.fromTo(".cd1", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);'
    'tl.to(".gl0, .gl1, .gl2, .gl3, .gl4", {opacity:0.35, x:40, duration:1.6, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);',
    'tl.fromTo(".fw2", {opacity:0, y:16}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".lb1", {opacity:0}, {opacity:1, duration:0.4}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".fw3", {opacity:0}, {opacity:1, duration:0.6}, 0.1);'
    'tl.fromTo(".wd3", {opacity:0, y:10}, {opacity:1, y:0, duration:0.6}, 0.4);'
    'tl.to(".w0, .w1, .w2, .w3, .w4, .w5, .w6", {rotate:6, transformOrigin:"50% 100%", duration:1.2, stagger:0.08, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.7);'
    'tl.fromTo(".brush", {opacity:0, x:60}, {opacity:1, x:0, duration:0.6}, 0.6);'
    'tl.to(".brush", {x:-90, duration:1.2, ease:"sine.inOut"}, 1.2);'
    'tl.to(".paint", {opacity:0.8, duration:0.3}, 1.6);'
    'tl.fromTo(".lb2", {opacity:0}, {opacity:1, duration:0.4}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".fp4", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.to(".gl0, .gl1, .gl2, .gl3, .gl4", {opacity:0.4, x:50, duration:1.5, stagger:0.2, yoyo:true, repeat:-1}, 0.8);'
    'tl.fromTo(".lb3", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".sun5", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6}, 0.1);'
    'tl.fromTo(".fp5", {opacity:0}, {opacity:1, duration:0.6}, 0.3);'
    'tl.fromTo(".arr0, .arr1, .arr2", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.6, stagger:0.2}, 0.7);'
    'tl.to(".arr0, .arr1, .arr2", {y:16, duration:1.0, stagger:0.15, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".fp6", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".hs6", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.fromTo(".cd6", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.to(".e0, .e1, .e2, .e3, .e4", {x:-250, duration:1.4, stagger:0.18, repeat:-1, ease:"none"}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".hs7", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".win1", {opacity:0.3}, {opacity:1, duration:0.6, yoyo:true, repeat:-1}, 0.5);'
    'tl.fromTo(".ap1, .ap2, .ap3", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 0.7);'
    'tl.to(".ap2", {rotate:360, transformOrigin:"50% 50%", duration:2, repeat:-1, ease:"linear"}, 1.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".fp8", {opacity:0}, {opacity:1, duration:0.6}, 0.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".sun9", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6}, 0.1);'
    'tl.fromTo(".fp9", {opacity:0}, {opacity:1, duration:0.6}, 0.3);'
    'tl.fromTo(".hs9", {opacity:0}, {opacity:1, duration:0.6}, 0.5);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SKY2}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
