#!/usr/bin/env python3
"""«Радио Кито 1949» — 9 сцен, плоский стиль (flat)."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/quito")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

CREAM = "#f6ecd8"
NAVY = "#16263f"
DEEP = "#0d1524"
RED = "#e04b2c"
MUST = "#f2b134"
TEAL = "#2a9d8f"
BLACK = "#101017"
GREY = "#8fa0b3"


def t(x, y, s, size=48, col=CREAM, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def bg(c=NAVY):
    return f'<rect width="1080" height="1920" fill="{c}"/>'


def radio(x, y, s=1.0, cls="radio", body=CREAM, dial=MUST, shadow=False):
    b = [f'<g class="{cls}">']
    if shadow:
        b.append(f'<rect x="{x+16}" y="{y+18}" width="{520*s}" height="{360*s}" rx="{28*s}" fill="{BLACK}" opacity="0.35"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{520*s}" height="{360*s}" rx="{28*s}" fill="{body}"/>')
    b.append(f'<rect x="{x+26*s}" y="{y+26*s}" width="{300*s}" height="{190*s}" rx="{14*s}" fill="{NAVY}"/>')
    # шкала
    for i in range(9):
        b.append(f'<rect x="{x+44*s+i*32*s}" y="{y+44*s}" width="{6*s}" height="{26*s}" fill="{MUST}" opacity="0.8"/>')
    b.append(f'<circle cx="{x+150*s}" cy="{y+140*s}" r="{44*s}" fill="{MUST}"/>')
    b.append(f'<circle cx="{x+150*s}" cy="{y+140*s}" r="{10*s}" fill="{NAVY}"/>')
    # решётка
    for i in range(6):
        b.append(f'<rect x="{x+352*s}" y="{y+36*s+i*30*s}" width="{140*s}" height="{14*s}" rx="{7*s}" fill="{NAVY}" opacity="0.85"/>')
    # ручки
    b.append(f'<circle cx="{x+380*s}" cy="{y+286*s}" r="{30*s}" fill="{RED}"/>')
    b.append(f'<circle cx="{x+460*s}" cy="{y+286*s}" r="{30*s}" fill="{TEAL}"/>')
    b.append('</g>')
    return "".join(b)


def person(x, y, s=1.0, col=BLACK, cls="p", run=False):
    """Плоский человечек: голова, корпус, ноги."""
    b = [f'<g class="{cls}">']
    b.append(f'<circle cx="{x}" cy="{y-150*s}" r="{34*s}" fill="{col}"/>')
    b.append(f'<path d="M {x-34*s} {y-110*s} L {x+34*s} {y-110*s} L {x+26*s} {y-6*s} L {x-26*s} {y-6*s} Z" fill="{col}"/>')
    if run:
        b.append(f'<path d="M {x-26*s} {y-6*s} l {-46*s} {86*s} l {28*s} {10*s} l {44*s} {-80*s} Z" fill="{col}"/>')
        b.append(f'<path d="M {x+20*s} {y-6*s} l {34*s} {92*s} l {-28*s} {8*s} l {-30*s} {-84*s} Z" fill="{col}"/>')
        b.append(f'<path d="M {x-34*s} {y-96*s} l {-50*s} {-30*s} l {-10*s} {22*s} l {50*s} {34*s} Z" fill="{col}"/>')
        b.append(f'<path d="M {x+30*s} {y-100*s} l {56*s} {20*s} l {4*s} {-24*s} l {-56*s} {-18*s} Z" fill="{col}"/>')
    else:
        b.append(f'<path d="M {x-24*s} {y-6*s} l {-6*s} {88*s} l {26*s} 0 l {10*s} {-80*s} Z" fill="{col}"/>')
        b.append(f'<path d="M {x+24*s} {y-6*s} l {6*s} {88*s} l {-26*s} 0 l {-10*s} {-80*s} Z" fill="{col}"/>')
        b.append(f'<path d="M {x-34*s} {y-100*s} l {-14*s} {64*s} l {16*s} 6*s l {12*s} {-56*s} Z" fill="{col}"/>')
        b.append(f'<path d="M {x+34*s} {y-100*s} l {14*s} {64*s} l {-16*s} 6*s l {-12*s} {-56*s} Z" fill="{col}"/>')
    b.append('</g>')
    return "".join(b)


def building(x, y, w, h, col=NAVY, win=MUST, cls="bldg", rows=5, cols=4):
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}"/>']
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 3 == 0:
                continue
            b.append(f'<rect x="{x+22+c*((w-44)/cols)}" y="{y+24+r*((h-48)/rows)}" width="{18}" height="{24}" fill="{win}" opacity="0.75"/>')
    b.append('</g>')
    return "".join(b)


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(DEEP)]
    b.append(f'<rect x="0" y="0" width="1080" height="26" fill="{RED}"/>')
    b.append(f'<rect x="0" y="1894" width="1080" height="26" fill="{RED}"/>')
    b.append(f'<circle cx="540" cy="1150" r="420" fill="{NAVY}" opacity="0.55"/>')
    b.append(radio(280, 960, 1.0, "radio1", CREAM, MUST, True))
    b.append(t(70, 250, "РАДИО СКАЗАЛО:", 46, MUST, ls=2))
    b.append(t(70, 360, "МАРСИАНЕ", 104, CREAM, ls=2))
    b.append(t(70, 470, "УЖЕ ЗДЕСЬ", 104, RED, ls=2))
    b.append(t(70, 540, "Кито · 12 февраля 1949", 26, GREY, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg(CREAM)]
    b.append(f'<rect x="0" y="1180" width="1080" height="740" fill="{NAVY}"/>')
    # микрофон
    b.append('<g class="mic">')
    b.append(f'<rect x="470" y="640" width="140" height="230" rx="70" fill="{NAVY}"/>')
    for i in range(6):
        b.append(f'<rect x="486" y="{668+i*32}" width="108" height="10" rx="5" fill="{CREAM}" opacity="0.55"/>')
    b.append(f'<rect x="524" y="870" width="32" height="150" fill="{NAVY}"/>')
    b.append(f'<ellipse cx="540" cy="1024" rx="150" ry="26" fill="{NAVY}"/>')
    b.append('</g>')
    # ведущий
    b.append(person(810, 1250, 1.5, RED, "host"))

    b.append(f'<g class="onair"><rect x="760" y="230" width="230" height="56" rx="10" fill="{RED}"/>'
             f'<text x="875" y="268" font-family="Nunito" font-size="26" font-weight="900" fill="{CREAM}" text-anchor="middle">В ЭФИРЕ</text></g>')
    b.append(t(70, 230, "СТУДИЯ", 44, RED, ls=4))
    b.append(t(70, 310, "РАДИО КИТО", 64, NAVY))
    b.append(t(70, 380, "экстренный выпуск", 28, NAVY, w=700))
    b.append(f'<g class="console"><rect x="0" y="1560" width="1080" height="360" fill="#101d30"/>'
             f'<rect x="40" y="1600" width="1000" height="10" rx="5" fill="{MUST}" opacity="0.6"/>'
             + "".join(f'<circle cx="{90+i*60}" cy="1670" r="14" fill="{MUST}" opacity="0.8"/>' for i in range(15))
             + f'<rect x="0" y="1740" width="1080" height="6" fill="{RED}" opacity="0.7"/></g>')
    b.append(f'<g class="waves"><circle cx="540" cy="760" r="180" fill="none" stroke="{RED}" stroke-width="3" opacity="0.5"/>'
             f'<circle cx="540" cy="760" r="250" fill="none" stroke="{RED}" stroke-width="3" opacity="0.3"/>'
             f'<circle cx="540" cy="760" r="320" fill="none" stroke="{RED}" stroke-width="3" opacity="0.18"/></g>')
    b.append(t(70, 1810, "микрофон · ведущий · сводки", 24, CREAM, w=600))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(NAVY)]
    b.append(f'<circle cx="820" cy="520" r="260" fill="{MUST}" opacity="0.16"/>')
    # холмы
    b.append(f'<path d="M 0 1280 q 260 -200 520 -20 q 260 180 560 -40 L 1080 1920 L 0 1920 Z" fill="{DEEP}"/>')
    # тарелка
    b.append('<g class="saucer">')
    b.append(f'<ellipse cx="560" cy="900" rx="260" ry="60" fill="{CREAM}"/>')
    b.append(f'<path d="M 370 900 q 190 -140 380 0 z" fill="{TEAL}"/>')
    b.append(f'<ellipse cx="560" cy="906" rx="120" ry="26" fill="{MUST}"/>')
    b.append(f'<path d="M 560 940 L 470 1240 L 650 1240 Z" fill="{MUST}" opacity="0.25"/>')
    b.append('</g>')
    b.append(t(70, 250, "ПОСАДКА", 52, MUST, ls=3))
    b.append(t(70, 330, "под Кито", 52, CREAM))
    b.append(t(70, 1660, "марсиане высадились", 28, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg("#0f2033")]
    b.append(building(60, 1280, 200, 400, "#1d3350", MUST))
    b.append(building(300, 1180, 240, 500, "#22405f", MUST))
    b.append(building(590, 1260, 220, 420, "#1d3350", MUST))
    b.append(building(850, 1200, 200, 480, "#22405f", MUST))
    for i, (cx, cy, r) in enumerate(((300, 900, 200), (620, 820, 240), (880, 980, 170), (150, 1050, 140))):
        b.append(f'<g class="gas{i}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEAL}" opacity="0.28"/>'
                 f'<circle cx="{cx-r*0.4}" cy="{cy+r*0.3}" r="{r*0.7}" fill="{TEAL}" opacity="0.22"/>'
                 f'<circle cx="{cx+r*0.5}" cy="{cy+r*0.2}" r="{r*0.6}" fill="{TEAL}" opacity="0.2"/></g>')
    b.append(t(70, 250, "ГАЗ", 96, TEAL, ls=8))
    b.append(t(70, 330, "над городом", 34, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg("#1a2333")]
    b.append(f'<rect x="0" y="1500" width="1080" height="420" fill="{DEEP}"/>')
    for i, x in enumerate((60, 220, 380, 760, 900)):
        b.append(building(x, 900 + (i % 2) * 80, 130, 600 - (i % 2) * 80, "#243450", MUST, f"b{i}", 4, 3))
    # грузовик
    b.append('<g class="truck">')
    b.append(f'<rect x="600" y="1320" width="300" height="150" rx="10" fill="{MUST}"/>')
    b.append(f'<rect x="880" y="1360" width="110" height="110" rx="10" fill="{MUST}"/>')
    b.append(f'<rect x="892" y="1374" width="70" height="46" fill="{NAVY}"/>')
    b.append(f'<circle cx="680" cy="1486" r="36" fill="{NAVY}"/><circle cx="920" cy="1486" r="36" fill="{NAVY}"/>')
    b.append('</g>')
    b.append(person(240, 1500, 1.25, CREAM, "run1", True))
    b.append(person(430, 1520, 1.15, CREAM, "run2", True))
    b.append(person(920, 1500, 1.35, RED, "sold1"))
    b.append(person(1010, 1505, 1.3, RED, "sold2"))
    b.append(t(70, 250, "ПАНИКА", 72, RED, ls=6))
    b.append(t(70, 320, "улицы · техника · солдаты", 26, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(CREAM)]
    # часы
    b.append('<g class="clock">')
    b.append(f'<circle cx="270" cy="760" r="150" fill="{NAVY}"/>')
    b.append(f'<circle cx="270" cy="760" r="120" fill="{CREAM}"/>')
    b.append(f'<rect x="262" y="670" width="16" height="96" fill="{NAVY}"/>')
    b.append(f'<rect x="270" y="752" width="76" height="16" fill="{RED}"/>')
    b.append('</g>')
    # газета
    b.append('<g class="news">')
    b.append(f'<rect x="470" y="600" width="520" height="700" fill="#fffaf0" stroke="{NAVY}" stroke-width="6"/>')
    b.append(t(730, 700, "ПОСТАНОВКА", 44, NAVY, "middle", 900))
    b.append(t(730, 760, "по Уэллсу", 30, RED, "middle", 800))
    for i in range(5):
        b.append(f'<rect x="510" y="{820+i*52}" width="440" height="16" fill="{GREY}"/>')
    b.append(f'<rect x="510" y="1120" width="220" height="120" fill="{NAVY}" opacity="0.25"/>')
    b.append('</g>')
    b.append(t(70, 250, "ЧЕРЕЗ ЧАС", 44, RED, ls=4))
    b.append(t(70, 320, "это была постановка", 34, NAVY, w=800))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg("#2a0f0c")]
    b.append(f'<circle cx="540" cy="1100" r="520" fill="{RED}" opacity="0.18"/>')
    b.append(building(260, 760, 560, 700, "#3a1a14", MUST, "bldg7", 6, 5))
    # пламя
    for i, (x, h, cls) in enumerate(((310, 380, "f0"), (440, 500, "f1"), (570, 430, "f2"), (700, 540, "f3"), (800, 360, "f4"))):
        b.append(f'<g class="{cls}"><path d="M {x-70} 760 q 70 -{h} 140 0 q -40 40 -70 20 q -30 20 -70 -20 z" fill="{MUST}"/>'
                 f'<path d="M {x-40} 760 q 40 -{h*0.6:.0f} 80 0 z" fill="{RED}"/></g>')
    # толпа
    for i, x in enumerate((90, 190, 290, 390, 490, 610, 710, 810, 930)):
        b.append(f'<g class="crowd"><circle cx="{x}" cy="1555" r="30" fill="{CREAM}"/>'
                 f'<path d="M {x-30} 1590 q 30 -18 60 0 l 8 130 l -76 0 z" fill="{CREAM}"/></g>')
    b.append(f'<rect x="0" y="1700" width="1080" height="220" fill="{BLACK}" opacity="0.5"/>')
    b.append(t(70, 250, "РЕДАКЦИЯ", 44, MUST, ls=4))
    b.append(t(70, 320, "сожжена толпой", 34, CREAM, w=800))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [bg(DEEP)]
    b.append(f'<rect x="0" y="0" width="1080" height="18" fill="{RED}"/>')
    b.append(radio(140, 1240, 0.9, "radio8", NAVY, RED, False))
    b.append(t(70, 380, "ФОРМАЛЬНО —", 44, GREY, ls=3))
    b.append(t(70, 500, "ШУТКА", 130, CREAM, ls=4))
    b.append(t(70, 660, "за неё заплатили", 34, MUST, w=700))
    b.append(t(70, 750, "пожаром и жизнями", 34, MUST, w=700))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [bg(NAVY)]
    b.append(f'<circle cx="540" cy="960" r="430" fill="{DEEP}"/>')
    b.append(radio(280, 760, 1.1, "radio9", CREAM, MUST, True))
    b.append(t(540, 1330, "ШУТКА, КОТОРУЮ", 50, CREAM, "middle", 900, ls=1))
    b.append(t(540, 1396, "ГОРОД ПРИНЯЛ", 50, CREAM, "middle", 900, ls=1))
    b.append(t(540, 1462, "ЗА ВОЙНУ", 50, RED, "middle", 900, ls=1))
    b.append(t(540, 1540, "Радио Кито · 1949", 26, MUST, "middle", 700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".radio1", {opacity:0, y:60}, {opacity:1, y:0, duration:0.8, ease:"back.out(1.4)"}, 0.05);'
    'tl.fromTo(".hl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.1}, 0.1);',
    'tl.fromTo(".mic", {opacity:0, y:40}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".host", {opacity:0}, {opacity:1, duration:0.7}, 0.5);'
    'tl.fromTo(".onair", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}, 0.9);'
    'tl.to(".onair", {opacity:0.45, duration:0.9, yoyo:true, repeat:-1}, 1.4);'
    'tl.fromTo(".waves circle", {opacity:0, scale:0.9}, {opacity:0.5, scale:1.05, duration:1.2, stagger:0.15, yoyo:true, repeat:2, ease:"sine.out"}, 0.3);'
    'tl.fromTo(".console", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".saucer", {opacity:0, y:-120}, {opacity:1, y:0, duration:1.0, ease:"power2.out"}, 0.1);'
    'tl.to(".saucer", {y:-12, duration:1.6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".gas0", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.9}, 0.1);'
    'tl.fromTo(".gas1", {opacity:0, x:40}, {opacity:1, x:0, duration:0.9}, 0.3);'
    'tl.fromTo(".gas2", {opacity:0, y:-40}, {opacity:1, y:0, duration:0.9}, 0.5);'
    'tl.fromTo(".gas3", {opacity:0, y:40}, {opacity:1, y:0, duration:0.9}, 0.7);'
    'tl.to(".gas0, .gas1, .gas2, .gas3", {y:-18, duration:2.2, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.2);',
    'tl.fromTo(".run1", {opacity:0, x:-60}, {opacity:1, x:0, duration:0.6}, 0.1);'
    'tl.fromTo(".run2", {opacity:0, x:-60}, {opacity:1, x:0, duration:0.6}, 0.3);'
    'tl.to(".run1", {x:26, duration:0.5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.to(".run2", {x:22, duration:0.55, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.85);'
    'tl.fromTo(".truck", {opacity:0, x:80}, {opacity:1, x:0, duration:0.8}, 0.2);'
    'tl.fromTo(".sold1, .sold2", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.5);',
    'tl.fromTo(".clock", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.6, ease:"back.out(1.5)"}, 0.1);'
    'tl.fromTo(".news", {opacity:0, x:60}, {opacity:1, x:0, duration:0.8}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.15}, 0.2);',
    'tl.fromTo(".bldg7", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".f0, .f1, .f2, .f3, .f4", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.4);'
    'tl.to(".f0, .f1, .f2, .f3, .f4", {scaleY:1.12, duration:0.5, stagger:0.08, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".crowd", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, stagger:0.07}, 0.8);',
    'tl.fromTo(".radio8", {opacity:0, y:40}, {opacity:1, y:0, duration:0.8}, 0.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.18}, 0.4);',
    'tl.fromTo(".radio9", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.9, ease:"back.out(1.3)"}, 0.1);'
    'tl.fromTo(".hl", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6, stagger:0.25}, 0.8);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{NAVY}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
