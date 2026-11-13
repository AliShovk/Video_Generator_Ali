#!/usr/bin/env python3
"""«Вайолет Джессоп: три корабля, одна жизнь» — 14 сцен, мультфильм."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/violet")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
NL = len(STARTS)

# Границы сцен по фразам (последняя сцена — финал)
GROUPS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 8), (8, 9), (9, 10),
          (10, 12), (12, 13), (13, 14), (14, 16), (16, NL)]
B = []
for a, b in GROUPS:
    st = STARTS[a]
    en = STARTS[b] if b < NL else TOTAL
    B.append((round(st, 3), round(en - st, 3)))

SKY1 = "#ffe9c9"; SKY2 = "#cfe9f7"
INK = "#22303a"; INK2 = "#5f6f7a"
SEA = "#3f9ec0"; SEA_D = "#1f6f8b"; SEA_L = "#7fd0e6"
NIGHT = "#0e2436"; NIGHT2 = "#1b3b52"
HULL = "#f6f2e8"; HULL_D = "#cfc7b3"
FUNNEL = "#c96a4a"; FUNNEL_D = "#a14f33"
DECK = "#d9c3a0"; DECK_D = "#b49c76"
STEEL = "#8f9ba1"; STEEL_D = "#63707a"
ICE = "#dff2f8"; ICE_D = "#a8d8e8"
SKIN = "#f2c6a0"; HAIR = "#6b4a33"
COAT = "#2b3f5c"; COAT_D = "#1d2c42"
RED = "#c0392b"; YEL = "#ffd23f"; WHITE = "#ffffff"
WOOD = "#a9764a"; WOOD_D = "#7d5330"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def sky(night=False, seed=1):
    if night:
        r = random.Random(seed)
        stars = "".join(f'<circle class="st{i}" cx="{r.uniform(30,1050):.0f}" cy="{r.uniform(40,700):.0f}" '
                        f'r="{r.uniform(1.6,3.4):.1f}" fill="#ffffff" opacity="{r.uniform(0.4,0.95):.2f}"/>' for i in range(60))
        return (f'<rect width="1080" height="1920" fill="{NIGHT}"/>'
                f'<rect y="0" width="1080" height="760" fill="{NIGHT2}" opacity="0.55"/>{stars}'
                f'<circle cx="880" cy="240" r="70" fill="#f4f1dd" opacity="0.95"/>'
                f'<circle cx="906" cy="222" r="60" fill="{NIGHT2}" opacity="0.9"/>')
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{SKY1}"/><stop offset="0.6" stop-color="{SKY2}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sky)"/>')


def sea(y=1300, night=False, cls="sea", horizon=True):
    top = NIGHT2 if night else SEA
    deep = NIGHT if night else SEA_D
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="{top}"/>')
    b.append(f'<rect x="0" y="{y+180}" width="1080" height="{1920-y-180}" fill="{deep}" opacity="0.75"/>')
    for i in range(5):
        yy = y + 26 + i * 54
        b.append(f'<path class="wv{i}" d="M -60 {yy} q 90 -22 180 0 t 180 0 t 180 0 t 180 0 t 180 0 t 180 0" '
                 f'stroke="{SEA_L if not night else "#2f5d78"}" stroke-width="7" fill="none" opacity="{0.55-0.07*i:.2f}"/>')
    b.append('</g>')
    return "".join(b)


def ship(x, y, s=1.0, cls="sh", funnels=4, night=False, list_deg=0):
    """Океанский лайнер в профиль. x,y — центр корпуса у ватерлинии."""
    hw, hh = 300 * s, 74 * s
    b = [f'<g class="{cls}"><g transform="rotate({list_deg} {x} {y})">']
    b.append(f'<path d="M {x-hw} {y-hh} L {x+hw*0.86:.0f} {y-hh} L {x+hw} {y-hh*0.35:.0f} '
             f'Q {x+hw*0.9:.0f} {y+hh*0.55:.0f} {x+hw*0.55:.0f} {y+hh*0.62:.0f} L {x-hw*0.7:.0f} {y+hh*0.62:.0f} '
             f'Q {x-hw*0.96:.0f} {y+hh*0.4:.0f} {x-hw} {y-hh} Z" fill="{HULL}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<path d="M {x-hw} {y-hh*0.2:.0f} L {x+hw*0.97:.0f} {y-hh*0.2:.0f} L {x+hw} {y-hh*0.35:.0f} '
             f'Q {x+hw*0.9:.0f} {y+hh*0.55:.0f} {x+hw*0.55:.0f} {y+hh*0.62:.0f} L {x-hw*0.7:.0f} {y+hh*0.62:.0f} '
             f'Q {x-hw*0.96:.0f} {y+hh*0.4:.0f} {x-hw} {y-hh*0.2:.0f} Z" fill="{FUNNEL_D}" opacity="0.25"/>')
    # палубы
    b.append(f'<rect x="{x-hw*0.92:.0f}" y="{y-hh*1.55:.0f}" width="{hw*1.7:.0f}" height="{hh*0.55:.0f}" fill="{HULL}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="{x-hw*0.7:.0f}" y="{y-hh*2.0:.0f}" width="{hw*1.1:.0f}" height="{hh*0.45:.0f}" fill="{HULL}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M {x-hw*0.92:.0f} {y-hh*1.0:.0f} l {hw*1.7:.0f} 0" stroke="{DECK_D}" stroke-width="3" opacity="0.5"/>')
    # трубы
    for i in range(funnels):
        fx = x - hw * 0.45 + i * hw * 0.34
        b.append(f'<path d="M {fx-22*s:.0f} {y-hh*2.0:.0f} l {44*s:.0f} 0 l {10*s:.0f} {-92*s:.0f} l {-64*s:.0f} 0 z" '
                 f'fill="{FUNNEL}" stroke="{INK}" stroke-width="4"/>')
        b.append(f'<path d="M {fx-24*s:.0f} {y-hh*2.0-92*s:.0f} l {64*s:.0f} 0 l {-4*s:.0f} {14*s:.0f} l {-56*s:.0f} 0 z" fill="{FUNNEL_D}" stroke="{INK}" stroke-width="3"/>')
        if i < 3:
            b.append(f'<path class="smk{i}" d="M {fx:.0f} {y-hh*2.0-100*s:.0f} q 18 -34 0 -60 q -20 -26 2 -52" '
                     f'stroke="#ffffff" stroke-width="{14*s:.0f}" fill="none" opacity="0.35" stroke-linecap="round"/>')
    # окна
    for i in range(9):
        b.append(f'<circle cx="{x-hw*0.8+i*hw*0.19:.0f}" cy="{y-hh*0.55:.0f}" r="{5*s:.0f}" fill="{NIGHT2 if night else "#7fb3c9"}" opacity="0.8"/>')
    b.append('</g></g>')
    return "".join(b)


def cruiser(x, y, s=0.65, cls="cr"):
    b = [f'<g class="{cls}">']
    hw, hh = 240 * s, 60 * s
    b.append(f'<path d="M {x-hw} {y-hh} L {x+hw*0.82:.0f} {y-hh} L {x+hw} {y-hh*0.2:.0f} Q {x+hw*0.8:.0f} {y+hh*0.6:.0f} {x+hw*0.3:.0f} {y+hh*0.62:.0f} '
             f'L {x-hw*0.75:.0f} {y+hh*0.62:.0f} Q {x-hw*0.95:.0f} {y+hh*0.3:.0f} {x-hw} {y-hh} Z" fill="{STEEL}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="{x-hw*0.35:.0f}" y="{y-hh*2.0:.0f}" width="{hw*0.8:.0f}" height="{hh*1.0:.0f}" fill="{STEEL}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="{x-hw*0.1:.0f}" y="{y-hh*2.7:.0f}" width="{hw*0.28:.0f}" height="{hh*0.7:.0f}" fill="{STEEL_D}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M {x-hw*0.05:.0f} {y-hh*2.7:.0f} l 0 {-60*s:.0f}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M {x-hw*0.05:.0f} {y-hh*2.7-60*s:.0f} l {40*s:.0f} 0" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def violet(x, y, s=1.0, cls="vi", arm=0, hat=True, case=False):
    """Стюардесса: пальто, воротник, фартук, пучок, ноги."""
    k = s
    b = [f'<g class="{cls}"><g transform="translate({x} {y}) scale({k})">']
    # ноги и туфли
    b.append(f'<path d="M -14 150 l 0 52" stroke="{SKIN}" stroke-width="14" stroke-linecap="round"/>')
    b.append(f'<path d="M 14 150 l 0 52" stroke="{SKIN}" stroke-width="14" stroke-linecap="round"/>')
    b.append(f'<path d="M -26 204 l 24 0 l 0 14 l -30 0 z" fill="{INK}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path d="M 2 204 l 24 0 l 6 14 l -30 0 z" fill="{INK}" stroke="{INK}" stroke-width="3"/>')
    # платье
    b.append(f'<path d="M -32 0 L 32 0 L 44 152 L -44 152 Z" fill="{COAT}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M -16 20 L 16 20 L 22 150 L -22 150 Z" fill="{WHITE}" opacity="0.92" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<path d="M -20 4 L 0 34 L 20 4" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
    # руки
    b.append(f'<path class="arm" d="M -32 26 q -30 42 -22 92" stroke="{COAT}" stroke-width="17" fill="none" stroke-linecap="round"/>')
    b.append(f'<circle cx="-56" cy="120" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path class="arm2" d="M 32 26 q 26 {30+arm*16} 22 {76+arm*8}" stroke="{COAT}" stroke-width="17" fill="none" stroke-linecap="round"/>')
    b.append(f'<circle cx="54" cy="{104+arm*8}" r="9" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>')
    if case:
        b.append(f'<rect x="-84" y="118" width="56" height="44" rx="6" fill="{WOOD}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<path d="M -70 118 q 0 -14 14 -14 q 14 0 14 14" stroke="{INK}" stroke-width="3" fill="none"/>')
    # голова
    b.append(f'<circle cx="0" cy="-32" r="34" fill="{SKIN}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<path d="M -34 -40 q 34 -44 68 0 q -6 -32 -34 -34 q -28 2 -34 34 z" fill="{HAIR}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<circle cx="-36" cy="-16" r="12" fill="{HAIR}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<circle cx="-12" cy="-28" r="4" fill="{INK}"/><circle cx="12" cy="-28" r="4" fill="{INK}"/>')
    b.append(f'<path d="M -7 -12 q 7 7 14 0" stroke="{INK}" stroke-width="3" fill="none"/>')
    if hat:
        b.append(f'<path d="M -38 -60 q 38 -24 76 0 l 0 9 l -76 0 z" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
    b.append('</g></g>')
    return "".join(b)


def lifeboat(x, y, s=1.0, cls="lb", people=3):
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x-120*s:.0f} {y} q 120 {86*s:.0f} 240 0 l -22 {34*s:.0f} q -98 {52*s:.0f} -196 0 z" '
             f'fill="{WOOD}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<path d="M {x-120*s:.0f} {y} q 120 {86*s:.0f} 240 0" stroke="{WOOD_D}" stroke-width="8" fill="none"/>')
    for i in range(people):
        px = x - 70 * s + i * 62 * s
        b.append(f'<path d="M {px-22*s:.0f} {y-4*s:.0f} q {22*s:.0f} {-34*s:.0f} {44*s:.0f} 0 z" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<circle cx="{px:.0f}" cy="{y-40*s:.0f}" r="{15*s:.0f}" fill="{SKIN}" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<path d="M {px-16*s:.0f} {y-46*s:.0f} q {16*s:.0f} {-18*s:.0f} {32*s:.0f} 0" fill="{HAIR}" stroke="{INK}" stroke-width="2"/>')
    b.append(f'<path class="oar" d="M {x+96*s:.0f} {y+6*s:.0f} l {78*s:.0f} {40*s:.0f}" stroke="{WOOD_D}" stroke-width="9" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def pier(x, y, w=420, cls="pr"):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="26" fill="{WOOD}" stroke="{INK}" stroke-width="4"/>')
    for i in range(int(w // 90)):
        px = x + 26 + i * 90
        b.append(f'<path d="M {px} {y+26} l 0 120" stroke="{WOOD_D}" stroke-width="12"/>')
    b.append(f'<path d="M {x} {y+8} l {w} 0" stroke="{WOOD_D}" stroke-width="3" opacity="0.6"/>')
    b.append('</g>')
    return "".join(b)


def iceberg(x, y, s=1.0, cls="ic"):
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x-150*s:.0f} {y} L {x-70*s:.0f} {y-190*s:.0f} L {x-10*s:.0f} {y-120*s:.0f} '
             f'L {x+60*s:.0f} {y-230*s:.0f} L {x+140*s:.0f} {y} Z" fill="{ICE}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<path d="M {x-70*s:.0f} {y-190*s:.0f} L {x-30*s:.0f} {y:.0f} M {x+60*s:.0f} {y-230*s:.0f} L {x+40*s:.0f} {y:.0f}" '
             f'stroke="{ICE_D}" stroke-width="4" opacity="0.8"/>')
    b.append(f'<path d="M {x-150*s:.0f} {y} q 150 {20*s:.0f} 290 0" stroke="{ICE_D}" stroke-width="5" fill="none"/>')
    b.append('</g>')
    return "".join(b)


def label(x, y, s, size=22, cls="lb", col=INK):
    w = len(s) * size * 0.68 + 34
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="8" fill="#ffffff" opacity="0.93" stroke="{INK2}" stroke-width="1.5"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ================================================================ 1 · хук
def s1():
    b = [sky(True)]
    b.append(sea(1320, True, "sea1"))
    for i, (sx, tilt) in enumerate(((230, 14), (540, -10), (850, 16))):
        b.append(f'<g class="sink{i}" opacity="0.95">')
        b.append(ship(sx, 1330 + i * 10, 0.52, f"sh{i}", 3, True, tilt))
        b.append('</g>')
    b.append(t(54, 210, "ТРИ КОРАБЛЯ.", 66, WHITE))
    b.append(t(54, 286, "ТРИ КАТАСТРОФЫ.", 66, WHITE))
    b.append(t(54, 362, "ОДНА ЖЕНЩИНА", 66, YEL))
    return b


# ================================================================ 2 · Вайолет
def s2():
    b = [sky(), sea(1300, False, "sea2")]
    b.append(ship(740, 1270, 1.0, "sh2", 4))
    b.append(pier(120, 1270, 380, "pr2"))
    b.append(violet(270, 1005, 1.3, "vi2", case=True))
    b.append(label(150, 430, "ВАЙОЛЕТ ДЖЕССОП · СТЮАРДЕССА", 20, "lb2"))
    b.append(t(54, 200, "МИСС", 62, INK))
    b.append(t(54, 268, "НЕПОТОПЛЯЕМАЯ", 54, SEA_D))
    return b


# ================================================================ 3 · Олимпик
def s3():
    b = [sky(), sea(1300, False, "sea3")]
    b.append(ship(480, 1290, 1.0, "sh3", 4))
    b.append(cruiser(880, 1240, 0.55, "cr3"))
    b.append(label(60, 980, "«ОЛИМПИК» · 1911", 22, "lb3"))
    return b


# ================================================================ 4 · столкновение
def s4():
    b = [sky(), sea(1300, False, "sea4")]
    b.append(ship(560, 1290, 1.0, "sh4", 4, list_deg=-4))
    b.append(cruiser(870, 1250, 0.55, "cr4"))
    b.append(f'<g class="hit"><path d="M 700 1210 l 40 -40 l -10 60 l 50 -30 l -30 60" stroke="{YEL}" stroke-width="10" fill="none" stroke-linecap="round"/></g>')
    b.append(f'<path class="hole" d="M 690 1290 q 40 30 80 0 q -10 40 -40 40 q -30 0 -40 -40 z" fill="{SEA_D}" stroke="{INK}" stroke-width="4"/>')
    b.append(label(80, 1020, "ПРОБОИНА", 22, "lb4", RED))
    return b


# ================================================================ 5 · без жертв
def s5():
    b = [sky(), sea(1360, False, "sea5")]
    b.append(ship(760, 1350, 0.8, "sh5", 4, list_deg=6))
    for i, (bx, by) in enumerate(((220, 1450), (420, 1500), (620, 1560))):
        b.append(lifeboat(bx, by, 0.9, f"lb5_{i}", 3))
    b.append(label(120, 1180, "ВСЕХ СПАСЛИ", 24, "lb5", "#2f8a4a"))
    b.append(t(54, 210, "БЕЗ ЖЕРТВ", 60, "#2f8a4a"))
    return b


# ================================================================ 6 · Титаник
def s6():
    b = [sky(), sea(1300, False, "sea6")]
    b.append(ship(590, 1270, 1.2, "sh6", 4))
    b.append(pier(90, 1270, 400, "pr6"))
    b.append(violet(240, 1010, 1.25, "vi6", case=True))
    b.append(label(60, 640, "«ТИТАНИК» · 1912", 24, "lb6"))
    b.append(t(54, 210, "ЧЕРЕЗ ГОД", 54, INK))
    return b


# ================================================================ 7 · айсберг
def s7():
    b = [sky(True)]
    b.append(sea(1320, True, "sea7"))
    b.append(iceberg(760, 1330, 1.0, "ic7"))
    b.append(ship(420, 1330, 1.0, "sh7", 4, True, -2))
    b.append(f'<g class="spark"><path d="M 620 1300 l 30 -30 M 640 1310 l 34 -18 M 610 1320 l 24 -34" stroke="{YEL}" stroke-width="7" stroke-linecap="round"/></g>')
    b.append(t(54, 210, "НОЧЬ.", 58, WHITE))
    b.append(t(54, 276, "АЙСБЕРГ.", 58, "#8fd8ee"))
    return b


# ================================================================ 8 · тонет
def s8():
    b = [sky(True)]
    b.append(sea(1280, True, "sea8"))
    b.append(f'<g class="sink8">')
    b.append(ship(540, 1180, 1.15, "sh8", 4, True, 24))
    b.append('</g>')
    b.append(f'<path class="waterring" d="M 180 1300 q 360 60 720 0" stroke="{SEA_L}" stroke-width="8" fill="none" opacity="0.6"/>')
    b.append(t(54, 210, "2 ЧАСА", 60, WHITE))
    b.append(t(54, 276, "40 МИНУТ", 60, WHITE))
    return b


# ================================================================ 9 · 1496
def s9():
    b = [sky(True)]
    b.append(sea(1500, True, "sea9"))
    b.append(t(540, 760, "1496", 190, "#ff7a6a", "middle", 900))
    b.append(t(540, 850, "ЧЕЛОВЕК ПОГИБ", 34, WHITE, "middle", 800))
    b.append(f'<g class="drown5" opacity="0.5">')
    b.append(ship(540, 1520, 0.75, "sh9", 4, True, 34))
    b.append('</g>')
    b.append(f'<g class="ripple"><ellipse cx="540" cy="1500" rx="240" ry="26" fill="{SEA_L}" opacity="0.25"/></g>')
    return b


# ================================================================ 10 · шлюпка 16
def s10():
    b = [sky(True)]
    b.append(sea(1250, True, "sea10"))
    b.append(lifeboat(600, 1290, 1.6, "lb10", 1))
    b.append(violet(500, 1080, 1.15, "vi10", arm=1, hat=True))
    b.append(f'<g class="child"><path d="M 552 1122 q 16 -26 34 0 z" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>'
             f'<circle cx="569" cy="1102" r="17" fill="{SKIN}" stroke="{INK}" stroke-width="4"/></g>')
    b.append(f'<path d="M 408 1300 q 192 132 384 0" stroke="{WOOD}" stroke-width="30" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M 408 1300 q 192 132 384 0" stroke="{WOOD_D}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    b.append(label(250, 830, "ШЛЮПКА № 16", 26, "lb10l", SEA_D))
    return b


# ================================================================ 11 · Британик
def s11():
    b = [sky(), sea(1300, False, "sea11")]
    b.append(ship(520, 1290, 1.0, "sh11", 3))
    b.append(f'<circle cx="850" cy="400" r="80" fill="{YEL}" opacity="0.9"/>')
    b.append(label(70, 980, "«БРИТАНИК» · 1916", 22, "lb11"))
    return b


# ================================================================ 12 · мина
def s12():
    b = [sky(), sea(1320, False, "sea12")]
    b.append(ship(520, 1300, 1.0, "sh12", 3, list_deg=5))
    b.append(f'<g class="boom"><circle cx="700" cy="1290" r="60" fill="{YEL}" opacity="0.9"/>'
             f'<circle cx="700" cy="1290" r="110" fill="#ff8a3c" opacity="0.5"/></g>')
    b.append(f'<g class="debris"><rect x="660" y="1180" width="26" height="26" fill="{STEEL}" stroke="{INK}" stroke-width="3" transform="rotate(20 673 1193)"/>'
             f'<rect x="730" y="1130" width="20" height="20" fill="{STEEL_D}" stroke="{INK}" stroke-width="3" transform="rotate(-30 740 1140)"/></g>')
    b.append(label(60, 1000, "НЕМЕЦКАЯ МИНА", 22, "lb12", RED))
    b.append(t(54, 210, "СРЕДИЗЕМНОЕ", 46, INK))
    b.append(t(54, 268, "МОРЕ", 46, SEA_D))
    return b


# ================================================================ 13 · 30 шлюпок
def s13():
    b = [sky(), sea(1240, False, "sea13")]
    b.append(f'<circle cx="860" cy="330" r="120" fill="#ffffff" opacity="0.75" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(860, 310, "30", 80, SEA_D, "middle", 900))
    b.append(t(860, 370, "ШЛЮПОК", 26, INK, "middle", 800))
    b.append(label(560, 470, "ЗА 30 МИНУТ", 22, "lb13", "#2f8a4a"))
    for i in range(4):
        b.append(lifeboat(150 + i * 230, 1400 + (i % 2) * 60, 0.7, f"lb13_{i}", 2))
    b.append(t(54, 210, "ВЧЕТВЕРО", 52, INK))
    b.append(t(54, 268, "БЫСТРЕЕ", 52, SEA_D))
    return b


# ================================================================ 14 · финал
def s14():
    b = [sky(), sea(1300, False, "sea14")]
    b.append(ship(770, 1275, 0.95, "sh14", 4))
    b.append(violet(250, 1030, 1.2, "vi14", case=True))
    b.append(t(54, 210, "ДО ПЕНСИИ", 46, INK))
    b.append(t(54, 268, "В МОРЕ", 46, SEA_D))
    b.append(t(540, 760, "1887 — 1971", 34, INK2, "middle", 800, cls="yrs"))
    b.append(t(540, 1740, "ТРИ КОРАБЛЯ.", 44, WHITE, "middle", 900, cls="fin1"))
    b.append(t(540, 1800, "ОДНА ЖИЗНЬ.", 44, YEL, "middle", 900, cls="fin2"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]

WAVE = ('tl.to(".wv0, .wv1, .wv2, .wv3, .wv4", {x:-180, duration:3.2, repeat:-1, ease:"none"}, 0);')

ANIM = [
    # 1
    WAVE + 'tl.fromTo(".sink0", {opacity:0, y:40}, {opacity:1, y:0, duration:0.5}, 0.1);'
    'tl.fromTo(".sink1", {opacity:0, y:40}, {opacity:1, y:0, duration:0.5}, 0.45);'
    'tl.fromTo(".sink2", {opacity:0, y:40}, {opacity:1, y:0, duration:0.5}, 0.8);'
    'tl.to(".sink0, .sink1, .sink2", {y:40, rotation:3, duration:2.4, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.2);'
    'tl.fromTo(".hl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.4, stagger:0.22}, 0.2);',
    # 2
    WAVE + 'tl.fromTo(".sh2", {opacity:0, x:120}, {opacity:1, x:0, duration:0.9}, 0.1);'
    'tl.fromTo(".vi2", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.4);'
    'tl.to(".vi2", {y:-10, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".lb2", {opacity:0}, {opacity:1, duration:0.4}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    # 3
    WAVE + 'tl.fromTo(".sh3", {opacity:0, x:-120}, {opacity:1, x:0, duration:1.0}, 0.1);'
    'tl.fromTo(".cr3", {opacity:0, x:140}, {opacity:1, x:0, duration:1.0}, 0.5);'
    'tl.to(".sh3", {y:-8, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.to(".cr3", {y:8, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".lb3", {opacity:0}, {opacity:1, duration:0.4}, 1.0);',
    # 4
    WAVE + 'tl.fromTo(".sh4", {x:-40}, {x:0, duration:0.5}, 0.1);'
    'tl.fromTo(".cr4", {x:120, opacity:0}, {x:0, opacity:1, duration:0.7, ease:"power2.out"}, 0.1);'
    'tl.fromTo(".hit", {opacity:0, scale:0.6}, {opacity:1, scale:1, duration:0.3}, 0.65);'
    'tl.to(".hit", {opacity:0, duration:0.3}, 1.4);'
    'tl.fromTo(".hole", {opacity:0, scale:0.5}, {opacity:1, scale:1, duration:0.5}, 1.0);'
    'tl.to(".sh4", {rotation:-3, duration:1.6, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".lb4", {opacity:0}, {opacity:1, duration:0.4}, 1.5);',
    # 5
    WAVE + 'tl.to(".sh5", {rotation:7, duration:2.4, ease:"sine.out"}, 0.1);'
    'tl.fromTo(".lb5_0", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.4);'
    'tl.fromTo(".lb5_1", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.6);'
    'tl.fromTo(".lb5_2", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.8);'
    'tl.to(".lb5_0, .lb5_1, .lb5_2", {y:-14, duration:1.0, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".lb5", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.3);',
    # 6
    WAVE + 'tl.fromTo(".sh6", {opacity:0, x:120}, {opacity:1, x:0, duration:1.0}, 0.1);'
    'tl.fromTo(".vi6", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.5);'
    'tl.to(".vi6", {y:-8, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".lb6", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.3);',
    # 7
    WAVE + 'tl.fromTo(".ic7", {opacity:0, x:80}, {opacity:1, x:0, duration:1.0}, 0.1);'
    'tl.fromTo(".sh7", {opacity:0, x:-90}, {opacity:1, x:0, duration:1.2}, 0.1);'
    'tl.fromTo(".spark", {opacity:0}, {opacity:1, duration:0.3}, 0.9);'
    'tl.to(".spark", {opacity:0, duration:0.4}, 1.5);'
    'tl.to(".sh7", {x:40, duration:2.0, ease:"power1.inOut"}, 1.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    # 8
    WAVE + 'tl.fromTo(".sh8", {rotation:10}, {rotation:26, duration:2.4, ease:"power1.in"}, 0.1);'
    'tl.to(".sh8", {y:120, duration:2.4, ease:"power1.in"}, 0.1);'
    'tl.to(".waterring", {scaleX:1.1, opacity:0.3, duration:1.6, yoyo:true, repeat:-1}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.2}, 0.2);',
    # 9
    WAVE + 'tl.fromTo(".hl", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.6, ease:"back.out(1.6)"}, 0.1);'
    'tl.fromTo(".drown5", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.6);'
    'tl.to(".drown5", {y:-20, duration:2.0, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);',
    # 10
    WAVE + 'tl.fromTo(".lb10", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.to(".lb10", {y:-10, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".vi10", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6}, 0.5);'
    'tl.fromTo(".child", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.fromTo(".lb10l", {opacity:0}, {opacity:1, duration:0.4}, 1.0);',
    # 11
    WAVE + 'tl.fromTo(".sh11", {opacity:0, x:-120}, {opacity:1, x:0, duration:1.0}, 0.1);'
    'tl.to(".sh11", {y:-8, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".lb11", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.3);',
    # 12
    WAVE + 'tl.fromTo(".sh12", {x:-30}, {x:0, duration:0.4}, 0.1);'
    'tl.fromTo(".boom", {opacity:0, scale:0.4}, {opacity:1, scale:1.2, duration:0.4, ease:"power2.out"}, 0.45);'
    'tl.to(".boom", {opacity:0.1, scale:1.6, duration:0.6}, 0.9);'
    'tl.fromTo(".debris", {opacity:0, y:20}, {opacity:1, y:-40, duration:1.2, ease:"power1.out"}, 0.5);'
    'tl.to(".sh12", {rotation:6, duration:2.0}, 0.6);'
    'tl.fromTo(".lb12", {opacity:0}, {opacity:1, duration:0.4}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.2}, 0.2);',
    # 13
    WAVE + 'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.15}, 0.1);'
    'tl.fromTo(".lb13", {opacity:0}, {opacity:1, duration:0.4}, 0.5);'
    'tl.fromTo(".lb13_0, .lb13_1, .lb13_2, .lb13_3", {opacity:0, y:24}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.5);'
    'tl.to(".lb13_0, .lb13_1, .lb13_2, .lb13_3", {y:-12, duration:0.9, stagger:0.12, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);',
    # 14
    WAVE + 'tl.fromTo(".sh14", {opacity:0, x:100}, {opacity:1, x:0, duration:1.0}, 0.1);'
    'tl.fromTo(".vi14", {opacity:0}, {opacity:1, duration:0.7}, 0.4);'
    'tl.to(".vi14", {y:-8, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.15}, 0.2);'
    'tl.fromTo(".yrs", {opacity:0}, {opacity:1, duration:0.5}, 0.9);'
    'tl.fromTo(".fin1", {opacity:0, y:14}, {opacity:1, y:0, duration:0.5}, 1.6);'
    'tl.fromTo(".fin2", {opacity:0, y:14}, {opacity:1, y:0, duration:0.5}, 1.9);',
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
