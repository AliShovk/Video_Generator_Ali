#!/usr/bin/env python3
"""«Солнечное отопление» — 8 сцен, светлая объёмная иллюстрация."""
import json
import math
from pathlib import Path

ROOT = Path("/root/video-gen/solar")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG1 = "#f3f7fa"; BG2 = "#e6eef4"
INK = "#33404a"; INK2 = "#5f7079"
WALL = "#f7efdd"; WALL_D = "#e6d9bd"
RED = "#d1543f"; RED_D = "#a83a2a"
BLUE = "#5b8fb9"; BLUE_D = "#3f6b91"
YEL = "#e8b63d"; GLASS = "#9db9c4"; GLASS_D = "#7a97a3"
TANK = "#bcd6e2"; TANK_D = "#8fb2c3"; WATER = "#7fb8d4"
WOOD = "#c9a06a"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def title(x, y, s, size=38, cls="hl", col=INK):
    w = len(s) * size * 0.62 + 34
    return (f'<g class="{cls}"><rect x="{x-12}" y="{y-size*1.1:.0f}" width="{w:.0f}" height="{size*1.6:.0f}" rx="{size*0.3:.0f}" '
            f'fill="#ffffff" opacity="0.85"/>'
            f'<text x="{x}" y="{y}" font-family="Nunito" font-size="{size}" font-weight="900" fill="{col}" letter-spacing="1">{s}</text></g>')


def bg():
    return ('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#bg)"/>')


def house(cls="hs"):
    """Разрез дома: фасад, боковая грань, двускатная крыша с толщиной."""
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M 930 420 L 1000 380 L 1000 1540 L 930 1600 Z" fill="{WALL_D}" stroke="{INK2}" stroke-width="3"/>')
    b.append(f'<path d="M 150 420 L 930 420 L 930 1600 L 150 1600 Z" fill="{WALL}" stroke="{INK2}" stroke-width="4"/>')
    b.append(f'<path d="M 130 424 L 540 230 L 950 424 L 930 448 L 540 258 L 150 448 Z" fill="#e9dcc0" stroke="{INK2}" stroke-width="4"/>')
    b.append(f'<path d="M 150 448 L 930 448" stroke="{INK2}" stroke-width="2" opacity="0.5"/>')
    b.append(f'<rect x="150" y="1000" width="780" height="24" fill="{WALL_D}" stroke="{INK2}" stroke-width="2"/>')
    b.append('</g>')
    return "".join(b)


def roof_collectors(cls="cl", n=4):
    """Панели, лежащие на левом скате крыши (длинная сторона — вниз по скату)."""
    x0, y0 = 185, 452
    x1, y1 = 525, 292
    dx, dy = (x1 - x0) / n, (y1 - y0) / n
    ux, uy = dx, dy
    vx, vy = 52, 118
    b = [f'<g class="{cls}">']
    for i in range(n):
        px, py = x0 + ux * i, y0 + uy * i
        w = ux * 0.80
        hx, hy = ux * 0.80, uy * 0.80
        b.append(f'<path d="M {px:.0f} {py:.0f} l {hx:.0f} {hy:.0f} l {vx} {vy} l {-hx:.0f} {-hy:.0f} z" '
                 f'fill="{GLASS}" stroke="{GLASS_D}" stroke-width="3"/>')
        for k in range(5):
            t = 0.12 + k * 0.18
            b.append(f'<path d="M {px+hx*t:.0f} {py+hy*t:.0f} l {vx*0.9:.0f} {vy*0.9:.0f}" stroke="#ffffff" stroke-width="2" opacity="0.45"/>')
    b.append('</g>')
    return "".join(b)


def pipe(pts, col=RED, w=8, cls="pp", dash="10 12"):
    d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    return (f'<g class="{cls}"><path d="{d}" stroke="{col}" stroke-width="{w}" fill="none" stroke-linecap="round" opacity="0.95"/>'
            f'<path class="flow" d="{d}" stroke="#ffffff" stroke-width="{w*0.45:.1f}" fill="none" stroke-linecap="round" '
            f'stroke-dasharray="{dash}" opacity="0.85"/></g>')


def tank(x, y, w=170, h=250, cls="tk"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{TANK}" stroke="{TANK_D}" stroke-width="4"/>'
            f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="26" fill="#d8ecf3" stroke="{TANK_D}" stroke-width="4"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+h}" rx="{w/2}" ry="26" fill="{TANK}" stroke="{TANK_D}" stroke-width="4"/>'
            f'<rect class="wlevel" x="{x+8}" y="{y+h*0.45:.0f}" width="{w-16}" height="{h*0.5:.0f}" fill="{WATER}" opacity="0.55"/></g>')


def exchanger(x, y, cls="ex"):
    b = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="110" height="230" rx="20" fill="#e8f1f5" stroke="{GLASS_D}" stroke-width="3"/>']
    for i in range(7):
        b.append(f'<path d="M {x+14} {y+22+i*28} q 41 18 82 0" stroke="{RED}" stroke-width="6" fill="none"/>')
    b.append('</g>')
    return "".join(b)


def floor_loop(x, y, w, h, rows=6, cls="fl"):
    """Змейка тёплого пола."""
    step = h / rows
    d = [f"M {x} {y}"]
    for r in range(rows):
        yy = y + r * step
        if r % 2 == 0:
            d.append(f"L {x+w} {yy}")
            d.append(f"L {x+w} {yy+step}")
        else:
            d.append(f"L {x} {yy}")
            d.append(f"L {x} {yy+step}")
    d.append(f"L {x+w} {y+h}")
    return (f'<g class="{cls}"><path d="{" ".join(d)}" fill="none" stroke="{RED}" stroke-width="7" stroke-linejoin="round" opacity="0.95"/>'
            f'<path class="flow" d="{" ".join(d)}" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="8 14" opacity="0.8"/></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [bg(), house("hs1"), roof_collectors("c1")]
    b.append(floor_loop(210, 560, 620, 380, 6, "f1"))
    b.append(tank(560, 1220, 180, 250, "tk1"))
    b.append(exchanger(300, 1230, "ex1"))
    b.append(pipe([(900, 470), (900, 1290), (745, 1290)], BLUE, 7, "p1", "12 16"))
    b.append(pipe([(220, 470), (220, 1310), (300, 1310)], RED, 7, "p2", "12 16"))
    b.append(pipe([(650, 1218), (650, 960), (560, 960)], RED, 7, "p3", "12 16"))
    b.append(title(60, 180, "СОЛНЦЕ ГРЕЕТ ДОМ", 38))
    b.append(t(64, 240, "замкнутый контур", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [bg()]
    b.append(f'<circle cx="880" cy="300" r="110" fill="{YEL}" opacity="0.9"/>')
    for i in range(10):
        a = math.radians(i * 36)
        b.append(f'<path d="M {880+130*math.cos(a):.0f} {300+130*math.sin(a):.0f} l {40*math.cos(a):.0f} {40*math.sin(a):.0f}" '
                 f'stroke="{YEL}" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
    b.append(f'<path d="M 120 700 L 540 520 L 960 700 L 960 1560 L 120 1560 Z" fill="{WALL}" stroke="{INK2}" stroke-width="4"/>')
    b.append(roof_collectors("c1"))
    b.append(f'<path class="sunray" d="M 820 400 L 640 620" stroke="{YEL}" stroke-width="6" stroke-dasharray="14 12" opacity="0.8"/>')
    b.append(title(60, 190, "КОЛЛЕКТОРЫ НА КРЫШЕ", 32))
    b.append(t(150, 980, "тёмные трубки ловят свет", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [bg(), house("hs3")]
    b.append(roof_collectors("c2"))
    b.append(pipe([(300, 360), (300, 470), (940, 470), (940, 1300)], RED, 9, "p3", "14 18"))
    b.append(f'<circle class="pump" cx="620" cy="470" r="46" fill="{RED}" opacity="0.9"/>')
    b.append(f'<path d="M 604 470 l 32 0 M 620 454 l 0 32" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>')
    b.append(t(680, 420, "НАСОС", 26, INK, w=800))
    b.append(title(60, 180, "ВНИЗ, В БАК", 40))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [bg(), house("hs4")]
    b.append(exchanger(240, 900, "ex4"))
    b.append(tank(620, 880, 230, 320, "tk4"))
    b.append(f'<path class="hw" d="M 380 980 q 90 0 150 40" stroke="{RED}" stroke-width="8" fill="none"/>')
    b.append(f'<path class="cw" d="M 380 1080 q 90 0 150 -30" stroke="{BLUE}" stroke-width="8" fill="none"/>')
    b.append(t(380, 1280, "ЗМЕЕВИК", 24, INK, w=800))
    b.append(title(60, 180, "ТЕПЛООБМЕННИК", 34))
    b.append(t(64, 240, "отдаёт тепло воде в баке", 22, INK2, w=700))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [bg(), house("hs5")]
    b.append(tank(380, 620, 320, 620, "tk5"))
    b.append(f'<path class="lvl" d="M 400 1150 l 280 0" stroke="#ffffff" stroke-width="4" opacity="0.7"/>')
    b.append(title(60, 180, "БАК-АККУМУЛЯТОР", 34))
    b.append(t(64, 240, "запас на ночь и на пасмурный день", 22, INK2, w=700))
    b.append(f'<circle class="moon" cx="860" cy="320" r="70" fill="#dfe9f0" stroke="{GLASS_D}" stroke-width="4"/>')
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [bg(), house("hs6")]
    b.append(floor_loop(200, 560, 660, 380, 6, "f6"))
    b.append(pipe([(300, 1480), (300, 1400), (300, 1380)], BLUE, 8, "p6", "12 16"))
    b.append(t(120, 900, "ТЁПЛЫЙ ПОЛ", 30, INK, w=900))
    b.append(t(120, 950, "второй контур", 22, INK2, w=700))
    b.append(f'<path d="M 540 1020 l 0 -70" stroke="{RED}" stroke-width="6" opacity="0.5"/>')
    b.append(f'<path d="M 540 950 l -16 26 l 32 0 z" fill="{RED}" opacity="0.6"/>')
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [bg(), house("hs7")]
    b.append(roof_collectors("c3"))
    b.append(f'<rect x="640" y="760" width="220" height="300" rx="20" fill="#eef3f6" stroke="{INK2}" stroke-width="3"/>')
    b.append(t(750, 830, "АВТОМАТИКА", 20, INK, "middle", 800))
    b.append(f'<text x="750" y="920" font-family="Nunito" font-size="46" font-weight="900" fill="{RED}" text-anchor="middle">ΔT</text>')
    b.append(f'<circle class="led" cx="750" cy="1000" r="14" fill="{YEL}"/>')
    b.append(f'<path d="M 640 900 l -120 -60" stroke="{INK2}" stroke-width="4" stroke-dasharray="10 8"/>')
    b.append(f'<path d="M 640 980 l -120 60" stroke="{INK2}" stroke-width="4" stroke-dasharray="10 8"/>')
    b.append(title(60, 180, "УМНЫЙ НАСОС", 38))
    b.append(t(64, 240, "включается, когда коллектор горячее бака", 20, INK2, w=700))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [bg(), house("hs8"), roof_collectors("c8")]
    b.append(floor_loop(210, 560, 620, 380, 6, "f8"))
    b.append(tank(560, 1220, 180, 250, "tk8"))
    b.append(exchanger(300, 1230, "ex8"))
    b.append(title(60, 180, "МЕНЬШЕ ГАЗА", 44))
    b.append(t(64, 246, "солнце + бак + тёплый пол", 24, INK2, w=700))
    b.append(f'<circle cx="900" cy="300" r="80" fill="{YEL}" opacity="0.85"/>')
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".hs1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".c1", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.6}, 0.3);'
    'tl.fromTo(".tk1, .ex1", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.5);'
    'tl.to(".flow", {strokeDashoffset:-80, duration:2, repeat:-1, ease:"none"}, 0.6);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".c2", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.8}, 0.1);'
    'tl.to(".sunray", {strokeDashoffset:-60, duration:1.4, repeat:-1, ease:"none"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".hs3", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.to(".flow", {strokeDashoffset:-90, duration:1.6, repeat:-1, ease:"none"}, 0.4);'
    'tl.fromTo(".pump", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}, 0.5);'
    'tl.to(".pump", {rotate:360, transformOrigin:"620px 470px", duration:3, repeat:-1, ease:"linear"}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".hs4", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".ex4", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6}, 0.2);'
    'tl.fromTo(".tk4", {opacity:0, x:30}, {opacity:1, x:0, duration:0.6}, 0.4);'
    'tl.fromTo(".hw, .cw", {opacity:0}, {opacity:1, duration:0.6, stagger:0.2}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".tk5", {opacity:0, scale:0.96}, {opacity:1, scale:1, duration:0.7}, 0.1);'
    'tl.fromTo(".wlevel", {opacity:0, y:60}, {opacity:0.55, y:0, duration:1.4}, 0.5);'
    'tl.fromTo(".lvl", {opacity:0}, {opacity:0.7, duration:0.6}, 1.4);'
    'tl.fromTo(".moon", {opacity:0, y:-14}, {opacity:1, y:0, duration:0.6}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".hs6", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".f6", {opacity:0}, {opacity:0.95, duration:0.8}, 0.2);'
    'tl.to(".flow", {strokeDashoffset:-70, duration:1.8, repeat:-1, ease:"none"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".c7", {opacity:0}, {opacity:1, duration:0.5}, 0.1);'
    'tl.fromTo(".led", {opacity:0.3}, {opacity:1, duration:0.7, yoyo:true, repeat:-1}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".hs8", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".c8", {opacity:0, y:-16}, {opacity:1, y:0, duration:0.6}, 0.3);'
    'tl.fromTo(".f8, .tk8, .ex8", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.5);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG1}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
