#!/usr/bin/env python3
"""«Как студенческий рисунок стал знаком переработки» — 8 сцен, винтаж."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/recycle")
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
PAPER_D = "#e2d3b1"
INK = "#2f2418"
LINE = "#7a6446"
GOLD = "#a8843f"
GREEN = "#4f7f43"


def txt(x, y, s, size=40, col=INK, anchor="middle", weight=700, cls="", family="'Playfair Display', Georgia, serif", italic=False):
    st = 'font-style="italic" ' if italic else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'{st}fill="{col}" text-anchor="{anchor}">{s}</text>')


def paper(seed=1):
    r = random.Random(seed)
    out = [f'<rect width="1080" height="1920" fill="{PAPER}"/>']
    for _ in range(240):
        out.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,2.0):.1f}" '
                   f'fill="#8a7350" opacity="{r.uniform(0.03,0.08):.2f}"/>')
    return "".join(out)


def frame():
    return (f'<g class="frame"><rect x="36" y="36" width="1008" height="1848" fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="52" y="52" width="976" height="1816" fill="none" stroke="{GOLD}" stroke-width="1.5"/>'
            + "".join(
                f'<path d="M {x} {y} q {dx*26} 0 {dx*44} {dy*26} q 0 {dy*44} {dx*-26} {dy*44}" fill="none" stroke="{GOLD}" stroke-width="2"/>'
                for x, y, dx, dy in [(80, 80, 1, 1), (1000, 80, -1, 1), (80, 1840, 1, -1), (1000, 1840, -1, -1)])
            + '</g>')


def head(label="ИСТОРИЯ ПРИВЫЧНЫХ ЗНАКОВ"):
    return (f'<g class="head"><path d="M 270 96 L 810 96" stroke="{LINE}" stroke-width="1.5"/>'
            f'<text x="540" y="112" font-family="Nunito, Arial" font-size="19" letter-spacing="6" fill="{LINE}" '
            f'text-anchor="middle">{label}</text>'
            f'<path d="M 270 128 L 810 128" stroke="{LINE}" stroke-width="1.5"/></g>')


def recycle(cx, cy, s=1.0, col=INK, fill=PAPER_D, cls="rec", w=4.0, R=190, band=46):
    """Три дуговые стрелки по кругу — знак переработки."""
    out = [f'<g class="{cls}">']
    for i in range(3):
        a0 = math.radians(i * 120 + 10)
        a1 = math.radians((i + 1) * 120 - 20)
        x0, y0 = cx + R * s * math.cos(a0), cy + R * s * math.sin(a0)
        x1, y1 = cx + R * s * math.cos(a1), cy + R * s * math.sin(a1)
        out.append(f'<path d="M {x0:.1f} {y0:.1f} A {R*s:.1f} {R*s:.1f} 0 0 1 {x1:.1f} {y1:.1f}" '
                   f'fill="none" stroke="{col}" stroke-width="{band*s}" stroke-linecap="butt"/>')
        # наконечник
        tx, ty = -math.sin(a1), math.cos(a1)   # касательная
        nx, ny = math.cos(a1), math.sin(a1)    # нормаль
        hb = band * s * 1.05
        tipx, tipy = x1 + tx * 52 * s, y1 + ty * 52 * s
        out.append(f'<path d="M {x1 + nx*hb:.1f} {y1 + ny*hb:.1f} L {tipx:.1f} {tipy:.1f} '
                   f'L {x1 - nx*hb:.1f} {y1 - ny*hb:.1f} Z" fill="{col}"/>')
    out.append('</g>')
    return "".join(out)


def notebook(x, y, w=420, h=300, rot=-6, cls="nb"):
    lines = "".join(f'<path d="M {x+24} {y+40+i*34} l {w-48} 0" stroke="{LINE}" stroke-width="1.4" opacity="0.5"/>' for i in range(6))
    rings = "".join(f'<circle cx="{x-6}" cy="{y+26+i*38}" r="7" fill="none" stroke="{INK}" stroke-width="2"/>' for i in range(7))
    return (f'<g class="{cls}" transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f6ecd6" stroke="{INK}" stroke-width="3"/>'
            f'{lines}{rings}</g>')


def pencil(x, y, rot=-20, cls="pen"):
    return (f'<g class="{cls}" transform="rotate({rot} {x} {y})">'
            f'<rect x="{x}" y="{y}" width="190" height="18" rx="3" fill="{PAPER_D}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M {x+190} {y} l 26 9 l -26 9 z" fill="{PAPER_D}" stroke="{INK}" stroke-width="2.5"/>'
            f'<path d="M {x+216} {y+9} l 8 0" stroke="{INK}" stroke-width="3"/></g>')


def box(x, y, w, h, d=26, cls="bx"):
    return (f'<g class="{cls}"><path d="M {x} {y} l {d} {-d} l {w} 0 l 0 {h} l {-d} {d} l {-w} 0 z" fill="{PAPER_D}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {x} {y} l {w} 0 l 0 {h}" fill="none" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M {x+w} {y} l {d} {-d}" stroke="{INK}" stroke-width="2"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [paper(1), frame(), head()]
    b.append(txt(540, 210, "КАК СТУДЕНЧЕСКИЙ РИСУНОК", 40))
    b.append(txt(540, 262, "ОКАЗАЛСЯ НА МИЛЛИОНАХ", 40))
    b.append(txt(540, 314, "УПАКОВОК?", 46, INK, weight=900))
    b.append(txt(540, 366, "История трёх знакомых стрелок", 26, LINE, italic=True))
    b.append(recycle(540, 660, 1.15, INK, PAPER_D, "bigRec", 5))
    b.append(notebook(90, 980, 380, 250, -8))
    b.append(recycle(200, 1080, 0.34, LINE, "none", "sketchRec", 2.5))
    b.append(pencil(300, 1130, -14))
    b.append(txt(540, 1400, "1970 · конкурс на знак переработки бумаги", 28, LINE, italic=True))
    b.append(txt(540, 1700, "эскиз занял день или два", 30, INK, italic=True))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [paper(2), frame(), head()]
    b.append(txt(540, 200, "1970 ГОД", 30, LINE, extra="") if False else "")
    b.append(txt(540, 200, "1970 ГОД", 30, LINE))
    b.append(txt(540, 268, "ОБЪЯВИЛИ КОНКУРС", 44, INK, weight=900))
    b.append(txt(540, 322, "на знак переработки бумаги", 26, LINE, italic=True))
    # доска объявлений
    b.append(f'<g class="board"><rect x="180" y="420" width="720" height="560" fill="#f6ecd6" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="204" y="444" width="672" height="512" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
             f'<text x="540" y="530" font-family="serif" font-size="34" font-weight="700" fill="{INK}" text-anchor="middle">КОНКУРС</text>'
             f'<text x="540" y="580" font-family="serif" font-size="24" font-style="italic" fill="{LINE}" text-anchor="middle">придумайте знак переработки</text>'
             f'<path d="M 300 620 l 480 0" stroke="{LINE}" stroke-width="1.5"/>')
    b.append(recycle(540, 740, 0.62, LINE, "none", "qRec", 3))
    b.append('</g>')
    b.append(txt(540, 1090, "победителю — премия", 26, LINE, italic=True))
    b.append(txt(540, 1700, "задача: простой и понятный символ", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [paper(3), frame(), head()]
    b.append(txt(540, 200, "СТУДЕНТ ГЭРИ АНДЕРСОН", 40, INK, weight=900))
    b.append(txt(540, 252, "23 года", 28, LINE, italic=True))
    b.append(notebook(140, 420, 800, 560, -3, "deskBook"))
    b.append(recycle(380, 640, 0.85, LINE, "none", "sk1", 3))
    b.append(recycle(700, 700, 0.55, LINE, "none", "sk2", 2.5))
    b.append(pencil(300, 900, -8))
    b.append(f'<path d="M 640 960 l 300 0" stroke="{INK}" stroke-width="4"/>')
    for i in range(10):
        b.append(f'<path d="M {650+i*28} 960 l 0 12" stroke="{INK}" stroke-width="2"/>')
    b.append(txt(540, 1120, "эскиз за день или два", 30, INK, italic=True))
    b.append(txt(540, 1700, "без компьютеров — только карандаш и бумага", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [paper(4), frame(), head()]
    b.append(txt(540, 210, "ТРИ СТРЕЛКИ — ОДНА ПЕТЛЯ", 40, INK, weight=900))
    b.append(recycle(540, 700, 1.25, INK, PAPER_D, "bigRec4", 5))
    b.append(txt(540, 1120, "стрелки замкнулись в круг", 30, LINE, italic=True))
    b.append(txt(540, 1300, "движение без начала и конца", 30, INK, italic=True))
    b.append(txt(540, 1700, "знак читается с любого расстояния", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [paper(5), frame(), head()]
    b.append(txt(540, 210, "В ОСНОВЕ — ЛЕНТА МЁБИУСА", 36, INK, weight=900))
    # лента
    b.append(f'<g class="mobius"><path d="M 220 760 q 160 -220 320 0 q 160 220 320 0 q -160 220 -320 0 q -160 -220 -320 0 z" '
             f'fill="{PAPER_D}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 220 760 q 160 -220 320 0" fill="none" stroke="{INK}" stroke-width="2" opacity="0.5"/>'
             + "".join(f'<path d="M {250+i*40} {790 - (i%5)*30} q 30 -40 60 0" fill="none" stroke="{LINE}" stroke-width="1.2" opacity="0.5"/>' for i in range(12))
             + '</g>')
    b.append(txt(540, 1120, "у ленты всего одна сторона", 32, INK, italic=True))
    b.append(txt(540, 1180, "и один край", 28, LINE, italic=True))
    b.append(txt(540, 1400, "поэтому стрелки идут по кругу", 26, LINE))
    b.append(txt(540, 1700, "красивая математика в бытовом знаке", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [paper(6), frame(), head()]
    b.append(txt(540, 210, "РИСУНОК ПОБЕДИЛ", 44, INK, weight=900))
    b.append(f'<g class="cheque"><rect x="170" y="360" width="740" height="420" fill="#f7eeda" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="194" y="384" width="692" height="372" fill="none" stroke="{LINE}" stroke-width="1.5"/>'
             f'<text x="540" y="470" font-family="serif" font-size="28" fill="{LINE}" text-anchor="middle">ПРЕМИЯ</text>'
             f'<text x="540" y="600" font-family="serif" font-size="96" font-weight="900" fill="{INK}" text-anchor="middle">$2 500</text>'
             f'<text x="540" y="680" font-family="serif" font-size="24" font-style="italic" fill="{LINE}" text-anchor="middle">Гэри Андерсон · 1970</text></g>')
    b.append(recycle(250, 1020, 0.45, LINE, "none", "prizeRec", 3))
    b.append(txt(540, 1180, "премию потратил на учёбу", 30, INK, italic=True))
    b.append(txt(540, 1700, "победил не самый сложный, а самый понятный", 26, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [paper(7), frame(), head()]
    b.append(txt(540, 200, "ЗНАК РАЗОШЁЛСЯ ПО МИРУ", 38, INK, weight=900))
    for i, (x, y, s) in enumerate(((120, 420, 1.0), (420, 380, 1.2), (740, 430, 1.0),
                                   (180, 800, 1.15), (520, 780, 0.95), (820, 820, 1.1))):
        b.append(box(x, y, 200, 260, 30, f"b{i}"))
        b.append(recycle(x + 110, y + 120, 0.34, INK, "none", f"br{i}", 2.5))
        b.append(txt(x + 110, y + 220, ["PAPER", "PET", "GLASS", "METAL", "BOX", "MIX"][i], 18, LINE, family="Nunito, Arial"))
    b.append(txt(540, 1240, "упаковка, бутылки, контейнеры", 28, LINE, italic=True))
    b.append(txt(540, 1700, "студенческий эскиз стал международным символом", 24, LINE, italic=True))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [paper(8), frame(), head()]
    b.append(recycle(540, 640, 1.05, GREEN, PAPER_D, "finRec", 5))
    b.append(txt(540, 1000, "ИНОГДА БОЛЬШАЯ ИСТОРИЯ", 38, INK, weight=900))
    b.append(txt(540, 1058, "НАЧИНАЕТСЯ", 38, INK, weight=900))
    b.append(txt(540, 1116, "С ЛИСТА БУМАГИ", 38, GREEN, weight=900))
    # лист
    b.append(f'<g class="sheet"><path d="M 380 1280 l 320 0 l 0 300 l -60 60 l -260 0 z" fill="#f8f0dc" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M 640 1580 l 0 -60 l 60 0" fill="none" stroke="{INK}" stroke-width="3"/>'
             + "".join(f'<path d="M 410 {1330+i*40} l 260 0" stroke="{LINE}" stroke-width="1.4" opacity="0.5"/>' for i in range(5))
             + '</g>')
    b.append(txt(540, 1760, "1970 → сегодня", 26, LINE, italic=True))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".frame, .head", {opacity:0}, {opacity:1, duration:0.5}, 0);'
    'tl.fromTo(".bigRec", {opacity:0, scale:0.75, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.9, ease:"back.out(1.5)"}, 0.3);',

    'tl.fromTo(".board", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.fromTo(".qRec", {opacity:0}, {opacity:1, duration:0.6}, 0.7);',

    'tl.fromTo(".deskBook", {opacity:0, rotate:-8}, {opacity:1, rotate:-3, duration:0.7}, 0.15);'
    'tl.fromTo(".sk1", {opacity:0, scale:0.8, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.6}, 0.7);'
    'tl.fromTo(".sk2", {opacity:0}, {opacity:1, duration:0.5}, 1.1);'
    'tl.fromTo(".pen", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.5}, 1.2);',

    'tl.fromTo(".bigRec4 .ra", {opacity:0}, {opacity:1, duration:0.4}, 0.2);'
    'tl.fromTo(".bigRec4 .rb", {opacity:0}, {opacity:1, duration:0.4}, 0.7);'
    'tl.fromTo(".bigRec4 .rc", {opacity:0}, {opacity:1, duration:0.4}, 1.2);'
    'tl.to(".bigRec4", {rotate:6, transformOrigin:"50% 50%", duration:2.4, ease:"sine.inOut"}, 0.3);',

    'tl.fromTo(".mobius", {opacity:0, scale:0.9, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.8}, 0.2);'
    'tl.to(".mobius", {rotate:3, transformOrigin:"50% 50%", duration:3, yoyo:true, repeat:1, ease:"sine.inOut"}, 0.6);',

    'tl.fromTo(".cheque", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.2);'
    'tl.fromTo(".prizeRec", {opacity:0}, {opacity:1, duration:0.5}, 0.8);',

    'tl.fromTo(".bx", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, stagger:0.18}, 0.2);',

    'tl.fromTo(".finRec", {opacity:0, scale:0.8, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.8, ease:"back.out(1.5)"}, 0.2);'
    'tl.fromTo(".sheet", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.9);',
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
