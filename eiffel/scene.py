#!/usr/bin/env python3
"""Эйфелева башня растёт за день — 42 с, 9:16, много движения."""
import random
from pathlib import Path

OUT = Path("/root/video-gen/eiffel/compositions")
OUT.mkdir(parents=True, exist_ok=True)

SKY1, SKY2 = "#8fc9ef", "#e8f4ff"
IRON, IRON_D, IRON_L = "#6b5545", "#4a3a2e", "#8a6f58"
GROUND, PATH = "#7fbf5a", "#d8cbb0"
SUN, SUN2 = "#ffd166", "#ffe9a8"
INK = "#20242c"

DEFS = """<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#7cc0ea"/><stop offset="0.55" stop-color="#bfe0f5"/><stop offset="1" stop-color="#eef7ff"/>
  </linearGradient>
  <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#7fc75a"/><stop offset="1" stop-color="#5aa63c"/>
  </linearGradient>
  <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ffe9a8" stop-opacity="0.95"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ironG" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#4a3a2e"/><stop offset="0.5" stop-color="#8a6f58"/><stop offset="1" stop-color="#4a3a2e"/>
  </linearGradient>
</defs>"""


def cloud(x, y, s=1.0, cls="cloud"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})" opacity="0.95">'
            f'<ellipse cx="0" cy="0" rx="80" ry="36" fill="#fff"/><ellipse cx="-46" cy="10" rx="48" ry="26" fill="#fff"/>'
            f'<ellipse cx="48" cy="12" rx="54" ry="28" fill="#fff"/></g>')


def bird(x, y, s=1.0):
    return (f'<path class="bird" d="M {x-14*s} {y} q {7*s} {-8*s} {14*s} 0 q {7*s} {-8*s} {14*s} 0" '
            f'stroke="{INK}" stroke-width="{2.4*s}" fill="none" stroke-linecap="round" opacity="0.55"/>')


def person(x, y, s=1.0, color="#2b3560", cls="walker"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<circle cx="0" cy="-26" r="5" fill="#f2c39d"/>'
            f'<rect x="-4" y="-21" width="8" height="14" rx="3" fill="{color}"/>'
            f'<rect x="-4" y="-8" width="3" height="9" fill="#1f2740"/><rect x="1" y="-8" width="3" height="9" fill="#1f2740"/>'
            f'</g>')


def tower(x, base, h=760, w=300, ident="tower"):
    """Эйфелева башня: 4 опоры, арка, 3 платформы, решётка, антенна."""
    top = base - h
    half_b, half_t = w / 2, w * 0.055
    silhouette = (f"M {x-half_b} {base} "
                  f"C {x-half_b*0.78} {base-h*0.34}, {x-half_t*3.2} {base-h*0.62}, {x-half_t} {top} "
                  f"L {x+half_t} {top} "
                  f"C {x+half_t*3.2} {base-h*0.62}, {x+half_b*0.78} {base-h*0.34}, {x+half_b} {base} Z")
    arch = (f"M {x-half_b*0.62} {base} "
            f"C {x-half_b*0.50} {base-h*0.30}, {x-half_b*0.22} {base-h*0.34}, {x} {base-h*0.34} "
            f"C {x+half_b*0.22} {base-h*0.34}, {x+half_b*0.50} {base-h*0.30}, {x+half_b*0.62} {base} Z")
    out = [f'<defs><clipPath id="clip_{ident}"><path d="{silhouette}"/></clipPath></defs>',
           f'<g id="{ident}">',
           f'<path d="{silhouette} {arch}" fill="url(#ironG)" fill-rule="evenodd"/>']
    # решётка внутри силуэта
    cells = []
    step = 34
    import math
    for i in range(-14, 15):
        cells.append(f'<line x1="{x + i*step}" y1="{top}" x2="{x + i*step - 120}" y2="{base}" stroke="#2b211a" stroke-width="2.2" opacity="0.45"/>')
        cells.append(f'<line x1="{x + i*step}" y1="{top}" x2="{x + i*step + 120}" y2="{base}" stroke="#2b211a" stroke-width="2.2" opacity="0.45"/>')
    for j in range(0, 22):
        yy = base - j * (h / 22)
        ww = half_b * (1 - j / 22.0) ** 0.85
        cells.append(f'<line x1="{x-ww:.1f}" y1="{yy:.1f}" x2="{x+ww:.1f}" y2="{yy:.1f}" stroke="#2b211a" stroke-width="2.4" opacity="0.4"/>')
    out.append(f'<g clip-path="url(#clip_{ident})">{"".join(cells)}</g>')
    # платформы
    for frac, ww, hh in ((0.34, 0.92, 22), (0.62, 0.56, 18), (0.82, 0.28, 14)):
        yy = base - h * frac
        out.append(f'<rect x="{x-ww*w/2:.1f}" y="{yy:.1f}" width="{ww*w:.1f}" height="{hh}" rx="4" fill="{IRON_D}"/>')
        out.append(f'<rect x="{x-ww*w/2:.1f}" y="{yy:.1f}" width="{ww*w:.1f}" height="6" rx="3" fill="{IRON_L}" opacity="0.8"/>')
    # верхняя площадка и антенна
    out.append(f'<rect x="{x-half_t*3.4:.1f}" y="{top-8}" width="{half_t*6.8:.1f}" height="16" rx="4" fill="{IRON_D}"/>')
    out.append(f'<rect x="{x-4}" y="{top-96}" width="8" height="98" fill="{IRON_D}"/>')
    out.append(f'<rect x="{x-14}" y="{top-118}" width="28" height="10" rx="4" fill="{IRON_D}"/>')
    out.append(f'<circle cx="{x}" cy="{top-120}" r="7" fill="#e6402f"/>')
    out.append('</g>')
    return "".join(out)


def trees(y, n=9):
    out = []
    r = random.Random(4)
    for i in range(n):
        x = 40 + i * (1000 / (n - 1)) + r.uniform(-18, 18)
        h = r.uniform(60, 92)
        out.append(f'<ellipse cx="{x}" cy="{y-h*0.55:.0f}" rx="{h*0.34:.0f}" ry="{h*0.42:.0f}" fill="#3f8f3a" opacity="0.9"/>')
        out.append(f'<rect x="{x-4}" y="{y-h*0.3:.0f}" width="8" height="{h*0.3:.0f}" fill="#6b4a2f"/>')
    return "".join(out)


def ground(y):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="url(#grass)"/>'
            f'<rect x="0" y="{y+70}" width="1080" height="46" fill="{PATH}" opacity="0.9"/>'
            f'<rect x="0" y="{y+150}" width="1080" height="26" fill="#9aa7b4" opacity="0.5"/>')


def scene_bg(extra_people=8):
    b = ['<rect width="1080" height="1920" fill="url(#sky)"/>',
         '<circle cx="880" cy="300" r="230" fill="url(#sunGlow)"/>',
         '<circle cx="880" cy="300" r="66" fill="{0}"/>'.format(SUN),
         cloud(200, 260, 1.0, "cloud c1"), cloud(700, 170, 0.7, "cloud c2"), cloud(960, 380, 0.55, "cloud c3")]
    b.append(bird(300, 420, 1.0) + bird(360, 450, 0.8) + bird(250, 470, 0.7))
    b.append(ground(1560))
    b.append(trees(1560, 11))
    r = random.Random(9)
    for i in range(extra_people):
        x = r.uniform(60, 1020)
        b.append(person(x, 1660, r.uniform(0.9, 1.2), "#2b3560", "walker"))
    return "".join(b)
