#!/usr/bin/env python3
"""«12 применений WD-40» — постер-стиль, 30 с с концовкой."""
import json
import math
from pathlib import Path

ROOT = Path("/root/video-gen/wd40")
T = json.load(open(ROOT / "timings.json"))
ICON_T = T["icon_times"]
OUTRO_T = T["outro"]
TOTAL = T["total"] + 4.63  # концовка

BG = "#f4ead4"
INK = "#1d2b3a"
BLUE = "#1b4f9c"
BLUE_D = "#123a75"
YELLOW = "#f7d117"
RED = "#c62828"
GREY = "#8a949c"

parts = []


def add(s):
    parts.append(s)


def txt(x, y, s, size=40, col=INK, anchor="middle", weight=900, cls="", family="Nunito, Arial"):
    add(f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def circle_icon(n, cx, cy, r=72):
    return (f'<g class="ic ic{n}" opacity="0">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fffdf6" stroke="{BLUE}" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r-8}" fill="none" stroke="{BLUE}" stroke-width="2" opacity="0.35"/>'
            f'</g>')


def num_badge(n, x, y, r=24):
    return (f'<g class="nb nb{n}" opacity="0"><circle cx="{x}" cy="{y}" r="{r}" fill="{BLUE}"/>'
            f'<text x="{x}" y="{y+9}" font-family="Nunito" font-size="28" font-weight="900" fill="#ffffff" '
            f'text-anchor="middle">{n}</text></g>')


# ---------------------------------------------------------------- иконки (в локальных координатах 160×160)
def icon_art(n, cx, cy):
    """Рисует пиктограмму внутри круга r=84 с центром cx,cy."""
    s = f'<g class="art art{n}" opacity="0" transform="translate({cx} {cy}) scale(1.0)">'
    k = 1.0
    if n == 1:  # унитаз
        s += (f'<path d="M -34 -18 q 0 40 34 40 q 34 0 34 -40 z" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="-26" y="-46" width="30" height="28" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M -6 -44 l 0 -18 l 16 0 l 0 18" fill="none" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M 34 -30 l 16 6 M 40 -46 l 12 12" stroke="{YELLOW}" stroke-width="5"/>')
    elif n == 2:  # обувь
        s += (f'<path d="M -40 22 l 0 -34 q 0 -12 12 -12 l 10 0 l 8 20 l 34 12 q 18 8 18 14 z" fill="#8a5a34" '
              f'stroke="{INK}" stroke-width="4"/>'
              f'<path d="M -28 22 l 64 0" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M 12 -22 q 8 10 0 18" stroke="{INK}" stroke-width="3" fill="none"/>'
              f'<circle cx="-22" cy="-38" r="5" fill="#5aa0d8"/><circle cx="-8" cy="-46" r="5" fill="#5aa0d8"/>')
    elif n == 3:  # молния
        s += (f'<path d="M 0 -46 l 0 92" stroke="{INK}" stroke-width="6"/>'
              + "".join(f'<path d="M -18 {-38+i*14} l 18 6 M 18 {-38+i*14} l -18 6" stroke="{INK}" stroke-width="3"/>'
                        for i in range(8))
              + f'<rect x="-22" y="-56" width="44" height="16" rx="4" fill="{GREY}" stroke="{INK}" stroke-width="3"/>'
              + f'<path d="M 34 -34 l 0 20 M 42 -34 l 0 20" stroke="{YELLOW}" stroke-width="5"/>')
    elif n == 4:  # хром / авто
        s += (f'<path d="M -46 16 l 8 -22 q 4 -10 16 -10 l 30 0 q 12 0 16 10 l 22 22 z" fill="#c9d4dc" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="-24" cy="18" r="10" fill="{INK}"/><circle cx="26" cy="18" r="10" fill="{INK}"/>'
              f'<path d="M -14 -18 l 40 0" stroke="#ffffff" stroke-width="4"/>'
              f'<path d="M 34 -40 l 6 -10 M 44 -34 l 12 -4" stroke="{YELLOW}" stroke-width="5"/>')
    elif n == 5:  # ножницы
        s += (f'<path d="M -30 28 L 22 -30 M -30 -30 L 22 28" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
              f'<circle cx="-36" cy="34" r="14" fill="none" stroke="{BLUE}" stroke-width="7"/>'
              f'<circle cx="-36" cy="-34" r="14" fill="none" stroke="{BLUE}" stroke-width="7"/>'
              f'<circle cx="20" cy="0" r="6" fill="{YELLOW}"/>')
    elif n == 6:  # жвачка
        s += (f'<path d="M -40 8 q 6 -34 34 -30 q 26 4 28 26 q 2 26 -26 30 q -30 4 -36 -26 z" fill="#e88fb0" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M -46 34 l 92 0" stroke="{INK}" stroke-width="7"/>'
              f'<path d="M -10 -6 q 10 -12 22 -2" stroke="#ffffff" stroke-width="5" fill="none"/>')
    elif n == 7:  # наклейка
        s += (f'<path d="M -34 -34 l 68 0 l 0 56 l -22 22 l -46 0 z" fill="#f4c95a" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M 34 22 l -22 22 l 0 -22 z" fill="#e0a93a" stroke="{INK}" stroke-width="3"/>'
              f'<path d="M -18 -10 l 30 0" stroke="#ffffff" stroke-width="5"/>')
    elif n == 8:  # карандаш
        s += (f'<path d="M -40 30 l 54 -54 l 18 18 l -54 54 l -24 6 z" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M 14 -24 l 18 18" stroke="{INK}" stroke-width="3"/>'
              f'<path d="M -46 36 l -6 22 l 22 -6 z" fill="#e8b27a" stroke="{INK}" stroke-width="3"/>'
              f'<path d="M -34 40 l 10 10" stroke="{RED}" stroke-width="5"/>')
    elif n == 9:  # кольцо
        s += (f'<circle cx="0" cy="10" r="34" fill="none" stroke="{YELLOW}" stroke-width="12"/>'
              f'<circle cx="0" cy="10" r="34" fill="none" stroke="{INK}" stroke-width="3"/>'
              f'<path d="M 20 -44 l 4 -14 l 6 12 l 14 2 l -10 10 l 2 14 l -12 -8 l -12 8 l 2 -14 l -10 -10 l 14 -2 z" '
              f'fill="{YELLOW}" stroke="{INK}" stroke-width="3"/>')
    elif n == 10:  # замок
        s += (f'<rect x="-34" y="-6" width="68" height="50" rx="8" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M -20 -6 l 0 -18 q 0 -24 20 -24 q 20 0 20 24 l 0 18" fill="none" stroke="{INK}" stroke-width="8"/>'
              f'<circle cx="0" cy="16" r="7" fill="{INK}"/><rect x="-3" y="16" width="6" height="16" fill="{INK}"/>')
    elif n == 11:  # смола/краска
        s += (f'<path d="M -44 20 l 10 -20 q 6 -10 18 -10 l 26 0 q 12 0 16 10 l 18 20 z" fill="#4a6fa5" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="-22" cy="22" r="9" fill="{INK}"/><circle cx="24" cy="22" r="9" fill="{INK}"/>'
              f'<path d="M 6 -34 q 10 -8 18 0 q -4 12 -18 8 z" fill="#5a4a3a" stroke="{INK}" stroke-width="3"/>')
    else:  # петли
        s += (f'<rect x="-30" y="-40" width="22" height="80" fill="{GREY}" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="8" y="-40" width="22" height="80" fill="{GREY}" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="-19" cy="-22" r="4" fill="{INK}"/><circle cx="-19" cy="22" r="4" fill="{INK}"/>'
              f'<circle cx="19" cy="-22" r="4" fill="{INK}"/><circle cx="19" cy="22" r="4" fill="{INK}"/>'
              f'<path d="M 30 0 l 22 0" stroke="{BLUE}" stroke-width="6"/>')
    s += '</g>'
    return s


CAPS = [
    ("ОЧИСТИ УНИТАЗ", "и блеск"), ("ПРОСУШИ ОБУВЬ", "и кожу"), ("РАЗБЛОКИРУЙ", "молнию"),
    ("ВЕРНИ БЛЕСК", "хрому"), ("ОЖИВИ НОЖНИЦЫ", "и инструмент"), ("УБЕРИ ЖВАЧКУ", "с пола"),
    ("СНИМИ НАКЛЕЙКИ", "и скотч"), ("ОТМОЙ СЛЕДЫ", "карандаша"), ("СНИМИ КОЛЬЦО", "с пальца"),
    ("РАЗБЛОКИРУЙ", "замок"), ("УБЕРИ СМОЛУ", "и краску"), ("СМАЖЬ ПЕТЛИ", "без скрипа"),
]

# ---------------------------------------------------------------- каркас
add('<defs>'
    '<linearGradient id="canG" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="#2a63b5"/><stop offset="0.35" stop-color="#4d86cf"/>'
    f'<stop offset="1" stop-color="#1b4f9c"/></linearGradient>'
    '<linearGradient id="goldG" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#ffe14a"/><stop offset="1" stop-color="#efb90e"/></linearGradient>'
    '</defs>')
add(f'<rect width="1080" height="1920" fill="{BG}"/>')

# верхняя лента
add(f'<g class="topBand"><path d="M 50 120 L 1030 120 L 1000 214 L 80 214 Z" fill="{BLUE_D}" stroke="{INK}" stroke-width="4"/>'
    f'<path d="M 30 100 L 1050 100 L 1030 128 L 50 128 Z" fill="{BLUE}"/></g>')
txt(540, 180, "12 ГЕНИАЛЬНЫХ ПРИМЕНЕНИЙ", 46, "#ffffff")
txt(540, 250, "универсальный спрей для всего", 26, BLUE_D)

# баллон
add(f'<g class="can" opacity="0">')
add(f'<rect x="430" y="330" width="220" height="440" rx="26" fill="url(#canG)" stroke="{INK}" stroke-width="5"/>')
add(f'<rect x="452" y="300" width="176" height="46" rx="12" fill="#d9dee3" stroke="{INK}" stroke-width="5"/>')
add(f'<rect x="500" y="268" width="80" height="36" rx="8" fill="{YELLOW}" stroke="{INK}" stroke-width="4"/>')
add(f'<rect x="530" y="252" width="20" height="20" rx="4" fill="{RED}" stroke="{INK}" stroke-width="3"/>')
add(f'<ellipse cx="540" cy="520" rx="98" ry="68" fill="url(#goldG)" stroke="{INK}" stroke-width="4"/>')
add(f'<text x="540" y="540" font-family="Arial Black, Arial" font-size="56" font-weight="900" fill="{BLUE_D}" text-anchor="middle">WD-40</text>')
add(f'<text x="540" y="624" font-family="Nunito" font-size="15" font-weight="800" fill="#ffffff" text-anchor="middle">МНОГОФУНКЦИОНАЛЬНЫЙ</text>')
add(f'<text x="540" y="648" font-family="Nunito" font-size="15" font-weight="800" fill="#ffffff" text-anchor="middle">ПРОДУКТ</text>')
add('</g>')

# спрей
add(f'<g class="spray" opacity="0"><path d="M 600 282 q 90 -26 150 -60" stroke="#e88a9a" stroke-width="16" opacity="0.55" stroke-linecap="round"/>'
    f'<path d="M 600 282 q 110 6 170 -14" stroke="#e88a9a" stroke-width="12" opacity="0.45" stroke-linecap="round"/></g>')

# сетка иконок 3×4
POS = []
for row in range(4):
    for col in range(3):
        POS.append((200 + col * 340, 910 + row * 236))

for i, (cx, cy) in enumerate(POS, start=1):
    add(circle_icon(i, cx, cy))
    add(icon_art(i, cx, cy))
    add(num_badge(i, cx - 58, cy - 58, 22))
    l1, l2 = CAPS[i - 1]
    add(f'<text class="cap{i}" opacity="0" x="{cx}" y="{cy+102}" font-family="Nunito" font-size="22" font-weight="900" '
        f'fill="{BLUE_D}" text-anchor="middle">{l1}</text>')
    add(f'<text class="cap{i}" opacity="0" x="{cx}" y="{cy+128}" font-family="Nunito" font-size="19" font-weight="700" '
        f'fill="#5a6a7a" text-anchor="middle">{l2}</text>')

# нижняя лента
add(f'<g class="botBand" opacity="0"><path d="M 40 1770 L 1040 1770 L 1010 1860 L 70 1860 Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>'
    f'<path d="M 20 1740 L 1060 1740 L 1040 1776 L 40 1776 Z" fill="#a51f1f"/>'
    f'<text x="540" y="1826" font-family="Nunito" font-size="34" font-weight="900" fill="#ffffff" text-anchor="middle">НЕЗАМЕНИМЫЙ ПОМОЩНИК В КАЖДОМ ДОМЕ</text></g>')

svg = f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'

# ---------------------------------------------------------------- таймлайн
lines = []
lines.append('gsap.set(".can", {y:60});')
lines.append('tl.to(".can", {opacity:1, y:0, duration:0.8, ease:"power2.out"}, 0.2);')
lines.append('tl.to(".topBand", {y:0, duration:0.5}, 0);')
lines.append('tl.to(".spray", {opacity:1, duration:0.4}, 0.9);')
lines.append('tl.to(".spray", {opacity:0.35, duration:0.5, yoyo:true, repeat:3}, 1.2);')

for i, t in enumerate(ICON_T, start=1):
    lines.append(f'tl.to(".ic{i}", {{opacity:1, duration:0.3}}, {t-0.15:.2f});')
    lines.append(f'tl.fromTo(".art{i}", {{opacity:0, scale:0.6, transformOrigin:"50% 50%"}}, {{opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}}, {t-0.05:.2f});')
    lines.append(f'tl.to(".nb{i}", {{opacity:1, duration:0.25}}, {t-0.1:.2f});')
    lines.append(f'tl.to(".cap{i}", {{opacity:1, duration:0.3}}, {t+0.05:.2f});')

lines.append(f'tl.to(".botBand", {{opacity:1, duration:0.5}}, {OUTRO_T-0.2:.2f});')
lines.append(f'tl.fromTo(".world", {{scale:1.0}}, {{scale:1.02, duration:{TOTAL}, ease:"none"}}, 0);')

html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.world{{position:absolute;inset:0;width:100%;height:100%}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{svg}
<script>
const tl = gsap.timeline({{paused:true}});
window.__timelines = {{}};
{chr(10).join(lines)}
window.__timelines["main"] = tl;
</script>
</div></body></html>"""

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
