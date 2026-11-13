#!/usr/bin/env python3
"""«Бушменская дыра» — разрез породы, водолазы уходят вниз."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/bluehole")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

DEEP = "#030d12"
GLOW = "#9fe8dd"
TORCH = "#ffe6a8"
MUTED = "#8aa9b3"
RED = "#d9524a"
STONE = ["#242c31", "#1b2227", "#2d363b", "#161d21", "#313b40"]
SOIL = "#2a2119"
GRASS = "#2b3a2b"


def t(x, y, s, size=46, col=GLOW, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}" stroke="#020a0e" stroke-width="9" '
            f'paint-order="stroke" stroke-linejoin="round">{s}</text>')


def rock(pts, gid, seed=1, top_soil=False, dark=0.0):
    """Скальный массив: градиент, слоистые пятна, трещины, кромка."""
    d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts) + " Z"
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    bx, by, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    r = random.Random(seed)
    cid, gidr = f"c_{gid}", f"rg_{gid}"
    spots = []
    for _ in range(85):
        cx = r.uniform(bx, bx + bw); cy = r.uniform(by, by + bh)
        w = r.uniform(40, 150); h = r.uniform(20, 70)
        col = STONE[r.randrange(len(STONE))]
        spots.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{w:.0f}" ry="{h:.0f}" fill="{col}" '
                     f'opacity="{r.uniform(0.25,0.6):.2f}" transform="rotate({r.uniform(-25,25):.0f} {cx:.0f} {cy:.0f})"/>')
    cracks = []
    for _ in range(9):
        x0 = r.uniform(bx, bx + bw); y0 = r.uniform(by, by + bh)
        seg = [f"M {x0:.0f} {y0:.0f}"]
        for k in range(4):
            x0 += r.uniform(-70, 70); y0 += r.uniform(30, 90)
            seg.append(f"L {x0:.0f} {y0:.0f}")
        cracks.append(f'<path d="{" ".join(seg)}" stroke="#0b1013" stroke-width="{r.uniform(1.5,3.5):.1f}" fill="none" opacity="0.55"/>')
    soil = ""
    if top_soil:
        soil = (f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="18" fill="{GRASS}"/>'
                f'<rect x="{bx:.0f}" y="{by+18:.0f}" width="{bw:.0f}" height="26" fill="{SOIL}"/>')
    return (f'<defs><clipPath id="{cid}"><path d="{d}"/></clipPath>'
            f'<linearGradient id="{gidr}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#39454b"/><stop offset="0.5" stop-color="#232b31"/>'
            f'<stop offset="1" stop-color="#131a1f"/></linearGradient></defs>'
            f'<path d="{d}" fill="url(#{gidr})"/>'
            f'<g clip-path="url(#{cid})">{soil}{"".join(spots)}{"".join(cracks)}</g>'
            f'<path d="{d}" fill="none" stroke="#5d7b85" stroke-width="2.5" opacity="0.75"/>')


def void(pts, gid):
    """Полость с водой: тёмный проход с подсветкой у входа."""
    d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in pts) + " Z"
    return (f'<defs><linearGradient id="vg_{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#1d6d78"/><stop offset="0.35" stop-color="#0b3a45"/>'
            f'<stop offset="1" stop-color="#03151b"/></linearGradient></defs>'
            f'<path d="{d}" fill="url(#vg_{gid})" stroke="#7fb0ba" stroke-width="1.5" opacity="0.95"/>')


def diver(x, y, s=1.0, col="#0a1a20", cls="dv", flip=False):
    """Водолаз в горизонтальном положении: корпус, голова, руки вперёд, ласты."""
    g = [f'<g class="{cls}">']
    # корпус
    g.append(f'<path d="M {x-46*s} {y-18*s} q {44*s} {-14*s} {88*s} {4*s} q {12*s} {10*s} {-2*s} {22*s} '
             f'q {-44*s} {10*s} {-86*s} {-2*s} q {-10*s} {-8*s} 0*s {-24*s} z" fill="{col}"/>')
    # голова
    g.append(f'<circle cx="{x+50*s}" cy="{y-8*s}" r="{14*s}" fill="{col}"/>')
    g.append(f'<rect x="{x+44*s}" y="{y-14*s}" width="{16*s}" height="{8*s}" rx="{4*s}" fill="{TORCH}" opacity="0.9"/>')
    # баллон
    g.append(f'<rect x="{x-34*s}" y="{y-32*s}" width="{56*s}" height="{13*s}" rx="{6*s}" fill="#173741"/>')
    # рука вперёд
    g.append(f'<path d="M {x+18*s} {y-4*s} l {26*s} {6*s}" stroke="{col}" stroke-width="{9*s}" stroke-linecap="round"/>')
    # ноги
    g.append(f'<path d="M {x-46*s} {y-6*s} l {-26*s} {-12*s}" stroke="{col}" stroke-width="{10*s}" stroke-linecap="round"/>')
    g.append(f'<path d="M {x-46*s} {y+8*s} l {-26*s} {12*s}" stroke="{col}" stroke-width="{10*s}" stroke-linecap="round"/>')
    # ласты
    g.append(f'<path d="M {x-72*s} {y-18*s} l {-26*s} {-10*s} l {-2*s} {12*s} l {22*s} {10*s} z" fill="{col}"/>')
    g.append(f'<path d="M {x-72*s} {y+20*s} l {-26*s} {10*s} l {-2*s} {-12*s} l {22*s} {-10*s} z" fill="{col}"/>')
    # фонарь
    g.append(f'<rect x="{x+64*s}" y="{y-10*s}" width="{16*s}" height="{9*s}" rx="{4*s}" fill="{TORCH}"/>')
    g.append('</g>')
    return "".join(g)


def beam(x, y, ang, cls="bm", length=420, spread=7, col=TORCH, op=0.12):
    out = [f'<g class="{cls}">']
    for sp, o in ((spread, op), (spread*0.6, op*1.6), (spread*0.3, op*2.3)):
        a0 = math.radians(ang - sp); a1 = math.radians(ang + sp)
        out.append(f'<path d="M {x} {y} L {x+length*math.cos(a0):.0f} {y+length*math.sin(a0):.0f} '
                   f'L {x+length*math.cos(a1):.0f} {y+length*math.sin(a1):.0f} Z" fill="{col}" opacity="{o:.3f}"/>')
    out.append(f'<circle cx="{x}" cy="{y}" r="18" fill="{col}" opacity="0.22"/>')
    out.append('</g>')
    return "".join(out)


def hud(x, y, date="1 СЕНТЯБРЯ 1991", time="15:19", depth="34 М", cls="hud"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="286" height="186" rx="4" fill="#000" opacity="0.62"/>'
            f'<text x="{x+18}" y="{y+28}" font-family="Nunito" font-size="13" font-weight="800" fill="#d9c46a" letter-spacing="2">ДАТА</text>'
            f'<text x="{x+18}" y="{y+62}" font-family="Nunito" font-size="27" font-weight="900" fill="#fff">{date}</text>'
            f'<text x="{x+18}" y="{y+96}" font-family="Nunito" font-size="13" font-weight="800" fill="#d9c46a" letter-spacing="2">ВРЕМЯ</text>'
            f'<text x="{x+18}" y="{y+130}" font-family="Nunito" font-size="27" font-weight="900" fill="#fff">{time}</text>'
            f'<text x="{x+18}" y="{y+162}" font-family="Nunito" font-size="13" font-weight="800" fill="#d9c46a" letter-spacing="2">ГЛУБИНА</text>'
            f'<text x="{x+108}" y="{y+164}" font-family="Nunito" font-size="27" font-weight="900" fill="#fff">{depth}</text></g>')


def chip(x, y, label, cls="chip", w=190):
    return (f'<g class="{cls}"><text x="{x}" y="{y}" font-family="Nunito" font-size="26" font-weight="900" fill="#f2f6f7">{label}</text>'
            f'<path d="M {x+92} {y-9} l {w} 0" stroke="#f2f6f7" stroke-width="2.5" opacity="0.85"/></g>')


def sky_band(h=210):
    return (f'<rect x="0" y="0" width="1080" height="{h}" fill="#0a1820"/>'
            f'<ellipse cx="820" cy="120" rx="260" ry="90" fill="#123039" opacity="0.7"/>')


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', sky_band(230)]
    # левая и правая порода, между ними шахта
    b.append(rock([(0, 230), (300, 230), (330, 560), (300, 980), (250, 1420), (270, 1920), (0, 1920)], "k1a", 1, True))
    b.append(rock([(1080, 230), (760, 230), (730, 600), (780, 1040), (820, 1480), (800, 1920), (1080, 1920)], "k1b", 2, True))
    b.append(void([(300, 230), (760, 230), (730, 600), (780, 1040), (820, 1480), (800, 1920), (270, 1920),
                   (250, 1420), (300, 980), (330, 560)], "v1"))
    # трос от входа
    b.append(f'<path class="rope" d="M 540 250 q -30 300 10 560 q 40 300 -20 700" stroke="#cfe6e2" stroke-width="2" fill="none" opacity="0.55"/>')
    b.append(diver(470, 640, 1.15, "#0a1a20", "dv1"))
    b.append(beam(540, 632, 68, "bm1", 520, 8, TORCH, 0.13))
    b.append(diver(610, 900, 0.9, "#0a1a20", "dv1b"))
    b.append(beam(668, 894, 74, "bm1b", 380, 8, TORCH, 0.10))
    b.append(chip(120, 1180, "37 м"))
    b.append(hud(60, 300, "1 СЕНТЯБРЯ 1991", "15:19", "34 М"))
    b.append(t(60, 1760, "СВОЯ ВЕРЁВКА — ОТ ВХОДА", 24, "#f0e2a0", w=800))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', sky_band(120)]
    b.append(rock([(0, 120), (250, 120), (270, 620), (240, 1240), (280, 1920), (0, 1920)], "k2a", 3, True))
    b.append(rock([(1080, 120), (830, 120), (810, 640), (850, 1260), (800, 1920), (1080, 1920)], "k2b", 4, True))
    b.append(void([(250, 120), (830, 120), (810, 640), (850, 1260), (800, 1920), (280, 1920), (240, 1240), (270, 620)], "v2"))
    for lbl, yy in (("0 м", 300), ("50", 560), ("100", 760), ("200", 1080), ("283 м", 1500)):
        b.append(chip(760, yy, lbl, f"ch2{lbl}", 150))
    b.append(diver(520, 520, 0.55, "#0a1a20", "m0"))
    b.append(diver(560, 900, 0.5, "#0a1a20", "m1"))
    b.append(diver(520, 1320, 0.48, "#0a1a20", "m2"))
    b.append(t(60, 70, "РАЗРЕЗ ПЕЩЕРЫ · 283 М", 30, GLOW, ls=1))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', sky_band(120)]
    b.append(rock([(0, 120), (210, 120), (230, 900), (200, 1920), (0, 1920)], "k3a", 5, True))
    b.append(rock([(1080, 120), (870, 120), (850, 920), (890, 1920), (1080, 1920)], "k3b", 6, True))
    b.append(void([(210, 120), (870, 120), (850, 920), (890, 1920), (200, 1920), (230, 900)], "v3"))
    b.append(f'<rect x="420" y="700" width="190" height="820" fill="#1b3038" stroke="{GLOW}" stroke-width="2.5" opacity="0.9"/>')
    for i in range(20):
        b.append(f'<rect x="442" y="{730+i*38}" width="26" height="18" fill="{TORCH}" opacity="0.45"/>')
        b.append(f'<rect x="562" y="{730+i*38}" width="26" height="18" fill="{TORCH}" opacity="0.45"/>')
    b.append(t(630, 760, "100 этажей", 22, MUTED))
    b.append(t(60, 70, "ГЛУБЖЕ ВЫСОТКИ", 30, GLOW, ls=1))
    b.append(t(60, 1800, "283 м ≈ 100 этажей", 24, TORCH, w=800))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', sky_band(150)]
    b.append(rock([(0, 150), (240, 150), (260, 760), (220, 1920), (0, 1920)], "k4a", 7, True))
    b.append(rock([(1080, 150), (840, 150), (820, 780), (860, 1920), (1080, 1920)], "k4b", 8, True))
    b.append(void([(240, 150), (840, 150), (820, 780), (860, 1920), (220, 1920), (260, 760)], "v4"))
    b.append(diver(470, 800, 1.0, "#0a1a20", "dv4"))
    b.append(beam(540, 792, 72, "bm4", 440, 8, TORCH, 0.12))
    b.append(chip(120, 980, "40 м"))
    b.append(hud(60, 230, "1994", "12:40", "40 М"))
    b.append(t(60, 1700, "ДЕОН ДРЕЙЕР · 20 ЛЕТ", 24, "#f0e2a0", w=800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(rock([(0, 0), (300, 0), (330, 620), (280, 1300), (320, 1920), (0, 1920)], "k5a", 9))
    b.append(rock([(1080, 0), (720, 0), (700, 660), (760, 1320), (720, 1920), (1080, 1920)], "k5b", 10))
    b.append(void([(300, 0), (720, 0), (700, 660), (760, 1320), (720, 1920), (320, 1920), (280, 1300), (330, 620)], "v5"))
    b.append(diver(480, 780, 0.85, "#0a1a20", "dv5"))
    b.append(beam(540, 774, 86, "bm5", 360, 8, TORCH, 0.11))
    b.append(chip(120, 700, "50 м"))
    b.append(hud(60, 200, "1994", "13:02", "50 М"))
    b.append(t(60, 1720, "ВСПЛЫВАЛ — И НЕ ДОБРАЛСЯ", 22, GLOW, w=800))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(rock([(0, 0), (200, 0), (220, 700), (180, 1920), (0, 1920)], "k6a", 11))
    b.append(rock([(1080, 0), (880, 0), (900, 720), (860, 1920), (1080, 1920)], "k6b", 12))
    b.append(void([(200, 0), (880, 0), (900, 720), (860, 1920), (180, 1920), (220, 700)], "v6"))
    # дно камеры
    b.append(f'<path d="M 180 1560 q 360 -40 700 0 l 0 360 l -700 0 z" fill="#0a2028" stroke="#5d7b85" stroke-width="2" opacity="0.95"/>')
    b.append(f'<rect x="330" y="1470" width="180" height="46" rx="23" fill="#8ba3ad" opacity="0.9"/>')
    b.append(f'<circle cx="520" cy="1492" r="25" fill="#a3bac4" opacity="0.95"/>')
    b.append(f'<path d="M 330 1492 l -46 -22 l 0 44 z" fill="#75919c"/>')
    b.append(f'<circle cx="470" cy="1470" r="46" fill="{TORCH}" opacity="0.10"/>')
    b.append(chip(760, 1380, "270 м"))
    b.append(t(60, 180, "ТЕЛО НА ГЛУБИНЕ 270 М", 30, GLOW, ls=1))
    b.append(t(60, 1720, "десять лет никто не мог его достать", 22, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    for i in range(6):
        b.append(f'<circle cx="540" cy="960" r="{160+i*110}" fill="none" stroke="{MUTED}" stroke-width="1.5" opacity="{0.28-i*0.04:.2f}"/>')
    b.append(t(540, 900, "10", 240, TORCH, "middle", 900))
    b.append(t(540, 1000, "ЛЕТ", 72, GLOW, "middle", 900, ls=6))
    b.append(t(540, 1120, "никто не мог его достать", 30, MUTED, "middle", 700))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="#010609"/>']
    b.append(rock([(0, 0), (300, 0), (280, 1920), (0, 1920)], "k8a", 13))
    b.append(rock([(1080, 0), (800, 0), (820, 1920), (1080, 1920)], "k8b", 14))
    b.append(t(540, 860, "ГЛУБИНА", 64, GLOW, "middle", 900, ls=4))
    b.append(t(540, 940, "НЕ ПРОЩАЕТ", 64, RED, "middle", 900, ls=2))
    b.append(t(540, 1030, "нет света · нет второго шанса", 26, MUTED, "middle", 700))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', sky_band(150)]
    b.append(rock([(0, 150), (230, 150), (250, 780), (210, 1920), (0, 1920)], "k9a", 15, True))
    b.append(rock([(1080, 150), (850, 150), (830, 800), (870, 1920), (1080, 1920)], "k9b", 16, True))
    b.append(void([(230, 150), (850, 150), (830, 800), (870, 1920), (210, 1920), (250, 780)], "v9"))
    b.append(diver(500, 820, 1.0, "#0a1a20", "dv9"))
    b.append(beam(570, 812, 78, "bm9", 420, 8, TORCH, 0.12))
    b.append(chip(120, 1000, "30 м"))
    b.append(hud(60, 250, "2005", "08:15", "30 М"))
    b.append(t(60, 1700, "ДЭЙВ ШОУ · АВСТРАЛИЙСКИЙ ПИЛОТ", 22, "#f0e2a0", w=800))
    return b


# ---------------------------------------------------------------- 10
def s10():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(rock([(0, 0), (150, 0), (150, 1920), (0, 1920)], "k10a", 17))
    b.append(rock([(1080, 0), (930, 0), (930, 1920), (1080, 1920)], "k10b", 18))
    b.append(f'<rect x="300" y="700" width="220" height="280" rx="18" fill="#12303b" stroke="{GLOW}" stroke-width="3"/>')
    b.append(f'<circle cx="410" cy="800" r="44" fill="{TORCH}" opacity="0.7"/>')
    b.append(f'<rect x="600" y="720" width="80" height="260" rx="38" fill="#12303b" stroke="{GLOW}" stroke-width="3"/>')
    b.append(f'<rect x="710" y="720" width="80" height="260" rx="38" fill="#12303b" stroke="{GLOW}" stroke-width="3"/>')
    b.append(f'<path d="M 560 760 q 50 -34 100 0" stroke="{GLOW}" stroke-width="5" fill="none"/>')
    b.append(t(60, 260, "ГОД ПОДГОТОВКИ", 42, GLOW, ls=1))
    b.append(t(60, 320, "ребризер · смеси · команда", 24, MUTED, w=700))
    b.append(t(60, 1620, "ошибка стоит жизни", 26, TORCH, w=800))
    return b


# ---------------------------------------------------------------- 11
def s11():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(rock([(0, 0), (280, 0), (300, 820), (260, 1920), (0, 1920)], "k11a", 19))
    b.append(rock([(1080, 0), (780, 0), (760, 840), (800, 1920), (1080, 1920)], "k11b", 20))
    b.append(void([(280, 0), (780, 0), (760, 840), (800, 1920), (260, 1920), (300, 820)], "v11"))
    b.append(f'<path d="M 540 200 L 540 1700" stroke="#dbe9e6" stroke-width="2.5" stroke-dasharray="22 14" opacity="0.7"/>')
    for i, yy in enumerate((360, 660, 960, 1260)):
        b.append(f'<g class="mk{i}">{diver(470, yy, 0.42, "#0a1a20", f"mk{i}d")}'
                 f'<circle cx="540" cy="{yy}" r="7" fill="{TORCH}"/></g>')
    b.append(t(60, 180, "СПУСК 25 МИНУТ", 38, GLOW, ls=1))
    b.append(t(60, 232, "подъём — много часов", 22, MUTED, w=700))
    b.append(hud(60, 300, "08.01.2005", "09:20", "270 М"))
    return b


# ---------------------------------------------------------------- 12
def s12():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(rock([(0, 0), (190, 0), (210, 820), (170, 1920), (0, 1920)], "k12a", 21))
    b.append(rock([(1080, 0), (890, 0), (870, 840), (910, 1920), (1080, 1920)], "k12b", 22))
    b.append(void([(190, 0), (890, 0), (870, 840), (910, 1920), (170, 1920), (210, 820)], "v12"))
    b.append(f'<path d="M 170 1520 q 370 -40 740 0 l 0 400 l -740 0 z" fill="#0a2028" stroke="#5d7b85" stroke-width="2"/>')
    b.append(f'<rect x="320" y="1310" width="180" height="46" rx="23" fill="#8ba3ad" opacity="0.92"/>')
    b.append(f'<circle cx="510" cy="1332" r="25" fill="#a3bac4"/>')
    b.append(f'<path d="M 320 1332 l -46 -22 l 0 44 z" fill="#75919c"/>')
    b.append(diver(520, 1080, 0.85, "#0a1a20", "dv12"))
    b.append(beam(590, 1072, 92, "bm12", 320, 8, TORCH, 0.12))
    b.append(chip(700, 1440, "270 м"))
    b.append(t(60, 200, "ОН НАШЁЛ ЕГО", 40, GLOW, ls=1))
    b.append(t(60, 250, "и начал поднимать к свету", 22, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 13
def s13():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(rock([(0, 0), (400, 0), (420, 700), (370, 1320), (410, 1920), (0, 1920)], "k13a", 23))
    b.append(rock([(1080, 0), (700, 0), (680, 720), (740, 1320), (700, 1920), (1080, 1920)], "k13b", 24))
    b.append(void([(400, 0), (700, 0), (680, 720), (740, 1320), (700, 1920), (410, 1920), (370, 1320), (420, 700)], "v13"))
    for i in range(3):
        b.append(f'<path class="ln{i}" d="M {420+i*40} 260 q 150 280 30 580 q -120 300 90 520" stroke="#cfe6e2" '
                 f'stroke-width="3" fill="none" opacity="{0.5-i*0.12:.2f}"/>')
    b.append(f'<circle cx="540" cy="980" r="110" fill="{TORCH}" opacity="0.12"/>')
    b.append(diver(520, 980, 1.0, "#2a4a55", "dv13"))
    b.append(t(60, 200, "СТРАХОВОЧНЫЙ ТРОС", 28, MUTED, ls=1))
    b.append(t(60, 250, "запутал его на глубине", 26, RED, w=800))
    return b


# ---------------------------------------------------------------- 14
def s14():
    b = [f'<rect width="1080" height="1920" fill="#01070a"/>']
    b.append(rock([(0, 0), (260, 0), (280, 1920), (0, 1920)], "k14a", 25))
    b.append(rock([(1080, 0), (820, 0), (800, 1920), (1080, 1920)], "k14b", 26))
    b.append(f'<circle cx="540" cy="900" r="300" fill="{TORCH}" opacity="0.06"/>')
    b.append(f'<circle class="flash" cx="540" cy="900" r="90" fill="{TORCH}" opacity="0.35"/>')
    b.append(t(540, 1300, "ЛУЧ ЕЩЁ ДВИГАЛСЯ", 36, GLOW, "middle", 900))
    b.append(t(540, 1360, "потом замер", 30, MUTED, "middle", 700))
    return b


# ---------------------------------------------------------------- 15
def s15():
    b = [f'<rect width="1080" height="1920" fill="#050b0e"/>']
    b.append(f'<rect x="90" y="420" width="900" height="1080" fill="#0b1c22" stroke="{MUTED}" stroke-width="3"/>')
    b.append(f'<circle cx="150" cy="480" r="12" fill="{RED}"/>')
    b.append(t(180, 490, "REC", 24, RED, w=900))
    b.append(f'<path d="M 300 1200 q 200 -300 480 -200" stroke="{TORCH}" stroke-width="5" fill="none" opacity="0.5"/>')
    b.append(f'<circle cx="640" cy="900" r="60" fill="{TORCH}" opacity="0.12"/>')
    b.append(t(60, 250, "КАМЕРА НА ШЛЕМЕ", 34, MUTED, ls=1))
    b.append(t(60, 1620, "записала последние минуты", 24, GLOW, w=700))
    return b


# ---------------------------------------------------------------- 16
def s16():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', sky_band(150)]
    b.append(rock([(0, 150), (280, 150), (300, 900), (250, 1920), (0, 1920)], "k16a", 27, True))
    b.append(rock([(1080, 150), (800, 150), (780, 920), (830, 1920), (1080, 1920)], "k16b", 28, True))
    b.append(void([(280, 150), (800, 150), (780, 920), (830, 1920), (250, 1920), (300, 900)], "v16"))
    b.append(f'<ellipse cx="540" cy="230" rx="300" ry="70" fill="{TORCH}" opacity="0.25"/>')
    b.append(diver(470, 900, 0.75, "#0a1a20", "d16a"))
    b.append(beam(530, 894, 40, "bm16a", 300, 8, TORCH, 0.10))
    b.append(diver(600, 1030, 0.7, "#0a1a20", "d16b"))
    b.append(beam(656, 1024, 40, "bm16b", 280, 8, TORCH, 0.09))
    b.append(t(60, 240, "12 ЯНВАРЯ", 40, GLOW, ls=2))
    b.append(t(60, 292, "подняли обоих", 26, TORCH, w=800))
    return b


# ---------------------------------------------------------------- 17
def s17():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(f'<circle cx="540" cy="820" r="300" fill="#0a2a33" opacity="0.6"/>')
    b.append(f'<circle cx="540" cy="820" r="120" fill="{TORCH}" opacity="0.12"/>')
    b.append(t(540, 780, "ДЭЙВ", 70, GLOW, "middle", 900, ls=4))
    b.append(t(540, 858, "НЕ ВЕРНЁТСЯ", 70, TORCH, "middle", 900, ls=2))
    b.append(t(540, 950, "документальный фильм, 2020", 24, MUTED, "middle", 700))
    b.append(t(540, 1660, "Boesmansgat · ЮАР", 22, MUTED, "middle", 700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17]
ANIM = [
    'tl.fromTo(".dv1", {opacity:0, y:-40}, {opacity:1, y:0, duration:1.0}, 0.05);'
    'tl.to(".dv1", {y:120, duration:3.2, ease:"sine.inOut"}, 1.0);'
    'tl.to(".dv1b", {y:80, duration:3.0, ease:"sine.inOut"}, 1.2);'
    'tl.fromTo(".rope", {opacity:0}, {opacity:0.55, duration:0.8}, 0.3);'
    'tl.fromTo(".hud", {opacity:0, y:-12}, {opacity:1, y:0, duration:0.5}, 0.4);'
    'tl.fromTo(".chip", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 1.0);',
    'tl.fromTo(".m0", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.to(".m0", {y:260, duration:3.0, ease:"sine.inOut"}, 0.4);'
    'tl.fromTo(".m1", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.to(".m1", {y:220, duration:3.2, ease:"sine.inOut"}, 0.7);'
    'tl.fromTo(".m2", {opacity:0}, {opacity:1, duration:0.5}, 0.8);'
    'tl.to(".m2", {y:180, duration:3.4, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0);',
    'tl.fromTo(".dv4", {opacity:0, y:-30}, {opacity:1, y:0, duration:0.9}, 0.05);'
    'tl.to(".dv4", {y:180, duration:2.4, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".hud", {opacity:0}, {opacity:1, duration:0.5}, 0.4);'
    'tl.fromTo(".chip", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 1.0);',
    'tl.fromTo(".dv5", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.05);'
    'tl.to(".dv5", {y:-160, duration:2.4, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".hud", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.fromTo(".chip", {opacity:0}, {opacity:1, duration:0.4}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.9);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.15}, 0);'
    'tl.fromTo(".chip", {opacity:0}, {opacity:1, duration:0.4}, 0.3);',
    'tl.fromTo(".hl", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6, stagger:0.1}, 0);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0);',
    'tl.fromTo(".dv9", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.8}, 0.05);'
    'tl.to(".dv9", {y:200, duration:2.4, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".hud", {opacity:0}, {opacity:1, duration:0.5}, 0.35);'
    'tl.fromTo(".chip", {opacity:0}, {opacity:1, duration:0.4}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 1.0);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.1}, 0);',
    'tl.fromTo(".mk0, .mk1, .mk2, .mk3", {opacity:0}, {opacity:1, duration:0.4, stagger:0.3}, 0.2);'
    'tl.fromTo(".hud", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".dv12", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.8}, 0.05);'
    'tl.to(".dv12", {y:90, duration:2.0, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".chip", {opacity:0}, {opacity:1, duration:0.4}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".dv13", {opacity:0}, {opacity:1, duration:0.5}, 0.05);'
    'tl.to(".ln0, .ln1, .ln2", {x:10, duration:0.9, stagger:0.1, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.1}, 0);',
    'tl.fromTo(".flash", {opacity:0.5, scale:1}, {opacity:0.05, scale:1.7, duration:1.6, repeat:-1, ease:"power2.out"}, 0.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.1}, 0);',
    'tl.fromTo(".d16a, .d16b", {opacity:0, y:40}, {opacity:1, y:0, duration:0.8, stagger:0.2}, 0.1);'
    'tl.to(".d16a", {y:-220, duration:2.4, ease:"sine.inOut"}, 1.0);'
    'tl.to(".d16b", {y:-260, duration:2.6, ease:"sine.inOut"}, 1.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".hl", {opacity:0, y:16}, {opacity:1, y:0, duration:0.6, stagger:0.18}, 0.1);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{DEEP}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
