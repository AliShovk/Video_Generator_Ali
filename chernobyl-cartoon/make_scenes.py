#!/usr/bin/env python3
"""Чернобыльская арка — плоская мультяшная подача (как референс): разрез, яркие цвета, жёлтые плашки."""
from pathlib import Path

OUT = Path("/root/video-gen/chernobyl-cartoon/compositions")
OUT.mkdir(parents=True, exist_ok=True)

SKY_T, SKY_B = "#79c6f3", "#d3ecfd"
GRASS, GRASS_D = "#63bf46", "#4ea336"
SOIL, SOIL_L, SOIL_D = "#8a5a30", "#9d6b3c", "#6d4522"
WALL, ROOF = "#f4f0e4", "#b03a2e"
STEEL, STEEL_S, STEEL_L = "#e2eaef", "#b9c7d1", "#8ea3b0"
YELLOW, INK = "#f7c93f", "#241f1a"
BLUE, BLUE_D = "#2aa7e0", "#1b7fb0"

W, H = 1080, 1920


def svg(body):
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>'
            f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY_T}"/><stop offset="1" stop-color="{SKY_B}"/></linearGradient>'
            f'<linearGradient id="steel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f7fa"/><stop offset="1" stop-color="{STEEL_S}"/></linearGradient>'
            f'</defs>'
            f'<rect width="1080" height="1920" fill="url(#sky)"/>{body}</svg>')


def t(x, y, s, size=30, color=INK, anchor="start", weight="800", ls=0):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}">{s}</text>')


def pill(cx, cy, text, size=38, pad=30, fill=YELLOW, color=INK):
    w = len(text) * size * 0.56 + pad * 2
    h = size + pad * 1.15
    return (f'<rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h/2:.0f}" fill="{fill}"/>'
            + t(cx, cy + size * 0.34, text, size, color, "middle"))


def cloud(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" opacity="0.95">'
            f'<ellipse cx="0" cy="0" rx="70" ry="34" fill="#ffffff"/>'
            f'<ellipse cx="-40" cy="8" rx="44" ry="24" fill="#ffffff"/>'
            f'<ellipse cx="42" cy="10" rx="48" ry="26" fill="#ffffff"/>'
            f'</g>')


def tree(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-7" y="-40" width="14" height="48" rx="4" fill="#7a5230"/>'
            f'<circle cx="0" cy="-70" r="46" fill="{GRASS_D}"/>'
            f'<circle cx="-28" cy="-52" r="30" fill="{GRASS}"/>'
            f'<circle cx="30" cy="-54" r="32" fill="{GRASS}"/>'
            f'</g>')


def person(x, y, s=1.0, body="#2f4a5a", helmet=YELLOW):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-11" y="-52" width="22" height="34" rx="8" fill="{body}"/>'
            f'<rect x="-10" y="-20" width="8" height="22" rx="4" fill="#24323c"/>'
            f'<rect x="2" y="-20" width="8" height="22" rx="4" fill="#24323c"/>'
            f'<circle cx="0" cy="-62" r="11" fill="#f0c39a"/>'
            f'<path d="M-13 -66 a13 11 0 0 1 26 0 z" fill="{helmet}"/>'
            f'</g>')


def truck(x, y, s=1.0, col="#3a5a6e"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-46" y="-34" width="34" height="30" rx="8" fill="{col}"/>'
            f'<rect x="-12" y="-28" width="62" height="24" rx="8" fill="{col}"/>'
            f'<rect x="-52" y="-10" width="106" height="14" rx="7" fill="#22323c"/>'
            f'<circle cx="-30" cy="4" r="10" fill="#1b262e"/><circle cx="30" cy="4" r="10" fill="#1b262e"/>'
            f'</g>')


def ground_cut(y=1150):
    """Небо -> трава -> разрез грунта."""
    out = [f'<rect x="0" y="{y}" width="1080" height="80" fill="{GRASS}"/>',
           f'<rect x="0" y="{y+26}" width="1080" height="14" fill="{GRASS_D}" opacity="0.55"/>',
           f'<rect x="0" y="{y+80}" width="1080" height="{1920-y-80}" fill="{SOIL}"/>']
    # текстурные пятна грунта
    spots = [(90, 1290, 26), (300, 1360, 18), (520, 1420, 30), (760, 1330, 22), (940, 1470, 28),
             (170, 1560, 24), (420, 1620, 20), (650, 1540, 26), (860, 1650, 18), (1010, 1580, 22),
             (60, 1430, 16), (250, 1690, 22), (560, 1750, 26), (790, 1710, 18), (990, 1760, 24)]
    for x, yy, r in spots:
        out.append(f'<ellipse cx="{x}" cy="{yy}" rx="{r}" ry="{r*0.62:.0f}" fill="{SOIL_L}" opacity="0.75"/>')
    out.append(f'<rect x="0" y="{y+80}" width="1080" height="22" fill="{SOIL_D}" opacity="0.5"/>')
    return "".join(out)


def house(x, y, w=250, h=230, roof=True):
    """Карточный домик-реактор: белые стены, красная крыша."""
    out = [f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="10" fill="{WALL}"/>']
    if roof:
        out.append(f'<path d="M {x-24} {y-h} L {x+w/2} {y-h-95} L {x+w+24} {y-h} Z" fill="{ROOF}"/>')
    out.append(f'<rect x="{x+30}" y="{y-h+50}" width="54" height="54" rx="8" fill="#bfe3f5" stroke="#9dc4d8" stroke-width="4"/>')
    out.append(f'<rect x="{x+w-84}" y="{y-h+50}" width="54" height="54" rx="8" fill="#bfe3f5" stroke="#9dc4d8" stroke-width="4"/>')
    out.append(f'<rect x="{x+w/2-26}" y="{y-96}" width="52" height="96" rx="8" fill="#cbb79a"/>')
    return "".join(out)


def arch(cx, base_y, span, height, thick=44, ribs=16):
    """Полуэллиптическая арка в мультяшном стиле."""
    rx, ry = span / 2, height
    x0, x1 = cx - rx, cx + rx
    irx, iry = rx - thick, ry - thick * 0.95
    body = (f"M {x0} {base_y} A {rx} {ry} 0 0 1 {x1} {base_y} "
            f"L {cx+irx} {base_y} A {irx} {iry} 0 0 0 {cx-irx} {base_y} Z")
    out = [f'<path d="{body}" fill="url(#steel)"/>']
    # тёмная внутренняя кромка
    out.append(f'<path d="M {cx-irx} {base_y} A {irx} {iry} 0 0 1 {cx+irx} {base_y}" fill="none" stroke="{STEEL_L}" stroke-width="8"/>')
    for i in range(1, ribs):
        a = 3.14159 * i / ribs
        import math
        ox, oy = cx - rx * math.cos(a), base_y - ry * math.sin(a)
        ix, iy = cx - irx * math.cos(a), base_y - iry * math.sin(a)
        out.append(f'<line x1="{ox:.0f}" y1="{oy:.0f}" x2="{ix:.0f}" y2="{iy:.0f}" stroke="{STEEL_L}" stroke-width="5" opacity="0.75"/>')
    # блик
    out.append(f'<path d="M {x0+40} {base_y-6} A {rx-40} {ry-20} 0 0 1 {cx-40} {base_y-ry+18}" fill="none" stroke="#ffffff" stroke-width="8" opacity="0.55"/>')
    return "".join(out)
