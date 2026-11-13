#!/usr/bin/env python3
"""«Что, если гравитация исчезнет на 10 секунд» — плоская мультяшная подача."""
from make_scenes import (BLUE, BLUE_D, GRASS, GRASS_D, INK, ROOF, SOIL, SOIL_D, SOIL_L, STEEL_L,
                         WALL, YELLOW, cloud, ground_cut, person, pill, svg, t, tree)

ROOM_WALL = "#f6efe2"
ROOM_FLOOR = "#d9c39d"
ROOM_LINE = "#c3a97e"


def cup(x, y, s=1.0, rot=0, coffee=True):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<path d="M -34 -46 L 34 -46 L 26 30 L -26 30 Z" fill="#ffffff" stroke="#d8d2c6" stroke-width="3"/>'
            f'<path d="M 34 -34 q26 0 26 18 q0 18 -26 18" fill="none" stroke="#d8d2c6" stroke-width="7"/>'
            + (f'<ellipse cx="0" cy="-44" rx="32" ry="8" fill="#7a4a2a"/>' if coffee else '')
            + '</g>')


def chair(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<rect x="-44" y="-26" width="88" height="18" rx="8" fill="#c58b52"/>'
            f'<rect x="-44" y="-96" width="16" height="74" rx="7" fill="#c58b52"/>'
            f'<rect x="-40" y="-12" width="12" height="46" rx="6" fill="#9a6a3c"/>'
            f'<rect x="28" y="-12" width="12" height="46" rx="6" fill="#9a6a3c"/>'
            f'</g>')


def car(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
            f'<rect x="-90" y="-46" width="180" height="52" rx="18" fill="#3f7fb5"/>'
            f'<path d="M -54 -46 L -30 -84 L 34 -84 L 58 -46 Z" fill="#5b9ccf"/>'
            f'<rect x="-26" y="-78" width="56" height="28" rx="6" fill="#bfe3f5"/>'
            f'<circle cx="-52" cy="8" r="18" fill="#22323c"/><circle cx="52" cy="8" r="18" fill="#22323c"/>'
            f'<circle cx="-52" cy="8" r="7" fill="#8f9ea9"/><circle cx="52" cy="8" r="7" fill="#8f9ea9"/>'
            f'</g>')


def earth(cx, cy, r):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#3d8fd0"/>']
    # континенты
    out.append(f'<path d="M {cx-r*0.5} {cy-r*0.3} q {r*0.22} {-r*0.3} {r*0.42} {-r*0.05} q {r*0.16} {r*0.2} {-r*0.05} {r*0.3} q {-r*0.3} {r*0.1} {-r*0.37} {-r*0.25} z" fill="#5cb85c"/>')
    out.append(f'<path d="M {cx+r*0.05} {cy+r*0.15} q {r*0.3} {-r*0.1} {r*0.32} {r*0.2} q {-r*0.1} {r*0.3} {-r*0.35} {r*0.15} z" fill="#5cb85c"/>')
    out.append(f'<path d="M {cx-r*0.15} {cy+r*0.45} q {r*0.2} {-r*0.08} {r*0.22} {r*0.12} q {-r*0.2} {r*0.1} {-r*0.22} {-r*0.12} z" fill="#5cb85c"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8fd3ff" stroke-width="6" opacity="0.5"/>')
    return "".join(out)


def scene1():
    b = [f'<rect width="1080" height="1920" fill="{ROOM_WALL}"/>',
         f'<rect x="0" y="1180" width="1080" height="740" fill="{ROOM_FLOOR}"/>',
         f'<rect x="0" y="1170" width="1080" height="22" fill="{ROOM_LINE}"/>']
    # окно
    b.append('<rect x="700" y="430" width="280" height="360" rx="18" fill="#bfe4f8" stroke="#d8cdb8" stroke-width="12"/>')
    b.append('<line x1="840" y1="430" x2="840" y2="790" stroke="#d8cdb8" stroke-width="10"/>')
    b.append('<line x1="700" y1="610" x2="980" y2="610" stroke="#d8cdb8" stroke-width="10"/>')
    # стол
    b.append('<rect x="250" y="1010" width="520" height="34" rx="12" fill="#b98451"/>')
    b.append('<rect x="286" y="1044" width="20" height="150" rx="8" fill="#9a6a3c"/>')
    b.append('<rect x="714" y="1044" width="20" height="150" rx="8" fill="#9a6a3c"/>')
    b.append(cup(410, 1010, 1.0))
    b.append(chair(880, 1180, 1.0))
    b.append(person(660, 1180, 1.0))
    return svg("".join(b))


def scene2():
    b = [f'<rect width="1080" height="1920" fill="{ROOM_WALL}"/>',
         f'<rect x="0" y="1180" width="1080" height="740" fill="{ROOM_FLOOR}"/>',
         f'<rect x="0" y="1170" width="1080" height="22" fill="{ROOM_LINE}"/>']
    b.append('<rect x="700" y="430" width="280" height="360" rx="18" fill="#bfe4f8" stroke="#d8cdb8" stroke-width="12"/>')
    b.append('<line x1="840" y1="430" x2="840" y2="790" stroke="#d8cdb8" stroke-width="10"/>')
    b.append('<line x1="700" y1="610" x2="980" y2="610" stroke="#d8cdb8" stroke-width="10"/>')
    b.append('<rect x="250" y="1010" width="520" height="34" rx="12" fill="#b98451"/>')
    b.append('<rect x="286" y="1044" width="20" height="150" rx="8" fill="#9a6a3c"/>')
    b.append('<rect x="714" y="1044" width="20" height="150" rx="8" fill="#9a6a3c"/>')
    # всё всплывает
    b.append(f'<g id="cup-float">{cup(410, 810, 1.05, -12)}</g>')
    b.append('<g id="chair-float">' + chair(880, 900, 1.0, 14) + '</g>')
    b.append('<g id="person-float">' + person(640, 860, 1.05) + '</g>')
    # капли/книги
    b.append('<rect x="300" y="700" width="80" height="26" rx="6" fill="#e07a5f"/>')
    b.append('<rect x="320" y="660" width="80" height="26" rx="6" fill="#6fa8dc"/>')
    b.append('<rect x="900" y="640" width="70" height="22" rx="6" fill="#8bc34a"/>')
    for x, y in ((220, 620), (500, 700), (770, 560), (980, 860)):
        b.append(f'<circle cx="{x}" cy="{y}" r="9" fill="#9fd8f5"/>')
    # стрелки вверх
    for x in (200, 960):
        b.append(f'<path d="M {x} 1120 L {x} 980" stroke="#2aa7e0" stroke-width="10" stroke-linecap="round"/>')
        b.append(f'<polygon points="{x},950 {x-22},992 {x+22},992" fill="#2aa7e0"/>')
    return svg("".join(b))


def scene3():
    b = [f'<rect width="1080" height="1920" fill="#bfe4f8"/>', cloud(180, 260, 1.0), cloud(860, 200, 0.85)]
    b.append('<circle cx="900" cy="120" r="66" fill="#ffe08a"/>')
    b.append(ground_cut(1300))
    b.append(tree(90, 1300, 0.9)); b.append(tree(990, 1300, 0.8))
    # дома
    b.append('<rect x="120" y="1010" width="240" height="290" rx="12" fill="#f4f0e4"/>')
    b.append('<path d="M 100 1010 L 240 900 L 380 1010 Z" fill="#b03a2e"/>')
    b.append('<rect x="700" y="1060" width="200" height="240" rx="12" fill="#e9e2d2"/>')
    b.append('<path d="M 682 1060 L 800 970 L 918 1060 Z" fill="#a8453a"/>')
    # дорога
    b.append('<rect x="0" y="1220" width="1080" height="90" fill="#8f9ea9"/>')
    b.append('<rect x="0" y="1258" width="1080" height="10" fill="#f0e9d6" stroke-dasharray="40 30"/>')
    # машина и люди всплывают
    b.append(f'<g id="car-float">{car(420, 1050, 0.95, -8)}</g>')
    b.append(f'<g id="people-float">{person(250, 1150, 0.9)}{person(620, 1120, 0.85)}</g>')
    # прорванная труба и вода
    b.append('<rect x="120" y="1140" width="150" height="26" rx="12" fill="#8fa3b0"/>')
    b.append('<g id="water">')
    for i, (wx, wy, wr) in enumerate([(300, 1120, 12), (330, 1080, 9), (360, 1040, 11), (392, 1000, 8),
                                      (430, 960, 12), (470, 920, 9), (515, 880, 11), (560, 845, 8),
                                      (610, 810, 10), (660, 780, 7)]):
        b.append(f'<circle cx="{wx}" cy="{wy}" r="{wr}" fill="#7fd0f5"/>')
    b.append('</g>')
    return svg("".join(b))


def scene4():
    b = ['<rect width="1080" height="1920" fill="#060a18"/>']
    rnd = __import__("random").Random(4)
    for _ in range(90):
        b.append(f'<circle cx="{rnd.uniform(0,1080):.0f}" cy="{rnd.uniform(0,1920):.0f}" r="{rnd.uniform(0.8,2.2):.1f}" fill="#dfe9ff" opacity="{rnd.uniform(0.2,0.8):.2f}"/>')
    b.append('<circle cx="880" cy="330" r="110" fill="#ffd166"/>')
    b.append('<circle cx="880" cy="330" r="150" fill="#ffd166" opacity="0.18"/>')
    b.append(f'<g id="earth">{earth(540, 1100, 300)}</g>')
    # атмосфера, которую сдувает
    b.append('<ellipse cx="540" cy="1100" rx="330" ry="330" fill="none" stroke="#8fd3ff" stroke-width="20" opacity="0.45"/>')
    b.append('<ellipse cx="540" cy="1100" rx="356" ry="356" fill="none" stroke="#8fd3ff" stroke-width="10" opacity="0.22"/>')
    # объекты улетают
    for x, y, col, r in ((200, 700, "#ff8a65", 26), (280, 610, "#ffffff", 18), (880, 720, "#8bc34a", 22), (800, 600, "#ffd166", 20)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
        b.append(f'<line x1="{x}" y1="{y+r+8}" x2="{x-r*1.6}" y2="{y+r+70}" stroke="{col}" stroke-width="6" opacity="0.4" stroke-linecap="round"/>')
    return svg("".join(b))


def scene5():
    b = [f'<rect width="1080" height="1920" fill="{ROOM_WALL}"/>',
         f'<rect x="0" y="1180" width="1080" height="740" fill="{ROOM_FLOOR}"/>',
         f'<rect x="0" y="1170" width="1080" height="22" fill="{ROOM_LINE}"/>']
    b.append('<rect x="250" y="1010" width="520" height="34" rx="12" fill="#b98451"/>')
    # падающие предметы
    b.append('<g id="fall-cup">' + cup(400, 470, 1.1, 30) + '</g>')
    b.append('<g id="fall-chair">' + chair(760, 400, 1.05, 40) + '</g>')
    b.append('<g id="fall-person">' + person(560, 450, 1.1) + '</g>')
    for x in (400, 760, 560):
        for k in range(3):
            b.append(f'<line x1="{x-18+k*18}" y1="{180+k*26}" x2="{x-18+k*18}" y2="{260+k*26}" stroke="#2aa7e0" stroke-width="7" opacity="0.45" stroke-linecap="round"/>')
    return svg("".join(b))


def scene6():
    b = [f'<rect width="1080" height="1920" fill="{ROOM_WALL}"/>',
         f'<rect x="0" y="1180" width="1080" height="740" fill="{ROOM_FLOOR}"/>']
    b.append('<rect x="230" y="1060" width="560" height="30" rx="12" fill="#b98451" transform="rotate(-6 510 1075)"/>')
    b.append('<rect x="286" y="1084" width="20" height="140" rx="8" fill="#9a6a3c" transform="rotate(-6 296 1154)"/>')
    b.append(cup(390, 1130, 1.0, 82))
    b.append('<path d="M 520 1120 l 40 -30 l 30 40" stroke="#e07a5f" stroke-width="10" fill="none" stroke-linecap="round"/>')
    b.append(person(760, 1180, 1.0, "#2f4a5a"))
    return svg("".join(b))


SCENES = [
    ("s1", scene1(), 4), ("s2", scene2(), 8), ("s3", scene3(), 12),
    ("s4", scene4(), 14), ("s5", scene5(), 10), ("s6", scene6(), 7),
]
