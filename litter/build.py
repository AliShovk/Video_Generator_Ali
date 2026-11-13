#!/usr/bin/env python3
"""«Глубокая подстилка» — 9 сцен, тёплая инфографика."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/litter")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#fdf4e3"
INK = "#4a3a2a"
WOOD = "#c98a4b"
WOOD_D = "#8a5a30"
ROOF = "#a4653a"
STRAW = "#e8cf94"
HAY = "#d9b45e"
SOIL = "#5a4030"
SOIL_D = "#3f2c20"
CHICK = "#d97b3c"
CHICK2 = "#e8a13a"
WHITE = "#fbf7ef"
COMB = "#d2452f"
GREEN = "#7fa05a"
BLUE = "#4a8f9e"
RED = "#c94a3a"
OK = "#4f8f4a"


def S(d, w=5, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, op=1.0, cls="fillshape", stroke=INK, sw=5):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=52, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def grain(seed, n=120):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.4):.1f}" '
                   f'fill="#a08a6a" opacity="{r.uniform(0.03,0.08):.2f}"/>' for _ in range(n))


def chicken(x, y, s=1.0, col=CHICK, cls="chick", flip=False):
    f = -1 if flip else 1
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s*f} {s})">'
            # хвост
            f'<path d="M -34 -46 q -26 -18 -34 -2 M -34 -38 q -28 -8 -34 8 M -30 -30 q -26 0 -28 14" '
            f'stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/>'
            # тело
            f'<ellipse cx="0" cy="-38" rx="42" ry="34" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            # крыло
            f'<path d="M -12 -48 q 22 -8 30 14 q -18 12 -32 -2" fill="none" stroke="{INK}" stroke-width="4"/>'
            # шея
            f'<path d="M 22 -62 q 6 -18 18 -20 l 10 0 l 0 26 z" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            # голова
            f'<circle cx="42" cy="-84" r="21" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            # гребень
            f'<path d="M 30 -102 q 4 -14 12 -6 q 6 -12 12 -2 q 8 -6 8 8 q -16 8 -32 0 z" fill="{COMB}" stroke="{INK}" stroke-width="3"/>'
            # клюв
            f'<path d="M 62 -82 l 18 6 l -18 8 z" fill="#e8a13a" stroke="{INK}" stroke-width="3"/>'
            # серьга
            f'<path d="M 52 -66 q 6 12 -2 14 q -8 -2 -6 -14 z" fill="{COMB}" stroke="{INK}" stroke-width="2.5"/>'
            # глаз
            f'<circle cx="50" cy="-88" r="3.2" fill="{INK}"/>'
            # ноги
            f'<path d="M -10 0 l 0 26 M 10 0 l 0 26" stroke="#d99a2e" stroke-width="7" stroke-linecap="round"/>'
            f'<path d="M -10 26 l -12 8 M -10 26 l 10 8 M 10 26 l -10 8 M 10 26 l 12 8" '
            f'stroke="#d99a2e" stroke-width="6" stroke-linecap="round"/>'
            f'</g>')


def egg(x, y, s=1.0, cls="egg"):
    return (f'<ellipse class="{cls}" cx="{x}" cy="{y}" rx="{13*s}" ry="{17*s}" fill="{WHITE}" stroke="{INK}" stroke-width="4"/>')


def coop(x, y, w, h, cut=False, cls="coop"):
    """Курятник: фронтальный разрез или фасад."""
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x-24} {y} L {x+w/2} {y-96} L {x+w+24} {y} Z" fill="{ROOF}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WOOD}" stroke="{INK}" stroke-width="6"/>')
    if cut:
        b.append(f'<rect x="{x+16}" y="{y+16}" width="{w-32}" height="{h-32}" fill="#f6e6cc" stroke="{INK}" stroke-width="4"/>')
        b.append(f'<circle cx="{x+w/2}" cy="{y-46}" r="18" fill="#8a5a30" stroke="{INK}" stroke-width="4"/>')
    if not cut:
        b.append(f'<rect x="{x+w*0.18}" y="{y+h*0.22}" width="{w*0.16}" height="{w*0.14}" fill="#9fc4cf" stroke="{INK}" stroke-width="5"/>'
                 f'<path d="M {x+w*0.26} {y+h*0.22} l 0 {w*0.14} M {x+w*0.18} {y+h*0.22+w*0.07} l {w*0.16} 0" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<rect x="{x+w*0.42}" y="{y+h*0.58}" width="{w*0.18}" height="{h*0.42}" fill="{WOOD_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<path d="M {x+4} {y+h-20} l 0 26 M {x+w-4} {y+h-20} l 0 26" stroke="{INK}" stroke-width="8"/>')
    b.append('</g>')
    return "".join(b)


def litter_block(x, y, w, h, top=0.28, cls="lit"):
    """Разрез подстилки: солома сверху, перегной, земля."""
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SOIL}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h*0.52}" fill="{SOIL_D}" stroke="none"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h*top}" fill="{STRAW}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="{x}" y="{y+h*top}" width="{w}" height="{h*0.26}" fill="{HAY}" stroke="{INK}" stroke-width="4"/>')
    b.append('</g>')
    return "".join(b)


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(1)]
    b.append(f'<ellipse cx="540" cy="1520" rx="420" ry="60" fill="{GREEN}" opacity="0.25"/>')
    b.append(coop(220, 720, 640, 700))
    b.append(f'<rect x="470" y="1120" width="120" height="300" fill="{WOOD_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<circle cx="540" cy="854" r="26" fill="#f0dfc0" stroke="{INK}" stroke-width="5"/>')
    b.append(chicken(330, 1520, 1.8, CHICK, "c1"))
    b.append(chicken(560, 1540, 1.6, CHICK2, "c2", True))
    b.append(chicken(790, 1530, 1.7, WHITE, "c3"))
    b.append(txt(60, 230, "ГЛУБОКАЯ", 74))
    b.append(txt(60, 310, "ПОДСТИЛКА", 74, WOOD_D))
    b.append(txt(60, 1750, "УБОРКА ДВА РАЗА В ГОД", 34, OK))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(2)]
    b.append(coop(150, 470, 780, 820, cut=True, cls="coop2"))
    # внутренний объём
    b.append(f'<rect x="166" y="486" width="748" height="788" fill="#f6e6cc" stroke="none"/>')
    b.append(litter_block(166, 820, 748, 452, 0.34, "lit2"))
    b.append(chicken(360, 820, 1.6, CHICK, "c2a"))
    b.append(chicken(650, 826, 1.5, CHICK2, "c2b", True))
    b.append(egg(790, 840, 1.3, "e2"))
    b.append(f'<path d="M 890 880 L 940 880" stroke="{INK}" stroke-width="4"/>')
    b.append(txt(1070, 892, "солома", 32, INK, "end"))
    b.append(f'<path d="M 890 1010 L 940 1010" stroke="{INK}" stroke-width="4"/>')
    b.append(txt(1070, 1022, "перегной", 32, INK, "end"))
    b.append(f'<path d="M 890 1180 L 940 1180" stroke="{INK}" stroke-width="4"/>')
    b.append(txt(1070, 1192, "земля", 32, INK, "end"))
    b.append(txt(60, 300, "КАК ЭТО РАБОТАЕТ", 54))
    b.append(txt(60, 1780, "СЛОЙ РАБОТАЕТ КАК КОМПОСТ", 28, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(3)]
    b.append(litter_block(100, 520, 880, 720, 0.24, "lit3"))
    r = random.Random(9)
    # черви
    for i in range(7):
        x = 170 + i * 115
        y = 900 + r.uniform(-40, 120)
        b.append(f'<path class="worm" d="M {x} {y} q 20 -18 40 0 q 20 18 40 0" stroke="#c98a8a" stroke-width="10" fill="none" stroke-linecap="round"/>')
    # жуки
    for i in range(5):
        x = 220 + i * 150
        y = 1080 + r.uniform(-30, 60)
        b.append(f'<g class="bug"><ellipse cx="{x}" cy="{y}" rx="16" ry="11" fill="#6b4a2a" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M {x-16} {y} l 32 0" stroke="{INK}" stroke-width="2"/></g>')
    # бактерии
    for i in range(6):
        x = 200 + i * 130
        y = 760 + r.uniform(-30, 40)
        b.append(f'<circle class="bac" cx="{x}" cy="{y}" r="9" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
    b.append(txt(60, 330, "ЖИЗНЬ ВНУТРИ", 54))
    b.append(txt(60, 400, "бактерии и черви перерабатывают помёт", 26, "#7a5a3a"))
    b.append(txt(60, 1700, "ЧЕМ БОЛЬШЕ СЛОЙ — ТЕМ АКТИВНЕЕ", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(4)]
    b.append(coop(180, 520, 720, 760, cut=True, cls="coop4"))
    b.append(f'<rect x="196" y="536" width="688" height="728" fill="#f6e6cc" stroke="none"/>')
    b.append(litter_block(196, 900, 688, 364, 0.4, "lit4"))
    b.append(chicken(380, 900, 1.6, CHICK, "c4"))
    b.append(chicken(680, 906, 1.5, CHICK2, "c4b", True))
    # тепло
    for i in range(4):
        b.append(f'<path class="heat4" d="M {340 + i*140} 860 q 22 -40 0 -80 q -22 -40 0 -80" stroke="#e8a13a" '
                 f'stroke-width="8" fill="none" opacity="0.8"/>')
    b.append(txt(60, 300, "ТЕПЛО ЗИМОЙ", 56))
    b.append(f'<g class="th4"><rect x="120" y="1180" width="54" height="300" rx="26" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="130" y="1350" width="34" height="120" rx="16" fill="{BLUE}"/>'
             f'<circle cx="147" cy="1500" r="34" fill="{BLUE}" stroke="{INK}" stroke-width="5"/>'
             f'<text x="147" y="1580" font-family="Nunito" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">−10°</text></g>')
    b.append(f'<g class="th4b"><rect x="900" y="1120" width="54" height="360" rx="26" fill="{WHITE}" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="910" y="1190" width="34" height="280" rx="16" fill="{RED}"/>'
             f'<circle cx="927" cy="1500" r="34" fill="{RED}" stroke="{INK}" stroke-width="5"/>'
             f'<text x="927" y="1580" font-family="Nunito" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">+12°</text></g>')
    b.append(txt(60, 1780, "БЕЗ ОБОГРЕВАТЕЛЯ", 30, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(5)]
    b.append(litter_block(110, 760, 860, 460, 0.34, "lit5"))
    # вилы
    b.append(f'<g class="fork5"><path d="M 300 330 L 470 760" stroke="{WOOD_D}" stroke-width="16" stroke-linecap="round"/>'
             f'<path d="M 430 740 l 40 40 M 460 760 l 40 40 M 490 780 l 40 40" stroke="#8a8f95" stroke-width="9" stroke-linecap="round"/></g>')
    # мешок
    b.append(f'<g class="sack5"><path d="M 760 760 q -30 -80 34 -104 q 66 -24 100 30 q 30 48 -10 74 z" fill="#d8c3a0" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 796 660 q 26 -22 58 -12" stroke="{INK}" stroke-width="4" fill="none"/></g>')
    for i in range(8):
        b.append(f'<circle class="fall5" cx="{700 + (i%4)*34}" cy="{700 - (i//4)*30}" r="7" fill="{STRAW}" stroke="{INK}" stroke-width="2"/>')
    b.append(txt(60, 330, "РАЗ В НЕДЕЛЮ", 54))
    b.append(txt(60, 400, "провернуть вилами и подсыпать", 26, "#7a5a3a"))
    b.append(txt(60, 1700, "СВЕЖИЙ СЛОЙ — СВЕРХУ", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(6)]
    b.append(litter_block(120, 1180, 840, 300, 0.4, "lit6"))
    # стена с дверью
    b.append(f'<rect x="120" y="620" width="380" height="560" fill="{WOOD}" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<rect x="200" y="760" width="220" height="420" fill="{WOOD_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="220" y="800" width="180" height="150" fill="#9fc4cf" stroke="{INK}" stroke-width="4"/>')
    # порог и уровень
    b.append(f'<rect x="190" y="1160" width="240" height="26" fill="#b98a50" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<path class="lvl6" d="M 470 1180 l 0 -130" stroke="{RED}" stroke-width="7"/>')
    b.append(f'<path d="M 456 1050 l 28 0 M 456 1180 l 28 0" stroke="{RED}" stroke-width="6"/>')
    b.append(txt(500, 1120, "6–8 см", 40, RED))
    b.append(txt(540, 700, "ПОРОГ", 46))
    b.append(txt(540, 770, "выше подстилки", 26, "#7a5a3a"))
    b.append(txt(60, 330, "ВЫСОТА ПОРОГА", 50))
    b.append(txt(60, 1720, "ИНАЧЕ ПОДСТИЛКА ПОЛЕЗЕТ НАРУЖУ", 24, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(7)]
    b.append(txt(60, 300, "МАТЕРИАЛЫ", 54))
    # хорошо
    b.append(f'<rect x="80" y="420" width="440" height="900" rx="28" fill="#eef6ea" stroke="{OK}" stroke-width="7"/>')
    b.append(f'<circle cx="300" cy="500" r="46" fill="{OK}"/>')
    b.append(f'<path d="M 272 500 l 20 24 l 40 -50" stroke="{WHITE}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    b.append(txt(300, 600, "ОПИЛКИ", 42, INK, "middle"))
    b.append(txt(300, 650, "КОНОПЛЯ", 42, INK, "middle"))
    for i in range(7):
        b.append(f'<path class="good7" d="M {150 + i*50} 760 q 20 -30 0 -60" stroke="{STRAW}" stroke-width="9" fill="none"/>')
    b.append(f'<path d="M 150 860 q 150 -40 300 0" stroke="{HAY}" stroke-width="18" fill="none"/>')
    b.append(txt(300, 1000, "впитывает", 28, "#4a6b3a", "middle"))
    b.append(txt(300, 1045, "и разлагается", 28, "#4a6b3a", "middle"))
    b.append(txt(300, 1230, "рыхлые", 26, "#4a6b3a", "middle"))
    # плохо
    b.append(f'<rect x="560" y="420" width="440" height="900" rx="28" fill="#fdecea" stroke="{RED}" stroke-width="7"/>')
    b.append(f'<circle cx="780" cy="500" r="46" fill="{RED}"/>')
    b.append(f'<path d="M 758 478 l 44 44 M 802 478 l -44 44" stroke="{WHITE}" stroke-width="12" stroke-linecap="round"/>')
    b.append(txt(780, 600, "СЕНО", 44, INK, "middle"))
    for i in range(6):
        b.append(f'<path class="bad7" d="M {620 + i*50} 760 q 26 -34 0 -70" stroke="#b9a36a" stroke-width="9" fill="none"/>')
    b.append(f'<path d="M 620 870 q 160 -30 320 0" stroke="#a08a5a" stroke-width="18" fill="none"/>')
    b.append(txt(780, 1000, "не впитывает", 28, "#8a3a2a", "middle"))
    b.append(txt(780, 1230, "киснет", 28, "#8a3a2a", "middle"))
    b.append(txt(60, 1700, "СЕНО ПЛЕСНЕВЕЕТ И ДАЁТ ЗАПАХ", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(8)]
    b.append(litter_block(100, 900, 880, 540, 0.32, "lit8"))
    # банка-распылитель
    b.append(f'<g class="hand8"><g transform="translate(790 690) rotate(-22) scale(1.55)">'
             f'<rect x="-70" y="-60" width="140" height="120" rx="14" fill="#e8dcc4" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="-70" y="-60" width="140" height="40" rx="12" fill="#c9b28a" stroke="{INK}" stroke-width="6"/>'
             f'<text x="0" y="24" font-family="Nunito" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">DE</text>'
             f'<g opacity="0.8">'
             + "".join(f'<circle cx="{-40 + (i%5)*20}" cy="-50" r="4" fill="{INK}"/>' for i in range(10))
             + '</g></g></g>')
    for i in range(18):
        b.append(f'<circle class="pow8" cx="{650 - (i%5)*26}" cy="{800 + (i//5)*34}" r="8" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>')
    # пыль на поверхности
    b.append(f'<path class="dust8" d="M 220 912 q 130 -26 280 0 q -130 22 -280 0 z" fill="{WHITE}" opacity="0.85" stroke="{INK}" stroke-width="4"/>')
    # клещ и крест
    b.append(f'<g class="mite8"><circle cx="320" cy="906" r="26" fill="#8a3a2a" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M 296 888 l -18 -14 M 344 888 l 18 -14 M 296 924 l -18 14 M 344 924 l 18 14" stroke="{INK}" stroke-width="3"/></g>')
    b.append(f'<path class="x8" d="M 262 846 l 116 118 M 378 846 l -116 118" stroke="{RED}" stroke-width="11" stroke-linecap="round"/>')
    b.append(txt(60, 330, "ДИАТОМИТ", 54))
    b.append(txt(60, 400, "тонкий слой от клещей и пухоедов", 26, "#7a5a3a"))
    b.append(txt(60, 1780, "БЕЗОПАСНО ДЛЯ КУР И ЯИЦ", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s9
def s9():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(9)]
    b.append(f'<ellipse cx="540" cy="1420" rx="420" ry="60" fill="{GREEN}" opacity="0.25"/>')
    b.append(coop(230, 660, 620, 640))
    b.append(chicken(340, 1400, 2.0, CHICK, "c9a"))
    b.append(chicken(690, 1420, 1.8, WHITE, "c9b", True))
    b.append(egg(500, 1400, 1.2, "e9"))
    b.append(egg(560, 1420, 1.2, "e9b"))
    items = ["сухо", "тепло", "чисто"]
    for i, s_ in enumerate(items):
        y = 1500 + i * 90
        b.append(f'<circle cx="140" cy="{y-18}" r="26" fill="{OK}"/>')
        b.append(f'<path d="M 128 {y-18} l 10 12 l 20 -24" stroke="{WHITE}" stroke-width="7" fill="none" stroke-linecap="round"/>')
        b.append(txt(190, y, s_, 40))
    b.append(txt(60, 340, "ИТОГ", 56))
    b.append(txt(60, 420, "меньше работы — больше яиц", 28, "#7a5a3a"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".chick", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6, stagger:0.2}, 0.2);'
    'tl.to(".chick", {y:-8, duration:0.5, stagger:0.15, yoyo:true, repeat:3}, 1.2);',
    'tl.fromTo(".coop2", {opacity:0, scale:0.9, transformOrigin:"50% 100%"}, {opacity:1, scale:1, duration:0.7}, 0.1);'
    'tl.fromTo(".lit2", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.9}, 0.5);'
    'tl.fromTo(".chick", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 1.0);'
    'tl.fromTo(".egg", {opacity:0, scale:0.4, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.4}, 1.8);',
    'tl.fromTo(".worm", {opacity:0}, {opacity:1, duration:0.5, stagger:0.18}, 0.3);'
    'tl.fromTo(".bug", {opacity:0, y:10}, {opacity:1, y:0, duration:0.4, stagger:0.15}, 0.7);'
    'tl.fromTo(".bac", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.4, stagger:0.1}, 1.1);'
    'tl.to(".worm", {x:18, duration:1.2, yoyo:true, repeat:3, ease:"sine.inOut", stagger:0.1}, 1.0);',
    'tl.to(".heat4", {y:-16, opacity:0.3, duration:0.9, stagger:0.12, yoyo:true, repeat:6}, 0.3);'
    'tl.to(".chick", {y:-6, duration:0.5, yoyo:true, repeat:4}, 0.6);'
    'tl.fromTo(".th4, .th4b", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.3}, 0.8);',
    'tl.fromTo(".fork5", {rotation:-16, transformOrigin:"30% 90%"}, {rotation:8, duration:1.0, yoyo:true, repeat:3, ease:"sine.inOut"}, 0.2);'
    'tl.fromTo(".sack5", {opacity:0, x:40}, {opacity:1, x:0, duration:0.5}, 0.8);'
    'tl.to(".fall5", {y:80, opacity:0, duration:0.9, stagger:0.1, repeat:4}, 1.0);',
    'tl.fromTo(".lvl6", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.7}, 0.6);'
    'tl.fromTo(".lit6", {scaleY:0.4, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.8}, 0.3);',
    'tl.fromTo(".good7", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.4, stagger:0.08}, 0.5);'
    'tl.fromTo(".bad7", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.4, stagger:0.08}, 0.9);',
    'tl.fromTo(".hand8", {y:-60, opacity:0}, {y:0, opacity:1, duration:0.7}, 0.3);'
    'tl.to(".pow8", {y:120, opacity:0, duration:1.1, stagger:0.06, repeat:4}, 0.7);'
    'tl.fromTo(".mite8, .x8", {opacity:0}, {opacity:1, duration:0.4}, 1.4);',
    'tl.fromTo(".chick", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6, stagger:0.2}, 0.2);'
    'tl.to(".chick", {y:-8, duration:0.5, stagger:0.2, yoyo:true, repeat:3}, 1.2);'
    'tl.fromTo(".egg", {opacity:0, scale:0.4, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.4, stagger:0.2}, 1.4);',
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
