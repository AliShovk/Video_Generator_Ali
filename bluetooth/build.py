#!/usr/bin/env python3
"""«Король в телефоне» — 7 сцен, винтажный постер."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/bluetooth")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

PAPER = "#efe3c8"
PAPER_D = "#e3d4b2"
INK = "#2f2418"
LINE = "#7a6446"
BLUE = "#2b6fd6"
GOLD = "#a8843f"


def txt(x, y, s, size=40, col=INK, anchor="middle", weight=700, cls="", family="'Playfair Display', Georgia, serif", italic=False):
    st = 'font-style="italic" ' if italic else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'{st}fill="{col}" text-anchor="{anchor}">{{}}</text>').replace("{}", s)


def paper(seed=1):
    r = random.Random(seed)
    out = [f'<rect width="1080" height="1920" fill="{PAPER}"/>']
    for _ in range(260):
        out.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,2.2):.1f}" '
                   f'fill="#8a7350" opacity="{r.uniform(0.03,0.09):.2f}"/>')
    # виньетка
    out.append(f'<rect x="0" y="0" width="1080" height="1920" fill="none" stroke="#c9b287" stroke-width="80" opacity="0.35"/>')
    return "".join(out)


def frame():
    return (f'<g class="frame"><rect x="36" y="36" width="1008" height="1848" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="52" y="52" width="976" height="1816" fill="none" stroke="{GOLD}" stroke-width="1.5"/>'
            + "".join(
                f'<path d="M {x} {y} q {dx*26} 0 {dx*44} {dy*26} q 0 {dy*44} {dx*-26} {dy*44}" fill="none" stroke="{GOLD}" stroke-width="2"/>'
                for x, y, dx, dy in [(80, 80, 1, 1), (1000, 80, -1, 1), (80, 1840, 1, -1), (1000, 1840, -1, -1)])
            + '</g>')


def head(label="ИСТОРИЯ ПРИВЫЧНЫХ ЗНАКОВ"):
    return (f'<g class="head"><path d="M 300 96 L 780 96" stroke="{LINE}" stroke-width="1.5"/>'
            f'<text x="540" y="112" font-family="Nunito, Arial" font-size="19" letter-spacing="6" fill="{LINE}" '
            f'text-anchor="middle">{label}</text>'
            f'<path d="M 300 128 L 780 128" stroke="{LINE}" stroke-width="1.5"/>'
            '</g>')


def logo(cx, cy, s=1.0, col=INK, w=26, cls="logo", op=1.0):
    p = (f"M {cx} {cy-100*s} L {cx} {cy+100*s} "
         f"M {cx} {cy-100*s} L {cx+62*s} {cy-50*s} L {cx} {cy} "
         f"M {cx} {cy+100*s} L {cx+62*s} {cy+50*s} L {cx} {cy} "
         f"M {cx-62*s} {cy+50*s} L {cx+62*s} {cy-50*s}")
    return f'<path class="{cls}" d="{p}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'


def rune_hagall(cx, cy, s=1.0, col=INK, w=16, cls="rune"):
    return (f'<path class="{cls}" d="M {cx-40*s} {cy-90*s} L {cx-40*s} {cy+90*s} '
            f'M {cx+40*s} {cy-90*s} L {cx+40*s} {cy+90*s} '
            f'M {cx-40*s} {cy-20*s} L {cx+40*s} {cy+40*s}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round"/>')


def rune_bjarkan(cx, cy, s=1.0, col=INK, w=16, cls="rune"):
    return (f'<path class="{cls}" d="M {cx-40*s} {cy-90*s} L {cx-40*s} {cy+90*s}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path class="{cls}" d="M {cx-40*s} {cy-90*s} L {cx+40*s} {cy-30*s} L {cx-40*s} {cy+10*s}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path class="{cls}" d="M {cx-40*s} {cy+10*s} L {cx+40*s} {cy+60*s} L {cx-40*s} {cy+90*s}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>')


def mountains(y=1250, cls="mtn"):
    """Гравированные горы линиями."""
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M 60 {y+220} L 250 {y-80} L 380 {y+90} L 520 {y-140} L 700 {y+70} L 860 {y-90} L 1020 {y+220} Z" '
             f'fill="none" stroke="{LINE}" stroke-width="3"/>')
    for i in range(9):
        x = 110 + i * 100
        b.append(f'<path d="M {x} {y+200} l {i*4} -160" stroke="{LINE}" stroke-width="1" opacity="0.5"/>')
    b.append('</g>')
    return "".join(b)


def ship(cx, cy, s=1.0, cls="ship"):
    b = [f'<g class="{cls}">']
    # корпус
    b.append(f'<path d="M {cx-230*s} {cy} q 40 {70*s} 230 {70*s} q 190 0 230 {-70*s} q -80 20 -230 20 q -150 0 -230 {-20} z" '
             f'fill="{PAPER_D}" stroke="{INK}" stroke-width="4"/>')
    # штевни
    b.append(f'<path d="M {cx-230*s} {cy} q -30 -60 10 -110 q 10 20 6 40" fill="none" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<path d="M {cx+230*s} {cy} q 30 -50 0 -96 q -14 18 -10 38" fill="none" stroke="{INK}" stroke-width="5"/>')
    # мачта и парус
    b.append(f'<path d="M {cx} {cy-10} l 0 -300" stroke="{INK}" stroke-width="7"/>')
    b.append(f'<path d="M {cx-150*s} {cy-290} q 150 -40 300 0 l 0 210 q -150 30 -300 0 z" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    for i in range(4):
        yy = cy - 270 + i * 52
        b.append(f'<path d="M {cx-140*s} {yy} q 140 -18 280 0" fill="none" stroke="{LINE}" stroke-width="1.6"/>')
    # щиты по борту
    for i in range(7):
        x = cx - 150 * s + i * 50 * s
        b.append(f'<circle cx="{x}" cy="{cy+24*s}" r="{16*s}" fill="none" stroke="{INK}" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def crown(cx, cy, s=1.0, col=INK):
    return (f'<path d="M {cx-60*s} {cy} l 0 -50 l 30 26 l 30 -50 l 30 50 l 30 -26 l 0 50 z" fill="{GOLD}" '
            f'stroke="{col}" stroke-width="4"/>')


# ---------------------------------------------------------------- s1
def s1():
    b = [paper(1), frame(), head()]
    b.append(txt(540, 250, "ЧТО ДЕЛАЕТ", 62, INK, weight=900))
    b.append(txt(540, 330, "СРЕДНЕВЕКОВЫЙ КОРОЛЬ", 58, INK, weight=900))
    b.append(txt(540, 410, "В ВАШЕМ ТЕЛЕФОНЕ?", 58, INK, weight=900))
    b.append(txt(540, 468, "Удивительная история знака Bluetooth", 30, LINE, italic=True))
    b.append(f'<circle cx="540" cy="820" r="210" fill="none" stroke="{BLUE}" stroke-width="6" opacity="0.18"/>')
    b.append(logo(540, 830, 1.9, BLUE, 34, "bigLogo"))
    b.append(txt(540, 1120, "ХАРАЛЬД СИНЕЗУБЫЙ · X ВЕК", 26, LINE))
    b.append(txt(540, 1700, "тысяча лет истории — в одном значке", 32, INK, italic=True))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [paper(2), frame(), head()]
    b.append(txt(540, 210, "X ВЕК · ДАНИЯ", 26, LINE))
    b.append(txt(540, 280, "ХАРАЛЬД ГОРМССОН", 52, INK, weight=900))
    b.append(txt(540, 336, "по прозвищу Синезубый", 32, LINE, italic=True))
    # профиль короля
    b.append(f'<g class="king">')
    b.append(f'<path d="M 380 900 q 0 -220 160 -220 q 160 0 160 220 q -40 40 -80 40 l 0 120 l -160 0 l 0 -120 q -40 0 -80 -40 z" '
             f'fill="{PAPER_D}" stroke="{INK}" stroke-width="5"/>')
    b.append(crown(540, 690, 1.4))
    b.append(f'<path d="M 470 830 q 70 40 140 0" fill="none" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<circle cx="500" cy="790" r="7" fill="{INK}"/><circle cx="580" cy="790" r="7" fill="{INK}"/>')
    b.append(f'<path d="M 540 900 q -30 40 0 60 q 30 -20 0 -60" fill="{INK}" opacity="0.6"/>')
    b.append('</g>')
    b.append(txt(540, 1180, "объединил Данию и Норвегию", 28, LINE, italic=True))
    b.append(txt(540, 1700, "прозвище — Bluetooth", 30, INK))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [paper(3), frame(), head()]
    b.append(txt(540, 210, "1996 ГОД", 28, LINE))
    b.append(txt(540, 280, "ИНЖЕНЕР ДЖИМ КАРДАШ", 46, INK, weight=900))
    b.append(txt(540, 340, "предложил имя для новой технологии", 26, LINE, italic=True))
    # стол, чип, волны
    b.append(f'<g class="desk">')
    b.append(f'<rect x="180" y="980" width="720" height="26" fill="{PAPER_D}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="420" y="880" width="240" height="100" rx="10" fill="#cbb98f" stroke="{INK}" stroke-width="4"/>')
    for i in range(6):
        b.append(f'<path d="M {440+i*36} 880 l 0 -26 M {440+i*36} 980 l 0 26" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<text x="540" y="944" font-family="Nunito" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">BT</text>')
    for i in range(3):
        b.append(f'<path class="wave3" d="M 700 {930-i*26} q 60 -40 120 0" fill="none" stroke="{BLUE}" stroke-width="4" opacity="0.7"/>')
    b.append('</g>')
    b.append(txt(540, 1180, "беспроводная связь между устройствами", 26, LINE, italic=True))
    b.append(txt(540, 1700, "название придумали за один вечер", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [paper(4), frame(), head()]
    b.append(txt(540, 240, "НАЗВАНИЕ СЧИТАЛОСЬ", 40, INK))
    b.append(txt(540, 300, "ВРЕМЕННЫМ", 54, INK, weight=900))
    b.append(f'<g class="stamp"><rect x="230" y="420" width="620" height="150" rx="12" fill="none" stroke="{LINE}" stroke-width="6"/>'
             f'<text x="540" y="520" font-family="Nunito" font-size="44" font-weight="900" fill="{LINE}" text-anchor="middle">ВРЕМЕННОЕ НАЗВАНИЕ</text></g>')
    b.append(f'<path class="cross4" d="M 250 440 L 830 550 M 830 440 L 250 550" stroke="{INK}" stroke-width="7" opacity="0.55"/>')
    b.append(txt(540, 720, "но Bluetooth прижился", 44, INK, italic=True))
    b.append(logo(540, 1000, 1.35, BLUE, 26, "keepLogo"))
    b.append(txt(540, 1320, "и остался навсегда", 30, LINE, italic=True))
    b.append(txt(540, 1700, "имя стало брендом", 26, LINE))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [paper(5), frame(), head()]
    b.append(txt(540, 220, "В ЗНАКЕ СПРЯТАНЫ ДВЕ РУНЫ", 34, INK, weight=900))
    b.append(f'<g class="r1">{rune_hagall(300, 620, 2.2, INK, 22)}</g>')
    b.append(txt(300, 880, "HAGALL", 40, INK, weight=900))
    b.append(txt(300, 926, "руна Х", 28, LINE, italic=True))
    b.append(f'<g class="r2">{rune_bjarkan(780, 620, 2.2, INK, 22)}</g>')
    b.append(txt(780, 880, "BJARKAN", 40, INK, weight=900))
    b.append(txt(780, 926, "руна Б", 28, LINE, italic=True))
    b.append(f'<path class="arrow5" d="M 420 620 l 90 0 M 480 605 l 22 15 l -22 15" stroke="{LINE}" stroke-width="5" fill="none"/>')
    b.append(f'<path class="arrow5" d="M 660 620 l -90 0 M 600 605 l -22 15 l 22 15" stroke="{LINE}" stroke-width="5" fill="none"/>')
    b.append(txt(540, 1240, "Хагаль и Бьяркан —", 30, LINE, italic=True))
    b.append(txt(540, 1290, "первая и вторая буквы имени Harald Bluetooth", 26, LINE, italic=True))
    b.append(txt(540, 1700, "H и B", 44, INK, weight=900))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [paper(6), frame(), head()]
    b.append(txt(540, 220, "СОЕДИНИЛИ — ПОЛУЧИЛИ ЗНАК", 34, INK, weight=900))
    b.append(f'<g class="m1">{rune_hagall(300, 760, 1.9, INK, 20)}</g>')
    b.append(f'<g class="m2">{rune_bjarkan(780, 760, 1.9, INK, 20)}</g>')
    b.append(f'<g class="merged" opacity="0">{logo(540, 780, 1.75, BLUE, 34, "finalLogo")}</g>')
    b.append(txt(540, 1120, "инициалы короля", 32, LINE, italic=True))
    b.append(txt(540, 1250, "Харальд Bluetooth", 44, INK, weight=900))
    b.append(txt(540, 1310, "X век", 28, LINE))
    b.append(txt(540, 1700, "так появился знакомый значок", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [paper(7), frame(), head()]
    b.append(mountains(1080))
    b.append(ship(430, 1290, 0.95, "ship7"))
    # рунический камень
    b.append(f'<g class="stone"><path d="M 800 1420 q -60 -180 10 -300 q 40 -70 110 -10 q 50 60 20 310 z" fill="{PAPER_D}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 830 1200 q 40 -40 70 10 q 10 60 -20 100 q -40 30 -60 -20 q -10 -50 10 -90 z" fill="none" stroke="{LINE}" stroke-width="3"/>'
             f'<path d="M 845 1250 q 20 -20 30 10" fill="none" stroke="{LINE}" stroke-width="3"/></g>')
    # телефон и наушники
    b.append(f'<g class="phone"><rect x="560" y="1520" width="150" height="230" rx="22" fill="{PAPER}" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="574" y="1540" width="122" height="190" rx="12" fill="{PAPER_D}" stroke="{LINE}" stroke-width="2"/>'
             f'{logo(635, 1635, 0.5, BLUE, 10)}</g>')
    b.append(f'<g class="hp"><path d="M 760 1700 q 0 -120 90 -120 q 90 0 90 120" fill="none" stroke="{INK}" stroke-width="9"/>'
             f'<rect x="742" y="1660" width="52" height="90" rx="20" fill="{INK}"/>'
             f'<rect x="906" y="1660" width="52" height="90" rx="20" fill="{INK}"/></g>')
    b.append(txt(540, 300, "ТЫСЯЧА ЛЕТ ИСТОРИИ —", 40, INK, weight=900))
    b.append(txt(540, 356, "В ОДНОМ ЗНАКОМОМ ЗНАЧКЕ", 40, INK, weight=900))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7]
ANIM = [
    'tl.fromTo(".frame, .head", {opacity:0}, {opacity:1, duration:0.6}, 0);'
    'tl.fromTo(".bigLogo", {opacity:0, scale:0.7, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:1.0, ease:"back.out(1.6)"}, 0.5);'
    'tl.to(".bigLogo", {opacity:0.75, duration:1.6, yoyo:true, repeat:4}, 1.6);',
    'tl.fromTo(".king", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.3);'
    'tl.fromTo(".frame", {opacity:0}, {opacity:1, duration:0.5}, 0);',
    'tl.fromTo(".desk", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.to(".wave3", {opacity:0.2, duration:0.6, stagger:0.15, yoyo:true, repeat:4}, 0.9);',
    'tl.fromTo(".stamp", {opacity:0, scale:1.2, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.5}, 0.3);'
    'tl.fromTo(".cross4", {opacity:0}, {opacity:0.55, duration:0.4}, 0.8);'
    'tl.fromTo(".keepLogo", {opacity:0}, {opacity:1, duration:0.6}, 1.1);',
    'tl.fromTo(".r1", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.2);'
    'tl.fromTo(".r2", {opacity:0, x:40}, {opacity:1, x:0, duration:0.6}, 0.5);'
    'tl.fromTo(".arrow5", {opacity:0}, {opacity:1, duration:0.5}, 0.9);',
    'tl.to(".m1", {x:120, duration:1.0, ease:"power2.inOut"}, 0.3);'
    'tl.to(".m2", {x:-120, duration:1.0, ease:"power2.inOut"}, 0.3);'
    'tl.to(".m1, .m2", {opacity:0, duration:0.3}, 1.25);'
    'tl.to(".merged", {opacity:1, duration:0.3}, 1.3);'
    'tl.fromTo(".finalLogo", {scale:0.8, transformOrigin:"50% 50%"}, {scale:1, duration:0.4, ease:"back.out(2)"}, 1.35);',
    'tl.fromTo(".ship7", {opacity:0, x:-30}, {opacity:1, x:0, duration:1.0}, 0.2);'
    'tl.fromTo(".stone", {opacity:0}, {opacity:1, duration:0.8}, 0.5);'
    'tl.fromTo(".phone, .hp", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6, stagger:0.2}, 1.0);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{PAPER}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.02, duration:{dur}, ease:"none" }}, 0);
    {anim}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, fn in enumerate(SCENES):
        sid = f"s{i+1}"
        st, dur = B[i]
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur, ANIM[i]), encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Playfair+Display:ital,wght@0,700;0,900;1,700&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("ok", TOTAL, B)


if __name__ == "__main__":
    build()
