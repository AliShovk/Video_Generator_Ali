#!/usr/bin/env python3
"""Чернобыльская арка — 7 сцен, 2D-инфографика, 1080×1920."""
import math
from pathlib import Path

OUT = Path("/root/video-gen/chernobyl/compositions")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920

DEFS = """
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#05080c"/><stop offset="0.6" stop-color="#0b141c"/><stop offset="1" stop-color="#04070a"/>
  </linearGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#9fb2c2"/><stop offset="0.5" stop-color="#5d7180"/><stop offset="1" stop-color="#33424d"/>
  </linearGradient>
  <linearGradient id="steelDark" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#4a5b68"/><stop offset="1" stop-color="#222d36"/>
  </linearGradient>
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#20262b"/><stop offset="1" stop-color="#0c1014"/>
  </linearGradient>
  <linearGradient id="concrete" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3a4148"/><stop offset="1" stop-color="#1c2126"/>
  </linearGradient>
  <linearGradient id="glow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff7a1a" stop-opacity="0.55"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="halo" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#6fd3f2" stop-opacity="0.25"/><stop offset="1" stop-color="#6fd3f2" stop-opacity="0"/>
  </radialGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
  <pattern id="panels" width="26" height="26" patternUnits="userSpaceOnUse">
    <rect width="26" height="26" fill="none"/>
    <line x1="0" y1="0" x2="0" y2="26" stroke="#0d151b" stroke-width="3" opacity="0.45"/>
    <line x1="0" y1="13" x2="26" y2="13" stroke="#0d151b" stroke-width="1.5" opacity="0.25"/>
  </pattern>
  <pattern id="hatch" width="10" height="10" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="10" stroke="#8b98a3" stroke-width="1" opacity="0.35"/>
  </pattern>
</defs>
"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def text(x, y, s, size=30, color="#e9e4da", anchor="start", mono=True, ls=2, weight="400"):
    fam = "JetBrains Mono, monospace" if mono else "Inter, sans-serif"
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{fam}" font-size="{size}" letter-spacing="{ls}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def dim_h(x1, x2, y, label, color="#6fd3f2"):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x1}" y1="{y-12}" x2="{x1}" y2="{y+12}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x2}" y1="{y-12}" x2="{x2}" y2="{y+12}" stroke="{color}" stroke-width="2"/>'
            + text((x1 + x2) / 2, y - 18, label, 30, color, "middle"))


def dim_v(y1, y2, x, label, color="#6fd3f2"):
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x-12}" y1="{y1}" x2="{x+12}" y2="{y1}" stroke="{color}" stroke-width="2"/>'
            f'<line x1="{x-12}" y1="{y2}" x2="{x+12}" y2="{y2}" stroke="{color}" stroke-width="2"/>')


def arch(cx, base_y, span, height, thickness=46, fill="url(#steel)", ribs=26, opacity=1.0, panels=True):
    """Полуэллиптическая арка с ферменными рёбрами и панелями."""
    rx, ry = span / 2, height
    x0, x1 = cx - rx, cx + rx
    irx, iry = rx - thickness, ry - thickness * 0.92
    outer = f"M {x0} {base_y} A {rx} {ry} 0 0 1 {x1} {base_y}"
    inner = f"M {cx - irx} {base_y} A {irx} {iry} 0 0 1 {cx + irx} {base_y}"
    body = f"{outer} L {cx + irx} {base_y} A {irx} {iry} 0 0 0 {cx - irx} {base_y} Z"
    out = [f'<path d="{body}" fill="{fill}" opacity="{opacity}"/>']
    if panels:
        out.append(f'<path d="{body}" fill="url(#panels)" opacity="0.55"/>')
    # рёбра (радиальные линии по дуге)
    import math as _m
    for i in range(1, ribs):
        a = _m.pi * i / ribs
        ox, oy = cx - rx * _m.cos(a), base_y - ry * _m.sin(a)
        ix, iy = cx - irx * _m.cos(a), base_y - iry * _m.sin(a)
        out.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#1a232b" stroke-width="{max(2, thickness*0.09):.1f}" opacity="0.65"/>')
    # раскосы между рёбрами
    for i in range(ribs - 1):
        a1 = _m.pi * i / ribs
        a2 = _m.pi * (i + 1) / ribs
        ox1, oy1 = cx - rx * _m.cos(a1), base_y - ry * _m.sin(a1)
        ix2, iy2 = cx - irx * _m.cos(a2), base_y - iry * _m.sin(a2)
        out.append(f'<line x1="{ox1:.1f}" y1="{oy1:.1f}" x2="{ix2:.1f}" y2="{iy2:.1f}" stroke="#22303a" stroke-width="2" opacity="0.45"/>')
    out.append(f'<path d="{outer}" fill="none" stroke="#c9d8e3" stroke-width="3.5" opacity="0.85"/>')
    out.append(f'<path d="{inner}" fill="none" stroke="#7f93a3" stroke-width="2" opacity="0.55"/>')
    # торцевые стойки
    for xx in (x0, x1):
        out.append(f'<rect x="{xx-6}" y="{base_y-40}" width="12" height="40" fill="#7f93a3" opacity="0.7"/>')
    return "".join(out)


def reactor(x, y, w=300, h=210):
    out = [f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="url(#concrete)" stroke="#4a555e" stroke-width="3"/>']
    # руины/вентиляция
    out.append(f'<rect x="{x+w*0.15}" y="{y-h-60}" width="{w*0.28}" height="60" fill="#2b3238" stroke="#4a555e" stroke-width="2"/>')
    out.append(f'<rect x="{x+w*0.55}" y="{y-h-40}" width="{w*0.22}" height="40" fill="#2b3238" stroke="#4a555e" stroke-width="2"/>')
    for i in range(4):
        out.append(f'<rect x="{x+18+i*36}" y="{y-h+24}" width="22" height="16" fill="#ffb066" opacity="0.35"/>')
    return "".join(out)


def ground(y=1560):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="url(#ground)"/>'
            f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#3a4a55" stroke-width="3"/>')


def scene1():
    b = [f'<rect width="1080" height="1920" fill="url(#sky)"/>']
    b.append('<circle cx="540" cy="1500" r="520" fill="url(#halo)"/>')
    b.append(ground(1560))
    b.append(reactor(350, 1560, 300, 210))
    b.append(arch(540, 1560, 760, 620, 54, ribs=22))
    b.append('<rect x="0" y="1560" width="1080" height="360" fill="#05080b" opacity="0.35"/>')
    return svg("".join(b))


def scene2():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append('<rect x="0" y="0" width="1080" height="1920" fill="url(#sky)" opacity="0.7"/>')
    b.append(arch(540, 1440, 780, 640, 60, ribs=30))
    b.append(dim_h(150, 930, 1520, "257 м — пролёт"))
    b.append(dim_v(1440, 800, 1000, ""))
    b.append(f'<g transform="translate(995 1120) rotate(90)">{text(0, 0, "108 м", 30, "#6fd3f2", "middle")}</g>')
    b.append(text(540, 640, "СТАЛЬНАЯ АРКА", 30, "#8f9aa4", "middle"))
    return svg("".join(b))


def scene3():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    # план сверху
    b.append('<rect x="90" y="420" width="900" height="1100" fill="none" stroke="#22404f" stroke-width="2"/>')
    for i in range(1, 10):
        b.append(f'<line x1="{90+i*90}" y1="420" x2="{90+i*90}" y2="1520" stroke="#122330" stroke-width="1"/>')
    for i in range(1, 12):
        b.append(f'<line x1="90" y1="{420+i*92}" x2="990" y2="{420+i*92}" stroke="#122330" stroke-width="1"/>')
    # реактор
    b.append('<circle cx="760" cy="760" r="60" fill="#2b3238" stroke="#ff7a1a" stroke-width="3"/>')
    b.append(text(760, 770, "4", 34, "#ffb066", "middle"))
    # площадка сборки
    b.append('<rect x="150" y="1080" width="300" height="220" fill="none" stroke="#6fd3f2" stroke-width="3" stroke-dasharray="12 10"/>')
    b.append(text(300, 1200, "СБОРКА", 30, "#8fd8ef", "middle"))
    # путь
    b.append('<path d="M 450 1180 Q 620 1100 700 860" fill="none" stroke="#ff7a1a" stroke-width="6" stroke-dasharray="18 14"/>')
    b.append('<polygon points="706,846 690,876 722,872" fill="#ff7a1a"/>')
    b.append(text(560, 1010, "327 м", 32, "#ffb066", "middle"))
    b.append(text(300, 1340, "В 300 м ОТ БЛОКА", 26, "#7f93a3", "middle"))
    return svg("".join(b))


def scene4():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1420))
    # рельсы
    b.append('<rect x="0" y="1420" width="1080" height="26" fill="#39434c"/>')
    b.append('<rect x="0" y="1400" width="1080" height="12" fill="#5a6b78"/>')
    # нога арки и домкраты
    b.append('<rect x="380" y="900" width="110" height="520" fill="url(#steelDark)" stroke="#7f93a3" stroke-width="3"/>')
    for i, x in enumerate([300, 380, 460, 540]):
        b.append(f'<rect x="{x}" y="1330" width="64" height="80" fill="#2a333c" stroke="#6fd3f2" stroke-width="2"/>')
        b.append(f'<rect x="{x+8}" y="1300" width="48" height="34" fill="#4a5b68" stroke="#8fd8ef" stroke-width="2"/>')
    for x in (332, 412, 492, 572):
        b.append(f'<path d="M{x} 1290 v-40" stroke="#ff7a1a" stroke-width="4"/>')
        b.append(f'<polygon points="{x},1240 {x-8},1258 {x+8},1258" fill="#ff7a1a"/>')
    b.append(text(540, 1180, "224 ГИДРАВЛИЧЕСКИХ ДОМКРАТА", 30, "#8fd8ef", "middle"))
    b.append(text(540, 1520, "НАПРАВЛЯЮЩИЕ", 26, "#7f93a3", "middle"))
    return svg("".join(b))


def scene5():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1500))
    b.append(reactor(700, 1500, 260, 190))
    b.append(f'<g id="arch-move">{arch(250, 1500, 420, 340, 38, ribs=18)}</g>')
    # рельсы
    b.append('<rect x="0" y="1500" width="1080" height="18" fill="#39434c"/>')
    for x in range(40, 1080, 90):
        b.append(f'<rect x="{x}" y="1494" width="46" height="8" fill="#5a6b78" opacity="0.7"/>')
    b.append(text(540, 760, "СБОРКА → РЕАКТОР", 26, "#7f93a3", "middle"))
    return svg("".join(b))


def scene6():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1540))
    b.append(reactor(360, 1540, 320, 220))
    b.append(arch(540, 1540, 820, 660, 56, ribs=24))
    b.append('<rect x="360" y="1320" width="320" height="220" fill="url(#glow)" opacity="0.35"/>')
    b.append(text(540, 780, "ЗАЩИТНЫЙ КОНФАЙНМЕНТ", 32, "#cfdae4", "middle"))
    b.append(text(540, 830, "срок службы — 100 лет", 26, "#7f93a3", "middle"))
    return svg("".join(b))


def scene7():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append('<circle cx="540" cy="760" r="420" fill="url(#halo)" opacity="0.5"/>')
    b.append(text(540, 700, "ФЕВРАЛЬ 2025", 74, "#ff7a1a", "middle"))
    b.append(text(540, 800, "АРКА ПОВРЕЖДЕНА", 46, "#e9e4da", "middle"))
    b.append(text(540, 900, "восстановление ещё не завершено", 28, "#8f8a80", "middle"))
    b.append('<line x1="240" y1="960" x2="840" y2="960" stroke="#2a3540" stroke-width="2"/>')
    b.append(text(540, 1030, "ИСТОРИЯ СТРОИТЕЛЬСТВА", 26, "#6f7a84", "middle"))
    b.append(text(540, 1072, "НЕ ЗНАЧИТ, ЧТО ОБЪЕКТ СЕЙЧАС В СТРОЮ", 22, "#4f5a64", "middle"))
    return svg("".join(b))


SCENES = [
    ("s1", scene1(), 5),
    ("s2", scene2(), 8),
    ("s3", scene3(), 10),
    ("s4", scene4(), 12),
    ("s5", scene5(), 11),
    ("s6", scene6(), 8),
    ("s7", scene7(), 6),
]
