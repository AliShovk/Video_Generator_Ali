#!/usr/bin/env python3
"""Иллюстрация «дом-башня на колёсах, который тянут быки» — по мотивам референса."""
from pathlib import Path

ROOT = Path("/root/video-gen/towerhouse")
ROOT.mkdir(parents=True, exist_ok=True)

INK = "#3b332b"
CREAM = "#efe3cc"
CREAM_D = "#e4d5ba"
ORANGE = "#e79a36"
ORANGE_D = "#cf7d2a"
TERRA = "#c8703a"
RED = "#b5462f"
BLUE = "#4a8f9e"
BLUE_D = "#3a7280"
GREEN = "#7f9c68"
GREEN_D = "#5f7d4a"
BROWN = "#8a5a3a"
SAND = "#d8c3a0"
WHITE = "#fbf7ef"
GRASS = "#b9c98a"

parts = []


def add(s):
    parts.append(s)


def p(d, fill="none", stroke=INK, w=2.4, extra="", op=1.0):
    add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" '
        f'stroke-linecap="round" opacity="{op}" {extra}/>')


def rect(x, y, w, h, fill=CREAM, stroke=INK, sw=2.4, rx=0, extra=""):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}" {extra}/>')


def circ(cx, cy, r, fill=CREAM, stroke=INK, sw=2.4):
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def line(x1, y1, x2, y2, stroke=INK, w=2.2, extra=""):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}" {extra}/>')


# ---------------------------------------------------------------- фон
add('<rect width="830" height="1000" fill="#fdfaf3"/>')
add(f'<ellipse cx="400" cy="905" rx="360" ry="34" fill="{GRASS}" opacity="0.35"/>')

# ---------------------------------------------------------------- башня (корпус)
p("M 258 838 L 258 300 Q 258 250 300 236 L 420 236 Q 462 250 462 300 L 462 838 Z", CREAM, INK, 2.8)

# фактура штукатурки
for i in range(9):
    y = 320 + i * 56
    add(f'<path d="M {270 + (i%3)*8} {y} q 40 -6 80 0" stroke="{CREAM_D}" stroke-width="3" fill="none" opacity="0.8"/>')

# ---------------------------------------------------------------- арка-крыша
p("M 250 300 Q 250 196 300 190 L 420 190 Q 470 196 470 300 Z", ORANGE, INK, 2.8)
# узор крыши
for i in range(11):
    x = 262 + i * 19
    p(f"M {x} 206 l 9 18 l 9 -18", "none", ORANGE_D, 2.2)
for i in range(9):
    x = 268 + i * 22
    p(f"M {x} 246 l 10 18 l 10 -18", "none", "#f0b95e", 2.0, op=0.9)
p("M 250 300 Q 250 276 300 272 L 420 272 Q 470 276 470 300 Z", "#f2b45c", INK, 2.2)

# люк на крыше
rect(330, 268, 60, 26, "#8a5a3a", INK, 2.2, 3)
line(336, 281, 384, 281, "#f0d9b0", 2)

# флюгер
add('<g class="vane">')
line(360, 190, 360, 96, INK, 3)
p("M 330 128 L 396 118 L 396 138 Z", "#5aa9bd", INK, 2.2)
add(f'<text x="363" y="132" font-family="Nunito, Arial" font-size="12" font-weight="900" fill="#f6f1e6" '
    f'text-anchor="middle">N</text>')
# петух
p("M 352 92 q 6 -18 18 -16 q 12 2 10 16 q -2 12 -14 12 q -14 0 -14 -12 z", "#cf7d2a", INK, 2)
p("M 366 76 q 4 -12 12 -10 q 3 8 -4 12 z", "#b5462f", INK, 1.8)
p("M 352 84 q -10 -4 -12 4 q 8 4 12 2 z", "#cf7d2a", INK, 1.8)
circ(372, 84, 1.8, INK, INK, 1)
add('</g>')

# ---------------------------------------------------------------- лестница
line(300, 236, 268, 420, INK, 3)
line(330, 238, 298, 424, INK, 3)
for i in range(7):
    t = i / 7
    x1 = 300 - 32 * t
    y1 = 236 + 184 * t
    line(x1, y1, x1 + 30, y1 + 2, INK, 2.2)

# ---------------------------------------------------------------- свисающие корзины и балки
p("M 262 356 L 214 356", BROWN, INK, 5)
p("M 262 372 L 218 372", BROWN, INK, 5)
line(226, 356, 226, 392, "#6b4a2a", 2)
line(246, 356, 246, 398, "#6b4a2a", 2)
p("M 212 392 l 28 0 l -5 24 l -18 0 z", "#c9a06a", INK, 2)
p("M 236 398 l 26 0 l -4 20 l -18 0 z", "#b98a50", INK, 2)

# ---------------------------------------------------------------- окна
def window(x, y, w=34, h=40, shutters=False):
    rect(x, y, w, h, "#f7d98a", INK, 2.2)
    line(x + w / 2, y, x + w / 2, y + h, INK, 1.8)
    line(x, y + h / 2, x + w, y + h / 2, INK, 1.8)
    if shutters:
        rect(x - 10, y + 2, 8, h - 4, "#8fa9a0", INK, 1.8)
        rect(x + w + 2, y + 2, 8, h - 4, "#8fa9a0", INK, 1.8)
    # горшок
    p(f"M {x+6} {y+h} q 10 14 22 0", "#c8703a", INK, 2)


window(300, 300, 34, 40, True)
window(392, 330, 30, 34)
window(300, 470, 36, 42, True)
window(392, 486, 30, 36)

# бельевая верёвка
line(330, 452, 446, 470, INK, 1.6)
for i, (dx, col) in enumerate([(12, "#e8a13a"), (34, "#7fa8c0"), (58, "#c8703a"), (82, "#8fa9a0")]):
    add(f'<path d="M {334+dx} 456 l 14 0 l -4 30 l -8 0 z" fill="{col}" stroke="{INK}" stroke-width="1.6"/>')

# вывеска-флажок
p("M 392 430 l 40 0 l -8 22 l -32 0 z", "#e7c98a", INK, 2)
add('<text x="400" y="445" font-family="Nunito, Arial" font-size="10" font-weight="700" fill="#3b332b">дом</text>')

# ---------------------------------------------------------------- зелёный навес
p("M 372 640 q 44 -22 88 0 l 0 10 l -88 0 z", GREEN, INK, 2.4)
for i in range(6):
    p(f"M {376 + i*15} 640 l 7 10 l 7 -10", "none", GREEN_D, 1.8)

# окно под навесом
window(396, 656, 32, 40)

# ---------------------------------------------------------------- низ башни
p("M 258 800 L 462 800 L 462 838 L 258 838 Z", BLUE, INK, 2.4)
circ(300, 818, 12, "#bfe0e6", INK, 2.2)
circ(420, 818, 12, "#bfe0e6", INK, 2.2)

# дверь с навесом
rect(330, 726, 60, 92, "#a9713f", INK, 2.4, 3)
line(360, 730, 360, 814, "#7d4f28", 2)
circ(352, 776, 2.4, "#e8c98a", INK, 1.4)
p("M 318 726 q 42 -34 84 0 z", "#c8703a", INK, 2.2)
# ступени
p("M 326 818 l 68 0 l 6 12 l -80 0 z", "#d8c3a0", INK, 2)

# ---------------------------------------------------------------- левый флигель
p("M 62 838 L 62 640 L 156 596 L 256 640 L 256 838 Z", CREAM, INK, 2.6)
p("M 50 646 L 156 588 L 264 646 L 256 662 L 156 610 L 62 662 Z", ORANGE, INK, 2.4)
# черепица
for i in range(5):
    y = 660 + i * 34
    add(f'<path d="M {70 + i*4} {y} q 40 -8 80 0 q 40 8 80 0" stroke="{ORANGE_D}" stroke-width="2" fill="none" opacity="0.85"/>')
rect(150, 596, 0.1, 0.1, "none", "none", 0)
# заплатки на крыше
p("M 96 690 l 34 -4 l 4 26 l -34 4 z", "#f0c98a", INK, 1.8)
p("M 176 700 l 30 -2 l 2 22 l -30 2 z", "#e8b96a", INK, 1.8)
# труба
p("M 92 600 l 22 0 l 0 -46 l -22 0 z", "#b07a56", INK, 2.4)
p("M 88 554 l 30 0 l 0 8 l -30 0 z", "#8a5a3a", INK, 2.2)

# окна флигеля
window(96, 720, 40, 44, True)
window(170, 720, 40, 44, True)
# дверь-проём с животным
p("M 120 828 L 120 712 q 26 -18 52 0 L 172 828 Z", "#7d4f28", INK, 2.4)
p("M 132 800 q 14 -22 28 0 q -14 18 -28 0 z", "#e8dcc4", INK, 2)
circ(140, 792, 2, INK, INK, 1)

# маленькая пристройка-тележка слева
p("M 24 828 L 24 760 L 66 738 L 66 828 Z", "#d9c9a8", INK, 2.4)
p("M 18 764 L 66 734 L 74 746 L 26 776 Z", TERRA, INK, 2.2)
rect(34, 782, 20, 20, "#f7d98a", INK, 2)

# ---------------------------------------------------------------- колёса
def wheel(cx, cy, r):
    add(f'<g class="whl" data-cx="{cx}" data-cy="{cy}">')
    circ(cx, cy, r, "#e8dcc4", INK, 2.6)
    circ(cx, cy, r * 0.55, "#c9b28a", INK, 2.2)
    circ(cx, cy, r * 0.18, BLUE, INK, 2)
    for i in range(8):
        import math
        a = i * math.pi / 4
        line(cx + r * 0.2 * math.cos(a), cy + r * 0.2 * math.sin(a),
             cx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a), INK, 1.8)
    add('</g>')


wheel(58, 842, 30)
wheel(196, 842, 30)
wheel(292, 850, 26)
wheel(430, 850, 26)

# ---------------------------------------------------------------- гирлянда флажков
add('<g class="flags">')
line(244, 470, 120, 500, INK, 1.6)
line(244, 470, 60, 430, INK, 1.6)
for i in range(7):
    t = i / 7
    x = 244 - 124 * t
    y = 470 + 30 * t
    p(f"M {x} {y} l 12 2 l -4 16 z", ["#e8a13a", "#7fa8c0", "#c8703a", "#8fa9a0"][i % 4], INK, 1.6)
for i in range(5):
    t = i / 5
    x = 244 - 184 * t
    y = 470 - 40 * t
    p(f"M {x} {y} l 12 2 l -4 16 z", ["#c8703a", "#8fa9a0", "#e8a13a"][i % 3], INK, 1.6)
add('</g>')

# ---------------------------------------------------------------- быки и упряжь
OXN = [0]


def ox(x, y, s, col, horn="#e8dcc4", facing=1):
    OXN[0] += 1
    add(f'<g class="ox ox{OXN[0]}"><g transform="translate({x} {y}) scale({s * facing} {s})">')
    # хвост
    p("M -60 -6 q -18 6 -14 30 q 6 -18 16 -22", "none", INK, 2.4)
    p("M -74 24 q 6 10 0 16", col, INK, 4)
    # тело с горбом
    p("M -60 4 q -8 -42 30 -46 l 46 0 q 34 4 34 34 q 0 34 -40 36 l -40 0 q -28 0 -30 -24 z", col, INK, 2.6)
    p("M -6 -42 q 18 -14 38 -4", "none", INK, 2.0)
    # ноги с копытами
    for lx in (-42, -18, 12, 36):
        p(f"M {lx} 20 l 0 28", col, INK, 8)
        add(f'<rect x="{lx-5}" y="{46}" width="12" height="8" rx="2" fill="#5c4a3a" stroke="{INK}" stroke-width="1.8"/>')
    # шея и голова
    p("M 46 -34 q 18 -26 40 -18 l 12 16 q -6 26 -30 30 l -22 -4 z", col, INK, 2.6)
    # морда
    p("M 88 -34 q 20 0 20 14 q 0 14 -18 14 l -12 0 q -6 -14 10 -28 z", "#e8c9a8", INK, 2.4)
    circ(92, -26, 2.6, INK, INK, 1)
    circ(98, -14, 2.0, "#8a5a3a", "#8a5a3a", 1)
    # рога
    p("M 66 -48 q 4 -20 22 -22 q 2 14 -8 20", horn, INK, 2.2)
    p("M 58 -50 q -10 -18 -26 -14 q 2 12 12 16", horn, INK, 2.2)
    # уши
    p("M 56 -40 q -12 -8 -16 0 q 6 10 14 6 z", col, INK, 1.8)
    add('</g></g>')


def yoke(x, y, s=1.0):
    add(f'<g transform="translate({x} {y}) scale({s})">')
    p("M -34 -18 l 68 0", "#a9713f", INK, 6)
    p("M -30 -18 l 0 -12 M 30 -18 l 0 -12", "#8a5a3a", INK, 4)
    add('</g>')


# верёвки от башни к быкам
for (x, y) in [(440, 806), (570, 810), (700, 814)]:
    line(452, 330, x, y, "#8a7a63", 2.0)

ox(470, 814, 0.80, "#b9b3aa", "#e8dcc4", 1)
yoke(440, 790, 0.82)
ox(600, 818, 0.80, "#efe3cc", "#e8dcc4", 1)
yoke(570, 792, 0.82)
ox(730, 822, 0.80, "#c98f4e", "#e8dcc4", 1)
yoke(700, 796, 0.82)

# травка
for i in range(16):
    x = 30 + i * 42
    p(f"M {x} 900 q 4 -14 8 0", "none", GREEN_D, 2, op=0.8)

head = ''.join(parts[:2])
body = ''.join(parts[2:])
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 830 1000" width="1080" height="1301">
{head}<g class="cart">{body}</g>
</svg>'''

(ROOT / "tower.svg").write_text(svg, encoding="utf-8")

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;background:#fdfaf3}} svg{{display:block;width:1080px;height:1470px}}
</style></head><body>{svg}</body></html>"""
(ROOT / "tower.html").write_text(html, encoding="utf-8")
print("ok", len(parts), "элементов")
