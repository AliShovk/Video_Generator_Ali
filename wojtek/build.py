#!/usr/bin/env python3
"""«Войтек» — 7 сцен, кинематографичные силуэты."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/wojtek")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

DARK = "#241612"
INK = "#1b100c"
CREAM = "#f7e6c8"
GOLD = "#f0c060"
EMBER = "#ff9a3c"
SKY1 = "#f6c48a"
SKY2 = "#c9713c"
SKY3 = "#5a2f26"
SAND = "#e0b073"
OLIVE = "#5d6b3f"


def txt(x, y, s, size=44, col=CREAM, anchor="start", weight=900, cls="hl", ls=0, family="Nunito, Arial"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def vignette():
    return ('<defs><radialGradient id="vig" cx="50%" cy="45%" r="75%">'
            '<stop offset="55%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity="0.55"/></radialGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#vig)"/>')


def grain(seed=1, n=90):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.8):.1f}" '
                   f'fill="#fff2d0" opacity="{r.uniform(0.02,0.07):.2f}"/>' for _ in range(n))


def sky(c1=SKY1, c2=SKY2, c3=SKY3):
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="0.55" stop-color="{c2}"/>'
            f'<stop offset="1" stop-color="{c3}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#sky)"/>')


def smoke(cx, cy, w, h, op=0.35, cls="smoke"):
    return (f'<g class="{cls}" opacity="{op}"><ellipse cx="{cx}" cy="{cy}" rx="{w*0.5}" ry="{h*0.5}" fill="{CREAM}"/>'
            f'<ellipse cx="{cx-w*0.22}" cy="{cy+h*0.12}" rx="{w*0.3}" ry="{h*0.38}" fill="{CREAM}"/>'
            f'<ellipse cx="{cx+w*0.2}" cy="{cy+h*0.1}" rx="{w*0.34}" ry="{h*0.42}" fill="{CREAM}"/></g>')


def bear(cx, cy, s=1.0, col=DARK, crate=True, cls="bear", rot=0):
    b = [f'<g class="{cls}" transform="translate({cx} {cy}) rotate({rot}) scale({s})">']
    # ноги
    b.append(f'<path d="M -38 60 l 0 60 q 0 16 18 16 l 8 0 q 14 0 14 -16 l 0 -60 z" fill="{col}"/>')
    b.append(f'<path d="M 4 60 l 0 60 q 0 16 16 16 l 8 0 q 14 0 14 -16 l 0 -60 z" fill="{col}"/>')
    # тело
    b.append(f'<path d="M -62 40 q -30 -110 30 -140 l 64 0 q 60 30 30 140 q -16 46 -62 46 q -46 0 -62 -46 z" fill="{col}"/>')
    # голова
    b.append(f'<circle cx="0" cy="-152" r="46" fill="{col}"/>')
    b.append(f'<circle cx="-34" cy="-186" r="16" fill="{col}"/><circle cx="34" cy="-186" r="16" fill="{col}"/>')
    b.append(f'<ellipse cx="16" cy="-140" rx="22" ry="16" fill="{col}"/>')
    # лапы
    b.append(f'<path d="M -58 -20 q -26 40 -6 70" stroke="{col}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M 58 -20 q 26 40 6 70" stroke="{col}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    if crate:
        b.append(f'<rect x="-56" y="-46" width="112" height="94" rx="6" fill="#6b4a2a" stroke="#3a2416" stroke-width="4"/>')
        b.append(f'<path d="M -56 -16 l 112 0 M -56 22 l 112 0" stroke="#3a2416" stroke-width="3"/>')
        b.append(f'<path d="M 0 -46 l 0 94" stroke="#3a2416" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


def soldier(cx, cy, s=1.0, col=DARK, cls="sold", helmet=True):
    b = [f'<g class="{cls}" transform="translate({cx} {cy}) scale({s})">']
    b.append(f'<path d="M -22 0 l 0 -60 q 0 -20 22 -20 q 22 0 22 20 l 0 60 z" fill="{col}"/>')
    b.append(f'<path d="M -20 0 l -8 70 l 16 0 l 10 -60 M 20 0 l 8 70 l -16 0 l -10 -60" fill="{col}"/>')
    b.append(f'<circle cx="0" cy="-96" r="20" fill="{col}"/>')
    if helmet:
        b.append(f'<path d="M -26 -100 q 0 -26 26 -26 q 26 0 26 26 q -26 8 -52 0 z" fill="{col}"/>')
    b.append('</g>')
    return "".join(b)


def embers(n=16, seed=3):
    r = random.Random(seed)
    out = []
    for i in range(n):
        out.append(f'<circle class="emb" cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(600,1700):.0f}" r="{r.uniform(2,5):.1f}" '
                   f'fill="{EMBER}" opacity="{r.uniform(0.3,0.8):.2f}"/>')
    return "".join(out)


# ---------------------------------------------------------------- s1
def s1():
    b = [sky(), ]
    b.append(f'<circle cx="540" cy="760" r="300" fill="{EMBER}" opacity="0.25"/>')
    b.append(smoke(300, 900, 700, 500, 0.22, "sm1"))
    b.append(smoke(820, 1000, 620, 460, 0.18, "sm2"))
    b.append(bear(540, 900, 1.5, DARK, True, "bearHero"))
    b.append(embers(18, 2))
    b.append(f'<rect x="0" y="0" width="1080" height="620" fill="#1b100c" opacity="0.25"/>')
    b.append(txt(70, 250, "МЕДВЕДЬ", 96, CREAM, ls=6))
    b.append(txt(70, 360, "В СТРОЮ", 96, GOLD, ls=6))
    b.append(txt(74, 440, "капрал Войтек · 1942–1945", 30, CREAM, weight=700))
    b.append(vignette())
    b.append(grain(1))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [sky("#f7d7a8", "#dfa05e", "#8a5230")]
    b.append(f'<path d="M 0 1150 q 300 -80 540 -20 q 260 60 540 -10 L 1080 1920 L 0 1920 Z" fill="{SAND}"/>')
    b.append(f'<path d="M 0 1180 q 300 -80 540 -20 q 260 60 540 -10" stroke="#b9863f" stroke-width="4" fill="none" opacity="0.6"/>')
    # палатки
    for i, x in enumerate((180, 700, 900)):
        b.append(f'<g class="tent{i}"><path d="M {x-120} 1180 L {x} 980 L {x+120} 1180 Z" fill="#8a6a45" stroke="#5a3f28" stroke-width="5"/>'
                 f'<path d="M {x-40} 1180 L {x} 1060 L {x+40} 1180 Z" fill="#3f2d1f"/></g>')
    # солдаты и мальчик
    b.append(soldier(420, 1180, 1.25, DARK, "s2a"))
    b.append(soldier(520, 1180, 1.2, DARK, "s2b"))
    b.append(f'<g class="boy"><circle cx="640" cy="1100" r="20" fill="{DARK}"/>'
             f'<path d="M 620 1120 l 40 0 l 6 60 l -52 0 z" fill="{DARK}"/></g>')
    # медвежонок
    b.append(f'<g class="cub"><ellipse cx="730" cy="1150" rx="36" ry="30" fill="#6b4a30"/>'
             f'<circle cx="756" cy="1128" r="22" fill="#6b4a30"/>'
             f'<circle cx="744" cy="1110" r="8" fill="#6b4a30"/><circle cx="768" cy="1110" r="8" fill="#6b4a30"/></g>')
    b.append(txt(70, 260, "СИРИЯ · 1942", 52, INK, ls=4))
    b.append(txt(70, 330, "выкупили медвежонка у мальчика", 28, "#5a3f28", weight=700))
    b.append(vignette())
    b.append(grain(2))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [sky("#3a2a35", "#5a3428", "#241612")]
    b.append(f'<circle cx="540" cy="1150" r="420" fill="{EMBER}" opacity="0.18"/>')
    b.append(f'<path d="M 0 1250 L 1080 1250 L 1080 1920 L 0 1920 Z" fill="#2a1a14"/>')
    # палатка
    b.append(f'<path d="M 90 1250 L 540 700 L 990 1250 Z" fill="#3a2620" stroke="#1b100c" stroke-width="6"/>')
    b.append(f'<path d="M 300 1250 L 540 900 L 780 1250 Z" fill="#5a3a24" opacity="0.55"/>')
    # фонарь
    b.append(f'<g class="lantern"><circle cx="540" cy="900" r="90" fill="{GOLD}" opacity="0.28"/>'
             f'<rect x="528" y="880" width="24" height="40" rx="4" fill="{GOLD}"/></g>')
    b.append(bear(400, 1120, 1.15, DARK, False, "bearMug"))
    # кружка
    b.append(f'<g class="mug"><rect x="430" y="1040" width="46" height="58" rx="6" fill="#8a6a45"/>'
             f'<path d="M 476 1052 q 22 0 22 20 q 0 20 -22 20" fill="none" stroke="#8a6a45" stroke-width="8"/></g>')
    b.append(soldier(700, 1200, 1.15, DARK, "s3a"))
    b.append(soldier(820, 1210, 1.1, DARK, "s3b"))
    b.append(embers(14, 5))
    b.append(txt(70, 260, "ЖИЛ В ПАЛАТКЕ", 54, CREAM, ls=3))
    b.append(txt(70, 330, "пил пиво · вставал по команде «смирно»", 26, GOLD, weight=700))
    b.append(vignette())
    b.append(grain(3))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [sky("#e8a05a", "#a04a28", "#3a1f18")]
    b.append(f'<circle cx="300" cy="700" r="220" fill="{EMBER}" opacity="0.3"/>')
    # монастырь на холме
    b.append(f'<path d="M 620 980 L 900 980 L 900 760 L 620 760 Z" fill="#3a2a22"/>')
    b.append(f'<path d="M 620 760 L 700 700 L 760 700 L 760 760" fill="#3a2a22"/>')
    b.append(f'<path d="M 660 700 L 660 640 L 690 640 L 690 700" fill="#3a2a22"/>')
    b.append(f'<path d="M 780 760 L 780 690 L 830 690 L 830 760" fill="#3a2a22"/>')
    # дым и вспышки
    b.append(smoke(760, 640, 500, 380, 0.3, "sm4"))
    b.append(f'<circle class="flash4" cx="700" cy="660" r="120" fill="{EMBER}" opacity="0.25"/>')
    # руины
    b.append(f'<path d="M 0 1300 L 200 1240 L 320 1300 L 460 1230 L 600 1300 L 760 1250 L 900 1310 L 1080 1260 L 1080 1920 L 0 1920 Z" fill="#2a1a14"/>')
    b.append(bear(420, 1230, 1.35, DARK, True, "bearLoad", -6))
    b.append(soldier(230, 1290, 1.1, DARK, "s4a"))
    b.append(soldier(620, 1290, 1.15, DARK, "s4b"))
    b.append(embers(20, 7))
    b.append(txt(70, 250, "МОНТЕ-КАССИНО · 1944", 44, CREAM, ls=2))
    b.append(txt(70, 320, "ящики с боеприпасами — вверх по склону", 24, GOLD, weight=700))
    b.append(vignette())
    b.append(grain(4))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [sky("#e8b070", "#b5673a", "#4a2a20")]
    b.append(f'<rect x="0" y="700" width="1080" height="1220" fill="#2a1a14" opacity="0.55"/>')
    # погоны
    b.append(f'<g class="strapA"><rect x="120" y="880" width="330" height="120" rx="14" fill="#4a3a24" stroke="{GOLD}" stroke-width="5"/>'
             f'<path d="M 150 940 l 270 0" stroke="{GOLD}" stroke-width="6"/></g>')
    b.append(f'<g class="strapB"><rect x="630" y="880" width="330" height="120" rx="14" fill="#4a3a24" stroke="{GOLD}" stroke-width="5"/>'
             f'<path d="M 660 940 l 270 0" stroke="{GOLD}" stroke-width="6"/>'
             f'<path d="M 700 910 l 0 60 M 760 910 l 0 60" stroke="{GOLD}" stroke-width="8"/></g>')
    b.append(txt(285, 1080, "РЯДОВОЙ", 34, CREAM, "middle"))
    b.append(txt(795, 1080, "КАПРАЛ", 34, GOLD, "middle"))
    b.append(f'<path class="arrow5" d="M 470 940 l 120 0 M 560 920 l 30 20 l -30 20" stroke="{GOLD}" stroke-width="6" fill="none"/>')
    b.append(txt(540, 1300, "повышение в звании", 30, CREAM, "middle", 700))
    b.append(txt(70, 260, "ОТ РЯДОВОГО", 52, INK, ls=3))
    b.append(txt(70, 330, "ДО КАПРАЛА", 52, GOLD, ls=3))
    b.append(vignette())
    b.append(grain(5))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [sky("#3a2a24", "#4a2f24", "#241612")]
    b.append(f'<circle cx="540" cy="900" r="440" fill="{EMBER}" opacity="0.12"/>')
    # нашивка-щит
    b.append(f'<g class="patch"><path d="M 300 520 L 780 520 L 780 1120 L 540 1300 L 300 1120 Z" fill="#5d6b3f" stroke="{GOLD}" stroke-width="8"/>'
             f'<path d="M 330 550 L 750 550 L 750 1100 L 540 1262 L 330 1100 Z" fill="none" stroke="{GOLD}" stroke-width="3" opacity="0.7"/>')
    b.append(bear(540, 940, 1.0, "#2a1a14", True, "bearPatch"))
    b.append(txt(540, 1210, "22 КОМПАНИЯ СНАБЖЕНИЯ", 22, CREAM, "middle", 800))
    b.append('</g>')
    b.append(txt(70, 280, "ЭМБЛЕМА", 56, CREAM, ls=4))
    b.append(txt(70, 350, "медведь, несущий снаряд", 26, GOLD, weight=700))
    b.append(vignette())
    b.append(grain(6))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [sky("#c97a45", "#8a4a2c", "#2e1c16")]
    b.append(smoke(400, 1100, 800, 520, 0.2, "sm7"))
    b.append(bear(540, 1130, 1.15, DARK, True, "bearFinal", -3))
    b.append(embers(12, 9))
    b.append(txt(540, 300, "ВОЙТЕК", 92, CREAM, "middle", 900, ls=10))
    b.append(txt(540, 380, "капрал польской армии", 32, GOLD, "middle", 700))
    b.append(txt(540, 1640, "Imperial War Museum", 26, CREAM, "middle", 600))
    b.append(vignette())
    b.append(grain(7))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7]
ANIM = [
    'tl.fromTo(".bearHero", {opacity:0, y:40}, {opacity:1, y:0, duration:1.0, ease:"power2.out"}, 0.1);'
    'tl.to(".sm1", {x:60, duration:6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.to(".sm2", {x:-50, duration:7, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.to(".emb", {y:-40, opacity:0, duration:2.4, stagger:0.15, repeat:-1}, 0.5);',
    'tl.fromTo(".tent0, .tent1, .tent2", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6, stagger:0.2}, 0.2);'
    'tl.fromTo(".s2a, .s2b", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6, stagger:0.15}, 0.5);'
    'tl.fromTo(".boy, .cub", {opacity:0, scale:0.9, transformOrigin:"50% 100%"}, {opacity:1, scale:1, duration:0.6, stagger:0.2}, 0.9);',
    'tl.fromTo(".bearMug", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.2);'
    'tl.fromTo(".mug", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5}, 0.8);'
    'tl.to(".lantern", {opacity:0.55, duration:0.8, yoyo:true, repeat:-1}, 0);'
    'tl.fromTo(".s3a, .s3b", {opacity:0}, {opacity:1, duration:0.5, stagger:0.2}, 0.6);',
    'tl.fromTo(".bearLoad", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.8}, 0.2);'
    'tl.to(".bearLoad", {y:-8, duration:0.5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.6);'
    'tl.to(".flash4", {opacity:0.45, duration:0.25, yoyo:true, repeat:8, stagger:0.3}, 0.5);'
    'tl.to(".sm4", {x:40, duration:5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.fromTo(".s4a, .s4b", {opacity:0}, {opacity:1, duration:0.6, stagger:0.2}, 0.7);',
    'tl.fromTo(".strapA", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.6}, 0.2);'
    'tl.fromTo(".strapB", {opacity:0, x:40}, {opacity:1, x:0, duration:0.6}, 0.6);'
    'tl.fromTo(".arrow5", {opacity:0}, {opacity:1, duration:0.5}, 1.0);'
    'tl.to(".strapB", {scale:1.04, transformOrigin:"50% 50%", duration:0.6, yoyo:true, repeat:3}, 1.2);',
    'tl.fromTo(".patch", {opacity:0, scale:0.8, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.8, ease:"back.out(1.4)"}, 0.2);'
    'tl.to(".patch", {rotate:3, transformOrigin:"50% 50%", duration:2.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);',
    'tl.fromTo(".bearFinal", {opacity:0, y:30}, {opacity:1, y:0, duration:1.0}, 0.2);'
    'tl.to(".sm7", {x:-50, duration:6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.to(".emb", {y:-50, opacity:0, duration:2.6, stagger:0.2, repeat:-1}, 0.6);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{DARK}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.02 }}, {{ scale:1.08, duration:{dur}, ease:"none" }}, 0);
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
