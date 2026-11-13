#!/usr/bin/env python3
"""«Люстиг: башня дважды» — 8 сцен, ар-деко."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/lustig")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#14141a"
BG2 = "#1d1d26"
GOLD = "#d9b26a"
GOLD_L = "#f0cf8a"
CREAM = "#f4e9d4"
WINE = "#6e1f2a"
TEAL = "#2f6b6b"
INK = "#0d0d12"


def txt(x, y, s, size=44, col=CREAM, anchor="start", weight=900, cls="hl", ls=0, family="Nunito, Arial"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def frame():
    return (f'<g class="fr"><rect x="40" y="40" width="1000" height="1840" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.75"/>'
            f'<rect x="54" y="54" width="972" height="1812" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.45"/>'
            + "".join(f'<path d="M {x} {y} l {dx*40} 0 M {x} {y} l 0 {dy*40}" stroke="{GOLD}" stroke-width="3"/>'
                      for x, y, dx, dy in [(54, 54, 1, 1), (1026, 54, -1, 1), (54, 1866, 1, -1), (1026, 1866, -1, -1)])
            + '</g>')


def rays(cx, cy, r=900, n=28, op=0.12, cls="rays"):
    out = [f'<g class="{cls}" opacity="{op}">']
    for i in range(n):
        a1 = 2 * math.pi * i / n
        a2 = a1 + math.pi / n * 0.7
        out.append(f'<path d="M {cx} {cy} L {cx + r*math.cos(a1):.0f} {cy + r*math.sin(a1):.0f} '
                   f'L {cx + r*math.cos(a2):.0f} {cy + r*math.sin(a2):.0f} Z" fill="{GOLD}"/>')
    out.append('</g>')
    return "".join(out)


def tower(cx, base_y=1500, h=900, w=380, col=GOLD, cls="tower", op=1.0):
    """Эйфелева башня: изогнутые ноги, арка, платформы, шпиль."""
    top = base_y - h
    hw = w * 0.5
    b = [f'<g class="{cls}" opacity="{op}">']
    d = (f"M {cx - hw} {base_y} "
         f"C {cx - hw*0.72} {base_y - h*0.14} {cx - hw*0.34} {base_y - h*0.24} {cx - hw*0.24} {base_y - h*0.32} "
         f"L {cx - hw*0.10} {base_y - h*0.62} L {cx - hw*0.055} {base_y - h*0.70} "
         f"L {cx - hw*0.022} {top} L {cx + hw*0.022} {top} "
         f"L {cx + hw*0.055} {base_y - h*0.70} L {cx + hw*0.10} {base_y - h*0.62} "
         f"L {cx + hw*0.24} {base_y - h*0.32} "
         f"C {cx + hw*0.34} {base_y - h*0.24} {cx + hw*0.72} {base_y - h*0.14} {cx + hw} {base_y} Z")
    b.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5"/>')
    # арка
    b.append(f'<path d="M {cx - hw*0.26} {base_y} Q {cx} {base_y - h*0.17} {cx + hw*0.26} {base_y}" '
             f'fill="none" stroke="{col}" stroke-width="4" opacity="0.9"/>')
    # решётка по высоте
    for i in range(16):
        t = i / 15
        y = base_y - h * 0.02 - h * 0.95 * t
        half = hw * (0.10 + 0.30 * (1 - t) ** 2) if t < 0.7 else hw * 0.03
        if t < 0.32:
            half = hw * (0.26 + 0.5 * (0.32 - t))
        b.append(f'<path d="M {cx-half:.0f} {y:.0f} L {cx+half:.0f} {y:.0f}" stroke="{col}" stroke-width="2" opacity="0.5"/>')
    # диагонали
    for i in range(12):
        t = i / 11
        x = cx - hw + hw * 2 * t
        b.append(f'<path d="M {x:.0f} {base_y} L {cx} {base_y - h*0.55:.0f}" stroke="{col}" stroke-width="1.4" opacity="0.25"/>')
    # платформы
    for fy, fw in ((0.32, 0.30), (0.62, 0.15), (0.70, 0.09)):
        y = base_y - h * fy
        b.append(f'<rect x="{cx - w*fw/2:.0f}" y="{y - 9:.0f}" width="{w*fw:.0f}" height="13" fill="{col}" opacity="0.9"/>')
    # шпиль
    b.append(f'<path d="M {cx} {top} L {cx} {top-64}" stroke="{col}" stroke-width="4"/>')
    b.append(f'<circle cx="{cx}" cy="{top-70}" r="5" fill="{col}"/>')
    b.append('</g>')
    return "".join(b)


def eyes(cx, cy, s=1.0, cls="eyes", op=0.9):
    """Пара «сканирующих» глаз."""
    return (f'<g class="{cls}" opacity="{op}" transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M -70 0 q 70 -52 140 0 q -70 52 -140 0 z" fill="none" stroke="{GOLD}" stroke-width="4"/>'
            f'<circle cx="0" cy="0" r="20" fill="{GOLD}"/><circle cx="0" cy="0" r="8" fill="{INK}"/>'
            f'<path class="lid" d="M -70 0 q 70 -52 140 0" fill="{BG}" opacity="0"/></g>')


def gentleman(cx, cy, s=1.0, col=INK, cls="gent", hat=True, coat=True):
    b = [f'<g class="{cls}" transform="translate({cx} {cy}) scale({s})">']
    # ноги
    b.append(f'<path d="M -26 0 l -6 118 l 22 0 l 10 -112 l 2 0 l 10 112 l 22 0 l -6 -118 Z" fill="{col}" stroke="{GOLD}" stroke-width="1.6"/>')
    # пальто
    b.append(f'<path d="M -34 4 L -26 -142 q 2 -28 26 -28 q 24 0 26 28 L 34 4 Z" fill="{col}" stroke="{GOLD}" stroke-width="2"/>')
    # руки
    b.append(f'<path d="M -26 -126 q -14 40 -10 96 M 26 -126 q 14 40 10 96" stroke="{GOLD}" stroke-width="1.6" fill="none" opacity="0.7"/>')
    # воротник и галстук
    b.append(f'<path d="M -12 -164 l 12 22 l 12 -22" fill="none" stroke="{GOLD}" stroke-width="2"/>')
    # голова
    b.append(f'<circle cx="0" cy="-192" r="24" fill="{col}" stroke="{GOLD}" stroke-width="2"/>')
    if hat:
        b.append(f'<path d="M -38 -198 q 38 -32 76 0 q 6 8 -2 10 l -72 0 q -8 -2 -2 -10 z" fill="{col}" stroke="{GOLD}" stroke-width="1.8"/>'
                 f'<rect x="-27" y="-208" width="54" height="10" rx="3" fill="{col}" stroke="{GOLD}" stroke-width="1.6"/>')
    if coat:
        b.append(f'<path d="M -10 -140 l 0 140 M 10 -140 l 0 140" stroke="{GOLD}" stroke-width="1.4" opacity="0.45"/>')
    b.append('</g>')
    return "".join(b)


def document(x, y, w=420, h=540, rot=-4, cls="doc"):
    lines = "".join(f'<path d="M {x+30} {y+120+i*34} l {w-60} 0" stroke="#8a7a5a" stroke-width="2" opacity="0.55"/>' for i in range(9))
    return (f'<g class="{cls}" transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x+16}" y="{y+16}" width="{w-32}" height="{h-32}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.8"/>'
            f'<text x="{x+30}" y="{y+70}" font-family="Nunito" font-size="26" font-weight="900" fill="{INK}">ДОГОВОР</text>'
            f'{lines}'
            f'<circle cx="{x+w-80}" cy="{y+h-90}" r="34" fill="none" stroke="{WINE}" stroke-width="4" opacity="0.8"/>'
            f'<text x="{x+w-80}" y="{y+h-80}" font-family="Nunito" font-size="16" font-weight="900" fill="{WINE}" '
            f'text-anchor="middle">ПЕЧАТЬ</text></g>')


def envelope(x, y, w=520, h=320, rot=0, cls="env"):
    return (f'<g class="{cls}" transform="rotate({rot} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{CREAM}" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M {x} {y} L {x+w/2} {y+h*0.62} L {x+w} {y} " fill="none" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="{x+w-150}" y="{y+h-90}" width="120" height="60" fill="{WINE}" opacity="0.9"/>'
            f'<text x="{x+w-90}" y="{y+h-50}" font-family="Nunito" font-size="18" font-weight="900" fill="{CREAM}" '
            f'text-anchor="middle">ФРАНКИ</text></g>')


def note(x, y, rot, cls="note"):
    return (f'<g class="{cls}" transform="rotate({rot} {x} {y})">'
            f'<rect x="{x-40}" y="{y-22}" width="80" height="44" rx="4" fill="#e8dcc0" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="12" fill="none" stroke="{WINE}" stroke-width="2"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 900, 1000, 30, 0.10, "rays1"), frame()]
    b.append(tower(540, 1520, 880, 440, GOLD, "towerHero", 0.95))
    b.append(eyes(880, 470, 1.0, "eyesA", 0.85))
    b.append(eyes(800, 300, 0.7, "eyesB", 0.5))
    b.append(txt(70, 220, "ПРОДАЛ БАШНЮ", 62, CREAM, ls=3))
    b.append(txt(70, 292, "ДВАЖДЫ", 62, GOLD, ls=8))
    b.append(txt(74, 356, "Виктор Люстиг · Париж · 1925", 26, GOLD_L, weight=700))
    b.append(txt(540, 1720, "афера, вошедшая в историю криминалистики", 24, CREAM, "middle", 600))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 700, 950, 26, 0.09, "rays2"), frame()]
    # город
    r = random.Random(4)
    for i in range(9):
        x = 40 + i * 120
        h = 160 + r.randint(0, 160)
        b.append(f'<rect x="{x}" y="{1250-h}" width="100" height="{h}" fill="{BG2}" stroke="{GOLD}" stroke-width="1.5" opacity="0.7"/>')
        for k in range(4):
            b.append(f'<rect x="{x+14+k*20}" y="{1250-h+20}" width="10" height="14" fill="{GOLD}" opacity="0.35"/>')
    b.append(f'<rect x="0" y="1250" width="1080" height="670" fill="{BG2}"/>')
    b.append(tower(760, 1250, 620, 210, GOLD, "tower2", 0.95))
    b.append(txt(70, 260, "ПАРИЖ", 72, CREAM, ls=6))
    b.append(txt(70, 340, "1925 год", 36, GOLD, weight=700, ls=2))
    b.append(txt(70, 1500, "Эйфелеву башню собирались сдать в лом", 26, CREAM, weight=600))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 1200, 900, 24, 0.08, "rays3"), frame()]
    b.append(tower(830, 1380, 760, 300, GOLD, "tower3", 0.28))
    b.append(gentleman(200, 1150, 1.45, "#3a3444", "g3a"))
    b.append(gentleman(340, 1170, 1.4, "#2f2a3a", "g3b"))
    b.append(document(600, 800, 340, 430, -6, "doc3"))
    b.append(txt(70, 250, "СДЕЛКА", 64, CREAM, ls=6))
    b.append(txt(70, 320, "«башню сдадут в лом — тайно»", 26, GOLD_L, weight=700))
    b.append(txt(70, 1560, "документы · подпись · печать", 26, CREAM, weight=600))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 1000, 950, 28, 0.10, "rays4"), frame()]
    b.append(envelope(300, 900, 520, 320, -4, "env4"))
    for i, (x, y, rot) in enumerate(((250, 760, -18), (420, 700, 12), (600, 760, -8), (760, 820, 16), (540, 1180, -12))):
        b.append(note(x, y, rot, f"n{i}"))
    b.append(txt(70, 250, "КОНВЕРТ", 64, CREAM, ls=6))
    b.append(txt(70, 320, "с деньгами за башню", 26, GOLD_L, weight=700))
    b.append(txt(70, 1600, "поверил и заплатил", 30, GOLD, weight=700))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 900, 950, 26, 0.08, "rays5"), frame()]
    b.append(tower(300, 1500, 700, 230, GOLD, "t1", 0.9))
    b.append(tower(780, 1500, 700, 230, GOLD, "t2", 0.9))
    b.append(txt(300, 1640, "ПЕРВЫЙ РАЗ", 26, GOLD_L, "middle", 700))
    b.append(txt(780, 1640, "ВТОРОЙ РАЗ", 26, GOLD_L, "middle", 700))
    b.append(f'<path class="loop5" d="M 420 1500 q 120 -220 240 0" fill="none" stroke="{WINE}" stroke-width="6" stroke-dasharray="14 12"/>')
    b.append(txt(70, 250, "ДВАЖДЫ", 72, GOLD, ls=8))
    b.append(txt(70, 330, "одна и та же башня", 28, CREAM, weight=600))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 900, 900, 22, 0.07, "rays6"), frame()]
    # папка
    b.append(f'<g class="folder"><rect x="150" y="520" width="780" height="900" rx="12" fill="#c9b48a" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="150" y="470" width="300" height="70" rx="10" fill="#b5a077" stroke="{INK}" stroke-width="4"/>'
             f'<text x="300" y="520" font-family="Nunito" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">ДЕЛО LUSTIG</text>'
             f'<text x="540" y="760" font-family="Nunito" font-size="120" font-weight="900" fill="{WINE}" text-anchor="middle">FBI</text>'
             f'<path d="M 260 900 l 560 0 M 260 980 l 560 0 M 260 1060 l 380 0" stroke="#6b5a3a" stroke-width="4" opacity="0.6"/>'
             f'<g class="stamp6"><rect x="620" y="1180" width="240" height="90" rx="8" fill="none" stroke="{WINE}" stroke-width="5" transform="rotate(-8 740 1225)"/>'
             f'<text x="740" y="1240" font-family="Nunito" font-size="26" font-weight="900" fill="{WINE}" text-anchor="middle" transform="rotate(-8 740 1225)">АРХИВ</text></g></g>')
    b.append(txt(70, 300, "ИСТОРИЯ КРИМИНАЛИСТИКИ", 34, CREAM, ls=2))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 960, 900, 30, 0.1, "rays7"), frame()]
    # газета
    b.append(f'<g class="paper"><rect x="110" y="420" width="860" height="1000" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>'
             f'<text x="540" y="540" font-family="Nunito" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">LE JOURNAL</text>'
             f'<path d="M 140 570 l 800 0" stroke="{INK}" stroke-width="3"/>'
             f'<text x="540" y="760" font-family="Nunito" font-size="86" font-weight="900" fill="{INK}" text-anchor="middle">АФЕРА</text>'
             f'<text x="540" y="860" font-family="Nunito" font-size="86" font-weight="900" fill="{WINE}" text-anchor="middle">ВЕКА</text>'
             f'<path d="M 160 920 l 760 0 M 160 990 l 760 0 M 160 1060 l 620 0 M 160 1130 l 760 0 M 160 1200 l 480 0" stroke="#8a7a5a" stroke-width="3" opacity="0.6"/>'
             f'<rect x="160" y="1240" width="300" height="150" fill="{BG2}"/>'
             f'<circle cx="310" cy="1315" r="46" fill="none" stroke="{GOLD}" stroke-width="4"/></g>')
    b.append(txt(70, 300, "ПАРИЖСКАЯ ПРЕССА", 30, GOLD_L, ls=3))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', rays(540, 800, 950, 28, 0.09, "rays8"), frame()]
    b.append(tower(540, 1300, 700, 260, GOLD, "towerFin", 0.8))
    b.append(eyes(180, 1500, 0.6, "eyesF", 0.35))
    b.append(txt(540, 300, "ВИКТОР", 64, CREAM, "middle", 900, ls=8))
    b.append(txt(540, 372, "ЛЮСТИГ", 64, GOLD, "middle", 900, ls=8))
    b.append(txt(540, 1640, "источник: архив ФБР, дело Lustig", 24, GOLD_L, "middle", 600))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".towerHero", {opacity:0, y:40}, {opacity:1, y:0, duration:1.0}, 0.1);'
    'tl.to(".rays1", {rotate:8, transformOrigin:"540px 900px", duration:12, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0);'
    'tl.to(".eyesA", {scaleX:1.1, duration:2.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.6);'
    'tl.to(".eyesB", {scaleX:1.08, duration:2.8, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);',
    'tl.fromTo(".tower2", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.2);'
    'tl.to(".rays2", {rotate:-6, transformOrigin:"540px 700px", duration:14, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.2}, 0.1);',
    'tl.fromTo(".g3a", {opacity:0}, {opacity:1, duration:0.8}, 0.2);'
    'tl.fromTo(".g3b", {opacity:0}, {opacity:1, duration:0.8}, 0.5);'
    'tl.fromTo(".doc3", {opacity:0, y:30, rotate:-12}, {opacity:1, y:0, rotate:-6, duration:0.7}, 0.8);'
    'tl.to(".rays3", {rotate:5, transformOrigin:"540px 1200px", duration:12, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0);',
    'tl.fromTo(".env4", {opacity:0, y:40}, {opacity:1, y:0, duration:0.7}, 0.2);'
    'tl.fromTo(".note", {opacity:0, y:-40}, {opacity:1, y:0, duration:0.8, stagger:0.12}, 0.7);'
    'tl.to(".note", {y:-16, rotation:"+=4", duration:1.6, stagger:0.08, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.4);',
    'tl.fromTo(".t1", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.2);'
    'tl.fromTo(".t2", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.7);'
    'tl.to(".loop5", {strokeDashoffset:-120, duration:2, repeat:-1, ease:"none"}, 0.5);',
    'tl.fromTo(".folder", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.2);'
    'tl.fromTo(".stamp6", {opacity:0, scale:1.4, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.5}, 0.9);',
    'tl.fromTo(".paper", {opacity:0, y:40}, {opacity:1, y:0, duration:0.8}, 0.2);'
    'tl.to(".rays7", {rotate:6, transformOrigin:"540px 960px", duration:12, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0);',
    'tl.fromTo(".towerFin", {opacity:0, y:30}, {opacity:1, y:0, duration:1.0}, 0.2);'
    'tl.to(".eyesF", {opacity:0.7, duration:1.6, yoyo:true, repeat:-1}, 0.6);'
    'tl.to(".rays8", {rotate:-8, transformOrigin:"540px 800px", duration:14, repeat:-1, yoyo:true, ease:"sine.inOut"}, 0);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.02 }}, {{ scale:1.07, duration:{dur}, ease:"none" }}, 0);
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
