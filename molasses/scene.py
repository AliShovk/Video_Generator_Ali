#!/usr/bin/env python3
"""Общие элементы: «Волна патоки», Бостон 1919."""
import random

NIGHT = "#0e1418"
SKY = "#1b2a33"
BRICK = "#5b3a2e"
BRICK_L = "#7a4f3c"
MOL = "#4a2b12"
MOL_L = "#6b3f1a"
STEEL = "#8d99a3"
STEEL_D = "#5f6b74"
GOLD = "#e0a33e"
CREAM = "#f0e6d2"
RED = "#c0392b"

DEFS = f"""
<defs>
  <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#243642"/><stop offset="0.6" stop-color="{SKY}"/><stop offset="1" stop-color="#101a20"/></linearGradient>
  <linearGradient id="molG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MOL_L}"/><stop offset="0.5" stop-color="{MOL}"/><stop offset="1" stop-color="#2a1808"/></linearGradient>
  <linearGradient id="steelG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6d7881"/><stop offset="0.45" stop-color="#a9b4bd"/><stop offset="1" stop-color="#5a636b"/></linearGradient>
  <radialGradient id="lampG"><stop offset="0" stop-color="#ffe9b0" stop-opacity="0.55"/><stop offset="1" stop-color="#ffe9b0" stop-opacity="0"/></radialGradient>
</defs>
"""


def tank(x, y, w=380, h=620, ident="tank"):
    """Резервуар с клёпкой и подтёками."""
    r = random.Random(7)
    rivets = []
    for row in range(int(h // 42)):
        for i in range(9):
            rivets.append(f'<circle cx="{x + 18 + i * (w - 36) / 8:.0f}" cy="{y - 30 - row * 42}" r="4.5" fill="{STEEL_D}"/>')
    leaks = "".join(
        f'<path class="leak" d="M {x + 40 + i * 46} {y - 120 - (i % 5) * 90} q 6 34 0 62" stroke="{MOL}" '
        f'stroke-width="{6 + i % 4}" fill="none" opacity="0.85"/>' for i in range(7))
    return (f'<g id="{ident}">'
            f'<ellipse cx="{x + w/2}" cy="{y - h}" rx="{w/2}" ry="26" fill="{STEEL}"/>'
            f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="url(#steelG)"/>'
            f'<ellipse cx="{x + w/2}" cy="{y}" rx="{w/2}" ry="26" fill="{STEEL_D}"/>'
            f'<rect x="{x}" y="{y - h * 0.55}" width="{w}" height="12" fill="{STEEL_D}" opacity="0.6"/>'
            f'<rect x="{x}" y="{y - h * 0.25}" width="{w}" height="12" fill="{STEEL_D}" opacity="0.6"/>'
            f'{"".join(rivets)}{leaks}'
            f'<path d="M {x + w - 40} {y - h + 10} l 0 -60 l 26 0 l 0 60" fill="{STEEL_D}"/>'
            f'</g>')


def wave(x, y, w=1200, h=420, cls="wave"):
    crest = (f"M {x} {y} q {w*0.25} -{h*0.95} {w*0.5} -{h*0.6} q {w*0.18} {h*0.18} {w*0.5} -{h*0.22}")
    foam = "".join(
        f'<ellipse cx="{x + w*0.18 + i*46}" cy="{y - h*0.62 + (i%3)*14}" rx="{18 + (i%4)*7}" ry="{8 + i%3*4}" '
        f'fill="#8a5a2a" opacity="0.55"/>' for i in range(12))
    return (f'<g class="{cls}">'
            f'<path d="{crest} l 0 {h} l -{w} 0 z" fill="url(#molG)"/>'
            f'<path d="{crest}" stroke="#7a4a1e" stroke-width="10" fill="none" opacity="0.8"/>'
            f'{foam}</g>')


def person(x, y, s=1.0, col="#20262c", run=False):
    lean = 12 if run else 0
    return (f'<g transform="translate({x} {y}) scale({s}) rotate({lean})">'
            f'<circle cx="0" cy="-52" r="9" fill="#e8c9a8"/>'
            f'<rect x="-9" y="-44" width="18" height="30" rx="6" fill="{col}"/>'
            f'<rect x="-8" y="-14" width="6" height="18" fill="#1a1f24"/><rect x="2" y="-14" width="6" height="18" fill="#1a1f24"/>'
            f'<rect x="-8" y="-14" width="6" height="9" fill="#1a1f24"/><rect x="2" y="-14" width="6" height="9" fill="#1a1f24"/></g>')


def building(x, y, w, h, col=BRICK, win=4):
    out = [f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{col}"/>',
           f'<rect x="{x}" y="{y - h}" width="{w}" height="10" fill="{BRICK_L}"/>']
    for r in range(int(h // 90)):
        for c in range(win):
            out.append(f'<rect x="{x + 16 + c * (w - 32) / max(win,1):.0f}" y="{y - h + 30 + r * 90}" '
                       f'width="22" height="34" rx="3" fill="#ffd98a" opacity="{0.25 + 0.5*((r+c) % 3 == 0)}"/>')
    return "".join(out)


def label(x, y, t, size=46, col=CREAM, weight=900, anchor="start", cls="lbl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{col}" text-anchor="{anchor}">{t}</text>')
