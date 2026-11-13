#!/usr/bin/env python3
"""Сцены в мультяшном стиле."""
import math

from make_scenes import (BLUE, BLUE_D, GRASS, GRASS_D, INK, ROOF, SOIL, SOIL_D, SOIL_L, STEEL_L,
                         WALL, YELLOW, arch, cloud, ground_cut, house, person, pill, svg, t, tree, truck)


def scene1():
    b = ['<g id="sky-layer">', cloud(180, 300, 1.1), cloud(760, 220, 0.9), cloud(940, 430, 0.7),
         '<circle id="sun" cx="900" cy="140" r="70" fill="#ffe08a"/>', '</g>']
    b.append(ground_cut(1150))
    b.append(tree(120, 1150, 1.0)); b.append(tree(950, 1150, 0.85))
    b.append(house(370, 1150, 260, 230))
    b.append(f'<g id="arch-main">{arch(560, 1150, 760, 580)}</g>')
    b.append(f'<g id="truck1">{truck(230, 1240, 0.9)}</g>'); b.append(truck(880, 1250, 0.8))
    b.append(f'<g id="crowd">{person(430, 1225, 0.85)}{person(700, 1230, 0.8)}</g>')
    return svg("".join(b))


def scene2():
    b = [cloud(200, 260, 1.0), cloud(830, 300, 0.8)]
    b.append(ground_cut(1150))
    b.append(tree(90, 1150, 0.8)); b.append(tree(990, 1150, 0.7))
    b.append(house(380, 1150, 240, 215))
    b.append(arch(560, 1150, 760, 580, 52, 18))
    # размеры
    b.append('<g id="dims">')
    b.append(f'<line x1="170" y1="1215" x2="950" y2="1215" stroke="{INK}" stroke-width="6" opacity="0.75"/>')
    b.append(f'<line x1="170" y1="1195" x2="170" y2="1235" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<line x1="950" y1="1195" x2="950" y2="1235" stroke="{INK}" stroke-width="6"/>')
    b.append(pill(560, 1300, "257 м", 40))
    b.append(f'<line x1="985" y1="575" x2="985" y2="1145" stroke="{INK}" stroke-width="6" opacity="0.75"/>')
    b.append(f'<line x1="965" y1="575" x2="1005" y2="575" stroke="{INK}" stroke-width="6"/>')
    b.append(f'<line x1="965" y1="1145" x2="1005" y2="1145" stroke="{INK}" stroke-width="6"/>')
    b.append(pill(985, 860, "108 м", 40))
    b.append('</g>')
    return svg("".join(b))


def scene3():
    b = [f'<rect width="1080" height="1920" fill="{GRASS}"/>',
         f'<rect x="0" y="0" width="1080" height="1920" fill="#a8dc84" opacity="0.45"/>']
    # участок
    b.append('<rect x="70" y="420" width="940" height="980" rx="36" fill="#cbb894" stroke="#8a7550" stroke-width="8"/>')
    b.append('<rect x="100" y="450" width="880" height="920" rx="26" fill="#d9c9a6"/>')
    # дорога
    b.append('<path d="M 100 1240 Q 540 1180 980 1000" stroke="#b9ada0" stroke-width="86" fill="none"/>')
    b.append('<path d="M 100 1240 Q 540 1180 980 1000" stroke="#efe6d2" stroke-width="52" fill="none"/>')
    # площадка сборки
    b.append(f'<rect x="150" y="980" width="330" height="250" rx="26" fill="#e6d9bf" stroke="{BLUE_D}" stroke-width="8" stroke-dasharray="22 16"/>')
    b.append(t(315, 1075, "СБОРКА", 34, INK, "middle"))
    b.append(t(315, 1122, "300 м от блока", 22, "#6b6252", "middle"))
    # блок
    b.append(f'<circle id="unit4" cx="790" cy="700" r="108" fill="#f3e6cf" stroke="{ROOF}" stroke-width="10"/>')
    b.append(t(790, 736, "4", 68, ROOF, "middle"))
    b.append(t(790, 840, "энергоблок", 22, "#6b6252", "middle"))
    # путь
    b.append('<g id="route">')
    b.append(f'<path d="M 500 1060 Q 640 960 740 810" fill="none" stroke="{BLUE}" stroke-width="18" stroke-dasharray="30 20" stroke-linecap="round"/>')
    b.append(f'<polygon points="752,784 726,844 784,832" fill="{BLUE}"/>')
    b.append(pill(600, 1200, "327 м", 46))
    b.append('</g>')
    b.append(tree(120, 520, 0.8)); b.append(tree(950, 1300, 0.85))
    return svg("".join(b))


def scene4():
    b = [f'<rect width="1080" height="1920" fill="#bfe4f8"/>']
    b.append(ground_cut(800))
    # рельс
    b.append(f'<rect x="0" y="800" width="1080" height="30" fill="#43555f"/>')
    b.append(f'<rect x="0" y="786" width="1080" height="18" rx="9" fill="{STEEL_L}"/>')
    for x in range(30, 1080, 120):
        b.append(f'<rect x="{x}" y="806" width="52" height="14" rx="6" fill="#5f727d" opacity="0.7"/>')
    # опорная плита
    b.append(f'<rect x="210" y="700" width="660" height="86" rx="18" fill="#8ea3b0"/>')
    b.append(f'<rect x="210" y="700" width="660" height="28" rx="14" fill="#c3d2dc"/>')
    # домкраты
    b.append('<g id="jacks">')
    for x in (320, 540, 760):
        b.append(f'<rect x="{x-58}" y="830" width="116" height="120" rx="18" fill="#2f4a5a"/>')
        b.append(f'<rect x="{x-34}" y="760" width="68" height="80" rx="12" fill="#dbe8f0"/>')
        b.append(f'<rect class="piston" x="{x-10}" y="780" width="20" height="52" rx="8" fill="{YELLOW}"/>')
    b.append('</g>')
    # гидролинии с точками (как трубы в референсе)
    b.append('<g id="pipes"><path d="M 380 950 L 700 950" stroke="#2aa7e0" stroke-width="26" fill="none" stroke-linecap="round"/>')
    for x in range(400, 700, 46):
        b.append(f'<circle cx="{x}" cy="950" r="9" fill="#ffffff" opacity="0.9"/>')
    b.append('<path d="M 700 950 q60 0 70 -60" stroke="#2aa7e0" stroke-width="26" fill="none" stroke-linecap="round"/></g>')
    b.append(person(150, 1000, 1.0))
    b.append(person(930, 1000, 0.95))
    return svg("".join(b))


def scene5():
    b = [cloud(160, 260, 1.0), cloud(840, 220, 0.8)]
    b.append(ground_cut(1150))
    b.append(house(790, 1150, 220, 200))
    b.append(f'<rect x="0" y="1146" width="1080" height="26" rx="8" fill="#43555f"/>')
    b.append(f'<g id="arch-move">{arch(330, 1150, 620, 500, 50, 16)}</g>')
    # линии движения
    for i, yy in enumerate((1080, 1110, 1050)):
        b.append(f'<line x1="{60+i*10}" y1="{yy}" x2="{190}" y2="{yy}" stroke="#ffffff" stroke-width="8" opacity="0.45" stroke-linecap="round"/>')
    b.append(person(700, 1225, 0.8))
    return svg("".join(b))


def scene6():
    b = [cloud(200, 250, 1.0), cloud(880, 320, 0.75)]
    b.append(ground_cut(1150))
    b.append(house(380, 1150, 250, 220))
    b.append(arch(560, 1150, 780, 590, 54, 18))
    b.append('<g id="checks">')
    for cx, cy in ((330, 980), (790, 980)):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="42" fill="#4ea336"/>')
        b.append(f'<path d="M {cx-18} {cy+2} l 14 16 l 24 -30" stroke="#ffffff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append('</g>')
    return svg("".join(b))


def scene7():
    b = [cloud(180, 250, 0.9), cloud(860, 300, 0.7)]
    b.append(ground_cut(1150))
    b.append(house(380, 1150, 250, 220))
    b.append(arch(560, 1150, 780, 590, 54, 18))
    # трещина и повреждение
    b.append('<path id="crack" d="M 640 780 L 700 850 L 660 900 L 730 980" stroke="#2a2a2a" stroke-width="10" fill="none" stroke-linecap="round" stroke-dasharray="600" stroke-dashoffset="600"/>')
    b.append('<g id="warn"><circle cx="700" cy="860" r="54" fill="#d94f3d"/>')
    b.append(t(700, 884, "!", 62, "#ffffff", "middle"))
    b.append('</g>')
    b.append('<rect x="760" y="700" width="90" height="60" rx="14" fill="#f0efe6" opacity="0.85"/>')
    return svg("".join(b))


SCENES = [
    ("s1", scene1(), 5), ("s2", scene2(), 7), ("s3", scene3(), 7),
    ("s4", scene4(), 8), ("s5", scene5(), 8), ("s6", scene6(), 7), ("s7", scene7(), 5),
]
