#!/usr/bin/env python3
"""«Дождевая вода» — 9:16, разрез участка, 8 битов."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/rainwater")
T = json.load(open(ROOT / "timings.json"))
ST = T["starts"]
TOTAL = T["total"]

INK = "#3a3128"
SKY1 = "#bfe3f2"
SKY2 = "#e8f5fb"
GRASS = "#7fa64f"
GRASS_D = "#5f8438"
SOIL = "#8a5a34"
SOIL_D = "#6b4426"
SOIL_L = "#a06c3f"
ROOF = "#6b7f88"
WALL = "#e8dcc4"
WATER = "#4aa3d8"
WATER_D = "#2f7fae"
CONC = "#cfd3d6"
CONC_D = "#a9b0b4"
GREEN = "#5f8f3f"
GREEN_D = "#47702c"
WHITE = "#ffffff"
CAP = "#f7f5ef"

parts = []


def add(s):
    parts.append(s)


def txt(x, y, s, size=44, col=INK, anchor="start", cls="", weight=900, extra=""):
    add(f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
        f'font-weight="{weight}" fill="{col}" text-anchor="{anchor}" {extra}>{s}</text>')


def caption(i, line1, line2=""):
    add(f'<g class="cap cap{i}" opacity="0">'
        f'<rect x="70" y="300" width="940" height="150" rx="18" fill="{CAP}" stroke="{INK}" stroke-width="4" opacity="0.96"/>'
        f'<text x="540" y="368" font-family="Nunito, Arial" font-size="42" font-weight="900" fill="{INK}" text-anchor="middle">{line1}</text>'
        + (f'<text x="540" y="420" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="#5b5045" '
           f'text-anchor="middle">{line2}</text>' if line2 else "") +
        '</g>')


# ---------------------------------------------------------------- фон
add('<defs>'
    '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{SKY1}"/><stop offset="1" stop-color="{SKY2}"/></linearGradient>'
    '<linearGradient id="soilG" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{SOIL_L}"/><stop offset="0.35" stop-color="{SOIL}"/>'
    f'<stop offset="1" stop-color="{SOIL_D}"/></linearGradient>'
    '<linearGradient id="waterG" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{WATER}"/><stop offset="1" stop-color="{WATER_D}"/></linearGradient>'
    '<clipPath id="tankClip"><rect x="452" y="1102" width="396" height="536" rx="10"/></clipPath>'
    '</defs>')

add(f'<rect width="1080" height="1920" fill="url(#sky)"/>')

# облака
for cx, cy, s, op in ((180, 250, 1.0, 0.9), (760, 180, 0.8, 0.75), (520, 330, 0.6, 0.6)):
    add(f'<g class="cloud" opacity="{op}">'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{110*s}" ry="{44*s}" fill="#ffffff"/>'
        f'<ellipse cx="{cx-70*s}" cy="{cy+14*s}" rx="{70*s}" ry="{34*s}" fill="#ffffff"/>'
        f'<ellipse cx="{cx+78*s}" cy="{cy+12*s}" rx="{66*s}" ry="{30*s}" fill="#ffffff"/></g>')

# ---------------------------------------------------------------- земля
add(f'<rect x="0" y="800" width="1080" height="1120" fill="url(#soilG)"/>')
add(f'<path d="M 0 800 Q 270 786 540 800 Q 810 814 1080 800 L 1080 812 L 0 812 Z" fill="{GRASS_D}"/>')
add(f'<rect x="0" y="780" width="1080" height="34" fill="{GRASS}"/>')
for i in range(26):
    x = 10 + i * 42 + (i % 3) * 6
    add(f'<path d="M {x} 782 q 4 -20 10 -2 M {x+8} 782 q 2 -26 12 -6" stroke="{GRASS_D}" stroke-width="4" fill="none" stroke-linecap="round"/>')

# камушки в грунте
r = random.Random(5)
for i in range(90):
    x = r.uniform(0, 1080)
    y = r.uniform(830, 1900)
    if 430 < x < 900 and 1060 < y < 1680:
        continue
    add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3,9):.1f}" ry="{r.uniform(2,6):.1f}" '
        f'fill="{"#b98a5e" if i%2 else "#5d3d24"}" opacity="{r.uniform(0.25,0.5):.2f}"/>')

# ---------------------------------------------------------------- дом
add(f'<g class="house">')
add(f'<rect x="90" y="520" width="360" height="262" fill="{WALL}" stroke="{INK}" stroke-width="5"/>')
add(f'<path d="M 70 522 L 270 400 L 470 522 Z" fill="{ROOF}" stroke="{INK}" stroke-width="5"/>')
add(f'<path d="M 84 522 L 270 412 L 456 522" fill="none" stroke="#4d5f68" stroke-width="4"/>')
# окно и дверь
add(f'<rect x="140" y="580" width="86" height="80" fill="#bcd8e2" stroke="{INK}" stroke-width="4"/>')
add(f'<path d="M 183 580 l 0 80 M 140 620 l 86 0" stroke="{INK}" stroke-width="3"/>')
add(f'<rect x="330" y="600" width="72" height="182" fill="#8a5a34" stroke="{INK}" stroke-width="4"/>')
add(f'<circle cx="392" cy="694" r="4" fill="{INK}"/>')
# труба на крыше
add(f'<rect x="380" y="420" width="26" height="70" fill="#9a6a44" stroke="{INK}" stroke-width="4"/>')
add(f'</g>')

# водосточный жёлоб
add(f'<path d="M 70 520 L 470 520 L 470 544 L 70 544 Z" fill="{CONC}" stroke="{INK}" stroke-width="4"/>')
add(f'<path d="M 80 536 L 460 536" stroke="{WATER_D}" stroke-width="6" opacity="0.6"/>')

# ---------------------------------------------------------------- фильтр
add(f'<g class="filter">')
add(f'<rect x="452" y="560" width="96" height="104" rx="8" fill="{CONC}" stroke="{INK}" stroke-width="5"/>')
add(f'<rect x="464" y="574" width="72" height="76" rx="4" fill="#9fb0b8" stroke="{INK}" stroke-width="3"/>')
for i in range(5):
    add(f'<path d="M 468 {582 + i*15} l 64 0" stroke="#6f7f88" stroke-width="4"/>')
# листья сверху
add(f'<path class="leaves" d="M 470 566 q 16 -16 30 -2 q -12 14 -30 2 z" fill="{GREEN}" stroke="{INK}" stroke-width="2"/>')
add(f'<path class="leaves" d="M 508 560 q 18 -10 28 6 q -16 10 -28 -6 z" fill="{GREEN_D}" stroke="{INK}" stroke-width="2"/>')
add(f'</g>')

# ---------------------------------------------------------------- труба вниз
add(f'<path class="pipe path" d="M 500 664 L 500 706 L 560 760 L 560 1070" fill="none" stroke="{CONC_D}" stroke-width="22" stroke-linejoin="round"/>')
add(f'<path d="M 500 664 L 500 706 L 560 760 L 560 1070" fill="none" stroke="#8b9499" stroke-width="12" stroke-linejoin="round" opacity="0.7"/>')

# первичный сброс
add(f'<g class="flush">')
add(f'<path d="M 560 800 L 690 830 L 690 890" fill="none" stroke="{CONC_D}" stroke-width="18" stroke-linejoin="round"/>')
add(f'<circle cx="690" cy="902" r="15" fill="{WATER}" stroke="{INK}" stroke-width="4" opacity="0.9"/>')
add(f'<path d="M 679 916 q 5 22 11 0" stroke="{WATER_D}" stroke-width="5" fill="none"/>')
add(f'</g>')

# ---------------------------------------------------------------- ёмкость
add(f'<g class="tankG">')
add(f'<rect x="430" y="1080" width="440" height="580" rx="16" fill="{CONC}" stroke="{INK}" stroke-width="6"/>')
add(f'<rect x="452" y="1102" width="396" height="536" rx="10" fill="#dfe4e6" stroke="{INK}" stroke-width="4"/>')
add(f'<g clip-path="url(#tankClip)"><rect class="waterLvl" x="452" y="1638" width="396" height="0" fill="url(#waterG)"/>'
    f'<rect class="waterLvl" x="452" y="1638" width="396" height="0" fill="{WATER}" opacity="0.25"/></g>')
# крышка
add(f'<ellipse cx="650" cy="1082" rx="120" ry="26" fill="{CONC_D}" stroke="{INK}" stroke-width="5"/>')
add(f'<path d="M 570 1082 q 80 -14 160 0" stroke="#7f878b" stroke-width="4" fill="none"/>')
add(f'</g>')

# насос
add(f'<g class="pump">')
add(f'<rect x="600" y="1480" width="64" height="130" rx="18" fill="#8b9499" stroke="{INK}" stroke-width="5"/>')
add(f'<rect x="616" y="1500" width="32" height="60" rx="8" fill="#5f6b70" stroke="{INK}" stroke-width="3"/>')
add(f'<path d="M 632 1480 L 632 1108" stroke="#6f7a80" stroke-width="12"/>')
add(f'<path d="M 632 1108 L 632 760 L 880 760" stroke="#6f7a80" stroke-width="12" fill="none" stroke-linejoin="round"/>')
add('</g>')

# ---------------------------------------------------------------- грядка и дождеватель
add(f'<g class="garden">')
add(f'<rect x="840" y="690" width="175" height="92" rx="10" fill="#8a5a34" stroke="{INK}" stroke-width="5"/>')
add(f'<path d="M 840 700 q 88 -16 175 0" stroke="{GREEN_D}" stroke-width="8" fill="none"/>')
for i, x in enumerate((870, 906, 942, 978)):
    add(f'<path d="M {x} 700 q 3 -46 6 -6" stroke="{GREEN}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    add(f'<circle cx="{x+4}" cy="676" r="11" fill="{GREEN}" stroke="{GREEN_D}" stroke-width="3"/>')
add(f'<path d="M 880 760 L 880 726" stroke="#6f7a80" stroke-width="10"/>')
add(f'<path d="M 880 726 q 36 -18 56 8" stroke="#6f7a80" stroke-width="9" fill="none"/>')
add('</g>')

# брызги
for i in range(9):
    add(f'<circle class="sprayS" cx="{886 + (i%3)*22}" cy="{716 + (i//3)*10}" r="4" fill="{WATER}" opacity="0"/>')

# дождь
for i in range(40):
    x = r.uniform(-20, 1100)
    y = r.uniform(-200, 700)
    add(f'<line class="rain" x1="{x:.0f}" y1="{y:.0f}" x2="{x-6:.0f}" y2="{y+26:.0f}" stroke="#8fcbe6" stroke-width="3" opacity="0.75"/>')

# капли по жёлобу и трубе
for i in range(7):
    add(f'<circle class="flow" cx="0" cy="0" r="7" fill="{WATER}" opacity="0"/>')

# ---------------------------------------------------------------- подписи
caption(1, "Дождь прошёл — вода ушла в землю", "а её можно сохранить")
caption(2, "Фильтр задерживает листья и песок")
caption(3, "По трубе — в подземную ёмкость")
caption(4, "Ёмкость наполняется")
caption(5, "Первые грязные литры — в дренаж")
caption(6, "Нужен полив — включается насос")
caption(7, "Вода идёт к грядкам")
caption(8, "Дождь сегодня — полив завтра")

# бейдж экономии
add(f'<g class="badge" opacity="0">'
    f'<rect x="640" y="880" width="330" height="96" rx="16" fill="#f2f8ec" stroke="{GREEN_D}" stroke-width="4"/>'
    f'<text x="805" y="926" font-family="Nunito" font-size="26" font-weight="800" fill="#4a6b3a" text-anchor="middle">ЭКОНОМИЯ ВОДЫ</text>'
    f'<text x="805" y="966" font-family="Nunito" font-size="30" font-weight="900" fill="{GREEN_D}" text-anchor="middle">до 50% полива</text></g>')

svg = (f'<svg class="world" viewBox="40 250 1000 1778" xmlns="http://www.w3.org/2000/svg">'
       f'{"".join(parts)}</svg>')

JS = """
const tl = gsap.timeline({paused:true});
window.__timelines = {};

gsap.utils.toArray(".rain").forEach((el,i)=>{
  tl.fromTo(el, {y:-140, opacity:0.9}, {y:560, opacity:0.35, duration:0.8+Math.random()*0.5,
    repeat:-1, ease:"none", delay:Math.random()*0.9}, 0);
});

tl.to(".cap1", {opacity:1, duration:0.3}, 0.05);
tl.to(".cap1", {opacity:0, duration:0.15}, 4.40);
tl.to(".cap2", {opacity:1, duration:0.3}, 4.45);
tl.to(".cap2", {opacity:0, duration:0.15}, 8.33);
tl.to(".cap3", {opacity:1, duration:0.3}, 8.38);
tl.to(".cap3", {opacity:0, duration:0.15}, 10.69);
tl.to(".cap4", {opacity:1, duration:0.3}, 10.74);
tl.to(".cap4", {opacity:0, duration:0.15}, 13.44);
tl.to(".cap5", {opacity:1, duration:0.3}, 13.49);
tl.to(".cap5", {opacity:0, duration:0.15}, 16.87);
tl.to(".cap6", {opacity:1, duration:0.3}, 16.92);
tl.to(".cap6", {opacity:0, duration:0.15}, 19.67);
tl.to(".cap7", {opacity:1, duration:0.3}, 19.72);
tl.to(".cap7", {opacity:0, duration:0.15}, 22.32);
tl.to(".cap8", {opacity:1, duration:0.3}, 22.37);

gsap.utils.toArray(".flow").forEach((el,i)=>{
  const t0 = 2.2 + i*0.28;
  tl.set(el, {opacity:1, x:500, y:664}, t0);
  tl.to(el, {y:706, duration:0.5, ease:"none"}, t0);
  tl.to(el, {x:560, y:760, duration:0.6, ease:"none"}, t0+0.5);
  tl.to(el, {y:1070, duration:1.6, ease:"none"}, t0+1.1);
  tl.to(el, {opacity:0, duration:0.15}, t0+2.7);
  tl.set(el, {opacity:0}, t0+2.96);
});

tl.set(".waterLvl", {attr:{y:1638, height:0}}, 0);
tl.to(".waterLvl", {attr:{y:1150, height:488}, duration:9.0, ease:"none"}, 9.0);

tl.to(".filter", {scale:1.06, transformOrigin:"50% 50%", duration:0.5, yoyo:true, repeat:3}, 4.6);

tl.fromTo(".flush", {opacity:0.25}, {opacity:1, duration:0.5}, 13.6);
tl.to(".flush", {opacity:0.3, duration:0.6, yoyo:true, repeat:4}, 14.0);

tl.fromTo(".pump", {opacity:0.6}, {opacity:1, duration:0.5}, 17.0);
tl.to(".pump", {scale:1.04, transformOrigin:"50% 60%", duration:0.4, yoyo:true, repeat:5}, 17.0);

tl.to(".sprayS", {opacity:0.9, y:-16, duration:0.5, stagger:0.05, yoyo:true, repeat:8}, 19.9);

tl.to(".badge", {opacity:1, duration:0.6}, 23.2);

tl.fromTo(".world", {scale:1.0}, {scale:1.035, duration:26.49, ease:"none"}, 0);
window.__timelines["main"] = tl;
"""

html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/MotionPathPlugin.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.world{{position:absolute;inset:0;width:100%;height:100%}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{svg}
<script>{JS.replace('{S}', str(ST))}
</script>
</div></body></html>"""

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
