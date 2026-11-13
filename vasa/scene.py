#!/usr/bin/env python3
"""«Васа»: корабль, который утонул через 1300 метров. 50 с, 9:16."""
import math
import random
from pathlib import Path

OUT = Path("/root/video-gen/vasa/compositions")
OUT.mkdir(parents=True, exist_ok=True)

SKY = "#bfe0f2"
SEA = "#2f6f96"
SEA_D = "#245a7d"
HULL = "#8a5a34"
HULL_D = "#6b4227"
GOLD = "#d9a441"
RED = "#b83227"
INK = "#1d2733"

DEFS = f"""
<defs>
  <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#d7ecf9"/><stop offset="0.7" stop-color="{SKY}"/><stop offset="1" stop-color="#e8f2f8"/>
  </linearGradient>
  <linearGradient id="seaG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5b9cc0"/><stop offset="0.4" stop-color="{SEA}"/><stop offset="1" stop-color="{SEA_D}"/>
  </linearGradient>
  <linearGradient id="hullG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#a06a3f"/><stop offset="1" stop-color="{HULL_D}"/>
  </linearGradient>
  <linearGradient id="goldG" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f0c25c"/><stop offset="1" stop-color="#b8862c"/>
  </linearGradient>
  <radialGradient id="glow"><stop offset="0" stop-color="#ffe9a8" stop-opacity="0.55"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
</defs>
"""


def sea(y, h=520, cls="sea"):
    waves = "".join(
        f'<path class="wave" d="M {x} {y + 40 + (i % 3) * 46} q 60 -16 120 0" stroke="#bfe0f5" stroke-width="5" fill="none" opacity="0.55"/>'
        for i, x in enumerate(range(-60, 1140, 120)))
    return (f'<rect class="{cls}" x="0" y="{y}" width="1080" height="{h}" fill="url(#seaG)"/>'
            f'<rect x="0" y="{y}" width="1080" height="10" fill="#7fb3cf" opacity="0.8"/>{waves}')


def gull(x, y, s=1.0):
    return (f'<g class="gull" transform="translate({x} {y}) scale({s})">'
            f'<path d="M -16 0 q 8 -10 16 0 q 8 -10 16 0" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/></g>')


def cloud(x, y, s=1.0, cls="cloud"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})" opacity="0.9">'
            f'<ellipse cx="0" cy="0" rx="80" ry="30" fill="#ffffff"/><ellipse cx="-42" cy="8" rx="46" ry="22" fill="#ffffff"/>'
            f'<ellipse cx="40" cy="10" rx="52" ry="24" fill="#ffffff"/></g>')


def person(x, y, s=1.0, col="#2b3560"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="-30" r="6" fill="#f0c8a0"/><path d="M -7 -24 L 7 -24 L 5 -6 L -5 -6 Z" fill="{col}"/>'
            f'<rect x="-5" y="-8" width="4" height="12" fill="#20304a"/><rect x="1" y="-8" width="4" height="12" fill="#20304a"/></g>')


def crowd(n=14, y=1500, seed=4):
    r = random.Random(seed)
    cols = ["#2b3560", "#7a3f3f", "#3f6f5a", "#5a4a7a", "#8a6a3a", "#35506e"]
    out = []
    for i in range(n):
        x = r.uniform(30, 1050)
        out.append(person(x, y + r.uniform(-18, 24), r.uniform(0.9, 1.3), r.choice(cols)).replace("<g ", '<g class="walker" ', 1))
    return "".join(out)


def ship(x=540, y=1180, s=1.0, heel=0, ident="ship", guns=True, sails=True):
    """Галеон: корпус, два пушечных дека, три мачты, паруса, корма."""
    p = [f'<g transform="translate({x} {y}) scale({s})"><g id="{ident}" transform="rotate({heel})">']
    # корпус
    p.append(f'<path d="M -300 -40 q 40 96 120 110 l 340 0 q 90 -18 130 -110 z" fill="url(#hullG)" stroke="{HULL_D}" stroke-width="4"/>')
    p.append(f'<path d="M -300 -40 l 560 0 l 30 -46 l -600 0 z" fill="{GOLD}" opacity="0.9"/>')
    p.append(f'<rect x="-292" y="-86" width="600" height="40" fill="{HULL}" stroke="{HULL_D}" stroke-width="3"/>')
    # пушечные порты
    if guns:
        for row, yy in ((0, -118), (1, -70)):
            for i in range(12):
                px = -270 + i * 50
                p.append(f'<rect x="{px}" y="{yy}" width="26" height="26" rx="4" fill="{RED}"/>')
                p.append(f'<rect x="{px+6}" y="{yy+8}" width="14" height="9" rx="4" fill="#2a1b12"/>')
    # палуба и надстройка
    p.append(f'<rect x="-200" y="-150" width="360" height="26" fill="{HULL_D}"/>')
    p.append(f'<path d="M -250 -150 q 60 -70 180 -64 q 40 6 60 64 z" fill="{HULL}"/>')
    # корма с резьбой
    p.append(f'<path d="M 200 -40 q 40 -60 30 -130 l -70 0 q 10 70 -20 130 z" fill="{GOLD}"/>')
    p.append(f'<circle cx="196" cy="-120" r="12" fill="#7a2f22"/>')
    # мачты и паруса
    masts = [(-150, -150, 470), (30, -170, 540), (190, -160, 430)]
    for mx, my, hh in masts:
        p.append(f'<rect x="{mx-5}" y="{my-hh}" width="10" height="{hh}" fill="#6b4a2a"/>')
        if sails:
            for k, (dy, w, hgt) in enumerate(((-40, 150, 120), (-180, 120, 100))):
                p.append(f'<path class="sail" d="M {mx-w/2} {my+dy-hgt} q {w/2} 18 {w} 0 l 0 {hgt} q {-w/2} 16 {-w} 0 z" fill="#f7f2e6" stroke="#ddd3bf" stroke-width="3"/>')
        p.append(f'<line x1="{mx}" y1="{my-hh}" x2="{mx-70}" y2="{my-hh+70}" stroke="#6b4a2a" stroke-width="3"/>')
        p.append(f'<line x1="{mx}" y1="{my-hh+60}" x2="{mx+80}" y2="{my-hh+140}" stroke="#6b4a2a" stroke-width="3"/>')
        p.append(f'<path class="flag" d="M {mx} {my-hh-4} l 46 8 l -46 12 z" fill="{GOLD}"/>')
    # бушприт
    p.append(f'<line x1="-300" y1="-50" x2="-430" y2="-130" stroke="#6b4a2a" stroke-width="10"/>')
    p.append('</g></g>')
    return "".join(p)


def block(x, y, w, h, col, op=1.0, cls=""):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{col}" opacity="{op}"/>'


def label(x, y, t, size=40, col=INK, weight=900, anchor="start", cls="lbl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{col}" text-anchor="{anchor}">{t}</text>')
