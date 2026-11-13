#!/usr/bin/env python3
"""«Что делает сантехник?» — постер-видео 25,4 с + концовка."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/plumber")
T = json.load(open(ROOT / "timings.json"))
GRID = T["grid"]
FLOW_T = T["flow"]
TOTAL = T["total"] + 4.63

BG = "#e9f3fa"
INK = "#1f3446"
BLUE = "#1f6bb5"
CREAM = "#fffdf7"
GREEN = "#4caf50"
ORANGE = "#ef8f1f"
SKY = "#2e86c1"
PURPLE = "#8e44ad"
RED = "#e2652a"
TEAL = "#16a085"
YELLOW = "#f4c95a"

parts = []


def add(s):
    parts.append(s)


def txt(x, y, s, size=34, col=INK, anchor="start", weight=900, cls="", family="Nunito, Arial"):
    add(f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def card(i, x, y, col, num, title, lines, w=490, h=252):
    add(f'<g class="card card{i}" opacity="0">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{CREAM}" stroke="{col}" stroke-width="5"/>'
        f'<path d="M {x+20} {y} L {x+w-20} {y} Q {x+w} {y} {x+w} {y+20} L {x+w} {y+58} L {x} {y+58} L {x} {y+20} '
        f'Q {x} {y} {x+20} {y} Z" fill="{col}"/>'
        f'<circle cx="{x+40}" cy="{y+29}" r="19" fill="#ffffff"/>'
        f'<text x="{x+40}" y="{y+37}" font-family="Nunito" font-size="24" font-weight="900" fill="{col}" '
        f'text-anchor="middle">{num}</text>'
        f'<text x="{x+70}" y="{y+38}" font-family="Nunito" font-size="25" font-weight="900" fill="#ffffff">{title}</text>'
        + "".join(f'<text x="{x+22}" y="{y+92+k*30}" font-family="Nunito" font-size="20" font-weight="700" '
                  f'fill="{INK}">{line}</text>' for k, line in enumerate(lines))
        + '</g>')


def icon1(cx, cy):
    return (f'<g class="ic ic1" opacity="0"><path d="M {cx-46} {cy} l 92 0 M {cx-46} {cy} l 0 46" stroke="#9aa7ae" '
            f'stroke-width="16" stroke-linecap="round"/>'
            f'<circle cx="{cx+26}" cy="{cy+22}" r="26" fill="#dff0fb" stroke="{BLUE}" stroke-width="7"/>'
            f'<path d="M {cx+44} {cy+40} l 26 26" stroke="{BLUE}" stroke-width="10" stroke-linecap="round"/></g>')


def icon2(cx, cy):
    return (f'<g class="ic ic2" opacity="0"><path d="M {cx-10} {cy-40} l 0 26 q 0 14 -18 14 l -22 0" stroke="#9aa7ae" '
            f'stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<path d="M {cx-52} {cy} l 0 12" stroke="#63b3e8" stroke-width="10"/>'
            f'<path class="drop2" d="M {cx-52} {cy+30} q 10 16 0 24 q -10 -8 0 -24 z" fill="#4aa3e0"/></g>')


def icon3(cx, cy):
    return (f'<g class="ic ic3" opacity="0"><path d="M {cx-44} {cy+20} l 88 0" stroke="#9aa7ae" stroke-width="18" stroke-linecap="round"/>'
            f'<path d="M {cx-20} {cy-34} l 40 40" stroke="#7a8b95" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M {cx+4} {cy-34} l 14 -12 l 14 14 l -14 12 z" fill="#b9c3c9" stroke="{INK}" stroke-width="3"/>'
            f'<ellipse class="puddle" cx="{cx+30}" cy="{cy+44}" rx="30" ry="9" fill="#8fd0ee" opacity="0.8"/></g>')


def icon4(cx, cy):
    return (f'<g class="ic ic4" opacity="0"><rect x="{cx-42}" y="{cy-46}" width="84" height="92" rx="12" fill="#e6eef3" '
            f'stroke="{INK}" stroke-width="4"/>'
            f'<circle cx="{cx}" cy="{cy-16}" r="16" fill="#ffffff" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {cx-16} {cy+34} l 32 0" stroke="{RED}" stroke-width="8"/></g>')


def icon5(cx, cy):
    return (f'<g class="ic ic5" opacity="0"><path d="M {cx-48} {cy} l 40 0 M {cx+8} {cy} l 40 0" stroke="#9aa7ae" '
            f'stroke-width="16" stroke-linecap="round"/>'
            f'<rect x="{cx-8}" y="{cy-20}" width="16" height="40" fill="#b9c3c9" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {cx-8} {cy-20} l 16 0 M {cx-8} {cy+20} l 16 0" stroke="{INK}" stroke-width="5"/></g>')


def icon6(cx, cy):
    return (f'<g class="ic ic6" opacity="0"><circle cx="{cx}" cy="{cy}" r="42" fill="#e8f5e9" stroke="{GREEN}" stroke-width="5"/>'
            f'<path d="M {cx-20} {cy} l 14 16 l 28 -34" stroke="{GREEN}" stroke-width="10" fill="none" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')


# ---------------------------------------------------------------- фон
add(f'<rect width="1080" height="1920" fill="{BG}"/>')
for i in range(14):
    x = 40 + (i * 97) % 1000
    y = 120 + (i * 137) % 1500
    add(f'<circle cx="{x}" cy="{y}" r="{8 + (i % 3) * 6}" fill="#d3e8f5" opacity="0.7"/>')

# ---------------------------------------------------------------- шапка
add(f'<g class="headG">')
add(f'<path d="M 40 60 L 1040 60 L 1010 210 L 70 210 Z" fill="{BLUE}"/>')
add(f'<path d="M 20 40 L 1060 40 L 1040 76 L 40 76 Z" fill="#2a7fc4"/>')
add(f'<text x="60" y="122" font-family="Nunito" font-size="52" font-weight="900" fill="#ffffff">ЧТО ДЕЛАЕТ</text>')
add(f'<text x="60" y="186" font-family="Nunito" font-size="62" font-weight="900" fill="{YELLOW}">САНТЕХНИК?</text>')
# маскот
add(f'<g class="mascot">'
    f'<circle cx="915" cy="146" r="62" fill="#f6c9a0" stroke="{INK}" stroke-width="4"/>'
    f'<circle cx="853" cy="150" r="12" fill="#f6c9a0" stroke="{INK}" stroke-width="3"/>'
    f'<circle cx="977" cy="150" r="12" fill="#f6c9a0" stroke="{INK}" stroke-width="3"/>'
    f'<path d="M 855 120 q 0 -52 60 -52 q 60 0 60 52 l 0 8 l -120 0 z" fill="{BLUE}" stroke="{INK}" stroke-width="4"/>'
    f'<path d="M 846 128 q 69 -16 138 0 l 0 12 q -69 -16 -138 0 z" fill="#174f86" stroke="{INK}" stroke-width="3"/>'
    f'<circle cx="893" cy="142" r="5.5" fill="{INK}"/><circle cx="937" cy="142" r="5.5" fill="{INK}"/>'
    f'<path d="M 895 172 q 20 16 40 0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>'
    f'<path d="M 862 208 q 53 22 106 0 l 0 30 l -106 0 z" fill="{BLUE}"/>')
add('</g>')
txt(60, 262, "Делает дом удобным и безопасным. Вот что он умеет.", 24, "#4a6070")

# ---------------------------------------------------------------- карточки
C = [(GREEN, "1", "ИЩЕТ НЕИСПРАВНОСТЬ", ["Осматривает трубы и", "сантехнику: что и", "почему сломалось."]),
     (ORANGE, "2", "РЕМОНТИРУЕТ КРАНЫ", ["Меняет прокладки,", "картриджи и кран-", "буксы."]),
     (SKY, "3", "УСТРАНЯЕТ ПРОТЕЧКИ", ["Находит место течи", "и заделывает его", "герметиком."]),
     (PURPLE, "4", "СТАВИТ ОБОРУДОВАНИЕ", ["Раковины, душевые,", "бойлеры, фильтры", "и новую технику."]),
     (RED, "5", "СОЕДИНЯЕТ ТРУБЫ", ["Фитинги, резьба и", "герметик — чтобы", "вода шла куда надо."]),
     (TEAL, "6", "ПРОВЕРЯЕТ РЕЗУЛЬТАТ", ["Всё работает, вода", "не капает, стыки", "сухие."])]
POS = [(40, 300), (550, 300), (40, 566), (550, 566), (40, 832), (550, 832)]
for i, (col, num, title, lines) in enumerate(C):
    x, y = POS[i]
    card(i + 1, x, y, col, num, title, lines)
    add(f'<g class="cardIcon">' + {1: icon1, 2: icon2, 3: icon3, 4: icon4, 5: icon5, 6: icon6}[i + 1](x + 420, y + 160) + '</g>')

# ---------------------------------------------------------------- схема работы
add(f'<g class="flowG" opacity="0"><rect x="40" y="1112" width="1000" height="330" rx="22" fill="#ffffff" stroke="{BLUE}" stroke-width="4"/>'
    f'<text x="540" y="1170" font-family="Nunito" font-size="32" font-weight="900" fill="{BLUE}" text-anchor="middle">КАК РАБОТАЕТ МАСТЕР?</text></g>')
STEPS = [("ОСМОТРЕЛ", "🔍"), ("НАШЁЛ", "💧"), ("ПОЧИНИЛ", "🔧"), ("ПРОВЕРИЛ", "✓")]
for i, (label, _) in enumerate(STEPS):
    cx = 165 + i * 250
    circles = {0: icon1, 1: icon2, 2: icon3, 3: icon6}[i]
    add(f'<g class="step step{i+1}" opacity="0"><circle cx="{cx}" cy="1280" r="56" fill="#f2f8fc" stroke="{BLUE}" stroke-width="4"/>'
        + circles(cx, 1280).replace('opacity="0"', 'opacity="1"').replace('class="ic ic', 'class="sic ic')
        + f'<text x="{cx}" y="1380" font-family="Nunito" font-size="24" font-weight="900" fill="{INK}" '
          f'text-anchor="middle">{label}</text></g>')
    if i < 3:
        add(f'<path class="stepArrow" d="M {cx+66} 1280 l 62 0 M {cx+112} 1266 l 18 14 l -18 14" stroke="{BLUE}" '
            f'stroke-width="8" fill="none" opacity="0"/>')

# нижняя плашка
add(f'<g class="bottomG" opacity="0"><rect x="40" y="1470" width="1000" height="140" rx="20" fill="#fff6d9" stroke="{YELLOW}" stroke-width="5"/>'
    f'<text x="540" y="1528" font-family="Nunito" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">Хороший мастер работает внимательно</text>'
    f'<text x="540" y="1572" font-family="Nunito" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">и обязательно проверяет результат!</text></g>')

add(f'<g class="sign" opacity="0"><text x="540" y="1680" font-family="Nunito" font-size="20" font-weight="700" '
    f'fill="#5a6a7a" text-anchor="middle">Сантехника · ремонт · обслуживание</text></g>')

svg = f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>'

# ---------------------------------------------------------------- таймлайн
L = []
L.append('tl.to(".headG, .mascot", {opacity:1, y:0, duration:0.6, ease:"power2.out"}, 0.1);')
L.append('tl.to(".card", {opacity:0.22, duration:0.6}, 0.5);')
L.append('tl.to(".flowG, .bottomG", {opacity:0.25, duration:0.6}, 0.5);')
L.append('gsap.from(".headG", {y:-40, duration:0.7, ease:"power2.out"}, 0);')
for i, t in enumerate(GRID, start=1):
    L.append(f'tl.to(".card{i}", {{opacity:1, duration:0.35}}, {t-0.15:.2f});')
    L.append(f'tl.fromTo(".card{i}", {{scale:0.92, transformOrigin:"50% 50%"}}, {{scale:1, duration:0.35, ease:"back.out(2)"}}, {t-0.15:.2f});')
    L.append(f'tl.to(".ic{i}", {{opacity:1, duration:0.3}}, {t+0.05:.2f});')
L.append(f'tl.to(".flowG", {{opacity:1, duration:0.4}}, {FLOW_T-0.2:.2f});')
for i in range(4):
    L.append(f'tl.to(".step{i+1}", {{opacity:1, duration:0.3}}, {FLOW_T + i*0.45:.2f});')
L.append(f'tl.to(".stepArrow", {{opacity:1, duration:0.25, stagger:0.3}}, {FLOW_T+0.5:.2f});')
L.append(f'tl.to(".bottomG", {{opacity:1, duration:0.5}}, {FLOW_T+1.6:.2f});')
L.append(f'tl.to(".sign", {{opacity:1, duration:0.4}}, {FLOW_T+2.0:.2f});')
L.append(f'tl.fromTo(".world", {{scale:1.0}}, {{scale:1.02, duration:{TOTAL}, ease:"none"}}, 0);')

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
{chr(10).join(L)}
window.__timelines["main"] = tl;
</script>
</div></body></html>"""

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
