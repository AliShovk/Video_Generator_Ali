#!/usr/bin/env python3
"""«Рекуператор» — 9 сцен, тёплая инфографика."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/recup")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#f7f1e6"
INK = "#3a3a3a"
WALL = "#e9dfcc"
WALL_D = "#d6c7ac"
WOOD = "#c98a4b"
ROOF = "#7fa05a"
ROOF_D = "#5f7d42"
HOT = "#e0632f"
HOT_L = "#f4a261"
COLD = "#3f8fc4"
COLD_L = "#8fc4e8"
UNIT = "#cfd8dc"
UNIT_D = "#9aa7ae"
OK = "#4f8f4a"
WHITE = "#fdfaf3"


def S(d, w=5, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, cls="fillshape", stroke=INK, sw=5, op=1.0):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=44, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def grain(seed, n=100):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.4):.1f}" '
                   f'fill="#a08a6a" opacity="{r.uniform(0.03,0.07):.2f}"/>' for _ in range(n))


def badge(x, y, text, col, size=40, w=150, h=64):
    return (f'<g class="badgeG"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{WHITE}" '
            f'stroke="{col}" stroke-width="4"/>'
            f'<text x="{x+w/2}" y="{y+h*0.68}" font-family="Nunito" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="middle">{text}</text></g>')


def duct(d, col, w=22, cls="duct"):
    return f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def arrow(x1, y1, x2, y2, col, w=12, cls="arrow"):
    return (f'<path class="{cls}" d="M {x1} {y1} L {x2} {y2}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<path d="M {x2} {y2} l -24 -10 l 4 24 z" fill="{col}"/>')


def house(cut=True, cls="houseG"):
    """Разрез дома: крыша, комната, окно."""
    b = [f'<g class="{cls}">']
    b.append(F("M 80 1040 L 80 560 L 540 360 L 1000 560 L 1000 1040 Z", WALL, "fillshape", INK, 6))
    b.append(F("M 60 570 L 540 340 L 1020 570 L 1000 600 L 540 380 L 80 600 Z", ROOF, "fillshape", INK, 6))
    for i in range(9):
        b.append(f'<path d="M {110+i*105} 590 L {540+i*55} 372" stroke="{ROOF_D}" stroke-width="3" opacity="0.4"/>')
    # внутренняя комната
    if cut:
        b.append(f'<rect x="110" y="600" width="860" height="420" fill="#f6ead6" stroke="{INK}" stroke-width="5"/>')
        b.append(f'<rect x="110" y="1000" width="860" height="46" fill="{WOOD}" stroke="{INK}" stroke-width="4"/>')
        # окно
        b.append(f'<rect x="170" y="660" width="150" height="120" fill="{COLD_L}" stroke="{INK}" stroke-width="5"/>')
        b.append(f'<path d="M 245 660 l 0 120 M 170 720 l 150 0" stroke="{INK}" stroke-width="3"/>')
        # кровать
        b.append(f'<rect x="700" y="880" width="230" height="100" rx="8" fill="#d9c3a0" stroke="{INK}" stroke-width="4"/>')
        # радиатор под окном
        b.append(f'<rect x="180" y="812" width="150" height="86" rx="8" fill="#e8e2d6" stroke="{INK}" stroke-width="4"/>')
        for i in range(6):
            b.append(f'<path d="M {190+i*24} 818 l 0 74" stroke="{INK}" stroke-width="3" opacity="0.6"/>')
        # ковёр
        b.append(f'<ellipse cx="470" cy="960" rx="150" ry="42" fill="#d8c3a0" stroke="{INK}" stroke-width="3" opacity="0.8"/>')
        # торшер
        b.append(f'<path d="M 380 880 L 380 790" stroke="{INK}" stroke-width="6"/>')
        b.append(f'<path d="M 350 790 l 60 0 l -12 -34 l -36 0 z" fill="#f0d9a8" stroke="{INK}" stroke-width="4"/>')
        # растение
        b.append(f'<path d="M 940 900 l -14 44 l 34 0 z" fill="#b98a50" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<path d="M 936 896 q -18 -26 4 -40 q 18 14 6 40 z" fill="#6f9b52" stroke="{INK}" stroke-width="3"/>')
        b.append(f'<rect x="700" y="846" width="60" height="44" rx="6" fill="{WHITE}" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def unit_box(x, y, w=190, h=130, cls="unitG"):
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{UNIT}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="{h-28}" rx="6" fill="#eef3f5" stroke="{UNIT_D}" stroke-width="3"/>')
    # крест-накрест каналы
    for i in range(3):
        b.append(f'<path d="M {x+24+i*8} {y+24} l {w-70} {h-56}" stroke="{COLD}" stroke-width="8" opacity="0.7"/>')
        b.append(f'<path d="M {x+24+i*8} {y+h-24} l {w-70} {-(h-56)}" stroke="{HOT}" stroke-width="8" opacity="0.7"/>')
    b.append('</g>')
    return "".join(b)



def foot(big, sub, col=HOT, y=1290):
    """Крупная карточка-вывод внизу кадра."""
    return (f'<g class="footG"><rect x="90" y="{y}" width="900" height="300" rx="26" fill="#fffdf8" '
            f'stroke="{col}" stroke-width="4"/>'
            f'<text x="540" y="{y+150}" font-family="Nunito, Arial" font-size="112" font-weight="900" '
            f'fill="{col}" text-anchor="middle">{big}</text>'
            f'<text x="540" y="{y+230}" font-family="Nunito, Arial" font-size="34" font-weight="800" '
            f'fill="#4a4a4a" text-anchor="middle">{sub}</text></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(1)]
    b.append(house(True, "h1"))
    # открытая форточка и уходящее тепло
    b.append(f'<path class="heatOut" d="M 240 700 q 60 -70 150 -40" stroke="{HOT}" stroke-width="10" fill="none"/>')
    b.append(f'<path class="heatOut" d="M 250 760 q 80 -40 170 -10" stroke="{HOT}" stroke-width="8" fill="none"/>')
    b.append(badge(820, 250, "−20°", COLD, 42, 160, 66))
    b.append(txt(60, 300, "ТЕПЛО УХОДИТ", 62))
    b.append(txt(60, 370, "в форточку вместе с воздухом", 28, "#7a5a3a"))
    b.append(foot("40%", "тепла уходит с воздухом"))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(2)]
    b.append(house(True, "h2"))
    b.append(unit_box(430, 600, 200, 140, "u2"))
    b.append(duct("M 520 600 L 520 470 L 700 470 L 700 380", COLD, 22, "d2a"))
    b.append(duct("M 630 740 L 630 660", HOT, 20, "d2b"))
    b.append(txt(60, 300, "ДВА ПОТОКА", 56))
    b.append(txt(60, 366, "приток с улицы · вытяжка из дома", 26, "#7a5a3a"))
    b.append(badge(730, 330, "−20°", COLD, 36, 130, 56))
    b.append(foot("2", "потока в одном корпусе", COLD))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(3)]
    b.append(house(True, "h3"))
    b.append(unit_box(420, 610, 210, 140, "u3"))
    b.append(duct("M 500 610 L 500 480 L 700 480 L 700 400", COLD, 24, "d3a"))
    b.append(duct("M 640 750 L 640 670", HOT, 22, "d3b"))
    b.append(duct("M 430 680 L 300 680 L 300 700", HOT, 20, "d3c"))
    b.append(badge(720, 300, "−20°", COLD, 36, 130, 56))
    b.append(badge(150, 830, "+22°", HOT, 36, 130, 56))
    b.append(txt(60, 300, "ЗИМА", 58))
    b.append(txt(60, 366, "внутри тепло, снаружи мороз", 26, "#7a5a3a"))
    b.append(foot("−20° / +22°", "улица и дом зимой", COLD))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(4)]
    b.append(f'<rect x="140" y="520" width="800" height="620" rx="24" fill="#eef3f5" stroke="{INK}" stroke-width="7"/>')
    # чередующиеся каналы: тёплый справа налево, холодный слева направо
    for i in range(5):
        y = 560 + i * 112
        b.append(f'<path class="coreRed" d="M 170 {y+34} L 910 {y+34}" stroke="{HOT}" stroke-width="26" opacity="0" stroke-linecap="round"/>')
        b.append(f'<path class="coreRed" d="M 170 {y+34} L 910 {y+34}" stroke="{HOT_L}" stroke-width="8" opacity="0" stroke-dasharray="18 14"/>')
        b.append(f'<path class="coreBlue" d="M 170 {y+78} L 910 {y+78}" stroke="{COLD}" stroke-width="26" opacity="0" stroke-linecap="round"/>')
        b.append(f'<path class="coreBlue" d="M 170 {y+78} L 910 {y+78}" stroke="{COLD_L}" stroke-width="8" opacity="0" stroke-dasharray="18 14"/>')
        b.append(f'<path d="M 150 {y+56} L 930 {y+56}" stroke="{UNIT_D}" stroke-width="3" opacity="0.6"/>')
    # направление потоков
    for i in range(5):
        y = 560 + i * 112
        b.append(f'<path class="dirRed" d="M 250 {y+34} l -34 0 l 12 -11 l 0 22 z" fill="{HOT}"/>')
        b.append(f'<path class="dirBlue" d="M 830 {y+78} l 34 0 l -12 -11 l 0 22 z" fill="{COLD}"/>')
    b.append(txt(170, 1130, "вытяжка из дома →", 24, HOT))
    b.append(txt(910, 1130, "← приток с улицы", 24, COLD, "end"))
    b.append(txt(60, 330, "ТЕПЛООБМЕННИК", 52))
    b.append(txt(60, 396, "каналы идут навстречу, воздух не смешивается", 24, "#7a5a3a"))
    b.append(badge(140, 1180, "вытяжка +22°", HOT, 28, 320, 62))
    b.append(badge(620, 1180, "приток −20°", COLD, 28, 310, 62))
    b.append(txt(60, 1330, "ТЕПЛО ПРОХОДИТ ЧЕРЕЗ СТЕНКУ КАНАЛА", 26, "#7a5a3a"))
    b.append(badge(360, 1400, "приток +16°", OK, 32, 360, 74))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(5)]
    b.append(house(True, "h5"))
    b.append(unit_box(420, 600, 210, 150, "u5"))
    b.append(duct("M 500 600 L 500 470 L 700 470 L 700 390", COLD, 24, "d5a"))
    b.append(duct("M 640 750 L 640 670", HOT, 22, "d5b"))
    b.append(duct("M 430 690 L 300 690", HOT, 20, "d5c"))
    b.append(badge(720, 300, "+16°", HOT_L, 36, 140, 56))
    b.append(badge(150, 840, "+22°", HOT, 34, 130, 54))
    b.append(badge(760, 1090, "+4°", COLD, 32, 120, 52))
    b.append(txt(60, 300, "ПРИТОК УЖЕ ТЁПЛЫЙ", 50))
    b.append(txt(60, 366, "вытяжка отдала ему тепло", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="#eef6f8"/>', grain(6)]
    b.append(house(True, "h6"))
    b.append(unit_box(420, 600, 210, 150, "u6"))
    b.append(duct("M 500 600 L 500 470 L 700 470 L 700 390", HOT, 24, "d6a"))
    b.append(duct("M 430 690 L 300 690", COLD, 22, "d6b"))
    b.append(badge(720, 300, "+30°", HOT, 36, 140, 56))
    b.append(badge(150, 840, "+24°", COLD, 34, 130, 54))
    b.append(txt(60, 300, "ЛЕТО", 58))
    b.append(txt(60, 366, "приток охлаждается, жара уходит", 26, "#2f5f70"))
    b.append(foot("летом", "приток охлаждается", COLD))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(7)]
    b.append(txt(60, 300, "ЭФФЕКТИВНОСТЬ", 54))
    b.append(txt(60, 366, "сколько тепла возвращается", 26, "#7a5a3a"))
    # шкала
    b.append(f'<rect x="100" y="620" width="880" height="90" rx="45" fill="#e6ddcc" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect class="bar7" x="100" y="620" width="0" height="90" rx="45" fill="{OK}"/>')
    b.append(txt(100, 790, "30%", 34, "#7a5a3a"))
    b.append(txt(890, 790, "95%", 34, OK))
    b.append(badge(340, 900, "до 90%", OK, 54, 400, 110))
    b.append(txt(60, 1200, "ЗАВИСИТ ОТ АППАРАТА И МОНТАЖА", 26, "#7a5a3a"))
    b.append(txt(60, 1320, "ЧЕМ БОЛЬШЕ ПЛОЩАДЬ ОБМЕНА —", 26, "#7a5a3a"))
    b.append(txt(60, 1370, "ТЕМ ВЫШЕ КПД", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(8)]
    b.append(f'<rect x="90" y="520" width="900" height="700" rx="20" fill="{WALL}" stroke="{INK}" stroke-width="6"/>')
    b.append(unit_box(360, 600, 360, 220, "u8"))
    # фильтры
    b.append(f'<rect x="390" y="640" width="120" height="60" rx="8" fill="#cfe0c8" stroke="{INK}" stroke-width="4"/>')
    b.append(txt(450, 682, "фильтр", 22, "#3a5a30", "middle"))
    # конденсат
    b.append(f'<path class="cond8" d="M 540 820 L 540 900 q 0 20 -20 20" stroke="{COLD}" stroke-width="8" fill="none"/>')
    b.append(f'<circle class="drop8" cx="520" cy="940" r="9" fill="{COLD}"/>')
    # выводы
    b.append(duct("M 360 660 L 220 660 L 220 560", COLD, 20, "d8a"))
    b.append(duct("M 720 660 L 860 660 L 860 560", HOT, 20, "d8b"))
    b.append(txt(60, 330, "МОНТАЖ", 56))
    b.append(txt(60, 396, "стена или вентиляция + фильтры + слив", 26, "#7a5a3a"))
    b.append(foot("слив", "конденсат в дренаж", COLD))
    return b


# ---------------------------------------------------------------- s9
def s9():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(9)]
    b.append(house(True, "h9"))
    b.append(unit_box(430, 600, 200, 140, "u9"))
    b.append(duct("M 500 600 L 500 470 L 700 470 L 700 390", COLD, 22, "d9a"))
    b.append(duct("M 640 740 L 640 670", HOT, 20, "d9b"))
    b.append(badge(720, 300, "−20°", COLD, 34, 130, 54))
    b.append(badge(150, 840, "+22°", HOT, 34, 130, 54))
    b.append(f'<g class="ok9"><path d="M 700 900 l 50 60 l 100 -130" stroke="{OK}" stroke-width="22" fill="none" stroke-linecap="round"/></g>')
    b.append(txt(60, 300, "СВЕЖИЙ ВОЗДУХ", 54))
    b.append(txt(60, 366, "без потерь тепла", 30, OK))
    b.append(foot("365", "дней свежий воздух", OK))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".houseG", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.to(".heatOut", {x:60, opacity:0.3, duration:1.2, stagger:0.2, yoyo:true, repeat:5}, 0.3);'
    'tl.fromTo(".badgeG", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.4, ease:"back.out(2)"}, 0.8);',
    'tl.fromTo(".u2", {opacity:0, scale:0.8, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.5}, 0.3);'
    'tl.fromTo(".d2a", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.6}, 0.7);'
    'tl.fromTo(".d2b", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.9);' +
    'tl.to(".duct", {strokeWidth:26, duration:0.4, yoyo:true, repeat:3}, 1.2);',
    'tl.fromTo(".d3a", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.fromTo(".d3b", {opacity:0}, {opacity:1, duration:0.5}, 0.5);'
    'tl.fromTo(".d3c", {opacity:0, x:20}, {opacity:1, x:0, duration:0.5}, 0.7);'
    'tl.to(".badgeG", {scale:1.06, transformOrigin:"50% 50%", duration:0.4, stagger:0.2, yoyo:true, repeat:3}, 1.0);',
    'tl.to(".coreRed", {opacity:1, duration:0.5, stagger:0.12}, 0.2);'
    'tl.to(".coreBlue", {opacity:1, duration:0.5, stagger:0.12}, 0.35);'
    'tl.to(".coreRed", {opacity:0.55, duration:0.7, yoyo:true, repeat:3}, 1.3);'
    'tl.to(".coreBlue", {opacity:0.55, duration:0.7, yoyo:true, repeat:3}, 1.3);'
    'tl.to(".dirRed", {x:-14, duration:0.6, stagger:0.1, yoyo:true, repeat:4}, 1.0);'
    'tl.to(".dirBlue", {x:14, duration:0.6, stagger:0.1, yoyo:true, repeat:4}, 1.0);',
    'tl.fromTo(".d5a", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.fromTo(".d5b", {opacity:0}, {opacity:1, duration:0.5}, 0.4);'
    'tl.fromTo(".d5c", {opacity:0, x:30}, {opacity:1, x:0, duration:0.5}, 0.6);'
    'tl.to(".badgeG", {y:-8, duration:0.4, stagger:0.15, yoyo:true, repeat:3}, 0.9);',
    'tl.fromTo(".d6a", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.fromTo(".d6b", {opacity:0, x:20}, {opacity:1, x:0, duration:0.5}, 0.4);',
    'tl.to(".bar7", {attr:{"width":790}, duration:1.6, ease:"power2.out"}, 0.3);'
    'tl.fromTo(".badgeG", {scale:0.4, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(2)"}, 1.4);',
    'tl.fromTo(".u8", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.to(".drop8", {y:18, opacity:0, duration:0.9, repeat:4}, 0.8);'
    'tl.to(".cond8", {opacity:0.4, duration:0.5, yoyo:true, repeat:3}, 0.6);',
    'tl.fromTo(".ok9", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 0.6);'
    'tl.to(".badgeG", {y:-6, duration:0.5, stagger:0.2, yoyo:true, repeat:3}, 0.4);',
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
