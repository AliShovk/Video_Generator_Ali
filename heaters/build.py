#!/usr/bin/env python3
"""«Виды обогревателей» — 10 сцен, у каждой своя палитра и своя анимация."""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, "/root/video-gen")
from icons import icon

ROOT = Path("/root/video-gen/heaters")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(10):
    end = STARTS[i + 1] if i + 1 < 10 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

DEFS = """<defs>
<linearGradient id="steelG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f5f7"/><stop offset="0.5" stop-color="#c9d3da"/><stop offset="1" stop-color="#8f9ba4"/></linearGradient>
<linearGradient id="oilG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f0e3d0"/><stop offset="1" stop-color="#c9ab8a"/></linearGradient>
<linearGradient id="hotG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb066"/><stop offset="1" stop-color="#e0592a"/></linearGradient>
<radialGradient id="glowO"><stop offset="0" stop-color="#ff9a4d" stop-opacity="0.85"/><stop offset="1" stop-color="#ff9a4d" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def txt(x, y, t, size=56, col="#ffffff", weight=900, anchor="start", cls="hl", spacing="-1"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{col}" text-anchor="{anchor}" letter-spacing="{spacing}">{t}</text>')


# ---------------------------------------------------------------- обогреватели
def convector(x, y, w=90, h=560, col="url(#steelG)"):
    ribs = "".join(f'<line x1="{x+8}" y1="{y+40 + i*14}" x2="{x+8}" y2="{y+h-20}" stroke="#7d8a93" stroke-width="3" opacity="0.5"/>'
                   for i in range(int((h-60)/14)))
    return (f'<g class="conv"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" stroke="#7d8a93" stroke-width="3"/>'
            f'<rect x="{x+6}" y="{y+16}" width="{w-12}" height="26" rx="6" fill="#7d8a93" opacity="0.55"/>'
            f'{ribs}'
            f'<rect x="{x+10}" y="{y+h-54}" width="{w-20}" height="20" rx="6" fill="#5f6b74" opacity="0.5"/></g>')


def oil(x, y, fins=9, fw=34, fh=430, col="url(#oilG)"):
    out = ['<g class="oilG">']
    for i in range(fins):
        out.append(f'<rect x="{x + i*fw + 4}" y="{y+14}" width="{fw-8}" height="{fh-14}" rx="12" fill="#000" opacity="0.12"/>')
        out.append(f'<rect class="fin" x="{x + i*fw}" y="{y}" width="{fw-8}" height="{fh}" rx="16" fill="{col}" stroke="#8a6b4a" stroke-width="4"/>')
        for j in range(7):
            out.append(f'<line x1="{x + i*fw + 4}" y1="{y + 24 + j*54}" x2="{x + i*fw + fw - 10}" y2="{y + 24 + j*54}" stroke="#b99a78" stroke-width="3" opacity="0.6"/>')
    out.append(f'<rect x="{x-6}" y="{y-18}" width="{fins*fw+6}" height="22" rx="10" fill="#9c7f60"/>')
    out.append(f'<rect x="{x-6}" y="{y+fh-4}" width="{fins*fw+6}" height="22" rx="10" fill="#9c7f60"/>')
    out.append(f'<circle cx="{x+30}" cy="{y+fh+22}" r="20" fill="#2b2b2b"/><circle cx="{x+fins*fw-40}" cy="{y+fh+22}" r="20" fill="#2b2b2b"/>')
    out.append('</g>')
    return "".join(out)


def fan(x, y, w=300, h=260, col="#2f4858", accent="#6fd3ff"):
    cx, cy = x + w / 2, y + h / 2
    blades = "".join(
        f'<g class="blade"><path d="M {cx} {cy} L {cx+92} {cy-30} Q {cx+116} {cy+14} {cx+58} {cy+34} Z" '
        f'fill="{accent}" opacity="0.85" transform="rotate({i*90} {cx} {cy})"/></g>' for i in range(4))
    grille = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{accent}" stroke-width="2" opacity="0.35"/>'
                     for r in (128, 104, 80))
    return (f'<g class="fanG"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="{col}" stroke="#1b2d38" stroke-width="5"/>'
            f'<circle cx="{cx}" cy="{cy}" r="140" fill="#0f2029" stroke="{accent}" stroke-width="4" opacity="0.95"/>'
            f'{grille}{blades}<circle cx="{cx}" cy="{cy}" r="18" fill="{accent}"/>'
            f'<circle cx="{x+w-70}" cy="{y+h-56}" r="18" fill="{accent}" opacity="0.7"/>'
            f'<circle cx="{x+w-120}" cy="{y+h-56}" r="18" fill="{accent}" opacity="0.4"/>'
            f'<rect x="{x+30}" y="{y+h-46}" width="{w-200}" height="10" rx="5" fill="{accent}" opacity="0.35"/></g>')


def tower(x, y, w=190, h=560, col="#e9eef1", accent="#4a90c2"):
    holes = "".join(
        f'<circle cx="{x + 24 + (i%7)*24}" cy="{y + 120 + (i//7)*30}" r="6" fill="#b9c6ce"/>' for i in range(56))
    return (f'<g class="towerG"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="42" fill="{col}" stroke="#b9c6ce" stroke-width="4"/>'
            f'<rect x="{x+18}" y="{y+18}" width="{w-36}" height="80" rx="18" fill="{accent}" opacity="0.85"/>'
            f'{holes}'
            f'<ellipse cx="{x+w/2}" cy="{y+h+18}" rx="{w/2-10}" ry="26" fill="#8fa3b1" opacity="0.5"/></g>')


def panel_ir(x, y, w=520, h=330, accent="#ff8a3d"):
    tubes = "".join(f'<rect x="{x+30 + i*90}" y="{y+40}" width="46" height="{h-120}" rx="20" fill="{accent}" opacity="0.9"/>' for i in range(5))
    return (f'<g class="irG"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#2a2c30" stroke="#4a4d52" stroke-width="4"/>'
            f'<rect x="{x+14}" y="{y+14}" width="{w-28}" height="{h-28}" rx="12" fill="none" stroke="#6b6f75" stroke-width="3"/>'
            f'{tubes}</g>')


# ---------------------------------------------------------------- s1
def s1():
    b = ['<rect width="1080" height="1920" fill="#0d1a24"/>']
    b.append(f'<circle cx="540" cy="500" r="380" fill="#16303f" opacity="0.7"/>')
    for i in range(24):
        b.append(f'<circle class="snowF" cx="{(i*89) % 1080}" cy="{(i*151) % 1500}" r="{2 + i%3}" fill="#cfe6f2" opacity="0.6"/>')
    b.append(convector(120, 1180, 80, 380, "#5b6b76"))
    b.append(oil(280, 1140, 5, 26, 300, "#6b5b4d"))
    b.append(fan(520, 1220, 200, 170, "#33454f", "#5b7583"))
    b.append(tower(800, 1120, 130, 420, "#5b6b76", "#3d5866"))
    b.append(txt(540, 340, "КАКОЙ", 96, "#ffffff", 900, "middle"))
    b.append(txt(540, 450, "ВЫБРАТЬ?", 96, "#ffb066", 900, "middle"))
    b.append(txt(540, 560, "четыре принципа — четыре задачи", 32, "#9fb3c0", 800, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s2 конвектор
def s2():
    b = ['<rect width="1080" height="1920" fill="#f4ead8"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="14" fill="#d9c9ad"/>')
    b.append(f'<rect x="120" y="540" width="14" height="900" fill="#d9c9ad"/>')
    b.append(f'<g class="conv2">{convector(120, 560, 110, 860, "url(#steelG)")}</g>')
    for i in range(7):
        b.append(f'<path class="air2" d="M {300 + i*40} 1500 q 30 -120 0 -240" stroke="#e0904a" stroke-width="9" fill="none" opacity="0.55"/>')
    b.append(icon("mdi-thermostat", 760, 620, 110, "#7a5a2a"))
    b.append(f'<rect x="700" y="760" width="280" height="80" rx="40" fill="#ffffff" opacity="0.8"/>')
    b.append(txt(840, 812, "+22°", 46, "#7a5a2a", 900, "middle"))
    b.append(txt(60, 1730, "КОНВЕКТОР", 74, "#2a2418"))
    b.append(txt(60, 1800, "тихо · на стену · постепенно", 34, "#7a6a4a", 800))
    return svg("".join(b))


# ---------------------------------------------------------------- s3 масляный
def s3():
    b = ['<rect width="1080" height="1920" fill="#5d2f24"/>']
    b.append(f'<circle cx="540" cy="1000" r="520" fill="url(#glowO)" opacity="0.45"/>')
    b.append(oil(210, 780, 9, 70, 520, "url(#oilG)"))
    b.append(f'<g class="waves3">' + "".join(
        f'<path d="M {140 + i*120} 1420 q 40 -60 0 -120 q -40 -60 0 -120" stroke="#ffbf7a" stroke-width="8" fill="none" opacity="0.5"/>' for i in range(7)) + '</g>')
    b.append(txt(60, 220, "МАСЛЯНЫЙ", 72, "#ffe2c2"))
    b.append(txt(60, 300, "РАДИАТОР", 72, "#ffb066"))
    b.append(txt(60, 380, "медленно, но долго", 34, "#e8bfa0", 800))
    b.append(txt(1020, 1700, "9 секций", 40, "#ffd9b8", 900, "end"))
    return svg("".join(b))


# ---------------------------------------------------------------- s4 вентиляторный
def s4():
    b = ['<rect width="1080" height="1920" fill="#0b2433"/>']
    b.append(f'<rect x="0" y="1250" width="1080" height="670" fill="#0f2f42"/>')
    b.append(fan(120, 700, 460, 420, "#16394d", "#6fd3ff"))
    for i in range(6):
        b.append(f'<path class="jet4" d="M {600 + i*10} {880 + i*40} q 180 -30 380 0" stroke="#9fe6ff" stroke-width="{14 - i}" fill="none" opacity="0.75"/>')
    for i in range(3):
        b.append(f'<path class="sound4" d="M 640 1240 q 60 -40 120 0" stroke="#6fd3ff" stroke-width="6" fill="none" opacity="0.5"/>')
    b.append(txt(60, 1700, "ВЕНТИЛЯТОРНЫЙ", 66, "#ffffff"))
    b.append(txt(60, 1770, "быстро · шумно · сушит", 34, "#9fd8ee", 800))
    b.append(txt(1020, 300, "3 сек", 90, "#6fd3ff", 900, "end"))
    return svg("".join(b))


# ---------------------------------------------------------------- s5 инфракрасный
def s5():
    b = ['<rect width="1080" height="1920" fill="#17181b"/>']
    b.append(panel_ir(80, 520, 520, 380))
    b.append(f'<circle cx="340" cy="710" r="360" fill="url(#glowO)" opacity="0.55" class="glow5"/>')
    for i in range(7):
        ang = -18 + i * 6
        b.append(f'<path class="ray5" d="M 620 700 L {980} {560 + i*70}" stroke="#ff9a4d" stroke-width="7" opacity="0.45"/>')
    b.append(f'<g class="man5"><circle cx="840" cy="1180" r="46" fill="#40444a"/>'
             f'<rect x="800" y="1230" width="80" height="150" rx="30" fill="#40444a"/>'
             f'<rect x="812" y="1380" width="22" height="140" rx="10" fill="#40444a"/>'
             f'<rect x="846" y="1380" width="22" height="140" rx="10" fill="#40444a"/></g>')
    b.append(txt(60, 1700, "ИНФРАКРАСНЫЙ", 62, "#ffd2a8"))
    b.append(txt(60, 1770, "греет предметы, а не воздух", 32, "#c9a98e", 800))
    return svg("".join(b))


# ---------------------------------------------------------------- s6 керамика
def s6():
    b = ['<rect width="1080" height="1920" fill="#e9f2ec"/>']
    b.append(f'<circle cx="540" cy="900" r="420" fill="#d3e8dd"/>')
    b.append(tower(430, 620, 240, 720, "#ffffff", "#4a90c2"))
    for i in range(5):
        b.append(f'<path class="sway6" d="M {700 + i*28} 900 q 40 -70 0 -140" stroke="#7fb8a0" stroke-width="7" fill="none" opacity="0.5"/>')
    b.append(txt(540, 260, "КЕРАМИЧЕСКАЯ", 62, "#1f3b2e", 900, "middle"))
    b.append(txt(540, 330, "БАШНЯ", 62, "#2c8a58", 900, "middle"))
    b.append(txt(540, 1640, "мягкий поток · поворот · для спальни", 32, "#4a6b5a", 800, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s7 сравнение
def s7():
    b = ['<rect width="1080" height="1920" fill="#101a1f"/>']
    b.append(txt(540, 220, "СРАВНЕНИЕ", 62, "#ffffff", 900, "middle"))
    cols = [("КОНВЕКТОР", "#f0c860", [0.5, 0.9, 0.8]),
            ("МАСЛО", "#e08a5a", [0.3, 1.0, 0.7]),
            ("ВЕНТИЛЯТОР", "#6fd3ff", [1.0, 0.2, 1.0]),
            ("ИК", "#ff9a4d", [0.8, 0.95, 1.0])]
    for ci, (name, col, bars) in enumerate(cols):
        x = 70 + ci * 245
        b.append(f'<g class="card7"><rect x="{x}" y="360" width="210" height="980" rx="22" fill="#182630"/>'
                 f'<text x="{x+105}" y="430" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{col}" text-anchor="middle">{name}</text>')
        for bi, v in enumerate(bars):
            h = int(600 * v)
            b.append(f'<rect class="bar7 b{ci}{bi}" x="{x+40}" y="{1180 - h}" width="130" height="{h}" rx="14" fill="{col}" opacity="0.8"/>')
        b.append('</g>')
    labels = ["скорость", "шум", "расход"]
    for bi, t in enumerate(labels):
        b.append(txt(1040, 1370 + bi * 40, t, 22, "#8fa3b1", 800, "end"))
    return svg("".join(b))


# ---------------------------------------------------------------- s8 расчёт
def s8():
    b = ['<rect width="1080" height="1920" fill="#eef2f5"/>']
    b.append(f'<rect x="80" y="420" width="920" height="620" rx="26" fill="#ffffff" stroke="#cfd8de" stroke-width="5"/>')
    b.append(txt(140, 560, "100 Вт × м²", 84, "#1f2c36"))
    b.append(f'<line x1="140" y1="620" x2="940" y2="620" stroke="#e2e8ec" stroke-width="4"/>')
    b.append(txt(140, 720, "комната 20 м²", 48, "#5d7280", 800))
    b.append(txt(940, 720, "2000 Вт", 64, "#c0392b", 900, "end"))
    b.append(txt(140, 840, "потолок до 3 м, обычное утепление", 30, "#7d8a93", 700))
    b.append(txt(140, 940, "холодная стена или гараж — плюс 20–30%", 30, "#7d8a93", 700))
    b.append(icon("mdi-calculator", 800, 1000, 120, "#5d7280"))
    b.append(txt(540, 1500, "МОЩНОСТЬ ПО ПЛОЩАДИ", 46, "#1f2c36", 900, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s9 безопасность
def s9():
    b = ['<rect width="1080" height="1920" fill="#fbf3e6"/>']
    b.append(txt(60, 260, "БЕЗОПАСНОСТЬ", 64, "#2a2418"))
    rows = [("mdi-water", "защита от брызг", "ванная"),
            ("mdi-alert-circle", "защита от опрокидывания", "дом"),
            ("mdi-thermostat", "термостат и отключение", "везде")]
    for i, (ic, t1, t2) in enumerate(rows):
        y = 620 + i * 380
        b.append(f'<g class="safe"><rect x="80" y="{y}" width="920" height="300" rx="24" fill="#ffffff" stroke="#e6d8c2" stroke-width="4"/>'
                 f'{icon(ic, 130, y + 90, 110, "#c0392b")}'
                 f'<text x="300" y="{y+140}" font-family="Nunito, Arial" font-size="44" font-weight="900" fill="#2a2418">{t1}</text>'
                 f'<text x="300" y="{y+200}" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="#8a7a5c">{t2}</text></g>')
    return svg("".join(b))


# ---------------------------------------------------------------- s10 итог
def s10():
    b = ['<rect width="1080" height="1920" fill="#0f1418"/>']
    b.append(txt(540, 220, "ЧТО КУДА", 64, "#ffffff", 900, "middle"))
    pairs = [("СПАЛЬНЯ", "конвектор", "#f0c860"), ("ВАННАЯ", "с защитой IP", "#6fd3ff"),
             ("ГАРАЖ", "инфракрасный", "#ff9a4d"), ("БЫСТРО", "вентилятор", "#e08a5a")]
    for i, (room, kind, col) in enumerate(pairs):
        y = 480 + i * 300
        b.append(f'<g class="row10"><rect x="70" y="{y}" width="940" height="230" rx="20" fill="#18242c"/>'
                 f'<text x="120" y="{y+90}" font-family="Nunito, Arial" font-size="44" font-weight="900" fill="#ffffff">{room}</text>'
                 f'<text x="120" y="{y+160}" font-family="Nunito, Arial" font-size="36" font-weight="900" fill="{col}">{kind}</text>'
                 f'<circle cx="930" cy="{y+115}" r="34" fill="{col}" opacity="0.85"/></g>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
BGS = ["#0d1a24", "#f4ead8", "#5d2f24", "#0b2433", "#17181b", "#e9f2ec", "#101a1f", "#eef2f5", "#fbf3e6", "#0f1418"]

# у каждой сцены свой набор анимаций
ANIM = [
    'tl.to(".snowF", {y:120, x:20, duration:3.4, stagger:0.05, repeat:2, ease:"none"}, 0);'
    'tl.fromTo(".conv", {y:60, opacity:0}, {y:0, opacity:1, duration:0.8, ease:"power2.out"}, 0.2);'
    'tl.fromTo(".oilG", {y:60, opacity:0}, {y:0, opacity:1, duration:0.8, ease:"power2.out"}, 0.5);'
    'tl.fromTo(".fanG", {y:40, opacity:0}, {y:0, opacity:1, duration:0.8, ease:"power2.out"}, 0.8);'
    'tl.fromTo(".towerG", {y:60, opacity:0}, {y:0, opacity:1, duration:0.8, ease:"power2.out"}, 1.1);',
    'tl.fromTo(".conv2", {x:-160, opacity:0}, {x:0, opacity:1, duration:1.1, ease:"power3.out"}, 0.1);'
    'tl.to(".air2", {x:40, opacity:0.2, duration:1.6, stagger:0.12, repeat:4, ease:"sine.inOut"}, 0.5);',
    'tl.fromTo(".fin", {scaleY:0.4, transformOrigin:"50% 100%", opacity:0}, {scaleY:1, opacity:1, duration:0.5, stagger:0.07, ease:"back.out(2)"}, 0.1);'
    'tl.fromTo(".oilG", {opacity:0}, {opacity:1, duration:0.4}, 0.05);'
    'tl.to(".waves3", {y:-40, opacity:0.25, duration:2.0, yoyo:true, repeat:3, ease:"sine.inOut"}, 0.4);',
    'tl.to(".blade", {rotation:360, svgOrigin:"350 910", duration:1.0, repeat:12, ease:"none"}, 0);'
    'tl.to(".jet4", {x:140, opacity:0.25, duration:1.2, stagger:0.08, repeat:6, ease:"none"}, 0.2);'
    'tl.to(".sound4", {opacity:0.15, duration:0.4, yoyo:true, repeat:10, stagger:0.1}, 0.3);',
    'tl.to(".glow5", {opacity:0.8, duration:1.4, yoyo:true, repeat:5, ease:"sine.inOut"}, 0);'
    'tl.to(".ray5", {opacity:0.75, duration:1.0, stagger:0.08, yoyo:true, repeat:5}, 0.3);'
    'tl.fromTo(".man5", {opacity:0}, {opacity:1, duration:1.0}, 0.8);',
    'tl.fromTo(".towerG", {y:200, opacity:0}, {y:0, opacity:1, duration:1.2, ease:"power3.out"}, 0.1);'
    'tl.to(".sway6", {x:26, opacity:0.25, duration:1.6, stagger:0.1, yoyo:true, repeat:4}, 0.5);',
    'tl.fromTo(".card7", {y:80, opacity:0}, {y:0, opacity:1, duration:0.6, stagger:0.14, ease:"power2.out"}, 0.1);'
    'tl.fromTo(".bar7", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.8, stagger:0.05, ease:"power2.out"}, 0.7);',
    'tl.fromTo(".hl", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6, stagger:0.12}, 0.1);'
    'tl.fromTo(".ico", {scale:0.5, opacity:0, transformOrigin:"50% 50%"}, {scale:1, opacity:1, duration:0.6, ease:"back.out(2)"}, 0.6);',
    'tl.fromTo(".safe", {opacity:0, y:40}, {opacity:1, y:0, duration:0.6, stagger:0.35}, 0.1);',
    'tl.fromTo(".row10", {opacity:0, x:-60}, {opacity:1, x:0, duration:0.5, stagger:0.3}, 0.1);',
]


def page(sid, body, dur, bg, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{bg}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">{body}</div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    {anim}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, fn in enumerate(SCENES):
        sid = f"s{i+1}"
        st, dur = BOUNDS[i]
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur, BGS[i], ANIM[i]), encoding="utf-8")
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
    print("ok", TOTAL, BOUNDS)


if __name__ == "__main__":
    build()
