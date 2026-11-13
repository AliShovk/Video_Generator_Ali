#!/usr/bin/env python3
"""Сцены: реалистичная подача (материалы, свет, воздух)."""
import math

math_pi = math.pi
math_cos = math.cos
math_sin = math.sin
from make_scenes import DEFS, dust, grain, human, svg, text, truck, crane, vignette

W, H = 1080, 1920


def arch(cx, base_y, span, height, thick=58, ribs=26, lit="right", opacity=1.0, glow_inside=True):
    rx, ry = span / 2, height
    x0, x1 = cx - rx, cx + rx
    irx, iry = rx - thick, ry - thick * 0.9
    outer = f"M {x0} {base_y} A {rx} {ry} 0 0 1 {x1} {base_y}"
    inner = f"M {cx - irx} {base_y} A {irx} {iry} 0 0 1 {cx + irx} {base_y}"
    body = f"{outer} L {cx + irx} {base_y} A {irx} {iry} 0 0 0 {cx - irx} {base_y} Z"
    out = [f'<g opacity="{opacity}">']
    out.append(f'<path d="{body}" fill="#0b1116" opacity="0.55" transform="translate(0 10)" filter="url(#soft24)"/>')
    out.append(f'<path d="{body}" fill="url(#steel)" filter="url(#metalNoise)"/>')
    # панельные швы
    for i in range(1, 44):
        a = math_pi * i / 44
        ox, oy = cx - rx * math_cos(a), base_y - ry * math_sin(a)
        ix, iy = cx - irx * math_cos(a), base_y - iry * math_sin(a)
        out.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#1b242c" stroke-width="2" opacity="0.5"/>')
    # рёбра жёсткости
    for i in range(0, ribs + 1):
        a = math_pi * i / ribs
        ox, oy = cx - rx * math_cos(a), base_y - ry * math_sin(a)
        ix, iy = cx - irx * math_cos(a), base_y - iry * math_sin(a)
        out.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#0e151a" stroke-width="5" opacity="0.75"/>')
        out.append(f'<line x1="{ox+3:.1f}" y1="{oy:.1f}" x2="{ix+3:.1f}" y2="{iy:.1f}" stroke="#cfdbe4" stroke-width="1.6" opacity="0.25"/>')
    # раскосы
    for i in range(ribs):
        a1 = math_pi * i / ribs; a2 = math_pi * (i + 0.5) / ribs
        ox1, oy1 = cx - rx * math_cos(a1), base_y - ry * math_sin(a1)
        ix2, iy2 = cx - irx * math_cos(a2), base_y - iry * math_sin(a2)
        out.append(f'<line x1="{ox1:.1f}" y1="{oy1:.1f}" x2="{ix2:.1f}" y2="{iy2:.1f}" stroke="#243039" stroke-width="2" opacity="0.4"/>')
    # световой контур
    out.append(f'<path d="{outer}" fill="none" stroke="#eaf4fb" stroke-width="2.5" opacity="0.55"/>')
    out.append(f'<path d="{inner}" fill="none" stroke="#0a0f13" stroke-width="4" opacity="0.65"/>')
    if glow_inside:
        out.append(f'<ellipse cx="{cx}" cy="{base_y - ry * 0.25}" rx="{rx * 0.55}" ry="{ry * 0.5}" fill="url(#warm)" opacity="0.30" filter="url(#soft60)"/>')
    out.append('</g>')
    return "".join(out)




def reactor(x, y, w=300, h=200, warm=0.35):
    out = [f'<g>']
    out.append(f'<ellipse cx="{x + w/2}" cy="{y+4}" rx="{w*0.6}" ry="12" fill="#000" opacity="0.45"/>')
    out.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="url(#concrete)"/>')
    out.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#000" opacity="0.12"/>')
    # блоки и вентиляция
    out.append(f'<rect x="{x+w*0.1}" y="{y-h-58}" width="{w*0.3}" height="58" fill="#2c343a"/>')
    out.append(f'<rect x="{x+w*0.52}" y="{y-h-34}" width="{w*0.26}" height="34" fill="#2c343a"/>')
    out.append(f'<rect x="{x+w*0.1}" y="{y-h-58}" width="{w*0.3}" height="4" fill="#6d777f" opacity="0.7"/>')
    for i in range(5):
        out.append(f'<rect x="{x+16+i*34}" y="{y-h+22}" width="18" height="12" fill="#ffb066" opacity="{warm}"/>')
    out.append('</g>')
    return "".join(out)


def ground(y, color="url(#ground)"):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="{color}"/>'
            f'<rect x="0" y="{y}" width="1080" height="6" fill="#8a949b" opacity="0.25"/>'
            f'<rect x="0" y="{y}" width="1080" height="220" fill="url(#haze)"/>')


def stars(n=70, seed=5):
    rnd = __import__("random").Random(seed)
    return "".join(f'<circle cx="{rnd.uniform(0,1080):.0f}" cy="{rnd.uniform(60,900):.0f}" r="{rnd.uniform(0.5,1.6):.1f}" fill="#cfe0ee" opacity="{rnd.uniform(0.15,0.7):.2f}"/>' for _ in range(n))


def dim_h(x1, x2, y, label, color="#a8e6f7"):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x1}" y1="{y-14}" x2="{x1}" y2="{y+14}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x2}" y1="{y-14}" x2="{x2}" y2="{y+14}" stroke="{color}" stroke-width="2"/>'
            f'<polygon points="{x1+6},{y} {x1+22},{y-5} {x1+22},{y+5}" fill="{color}"/>'
            f'<polygon points="{x2-6},{y} {x2-22},{y-5} {x2-22},{y+5}" fill="{color}"/>'
            + text((x1 + x2) / 2, y - 20, label, 30, color, "middle"))


def dim_v(y1, y2, x, label, color="#a8e6f7"):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x-14}" y1="{y1}" x2="{x+14}" y2="{y1}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x-14}" y1="{y2}" x2="{x+14}" y2="{y2}" stroke="{color}" stroke-width="2"/>'
            f'<g transform="translate({x+34} {(y1+y2)/2}) rotate(90)">{text(0, 0, label, 30, color, "middle")}</g>')


def scene1():
    b = [f'<rect width="1080" height="1920" fill="url(#skyDusk)"/>', stars()]
    b.append('<circle cx="880" cy="1240" r="520" fill="url(#sunGlow)"/>')
    b.append('<rect x="0" y="1280" width="1080" height="120" fill="#0a0f14" opacity="0.9"/>')
    b.append(ground(1330))
    b.append(reactor(150, 1430, 280, 190, 0.3))
    b.append(crane(980, 1470, 0.8))
    b.append(f'<g filter="url(#shadow)">{arch(560, 1490, 780, 690, 62, ribs=28)}</g>')
    b.append(truck(240, 1600, 0.9)); b.append(truck(880, 1610, 0.75, flip=True))
    b.append(human(410, 1650, 0.85)); b.append(human(700, 1660, 0.8))
    b.append(dust(120, 1200, 1750, 21))
    b.append('<rect x="0" y="0" width="1080" height="1920" fill="#05080c" opacity="0.18"/>')
    b.append(vignette())
    b.append(grain(0.06))
    return svg("".join(b))


def scene2():
    b = [f'<rect width="1080" height="1920" fill="#070b10"/>']
    # сетка чертежа
    for i in range(0, 1081, 90):
        b.append(f'<line x1="{i}" y1="0" x2="{i}" y2="1920" stroke="#0f1c26" stroke-width="1"/>')
    for j in range(0, 1921, 90):
        b.append(f'<line x1="0" y1="{j}" x2="1080" y2="{j}" stroke="#0f1c26" stroke-width="1"/>')
    b.append(ground(1450, "#0a0f14"))
    b.append(f'<g filter="url(#shadow)">{arch(540, 1440, 800, 660, 60, ribs=30)}</g>')
    b.append(dim_h(140, 940, 1330, "257 м — пролёт"))
    b.append(dim_v(1440, 780, 990, "108 м"))
    b.append(text(540, 600, "СТАЛЬНАЯ АРКА · 36 000 т", 28, "#7f93a3", "middle"))
    b.append(text(540, 1240, "162 м в длину · 36 000 тонн", 24, "#8f9aa4", "middle"))
    b.append(dust(60, 900, 1500, 8, "#8fb6c9", 0.25))
    b.append(vignette())
    b.append(grain(0.05))
    return svg("".join(b))


def scene3():
    b = [f'<rect width="1080" height="1920" fill="#080c10"/>']
    # местность сверху
    b.append('<rect x="40" y="420" width="1000" height="1040" fill="#101519"/>')
    for i in range(1, 9):
        b.append(f'<line x1="{40+i*111}" y1="420" x2="{40+i*111}" y2="1460" stroke="#1a232a" stroke-width="1.5"/>')
        b.append(f'<line x1="40" y1="{420+i*130}" x2="1040" y2="{420+i*130}" stroke="#1a232a" stroke-width="1.5"/>')
    # дороги
    b.append('<path d="M 60 980 L 420 900 L 800 760" stroke="#2a333a" stroke-width="26" fill="none" opacity="0.9"/>')
    b.append('<path d="M 60 980 L 420 900 L 800 760" stroke="#3d474f" stroke-width="2" stroke-dasharray="18 16" fill="none"/>')
    # площадка сборки
    b.append('<rect x="140" y="1060" width="380" height="300" fill="#20282e" stroke="#6fd3f2" stroke-width="3" stroke-dasharray="16 12"/>')
    b.append('<rect x="170" y="1090" width="320" height="240" fill="#2a343b" opacity="0.6"/>')
    b.append(text(330, 1150, "СБОРКА", 32, "#8fd8ef", "middle"))
    b.append(text(330, 1196, "6 лет, 300 м от блока", 21, "#5f7280", "middle"))
    # блок
    b.append('<circle cx="790" cy="740" r="96" fill="rgba(255,122,26,0.07)" stroke="#ff7a1a" stroke-width="3"/>')
    b.append('<circle cx="790" cy="740" r="34" fill="#3a2a20" stroke="#ffb066" stroke-width="2"/>')
    b.append(text(790, 748, "4", 40, "#ffb066", "middle"))
    # путь и маркеры
    b.append('<path d="M 520 1180 Q 650 1080 730 830" fill="none" stroke="#ff7a1a" stroke-width="6" stroke-dasharray="22 16"/>')
    b.append('<polygon points="736,810 714,850 754,842" fill="#ff7a1a"/>')
    for i, (mx, my) in enumerate([(556, 1140), (610, 1050), (668, 950)]):
        b.append(f'<circle cx="{mx}" cy="{my}" r="7" fill="#0b1116" stroke="#ffb066" stroke-width="3"/>')
    b.append(text(600, 1240, "327 м", 40, "#ffb066", "middle"))
    # масштаб
    b.append('<line x1="700" y1="1300" x2="940" y2="1300" stroke="#8f9aa4" stroke-width="3"/>')
    b.append('<line x1="700" y1="1290" x2="700" y2="1310" stroke="#8f9aa4" stroke-width="3"/>')
    b.append('<line x1="940" y1="1290" x2="940" y2="1310" stroke="#8f9aa4" stroke-width="3"/>')
    b.append(text(820, 1282, "100 м", 22, "#8f9aa4", "middle"))
    # север
    b.append('<path d="M 960 500 L 960 560" stroke="#5f7280" stroke-width="3"/><polygon points="960,486 950,512 970,512" fill="#5f7280"/>')
    b.append(text(960, 588, "С", 22, "#5f7280", "middle"))
    b.append(vignette())
    b.append(grain(0.05))
    return svg("".join(b))


def scene4():
    b = [f'<rect width="1080" height="1920" fill="#080c10"/>']
    # грунт и рельс
    b.append('<rect x="0" y="1250" width="1080" height="670" fill="#191b18"/>')
    b.append('<rect x="0" y="1250" width="1080" height="14" fill="#3b4038"/>')
    b.append('<rect x="0" y="1240" width="1080" height="12" fill="url(#rail)"/>')
    for x in range(16, 1080, 104):
        b.append(f'<rect x="{x}" y="1230" width="54" height="10" fill="#8f9ea9" opacity="0.75"/>')
    # нога арки над плитой
    b.append('<path d="M 300 720 L 380 720 L 380 1060 L 300 1060 Z" fill="url(#steel)" filter="url(#metalNoise)"/>')
    b.append('<path d="M 700 720 L 780 720 L 780 1060 L 700 1060 Z" fill="url(#steel)" filter="url(#metalNoise)"/>')
    for i in range(7):
        yy = 730 + i * 46
        b.append(f'<line x1="304" y1="{yy}" x2="376" y2="{yy+40}" stroke="#101820" stroke-width="3" opacity="0.45"/>')
        b.append(f'<line x1="704" y1="{yy}" x2="776" y2="{yy+40}" stroke="#101820" stroke-width="3" opacity="0.45"/>')
        b.append(f'<line x1="304" y1="{yy+40}" x2="376" y2="{yy}" stroke="#101820" stroke-width="2" opacity="0.3"/>')
    # опорная плита
    b.append('<rect x="220" y="1060" width="640" height="72" rx="6" fill="url(#steelDark)" stroke="#b6c6d2" stroke-width="3" filter="url(#metalNoise)"/>')
    b.append('<rect x="220" y="1060" width="640" height="10" fill="#dbe7ef" opacity="0.5"/>')
    # домкраты
    for x in (320, 540, 760):
        b.append(f'<rect x="{x-62}" y="1132" width="124" height="108" fill="#1e2a33" stroke="#7d93a3" stroke-width="3"/>')
        b.append(f'<rect x="{x-38}" y="1150" width="76" height="72" fill="#4a5a66" stroke="#9fb2c1" stroke-width="2"/>')
        b.append(f'<rect x="{x-14}" y="1060" width="28" height="72" fill="#c8d6e0" opacity="0.9"/>')
        b.append(f'<circle cx="{x}" cy="1148" r="5" fill="#ffb066"/>')
        b.append(f'<path d="M{x+58} 1200 q56 6 74 -40" stroke="#2f3d47" stroke-width="7" fill="none"/>')
    # насосная станция
    b.append('<rect x="840" y="1120" width="150" height="120" rx="6" fill="#243039" stroke="#5f7280" stroke-width="3"/>')
    b.append('<rect x="856" y="1136" width="118" height="42" fill="#3d4d59"/>')
    b.append('<circle cx="884" cy="1210" r="14" fill="#2b3944" stroke="#8f9ea9" stroke-width="2"/>')
    b.append('<circle cx="944" cy="1210" r="14" fill="#2b3944" stroke="#8f9ea9" stroke-width="2"/>')
    b.append(human(150, 1245, 0.95, "#0c1013", "#ffb066"))
    b.append('<circle cx="540" cy="1050" r="300" fill="url(#warm)" opacity="0.22" filter="url(#soft60)"/>')
    b.append(text(540, 610, "224 ГИДРАВЛИЧЕСКИХ ДОМКРАТА", 32, "#a8e6f7", "middle"))
    b.append(text(540, 656, "толкают опору по рельсам", 22, "#8f9aa4", "middle"))
    b.append(dust(36, 900, 1240, 33, "#ffd9b0", 0.25))
    b.append(vignette())
    b.append(grain(0.06))
    return svg("".join(b))


def scene5():
    b = [f'<rect width="1080" height="1920" fill="url(#skyDusk)"/>', stars(50, 9)]
    b.append('<circle cx="180" cy="1300" r="420" fill="url(#sunGlow)" opacity="0.7"/>')
    b.append(ground(1470))
    b.append('<rect x="0" y="1450" width="1080" height="20" fill="url(#rail)"/>')
    for x in range(20, 1080, 110):
        b.append(f'<rect x="{x}" y="1440" width="60" height="10" fill="#8f9ea9" opacity="0.65"/>')
    b.append(reactor(760, 1470, 260, 180, 0.45))
    b.append(crane(1010, 1470, 0.7))
    b.append(f'<g id="arch-move" filter="url(#shadow)">{arch(300, 1470, 520, 420, 44, ribs=22)}</g>')
    # пыль и свет фар
    b.append('<ellipse cx="300" cy="1470" rx="240" ry="26" fill="#b9a68c" opacity="0.12" filter="url(#soft24)"/>')
    b.append(truck(120, 1520, 0.8)); b.append(truck(980, 1540, 0.7, flip=True))
    b.append(human(470, 1530, 0.75)); b.append(human(560, 1535, 0.7))
    b.append(dust(110, 1250, 1600, 44))
    b.append(vignette())
    b.append(grain(0.06))
    return svg("".join(b))


def scene6():
    b = [f'<rect width="1080" height="1920" fill="url(#skyDusk)"/>', stars(60, 13)]
    b.append(ground(1520))
    b.append(reactor(360, 1520, 330, 220, 0.55))
    b.append(crane(1000, 1520, 0.75))
    b.append(f'<g filter="url(#shadow)">{arch(540, 1520, 780, 650, 58, ribs=26)}</g>')
    # пар
    b.append('<ellipse cx="430" cy="1300" rx="150" ry="60" fill="#c9d6df" opacity="0.10" filter="url(#soft60)"/>')
    b.append('<ellipse cx="620" cy="1240" rx="120" ry="50" fill="#c9d6df" opacity="0.08" filter="url(#soft60)"/>')
    b.append(human(480, 1540, 0.7)); b.append(human(600, 1540, 0.65))
    b.append(dust(70, 1200, 1600, 55, "#cfd8de", 0.25))
    b.append(vignette())
    b.append(grain(0.05))
    return svg("".join(b))


def scene7():
    b = [f'<rect width="1080" height="1920" fill="#070b10"/>']
    # крупный план повреждённой панели
    b.append('<rect x="0" y="0" width="1080" height="1920" fill="url(#steelDark)"/>')
    for i in range(0, 1081, 120):
        b.append(f'<line x1="{i}" y1="0" x2="{i}" y2="1920" stroke="#0a1015" stroke-width="4" opacity="0.6"/>')
    for j in range(0, 1921, 150):
        b.append(f'<line x1="0" y1="{j}" x2="1080" y2="{j}" stroke="#0a1015" stroke-width="3" opacity="0.5"/>')
    b.append('<path d="M 300 520 L 560 470 L 720 640 L 690 900 L 470 990 L 300 830 Z" fill="#03060a" stroke="#ff7a1a" stroke-width="3"/>')
    b.append('<path d="M 300 520 L 560 470 L 720 640" fill="none" stroke="#ffb066" stroke-width="5" opacity="0.85"/>')
    for x, y, r in ((380, 600, 26), (520, 700, 18), (610, 820, 22)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#000" opacity="0.6"/>')
    b.append('<circle cx="820" cy="1150" r="300" fill="url(#warm)" opacity="0.12" filter="url(#soft60)"/>')
    b.append(vignette())
    b.append(grain(0.07))
    return svg("".join(b), bg="#05080c")


SCENES = [
    ("s1", scene1(), 5), ("s2", scene2(), 7), ("s3", scene3(), 7),
    ("s4", scene4(), 8), ("s5", scene5(), 8), ("s6", scene6(), 7), ("s7", scene7(), 5),
]
