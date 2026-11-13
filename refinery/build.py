#!/usr/bin/env python3
"""«Перегонка нефти» — 9 сцен, техническая инфографика."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/refinery")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#0a1016"
PANEL = "#111a21"
STEEL = "#39464e"
WHITE = "#f4f7f8"
MUTED = "#8ea2ad"
FIRE = "#ff8a3c"
FIRE2 = "#ffd166"
GAS = "#dfefff"
PETROL = "#f2df8a"
KERO = "#9fdbe0"
DIESEL = "#8cc63f"
BITUM = "#4a3427"


def t(x, y, s, size=46, col=WHITE, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def column(x=360, y=340, w=360, h=1160, cls="col"):
    """Колонна с градиентом нагрева и тарелками."""
    g = [f'<g class="{cls}">']
    g.append(f'<defs><linearGradient id="colg" x1="0" y1="1" x2="0" y2="0">'
             f'<stop offset="0" stop-color="#ff7a2a"/><stop offset="0.35" stop-color="#c96a2a"/>'
             f'<stop offset="0.7" stop-color="#5c7a80"/><stop offset="1" stop-color="#cfe6ea"/></linearGradient>'
             f'<linearGradient id="glass" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="#ffffff" stop-opacity="0.16"/>'
             f'<stop offset="0.25" stop-color="#ffffff" stop-opacity="0.03"/>'
             f'<stop offset="0.8" stop-color="#000000" stop-opacity="0.12"/>'
             f'<stop offset="1" stop-color="#000000" stop-opacity="0.28"/></linearGradient></defs>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2}" fill="url(#colg)" opacity="0.92"/>')
    # тарелки
    for fy in (0.10, 0.28, 0.46, 0.64, 0.82):
        yy = y + h * fy
        g.append(f'<rect x="{x+26}" y="{yy:.0f}" width="{w-52}" height="12" rx="6" fill="#2b353b" opacity="0.65"/>')
        g.append(f'<rect x="{x+40}" y="{yy+12:.0f}" width="{w-80}" height="26" rx="8" fill="{WHITE}" opacity="0.10"/>')
    # стекло
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2}" fill="url(#glass)"/>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w/2}" fill="none" stroke="{STEEL}" stroke-width="6"/>')
    g.append('</g>')
    return "".join(g)


def bottle(x, y, col, label, temp, cls="bt", w=140, h=140):
    """Канистра с фракцией: корпус, тёмная крышка, блик, подпись."""
    return (f'<g class="{cls}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{col}" stroke="{WHITE}" stroke-width="2" opacity="0.92"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="18" fill="#0d161c" opacity="0.35"/>'
            f'<rect x="{x+w*0.36:.0f}" y="{y-16}" width="{w*0.28:.0f}" height="20" rx="6" fill="{STEEL}"/>'
            f'<rect x="{x+14}" y="{y+16}" width="{w*0.14:.0f}" height="{h-40}" rx="8" fill="{WHITE}" opacity="0.18"/>'
            f'<text x="{x+w+26}" y="{y+46}" font-family="Nunito" font-size="26" font-weight="900" fill="{WHITE}">{label}</text>'
            f'<text x="{x+w+26}" y="{y+82}" font-family="Nunito" font-size="22" font-weight="800" fill="{MUTED}">{temp}</text>'
            f'</g>')


def pipe(x1, y1, x2, cls="pp", col="#8d9aa1"):
    return (f'<g class="{cls}"><path d="M {x1} {y1} l {x2-x1} 0" stroke="{col}" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M {x1} {y1} l {x2-x1} 0" stroke="{BG}" stroke-width="4" stroke-linecap="round" opacity="0.5"/></g>')


def temp_scale(x=110, y=520, h=900, cls="ts"):
    g = [f'<g class="{cls}">']
    g.append(f'<defs><linearGradient id="tsg" x1="0" y1="1" x2="0" y2="0">'
             f'<stop offset="0" stop-color="#d64545"/><stop offset="0.5" stop-color="#e0b23a"/>'
             f'<stop offset="1" stop-color="#3fa9f5"/></linearGradient></defs>')
    g.append(f'<rect x="{x}" y="{y}" width="26" height="{h}" rx="13" fill="url(#tsg)"/>')
    for lbl, fy in (("25 °C", 0.0), ("100", 0.22), ("180", 0.44), ("250", 0.66), ("350", 0.86)):
        yy = y + h * fy
        g.append(f'<path d="M {x+30} {yy:.0f} l 16 0" stroke="{MUTED}" stroke-width="2"/>')
        g.append(f'<text x="{x+54}" y="{yy+8:.0f}" font-family="Nunito" font-size="22" font-weight="800" fill="{MUTED}">{lbl}</text>')
    g.append('</g>')
    return "".join(g)


def fire(cx=540, y=1600, cls="fire"):
    g = [f'<g class="{cls}">']
    g.append(f'<rect x="{cx-190}" y="{y}" width="380" height="220" rx="16" fill="#20272c" stroke="{STEEL}" stroke-width="4"/>')
    for i, (dx, hh, col) in enumerate(((-130, 180, FIRE), (-45, 230, FIRE2), (45, 200, FIRE), (130, 160, FIRE2))):
        g.append(f'<path class="fl{i}" d="M {cx+dx-40} {y+200} q 40 -{hh} 80 0 q -22 34 -40 26 q -18 8 -40 -26 z" fill="{col}" opacity="0.95"/>')
    g.append('</g>')
    return "".join(g)


def vapor(n=26, seed=3, cls="vp"):
    r = random.Random(seed)
    return "".join(f'<circle class="v{i}" cx="{r.uniform(400,680):.0f}" cy="{r.uniform(900,1450):.0f}" '
                   f'r="{r.uniform(3,9):.1f}" fill="{WHITE}" opacity="{r.uniform(0.15,0.5):.2f}"/>' for i in range(n))


def badge(x, y, label, col=FIRE, cls="bd", w=None):
    ww = w or (len(label) * 15 + 40)
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{ww}" height="52" rx="26" fill="{col}" opacity="0.18"/>'
            f'<text x="{x+ww/2}" y="{y+35}" font-family="Nunito" font-size="24" font-weight="900" fill="{col}" '
            f'text-anchor="middle">{label}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<circle cx="540" cy="900" r="520" fill="#16232b" opacity="0.8"/>')
    b.append(column(360, 420, 360, 1080, "col1"))
    b.append(fire(540, 1500, "fire1"))
    b.append(vapor(24, 2))
    b.append(t(60, 210, "ОДНА НЕФТЬ —", 46, MUTED, ls=2))
    b.append(t(60, 300, "МНОГО ПРОДУКТОВ", 62, WHITE))
    b.append(t(60, 380, "как работает перегонка", 26, FIRE2, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(column(360, 300, 360, 1000, "col2"))
    b.append(fire(540, 1290, "fire2"))
    # труба подвода
    b.append(f'<path d="M 120 1560 q 180 0 220 -120" stroke="{STEEL}" stroke-width="16" fill="none"/>')
    b.append(f'<path d="M 120 1560 q 180 0 220 -120" stroke="{FIRE}" stroke-width="6" fill="none" opacity="0.5"/>')
    b.append(t(60, 220, "НАГРЕВ", 58, WHITE, ls=2))
    b.append(t(60, 290, "почти 400 °C", 40, FIRE2, w=800))
    b.append(t(60, 1660, "нефть входит снизу", 26, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(column(360, 300, 360, 1200, "col3"))
    b.append(fire(540, 1490, "fire3"))
    b.append(vapor(30, 5))
    b.append(f'<path class="up" d="M 540 1400 l 0 -760" stroke="{WHITE}" stroke-width="4" stroke-dasharray="18 16" opacity="0.5"/>')
    b.append(f'<path d="M 540 620 l -22 40 l 44 0 z" fill="{WHITE}" opacity="0.8"/>')
    b.append(t(60, 220, "ПАРЫ ИДУТ ВВЕРХ", 44, WHITE, ls=1))
    b.append(t(60, 290, "и остывают по пути", 28, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(column(340, 300, 400, 1200, "col4"))
    b.append(fire(540, 1490, "fire4"))
    for i, yy in enumerate((520, 700, 880, 1060)):
        b.append(f'<g class="drop{i}"><circle cx="{600+i*10}" cy="{yy}" r="9" fill="{WHITE}" opacity="0.9"/></g>')
        b.append(f'<ellipse cx="560" cy="{yy+22}" rx="70" ry="9" fill="{WHITE}" opacity="0.12"/>')
    b.append(t(60, 220, "КОНДЕНСАЦИЯ", 52, WHITE, ls=1))
    b.append(t(60, 290, "на каждой тарелке — своя фракция", 26, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(column(300, 320, 300, 1100, "col5"))
    b.append(fire(450, 1410, "fire5"))
    b.append(pipe(600, 470, 760, "p1"))
    b.append(pipe(600, 640, 760, "p2"))
    b.append(pipe(600, 810, 760, "p3"))
    b.append(bottle(760, 400, GAS, "ГАЗ", "25–40 °C", "b1"))
    b.append(bottle(760, 570, PETROL, "БЕНЗИН", "100 °C", "b2"))
    b.append(bottle(760, 740, KERO, "КЕРОСИН", "180 °C", "b3"))
    b.append(t(60, 210, "ВЕРХ КОЛОННЫ", 40, MUTED, ls=2))
    b.append(t(60, 270, "лёгкие фракции", 32, WHITE, w=800))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(column(300, 260, 300, 1160, "col6"))
    b.append(fire(450, 1410, "fire6"))
    b.append(pipe(600, 900, 760, "p4"))
    b.append(pipe(600, 1080, 760, "p5"))
    b.append(bottle(760, 830, DIESEL, "ДИЗЕЛЬ", "250 °C", "b4"))
    b.append(bottle(760, 1010, BITUM, "БИТУМ", "350 °C", "b5"))
    b.append(t(60, 210, "НИЗ КОЛОННЫ", 40, MUTED, ls=2))
    b.append(t(60, 270, "тяжёлые фракции", 32, WHITE, w=800))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(temp_scale(120, 500, 900, "ts7"))
    for i, (yy, col, lbl) in enumerate(((560, GAS, "25°"), (700, PETROL, "100°"), (860, KERO, "180°"),
                                        (1020, DIESEL, "250°"), (1180, BITUM, "350°"))):
        b.append(f'<circle class="pt{i}" cx="150" cy="{yy}" r="12" fill="{col}"/>')
    b.append(t(60, 220, "ВСЁ ДЕЛО В", 40, MUTED, ls=2))
    b.append(t(60, 290, "ТЕМПЕРАТУРЕ КИПЕНИЯ", 44, WHITE))
    b.append(t(60, 1520, "чем ниже температура — тем выше фракция", 24, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # три иконки продуктов (векторные)
    b.append(f'<g class="pr0"><circle cx="210" cy="700" r="130" fill="#16232b" stroke="{PETROL}" stroke-width="4"/>'
             f'<rect x="164" y="640" width="70" height="110" rx="10" fill="{PETROL}"/>'
             f'<rect x="176" y="658" width="46" height="30" rx="5" fill="{BG}"/>'
             f'<path d="M 234 660 q 26 0 26 26 l 0 40 q 0 12 -12 12" stroke="{PETROL}" stroke-width="9" fill="none"/>'
             f'<text x="210" y="880" font-family="Nunito" font-size="26" font-weight="900" fill="{WHITE}" text-anchor="middle">ТОПЛИВО</text></g>')
    b.append(f'<g class="pr1"><circle cx="540" cy="700" r="130" fill="#16232b" stroke="{KERO}" stroke-width="4"/>'
             f'<rect x="512" y="640" width="52" height="96" rx="12" fill="{KERO}" opacity="0.9"/>'
             f'<rect x="526" y="614" width="24" height="30" rx="6" fill="{KERO}" opacity="0.9"/>'
             f'<rect x="512" y="668" width="52" height="10" fill="{BG}" opacity="0.35"/>'
             f'<text x="540" y="880" font-family="Nunito" font-size="26" font-weight="900" fill="{WHITE}" text-anchor="middle">ПЛАСТИК</text></g>')
    b.append(f'<g class="pr2"><circle cx="870" cy="700" r="130" fill="#16232b" stroke="{BITUM}" stroke-width="5"/>'
             f'<path d="M 790 770 l 30 -110 l 130 0 l 30 110 z" fill="#2a2f33"/>'
             f'<path d="M 840 770 l 12 -110 l 10 0 l -4 110 z M 890 770 l -6 -110 l 10 0 l 6 110 z" fill="{WHITE}" opacity="0.7"/>'
             f'<text x="870" y="880" font-family="Nunito" font-size="26" font-weight="900" fill="{WHITE}" text-anchor="middle">ДОРОГИ</text></g>')
    b.append(t(60, 300, "ТОПЛИВО · ПЛАСТИК · ДОРОГИ", 34, WHITE, "start", 900))
    b.append(t(60, 1660, "всё из одной бочки нефти", 26, MUTED, w=700))
    return b


# ---------------------------------------------------------------- 9
def s9():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(column(360, 380, 360, 900, "col9"))
    b.append(fire(540, 1270, "fire9"))
    b.append(t(60, 230, "ОДНА НЕФТЬ —", 44, MUTED, ls=2))
    b.append(t(60, 300, "ДЕСЯТКИ ПРОДУКТОВ", 52, WHITE))
    for i, (lbl, col) in enumerate((("ГАЗ", GAS), ("БЕНЗИН", PETROL), ("КЕРОСИН", KERO), ("ДИЗЕЛЬ", DIESEL), ("БИТУМ", BITUM))):
        b.append(badge(60 + (i % 2) * 300, 1640 + (i // 2) * 70, lbl, col, f"bd{i}", 260))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".col1", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.05);'
    'tl.to(".fl0, .fl1, .fl2, .fl3", {scaleY:1.12, duration:0.4, stagger:0.08, yoyo:true, repeat:-1, transformOrigin:"540px 1800px"}, 0.3);'
    'tl.fromTo(".v0", {opacity:0}, {opacity:0.4, duration:0.6}, 0.5);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".col2", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.to(".fl0, .fl1, .fl2, .fl3", {scaleY:1.15, duration:0.35, stagger:0.07, yoyo:true, repeat:-1, transformOrigin:"540px 1340px"}, 0.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.12}, 0.1);',
    'tl.fromTo(".col3", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.to(".up", {y:-140, duration:2.2, yoyo:true, repeat:1, ease:"sine.inOut"}, 0.3);'
    'tl.to(".v0, .v1, .v2, .v3", {y:-120, opacity:0, duration:2.4, stagger:0.2, repeat:-1, ease:"sine.out"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".col4", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".drop0, .drop1, .drop2, .drop3", {opacity:0, y:-30}, {opacity:1, y:0, duration:0.8, stagger:0.15}, 0.3);'
    'tl.to(".drop0, .drop1, .drop2, .drop3", {y:26, duration:0.9, stagger:0.12, yoyo:true, repeat:-1, ease:"sine.in"});'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".col5", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".b1", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 0.3);'
    'tl.fromTo(".b2", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 0.55);'
    'tl.fromTo(".b3", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".col6", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".b4", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 0.3);'
    'tl.fromTo(".b5", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".ts7", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.05);'
    'tl.fromTo(".pt0, .pt1, .pt2, .pt3, .pt4", {opacity:0, scale:0.6}, {opacity:1, scale:1, duration:0.4, stagger:0.15}, 0.3);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".pr0, .pr1, .pr2", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.18}, 0.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".col9", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".bd0, .bd1, .bd2, .bd3, .bd4", {opacity:0, y:10}, {opacity:1, y:0, duration:0.4, stagger:0.12}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
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
