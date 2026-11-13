#!/usr/bin/env python3
"""Гравитация исчезла — флэт-иллюстрация, 30 с, 9:16."""
from pathlib import Path

OUT = Path("/root/video-gen/gravity-flat/compositions")
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1920
WHITE = "#ffffff"
LAV = "#f3ecfb"
PINK = "#fdeaf2"
INK = "#2b2340"
PURPLE = "#7a4dff"
VIOLET = "#a06bff"
MAGENTA = "#e84fd0"
TEAL = "#22c1d6"
YELLOW = "#ffc845"
ORANGE = "#ff8a4c"
GREEN = "#5fbf6a"
SKIN = "#f2c39d"

DEFS = """
<defs>
  <filter id="sh" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#5b4a7a" flood-opacity="0.16"/>
  </filter>
  <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#9be3ee"/><stop offset="1" stop-color="#3aa8d8"/>
  </linearGradient>
</defs>
"""


def svg(body):
    # содержимое крупнее и выше: композиция занимает центр кадра
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            f'<rect width="1080" height="1920" fill="{WHITE}"/>'
            f'<g transform="translate(-43 -300) scale(1.08)">{body}</g></svg>')


def t(x, y, s, size=34, color=INK, anchor="start", weight="900"):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{s}</text>')


def blob(cx, cy, r, fill, op=1.0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{op}"/>'


def person(x, y, s=1.0, shirt=PURPLE, pants=INK, flip=False, arms_up=False, hair=INK, skin=SKIN):
    f = f'translate({x} {y}) scale({-s if flip else s} {s})'
    arms = ('<path d="M -22 -96 q -34 -30 -38 -66" stroke="{skin}" stroke-width="14" stroke-linecap="round" fill="none"/>'
            '<path d="M 22 -96 q 34 -30 38 -66" stroke="{skin}" stroke-width="14" stroke-linecap="round" fill="none"/>') if arms_up else \
           ('<path d="M -22 -96 q -30 20 -30 54" stroke="{skin}" stroke-width="14" stroke-linecap="round" fill="none"/>'
            '<path d="M 22 -96 q 30 20 30 54" stroke="{skin}" stroke-width="14" stroke-linecap="round" fill="none"/>')
    arms = arms.replace("{skin}", skin)
    return (f'<g transform="{f}">'
            f'<rect x="-24" y="-104" width="48" height="70" rx="20" fill="{shirt}"/>'
            f'<rect x="-22" y="-40" width="18" height="62" rx="9" fill="{pants}"/>'
            f'<rect x="4" y="-40" width="18" height="62" rx="9" fill="{pants}"/>'
            f'<circle cx="0" cy="-128" r="26" fill="{skin}"/>'
            f'<path d="M -27 -134 a 27 22 0 0 1 54 0 z" fill="{hair}"/>'
            + arms + '</g>')


def sofa(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#sh)">'
            f'<rect x="-190" y="-120" width="380" height="120" rx="34" fill="{YELLOW}"/>'
            f'<rect x="-210" y="-70" width="420" height="90" rx="30" fill="#ffd166"/>'
            f'<rect x="-196" y="-30" width="34" height="46" rx="14" fill="#e0a52f"/>'
            f'<rect x="162" y="-30" width="34" height="46" rx="14" fill="#e0a52f"/>'
            f'<rect x="-150" y="8" width="26" height="26" rx="8" fill="#c98f22"/>'
            f'<rect x="124" y="8" width="26" height="26" rx="8" fill="#c98f22"/>'
            f'</g>')


def desk(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#sh)">'
            f'<rect x="-170" y="-24" width="340" height="26" rx="10" fill="{PURPLE}"/>'
            f'<rect x="-150" y="2" width="24" height="120" rx="10" fill="#6038d0"/>'
            f'<rect x="126" y="2" width="24" height="120" rx="10" fill="#6038d0"/>'
            f'<rect x="-60" y="2" width="130" height="74" rx="8" fill="#6a43e0"/>'
            f'<rect x="-46" y="16" width="100" height="8" rx="4" fill="#8f6bff"/>'
            f'<rect x="-46" y="34" width="100" height="8" rx="4" fill="#8f6bff"/>'
            f'</g>')


def monitor(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<rect x="-96" y="-120" width="192" height="130" rx="10" fill="#2b2340"/>'
            f'<rect x="-84" y="-108" width="168" height="106" rx="6" fill="url(#screen)"/>'
            f'<path d="M -84 -108 L 84 -108 L -20 -2 L -84 -2 Z" fill="#ffffff" opacity="0.22"/>'
            f'<rect x="-10" y="10" width="20" height="26" fill="#2b2340"/>'
            f'<rect x="-54" y="34" width="108" height="12" rx="6" fill="#2b2340"/>'
            f'</g>')


def plant(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<path d="M -40 -60 q 6 66 12 66 h 56 q 6 0 12 -66 z" fill="{MAGENTA}"/>'
            f'<rect x="-46" y="-78" width="92" height="22" rx="10" fill="#c93bb3"/>'
            f'<path d="M 0 -78 q -40 -44 -22 -96 q 40 20 22 96" fill="{GREEN}"/>'
            f'<path d="M 0 -78 q 40 -50 26 -108 q -46 26 -26 108" fill="#4aa957"/>'
            f'<path d="M 0 -78 q -6 -60 -2 -104" stroke="#3f8f4a" stroke-width="5" fill="none"/>'
            f'</g>')


def clock(x, y, r=64):
    marks = "".join(f'<line x1="{x}" y1="{y-r+10}" x2="{x}" y2="{y-r+22}" stroke="{INK}" stroke-width="4" transform="rotate({a} {x} {y})"/>' for a in range(0, 360, 30))
    return (f'<g filter="url(#sh)"><circle cx="{x}" cy="{y}" r="{r}" fill="#fff1d6" stroke="{INK}" stroke-width="6"/>'
            + marks +
            f'<line x1="{x}" y1="{y}" x2="{x+22}" y2="{y-30}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
            f'<line x1="{x}" y1="{y}" x2="{x-8}" y2="{y-44}" stroke="{ORANGE}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle cx="{x}" cy="{y}" r="6" fill="{INK}"/></g>')


def cup(x, y, s=1.0, rot=0, spill=False):
    drops = ""
    if spill:
        drops = (f'<circle cx="46" cy="-54" r="9" fill="#7a4a2a"/>'
                 f'<circle cx="66" cy="-30" r="6" fill="#7a4a2a"/>'
                 f'<circle cx="34" cy="-74" r="5" fill="#7a4a2a"/>')
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<path d="M -34 -50 h 68 l -8 74 h -52 z" fill="#ffffff" stroke="#e6dced" stroke-width="4"/>'
            f'<ellipse cx="0" cy="-50" rx="34" ry="10" fill="#8a5a34"/>'
            f'<path d="M 34 -34 q 26 0 26 20 q 0 20 -26 20" fill="none" stroke="#e6dced" stroke-width="8"/>'
            + drops + '</g>')


def phone(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<rect x="-34" y="-64" width="68" height="128" rx="14" fill="{TEAL}"/>'
            f'<rect x="-26" y="-54" width="52" height="102" rx="8" fill="#d9f7fb"/></g>')


def dumbbell(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<rect x="-46" y="-10" width="92" height="20" rx="10" fill="#3a3350"/>'
            f'<rect x="-84" y="-30" width="34" height="60" rx="14" fill="#1f1b2d"/>'
            f'<rect x="50" y="-30" width="34" height="60" rx="14" fill="#1f1b2d"/></g>')


def floor(y=1500):
    return (f'<ellipse cx="540" cy="{y+40}" rx="520" ry="70" fill="#e9e2f5" opacity="0.75"/>')


def scene1():
    b = [blob(300, 420, 380, LAV, 0.7), blob(860, 700, 300, PINK, 0.7), floor()]
    b.append(clock(880, 330))
    b.append(plant(170, 1470, 1.0))
    b.append(sofa(330, 1470, 0.95))
    b.append(desk(760, 1470, 0.9))
    b.append(monitor(760, 1330, 0.8))
    b.append(person(300, 1450, 0.95, PURPLE, INK))
    b.append(person(620, 1450, 0.9, TEAL, "#3a3350", flip=True))
    return svg("".join(b))


def scene2():
    b = [blob(320, 380, 360, LAV, 0.65), blob(840, 760, 320, PINK, 0.6), floor(1660)]
    b.append(clock(900, 260, 56))
    b.append(plant(200, 1180, 0.95, -14))
    b.append(sofa(330, 1200, 0.9))
    b.append(desk(800, 1120, 0.85))
    b.append(monitor(800, 980, 0.75, 8))
    b.append(cup(560, 980, 0.9, -18, spill=True))
    b.append(phone(940, 1240, 0.9, 24))
    b.append(person(300, 1500, 0.95, PURPLE, INK, arms_up=True))
    b.append(person(640, 1560, 0.9, TEAL, "#3a3350", flip=True, arms_up=True))
    b.append(dumbbell(520, 1450, 0.85, 20))
    return svg("".join(b))


def scene3():
    b = [blob(540, 520, 420, PINK, 0.55), blob(280, 1300, 320, LAV, 0.6)]
    b.append(plant(780, 1000, 1.5, 18))
    b.append(cup(360, 1080, 1.9, -28, spill=True))
    b.append(phone(640, 1500, 1.6, -16))
    b.append(person(320, 1520, 1.35, PURPLE, INK, arms_up=True))
    return svg("".join(b))


def scene4():
    b = [blob(820, 420, 380, LAV, 0.6), f'<rect x="0" y="1500" width="1080" height="420" fill="#f1ecfa"/>']
    # дома
    b.append(f'<rect x="60" y="1120" width="280" height="380" rx="18" fill="#e7ddf7"/>')
    b.append(f'<rect x="740" y="1060" width="300" height="440" rx="18" fill="#f7e3ef"/>')
    for i in range(3):
        b.append(f'<rect x="{100+i*70}" y="{1160+i*40}" width="52" height="52" rx="10" fill="#ffffff" opacity="0.9"/>')
        b.append(f'<rect x="{780+i*70}" y="{1120+i*40}" width="52" height="52" rx="10" fill="#ffffff" opacity="0.9"/>')
    # дорога
    b.append(f'<rect x="0" y="1460" width="1080" height="90" fill="#dcd3ee"/>')
    for x in range(30, 1080, 130):
        b.append(f'<rect x="{x}" y="1494" width="70" height="12" rx="6" fill="#ffffff" opacity="0.9"/>')
    b.append(car(430, 1300, 1.25, -10))
    b.append(person(830, 1440, 1.0, TEAL, "#3a3350", arms_up=True))
    return svg("".join(b))


def car(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<path d="M -120 -30 q 10 -50 60 -50 h 60 q 50 0 60 50 z" fill="#ff9f6b"/>'
            f'<rect x="-130" y="-34" width="260" height="60" rx="24" fill="{ORANGE}"/>'
            f'<rect x="-50" y="-72" width="96" height="40" rx="10" fill="#d7f1f7"/>'
            f'<circle cx="-72" cy="32" r="26" fill="#3a3350"/><circle cx="72" cy="32" r="26" fill="#3a3350"/>'
            f'<circle cx="-72" cy="32" r="10" fill="#ffffff"/><circle cx="72" cy="32" r="10" fill="#ffffff"/></g>')


def scene5():
    b = [blob(300, 420, 320, LAV, 0.6), floor()]
    b.append(sofa(380, 1500, 0.9))
    b.append(cup(760, 1480, 1.1, 78))
    b.append(monitor(700, 1300, 0.7, -12))
    b.append(plant(170, 1480, 0.85, 66))
    b.append(person(560, 1560, 1.0, TEAL, "#3a3350"))
    return svg("".join(b))


SCENES = [("s1", scene1(), 6), ("s2", scene2(), 6), ("s3", scene3(), 6), ("s4", scene4(), 6), ("s5", scene5(), 6)]
