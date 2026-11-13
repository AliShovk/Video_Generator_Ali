#!/usr/bin/env python3
"""«Купель с термосифоном» — 10 сцен, объёмная иллюстрация."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/thermo")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG1 = "#eef4f8"
BG2 = "#dfe9f0"
INK = "#33404a"
WOOD = "#c08a52"
WOOD_D = "#9a6a3a"
WOOD_L = "#d8a86e"
HOOP = "#9aa4ab"
STEEL = "#b9c3c9"
STEEL_D = "#8b959b"
WATER = "#7fb8d4"
WATER_D = "#4f8fae"
HOT = "#d2603a"
FIRE = "#f0a13a"
FIRE2 = "#e06a2a"
LABEL = "#3a4650"

parts = []


def add(s):
    parts.append(s)


def txt(x, y, s, size=34, col=LABEL, anchor="start", cls="", weight=800):
    add(f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{weight}" '
        f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def grain(n=120, seed=3):
    r = random.Random(seed)
    for _ in range(n):
        add(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.5,1.4):.1f}" '
            f'fill="#9fb0bb" opacity="{r.uniform(0.03,0.08):.2f}"/>')


# ---------------------------------------------------------------- фон
add('<defs>'
    '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>'
    '<linearGradient id="wood" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{WOOD_D}"/><stop offset="0.35" stop-color="{WOOD_L}"/>'
    f'<stop offset="1" stop-color="{WOOD_D}"/></linearGradient>'
    '<linearGradient id="waterG" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="#a9d4e6"/><stop offset="1" stop-color="{WATER_D}"/></linearGradient>'
    '<linearGradient id="steel" x1="0" y1="0" x2="1" y2="0">'
    f'<stop offset="0" stop-color="{STEEL_D}"/><stop offset="0.4" stop-color="#e2e8ea"/>'
    f'<stop offset="1" stop-color="{STEEL_D}"/></linearGradient>'
    '<radialGradient id="fireG"><stop offset="0" stop-color="#ffd27a"/><stop offset="1" stop-color="#e0631f"/></radialGradient>'
    '</defs>')
add(f'<rect width="1080" height="1920" fill="url(#bg)"/>')
grain()

# пол
add(f'<ellipse cx="540" cy="1500" rx="470" ry="90" fill="#c9d6de" opacity="0.55"/>')

# ---------------------------------------------------------------- бочка
TUB_CX, TUB_CY, TUB_RX, TUB_RY = 420, 980, 290, 86
add(f'<g class="tub">')
add(f'<path d="M {TUB_CX-TUB_RX} {TUB_CY} L {TUB_CX-TUB_RX*0.92} 1330 Q {TUB_CX} 1390 {TUB_CX+TUB_RX*0.92} 1330 '
    f'L {TUB_CX+TUB_RX} {TUB_CY} Z" fill="url(#wood)" stroke="{INK}" stroke-width="4"/>')
# клёпки
for i in range(18):
    a = math.pi * (i / 17)
    x = TUB_CX - TUB_RX * math.cos(a)
    add(f'<path d="M {x:.0f} {TUB_CY+4} L {TUB_CX + (x-TUB_CX)*0.93:.0f} 1336" stroke="#8a5a30" stroke-width="2.5" opacity="0.5"/>')
# обручи
for yy, w in ((1080, 1.0), (1190, 0.97), (1290, 0.94)):
    add(f'<path d="M {TUB_CX-TUB_RX*w:.0f} {yy} Q {TUB_CX} {yy+34} {TUB_CX+TUB_RX*w:.0f} {yy}" '
        f'stroke="{HOOP}" stroke-width="12" fill="none"/>')
# верхний обрез
add(f'<ellipse cx="{TUB_CX}" cy="{TUB_CY}" rx="{TUB_RX}" ry="{TUB_RY}" fill="#8a5a34" stroke="{INK}" stroke-width="5"/>')
# вода
add(f'<ellipse class="waterTop" cx="{TUB_CX}" cy="{TUB_CY+10}" rx="{TUB_RX-18}" ry="{TUB_RY-10}" fill="url(#waterG)"/>')
# разрез: внутренняя стенка
add(f'<path d="M {TUB_CX+TUB_RX-18} {TUB_CY+8} L {TUB_CX+TUB_RX-34} 1290" stroke="#6b4426" stroke-width="3" opacity="0.5"/>')
add('</g>')

# стрелки тёплой воды внутри
for i, x in enumerate((300, 400, 500)):
    add(f'<path class="hotArrow" d="M {x} 1180 L {x} 1030" stroke="{HOT}" stroke-width="10" opacity="0.85"/>')
    add(f'<path d="M {x} 1000 l -14 26 l 28 0 z" fill="{HOT}" opacity="0.85"/>')

# пар
for i in range(5):
    add(f'<path class="steam" d="M {300+i*60} {TUB_CY-20} q -14 -40 4 -70 q 16 -30 0 -60" stroke="#ffffff" '
        f'stroke-width="7" fill="none" opacity="0.55"/>')

# ---------------------------------------------------------------- топка и змеевик
FX, FY = 850, 1230
add(f'<g class="stove">')
add(f'<path d="M 760 1300 L 760 1120 Q 760 1080 800 1080 L 900 1080 Q 940 1080 940 1120 L 940 1300 Z" '
    f'fill="#5f6a72" stroke="{INK}" stroke-width="4" opacity="0.35"/>')
# змеевик
for i in range(6):
    yy = 1100 + i * 34
    add(f'<ellipse class="coil" cx="850" cy="{yy}" rx="{70 - i*3}" ry="18" fill="none" stroke="url(#steel)" stroke-width="11"/>')
add(f'<path d="M 850 1090 L 850 1020" stroke="url(#steel)" stroke-width="12"/>')
add(f'<path d="M 780 1320 L 780 1360" stroke="url(#steel)" stroke-width="11"/>')
# топка
add(f'<path d="M 740 1340 L 960 1340 L 940 1470 L 760 1470 Z" fill="#3f4a52" stroke="{INK}" stroke-width="4"/>')
add(f'<path d="M 760 1340 L 760 1320 L 940 1320 L 940 1340" fill="none" stroke="{INK}" stroke-width="4"/>')
add('</g>')

# огонь
for i in range(7):
    x = 790 + i * 24
    add(f'<path class="flame" d="M {x} 1420 q -16 -50 8 -84 q 4 30 18 44 q 12 -22 10 -40 q 20 34 2 80 z" '
        f'fill="url(#fireG)" opacity="0.95"/>')
add(f'<ellipse class="glow" cx="850" cy="1400" rx="130" ry="70" fill="{FIRE}" opacity="0.22"/>')

# ---------------------------------------------------------------- трубы
# верхняя: змеевик -> бочка
add(f'<path class="pipeHot" d="M 850 1100 L 850 900 Q 850 860 810 860 L 640 860 Q 600 860 600 900 L 600 1020" '
    f'fill="none" stroke="url(#steel)" stroke-width="20" stroke-linejoin="round"/>')
add(f'<path d="M 850 1100 L 850 900 Q 850 860 810 860 L 640 860 Q 600 860 600 900 L 600 1020" '
    f'fill="none" stroke="{HOT}" stroke-width="7" opacity="0.55"/>')
# нижняя: бочка -> змеевик
add(f'<path class="pipeCold" d="M 600 1250 L 600 1400 Q 600 1440 640 1440 L 780 1440 L 780 1360" '
    f'fill="none" stroke="url(#steel)" stroke-width="20" stroke-linejoin="round"/>')
add(f'<path d="M 600 1250 L 600 1400 Q 600 1440 640 1440 L 780 1440 L 780 1360" '
    f'fill="none" stroke="{WATER}" stroke-width="7" opacity="0.6"/>')

# бегущие капли по контуру
for i in range(6):
    add(f'<circle class="flow" cx="0" cy="0" r="6" fill="{HOT}" opacity="0"/>')

# ---------------------------------------------------------------- подписи
def callout(x1, y1, x2, y2, text, size=26, anchor="start"):
    add(f'<path d="M {x1} {y1} L {x2} {y2}" stroke="{LABEL}" stroke-width="2" opacity="0.8"/>')
    add(f'<circle cx="{x1}" cy="{y1}" r="5" fill="{LABEL}"/>')
    add(f'<text class="lbl" x="{x2 + (10 if anchor=="start" else -10)}" y="{y2+8}" font-family="Nunito, Arial" '
        f'font-size="{size}" font-weight="800" fill="{LABEL}" text-anchor="{anchor}">{text}</text>')


callout(180, 960, 60, 880, "ДЕРЕВЯННАЯ КУПЕЛЬ", 24)
callout(720, 862, 1010, 800, "ВЕРХНЯЯ ТРУБА", 24, "end")
callout(900, 1120, 1015, 1090, "ЗМЕЕВИК", 24, "end")
callout(600, 1300, 430, 1330, "НИЖНЯЯ ТРУБА", 24)
callout(860, 1452, 980, 1520, "ОГОНЬ", 24, "end")
txt(300, 1210, "холодная вода", 22, "#3f6b80")
txt(330, 1120, "тёплая — вверх", 22, HOT)

# ---------------------------------------------------------------- заголовок и плашки
txt(60, 170, "КУПЕЛЬ БЕЗ НАСОСА", 52, INK)
txt(60, 224, "термосифон: вода идёт сама", 26, "#5a6a75")

add(f'<g class="badge" opacity="0"><rect x="620" y="1660" width="400" height="106" rx="18" fill="#fdf3e6" stroke="{HOT}" stroke-width="4"/>'
    f'<text x="820" y="1710" font-family="Nunito" font-size="26" font-weight="800" fill="#8a4a2a" text-anchor="middle">БЕЗ ЭЛЕКТРИЧЕСТВА</text>'
    f'<text x="820" y="1748" font-family="Nunito" font-size="30" font-weight="900" fill="{HOT}" text-anchor="middle">только огонь и вода</text></g>')

add(f'<g class="warn" opacity="0"><rect x="70" y="1790" width="940" height="70" rx="14" fill="#fdecea" stroke="#c0392b" stroke-width="3"/>'
    f'<text x="540" y="1836" font-family="Nunito" font-size="26" font-weight="800" fill="#8a2a1e" text-anchor="middle">'
    f'ВЕНТИЛЯЦИЯ ТОПКИ ОБЯЗАТЕЛЬНА — УГАРНЫЙ ГАЗ</text></g>')

SCENES = list(range(10))
svg = (f'<svg class="world" viewBox="20 130 1040 1849" xmlns="http://www.w3.org/2000/svg">'
       f'{"".join(parts)}</svg>')

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

// огонь
gsap.utils.toArray(".flame").forEach((el,i)=>{{
  tl.to(el, {{scaleY:1.15+Math.random()*0.2, scaleX:0.92, transformOrigin:"50% 100%",
    duration:0.24+Math.random()*0.18, yoyo:true, repeat:-1, ease:"sine.inOut"}}, i*0.05);
}});
tl.to(".glow", {{opacity:0.38, duration:0.8, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 0);

// пар
gsap.utils.toArray(".steam").forEach((el,i)=>{{
  tl.fromTo(el, {{opacity:0.1, y:10}}, {{opacity:0.6, y:-40, duration:2.4+Math.random(), repeat:-1,
    yoyo:true, ease:"sine.inOut"}}, i*0.3);
}});

// вода в бочке колышется
tl.to(".waterTop", {{scaleX:1.012, scaleY:1.03, transformOrigin:"50% 50%", duration:2.2, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 0);

// стрелки тепла поднимаются
gsap.utils.toArray(".hotArrow").forEach((el,i)=>{{
  tl.fromTo(el, {{opacity:0.15, y:40}}, {{opacity:0.95, y:0, duration:1.4, repeat:-1, ease:"sine.out"}}, i*0.35);
}});

// капли бегут по контуру: вверх по горячей, вниз по холодной
const hotPath = {{x:850,y:1100}};
gsap.utils.toArray(".flow").forEach((el,i)=>{{
  tl.set(el, {{opacity:1, x:850, y:1100}}, 1.0+i*0.45);
  tl.to(el, {{y:900, duration:0.45}}, 1.0+i*0.45);
  tl.to(el, {{x:810, y:860, duration:0.3}}, 1.45+i*0.45);
  tl.to(el, {{x:640, duration:0.7}}, 1.75+i*0.45);
  tl.to(el, {{x:600, y:900, duration:0.3}}, 2.45+i*0.45);
  tl.to(el, {{y:960, duration:0.3, opacity:0}}, 2.75+i*0.45);
  tl.set(el, {{opacity:0}}, 3.05+i*0.45);
}});

// змеевик пульсирует
tl.to(".coil", {{strokeWidth:13, duration:0.7, stagger:0.08, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 0);

// заголовок
tl.fromTo(".lbl", {{opacity:0}}, {{opacity:1, duration:0.6, stagger:0.25}}, 0.4);
tl.to(".badge", {{opacity:1, duration:0.6}}, 4.0);
tl.to(".warn", {{opacity:1, duration:0.6}}, 24.0);

tl.fromTo(".world", {{scale:1.0}}, {{scale:1.035, duration:{TOTAL}, ease:"none"}}, 0);
window.__timelines["main"] = tl;
</script>
</div></body></html>"""

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
