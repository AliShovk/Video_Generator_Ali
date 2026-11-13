#!/usr/bin/env python3
"""«Алькатрас» — 8 сцен, разноцветный мультик."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/alcatraz")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

INK = "#22313c"
SKY_N = "#2b2d6e"
SKY_D = "#ffd93d"
SEA = "#4ecdc4"
SEA_D = "#2f9e96"
CORAL = "#ff6b6b"
PURPLE = "#6c5ce7"
SAND = "#ffe8a3"
WHITE = "#fffaf0"
GREEN = "#7ed957"
ORANGE = "#ff9f1c"


def t(x, y, s, size=46, col=WHITE, anchor="start", w=900, ls=0, cls="hl", stroke=None):
    st = f' stroke="{stroke}" stroke-width="8" paint-order="stroke" stroke-linejoin="round"' if stroke else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}"{st}>{s}</text>')


def dots(n=40, seed=1, col=WHITE, op=0.18):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(3,8):.0f}" '
                   f'fill="{col}" opacity="{op}"/>' for _ in range(n))


def stars(n=26, seed=3):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = r.uniform(40, 1040), r.uniform(60, 900)
        s = r.uniform(4, 10)
        out.append(f'<path class="star" d="M {x} {y-s} L {x+s*0.35} {y-s*0.3} L {x+s} {y} L {x+s*0.35} {y+s*0.3} '
                   f'L {x} {y+s} L {x-s*0.35} {y+s*0.3} L {x-s} {y} L {x-s*0.35} {y-s*0.3} Z" fill="{WHITE}" opacity="{r.uniform(0.5,1):.2f}"/>')
    return "".join(out)


def guy(x, y, s=1.0, shirt=CORAL, skin="#f7c8a0", cls="guy", cap=None, oars=False):
    """Мультяшный человечек с толстым контуром."""
    b = [f'<g class="{cls}">']
    # ноги
    b.append(f'<rect x="{x-30*s}" y="{y-16*s}" width="{26*s}" height="{58*s}" rx="{12*s}" fill="{PURPLE}" stroke="{INK}" stroke-width="{6*s}"/>')
    b.append(f'<rect x="{x+6*s}" y="{y-16*s}" width="{26*s}" height="{58*s}" rx="{12*s}" fill="{PURPLE}" stroke="{INK}" stroke-width="{6*s}"/>')
    # тело
    b.append(f'<rect x="{x-42*s}" y="{y-96*s}" width="{84*s}" height="{84*s}" rx="{26*s}" fill="{shirt}" stroke="{INK}" stroke-width="{6*s}"/>')
    # руки
    if oars:
        b.append(f'<path d="M {x-42*s} {y-70*s} l {-40*s} {10*s}" stroke="{INK}" stroke-width="{12*s}" stroke-linecap="round"/>')
        b.append(f'<path d="M {x+42*s} {y-70*s} l {40*s} {10*s}" stroke="{INK}" stroke-width="{12*s}" stroke-linecap="round"/>')
    # голова
    b.append(f'<circle cx="{x}" cy="{y-134*s}" r="{40*s}" fill="{skin}" stroke="{INK}" stroke-width="{6*s}"/>')
    b.append(f'<circle cx="{x-14*s}" cy="{y-142*s}" r="{5*s}" fill="{INK}"/>')
    b.append(f'<circle cx="{x+14*s}" cy="{y-142*s}" r="{5*s}" fill="{INK}"/>')
    b.append(f'<path d="M {x-12*s} {y-122*s} q {12*s} {12*s} {24*s} 0" stroke="{INK}" stroke-width="{5*s}" fill="none" stroke-linecap="round"/>')
    if cap:
        b.append(f'<path d="M {x-42*s} {y-158*s} q {42*s} {-34*s} {84*s} 0 l {0} {10*s} l {-84*s} 0 z" fill="{cap}" stroke="{INK}" stroke-width="{5*s}"/>')
    b.append('</g>')
    return "".join(b)


def raft(x, y, s=1.0, cls="raft"):
    b = [f'<g class="{cls}">']
    b.append(f'<ellipse cx="{x}" cy="{y}" rx="{150*s}" ry="{40*s}" fill="{WHITE}" stroke="{INK}" stroke-width="7"/>')
    for i in range(4):
        b.append(f'<path d="M {x-110*s+i*60*s} {y-26*s} q {20*s} {26*s} {40*s} 0" fill="none" stroke="{SEA_D}" stroke-width="4"/>')
    b.append('</g>')
    return "".join(b)


def waves(y, col=SEA_D, op=0.9, cls="wv", amp=22):
    out = [f'<g class="{cls}" opacity="{op}">']
    for i in range(0, 1200, 100):
        out.append(f'<path d="M {i-60} {y} q 25 -{amp} 50 0 q 25 {amp} 50 0" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
    out.append('</g>')
    return "".join(out)


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{SKY_N}"/>', stars(30, 2)]
    b.append(f'<circle cx="860" cy="330" r="92" fill="{SKY_D}" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<rect x="0" y="1180" width="1080" height="740" fill="{SEA}"/>')
    b.append(waves(1240, SEA_D, 0.85, "w1"))
    b.append(waves(1330, SEA_D, 0.6, "w2"))
    # прожектор
    b.append(f'<g class="beam"><path d="M 300 1500 L 720 1150 L 840 1300 Z" fill="{WHITE}" opacity="0.18"/></g>')
    b.append(f'<path d="M 0 1620 L 180 1500 L 380 1580 L 380 1700 L 0 1700 Z" fill="#2f4858" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<rect x="110" y="1400" width="210" height="130" rx="12" fill="#3d5a6c" stroke="{INK}" stroke-width="7"/>')
    b.append(f'<rect x="136" y="1430" width="34" height="40" rx="6" fill="{SKY_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="198" y="1430" width="34" height="40" rx="6" fill="{SKY_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="260" y="1430" width="34" height="40" rx="6" fill="{SKY_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="330" y="1400" width="52" height="130" fill="#3d5a6c" stroke="{INK}" stroke-width="7"/>')
    b.append(f'<circle cx="356" cy="1392" r="18" fill="{SKY_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(raft(600, 1410, 1.45, "raft1"))
    b.append(guy(520, 1398, 0.9, CORAL, "#f7c8a0", "g1a", None, True))
    b.append(guy(600, 1390, 0.88, GREEN, "#e8b48c", "g1b", None, True))
    b.append(guy(678, 1398, 0.88, PURPLE, "#f7c8a0", "g1c", None, True))
    b.append(f'<rect x="0" y="1640" width="1080" height="280" fill="{SEA_D}" opacity="0.45"/>')
    b.append(t(60, 660, "ПОБЕГ ИЗ", 66, WHITE, ls=2, stroke=INK))
    b.append(t(60, 760, "АЛЬКАТРАСА", 66, SKY_D, ls=2, stroke=INK))
    b.append(t(64, 840, "1962 · трое · ни следа", 28, WHITE, w=700, stroke=INK))
    b.append(t(60, 1700, "самая охраняемая тюрьма Америки", 22, WHITE, w=700, stroke=INK))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{SKY_D}"/>']
    b.append(f'<rect x="0" y="1120" width="1080" height="800" fill="{SEA}"/>')
    b.append(waves(1160, SEA_D, 0.7, "wv2"))
    # остров с тюрьмой
    b.append(f'<path d="M 120 1120 q 220 -80 420 -30 q 220 50 420 -10 l 0 90 l -840 0 z" fill="{SAND}" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<rect x="380" y="880" width="340" height="220" rx="20" fill="{WHITE}" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<rect x="420" y="930" width="70" height="70" rx="10" fill="{SKY_N}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<rect x="520" y="930" width="70" height="70" rx="10" fill="{SKY_N}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<rect x="620" y="930" width="70" height="70" rx="10" fill="{SKY_N}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<path d="M 620 880 l 60 -70 l 60 70 z" fill="{CORAL}" stroke="{INK}" stroke-width="7"/>')
    # календарь
    b.append('<g class="cal">')
    b.append(f'<rect x="120" y="250" width="420" height="420" rx="26" fill="{WHITE}" stroke="{INK}" stroke-width="9"/>')
    b.append(f'<rect x="120" y="250" width="420" height="110" rx="26" fill="{CORAL}" stroke="{INK}" stroke-width="9"/>')
    b.append(t(330, 330, "ИЮНЯ", 48, WHITE, "middle", 900, stroke=None))
    b.append(t(330, 520, "11", 170, INK, "middle", 900))
    b.append(t(330, 610, "1962", 44, PURPLE, "middle", 900))
    b.append('</g>')
    b.append(t(620, 400, "НОЧЬ", 40, INK, w=900))
    b.append(t(60, 1760, "Фрэнк Моррис и братья Англины", 26, WHITE, w=800, stroke=INK))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{PURPLE}"/>']
    b.append(f'<rect x="70" y="500" width="940" height="900" rx="34" fill="{WHITE}" stroke="{INK}" stroke-width="10"/>')
    # дыра в стене
    b.append('<g class="hole">')
    b.append(f'<path d="M 760 640 q 90 10 90 110 q 0 100 -90 110 q -40 -10 -40 -110 q 0 -100 40 -110 z" fill="{INK}"/>')
    b.append(f'<path d="M 770 660 q 60 10 60 90 q 0 80 -60 90" fill="none" stroke="{SAND}" stroke-width="8"/>')
    b.append('</g>')
    # три койки с головами
    for i, y in enumerate((760, 1010, 1260)):
        b.append(f'<g class="bunk"><rect x="130" y="{y}" width="520" height="34" rx="12" fill="{SKY_D}" stroke="{INK}" stroke-width="7"/>'
                 f'<rect x="150" y="{y-120}" width="120" height="120" rx="20" fill="{SEA}" stroke="{INK}" stroke-width="7"/>'
                 f'<rect x="150" y="{y+34}" width="16" height="70" fill="{INK}"/><rect x="620" y="{y+34}" width="16" height="70" fill="{INK}"/>')
        b.append(f'<circle cx="330" cy="{y-60}" r="58" fill="{SAND}" stroke="{INK}" stroke-width="7"/>')
        b.append(f'<circle cx="312" cy="{y-72}" r="7" fill="{INK}"/><circle cx="348" cy="{y-72}" r="7" fill="{INK}"/>')
        b.append(f'<path d="M 312 {y-40} q 18 16 36 0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')
        b.append(f'<path d="M 300 {y-96} q 30 -18 60 0" stroke="{INK}" stroke-width="5" fill="none"/>')
        b.append('</g>')
    # надзиратель
    b.append(guy(860, 1320, 0.8, "#5c6b73", "#f7c8a0", "guard", "#2f4858"))
    b.append(t(60, 330, "ПАПЬЕ-МАШЕ", 46, WHITE, ls=2))
    b.append(t(60, 400, "в койках — «спящие» головы", 24, WHITE, w=700))
    b.append(t(60, 1660, "стена пробита ложкой", 26, SKY_D, w=800))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="#1f2a44"/>']
    # шахта
    b.append(f'<rect x="300" y="300" width="480" height="1300" fill="#2c3a5c" stroke="{INK}" stroke-width="10"/>')
    for i in range(6):
        b.append(f'<rect x="330" y="{360+i*200}" width="420" height="26" rx="13" fill="{SEA}" stroke="{INK}" stroke-width="6"/>')
    # труба
    b.append(f'<rect x="700" y="300" width="60" height="1300" fill="{CORAL}" stroke="{INK}" stroke-width="8"/>')
    # лезущие
    b.append(guy(430, 1520, 0.9, GREEN, "#e8b48c", "cl1"))
    b.append(guy(530, 1240, 0.85, CORAL, "#f7c8a0", "cl2"))
    b.append(guy(620, 960, 0.8, PURPLE, "#e8b48c", "cl3"))
    b.append(f'<path class="up" d="M 880 1200 l 0 -420" stroke="{SKY_D}" stroke-width="14" stroke-dasharray="26 22" stroke-linecap="round"/>')
    b.append(f'<path d="M 880 760 l -30 50 l 60 0 z" fill="{SKY_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(t(60, 250, "ПО ТРУБАМ", 52, WHITE, ls=2))
    b.append(t(60, 1700, "вверх, к вентиляции", 26, SKY_D, w=800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{SKY_N}"/>', stars(20, 7)]
    b.append(f'<rect x="0" y="1250" width="1080" height="670" fill="{SEA}"/>')
    b.append(waves(1300, SEA_D, 0.8, "wv5"))
    b.append(f'<path d="M 0 1250 q 260 -70 540 -20 q 280 50 540 -30 l 0 80 l -1080 0 z" fill="{SAND}" stroke="{INK}" stroke-width="8"/>')
    b.append(raft(520, 1240, 1.15, "raft5"))
    # дождевики-паруса
    b.append('<g class="coats">')
    for i in range(3):
        b.append(f'<path d="M {380+i*130} 1120 q 40 -90 90 0 l -10 60 l -70 0 z" fill="{GREEN}" stroke="{INK}" stroke-width="7"/>')
    b.append('</g>')
    b.append(guy(420, 1210, 0.65, GREEN, "#e8b48c", "k1"))
    b.append(guy(520, 1206, 0.65, CORAL, "#f7c8a0", "k2"))
    b.append(guy(620, 1212, 0.65, PURPLE, "#e8b48c", "k3"))
    b.append(t(60, 300, "ПЛОТ ИЗ", 48, WHITE, ls=2))
    b.append(t(60, 380, "ДОЖДЕВИКОВ", 48, SKY_D, ls=2))
    b.append(t(60, 1700, "сшили 50 плащей", 26, WHITE, w=800, stroke=INK))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{SKY_N}"/>', stars(24, 11)]
    b.append(f'<rect x="0" y="900" width="1080" height="1020" fill="{SEA}"/>')
    b.append(waves(980, SEA_D, 0.7, "wv6"))
    b.append(waves(1080, SEA_D, 0.5, "wv6b"))
    for i, (x, y, s) in enumerate(((240, 620, 1.0), (760, 520, 1.2), (520, 340, 0.85))):
        b.append(f'<g class="q{i}"><text x="{x}" y="{y}" font-family="Nunito" font-size="{210*s}" font-weight="900" '
                 f'fill="{SKY_D}" opacity="0.9">?</text></g>')
    b.append(t(540, 1300, "НИ СЛЕДОВ", 64, WHITE, "middle", 900, ls=2, stroke=INK))
    b.append(t(540, 1390, "с июня 1962 года", 30, SKY_D, "middle", 800, stroke=INK))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="{SEA}" opacity="0.5"/>')
    b.append('<g class="env">')
    b.append(f'<rect x="120" y="620" width="840" height="560" rx="24" fill="{WHITE}" stroke="{INK}" stroke-width="9"/>')
    b.append(f'<path d="M 120 640 L 540 950 L 960 640" fill="none" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<rect x="700" y="1000" width="200" height="120" fill="{CORAL}" stroke="{INK}" stroke-width="6"/>')
    b.append(t(800, 1075, "FBI", 44, WHITE, "middle", 900))
    b.append('</g>')
    b.append(t(540, 1320, "«Я ЖИВ»", 72, INK, "middle", 900))
    b.append(t(540, 1400, "письмо якобы от Джона Англина · 2013", 24, INK, "middle", 700))
    b.append('<g class="maybe">')
    b.append(f'<rect x="240" y="1480" width="600" height="110" rx="20" fill="{CORAL}" stroke="{INK}" stroke-width="8"/>')
    b.append(t(540, 1556, "НЕ ПОДТВЕРЖДЕНО", 40, WHITE, "middle", 900))
    b.append('</g>')
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{SKY_D}"/>', dots(30, 5, WHITE, 0.22)]
    b.append(f'<circle cx="540" cy="820" r="330" fill="{CORAL}" stroke="{INK}" stroke-width="10"/>')
    b.append(t(540, 760, "АЛЬКАТРАС", 62, WHITE, "middle", 900, ls=1, stroke=INK))
    b.append(t(540, 850, "1962", 62, WHITE, "middle", 900, ls=6, stroke=INK))
    b.append(t(540, 1320, "история без финала", 34, INK, "middle", 800))
    b.append(t(540, 1700, "архив ФБР", 24, INK, "middle", 700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".raft1", {opacity:0, y:40}, {opacity:1, y:0, duration:0.8, ease:"back.out(1.6)"}, 0.05);'
    'tl.to(".raft1", {y:-10, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".g1a, .g1b, .g1c", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.5);'
    'tl.to(".beam", {x:-120, duration:3.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.to(".star", {opacity:0.25, duration:1.2, stagger:0.06, yoyo:true, repeat:-1}, 0);'
    'tl.fromTo(".hl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".cal", {opacity:0, y:-60}, {opacity:1, y:0, duration:0.8, ease:"back.out(1.5)"}, 0.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);'
    'tl.to(".wv2", {x:-40, duration:3, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);',
    'tl.fromTo(".hole", {opacity:0, scale:0.6}, {opacity:1, scale:1, duration:0.6, ease:"back.out(1.7)"}, 0.2);'
    'tl.fromTo(".bunk", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6, stagger:0.18}, 0.5);'
    'tl.fromTo(".guard", {opacity:0}, {opacity:1, duration:0.6}, 1.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".cl1", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.fromTo(".cl2", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".cl3", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.to(".up", {y:-30, duration:0.9, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".coats", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.fromTo(".raft5", {opacity:0, y:40}, {opacity:1, y:0, duration:0.7, ease:"back.out(1.5)"}, 0.4);'
    'tl.to(".raft5", {y:-10, duration:1.5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".k1, .k2, .k3", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".q0", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.fromTo(".q1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.5);'
    'tl.fromTo(".q2", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.8);'
    'tl.to(".q0, .q1, .q2", {y:-16, duration:1.6, stagger:0.15, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.6, stagger:0.15}, 0.2);',
    'tl.fromTo(".env", {opacity:0, y:60}, {opacity:1, y:0, duration:0.8, ease:"back.out(1.5)"}, 0.1);'
    'tl.fromTo(".maybe", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.3);',
    'tl.fromTo(".hl", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6, stagger:0.15}, 0.1);'
    'tl.to(".dots", {opacity:0.1, duration:1.2, yoyo:true, repeat:-1}, 0);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SKY_D}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
