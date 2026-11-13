#!/usr/bin/env python3
"""Камин: как он устроен — ретро-плакат 1950-х, 30 с, 9:16."""
from pathlib import Path

OUT = Path("/root/video-gen/fireplace/compositions")
OUT.mkdir(parents=True, exist_ok=True)

PAPER, INK = "#f2e4c8", "#3a2a1e"
RED, TEAL, MUST, CREAM = "#c1442e", "#2f6b6b", "#d8a13a", "#fbf3e2"


def svg(body):
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            f'<defs>'
            f'<pattern id="brick" width="120" height="56" patternUnits="userSpaceOnUse">'
            f'<rect width="120" height="56" fill="{RED}" opacity="0.92"/>'
            f'<rect x="2" y="2" width="116" height="24" rx="3" fill="#b03c27"/>'
            f'<rect x="-58" y="30" width="116" height="24" rx="3" fill="#b03c27"/>'
            f'<rect x="62" y="30" width="116" height="24" rx="3" fill="#b03c27"/>'
            f'</pattern>'
            f'<pattern id="hatch" width="14" height="14" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">'
            f'<line x1="0" y1="0" x2="0" y2="14" stroke="{INK}" stroke-width="2" opacity="0.25"/></pattern>'
            f'</defs>'
            f'<rect width="1080" height="1920" fill="{PAPER}"/>{body}</svg>')


def t(x, y, s, size=28, color=INK, anchor="start", weight="700", fam="Oswald", ls=1):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{fam}, Georgia, serif" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{ls}" text-anchor="{anchor}">{s}</text>')


def frame():
    return (f'<rect x="34" y="34" width="1012" height="1852" rx="18" fill="none" stroke="{INK}" stroke-width="6" opacity="0.85"/>'
            f'<rect x="52" y="52" width="976" height="1816" rx="12" fill="none" stroke="{INK}" stroke-width="2" opacity="0.45"/>')


def label(x, y, s, tx, ty, size=29, color=INK, anchor="start"):
    return (f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" stroke="{color}" stroke-width="2.5"/>'
            f'<circle cx="{x}" cy="{y}" r="7" fill="{color}"/>'
            + t(tx + (10 if anchor == "start" else -10), ty - 10, s, size, color, anchor))


def fire(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M -46 0 q 6 -46 26 -62 q 4 30 22 40 q 6 -34 26 -46 q 14 44 -6 68 z" fill="{MUST}"/>'
            f'<path d="M -24 0 q 4 -28 18 -38 q 2 18 14 24 q 2 -20 16 -28 q 8 26 -4 42 z" fill="#e46b3c"/>'
            f'</g>')


def fireplace(x, y, w=420, h=560):
    """Разрез камина: топка, дымосборник, труба."""
    out = [f'<rect x="{x-40}" y="{y}" width="{w+80}" height="40" fill="{INK}" opacity="0.85"/>']  # фундамент
    out.append(f'<rect x="{x-26}" y="{y-30}" width="{w+52}" height="30" fill="#8f9ea9"/>')
    # корпус
    out.append(f'<path d="M {x} {y-30} L {x} {y-h} L {x+w} {y-h} L {x+w} {y-30} Z" fill="url(#brick)" stroke="{INK}" stroke-width="4"/>')
    # топка
    out.append(f'<path d="M {x+70} {y-30} L {x+70} {y-h+250} Q {x+w/2} {y-h+120} {x+w-70} {y-h+250} L {x+w-70} {y-30} Z" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    # шамотная облицовка
    out.append(f'<path d="M {x+70} {y-30} L {x+70} {y-h+250} Q {x+w/2} {y-h+120} {x+w-70} {y-h+250} L {x+w-70} {y-30}" fill="none" stroke="{TEAL}" stroke-width="10" opacity="0.75"/>')
    # дымосборник
    out.append(f'<path d="M {x+70} {y-h+250} L {x+w-70} {y-h+250} L {x+w-120} {y-h-10} L {x+120} {y-h-10} Z" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    # труба
    out.append(f'<rect x="{x+120}" y="{y-h-420}" width="{w-240}" height="410" fill="url(#brick)" stroke="{INK}" stroke-width="4"/>')
    out.append(f'<rect x="{x+150}" y="{y-h-420}" width="{w-300}" height="410" fill="{INK}" opacity="0.22"/>')
    out.append(f'<rect x="{x+120}" y="{y-h-440}" width="{w-240}" height="26" fill="{INK}" opacity="0.8"/>')
    return "".join(out)


def scene1():
    b = [frame()]
    b.append(t(72, 150, "КАМИН", 54))
    b.append(t(72, 205, "как он устроен", 26, TEAL))
    b.append(fireplace(320, 1270, 440, 520))
    b.append(label(760, 1130, "топка", 800, 1090, 26, TEAL))
    b.append(label(800, 800, "дымоход", 840, 760, 26, TEAL))
    b.append(label(300, 1310, "фундамент", 120, 1350, 24, TEAL, "start"))
    b.append(fire(540, 1238, 1.2))
    b.append(t(72, 1690, "кирпич · шамот · тяга", 22, INK))
    return svg("".join(b))


def scene2():
    b = [frame()]
    b.append(t(72, 150, "ТОПКА", 52))
    b.append(t(72, 200, "шамотный кирпич держит жар", 24, TEAL))
    b.append(fireplace(300, 1450, 480, 700))
    b.append(fire(540, 1410, 1.6))
    b.append('<g id="labels2">')
    b.append(label(520, 1200, "наклонная задняя стенка", 620, 1150, 26, TEAL))
    b.append(label(360, 1400, "под", 170, 1440, 26, TEAL))
    b.append('</g>')
    b.append(f'<path id="flow" d="M 540 1350 L 540 900" stroke="{RED}" stroke-width="7" stroke-dasharray="18 14" fill="none" marker-end=""/>')
    b.append(f'<polygon points="540,876 522,908 558,908" fill="{RED}"/>')
    b.append(f'<line x1="300" y1="1450" x2="780" y2="1450" stroke="{INK}" stroke-width="4"/>')
    b.append(t(72, 1700, "жар — вверх, дым — в дымоход", 22, INK))
    return svg("".join(b))


def scene3():
    b = [frame()]
    b.append(t(72, 150, "ДЫМОСБОРНИК", 50))
    b.append(t(72, 200, "зуб и задвижка", 24, TEAL))
    b.append(fireplace(300, 1540, 480, 640))
    # задвижка
    b.append(f'<rect x="430" y="790" width="220" height="20" fill="{MUST}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<circle cx="560" cy="800" r="26" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<line x1="560" y1="800" x2="640" y2="740" stroke="{INK}" stroke-width="5"/>')
    b.append(label(680, 800, "задвижка", 720, 760, 26, RED))
    b.append(label(600, 700, "дымовой зуб", 660, 650, 24, TEAL))
    b.append(t(72, 1700, "закрыл — тяга стоит", 22, INK))
    return svg("".join(b))


def scene4():
    b = [frame()]
    b.append(t(72, 150, "ТРУБА", 52))
    b.append(t(72, 200, "выше конька — иначе дым вернётся", 22, TEAL))
    # дом и труба
    b.append(f'<path d="M 120 1180 L 420 1000 L 720 1180 Z" fill="{RED}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="160" y="1180" width="520" height="300" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<g id="flue"><rect x="560" y="700" width="90" height="420" fill="url(#brick)" stroke="{INK}" stroke-width="4"/></g>')
    b.append(f'<rect x="548" y="678" width="114" height="24" fill="{INK}"/>')
    b.append(f'<rect x="556" y="676" width="98" height="8" fill="{MUST}"/>')
    b.append(f'<line id="ridge" x1="120" y1="1000" x2="900" y2="1000" stroke="{INK}" stroke-width="3" stroke-dasharray="16 12"/>')
    b.append(t(760, 992, "конёк", 24, TEAL))
    b.append(f'<line x1="700" y1="700" x2="900" y2="700" stroke="{MUST}" stroke-width="6"/>')
    b.append(t(706, 676, "выше конька", 24, RED))
    b.append(f'<line x1="480" y1="1480" x2="620" y2="1480" stroke="{TEAL}" stroke-width="6"/>')
    b.append(t(480, 1520, "≥ 5 м от топки", 22, TEAL))
    return svg("".join(b))


def scene5():
    b = [frame()]
    b.append(t(72, 150, "БЕЗОПАСНОСТЬ", 48))
    b.append(t(72, 200, "разделка и приток воздуха", 22, TEAL))
    b.append(fireplace(300, 1320, 460, 540))
    # разделка
    b.append(f'<rect x="800" y="820" width="60" height="560" fill="url(#hatch)" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<line x1="780" y1="960" x2="880" y2="960" stroke="{RED}" stroke-width="6"/>')
    b.append(f'<rect x="676" y="896" width="126" height="46" rx="8" fill="{PAPER}"/>')
    b.append(t(700, 932, "38 см", 30, RED))
    b.append(f'<rect x="660" y="980" width="150" height="34" rx="8" fill="{PAPER}"/>')
    b.append(t(668, 1006, "до горючих", 21, INK))
    b.append(f'<g id="air"><path d="M 170 1480 L 280 1480" stroke="{TEAL}" stroke-width="6"/><polygon points="300,1480 270,1468 270,1492" fill="{TEAL}"/></g>')
    b.append(t(112, 1520, "воздух", 23, TEAL))
    return svg("".join(b))


SCENES = [("s1", scene1(), 6), ("s2", scene2(), 6), ("s3", scene3(), 6), ("s4", scene4(), 6), ("s5", scene5(), 6)]
