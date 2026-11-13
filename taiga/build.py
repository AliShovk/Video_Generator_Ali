#!/usr/bin/env python3
"""«Тайга» — ремейк: тёмная инфографика, жёлтые акценты, крупные титры."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/taiga")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]

BG = "#07090a"
BG2 = "#101314"
YEL = "#f5c542"
AMB = "#e8a72c"
WHITE = "#f2f4f5"
GREY = "#8b969b"
DIM = "#4b5559"
BLUE = "#5d8fb5"


def t(x, y, s, size=40, col=WHITE, anchor="start", w=900, ls=0, cls="hl", op=1.0):
    return (f'<text class="{cls}" x="{x}" y="{y}" opacity="{op}" font-family="Nunito, Arial" font-size="{size}" '
            f'font-weight="{w}" fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def bg(seed=1):
    r = random.Random(seed)
    dots = "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.8):.1f}" '
                   f'fill="#ffffff" opacity="{r.uniform(0.03,0.12):.2f}"/>' for _ in range(150))
    return (f'<defs><radialGradient id="gl{seed}" cx="50%" cy="42%" r="60%">'
            f'<stop offset="0" stop-color="#3a2f18" stop-opacity="0.55"/>'
            f'<stop offset="0.5" stop-color="#151310" stop-opacity="0.5"/>'
            f'<stop offset="1" stop-color="#000000" stop-opacity="0.85"/></radialGradient>'
            f'<radialGradient id="vi{seed}" cx="50%" cy="45%" r="72%">'
            f'<stop offset="0.5" stop-color="#000" stop-opacity="0"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0.8"/></radialGradient></defs>'
            f'<rect width="1080" height="1920" fill="{BG}"/>'
            f'<rect width="1080" height="1920" fill="url(#gl{seed})"/>'
            f'{dots}<rect width="1080" height="1920" fill="url(#vi{seed})"/>')


def label(x, y, text, col=AMB, w=None, size=19, cls="lb"):
    ww = w or (len(text) * size * 0.62 + 34)
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{ww:.0f}" height="{size*1.9:.0f}" rx="6" fill="#0c0f10" opacity="0.9"/>'
            f'<rect x="{x}" y="{y}" width="{ww:.0f}" height="{size*1.9:.0f}" rx="6" fill="none" stroke="{col}" stroke-width="1.6" opacity="0.9"/>'
            f'<text x="{x+ww/2:.0f}" y="{y+size*1.32:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{col}" '
            f'text-anchor="middle" letter-spacing="1">{text}</text></g>')


def circles(cx, cy, radii, col=AMB, cls="cir"):
    out = [f'<g class="{cls}">']
    for i, r in enumerate(radii):
        out.append(f'<circle class="c{i}" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="2.2" '
                   f'stroke-dasharray="12 14" opacity="0.55"/>')
    out.append('</g>')
    return "".join(out)


def dotted(pts, col=YEL, w=6, cls="dp"):
    d = f"M {pts[0][0]} {pts[0][1]} " + " ".join(f"L {x} {y}" for x, y in pts[1:])
    return (f'<g class="{cls}"><path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" '
            f'stroke-dasharray="3 20" opacity="0.9"/>'
            f'<path d="{d}" stroke="{col}" stroke-width="{w*3}" fill="none" stroke-linecap="round" opacity="0.10"/></g>')


def caption(parts, y=1500, size=78, cls="cap"):
    """parts: [(text, color)] — по строке на элемент, крупно, по центру."""
    out = [f'<g class="{cls}">']
    yy = y
    for txt, col in parts:
        out.append(f'<text class="cl" x="540" y="{yy}" font-family="Nunito" font-size="{size}" font-weight="900" '
                   f'fill="{col}" text-anchor="middle" letter-spacing="-1">{txt}</text>')
        yy += int(size * 1.08)
    out.append('</g>')
    return "".join(out)


def train(x, y, s=1.0, cls="tr", windows=6, lit=True):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="{520*s}" height="{150*s}" rx="{16*s}" fill="#1a1f22" stroke="#333b3f" stroke-width="{2*s}"/>')
    b.append(f'<rect x="{x+8*s}" y="{y-18*s}" width="{470*s}" height="{22*s}" rx="{9*s}" fill="#232a2e"/>')
    for i in range(windows):
        wx = x + (34 + i * 78) * s
        b.append(f'<rect x="{wx}" y="{y+34*s}" width="{52*s}" height="{44*s}" rx="{5*s}" fill="{YEL if lit else "#2a3236"}" opacity="0.85"/>')
    b.append(f'<circle cx="{x+70*s}" cy="{y+150*s}" r="{26*s}" fill="#101416" stroke="#333b3f" stroke-width="{2*s}"/>')
    b.append(f'<circle cx="{x+440*s}" cy="{y+150*s}" r="{26*s}" fill="#101416" stroke="#333b3f" stroke-width="{2*s}"/>')
    b.append('</g>')
    return "".join(b)


def wagon_top(x, y, w, h, col="#1b2225", hot=False, cls="wt"):
    c = AMB if hot else "#2b3438"
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" stroke="{c}" stroke-width="2"/>'
            f'<rect x="{x+12}" y="{y+12}" width="{w-24}" height="{h-24}" rx="8" fill="none" stroke="{c}" stroke-width="1" opacity="0.4"/></g>')


def gauge(y=1700, pct=0.15, left="ВНУТРИ ВАГОНА 7", right="+8°C", col=YEL):
    return (f'<g class="gauge">'
            f'<text x="60" y="{y-14}" font-family="Nunito" font-size="20" font-weight="800" fill="{GREY}" letter-spacing="2">{left}</text>'
            f'<text x="1020" y="{y-14}" font-family="Nunito" font-size="30" font-weight="900" fill="{col}" text-anchor="end">{right}</text>'
            f'<rect x="60" y="{y}" width="960" height="16" rx="8" fill="#1b2225"/>'
            f'<rect class="gfill" x="60" y="{y}" width="{960*pct:.0f}" height="16" rx="8" fill="{col}"/>'
            f'<rect x="60" y="{y}" width="960" height="16" rx="8" fill="none" stroke="#39434700" stroke-width="1"/></g>')


def tree(x, y, s=1.0, col="#0e1416", cls="tr"):
    """Ёлка треугольниками."""
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x-7*s}" y="{y-40*s}" width="{14*s}" height="{40*s}" fill="#0a0f10"/>')
    for i, (ww, hh) in enumerate(((70, 130), (58, 115), (44, 95))):
        yy = y - 40 * s - i * 74 * s
        b.append(f'<path d="M {x-ww*s} {yy} L {x} {yy-hh*s} L {x+ww*s} {yy} Z" fill="{col}"/>')
    b.append('</g>')
    return "".join(b)


def figure(x, y, s=1.0, col="#0b0e0f", cls="fg", glow=False):
    b = [f'<g class="{cls}">']
    if glow:
        b.append(f'<circle cx="{x}" cy="{y-150*s}" r="{120*s}" fill="{YEL}" opacity="0.05"/>')
    b.append(f'<circle cx="{x}" cy="{y-150*s}" r="{26*s}" fill="{col}"/>')
    b.append(f'<path d="M {x-34*s} {y-118*s} q {34*s} {-24*s} {68*s} 0 l {10*s} {128*s} l {-88*s} 0 z" fill="{col}"/>')
    b.append('</g>')
    return "".join(b)


# ------------------------------------------------------------------ сцены
def s_hook():
    b = [bg(1)]
    b.append(tree(140, 1250, 1.6, "#0c1214", "tr1"))
    b.append(tree(250, 1330, 1.2, "#0a0f11", "tr2"))
    b.append(tree(940, 1200, 1.7, "#0c1214", "tr3"))
    b.append(tree(860, 1360, 1.1, "#0a0f11", "tr4"))
    b.append(train(120, 1000, 1.25, "trn1", 6))
    b.append(f'<circle cx="540" cy="700" r="380" fill="{AMB}" opacity="0.05"/>')
    b.append(label(700, 760, "НОЧЬ 1 // 02:14 · ТАЙГА", AMB, 300, 18))
    b.append(caption([("НЕ ВЫХОДИ", WHITE), ("ИЗ ВАГОНА", GREY)], 1480, 92))
    return b


def s_map():
    b = [bg(2)]
    b.append(circles(540, 900, [300, 150], AMB, "cir2"))
    b.append(label(760, 700, "50 КМ", AMB, 150, 20))
    b.append(label(660, 780, "10 КМ", AMB, 140, 18))
    b.append(f'<circle cx="540" cy="900" r="10" fill="{YEL}"/>')
    b.append(f'<circle cx="540" cy="900" r="26" fill="{YEL}" opacity="0.15"/>')
    b.append(caption([("ВЫ СИДИТЕ", WHITE), ("ЗДЕСЬ", GREY)], 1500, 86))
    return b


def s_error():
    b = [bg(3)]
    b.append(train(120, 900, 1.25, "trn3", 0))
    b.append(f'<path d="M 620 700 l 90 90 M 710 700 l -90 90" stroke="#c0392b" stroke-width="12" stroke-linecap="round"/>')
    b.append(label(620, 830, "СЕТЬ ОБЕСТОЧЕНА", "#c0392b", 300, 20))
    b.append(caption([("ФАТАЛЬНАЯ", WHITE), ("ОШИБКА", "#c0392b")], 1480, 84))
    return b


def s_path():
    b = [bg(4)]
    b.append(dotted([(800, 520), (740, 640), (700, 700), (760, 820), (700, 900), (740, 1030), (620, 1120), (560, 1180)], YEL, 7, "dp4"))
    b.append(f'<circle cx="800" cy="520" r="18" fill="{YEL}"/>')
    b.append(label(830, 560, "ПОЕЗД", AMB, 150, 18))
    b.append(label(300, 1180, "СТАНЦИЯ", BLUE, 170, 18))
    b.append(label(760, 860, "40 КМ", AMB, 150, 22))
    b.append(label(760, 940, "ПЕШКОМ 10 Ч", AMB, 250, 20))
    b.append(caption([("ДО СТАНЦИИ", WHITE), ("10 ЧАСОВ", GREY)], 1520, 80))
    return b


def s_cold():
    b = [bg(5)]
    b.append(f'<rect x="470" y="600" width="140" height="620" rx="70" fill="#12181a" stroke="#2c3639" stroke-width="3"/>')
    b.append(f'<rect class="merc" x="492" y="700" width="96" height="500" rx="48" fill="{BLUE}" opacity="0.8"/>')
    for i in range(6):
        b.append(f'<path d="M 630 {680+i*90} l 40 0" stroke="{DIM}" stroke-width="2"/>')
        b.append(t(690, 690 + i * 90, f"{i*10}", 24, GREY))
    b.append(label(220, 760, "2 ЧАСА", "#c0392b", 190, 24))
    b.append(caption([("ПЕРЕОХЛАЖДЕНИЕ", WHITE), ("ЧЕРЕЗ 2 ЧАСА", "#c0392b")], 1500, 64))
    return b


def s_boiler():
    b = [bg(6)]
    b.append(f'<rect x="120" y="760" width="840" height="460" rx="16" fill="#0d1113" stroke="#2a3337" stroke-width="3"/>')
    b.append(f'<rect x="200" y="860" width="240" height="260" rx="12" fill="#151b1d" stroke="{AMB}" stroke-width="2"/>')
    b.append(f'<path class="fire" d="M 250 1110 q 30 -90 70 -60 q 40 -70 70 -20 q 30 60 0 80 z" fill="{AMB}" opacity="0.9"/>')
    b.append(label(250, 800, "КОТЁЛ", AMB, 150, 22))
    b.append(f'<rect x="520" y="900" width="360" height="180" rx="10" fill="none" stroke="{DIM}" stroke-width="2" stroke-dasharray="10 8"/>')
    b.append(t(700, 1010, "НЕ НУЖНО ЭЛЕКТРИЧЕСТВО", 24, GREY, "middle", 800))
    b.append(caption([("КОТЁЛ", WHITE), ("УГОЛЬНЫЙ", GREY)], 1520, 82))
    return b


def s_coal():
    b = [bg(7)]
    b.append(wagon_top(140, 700, 800, 420, "#1b2225", False, "wt7"))
    b.append(f'<rect x="240" y="1140" width="600" height="180" rx="10" fill="#151b1d" stroke="{AMB}" stroke-width="2"/>')
    for i in range(9):
        b.append(f'<circle cx="{280+i*66}" cy="{1200+(i%2)*40}" r="22" fill="#2a2320" stroke="#3a322c" stroke-width="2"/>')
    b.append(label(300, 1370, "УГОЛЬ · 3 СУТОК", AMB, 320, 22))
    b.append(caption([("УГЛЯ", WHITE), ("НА 3 СУТОК", GREY)], 1540, 78))
    return b


def s_water():
    b = [bg(8)]
    b.append(f'<path d="M 120 800 L 960 800" stroke="{DIM}" stroke-width="26" stroke-linecap="round"/>')
    b.append(f'<path d="M 120 800 L 960 800" stroke="{BLUE}" stroke-width="10" stroke-linecap="round" opacity="0.35"/>')
    for i in range(4):
        b.append(f'<circle class="dr{i}" cx="{300+i*180}" cy="800" r="16" fill="{BLUE}" opacity="0.7"/>')
    b.append(label(620, 700, "3 ЧАСА", "#c0392b", 190, 24))
    b.append(caption([("ТРУБЫ ЗАМЁРЗНУТ", WHITE), ("ЧЕРЕЗ 3 ЧАСА", GREY)], 1480, 60))
    return b


def s_bottles():
    b = [bg(9)]
    for i in range(7):
        x = 170 + i * 110
        b.append(f'<rect x="{x}" y="{880 - i*18}" width="72" height="200" rx="14" fill="#182022" stroke="{AMB}" stroke-width="2"/>')
        b.append(f'<rect x="{x+8}" y="{960 - i*18}" width="56" height="112" rx="10" fill="{YEL}" opacity="0.75"/>')
        b.append(f'<rect x="{x+26}" y="{846 - i*18}" width="20" height="40" rx="5" fill="{DIM}"/>')
    b.append(label(660, 760, "КИПЯТОК", AMB, 200, 22))
    b.append(caption([("ВО ВСЕ БУТЫЛКИ", WHITE), ("И СЛИТЬ СИСТЕМУ", GREY)], 1480, 62))
    return b


def s_people():
    b = [bg(10)]
    for i in range(9):
        for j in range(4):
            x, y = 240 + i * 70, 800 + j * 90
            b.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{YEL}" opacity="{0.35 + 0.06*(i%3)}"/>')
            b.append(f'<circle cx="{x}" cy="{y}" r="40" fill="{YEL}" opacity="0.04"/>')
    b.append(label(700, 660, "100 ВТ · КАЖДЫЙ", AMB, 300, 22))
    b.append(caption([("ЛЮДИ —", WHITE), ("ЭТО ПЕЧКИ", GREY)], 1520, 84))
    return b


def s_gather():
    b = [bg(11)]
    for i in range(6):
        b.append(wagon_top(90 + i * 155, 760, 130, 260, "#1b2225", i == 3, f"w{i}"))
    for i in range(6):
        if i != 3:
            b.append(f'<path class="ar{i}" d="M {155 + i*155} 700 q 0 -90 {(3-i)*60} -130" stroke="{YEL}" stroke-width="4" fill="none" opacity="0.75"/>')
    b.append(label(400, 1120, "ВСЕ В ОДИН ВАГОН", AMB, 420, 22))
    b.append(caption([("СОБИРАЮТ", WHITE), ("В ОДИН ВАГОН", GREY)], 1500, 78))
    return b


def s_blanket():
    b = [bg(12)]
    b.append(f'<rect x="300" y="760" width="480" height="520" rx="14" fill="#0d1113" stroke="#2a3337" stroke-width="3"/>')
    b.append(f'<path d="M 330 800 q 210 -40 420 0 l 0 440 q -210 40 -420 0 z" fill="#1d2427" stroke="#39434700" stroke-width="2"/>')
    for i in range(5):
        b.append(f'<path d="M 350 {860+i*80} q 200 30 380 0" stroke="{DIM}" stroke-width="3" opacity="0.6"/>')
    b.append(label(820, 820, "ОДЕЯЛА", AMB, 190, 22))
    b.append(caption([("ТАМБУР", WHITE), ("ОДЕЯЛАМИ", GREY)], 1520, 80))
    return b


def s_list():
    b = [bg(13)]
    for i in range(12):
        col = 0 if i < 6 else 1
        x = 120 + col * 420
        y = 620 + (i % 6) * 92
        b.append(f'<rect x="{x}" y="{y}" width="360" height="70" rx="8" fill="#121719" stroke="#2a3337" stroke-width="1.5"/>')
        b.append(f'<rect x="{x+300}" y="{y}" width="60" height="70" rx="8" fill="#0c1011"/>')
        b.append(t(x + 20, y + 46, str(i + 1), 28, GREY))
    b.append(t(120, 1330, "192", 64, WHITE))
    b.append(t(260, 1330, "по билетам", 26, GREY))
    b.append(t(120, 1420, "191", 64, YEL))
    b.append(t(260, 1420, "в вагоне", 26, GREY))
    b.append(caption([("ОДНОГО НЕТ", WHITE)], 1540, 76))
    return b


def s_night():
    b = [bg(14)]
    b.append(train(90, 1120, 1.3, "trn14", 6))
    b.append(f'<circle cx="640" cy="1080" r="26" fill="{YEL}" opacity="0.9"/>')
    b.append(f'<circle cx="640" cy="1080" r="70" fill="{YEL}" opacity="0.10"/>')
    b.append(f'<path class="smoke" d="M 900 1080 q 40 -90 10 -170 q -30 -80 20 -150" stroke="{GREY}" stroke-width="12" fill="none" opacity="0.35"/>')
    b.append(label(760, 820, "ДЫМ", "#c0392b", 140, 22))
    b.append(caption([("НОЧЬЮ", WHITE), ("В ТАМБУР", GREY)], 1500, 82))
    return b


def s_window():
    b = [bg(15)]
    b.append(f'<rect x="180" y="620" width="720" height="620" rx="12" fill="#0b1011" stroke="#2a3337" stroke-width="4"/>')
    b.append(f'<rect x="220" y="660" width="640" height="540" rx="8" fill="#101a1d"/>')
    b.append(f'<g class="fig15">{figure(540, 1180, 1.15, "#05080a", "fg15", True)}</g>')
    b.append(f'<path d="M 220 1200 q 320 -40 640 0" stroke="{DIM}" stroke-width="3" opacity="0.6"/>')
    b.append(label(700, 560, "15-Й ВАГОН", AMB, 240, 20))
    b.append(caption([("ОН СМОТРИТ", WHITE), ("ПРЯМО НА ТЕБЯ", GREY)], 1500, 72))
    return b


def s_end():
    b = [bg(16)]
    b.append(f'<circle cx="540" cy="820" r="360" fill="{AMB}" opacity="0.06"/>')
    b.append(caption([("ОН ЗНАЕТ", WHITE), ("О НАС", GREY)], 860, 94))
    b.append(t(540, 1160, "ПРОДОЛЖЕНИЕ СЛЕДУЕТ", 34, AMB, "middle", 800, ls=3))
    return b


SCENES = [
    (s_hook, (0, 0)),
    (s_map, (1, 1)),
    (s_error, (2, 3)),
    (s_path, (4, 5)),
    (s_cold, (6, 6)),
    (s_boiler, (7, 8)),
    (s_coal, (9, 9)),
    (s_water, (10, 10)),
    (s_bottles, (11, 11)),
    (s_people, (12, 12)),
    (s_gather, (13, 13)),
    (s_blanket, (14, 14)),
    (s_list, (15, 17)),
    (s_night, (18, 20)),
    (s_window, (21, 24)),
    (s_end, (25, 28)),
]

ANIM = [
    'tl.fromTo(".trn1", {opacity:0, y:20}, {opacity:1, y:0, duration:1.0}, 0.2);'
    'tl.fromTo(".tr1, .tr2, .tr3, .tr4", {opacity:0}, {opacity:1, duration:1.0, stagger:0.12}, 0);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.6);',
    'tl.fromTo(".c0", {opacity:0, scale:0.9, transformOrigin:"540px 900px"}, {opacity:0.55, scale:1, duration:0.9}, 0.2);'
    'tl.fromTo(".c1", {opacity:0}, {opacity:0.55, duration:0.6}, 0.6);'
    'tl.to(".cir", {rotate:6, transformOrigin:"540px 900px", duration:6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5, stagger:0.2}, 0.8);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.6);',
    'tl.fromTo(".trn3", {opacity:0}, {opacity:1, duration:0.7}, 0.1);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.6);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".dp4", {opacity:0}, {opacity:1, duration:0.6}, 0.2);'
    'tl.to(".dp4", {strokeDashoffset:-120, duration:2.4, repeat:-1, ease:"none"}, 0.4);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.4, stagger:0.2}, 0.6);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".merc", {opacity:0, y:-120}, {opacity:0.8, y:0, duration:1.2, ease:"power2.out"}, 0.2);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.6);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.to(".fire", {scaleY:1.15, transformOrigin:"340px 1110px", duration:0.5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.4);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".wt7", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.6);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".dr0, .dr1, .dr2, .dr3", {opacity:0, y:-20}, {opacity:0.7, y:0, duration:0.6, stagger:0.15}, 0.3);'
    'tl.to(".dr0, .dr1, .dr2, .dr3", {y:60, opacity:0, duration:1.4, stagger:0.2, repeat:-1}, 0.9);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.6);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo("[class^=w]", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.1}, 0.2);'
    'tl.fromTo("[class^=ar]", {opacity:0}, {opacity:0.75, duration:0.5, stagger:0.1}, 0.6);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.3);',
    'tl.fromTo(".trn14", {opacity:0}, {opacity:1, duration:0.7}, 0.1);'
    'tl.to(".smoke", {y:-40, opacity:0.15, duration:2.2, repeat:-1, ease:"sine.out"}, 0.4);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.6);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.4);',
    'tl.fromTo(".fig15", {opacity:0, scale:0.9, transformOrigin:"540px 1100px"}, {opacity:1, scale:1, duration:1.2}, 0.4);'
    'tl.fromTo(".lb", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.fromTo(".cl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 0.6);',
    'tl.fromTo(".cl", {opacity:0, y:20}, {opacity:1, y:0, duration:0.8, stagger:0.25}, 0.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.6}, 1.0);',
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
    {anim}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, (fn, (a, z)) in enumerate(SCENES):
        sid = f"s{i+1}"
        st = STARTS[a] - 0.2
        end = STARTS[z + 1] if z + 1 < len(STARTS) else TOTAL
        dur = round(end - st, 3)
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
    print("ok", TOTAL)


if __name__ == "__main__":
    build()
