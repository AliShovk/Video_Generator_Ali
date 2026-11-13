#!/usr/bin/env python3
"""Ночь в −40 у костра: флэт-иллюстрация, 9:16."""
from pathlib import Path

OUT = Path("/root/video-gen/fire-survival/compositions")
OUT.mkdir(parents=True, exist_ok=True)

WHITE = "#ffffff"
INK = "#1f2740"
NIGHT = "#141b33"
SNOW = "#eaf1fb"
SNOW2 = "#d7e4f5"
FIRE = "#ff8a3d"
FIRE2 = "#ffc845"
EMBER = "#ff5a2b"
PURPLE = "#6b5bd2"
TEAL = "#2aa9c9"
SKIN = "#f2c39d"
GREY = "#3a4664"

DEFS = """
<defs>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ffb347" stop-opacity="0.75"/>
    <stop offset="1" stop-color="#ffb347" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffd9a8"/><stop offset="0.55" stop-color="#bfe0f7"/><stop offset="1" stop-color="#ffffff"/>
  </linearGradient>
  <filter id="sh" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#0b1226" flood-opacity="0.22"/>
  </filter>
</defs>
"""


def svg(body, bg=NIGHT):
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            f'<rect width="1080" height="1920" fill="{bg}"/>'
            f'<g transform="translate(-270 -780) scale(1.5)">{body}</g></svg>')


def t(x, y, s, size=34, color="#ffffff", anchor="start", weight="900"):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{s}</text>')


def stars(n=60, seed=5):
    import random
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(80,760):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#dfe8ff" opacity="{r.uniform(0.15,0.7):.2f}"/>' for _ in range(n))


def snowbank(y=1400):
    return (f'<path d="M 0 {y+80} Q 260 {y-40} 540 {y+30} Q 840 {y+90} 1080 {y-10} L 1080 1920 L 0 1920 Z" fill="{SNOW}"/>'
            f'<path d="M 0 {y+120} Q 300 {y+30} 560 {y+90} Q 830 {y+140} 1080 {y+50} L 1080 1920 L 0 1920 Z" fill="{SNOW2}"/>')


def fire(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<ellipse cx="0" cy="10" rx="150" ry="50" fill="url(#glow)"/>'
            f'<path d="M -80 0 q 18 -70 54 -96 q 10 44 30 58 q 12 -56 44 -74 q 22 74 -6 112 z" fill="{FIRE}"/>'
            f'<path d="M -44 0 q 12 -46 34 -62 q 6 28 20 38 q 8 -32 26 -44 q 14 46 -4 68 z" fill="{FIRE2}"/>'
            f'<path d="M -96 6 l 34 -22 l 30 22 l 32 -22 l 34 22 l 30 -22 l 32 22 l -30 -14 l -34 8 l -32 -14 l -30 12 z" fill="#6b4a2f"/>'
            f'</g>')


def person_sleep(x, y, s=1.0, flip=False, bag=PURPLE):
    f = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return (f'<g transform="{f}">'
            f'<ellipse cx="0" cy="6" rx="120" ry="26" fill="#000" opacity="0.25"/>'
            f'<path d="M -120 0 q 0 -46 56 -46 h 130 q 54 0 54 46 z" fill="{bag}"/>'
            f'<circle cx="-118" cy="-30" r="30" fill="{SKIN}"/>'
            f'<path d="M -146 -40 a 30 24 0 0 1 58 0 z" fill="#2b2340"/>'
            f'<path d="M -150 0 q 10 -20 34 -20" stroke="{bag}" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'</g>')


def person_stand(x, y, s=1.0, coat=PURPLE, hat="#2b2340", arms_up=False, flip=False):
    f = f'translate({x} {y}) scale({-s if flip else s} {s})'
    arms = ('<path d="M -24 -110 q -40 -34 -44 -74" stroke="{c}" stroke-width="16" stroke-linecap="round" fill="none"/>'
            '<path d="M 24 -110 q 40 -34 44 -74" stroke="{c}" stroke-width="16" stroke-linecap="round" fill="none"/>') if arms_up else \
           ('<path d="M -24 -110 q -26 26 -26 62" stroke="{c}" stroke-width="16" stroke-linecap="round" fill="none"/>'
            '<path d="M 24 -110 q 26 26 26 62" stroke="{c}" stroke-width="16" stroke-linecap="round" fill="none"/>')
    arms = arms.replace("{c}", coat)
    return (f'<g transform="{f}">'
            f'<ellipse cx="0" cy="8" rx="46" ry="12" fill="#000" opacity="0.25"/>'
            f'<rect x="-28" y="-120" width="56" height="86" rx="24" fill="{coat}"/>'
            f'<rect x="-24" y="-40" width="20" height="46" rx="10" fill="#2b2340"/>'
            f'<rect x="4" y="-40" width="20" height="46" rx="10" fill="#2b2340"/>'
            f'<circle cx="0" cy="-146" r="28" fill="{SKIN}"/>'
            f'<path d="M -30 -152 a 30 24 0 0 1 60 0 z" fill="{hat}"/>'
            f'<rect x="-30" y="-156" width="60" height="12" rx="6" fill="#ffffff" opacity="0.85"/>'
            + arms + '</g>')


def logs(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" filter="url(#sh)">'
            f'<rect x="-170" y="-34" width="340" height="62" rx="30" fill="#7a4f30"/>'
            f'<rect x="-170" y="-72" width="340" height="60" rx="30" fill="#8b5b38"/>'
            f'<path d="M -160 -34 q 160 22 320 0" stroke="{EMBER}" stroke-width="8" fill="none" opacity="0.9"/>'
            f'<ellipse cx="-170" cy="-4" rx="14" ry="30" fill="#a9743f"/><ellipse cx="170" cy="-4" rx="14" ry="30" fill="#a9743f"/>'
            f'<ellipse cx="-170" cy="-44" rx="14" ry="28" fill="#b8834a"/><ellipse cx="170" cy="-44" rx="14" ry="28" fill="#b8834a"/>'
            f'</g>')


def banner(x, y, s=1.0, rot=-6):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#sh)">'
            f'<rect x="-190" y="-150" width="380" height="300" rx="10" fill="#f4f1e6"/>'
            f'<rect x="-190" y="-150" width="380" height="300" rx="10" fill="none" stroke="#c9bfa6" stroke-width="6"/>'
            f'<rect x="-150" y="-100" width="300" height="60" rx="8" fill="{TEAL}" opacity="0.85"/>'
            f'<rect x="-150" y="-20" width="180" height="20" rx="10" fill="#c9bfa6"/>'
            f'<rect x="-150" y="20" width="240" height="20" rx="10" fill="#dcd3bd"/>'
            f'<circle cx="110" cy="70" r="40" fill="{FIRE}" opacity="0.85"/>'
            f'</g>')


def poles(x1, x2, y):
    return (f'<rect x="{x1-8}" y="{y-330}" width="16" height="340" rx="6" fill="#6b4a2f"/>'
            f'<rect x="{x2-8}" y="{y-360}" width="16" height="370" rx="6" fill="#6b4a2f"/>')


def ground_cut(y=1350):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="{SNOW}"/>'
            f'<rect x="0" y="{y+90}" width="1080" height="60" fill="{SNOW2}"/>'
            f'<rect x="0" y="{y+150}" width="1080" height="{1920-y-150}" fill="#b9a184"/>'
            f'<rect x="0" y="{y+150}" width="1080" height="26" fill="#a68b6a"/>')


def pines(y=1430):
    out = []
    for i, (x, h, op) in enumerate([(80, 210, 0.55), (200, 260, 0.45), (880, 240, 0.5), (990, 200, 0.6), (760, 170, 0.35)]):
        out.append(f'<path d="M {x} {y} L {x-h*0.22:.0f} {y-h*0.55:.0f} L {x-h*0.1:.0f} {y-h*0.52:.0f} '
                   f'L {x-h*0.3:.0f} {y-h*0.78:.0f} L {x:.0f} {y-h} L {x+h*0.3:.0f} {y-h*0.78:.0f} '
                   f'L {x+h*0.1:.0f} {y-h*0.52:.0f} L {x+h*0.22:.0f} {y-h*0.55:.0f} Z" fill="#0e1526" opacity="{op}"/>')
    return "".join(out)


def scene1():
    b = [stars()]
    b.append('<circle cx="880" cy="240" r="70" fill="#f4f7ff" opacity="0.9"/><circle cx="910" cy="225" r="62" fill="{0}"/>'.format(NIGHT))
    b.append(snowbank(1420))
    b.append(pines(1420))
    b.append(fire(320, 1400, 1.15))
    b.append(person_sleep(700, 1470, 1.0, bag=PURPLE))
    return svg("".join(b))


def scene2():
    b = [stars(40)]
    b.append(snowbank(1450))
    b.append(pines(1450))
    b.append(logs(400, 1420, 1.15))
    b.append(f'<ellipse cx="400" cy="1430" rx="240" ry="120" fill="url(#glow)" opacity="0.8"/>')
    b.append(person_stand(820, 1460, 0.95, TEAL, arms_up=False, flip=True))
    return svg("".join(b))


def scene3():
    b = [snowbank(1500), pines(1500)]
    b.append(fire(300, 1470, 1.2))
    b.append(person_sleep(700, 1510, 1.0, flip=True, bag=PURPLE))
    # тепло уходит в темноту
    for i, y in enumerate((1250, 1310, 1370)):
        b.append(f'<path d="M 640 {y} q 120 -30 260 0" stroke="{FIRE2}" stroke-width="8" fill="none" opacity="{0.6-i*0.15}" stroke-dasharray="18 16"/>')
    b.append(t(760, 1180, "тепло уходит", 32, "#ffcf8a", "middle"))
    return svg("".join(b))


def scene4():
    b = [stars(30)]
    b.append(snowbank(1480))
    b.append(pines(1480))
    b.append(poles(330, 980, 1460))
    b.append(banner(700, 1230, 1.05, -5))
    b.append(person_sleep(470, 1480, 0.9, flip=False))
    b.append(fire(300, 1460, 1.0))
    for i, y in enumerate((1300, 1360, 1420)):
        b.append(f'<path d="M 380 {y} q 120 -36 220 0" stroke="{FIRE2}" stroke-width="7" fill="none" opacity="0.55" stroke-dasharray="16 14"/>')
    return svg("".join(b))


def scene5():
    b = [ground_cut(1250)]
    # костёр сдвинут
    b.append(fire(780, 1250, 0.95))
    # прогретая земля
    b.append(f'<ellipse cx="360" cy="1330" rx="200" ry="70" fill="{FIRE2}" opacity="0.35"/>')
    b.append(f'<ellipse cx="360" cy="1315" rx="150" ry="46" fill="{FIRE}" opacity="0.45"/>')
    b.append(person_sleep(360, 1300, 0.95, bag=PURPLE))
    b.append(f'<path d="M 360 1400 v 120" stroke="{FIRE2}" stroke-width="8" stroke-dasharray="16 12"/>')
    b.append(f'<path d="M 330 1500 l 30 40 l 30 -40" fill="none" stroke="{FIRE2}" stroke-width="8"/>')
    return svg("".join(b))


def scene6():
    b = [f'<rect width="1080" height="1920" fill="url(#dawn)"/>',
         '<circle cx="840" cy="980" r="110" fill="#ffe08a"/>',
         '<circle cx="840" cy="980" r="170" fill="#ffe08a" opacity="0.25"/>']
    b.append(snowbank(1450))
    b.append(person_stand(540, 1490, 1.15, ORANGE if False else "#ff9f6b", arms_up=True))
    return svg("".join(b), bg="#dff0fb")


SCENES = [("s1", scene1(), 9), ("s2", scene2(), 9), ("s3", scene3(), 9), ("s4", scene4(), 9), ("s5", scene5(), 9), ("s6", scene6(), 7)]
