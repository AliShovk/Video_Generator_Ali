#!/usr/bin/env python3
"""«Вал вместо забора» — 8 сцен, скетч. Крупная композиция."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/berm")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

PAPER = "#f5efe3"
INK = "#2b2b2b"
EARTH = "#c08a4e"
EARTH_D = "#a9743c"
GRASS = "#8fae63"
GREEN = "#4f9b4a"
RED = "#d2452f"
SKY = "#e9f1f4"
CAR = "#b9bfc4"
HOUSE = "#dfe3e6"
GROUND = 1500


def S(d, w=7, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, op=1.0, cls="fillshape"):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}"/>'


def txt(x, y, s, size=54, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def hand(x, y, s, size=76, col=INK, anchor="middle", rot=-3):
    return (f'<text class="hand" x="{x}" y="{y}" font-family="Caveat, Nunito, cursive" font-size="{size}" '
            f'font-weight="700" fill="{col}" text-anchor="{anchor}" transform="rotate({rot} {x} {y})">{s}</text>')


def grain(seed, n=180):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.6):.1f}" '
                   f'fill="#8a7f6a" opacity="{r.uniform(0.04,0.1):.2f}"/>' for _ in range(n))


def tree(x, y, s=1.0, cls=""):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M 0 0 L 0 -110" stroke="#6b4a2a" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="M 0 -60 L -44 -110 M 0 -80 L 42 -124" stroke="#6b4a2a" stroke-width="9" stroke-linecap="round"/>'
            f'<ellipse cx="-24" cy="-176" rx="70" ry="52" fill="{GRASS}" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="54" cy="-192" rx="58" ry="44" fill="{GRASS}" stroke="{INK}" stroke-width="5"/>'
            f'<ellipse cx="12" cy="-232" rx="64" ry="48" fill="{GRASS}" stroke="{INK}" stroke-width="5"/></g>')


def house(x=80, y=940, w=400, h=560):
    return (f'<g class="houseG"><path d="M {x-40} {y} L {x+w/2} {y-120} L {x+w+40} {y} Z" fill="#6d7378" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{HOUSE}" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{x+56}" y="{y+70}" width="104" height="120" fill="{SKY}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x+236}" y="{y+70}" width="104" height="120" fill="{SKY}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x+140}" y="{y+330}" width="120" height="230" fill="#8a6a4a" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x-55}" y="{y+h-80}" width="80" height="80" fill="{HOUSE}" stroke="{INK}" stroke-width="5"/></g>')


def car(x=848, y=1470, s=0.9, cls="car"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M 0 0 l 0 -80 l 46 -58 l 126 -16 l 66 52 l 44 22 l 0 80 z" fill="{CAR}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="58" cy="8" r="30" fill="#3a3f44" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="238" cy="8" r="30" fill="#3a3f44" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M 70 -76 l 30 -46 l 92 -12 l 50 58 z" fill="{SKY}" stroke="{INK}" stroke-width="4"/></g>')


def person(x, y, s=1.0, col="#f5d94e", cls="person", sit=False):
    if sit:
        return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
                f'<circle cx="0" cy="-100" r="20" fill="#f0c9a0" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M -20 -80 L 20 -80 L 20 -40 L -20 -40 Z" fill="{col}" stroke="{INK}" stroke-width="4"/>'
                f'<path d="M -20 -40 L -20 0 L 34 0" stroke="{INK}" stroke-width="11" fill="none"/></g>')
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="-96" r="20" fill="#f0c9a0" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M -20 -76 L 20 -76 L 24 -20 L -24 -20 Z" fill="{col}" stroke="{INK}" stroke-width="4"/>'
            f'<path d="M -20 -20 L -20 16 M 20 -20 L 20 16" stroke="{INK}" stroke-width="10"/></g>')


def ground(y=GROUND, col=EARTH, op=1.0):
    return F(f"M 0 {y} L 1080 {y} L 1080 1920 L 0 1920 Z", col, op)


def berm(x0=480, x1=840, peak=1100, base=GROUND, col=EARTH_D, op=1.0, cls="bermShape"):
    mid = (x0 + x1) / 2
    d = (f"M {x0} {base} Q {x0+30} {peak+40} {mid-70} {peak+8} Q {mid} {peak} {mid+70} {peak+8} "
         f"Q {x1-30} {peak+40} {x1} {base} Z")
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}" stroke="{INK}" stroke-width="7"/>'


def waves(x, y, n=3, flip=False, col=RED, cls="wave"):
    out = []
    for i in range(n):
        r = 60 + i * 46
        d = (f"M {x} {y} a {r} {r} 0 0 1 0 {-2*r}" if not flip else f"M {x} {y} a {r} {r} 0 0 0 0 {-2*r}")
        out.append(f'<path class="{cls}" d="{d}" stroke="{col}" stroke-width="8" fill="none" opacity="0.85"/>')
    return "".join(out)


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(1)]
    b.append(ground())
    b.append(house())
    b.append(car())
    b.append(waves(880, 1330, 4))
    b.append(waves(700, 1300, 3, True))
    b.append(hand(80, 400, "вал вместо забора", 92, INK, "start"))
    b.append(txt(80, 480, "ШУМ · ВЗГЛЯДЫ · ТЕНЬ", 36, "#6b5a44"))
    b.append(txt(70, 1790, "И ЭТО БЕСПЛАТНО, ЕСЛИ ГРУНТ СВОЙ", 26, "#6b5a44"))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(2)]
    b.append(ground())
    b.append(house())
    b.append(car())
    b.append(tree(640, GROUND, 1.35))
    b.append(waves(880, 1330, 3))
    b.append(S("M 430 1230 L 900 1390", 5, INK, "draw", 'stroke-dasharray="16 12"'))
    b.append(txt(400, 1180, "взгляд", 30, INK, "end"))
    b.append('<g class="cross2"><path d="M 880 520 l 130 130 M 1010 520 l -130 130" stroke="#d2452f" stroke-width="26" stroke-linecap="round"/></g>')
    b.append(txt(70, 1790, "ОДНО ДЕРЕВО НЕ ПРЕГРАДА", 34, RED))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(3)]
    b.append(ground())
    b.append(house())
    b.append(car())
    b.append(f'<path class="ray3" d="M 900 1300 L 500 1210" stroke="{RED}" stroke-width="10" fill="none"/>')
    b.append(f'<path d="M 535 1215 l 40 -16 l -6 34 z" fill="{RED}"/>')
    b.append(S("M 900 1420 L 500 1330", 5, INK, "draw", 'stroke-dasharray="14 10"'))
    b.append(txt(540, 1170, "ЗВУК", 32, RED))
    b.append(txt(540, 1380, "ВЗГЛЯД", 32, INK))
    b.append(hand(540, 430, "всё идёт по прямой", 82, INK))
    b.append(txt(70, 1790, "ЗНАЧИТ НУЖНА ПРЕГРАДА НА ПУТИ", 28, "#6b5a44"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(4)]
    b.append(ground())
    b.append(house())
    b.append(car())
    b.append(berm())
    b.append(tree(600, 1140, 0.95))
    b.append(tree(740, 1150, 0.78))
    b.append(f'<path class="ray4" d="M 890 1300 L 690 1210" stroke="{RED}" stroke-width="10" fill="none"/>')
    b.append(f'<path class="ray4b" d="M 690 1210 L 640 880" stroke="{RED}" stroke-width="10" fill="none"/>')
    b.append(f'<path d="M 618 900 l -18 -30 M 618 900 l 26 -22" stroke="{RED}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    b.append(hand(760, 800, "звук вверх", 62, RED, "start"))
    b.append('<g class="ok4"><path d="M 890 470 l 54 64 l 108 -140" stroke="#3f9d4a" stroke-width="26" fill="none" stroke-linecap="round"/></g>')
    b.append(txt(70, 1790, "ВАЛ 1,5–2 М + ДЕРЕВЬЯ", 34, GREEN))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(5)]
    b.append(ground())
    b.append(house())
    b.append(car())
    b.append(berm())
    b.append(tree(610, 1140, 0.9))
    b.append(person(430, GROUND, 1.0, "#f5d94e", "sit5", True))
    b.append(person(370, GROUND, 1.0, "#e8734a", "sit5b", True))
    b.append(S("M 900 1290 L 760 1210", 6, INK, "draw", 'stroke-dasharray="14 10"'))
    b.append(f'<circle cx="760" cy="1210" r="18" fill="{RED}"/>')
    b.append(hand(790, 1060, "не видно", 66, RED))
    b.append(txt(70, 1790, "ТЕРРАСА СКРЫТА ОТ ДОРОГИ", 30, "#6b5a44"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(6)]
    b.append(ground())
    b.append(house())
    b.append(berm(460, 860, 1080))
    b.append(tree(600, 1120, 0.85))
    b.append(tree(750, 1130, 0.7))
    for i in range(4):
        b.append(f'<path class="sun6" d="M {1010 - i*50} {380 + i*40} L {720 - i*30} {1120 + i*40}" '
                 f'stroke="#e8b64c" stroke-width="8" opacity="0.85"/>')
    b.append(f'<circle class="sun6" cx="1010" cy="300" r="64" fill="#f2c14e" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<path class="shadow6" d="M 200 {GROUND} L 520 {GROUND} L 470 1240 L 300 1280 Z" fill="#7a6a52" opacity="0.35"/>')
    b.append(hand(300, 1210, "тень", 64, "#5f5138"))
    b.append(txt(70, 1790, "ВАЛ РАБОТАЕТ И КАК ТЕНЕВОЙ ЭКРАН", 26, "#6b5a44"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(7)]
    b.append(ground())
    b.append(berm(160, 880, 1020))
    for i, yy in enumerate(range(1060, GROUND, 62)):
        b.append(f'<path class="layer7" d="M {200 + i*8} {yy} L {840 - i*8} {yy}" stroke="#8a6a3a" stroke-width="4" opacity="0.55"/>')
    b.append(S("M 160 1500 L 300 1120", 5, INK))
    b.append(txt(150, 1330, "2", 34))
    b.append(txt(250, 1150, "1", 34))
    b.append(txt(60, 420, "ОТКОС 1 : 2", 46))
    b.append(txt(60, 490, "пологий — не сползает", 26, "#6b5a44"))
    b.append(f'<circle cx="900" cy="1460" r="38" fill="#b9c0c4" stroke="{INK}" stroke-width="5"/>')
    b.append(S("M 876 1456 l 48 0 M 900 1432 l 0 48", 5))
    b.append(hand(900, 1400, "дренаж", 54, "#2f6fa8"))
    b.append(S("M 970 1020 L 970 1500", 5, "#2f6fa8"))
    b.append(S("M 940 1020 L 1000 1020 M 940 1500 L 1000 1500", 5, "#2f6fa8"))
    b.append(txt(1000, 1280, "1,5–2 м", 36, "#2f6fa8", "end"))
    b.append(txt(60, 1790, "ТРАМБОВКА СЛОЯМИ · ВОДА ОТВЕДЕНА", 26, "#6b5a44"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', grain(8)]
    b.append(ground())
    b.append(house())
    b.append(f'<path class="bad8" d="M 560 1500 Q 600 1150 650 1150 Q 700 1150 720 1500 Z" fill="{EARTH_D}" stroke="{INK}" stroke-width="6"/>')
    b.append(S("M 610 1290 L 650 1350 M 650 1290 L 610 1350", 7, RED))
    b.append(hand(640, 1100, "нельзя", 52, RED))
    b.append(berm(800, 1050, 1120, GROUND, EARTH_D, 1.0, "good8"))
    b.append(tree(900, 1140, 0.5))
    b.append(S("M 730 1500 L 800 1500", 7, "#2f6fa8"))
    b.append(txt(730, 1460, "отступ", 26, "#2f6fa8"))
    b.append('<g class="ok8"><path d="M 860 800 l 44 50 l 86 -110" stroke="#3f9d4a" stroke-width="20" fill="none" stroke-linecap="round"/></g>')
    b.append(txt(70, 1790, "ОТСТУП ОТ СТЕНЫ + ДРЕНАЖ", 28, "#6b5a44"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.to(".wave", {opacity:0.15, duration:0.7, stagger:0.1, yoyo:true, repeat:5}, 0.2);'
    'tl.fromTo(".bermShape", {scaleY:0.3, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.2, ease:"power2.out"}, 0.3);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.8, stagger:0.1}, 0.1);',
    'tl.to(".wave", {opacity:0.2, duration:0.5, stagger:0.1, yoyo:true, repeat:6}, 0.2);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.9}, 0.3);'
    'tl.fromTo(".cross2", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 1.0);',
    'tl.fromTo(".ray3", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:1.1, ease:"power2.out"}, 0.2);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.9}, 0.4);',
    'tl.fromTo(".bermShape", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.0, ease:"power2.out"}, 0.1);'
    'tl.fromTo(".ray4", {scaleX:0, transformOrigin:"100% 50%"}, {scaleX:1, duration:0.6}, 0.8);'
    'tl.fromTo(".ray4b", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.6}, 1.4);'
    'tl.fromTo(".ok4", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 1.7);',
    'tl.fromTo(".bermShape", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.0}, 0.1);'
    'tl.fromTo(".sit5, .sit5b", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 0.8);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.9}, 0.9);',
    'tl.fromTo(".sun6", {opacity:0}, {opacity:1, duration:0.6, stagger:0.12}, 0.2);'
    'tl.fromTo(".shadow6", {opacity:0}, {opacity:0.35, duration:0.9}, 1.0);',
    'tl.to(".layer7", {opacity:0.9, duration:0.3, stagger:0.08}, 0.2);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.7, stagger:0.08}, 0.1);',
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:0.6, stagger:0.06}, 0.1);'
    'tl.fromTo(".good8", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.9}, 0.9);'
    'tl.fromTo(".bad8", {opacity:0}, {opacity:1, duration:0.5}, 0.2);'
    'tl.fromTo(".ok8", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.5, ease:"back.out(3)"}, 1.5);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{PAPER}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.035, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.08 }}, 0.05);
    tl.fromTo(".hand", {{ opacity:0, y:18 }}, {{ opacity:1, y:0, duration:0.6, stagger:0.15 }}, 0.15);
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
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
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
