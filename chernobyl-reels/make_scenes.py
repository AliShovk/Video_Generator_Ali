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
    b.append(ground(1640))
    b.append(reactor(390, 1640, 300, 210))
    b.append(arch(540, 1640, 940, 800, 64, ribs=30))
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
    # рамка площадки
    b.append('<rect x="80" y="520" width="920" height="980" fill="none" stroke="#1d3746" stroke-width="2"/>')
    for i in range(1, 6):
        b.append(f'<line x1="{80+i*153}" y1="520" x2="{80+i*153}" y2="1500" stroke="#0f1f2a" stroke-width="1"/>')
        b.append(f'<line x1="80" y1="{520+i*163}" x2="1000" y2="{520+i*163}" stroke="#0f1f2a" stroke-width="1"/>')
    # площадка сборки
    b.append('<rect x="150" y="1080" width="360" height="280" fill="rgba(111,211,242,0.05)" stroke="#6fd3f2" stroke-width="3" stroke-dasharray="14 10"/>')
    b.append(text(330, 1160, "СБОРКА", 34, "#8fd8ef", "middle"))
    b.append(text(330, 1210, "здесь арку собрали", 22, "#5f7280", "middle"))
    # реактор
    b.append('<circle cx="770" cy="760" r="92" fill="rgba(255,122,26,0.08)" stroke="#ff7a1a" stroke-width="3"/>')
    b.append(text(770, 750, "4", 46, "#ffb066", "middle"))
    b.append(text(770, 800, "БЛОК", 20, "#ffb066", "middle"))
    # путь
    b.append('<path d="M 512 1200 Q 640 1120 720 870" fill="none" stroke="#ff7a1a" stroke-width="7" stroke-dasharray="20 14"/>')
    b.append('<polygon points="726,852 706,890 744,884" fill="#ff7a1a"/>')
    b.append(text(560, 1330, "327 м", 40, "#ffb066", "middle"))
    # масштабная линейка
    b.append('<line x1="150" y1="1440" x2="390" y2="1440" stroke="#5f7280" stroke-width="3"/>')
    b.append('<line x1="150" y1="1430" x2="150" y2="1450" stroke="#5f7280" stroke-width="3"/>')
    b.append('<line x1="390" y1="1430" x2="390" y2="1450" stroke="#5f7280" stroke-width="3"/>')
    b.append(text(270, 1424, "100 м", 22, "#5f7280", "middle"))
    return svg("".join(b))


def scene4():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1500))
    # рельс
    b.append('<rect x="0" y="1500" width="1080" height="34" fill="#2f3941"/>')
    b.append('<rect x="0" y="1486" width="1080" height="16" fill="#6b7d8a"/>')
    for x in range(24, 1080, 96):
        b.append(f'<rect x="{x}" y="1478" width="52" height="10" fill="#8b9aa6" opacity="0.7"/>')
    # стальная опорная плита (низ арки)
    b.append('<rect x="250" y="1210" width="580" height="86" fill="url(#steelDark)" stroke="#9fb2c2" stroke-width="4"/>')
    b.append('<path d="M 250 1210 L 330 1050 L 750 1050 L 830 1210 Z" fill="url(#steel)" stroke="#9fb2c2" stroke-width="4" opacity="0.95"/>')
    b.append('<path d="M 330 1050 L 750 1050" stroke="#dfeaf2" stroke-width="3" opacity="0.6"/>')
    # домкраты под плитой
    for x in (330, 540, 750):
        b.append(f'<rect x="{x-70}" y="1296" width="140" height="190" fill="#243039" stroke="#6fd3f2" stroke-width="3"/>')
        b.append(f'<rect x="{x-44}" y="1320" width="88" height="130" fill="#3d4d59" stroke="#8fd8ef" stroke-width="2"/>')
        for dx in (-30, 30):
            b.append(f'<line x1="{x+dx}" y1="1450" x2="{x+dx}" y2="1380" stroke="#8fd8ef" stroke-width="2" opacity="0.35"/>')
        b.append(f'<line x1="{x}" y1="1296" x2="{x}" y2="1252" stroke="#ff7a1a" stroke-width="4"/>')
        b.append(f'<polygon points="{x},1226 {x-9},1254 {x+9},1254" fill="#ff7a1a"/>')
    b.append(text(540, 960, "224 ГИДРАВЛИЧЕСКИХ ДОМКРАТА", 30, "#8fd8ef", "middle"))
    
    return svg("".join(b))


def scene5():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1500))
    b.append(reactor(760, 1500, 250, 185))
    b.append(f'<g id="arch-move">{arch(340, 1500, 540, 430, 44, ribs=22)}</g>')
    # рельсы
    b.append('<rect x="0" y="1500" width="1080" height="18" fill="#39434c"/>')
    for x in range(40, 1080, 90):
        b.append(f'<rect x="{x}" y="1494" width="46" height="8" fill="#5a6b78" opacity="0.7"/>')
    b.append(text(540, 900, "СБОРКА  →  РЕАКТОР", 26, "#7f93a3", "middle"))
    return svg("".join(b))


def scene6():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1540))
    b.append(reactor(360, 1540, 320, 220))
    b.append(arch(540, 1540, 760, 640, 54, ribs=24))
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
    ("s2", scene2(), 7),
    ("s3", scene3(), 7),
    ("s4", scene4(), 8),
    ("s5", scene5(), 8),
    ("s6", scene6(), 7),
    ("s7", scene7(), 5),
]
