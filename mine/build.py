#!/usr/bin/env python3
"""«Как устроена шахта» — 8 сцен, объёмная инфографика с движением."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/mine")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

SKY1 = "#eaf3f8"; SKY2 = "#d8e7f1"
INK = "#2f3b44"; INK2 = "#5b6b76"
E1 = "#e8bb7c"; E2 = "#d49f5c"; E3 = "#bd8443"
ORE = "#c9a7d6"; ORE_D = "#a87fbb"
WOOD = "#a9743f"; WOOD_D = "#7d5227"; WOOD_L = "#c99a63"
STEEL = "#a7b1b8"; STEEL_D = "#7c868d"
BLDG = "#c3dcea"; ROOF = "#456a86"
TUN = "#f6ead2"; TUN_D = "#e6d3ae"
HOT = "#d2603a"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def title(x, y, s, size=40, cls="hl", col=INK):
    w = len(s) * size * 0.60 + 36
    return (f'<g class="{cls}"><rect x="{x-14}" y="{y-size*1.05:.0f}" width="{w:.0f}" height="{size*1.55:.0f}" rx="{size*0.3:.0f}" '
            f'fill="#ffffff" opacity="0.82"/>'
            f'<text x="{x}" y="{y}" font-family="Nunito" font-size="{size}" font-weight="900" fill="{col}" letter-spacing="1">{s}</text></g>')


def sky():
    return ('<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{SKY1}"/><stop offset="1" stop-color="{SKY2}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sk)"/>')


def earth(top=520, cls="gr", seed=1):
    """Толща: градиент, слои, камешки, кромка травы."""
    r = random.Random(seed)
    pebbles = "".join(f'<ellipse cx="{r.uniform(20,1060):.0f}" cy="{r.uniform(top+40,1900):.0f}" rx="{r.uniform(4,14):.0f}" '
                      f'ry="{r.uniform(3,8):.0f}" fill="{E3}" opacity="{r.uniform(0.12,0.3):.2f}"/>' for _ in range(110))
    strata = "".join(f'<path d="M -20 {top+120+i*210} q 300 {-28} 560 0 t 560 0" stroke="{E3}" stroke-width="3" '
                     f'fill="none" opacity="0.28"/>' for i in range(7))
    return (f'<defs><linearGradient id="ear{seed}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{E1}"/><stop offset="0.5" stop-color="{E2}"/><stop offset="1" stop-color="{E3}"/>'
            f'</linearGradient></defs>'
            f'<g class="{cls}"><rect x="0" y="{top}" width="1080" height="{1920-top}" fill="url(#ear{seed})"/>{strata}{pebbles}'
            f'<rect x="0" y="{top-18}" width="1080" height="24" fill="#89ad55"/>'
            f'<rect x="0" y="{top+6}" width="1080" height="5" fill="#6d8f3f" opacity="0.5"/></g>')


def shaft(x, y1, y2, w=90, cls="sh"):
    """Ствол: крепь, направляющие, лестница."""
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y1}" width="{w}" height="{y2-y1}" fill="#3a2c1e" opacity="0.55"/>')
    b.append(f'<rect x="{x+8}" y="{y1}" width="{w-16}" height="{y2-y1}" fill="#f7ecd8"/>')
    n = int((y2 - y1) / 150)
    for i in range(n + 1):
        yy = y1 + i * 150
        b.append(f'<path d="M {x-6} {yy} l {w+12} 0" stroke="{WOOD}" stroke-width="9" stroke-linecap="round"/>')
    b.append(f'<path d="M {x+16} {y1} l 0 {y2-y1}" stroke="{STEEL_D}" stroke-width="4" opacity="0.55"/>')
    b.append(f'<path d="M {x+w-16} {y1} l 0 {y2-y1}" stroke="{STEEL_D}" stroke-width="4" opacity="0.55"/>')
    b.append('</g>')
    return "".join(b)


def incline(x1, y1, x2, y2, w=64, cls="inc"):
    """Наклонная выработка: крепь, рельсы, шпалы."""
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    L = math.hypot(x2 - x1, y2 - y1)
    b = [f'<g class="{cls}" transform="translate({x1} {y1}) rotate({ang:.2f})">']
    b.append(f'<rect x="0" y="{-w/2}" width="{L:.0f}" height="{w}" fill="{TUN}" stroke="{WOOD_D}" stroke-width="3"/>')
    b.append(f'<rect x="0" y="{-w/2}" width="{L:.0f}" height="{w*0.3:.0f}" fill="{TUN_D}"/>')
    n = int(L / 46)
    for i in range(n):
        xx = i * 46
        b.append(f'<path d="M {xx} {-w/2-4} l 0 {w+8}" stroke="{WOOD}" stroke-width="6" opacity="0.85"/>')
    b.append(f'<path d="M 0 {w*0.16:.0f} l {L:.0f} 0" stroke="{STEEL_D}" stroke-width="4"/>')
    b.append(f'<path d="M 0 {w*0.3:.0f} l {L:.0f} 0" stroke="{STEEL_D}" stroke-width="4"/>')
    b.append('</g>')
    return "".join(b)


def cart(x, y, s=1.0, cls="ct", ang=0):
    return (f'<g class="{cls}"><g transform="translate({x} {y}) rotate({ang}) scale({s})">'
            f'<path d="M -46 -44 l 92 0 l -10 46 l -72 0 z" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="3"/>'
            f'<path d="M -40 -44 q 40 -34 80 0 z" fill="{ORE_D}"/>'
            f'<circle cx="-26" cy="6" r="10" fill="{INK}"/><circle cx="26" cy="6" r="10" fill="{INK}"/>'
            f'<path d="M -46 -30 l 92 0" stroke="{WOOD_L}" stroke-width="3" opacity="0.7"/></g></g>')


def cage(x, y, s=1.0, cls="cg", n=3):
    b = [f'<g class="{cls}"><g transform="translate({x} {y}) scale({s})">']
    b.append(f'<rect x="-46" y="-96" width="92" height="112" fill="#cdd8de" stroke="{STEEL_D}" stroke-width="4"/>')
    b.append(f'<rect x="-38" y="-88" width="76" height="96" fill="#e9eef1" opacity="0.9"/>')
    for i in range(n):
        px = -26 + i * 26
        b.append(f'<circle cx="{px}" cy="-58" r="9" fill="{INK}"/>')
        b.append(f'<rect x="{px-6}" y="-48" width="12" height="34" rx="4" fill="{HOT}" opacity="0.9"/>')
        b.append(f'<rect x="{px-6}" y="-14" width="5" height="14" fill="{INK}"/><rect x="{px+1}" y="-14" width="5" height="14" fill="{INK}"/>')
    b.append(f'<circle cx="-46" cy="-30" r="4" fill="#fff3b0"/>')
    b.append(f'<path d="M 0 -96 l 0 -40" stroke="{STEEL_D}" stroke-width="4"/>')
    b.append('</g></g>')
    return "".join(b)


def skip(x, y, s=1.0, cls="sk"):
    return (f'<g class="{cls}"><g transform="translate({x} {y}) scale({s})">'
            f'<path d="M -36 -74 l 72 0 l -9 84 l -54 0 z" fill="{STEEL}" stroke="{STEEL_D}" stroke-width="4"/>'
            f'<path d="M -31 -56 l 62 0" stroke="{ORE_D}" stroke-width="9" opacity="0.85"/>'
            f'<circle cx="-22" cy="-88" r="7" fill="{STEEL_D}"/><circle cx="22" cy="-88" r="7" fill="{STEEL_D}"/>'
            f'<circle cx="-24" cy="12" r="9" fill="{INK}"/><circle cx="24" cy="12" r="9" fill="{INK}"/></g></g>')


def worker(x, y, s=1.0, cls="wk", col=INK, lamp=True):
    b = [f'<g class="{cls}"><g transform="translate({x} {y}) scale({s})">']
    b.append(f'<circle cx="0" cy="-46" r="11" fill="{col}"/>')
    if lamp:
        b.append(f'<circle cx="0" cy="-52" r="5" fill="#fff3b0"/><circle cx="0" cy="-52" r="14" fill="#fff3b0" opacity="0.35"/>')
    b.append(f'<path d="M -12 -34 l 24 0 l 4 30 l -32 0 z" fill="{col}"/>')
    b.append(f'<path d="M -8 -4 l -4 16 M 8 -4 l 4 16" stroke="{col}" stroke-width="7" stroke-linecap="round"/>')
    b.append(f'<path d="M -12 -26 l -12 12 M 12 -26 l 12 12" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')
    b.append('</g></g>')
    return "".join(b)


def headframe(x, y, s=1.0, cls="hf"):
    b = [f'<g class="{cls}"><g transform="translate({x} {y}) scale({s})">']
    b.append(f'<path d="M -78 0 L 0 -250 L 78 0" stroke="{STEEL_D}" stroke-width="11" fill="none"/>')
    b.append(f'<path d="M -46 -80 L 46 -80 M -26 -160 L 26 -160 M -13 -215 L 13 -215" stroke="{STEEL_D}" stroke-width="7"/>')
    b.append(f'<path d="M -60 -40 L 60 -120 M 60 -40 L -60 -120" stroke="{STEEL_D}" stroke-width="4" opacity="0.7"/>')
    b.append(f'<circle cx="0" cy="-258" r="28" fill="{STEEL}" stroke="{STEEL_D}" stroke-width="5"/>')
    b.append(f'<circle cx="0" cy="-258" r="9" fill="{STEEL_D}"/>')
    b.append('</g></g>')
    return "".join(b)


def building(x, y, w=150, h=115, cls="bd", roof=ROOF):
    return (f'<g class="{cls}"><rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{BLDG}" stroke="{INK2}" stroke-width="3"/>'
            f'<path d="M {x-12} {y-h} L {x+w/2} {y-h-58} L {x+w+12} {y-h} Z" fill="{roof}" stroke="{INK2}" stroke-width="3"/>'
            f'<rect x="{x+w*0.28:.0f}" y="{y-h+22}" width="{w*0.15:.0f}" height="{h*0.36:.0f}" fill="#7fa3bd"/>'
            f'<rect x="{x+w*0.57:.0f}" y="{y-h+22}" width="{w*0.15:.0f}" height="{h*0.36:.0f}" fill="#7fa3bd"/>'
            f'<rect x="{x+w*0.42:.0f}" y="{y-h-28}" width="{w*0.16:.0f}" height="34" fill="{INK2}" opacity="0.6"/></g>')


def tunnel(x, y, w, h, cls="tn"):
    """Горизонтальная выработка с крепью и лампами."""
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x} {y+h} L {x} {y+h*0.42} Q {x} {y} {x+h*0.5:.0f} {y} L {x+w-h*0.5:.0f} {y} Q {x+w} {y} {x+w} {y+h*0.42} L {x+w} {y+h} Z" '
             f'fill="{TUN}" stroke="{WOOD_D}" stroke-width="3"/>')
    b.append(f'<path d="M {x} {y+h} L {x} {y+h*0.42} Q {x} {y} {x+h*0.5:.0f} {y}" fill="none" stroke="{WOOD}" stroke-width="7"/>')
    b.append(f'<path d="M {x+w} {y+h} L {x+w} {y+h*0.42} Q {x+w} {y} {x+w-h*0.5:.0f} {y}" fill="none" stroke="{WOOD}" stroke-width="7"/>')
    for i in range(3):
        lx = x + w * (0.25 + i * 0.25)
        b.append(f'<circle class="lamp{i}" cx="{lx:.0f}" cy="{y+16}" r="7" fill="#ffe9a8"/>')
        b.append(f'<circle cx="{lx:.0f}" cy="{y+16}" r="22" fill="#ffe9a8" opacity="0.16"/>')
    b.append('</g>')
    return "".join(b)


def ore(pts, cls="ob"):
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts) + " Z"
    return (f'<g class="{cls}"><path d="{d}" fill="{ORE}" stroke="{ORE_D}" stroke-width="5"/>'
            f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.45"/>'
            f'<path d="M {pts[1][0]} {pts[1][1]+18} q 40 30 90 10" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.35"/></g>')


def lbl(x, y, s, size=20, cls="lb", col=INK):
    w = len(s) * size * 0.60 + 28
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.75:.0f}" rx="6" fill="#ffffff" opacity="0.93"/>'
            f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.75:.0f}" rx="6" fill="none" stroke="{WOOD}" stroke-width="1.6" opacity="0.7"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.25:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [sky(), earth(520, "gr1", 1)]
    b.append(building(50, 520, 150, 110, "b1"))
    b.append(headframe(300, 520, 1.0, "hf1"))
    b.append(shaft(255, 520, 1820, 90, "sh1"))
    b.append(incline(860, 520, 520, 1300, 66, "in1"))
    b.append(tunnel(330, 1120, 300, 96, "t1"))
    b.append(tunnel(330, 1380, 300, 96, "t2"))
    b.append(ore([(640, 1360), (740, 1320), (820, 1400), (760, 1490), (650, 1470)], "o1"))
    b.append(cage(300, 900, 0.9, "cg1"))
    b.append(cart(700, 900, 0.9, "ct1", 22))
    b.append(worker(420, 1216, 0.9, "wk1"))
    b.append(worker(520, 1476, 0.9, "wk2"))
    b.append(title(60, 180, "ШАХТА", 76))
    b.append(t(64, 300, "город наизнанку", 26, INK2, w=700))
    b.append(lbl(64, 640, "КОПЁР", 20, "lb1"))
    b.append(lbl(64, 1150, "ГОРИЗОНТ", 20, "lb2"))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [sky(), earth(420, "gr2", 2)]
    b.append(headframe(540, 470, 1.15, "hf2"))
    b.append(shaft(495, 470, 1820, 90, "sh2"))
    b.append(cage(540, 700, 1.5, "cg2"))
    b.append(f'<path class="rope" d="M 540 480 l 0 {700-96*1.5:.0f}" stroke="{STEEL_D}" stroke-width="5"/>')
    b.append(f'<path class="dn" d="M 700 620 l 0 200" stroke="{HOT}" stroke-width="6" stroke-linecap="round"/>')
    b.append(f'<path d="M 700 840 l -16 -26 l 32 0 z" fill="{HOT}"/>')
    b.append(f'<path class="ups" d="M 400 820 l 0 -180" stroke="{INK2}" stroke-width="5" stroke-linecap="round"/>')
    b.append(f'<path d="M 400 620 l -14 24 l 28 0 z" fill="{INK2}"/>')
    b.append(title(60, 150, "ВЕРТИКАЛЬНЫЙ СТВОЛ", 28))
    b.append(lbl(640, 700, "КЛЕТЬ · ЛЮДИ", 20, "lb3"))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [sky(), earth(420, "gr3", 3)]
    b.append(headframe(300, 420, 0.95, "hf3"))
    b.append(shaft(255, 420, 1820, 90, "sh3"))
    b.append(skip(300, 1400, 1.6, "sk3"))
    b.append(f'<path d="M 300 420 l 0 900" stroke="{STEEL_D}" stroke-width="4"/>')
    b.append(f'<path class="rise" d="M 300 1350 l 0 -780" stroke="{ORE_D}" stroke-width="4" stroke-dasharray="14 18" opacity="0.85"/>')
    b.append(ore([(600, 1300), (700, 1260), (780, 1340), (720, 1420), (610, 1400)], "o3"))
    b.append(title(60, 200, "СКИПОВЫЙ ПОДЪЁМ", 34))
    b.append(lbl(380, 1200, "СКИП С РУДОЙ", 20, "lb4"))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [sky(), earth(420, "gr4", 4)]
    b.append(incline(900, 420, 380, 1420, 70, "in4"))
    b.append(cart(760, 700, 1.15, "ct4", 48))
    b.append(cart(600, 1060, 1.15, "ct4b", 48))
    b.append(worker(470, 1300, 0.9, "wk4"))
    b.append(title(60, 200, "НАКЛОННЫЙ СТВОЛ", 32))
    b.append(lbl(600, 600, "ПО ПЛАСТУ", 20, "lb5"))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [sky(), earth(360, "gr5", 5)]
    b.append(shaft(110, 360, 1820, 86, "sh5"))
    for i, yy in enumerate((640, 960, 1280)):
        b.append(tunnel(196, yy, 780, 110, f"tn{i}"))
        b.append(worker(700, yy + 104, 1.0, f"wk{i}"))
        b.append(cart(840, yy + 104, 0.85, f"c5{i}"))
        b.append(t(210, yy + 130, f"{i+1}-Й ГОРИЗОНТ", 22, WOOD_D, w=900))
    b.append(title(60, 240, "ГОРИЗОНТЫ И ШТРЕКИ", 30))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [sky(), earth(600, "gr6", 6)]
    # воронка карьера: вынутая порода
    b.append(f'<path d="M 110 600 L 970 600 L 800 1180 L 290 1180 Z" fill="#f7f1e4" stroke="{E3}" stroke-width="4"/>')
    # уступы
    steps = [(140, 640, 800, 110), (215, 750, 650, 110), (290, 860, 500, 110), (365, 970, 360, 110)]
    for i, (x, y, w, h) in enumerate(steps):
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{E1 if i % 2 == 0 else E2}" stroke="{E3}" stroke-width="3"/>')
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="10" fill="#ffffff" opacity="0.25"/>')
    # руда на дне
    b.append(f'<path d="M 400 1090 l 300 0 l -40 80 l -220 0 z" fill="{ORE}" stroke="{ORE_D}" stroke-width="3"/>')
    # самосвал на уступе
    b.append(f'<g class="truck"><rect x="470" y="1010" width="150" height="54" rx="6" fill="{HOT}" stroke="#a2452a" stroke-width="3"/>'
             f'<rect x="620" y="1024" width="60" height="40" rx="6" fill="{HOT}" stroke="#a2452a" stroke-width="3"/>'
             f'<circle cx="512" cy="1070" r="18" fill="{INK}"/><circle cx="652" cy="1070" r="18" fill="{INK}"/></g>')
    # пыль
    for i, (dx, dy) in enumerate(((0, 0), (40, -20), (-30, -40), (20, -70))):
        b.append(f'<circle class="dust{i}" cx="{540+dx}" cy="{1080+dy}" r="{6+i*2}" fill="{E3}" opacity="0.35"/>')
    b.append(title(60, 220, "КАРЬЕР", 56))
    b.append(lbl(150, 1140, "УСТУПЫ", 22, "lb6"))
    b.append(lbl(470, 950, "РУДА", 20, "lb6b"))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [sky(), earth(300, "gr7", 7)]
    b.append(ore([(180, 640), (420, 560), (650, 660), (660, 900), (400, 960), (170, 860)], "o7"))
    b.append(tunnel(240, 700, 340, 130, "st7"))
    b.append(worker(300, 820, 0.95, "wk7"))
    b.append(f'<path d="M 640 900 l 0 420" stroke="{WOOD}" stroke-width="8" stroke-dasharray="16 14"/>')
    b.append(f'<rect x="120" y="1420" width="840" height="220" rx="60" fill="#7fb8d4" stroke="#4f8fae" stroke-width="4"/>')
    b.append(f'<path d="M 160 1500 q 120 -22 240 0 t 240 0 t 240 0" stroke="#dff1f8" stroke-width="5" fill="none" opacity="0.7"/>')
    b.append(t(540, 1600, "ЗУМПФ · ВОДА", 32, "#2c6076", "middle", 900))
    b.append(title(60, 220, "РУДНОЕ ТЕЛО", 34))
    b.append(lbl(700, 620, "ОЧИСТНАЯ КАМЕРА", 20, "lb7"))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [sky(), earth(520, "gr8", 8)]
    b.append(building(50, 520, 140, 105, "b8a"))
    b.append(headframe(300, 520, 0.85, "hf8"))
    b.append(shaft(255, 520, 1820, 86, "sh8"))
    b.append(incline(880, 520, 560, 1280, 60, "in8"))
    b.append(tunnel(330, 1020, 320, 100, "t8a"))
    b.append(tunnel(330, 1250, 300, 100, "t8b"))
    b.append(ore([(630, 1160), (740, 1120), (810, 1210), (740, 1300), (640, 1280)], "o8"))
    b.append(cage(298, 820, 0.85, "cg8"))
    b.append(worker(420, 1116, 0.9, "wk8"))
    b.append(title(60, 220, "ГОРОД НАИЗНАНКУ", 40))
    b.append(t(64, 276, "ствол · горизонты · руда", 24, INK2, w=700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".b1", {opacity:0, y:18}, {opacity:1, y:0, duration:0.5}, 0.1);'
    'tl.fromTo(".hf1", {opacity:0}, {opacity:1, duration:0.6}, 0.2);'
    'tl.fromTo(".cg1", {opacity:0, y:-120}, {opacity:1, y:0, duration:1.2}, 0.6);'
    'tl.to(".cg1", {y:220, duration:2.4, ease:"sine.inOut"}, 1.8);'
    'tl.fromTo(".ct1", {opacity:0, y:-120}, {opacity:1, y:0, duration:1.4}, 0.9);'
    'tl.to(".ct1", {y:260, duration:2.6, ease:"sine.in"}, 2.2);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.4, stagger:0.1}, 0.1);'
    'tl.fromTo(".lb1, .lb2", {opacity:0}, {opacity:1, duration:0.4, stagger:0.2}, 0.8);'
    'tl.to(".wk1", {x:16, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.2);',
    'tl.fromTo(".hf2", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".cg2", {opacity:0, y:-400}, {opacity:1, y:0, duration:1.6, ease:"power2.out"}, 0.3);'
    'tl.to(".cg2", {y:300, duration:2.4, ease:"sine.inOut"}, 2.0);'
    'tl.fromTo(".dn", {opacity:0}, {opacity:1, duration:0.4}, 0.8);'
    'tl.to(".dn, .ups", {y:24, duration:0.9, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.1);'
    'tl.fromTo(".lb3", {opacity:0}, {opacity:1, duration:0.4}, 1.2);',
    'tl.fromTo(".hf3", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.fromTo(".sk3", {opacity:0, y:420}, {opacity:1, y:0, duration:1.9, ease:"power2.out"}, 0.3);'
    'tl.to(".rise", {strokeDashoffset:-160, duration:1.4, repeat:-1, ease:"none"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.1);'
    'tl.fromTo(".lb4", {opacity:0}, {opacity:1, duration:0.4}, 1.0);',
    'tl.fromTo(".ct4", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.to(".ct4", {x:-140, y:250, duration:2.2, ease:"sine.in"}, 0.8);'
    'tl.fromTo(".ct4b", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.to(".ct4b", {x:-120, y:220, duration:2.0, ease:"sine.in"}, 1.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.1);'
    'tl.fromTo(".lb5", {opacity:0}, {opacity:1, duration:0.4}, 0.7);',
    'tl.fromTo(".tn0, .tn1, .tn2", {opacity:0, x:40}, {opacity:1, x:0, duration:0.5, stagger:0.25}, 0.1);'
    'tl.fromTo(".wk0, .wk1, .wk2", {opacity:0}, {opacity:1, duration:0.4, stagger:0.15}, 0.6);'
    'tl.to(".wk0, .wk1, .wk2", {x:44, duration:1.2, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.to(".lamp0, .lamp1, .lamp2", {opacity:0.4, duration:0.7, stagger:0.2, yoyo:true, repeat:-1}, 0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.1);',
    'tl.fromTo(".truck", {opacity:0, x:100}, {opacity:1, x:0, duration:0.8}, 0.3);'
    'tl.to(".dust0, .dust1, .dust2, .dust3", {y:-60, opacity:0, duration:1.6, stagger:0.2, repeat:-1}, 0.6);'
    'tl.to(".truck", {x:56, duration:1.8, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.1);'
    'tl.fromTo(".lb6", {opacity:0}, {opacity:1, duration:0.4}, 0.6);',
    'tl.fromTo(".o7", {opacity:0, scale:0.94, transformOrigin:"420px 760px"}, {opacity:1, scale:1, duration:0.7}, 0.1);'
    'tl.fromTo(".st7", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5}, 0.5);'
    'tl.to(".st7", {y:-8, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.1);'
    'tl.fromTo(".lb7", {opacity:0}, {opacity:1, duration:0.4}, 0.9);',
    'tl.fromTo(".b8a, .hf8", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.1);'
    'tl.fromTo(".cg8", {opacity:0, y:-120}, {opacity:1, y:0, duration:1.2}, 0.5);'
    'tl.to(".cg8", {y:200, duration:2.2, ease:"sine.inOut"}, 1.7);'
    'tl.fromTo(".wk8", {opacity:0}, {opacity:1, duration:0.4}, 0.8);'
    'tl.to(".wk8", {x:20, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.2);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.1);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SKY1}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
