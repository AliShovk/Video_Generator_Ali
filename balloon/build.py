#!/usr/bin/env python3
"""«Шар через границу» — 8 сцен, ночная сказка."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/balloon")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

NIGHT = "#0b1226"
NIGHT2 = "#16213f"
CREAM = "#f7ecd2"
GOLD = "#f2b64a"
CORAL = "#e2725b"
TEAL = "#3fa9a0"
PLUM = "#7b5ea7"
DIM = "#8fa0c0"


def t(x, y, s, size=46, col=CREAM, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def sky(c1=NIGHT, c2=NIGHT2):
    return ('<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sk)"/>')


def stars(n=40, seed=2):
    r = random.Random(seed)
    return "".join(f'<circle class="st" cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1400):.0f}" r="{r.uniform(1.5,4):.1f}" '
                   f'fill="{CREAM}" opacity="{r.uniform(0.25,0.9):.2f}"/>' for _ in range(n))


def balloon(cx, cy, r=300, cls="bl", cols=(CREAM, GOLD, CORAL, TEAL, PLUM, CREAM), with_basket=True, sag=1.0):
    """Лоскутная оболочка (клип по эллипсу) + корзина + стропы."""
    cid = f"clip_{cls}"
    ry = r * 1.22 * sag
    b = [f'<g class="{cls}">']
    b.append(f'<defs><clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}"/></clipPath></defs>')
    b.append(f'<g clip-path="url(#{cid})">')
    # вертикальные лоскуты
    n = 10
    for i in range(n):
        x0 = cx - r + (2 * r) * i / n
        w = (2 * r) / n + 2
        b.append(f'<rect x="{x0:.0f}" y="{cy-ry:.0f}" width="{w:.0f}" height="{2*ry:.0f}" fill="{cols[i % len(cols)]}"/>')
    b.append('</g>')
    # контур
    b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="none" stroke="{NIGHT}" stroke-width="7"/>')
    # блик
    b.append(f'<ellipse cx="{cx-r*0.35:.0f}" cy="{cy-r*0.45:.0f}" rx="{r*0.22:.0f}" ry="{ry*0.3:.0f}" fill="{CREAM}" opacity="0.16"/>')
    if with_basket:
        by = cy + ry + 120
        for dx in (-70, -25, 25, 70):
            b.append(f'<path d="M {cx+dx} {cy+ry*0.92:.0f} L {cx+dx*0.35:.0f} {by:.0f}" stroke="{CREAM}" stroke-width="3" opacity="0.7"/>')
        b.append(f'<rect x="{cx-70}" y="{by}" width="140" height="110" rx="14" fill="#8a5a34" stroke="{NIGHT}" stroke-width="6"/>')
        b.append(f'<path d="M {cx-70} {by+30} l 140 0" stroke="{NIGHT}" stroke-width="4" opacity="0.5"/>')
    b.append('</g>')
    return "".join(b)


def beam(x, y, cls, col=CREAM, op=0.18, w=140, h=1000):
    return (f'<g class="{cls}"><path d="M {x} {y} L {x-w} {y+h} L {x+w} {y+h} Z" fill="{col}" opacity="{op}"/></g>')


def silhouette_ground(y=1600, col="#060a14"):
    return f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="{col}"/>'


# ---------------------------------------------------------------- 1
def s1():
    b = [sky(), stars(46, 3)]
    b.append(f'<circle cx="880" cy="330" r="90" fill="{CREAM}" opacity="0.85"/>')
    b.append(f'<circle cx="850" cy="310" r="90" fill="{NIGHT2}" opacity="0.9"/>')
    b.append(balloon(540, 800, 300, "bl1"))
    b.append(silhouette_ground(1560))
    b.append(t(60, 260, "ШАР", 96, CREAM, ls=6))
    b.append(t(60, 360, "ИЗ ПРОСТЫНЕЙ", 62, GOLD, ls=1))
    b.append(t(64, 430, "побег через границу · 1979", 26, DIM, w=700))
    b.append(t(60, 1760, "две семьи · ночь · два километра", 24, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="#101224"/>']
    b.append(f'<circle cx="820" cy="700" r="360" fill="{GOLD}" opacity="0.10"/>')
    # стол, ткань, швейная машинка
    b.append(f'<rect x="80" y="1180" width="920" height="240" fill="#3a2a22" stroke="#060a14" stroke-width="8"/>')
    b.append(f'<path d="M 620 1080 q 60 -80 170 -30 l 0 130 l -170 0 z" fill="{CORAL}" stroke="#060a14" stroke-width="7"/>')
    b.append(f'<path d="M 300 1180 q 40 -120 180 -90 l 0 90 z" fill="{TEAL}" stroke="#060a14" stroke-width="7"/>')
    b.append(f'<rect x="640" y="980" width="220" height="120" rx="16" fill="#2b3350" stroke="#060a14" stroke-width="7"/>')
    b.append(f'<path d="M 700 980 l 0 -80 l 40 0 l 0 80" fill="#2b3350" stroke="#060a14" stroke-width="7"/>')
    b.append(f'<circle cx="750" cy="1024" r="10" fill="{GOLD}"/>')
    # двое
    b.append(f'<g class="m2a"><circle cx="300" cy="900" r="46" fill="#e8b48c"/><rect x="252" y="952" width="96" height="150" rx="24" fill="{TEAL}"/></g>')
    b.append(f'<g class="m2b"><circle cx="470" cy="930" r="42" fill="#e8b48c"/><rect x="426" y="978" width="88" height="140" rx="22" fill="{PLUM}"/></g>')
    b.append(t(60, 260, "1979", 84, GOLD, ls=4))
    b.append(t(60, 340, "шьют годами", 34, CREAM, w=800))
    b.append(t(60, 1660, "Петер Штрельчик и Гюнтер Ветцель", 26, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="#0d1020"/>']
    b.append(f'<circle cx="540" cy="900" r="420" fill="{CORAL}" opacity="0.14"/>')
    # баллоны
    for i, x in enumerate((300, 420, 540)):
        b.append(f'<rect x="{x}" y="1080" width="90" height="300" rx="40" fill="{TEAL}" stroke="#060a14" stroke-width="7"/>')
        b.append(f'<rect x="{x+34}" y="1040" width="22" height="50" fill="{GOLD}"/>')
    # горелка
    b.append(f'<path class="flame" d="M 540 1040 q -40 -90 0 -150 q 40 60 0 150 z" fill="{GOLD}"/>')
    b.append(f'<path d="M 470 1020 l 140 0" stroke="{CORAL}" stroke-width="14" stroke-linecap="round"/>')
    b.append(t(60, 260, "ГОРЕЛКА", 62, CREAM, ls=2))
    b.append(t(60, 330, "из газовых баллонов", 28, GOLD, w=700))
    b.append(t(60, 1640, "варили сами", 30, CREAM, w=800))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [sky("#1a1630", "#2a1a2c"), stars(24, 5)]
    # провисший шар
    b.append(balloon(540, 900, 280, "bl4", (CREAM, CORAL, CORAL, GOLD, CREAM, PLUM), True, 0.72))
    b.append(f'<path d="M 300 1120 q 240 90 480 0" stroke="{DIM}" stroke-width="5" fill="none" opacity="0.4"/>')
    b.append(t(60, 260, "ПЕРВЫЙ ПОЛЁТ", 56, CREAM, ls=1))
    b.append(t(60, 330, "не тянет троих", 34, CORAL, w=800))
    b.append(t(60, 1700, "провал", 40, GOLD, w=900))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="#0a0f1e"/>']
    b.append(f'<circle cx="540" cy="760" r="420" fill="{GOLD}" opacity="0.08"/>')
    b.append(balloon(540, 720, 250, "bl5", (CREAM, GOLD, TEAL, CORAL, CREAM, PLUM), True))
    # семья у корзины
    for i, (x, s, c) in enumerate(((360, 0.8, TEAL), (450, 0.75, CORAL), (540, 0.55, GOLD), (620, 0.55, PLUM))):
        b.append(f'<g class="fam{i}"><circle cx="{x}" cy="{1310-(s*0 if i<2 else 30)}" r="{34*s}" fill="#e8b48c"/>'
                 f'<rect x="{x-30*s}" y="{1345-(s*0 if i<2 else 30)}" width="{60*s}" height="{90*s}" rx="14" fill="{c}"/></g>')
    b.append(t(60, 250, "ВТОРОЙ ПОЛЁТ", 54, CREAM, ls=1))
    b.append(t(60, 320, "ночью, с детьми", 32, GOLD, w=800))
    b.append(t(60, 1700, "над полосой смерти", 30, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [sky("#0a1024", "#101a34"), stars(30, 7)]
    b.append(silhouette_ground(1500))
    b.append(beam(240, 1330, "beam1", GOLD, 0.17, 170, -980))
    b.append(beam(840, 1330, "beam2", GOLD, 0.17, 170, -980))
    b.append(balloon(560, 620, 210, "bl6", (CREAM, TEAL, GOLD, CORAL, CREAM, PLUM), True))
    for x in (240, 840):
        b.append(f'<rect x="{x}" y="1330" width="14" height="180" fill="#060a14"/>')
        b.append(f'<circle cx="{x+7}" cy="1320" r="16" fill="{GOLD}" opacity="0.8"/>')
    b.append(f'<g class="sol"><circle cx="540" cy="1390" r="24" fill="#060a14"/><rect x="514" y="1416" width="52" height="86" fill="#060a14"/></g>')
    b.append(t(60, 240, "ПОГРАНИЧНИКИ", 40, DIM, ls=2))
    b.append(t(60, 310, "видят только облако", 34, CREAM, w=800))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{NIGHT}"/>']
    b.append(f'<circle cx="540" cy="900" r="380" fill="{GOLD}" opacity="0.10"/>')
    b.append(t(540, 760, "2", 260, CREAM, "middle", 900))
    b.append(t(540, 900, "КМ", 90, GOLD, "middle", 900, ls=6))
    b.append(f'<path d="M 180 1080 l 720 0" stroke="{CREAM}" stroke-width="3" opacity="0.4"/>')
    b.append(t(540, 1160, "высота полёта", 28, DIM, "middle", 700))
    b.append(t(540, 1500, "ВНИЗУ —", 40, DIM, "middle", 800))
    b.append(t(540, 1590, "ЗАПАДНАЯ ГЕРМАНИЯ", 46, GOLD, "middle", 900))
    b.append(silhouette_ground(1700))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [sky(), stars(34, 11)]
    b.append(balloon(540, 700, 220, "bl8", (CREAM, GOLD, CORAL, TEAL, CREAM, PLUM), True))
    b.append(silhouette_ground(1600))
    b.append(t(540, 1180, "СРАБОТАЛО", 78, CREAM, "middle", 900, ls=3))
    b.append(t(540, 1250, "все остались живы", 30, GOLD, "middle", 700))
    b.append(t(540, 1760, "Der Spiegel · архив BStU (Штази)", 22, DIM, "middle", 700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".bl1", {opacity:0, y:60}, {opacity:1, y:0, duration:1.0, ease:"power2.out"}, 0.05);'
    'tl.to(".bl1", {y:-12, duration:2.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.1);'
    'tl.to(".st", {opacity:0.25, duration:1.2, stagger:0.04, yoyo:true, repeat:-1}, 0);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".m2a", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6}, 0.15);'
    'tl.fromTo(".m2b", {opacity:0, x:30}, {opacity:1, x:0, duration:0.6}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".flame", {opacity:0, scale:0.6}, {opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}, 0.2);'
    'tl.to(".flame", {scaleY:1.15, duration:0.35, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".bl4", {opacity:0, y:40}, {opacity:1, y:0, duration:0.9}, 0.05);'
    'tl.to(".bl4", {y:10, duration:1.0, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.45, stagger:0.12}, 0.1);',
    'tl.fromTo(".bl5", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.05);'
    'tl.fromTo(".fam0, .fam1, .fam2, .fam3", {opacity:0, y:20}, {opacity:1, y:0, duration:0.45, stagger:0.12}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0.1);',
    'tl.fromTo(".bl6", {opacity:0, y:40}, {opacity:1, y:0, duration:0.9}, 0.05);'
    'tl.to(".beam1", {rotate:14, transformOrigin:"240px 1330px", duration:2.6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.2);'
    'tl.to(".beam2", {rotate:-16, transformOrigin:"840px 1330px", duration:3.0, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.2);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0.1);',
    'tl.fromTo(".hl", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.05);',
    'tl.fromTo(".bl8", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.05);'
    'tl.to(".bl8", {y:-10, duration:2.0, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{NIGHT}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
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
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
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
