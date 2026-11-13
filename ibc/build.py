#!/usr/bin/env python3
"""«Водопад из кубовой ёмкости» — 9 сцен, яркая плоская иллюстрация."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/ibc")
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
WATER = "#59bcd2"; WATER_D = "#2f8ca6"; WATER_L = "#a8e3ee"
STONE = "#d6cbb6"; STONE_D = "#a89b83"; STONE_L = "#eae2d1"
WOOD = "#a9764a"; WOOD_D = "#7d5330"
TANK = "#dde3e5"; TANK_D = "#9aa6ab"
PLANT = "#4f9b45"; PLANT_D = "#2f6d33"
SUN = "#ffb03a"; YEL = "#ffd23f"; WARM = "#ffd98a"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def fg(r):
    out = []
    for i in range(7):
        x, y = r.uniform(40, 1040), r.uniform(1560, 1840)
        out.append(plant(x, y, r.uniform(0.5, 0.9), f"fgp{i}", PLANT_D))
    for i in range(9):
        x, y = r.uniform(30, 1050), r.uniform(1500, 1860)
        c = "#ff8fa3" if i % 2 else "#ffd166"
        for k in range(5):
            a = math.radians(k * 72)
            out.append(f'<circle cx="{x+12*math.cos(a):.0f}" cy="{y+12*math.sin(a):.0f}" r="6" fill="{c}" opacity="0.95"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff3cf"/>')
    return "".join(out)


def bg(seed=1, hedge=True):
    r = random.Random(seed)
    tufts = "".join(f'<path d="M {r.uniform(0,1080):.0f} {r.uniform(1300,1880):.0f} l {r.uniform(-14,14):.0f} -{r.uniform(16,32):.0f}" '
                    f'stroke="{GRASS_D}" stroke-width="4" stroke-linecap="round" opacity="0.5"/>' for _ in range(70))
    h = ""
    if hedge:
        h = (f'<path d="M 0 900 q 90 -70 180 0 t 180 0 t 180 0 t 180 0 t 180 0 t 180 0 l 0 380 l -1080 0 z" fill="{PLANT_D}" opacity="0.25"/>'
             f'<path d="M 0 980 q 110 -60 220 0 t 220 0 t 220 0 t 220 0 t 200 0 l 0 300 l -1080 0 z" fill="{PLANT}" opacity="0.35"/>')
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{SKY1}"/><stop offset="0.55" stop-color="{SKY2}"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#sky)"/>{h}'
            f'<rect x="0" y="1260" width="1080" height="660" fill="{GRASS}"/>{tufts}{fg(r)}')


def stones(x, y, w, h, cls="sw", rows=4):
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{STONE}" stroke="{INK}" stroke-width="4"/>']
    rh = h / rows
    for r_ in range(rows):
        off = 0 if r_ % 2 == 0 else 26
        b.append(f'<path d="M {x} {y+rh*(r_+1):.0f} l {w} 0" stroke="{STONE_D}" stroke-width="3"/>')
        cx = x + off
        while cx < x + w - 10:
            bw = 46 if (int(cx) // 50) % 2 == 0 else 34
            b.append(f'<rect x="{cx:.0f}" y="{y+rh*r_+3:.0f}" width="{min(bw, x+w-cx-4):.0f}" height="{rh-6:.0f}" rx="7" '
                     f'fill="{STONE_L}" stroke="{STONE_D}" stroke-width="2"/>')
            cx += bw + 8
    b.append('</g>')
    return "".join(b)


def waterfall(x, y, w, h, cls="wf"):
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WATER_L}" opacity="0.95"/>']
    for i in range(6):
        xx = x + 6 + i * (w - 12) / 6
        b.append(f'<path class="ws{i}" d="M {xx:.0f} {y} l 0 {h}" stroke="#ffffff" stroke-width="6" opacity="0.55" '
                 f'stroke-dasharray="26 34"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{WATER_D}" stroke-width="3"/>')
    b.append(f'<ellipse class="foam" cx="{x+w/2:.0f}" cy="{y+h}" rx="{w*0.55:.0f}" ry="14" fill="#ffffff" opacity="0.75"/>')
    b.append('</g>')
    return "".join(b)


def pool(x, y, w, h, cls="pl"):
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{WATER}" stroke="{WATER_D}" stroke-width="4"/>']
    for i in range(3):
        b.append(f'<path class="rp{i}" d="M {x+30} {y+26+i*30} q 60 -14 120 0 t 140 0" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.45"/>')
    b.append(f'<rect x="{x}" y="{y+h-26}" width="{w}" height="26" fill="{WATER_D}" opacity="0.35"/>')
    b.append('</g>')
    return "".join(b)


def gravel(x, y, w, h, cls="gv"):
    r = random.Random(7)
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#cfc3a8" stroke="{INK}" stroke-width="3"/>']
    for _ in range(26):
        b.append(f'<circle cx="{r.uniform(x+8,x+w-8):.0f}" cy="{r.uniform(y+8,y+h-8):.0f}" r="{r.uniform(5,11):.0f}" '
                 f'fill="{r.choice(["#b8ab8e","#e2d8c0","#a3967c"])}" stroke="{STONE_D}" stroke-width="1.5"/>')
    b.append('</g>')
    return "".join(b)


def tank(x, y, w, h, cls="tk", cut=True):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{TANK}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="{x+18}" y="{y+18}" width="{w-36}" height="{h-36}" rx="8" fill="{WATER}" opacity="0.55"/>')
    if cut:
        b.append(f'<g class="cage"><path d="M {x+18} {y+18} l {w-36} 0 l 0 {h-36} l {-w+36} 0 z" fill="none" stroke="{TANK_D}" stroke-width="6"/>'
                 f'<path d="M {x+18} {y+18} l {w-36} 0 M {x+18} {y+18} l 0 {h-36}" stroke="{TANK_D}" stroke-width="5" opacity="0.7"/></g>')
    for bx in range(x + 40, x + w - 20, 56):
        b.append(f'<path d="M {bx} {y+18} l 0 {h-36}" stroke="{TANK_D}" stroke-width="3" opacity="0.45"/>')
    for by in range(y + 60, y + h - 20, 70):
        b.append(f'<path d="M {x+18} {by} l {w-36} 0" stroke="{TANK_D}" stroke-width="3" opacity="0.45"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="none" stroke="{INK}" stroke-width="5"/>')
    b.append('</g>')
    return "".join(b)


def pump(x, y, cls="pm"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="86" height="64" rx="10" fill="#8f9ba1" stroke="{INK}" stroke-width="4"/>'
            f'<circle class="imp" cx="{x+43}" cy="{y+32}" r="20" fill="#c3ccd1" stroke="{INK}" stroke-width="3"/>'
            f'<path class="imp2" d="M {x+43} {y+16} l 0 32 M {x+27} {y+32} l 32 0" stroke="{INK}" stroke-width="3"/></g>')


def plant(x, y, s=1.0, cls="pt", col=PLANT):
    b = [f'<g class="{cls}">']
    for i in range(4):
        a = -60 + i * 30
        b.append(f'<path d="M {x} {y} q {math.sin(math.radians(a))*50*s:.0f} {-60*s:.0f} {math.sin(math.radians(a))*90*s:.0f} {-40*s:.0f}" '
                 f'stroke="{col}" stroke-width="{9*s:.0f}" fill="none" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def fish(x, y, cls="fh", col="#f4895c"):
    return (f'<g class="{cls}"><ellipse cx="{x}" cy="{y}" rx="26" ry="14" fill="{col}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {x-24} {y} l -18 -12 l 0 24 z" fill="{col}" stroke="{INK}" stroke-width="3"/>'
            f'<circle cx="{x+13}" cy="{y-3}" r="3.5" fill="{INK}"/></g>')


def bubble(x, y, r=7, cls="bb"):
    return f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity="0.7" stroke="{WATER_D}" stroke-width="2"/>'


def arrow(d, cls="ar", col=YEL, wdt=9):
    return f'<path class="{cls}" d="{d}" stroke="{col}" stroke-width="{wdt}" fill="none" stroke-linecap="round"/>'


def label(x, y, s, size=22, cls="lb", col=INK):
    w = len(s) * size * 0.58 + 26
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="8" fill="#ffffff" opacity="0.93" stroke="{INK2}" stroke-width="1.5"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ---------------------------------------------------------------- геометрия
GT = 1260      # линия земли
PT = 1190      # поверхность воды в чаше
PB = 1360      # дно чаши
WT = 860       # верх каменной стенки
WB = 1190      # основание стенки
TT = 1000      # верх ёмкости
TB = 1330      # дно ёмкости


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(1, hedge=False)]
    b.append(stones(140, WT, 340, WB - WT, "sw1"))
    b.append(waterfall(280, WT + 20, 80, WB - WT - 20, "wf1"))
    b.append(pool(110, PT, 660, PB - PT, "pl1"))
    b.append(tank(790, TT, 250, TB - TT, "tk1"))
    b.append(pump(870, TB - 90, "pm1"))
    b.append(plant(80, PT + 6, 1.0, "pt1"))
    b.append(t(50, 150, "КУБОВАЯ", 62, INK))
    b.append(t(50, 220, "ЁМКОСТЬ", 62, INK))
    b.append(t(54, 282, "стала водопадом", 30, WATER_D, w=800))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg(2, hedge=False)]
    b.append(f'<rect x="700" y="{TT}" width="330" height="{TB-TT}" fill="#8a6a45" stroke="{WOOD_D}" stroke-width="4"/>')
    b.append(tank(730, TT, 270, TB - TT, "tk2"))
    b.append(stones(140, WT, 330, WB - WT, "sw2"))
    b.append(waterfall(280, WT + 20, 70, WB - WT - 20, "wf2"))
    b.append(pool(110, PT, 540, PB - PT, "pl2"))
    b.append(label(700, 760, "ВКОПАТЬ В ГРУНТ", 22, "lb1"))
    b.append(t(50, 170, "РАЗРЕЗАТЬ", 54, INK))
    b.append(t(50, 232, "И ВКОПАТЬ", 54, WATER_D))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(3, hedge=False)]
    b.append(tank(90, TT, 250, TB - TT, "tk3"))
    b.append(pump(160, TB - 110, "pm3"))
    b.append(stones(600, WT, 320, WB - WT, "sw3"))
    b.append(waterfall(730, WT + 20, 70, WB - WT - 20, "wf3"))
    b.append(pool(480, PT, 480, PB - PT, "pl3"))
    b.append(f'<path class="loop" d="M 350 {TB-40} q 170 80 330 0 q 110 -70 60 -230" stroke="{YEL}" stroke-width="10" fill="none" stroke-dasharray="24 18"/>')
    b.append(f'<path d="M 740 {WT+70} l 0 -60 l -34 40" fill="none" stroke="{YEL}" stroke-width="10" stroke-linecap="round"/>')
    b.append(t(50, 170, "ЗАМКНУТЫЙ", 54, INK))
    b.append(t(50, 232, "КРУГ", 54, WATER_D))
    b.append(t(54, 296, "насос гонит воду обратно", 26, INK2, w=700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg(4, hedge=False)]
    b.append(pool(80, 1120, 700, 240, "pl4"))
    b.append(gravel(110, 1300, 640, 90, "gv4"))
    b.append(plant(190, 1140, 0.9, "pt4a"))
    b.append(plant(330, 1130, 1.0, "pt4b"))
    b.append(plant(470, 1140, 0.8, "pt4c"))
    for i, (bx, by) in enumerate(((160, 1190), (250, 1230), (400, 1170), (520, 1220), (620, 1160))):
        b.append(bubble(bx, by, 6, f"b4_{i}"))
    b.append(t(50, 170, "ГРАВИЙ,", 52, INK))
    b.append(t(50, 230, "РАСТЕНИЯ", 52, PLANT_D))
    b.append(t(50, 290, "И БАКТЕРИИ ЧИСТЯТ ВОДУ", 24, INK2, w=800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg(5, hedge=False)]
    b.append(stones(110, WT + 40, 320, WB - WT - 40, "sw5"))
    b.append(waterfall(240, WT + 60, 80, WB - WT - 60, "wf5"))
    b.append(pool(90, PT, 880, PB - PT, "pl5"))
    b.append(fish(330, PB - 60, "fh5a"))
    b.append(fish(640, PB - 100, "fh5b", "#7fc4e8"))
    for i, (bx, by) in enumerate(((250, PT + 30), (300, PT), (350, PT + 30), (700, PT + 20), (750, PT))):
        b.append(bubble(bx, by, 8, f"b5_{i}"))
    b.append(t(50, 170, "ВОДОПАД —", 52, INK))
    b.append(t(50, 230, "КИСЛОРОД", 52, WATER_D))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(6, hedge=True)]
    b.append(stones(640, WT, 300, WB - WT, "sw6"))
    b.append(waterfall(760, WT + 20, 70, WB - WT - 20, "wf6"))
    b.append(pool(120, PT, 560, PB - PT, "pl6"))
    b.append(plant(1010, PT + 20, 1.1, "pt6a"))
    b.append(plant(930, PT + 40, 0.9, "pt6b"))
    for i, (hx, hy) in enumerate(((880, 960), (940, 920), (1000, 970))):
        b.append(f'<path class="hz{i}" d="M {hx} {hy} q 20 -26 40 0" stroke="{WATER_L}" stroke-width="7" fill="none" opacity="0.6"/>')
    b.append(t(50, 170, "ВЛАЖНОСТЬ", 52, INK))
    b.append(t(50, 230, "РЯДОМ ВЫШЕ", 46, WATER_D))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg(7, hedge=False)]
    b.append(pool(120, PT, 580, PB - PT, "pl7"))
    b.append(stones(720, WT + 60, 250, WB - WT - 60, "sw7"))
    b.append(waterfall(800, WT + 80, 60, WB - WT - 80, "wf7"))
    b.append(f'<circle cx="330" cy="820" r="130" fill="#ffffff" opacity="0.85" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(330, 800, "−5 %", 54, WATER_D, "middle", 900))
    b.append(t(330, 860, "в неделю", 24, INK2, "middle", 800))
    b.append(label(560, 940, "ДОЛИВ РАЗ В НЕДЕЛЮ", 22, "lb7"))
    b.append(t(50, 170, "ИСПАРЕНИЕ", 52, INK))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [bg(8, hedge=False)]
    b.append(tank(110, TT, 250, TB - TT, "tk8"))
    b.append(pump(180, TB - 110, "pm8"))
    b.append(f'<rect x="470" y="1000" width="470" height="250" rx="14" fill="#ffffff" opacity="0.92" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(705, 1085, "60–100 ВТ", 46, INK, "middle", 900))
    b.append(t(705, 1145, "насос", 26, INK2, "middle", 700))
    b.append(t(705, 1200, "зимой чашу сливают", 24, "#c0703f", "middle", 800))
    b.append(t(50, 170, "ЦЕНА КОМФОРТА", 46, INK))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [bg(9, hedge=False)]
    b.append(tank(90, TT + 60, 200, 250, "tk9"))
    b.append(t(90, 1320, "ДО", 28, INK2, w=800))
    b.append(f'<path d="M 360 1140 l 90 0 l -30 -26 M 450 1140 l -30 26" stroke="{INK}" stroke-width="8" fill="none"/>')
    b.append(stones(540, WT + 60, 260, WB - WT - 60, "sw9"))
    b.append(waterfall(640, WT + 80, 60, WB - WT - 80, "wf9"))
    b.append(pool(490, PT, 470, PB - PT, "pl9"))
    b.append(t(540, 1440, "ПОСЛЕ", 28, PLANT_D, w=800))
    b.append(t(50, 240, "ДАЁТ БОЛЬШЕ,", 46, INK))
    b.append(t(50, 300, "ЧЕМ БЕРЁТ", 46, WATER_D))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".sw1", {opacity:0, y:16}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".tk1", {opacity:0, x:20}, {opacity:1, x:0, duration:0.6}, 0.35);'
    'tl.fromTo(".pl1", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.5}, 0.5);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:60, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.6);'
    'tl.to(".rp0, .rp1, .rp2", {x:24, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".tk2", {opacity:0, y:24}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".sw2", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".pl2", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:50, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.9);'
    'tl.fromTo(".lb1", {opacity:0}, {opacity:1, duration:0.4}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".tk3", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".pm3", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.5}, 0.4);'
    'tl.to(".pm3", {scale:1.04, duration:0.5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".sw3", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:50, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.6);'
    'tl.fromTo(".loop", {opacity:0, strokeDashoffset:340}, {opacity:1, strokeDashoffset:0, duration:1.6, ease:"none"}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.fromTo(".pl4", {opacity:0, scale:0.96}, {opacity:1, scale:1, duration:0.6}, 0.1);'
    'tl.fromTo(".gv4", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".pt4a, .pt4b, .pt4c", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 0.7);'
    'tl.to(".b4_0, .b4_1, .b4_2, .b4_3, .b4_4", {y:-40, opacity:0, duration:1.6, stagger:0.2, repeat:-1, ease:"sine.out"}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.fromTo(".sw5", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".pl5", {opacity:0}, {opacity:1, duration:0.5}, 0.4);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:50, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.5);'
    'tl.fromTo(".fh5a", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.6);'
    'tl.to(".fh5a", {x:160, duration:3.4, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".fh5b", {opacity:0, x:40}, {opacity:1, x:0, duration:0.6}, 0.9);'
    'tl.to(".fh5b", {x:-180, duration:4, repeat:-1, yoyo:true, ease:"sine.inOut"}, 1.0);'
    'tl.to(".b5_0, .b5_1, .b5_2, .b5_3, .b5_4", {y:-46, opacity:0, duration:1.4, stagger:0.2, repeat:-1, ease:"sine.out"}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.fromTo(".pl6", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".sw6", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:46, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.5);'
    'tl.fromTo(".pt6a, .pt6b", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 0.6);'
    'tl.to(".hz0, .hz1, .hz2", {y:-24, opacity:0.25, duration:1.6, stagger:0.25, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.fromTo(".pl7", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:46, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.4);'
    'tl.fromTo(".lb7", {opacity:0}, {opacity:1, duration:0.4}, 0.6);'
    'tl.fromTo(".hl", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6, stagger:0.15}, 0.3);',
    'tl.fromTo(".tk8", {opacity:0, y:18}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".pm8", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.5}, 0.4);'
    'tl.to(".pm8", {scale:1.05, duration:0.45, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.5);',
    'tl.fromTo(".tk9", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".sw9", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.to(".ws0, .ws1, .ws2, .ws3, .ws4, .ws5", {y:46, duration:0.8, stagger:0.05, repeat:-1, ease:"none"}, 0.6);'
    'tl.fromTo(".pl9", {opacity:0}, {opacity:1, duration:0.5}, 0.7);'
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
