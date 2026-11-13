#!/usr/bin/env python3
"""«Дом в холме» — 10 сцен, разрез."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/earthhouse")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

SKY = "#dceef6"
EARTH = "#a9743f"
EARTH_D = "#7d5229"
EARTH_L = "#c08a4e"
GRASS = "#7fa04f"
GRASS_D = "#5d7d38"
WOOD = "#c98a4b"
CREAM = "#f7ecd8"
INK = "#3a2e24"
GLASS = "#9fc9d6"
HOT = "#d2603a"
COLD = "#3f8fc4"
OK = "#4f8f4a"
CONC = "#c9cfd2"
TYRE = "#4a4038"


def S(d, w=4, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, cls="fillshape", stroke=INK, sw=4, op=1.0):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=44, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def grain(seed, n=140):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(460,1900):.0f}" r="{r.uniform(1,3):.1f}" '
                   f'fill="#5d3d24" opacity="{r.uniform(0.05,0.13):.2f}"/>' for _ in range(n))


def sun(x=960, y=210, r=64):
    rays = "".join(
        f'<path d="M {x + (r+16)*math.cos(a):.0f} {y + (r+16)*math.sin(a):.0f} '
        f'L {x + (r+52)*math.cos(a):.0f} {y + (r+52)*math.sin(a):.0f}" stroke="#e8b23a" stroke-width="7" stroke-linecap="round"/>'
        for a in [i * math.pi / 6 for i in range(12)])
    return (f'<g class="sunG"><circle cx="{x}" cy="{y}" r="{r}" fill="#f4c95a" stroke="{INK}" stroke-width="4"/>'
            f'{rays}</g>')


def arrow(x1, y1, x2, y2, col, w=11, cls="arrow"):
    return (f'<path class="{cls}" d="M {x1} {y1} Q {(x1+x2)/2} {(y1+y2)/2 - 20} {x2} {y2}" stroke="{col}" '
            f'stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="M {x2} {y2} l -20 -4 l 6 20 z" fill="{col}"/>')


def caption(x, y, s, w=300):
    return (f'<g class="capG"><rect x="{x}" y="{y}" width="{w}" height="58" rx="12" fill="#fffdf6" '
            f'stroke="{INK}" stroke-width="3" opacity="0.95"/>'
            f'<text x="{x+w/2}" y="{y+38}" font-family="Nunito" font-size="24" font-weight="800" fill="{INK}" '
            f'text-anchor="middle">{s}</text></g>')


def base(seed=1, with_sun=True, cls="base"):
    b = [f'<rect width="1080" height="1920" fill="{SKY}"/>']
    if with_sun:
        b.append(sun())
    # холм
    b.append(F("M 0 470 Q 260 400 540 440 Q 820 480 1080 430 L 1080 1920 L 0 1920 Z", EARTH, "earthG", INK, 4))
    b.append(F("M 0 470 Q 260 400 540 440 Q 820 480 1080 430 L 1080 520 L 0 560 Z", EARTH_L, "earthTop", "none", 0, 0.7))
    # трава
    b.append(f'<path d="M 0 470 Q 260 400 540 440 Q 820 480 1080 430" stroke="{GRASS}" stroke-width="22" fill="none"/>')
    for i in range(22):
        x = 20 + i * 48
        b.append(f'<path d="M {x} 462 q 6 -22 12 -4 M {x+8} 466 q 4 -26 14 -8" stroke="{GRASS_D}" stroke-width="4" fill="none"/>')
    b.append(grain(seed))
    # нижний слой грунта
    b.append(F("M 0 1560 L 1080 1560 L 1080 1920 L 0 1920 Z", EARTH_D, "subG", "none", 0, 0.55))
    for i in range(9):
        y = 1600 + i * 40
        b.append(f'<path d="M 0 {y} l 1080 0" stroke="#5d3d24" stroke-width="2" opacity="0.25"/>')
    b.append(f'<text x="60" y="1880" font-family="Nunito" font-size="26" font-weight="800" fill="#f0dfc0" opacity="0.8">ГРУНТ</text>')
    return b


def house_cut(slab=True, tires=True, roof=True, glass=True, furniture=True, cls="houseG"):
    b = [f'<g class="{cls}">']
    # полость дома
    b.append(F("M 300 700 L 900 700 L 900 1180 L 300 1180 Z", CREAM, "fillshape", INK, 4))
    # стена из покрышек
    if tires:
        for i in range(6):
            y = 720 + i * 78
            b.append(f'<rect x="240" y="{y}" width="78" height="62" rx="20" fill="{TYRE}" stroke="{INK}" stroke-width="4"/>')
            b.append(f'<circle cx="279" cy="{y+31}" r="17" fill="#6b5f54" stroke="{INK}" stroke-width="2"/>')
    # зелёная крыша
    if roof:
        b.append(F("M 230 700 L 910 700 L 910 660 L 230 660 Z", GRASS, "fillshape", INK, 4))
        b.append(f'<path d="M 230 686 L 910 686" stroke="#8a6a3a" stroke-width="8"/>')
        b.append(f'<path d="M 230 672 L 910 672" stroke="#3f6b7a" stroke-width="6" opacity="0.8"/>')
        for i in range(14):
            x = 250 + i * 47
            b.append(f'<path d="M {x} 660 q 5 -20 11 -6 M {x+7} 660 q 3 -24 13 -10" stroke="{GRASS_D}" stroke-width="4" fill="none"/>')
    # остекление на юг
    if glass:
        b.append(F("M 900 700 L 1010 770 L 1010 1180 L 900 1180 Z", GLASS, "glassG", INK, 4, 0.75))
        for k in range(4):
            b.append(f'<path d="M {900+k*27} {700+k*17} L {900+k*27} {1180}" stroke="{INK}" stroke-width="3" opacity="0.5"/>')
    # плита пола
    if slab:
        b.append(F("M 240 1180 L 1010 1180 L 1010 1246 L 240 1246 Z", CONC, "slabG", INK, 4))
    # мебель
    if furniture:
        b.append(f'<rect x="470" y="1092" width="150" height="88" rx="10" fill="#c96f4a" stroke="{INK}" stroke-width="4"/>')
        b.append(f'<rect x="470" y="1070" width="40" height="30" rx="6" fill="#e8b48a" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<rect x="650" y="1100" width="110" height="14" rx="4" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<path d="M 670 1114 l 0 60 M 740 1114 l 0 60" stroke="{INK}" stroke-width="5"/>')
        b.append(f'<circle cx="820" cy="1120" r="26" fill="#6f9b52" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<path d="M 806 1146 l 28 0 l -6 34 l -16 0 z" fill="#b98a50" stroke="{INK}" stroke-width="3"/>')
        # человек
        b.append(f'<circle cx="420" cy="1078" r="16" fill="#f0c9a0" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<path d="M 404 1094 L 436 1094 L 440 1150 L 400 1150 Z" fill="#4f7fa0" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def tube(d="M 1010 1310 L 470 1310 Q 380 1310 380 1400 L 380 1520 Q 380 1600 470 1600 L 760 1600", cls="tubeG"):
    return (f'<g class="{cls}"><path d="{d}" fill="none" stroke="{CONC}" stroke-width="34" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{COLD}" stroke-width="12" stroke-linejoin="round" opacity="0.85"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = base(1)
    b.append(house_cut())
    b.append(tube())
    b.append(txt(60, 180, "ДОМ В ХОЛМЕ", 62))
    b.append(txt(60, 244, "тепло земли вместо котла", 28, "#4a5a5f"))
    b.append(caption(600, 130, "почти без отопления", 340))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = base(2)
    b.append(house_cut())
    b.append(arrow(120, 640, 260, 760, HOT, 12, "a2a"))
    b.append(arrow(300, 520, 300, 660, HOT, 12, "a2b"))
    b.append(txt(60, 180, "ЗЕМЛЯНОЙ ВАЛ", 56))
    b.append(txt(60, 244, "защита от ветра с трёх сторон", 26, "#4a5a5f"))
    b.append(caption(120, 330, "нет ветра — нет потерь", 360))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = base(3)
    b.append(house_cut(roof=True))
    b.append(f'<path class="l3" d="M 560 600 L 620 668" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path class="l3" d="M 700 560 L 700 656" stroke="{INK}" stroke-width="3"/>')
    b.append(caption(430, 520, "растения", 200))
    b.append(caption(660, 500, "гидроизоляция + утеплитель", 380))
    b.append(txt(60, 180, "ЗЕЛЁНАЯ КРЫША", 56))
    b.append(txt(60, 244, "держит тепло и вписывает дом в склон", 24, "#4a5a5f"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = base(4)
    b.append(house_cut())
    b.append(arrow(300, 900, 420, 940, HOT, 14, "a4a"))
    b.append(arrow(420, 1020, 300, 1060, HOT, 10, "a4b"))
    b.append(caption(70, 800, "массив копит тепло", 330))
    b.append(txt(60, 180, "СТЕНА ИЗ ЗЕМЛИ", 56))
    b.append(txt(60, 244, "покрышки и грунт: тепло днём — ночью", 24, "#4a5a5f"))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = base(5)
    b.append(house_cut())
    for i in range(4):
        b.append(f'<path class="ray5" d="M {1000 - i*26} {330 + i*30} L {900 - i*10} {800 + i*40}" stroke="#e8b23a" '
                 f'stroke-width="8" opacity="0.85"/>')
    b.append(caption(560, 330, "зимнее солнце", 300))
    b.append(txt(60, 180, "ТЕПЛИЦА НА ЮГ", 56))
    b.append(txt(60, 244, "ловит низкое солнце даже зимой", 24, "#4a5a5f"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = base(6)
    b.append(house_cut())
    b.append(arrow(520, 1080, 520, 800, HOT, 12, "a6a"))
    b.append(arrow(600, 1000, 840, 760, HOT, 12, "a6b"))
    b.append(f'<path class="out6" d="M 880 700 L 940 620" stroke="{HOT}" stroke-width="14" fill="none"/>')
    b.append(caption(600, 500, "выход тёплого воздуха", 380))
    b.append(txt(60, 180, "ТЯГА", 56))
    b.append(txt(60, 244, "тёплый воздух уходит вверху", 24, "#4a5a5f"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = base(7)
    b.append(house_cut())
    b.append(tube())
    b.append(arrow(980, 1380, 700, 1380, COLD, 12, "a7a"))
    b.append(caption(600, 1440, "труба в грунте", 300))
    b.append(txt(60, 180, "ЗЕМЛЯНАЯ ТРУБА", 54))
    b.append(txt(60, 244, "воздух идёт под землёй", 24, "#4a5a5f"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = base(8)
    b.append(house_cut(furniture=False))
    b.append(tube())
    b.append(f'<g class="th8"><rect x="600" y="1330" width="72" height="220" rx="36" fill="#fffdf6" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="614" y="1420" width="44" height="120" rx="22" fill="{COLD}"/>'
             f'<circle cx="636" cy="1556" r="34" fill="{COLD}" stroke="{INK}" stroke-width="4"/>'
             f'<text x="636" y="1630" font-family="Nunito" font-size="34" font-weight="900" fill="{INK}" text-anchor="middle">+10°</text></g>')
    b.append(arrow(900, 1330, 760, 1400, COLD, 10, "a8a"))
    b.append(arrow(500, 1400, 640, 1330, HOT, 10, "a8b"))
    b.append(txt(60, 180, "ПОЧВА КАК БАТАРЕЯ", 50))
    b.append(txt(60, 244, "летом охлаждает, зимой согревает", 24, "#4a5a5f"))
    return b


# ---------------------------------------------------------------- s9
def s9():
    b = base(9)
    b.append(house_cut())
    b.append(f'<rect class="slab9" x="240" y="1180" width="770" height="66" fill="{HOT}" opacity="0.35" stroke="{INK}" stroke-width="4"/>')
    for i in range(4):
        b.append(arrow(340 + i * 170, 1246, 340 + i * 170, 1150, HOT, 8, f"a9{i}"))
    b.append(txt(60, 180, "ПЛИТА-АККУМУЛЯТОР", 50))
    b.append(txt(60, 244, "накопила — отдала вечером", 24, "#4a5a5f"))
    b.append(caption(560, 1080, "инерция", 200))
    return b


# ---------------------------------------------------------------- s10
def s10():
    b = base(10)
    b.append(house_cut())
    b.append(tube())
    b.append(f'<g class="ok10"><path d="M 700 940 l 44 52 l 92 -118" stroke="{OK}" stroke-width="20" fill="none" stroke-linecap="round"/></g>')
    b.append(txt(60, 180, "ПАССИВНЫЙ ДОМ", 54))
    b.append(txt(60, 244, "но нужен расчёт и гидроизоляция", 24, "#8a4a2f"))
    b.append(caption(60, 1650, "иначе — сырость и плесень", 420))
    b.append(caption(60, 1740, "вентиляция обязательна", 380))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
ANIM = [
    'tl.fromTo(".houseG", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".tubeG", {opacity:0}, {opacity:1, duration:0.6}, 0.5);'
    'tl.to(".sunG", {rotate:8, transformOrigin:"960px 210px", duration:6, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0);',
    'tl.to(".a2a, .a2b", {x:16, opacity:0.5, duration:0.8, yoyo:true, repeat:4}, 0.2);'
    'tl.fromTo(".houseG", {opacity:0}, {opacity:1, duration:0.5}, 0.1);',
    'tl.fromTo(".l3", {opacity:0}, {opacity:1, duration:0.5, stagger:0.2}, 0.3);'
    'tl.fromTo(".capG", {opacity:0, y:10}, {opacity:1, y:0, duration:0.4, stagger:0.2}, 0.5);',
    'tl.to(".a4a", {scaleX:1.1, transformOrigin:"0% 50%", duration:0.7, yoyo:true, repeat:4}, 0.2);'
    'tl.to(".a4b", {x:-14, duration:0.7, yoyo:true, repeat:4}, 0.4);',
    'tl.to(".ray5", {opacity:0.4, duration:0.7, stagger:0.12, yoyo:true, repeat:5}, 0.1);'
    'tl.fromTo(".capG", {opacity:0}, {opacity:1, duration:0.4}, 0.8);',
    'tl.to(".a6a, .a6b", {y:-18, opacity:0.5, duration:0.8, stagger:0.15, yoyo:true, repeat:4}, 0.2);'
    'tl.to(".out6", {opacity:0.4, duration:0.6, yoyo:true, repeat:5}, 0.2);',
    'tl.to(".a7a", {x:-24, duration:0.9, yoyo:true, repeat:4}, 0.2);'
    'tl.fromTo(".tubeG", {opacity:0.4}, {opacity:1, duration:0.7}, 0.1);',
    'tl.fromTo(".th8", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5}, 0.2);'
    'tl.to(".a8a", {x:-20, duration:0.8, yoyo:true, repeat:4}, 0.3);'
    'tl.to(".a8b", {x:20, duration:0.8, yoyo:true, repeat:4}, 0.4);',
    'tl.to(".slab9", {opacity:0.6, duration:0.7, yoyo:true, repeat:4}, 0.2);'
    'tl.to(".a9a", {y:-14, duration:0.6, stagger:0.1, yoyo:true, repeat:4}, 0.3);',
    'tl.fromTo(".ok10", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 0.5);'
    'tl.fromTo(".capG", {opacity:0, y:10}, {opacity:1, y:0, duration:0.4, stagger:0.2}, 1.0);'
    'tl.to(".houseG", {opacity:1, duration:0.3}, 0);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SKY}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
