#!/usr/bin/env python3
"""«Солнечный паровой насос» — 9 сцен, яркая плоская иллюстрация."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/solarpump")
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
SAND = "#e6d5b0"; SAND_D = "#c9b48a"
WATER = "#59bcd2"; WATER_D = "#2f8ca6"; WATER_L = "#a8e3ee"
STEEL = "#cfd8dd"; STEEL_D = "#8f9ba1"
COPPER = "#c9773f"; COPPER_D = "#a85c2c"; COPPER_L = "#e3a06a"
SUN = "#ffb03a"; YEL = "#ffd23f"; WARM = "#ffd98a"
PLANT = "#4f9b45"; PLANT_D = "#2f6d33"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def plant(x, y, s=1.0, cls="pt", col=PLANT_D):
    b = [f'<g class="{cls}">']
    for i in range(4):
        a = -60 + i * 30
        b.append(f'<path d="M {x} {y} q {math.sin(math.radians(a))*50*s:.0f} {-60*s:.0f} {math.sin(math.radians(a))*90*s:.0f} {-40*s:.0f}" '
                 f'stroke="{col}" stroke-width="{9*s:.0f}" fill="none" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def fg(r):
    out = []
    for i in range(6):
        x, y = r.uniform(40, 1040), r.uniform(1560, 1840)
        out.append(plant(x, y, r.uniform(0.5, 0.85), f"fgp{i}", PLANT_D if not r.random() > 0.5 else PLANT))
    for i in range(8):
        x, y = r.uniform(30, 1050), r.uniform(1500, 1860)
        c = "#ff8fa3" if i % 2 else "#ffd166"
        for k in range(5):
            a = math.radians(k * 72)
            out.append(f'<circle cx="{x+12*math.cos(a):.0f}" cy="{y+12*math.sin(a):.0f}" r="6" fill="{c}" opacity="0.95"/>')
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff3cf"/>')
    return "".join(out)


def bg(seed=1, desert=False):
    r = random.Random(seed)
    tufts = "".join(f'<path d="M {r.uniform(0,1080):.0f} {r.uniform(1300,1880):.0f} l {r.uniform(-14,14):.0f} -{r.uniform(16,30):.0f}" '
                    f'stroke="{GRASS_D}" stroke-width="4" stroke-linecap="round" opacity="0.5"/>' for _ in range(60))
    ground = f'<rect x="0" y="1260" width="1080" height="660" fill="{GRASS}"/>{tufts}'
    if desert:
        ground = f'<rect x="0" y="1260" width="1080" height="660" fill="{SAND}"/>'
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{SKY1}"/><stop offset="0.55" stop-color="{SKY2}"/></linearGradient></defs>'
            f'<rect width="1080" height="1920" fill="url(#sky)"/>{ground}{fg(r)}')


def sun(cx=880, cy=280, r=90, cls="sun"):
    b = [f'<g class="{cls}">']
    for i in range(12):
        a = math.radians(i * 30)
        b.append(f'<path class="ray{i}" d="M {cx+r*1.28*math.cos(a):.0f} {cy+r*1.28*math.sin(a):.0f} '
                 f'l {44*math.cos(a):.0f} {44*math.sin(a):.0f}" stroke="#e58a1c" stroke-width="9" stroke-linecap="round" opacity="0.85"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SUN}"/>')
    b.append(f'<circle cx="{cx-r*0.28:.0f}" cy="{cy-r*0.28:.0f}" r="{r*0.4:.0f}" fill="#ffd27a" opacity="0.7"/>')
    b.append('</g>')
    return "".join(b)


def dish(cx, cy, r=210, cls="dsh", tilt=-18):
    b = [f'<g class="{cls}">']
    b.append(f'<g transform="rotate({tilt} {cx} {cy})">')
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.92:.0f}" fill="{STEEL}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.86:.0f}" ry="{r*0.79:.0f}" fill="#eaf3f7" stroke="{STEEL_D}" stroke-width="3"/>')
    for i in range(10):
        a = math.radians(i * 36)
        b.append(f'<path d="M {cx} {cy} L {cx+r*0.86*math.cos(a):.0f} {cy+r*0.79*math.sin(a):.0f}" stroke="{STEEL_D}" stroke-width="3" opacity="0.8"/>')
    for i in range(1, 4):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.86*i/4:.0f}" ry="{r*0.79*i/4:.0f}" fill="none" stroke="{STEEL_D}" stroke-width="2" opacity="0.7"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="{STEEL_D}" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    b.append(f'<path d="M {cx} {cy+r*0.6:.0f} l 0 300" stroke="{STEEL_D}" stroke-width="12"/>')
    b.append(f'<path d="M {cx-60} {cy+r*0.6+300:.0f} l 120 0" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    b.append('</g>')
    return "".join(b)


def beams(pts, cls="bm"):
    """Сходящиеся лучи к фокусу."""
    out = [f'<g class="{cls}">']
    for i, (x1, y1) in enumerate(pts):
        out.append(f'<path class="b{i}" d="M {x1} {y1} L 520 900" stroke="{YEL}" stroke-width="7" opacity="0.55" stroke-dasharray="18 14"/>')
    out.append('</g>')
    return "".join(out)


def boiler(cx, cy, r=54, cls="bo"):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" rx="{r*0.6:.0f}" fill="{COPPER}" stroke="{COPPER_D}" stroke-width="4"/>')
    b.append(f'<rect x="{cx-r+8}" y="{cy-r+8}" width="{2*r-16}" height="16" rx="8" fill="{COPPER_L}" opacity="0.8"/>')
    b.append(f'<rect x="{cx-10}" y="{cy-r-26}" width="20" height="26" fill="{COPPER_D}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<circle cx="{cx}" cy="{cy+6}" r="10" fill="{COPPER_D}" stroke="{INK}" stroke-width="2"/>')
    b.append('</g>')
    return "".join(b)


def steam(x, y, cls="st"):
    return (f'<g class="{cls}"><path class="p0" d="M {x} {y} q -22 -40 0 -66 q 26 -30 4 -58" stroke="#ffffff" stroke-width="12" fill="none" opacity="0.85" stroke-linecap="round"/>'
            f'<path class="p1" d="M {x+26} {y} q 26 -34 6 -62 q -18 -26 4 -52" stroke="#ffffff" stroke-width="9" fill="none" opacity="0.6" stroke-linecap="round"/></g>')


def engine(x, y, cls="en"):
    """Цилиндр + поршень + шатун + маховик."""
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="96" height="230" rx="12" fill="{STEEL}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="{x+10}" y="{y+12}" width="76" height="26" rx="6" fill="{STEEL_D}" opacity="0.6"/>')
    b.append(f'<g class="piston"><rect x="{x+14}" y="{y+60}" width="68" height="42" rx="8" fill="{COPPER}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M {x+48} {y+102} l 0 96" stroke="{INK}" stroke-width="10"/></g>')
    b.append(f'<path d="M {x+48} {y+198} l 78 0" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>')
    b.append(f'<circle cx="{x+168}" cy="{y+198}" r="58" fill="{COPPER_L}" stroke="{COPPER_D}" stroke-width="6"/>')
    for i in range(8):
        a = math.radians(i * 45)
        b.append(f'<path d="M {x+168} {y+198} L {x+168+50*math.cos(a):.0f} {y+198+50*math.sin(a):.0f}" stroke="{COPPER_D}" stroke-width="4"/>')
    b.append(f'<circle cx="{x+168}" cy="{y+198}" r="10" fill="{COPPER_D}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<rect x="{x-8}" y="{y+230}" width="112" height="70" fill="{STEEL_D}" stroke="{INK}" stroke-width="4"/>')
    b.append('</g>')
    return "".join(b)


def pipe(d, cls="pp"):
    return (f'<g class="{cls}"><path d="{d}" stroke="{STEEL_D}" stroke-width="24" fill="none" stroke-linejoin="round"/>'
            f'<path d="{d}" stroke="{STEEL}" stroke-width="10" fill="none" stroke-linejoin="round" opacity="0.85"/></g>')


def well(cx, y, w=210, h=180, cls="wl"):
    """Колодец в разрезе: каменный сруб, ствол, вода."""
    half = w / 2
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{cx-half:.0f}" y="{y}" width="{w}" height="{h}" fill="#7a6a52" stroke="{INK}" stroke-width="4"/>')
    for k in range(int(h // 44)):
        yy = y + 24 + k * 44
        b.append(f'<path d="M {cx-half:.0f} {yy:.0f} l {w} 0" stroke="#5c4f3c" stroke-width="3" opacity="0.8"/>')
    wy = y + h * 0.42
    b.append(f'<rect x="{cx-half+14:.0f}" y="{wy:.0f}" width="{w-28}" height="{y+h-14-wy:.0f}" fill="{WATER}" stroke="{WATER_D}" stroke-width="3"/>')
    b.append(f'<path class="rip" d="M {cx-half+30:.0f} {wy+26:.0f} q 40 -12 80 0 t 60 0" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.6"/>')
    b.append(f'<ellipse cx="{cx}" cy="{y}" rx="{half}" ry="34" fill="{SAND_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<ellipse cx="{cx}" cy="{y}" rx="{half-24}" ry="26" fill="#6b5a45" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<ellipse cx="{cx}" cy="{y+6}" rx="{half-34}" ry="20" fill="{WATER_D}" opacity="0.9"/>')
    b.append('</g>')
    return "".join(b)


def label(x, y, s, size=22, cls="lb", col=INK):
    w = len(s) * size * 0.58 + 26
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w:.0f}" height="{size*1.7:.0f}" rx="8" fill="#ffffff" opacity="0.93" stroke="{INK2}" stroke-width="1.5"/>'
            f'<text x="{x+w/2:.0f}" y="{y+size*1.2:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle">{s}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(1), sun(880, 250, 80, "sun1")]
    b.append(dish(250, 1010, 200, "dsh1"))
    b.append(boiler(470, 900, 48, "bo1"))
    b.append(pipe("M 470 952 L 470 1000 L 700 1000", "pp1"))
    b.append(engine(700, 790, "en1"))
    b.append(well(760, 1200, 230, 290, "wl1"))
    b.append(t(48, 150, "СОЛНЦЕ", 62, INK))
    b.append(t(48, 220, "КАЧАЕТ ВОДУ", 54, COPPER_D))
    b.append(t(52, 282, "без единой батарейки", 28, INK2, w=800))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg(2), sun(860, 300, 90, "sun2")]
    b.append(dish(330, 980, 240, "dsh2"))
    b.append(beams([(700, 380), (760, 470), (660, 520)], "bm2"))
    b.append(f'<circle cx="520" cy="900" r="34" fill="{YEL}" opacity="0.55"/>')
    b.append(f'<circle class="focus" cx="520" cy="900" r="14" fill="#ffffff" opacity="0.9"/>')
    b.append(t(48, 170, "ЗЕРКАЛО", 54, INK))
    b.append(t(48, 232, "СОБИРАЕТ ЛУЧИ", 46, COPPER_D))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(3)]
    b.append(dish(280, 1000, 210, "dsh3"))
    b.append(beams([(680, 420), (720, 500)], "bm3"))
    b.append(boiler(500, 880, 72, "bo3"))
    b.append(steam(500, 800, "st3"))
    for i, (bx, by) in enumerate(((470, 900), (500, 915), (530, 905))):
        b.append(f'<circle class="bb{i}" cx="{bx}" cy="{by}" r="7" fill="#ffffff" opacity="0.8"/>')
    b.append(t(48, 170, "МЕДНЫЙ", 54, INK))
    b.append(t(48, 232, "КОТЁЛ", 54, COPPER_D))
    b.append(t(52, 296, "вода закипает в фокусе", 24, INK2, w=800))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg(4)]
    b.append(boiler(200, 900, 62, "bo4"))
    b.append(steam(200, 820, "st4"))
    b.append(pipe("M 260 900 L 560 900 L 560 800", "pp4"))
    b.append(engine(560, 760, "en4"))
    b.append(f'<path class="sp" d="M 640 900 q 40 -30 20 -60" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.7" stroke-linecap="round"/>')
    b.append(t(48, 170, "ПАР", 54, INK))
    b.append(t(48, 232, "ТОЛКАЕТ ПОРШЕНЬ", 44, COPPER_D))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg(5)]
    b.append(engine(180, 760, "en5"))
    b.append(f'<path d="M 300 990 l 0 150" stroke="{INK}" stroke-width="10"/>')
    b.append(well(340, 1200, 240, 300, "wl5"))
    b.append(f'<path class="up" d="M 300 1010 l 0 130" stroke="{WATER}" stroke-width="10" stroke-dasharray="18 14"/>')
    b.append(label(560, 900, "ШЕСТЕРНИ → НАСОС", 22, "lb5"))
    b.append(t(48, 170, "ПОРШЕНЬ", 50, INK))
    b.append(t(48, 230, "ТЯНЕТ НАСОС", 44, COPPER_D))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(6)]
    b.append(engine(200, 720, "en6"))
    b.append(f'<path d="M 320 950 l 0 120" stroke="{INK}" stroke-width="10"/>')
    b.append(well(360, 1180, 230, 280, "wl6"))
    b.append(f'<path class="stream" d="M 520 1080 q 110 -20 150 60 q 30 70 -40 110" stroke="{WATER}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    b.append(f'<path class="stream2" d="M 520 1080 q 110 -20 150 60 q 30 70 -40 110" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.55"/>')
    b.append(t(48, 170, "ВОДА ИДЁТ", 54, INK))
    b.append(t(48, 232, "ПОКА СВЕТИТ", 46, WATER_D))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg(7)]
    b.append(boiler(320, 900, 80, "bo7"))
    b.append(steam(320, 800, "st7"))
    for i, (hx, hy) in enumerate(((440, 860), (500, 900), (560, 870), (620, 910))):
        b.append(f'<path class="ht{i}" d="M {hx} {hy} q 16 -30 32 0 q 16 30 32 0" stroke="#e08a3c" stroke-width="8" fill="none" opacity="0.7"/>')
    b.append(f'<rect x="700" y="800" width="300" height="220" rx="14" fill="#ffffff" opacity="0.92" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(850, 880, "КПД", 34, INK, "middle", 800))
    b.append(t(850, 950, "низкий", 44, "#c0703f", "middle", 900))
    b.append(t(48, 170, "ТЕПЛО —", 50, INK))
    b.append(t(48, 228, "В ВОЗДУХ", 50, "#c0703f"))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [bg(8, desert=True), sun(860, 300, 80, "sun8")]
    b.append(dish(280, 1000, 200, "dsh8"))
    b.append(boiler(500, 880, 56, "bo8"))
    b.append(f'<g class="cloud"><ellipse cx="700" cy="520" rx="120" ry="50" fill="#ffffff" opacity="0.9"/>'
             f'<ellipse cx="620" cy="540" rx="80" ry="40" fill="#ffffff" opacity="0.9"/></g>')
    b.append(f'<circle cx="880" cy="1120" r="80" fill="#ffffff" opacity="0.9" stroke="{INK2}" stroke-width="4"/>')
    b.append(t(880, 1112, "6 бар", 34, "#c0392b", "middle", 900))
    b.append(f'<path d="M 880 1120 l 40 -40" stroke="#c0392b" stroke-width="6"/>')
    b.append(t(48, 170, "НУЖНО ПРЯМОЕ", 42, INK))
    b.append(t(48, 224, "СОЛНЦЕ", 46, COPPER_D))
    b.append(t(48, 288, "и осторожно с давлением", 22, "#c0392b", w=800))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [bg(9, desert=True), sun(890, 260, 80, "sun9")]
    b.append(dish(250, 1000, 190, "dsh9"))
    b.append(boiler(450, 890, 50, "bo9"))
    b.append(engine(620, 800, "en9"))
    b.append(well(760, 1200, 230, 290, "wl9"))
    b.append(t(48, 240, "НЕТ СЕТИ —", 48, INK))
    b.append(t(48, 300, "НЕ ПРОБЛЕМА", 48, COPPER_D))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".sun1", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.5}, 0.1);'
    'tl.to(".sun1", {rotate:24, transformOrigin:"880px 250px", duration:8, repeat:-1, ease:"none"}, 0.4);'
    'tl.fromTo(".dsh1", {opacity:0, x:-24}, {opacity:1, x:0, duration:0.6}, 0.2);'
    'tl.fromTo(".en1", {opacity:0}, {opacity:1, duration:0.6}, 0.6);'
    'tl.fromTo(".wl1", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5}, 0.8);'
    'tl.to(".rip", {x:26, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".dsh2", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.6}, 0.1);'
    'tl.fromTo(".b0, .b1, .b2", {opacity:0}, {opacity:0.6, duration:0.4, stagger:0.15}, 0.5);'
    'tl.to(".b0, .b1, .b2", {strokeDashoffset:-64, duration:1.2, repeat:-1, ease:"none"}, 0.8);'
    'tl.fromTo(".focus", {opacity:0.3, scale:0.7}, {opacity:1, scale:1.2, duration:0.7, yoyo:true, repeat:-1}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".bo3", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.5}, 0.1);'
    'tl.to(".st3", {y:-18, opacity:0.5, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.6);'
    'tl.to(".bb0, .bb1, .bb2", {y:-30, opacity:0, duration:1.2, stagger:0.2, repeat:-1, ease:"sine.out"}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.fromTo(".bo4", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".pp4", {opacity:0, strokeDashoffset:200}, {opacity:1, strokeDashoffset:0, duration:0.9}, 0.3);'
    'tl.fromTo(".en4", {opacity:0, x:20}, {opacity:1, x:0, duration:0.5}, 0.5);'
    'tl.to(".piston", {y:52, duration:0.55, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.7);'
    'tl.to(".sp", {y:-16, opacity:0.3, duration:0.6, yoyo:true, repeat:-1}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.fromTo(".en5", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 0.1);'
    'tl.to(".piston", {y:46, duration:0.6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.5);'
    'tl.fromTo(".wl5", {opacity:0}, {opacity:1, duration:0.5}, 0.4);'
    'tl.fromTo(".up", {opacity:0}, {opacity:1, duration:0.4}, 0.6);'
    'tl.to(".up", {strokeDashoffset:-64, duration:1.1, repeat:-1, ease:"none"}, 0.7);'
    'tl.fromTo(".lb5", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);',
    'tl.to(".piston", {y:52, duration:0.6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.3);'
    'tl.fromTo(".stream", {opacity:0}, {opacity:1, duration:0.8}, 0.4);'
    'tl.to(".stream2", {opacity:0.25, duration:0.6, yoyo:true, repeat:-1}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".bo7", {opacity:0, scale:0.94}, {opacity:1, scale:1, duration:0.5}, 0.1);'
    'tl.to(".st7", {y:-20, opacity:0.45, duration:1.2, yoyo:true, repeat:-1}, 0.5);'
    'tl.to(".ht0, .ht1, .ht2, .ht3", {y:-26, opacity:0.2, duration:1.2, stagger:0.15, repeat:-1, ease:"sine.out"}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".cloud", {opacity:0, x:60}, {opacity:1, x:0, duration:0.8}, 0.4);'
    'tl.to(".cloud", {x:-30, duration:3, ease:"sine.inOut"}, 1.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".dsh9", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".bo9", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.to(".piston", {y:44, duration:0.6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.5);'
    'tl.fromTo(".wl9", {opacity:0}, {opacity:1, duration:0.5}, 0.6);'
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
