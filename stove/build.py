#!/usr/bin/env python3
"""«Как строят печь» — 9 сцен, тёплая инфографика."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/stove")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
N = len(STARTS)
B = []
for i in range(N):
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#fdf2df"
INK = "#3d2b1f"
BRICK = "#c0522f"
BRICK2 = "#cf6640"
BRICK3 = "#a94326"
MORTAR = "#eadfc8"
ACC = "#2f5f8f"
GREEN = "#4f8f4a"
RED = "#c0392b"
CREAM = "#fffaf0"

rnd = random.Random(7)


def S(d, w=5, col=INK, cls="draw", extra=""):
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" '
            f'stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, cls="fillshape", stroke=INK, sw=5, op=1.0):
    return f'<path class="{cls}" d="{d}" fill="{col}" opacity="{op}" stroke="{stroke}" stroke-width="{sw}"/>'


def txt(x, y, s, size=44, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="900" '
            f'fill="{col}" text-anchor="{anchor}">{s}</text>')


def grain(seed, n=90):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(0.6,1.6):.1f}" '
                   f'fill="#a08060" opacity="{r.uniform(0.03,0.07):.2f}"/>' for _ in range(n))


def brick(x, y, w=150, h=52, col=BRICK, cls="brk"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{col}" '
            f'stroke="{INK}" stroke-width="3.5"/>'
            f'<path d="M {x+6} {y+8} l {w-24} 0" stroke="#ffffff" stroke-width="2" opacity="0.18"/></g>')


def row(y, n=4, x0=250, w=150, h=52, offset=0, cols=None, cls="brkrow"):
    out = []
    for i in range(n):
        x = x0 + i * w + offset
        col = (cols or [BRICK, BRICK2, BRICK, BRICK3])[i % 4]
        out.append(brick(x, y, w, h, col, cls))
    return "".join(out)


def stove(rows=10, x0=290, w=125, h=56, y0=1560, cls="stoveG"):
    """Печь: столбы по бокам, топка между, перевязка."""
    b = [f'<g class="{cls}">']
    for r in range(rows):
        y = y0 - r * (h + 4)
        if 2 <= r <= 5:
            idx = [0, 3]
        else:
            idx = [0, 1, 2, 3]
        for i in idx:
            col = [BRICK, BRICK2, BRICK, BRICK3][(i + r) % 4]
            b.append(brick(x0 + i * w, y, w, h, col, f"br{r}_{i}"))
    b.append('</g>')
    return "".join(b)


def chimney(x=470, y_top=760, y_bottom=1020, w=150):
    return (f'<g class="chimney"><rect x="{x}" y="{y_top}" width="{w}" height="{y_bottom-y_top}" fill="{BRICK2}" '
            f'stroke="{INK}" stroke-width="5"/>'
            + "".join(f'<path d="M {x} {y_top+i*54} l {w} 0" stroke="{MORTAR}" stroke-width="6"/>' for i in range(1, 5))
            + f'<rect x="{x-14}" y="{y_top-16}" width="{w+28}" height="24" rx="4" fill="#8a8a8a" stroke="{INK}" stroke-width="4"/></g>')


def firebox(x, y, w=260, h=190):
    return (f'<g class="firebox"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#2a1a12" stroke="{INK}" stroke-width="5"/>'
            f'<path d="M {x+40} {y+h-20} q 30 -70 60 -20 q 20 -50 50 -10 q 20 -40 60 30 z" fill="#e8892e"/>'
            f'<path d="M {x+80} {y+h-20} q 20 -50 40 -8 q 16 -34 44 8 z" fill="#f4c25a"/>'
            f'<rect x="{x-10}" y="{y-14}" width="{w+20}" height="20" rx="6" fill="#6b6b6b" stroke="{INK}" stroke-width="4"/></g>')


def badge_num(n, x=90, y=200, col=ACC):
    return (f'<g class="numG"><circle cx="{x}" cy="{y}" r="52" fill="{col}" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{x}" y="{y+18}" font-family="Nunito" font-size="52" font-weight="900" fill="#ffffff" text-anchor="middle">{n}</text></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(1)]
    b.append(stove(10))
    b.append(chimney())
    b.append(firebox(420, 1258, 240, 182))
    # дым
    for i in range(4):
        b.append(f'<path class="smoke" d="M 545 {730 - i*60} q 24 -40 0 -70 q -20 -30 0 -60" stroke="#b9b0a4" '
                 f'stroke-width="10" fill="none" opacity="0.7"/>')
    b.append(txt(60, 200, "КАК СТРОЯТ", 62))
    b.append(txt(60, 272, "ПЕЧЬ", 62, BRICK3))
    b.append(txt(60, 340, "шесть шагов мастера", 28, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(2)]
    b.append(badge_num(1))
    b.append(f'<rect x="120" y="360" width="840" height="760" rx="16" fill="{CREAM}" stroke="{INK}" stroke-width="5"/>')
    # чертёж печи
    b.append(S("M 330 980 L 330 640 L 750 640 L 750 980 Z", 4, "#8a6a4a"))
    b.append(S("M 330 780 L 750 780 M 330 860 L 750 860", 3, "#b09070"))
    b.append(S("M 480 640 L 480 520 L 560 520 L 560 640", 4, "#8a6a4a"))
    b.append(f'<rect x="380" y="820" width="120" height="80" rx="6" fill="none" stroke="#8a6a4a" stroke-width="4"/>')
    # размеры
    b.append(S("M 300 640 L 300 980 M 280 640 L 320 640 M 280 980 L 320 980", 3, ACC))
    b.append(txt(240, 830, "высота", 24, ACC, "end"))
    b.append(S("M 330 1010 L 750 1010 M 330 990 L 330 1030 M 750 990 L 750 1030", 3, ACC))
    b.append(txt(540, 1060, "ширина", 24, ACC, "middle"))
    # карандаш и линейка
    b.append(f'<g class="pencil"><rect x="760" y="1040" width="150" height="22" rx="6" fill="#e8b23a" stroke="{INK}" stroke-width="3" transform="rotate(-18 835 1051)"/>'
             f'<path d="M 910 1040 l 26 11 l -26 11 z" fill="#e8dcc4" stroke="{INK}" stroke-width="3" transform="rotate(-18 835 1051)"/></g>')
    b.append(f'<rect x="150" y="1150" width="420" height="26" rx="4" fill="#e8c98a" stroke="{INK}" stroke-width="3"/>')
    for i in range(10):
        b.append(f'<path d="M {170+i*40} 1150 l 0 12" stroke="{INK}" stroke-width="2"/>')
    b.append(txt(60, 180, "ШАГ 1 · ПРОЕКТ", 46))
    b.append(txt(60, 1260, "размер · место · путь дыма", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(3)]
    b.append(badge_num(2))
    # штабель кирпичей
    for r in range(4):
        b.append(row(1240 - r * 56, n=3, x0=180, w=160, h=52, offset=0 if r % 2 == 0 else -40, cls=f"pile{r}"))
    # ведро с раствором
    b.append(f'<g class="bucket"><path d="M 680 1080 l 180 0 l -22 170 l -136 0 z" fill="#8b9499" stroke="{INK}" stroke-width="5"/>'
             f'<ellipse cx="770" cy="1080" rx="90" ry="20" fill="#cfc3a8" stroke="{INK}" stroke-width="4"/></g>')
    # дверца и колосник
    b.append(f'<g class="door"><rect x="700" y="800" width="150" height="170" rx="8" fill="#4a4a4a" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="775" cy="885" r="14" fill="#c9a34a" stroke="{INK}" stroke-width="3"/></g>')
    b.append(f'<g class="grate"><rect x="240" y="880" width="170" height="90" rx="6" fill="#6b6b6b" stroke="{INK}" stroke-width="4"/>'
             + "".join(f'<path d="M {260+i*26} 890 l 0 70" stroke="{INK}" stroke-width="5"/>' for i in range(6)) + '</g>')
    b.append(txt(60, 180, "ШАГ 2 · МАТЕРИАЛЫ", 42))
    b.append(txt(60, 700, "кирпич · раствор · дверцы", 26, "#7a5a3a"))
    b.append(txt(60, 1560, "КОЛОСНИК · ЗАСЛОНКА · УГОЛОК", 24, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(4)]
    b.append(badge_num(3, col=BRICK3))
    b.append(f'<rect x="180" y="1560" width="720" height="120" fill="#cfc3a8" stroke="{INK}" stroke-width="4"/>')
    b.append(row(1500, n=4, x0=240, w=150, h=52, cls="firstRow"))
    # уровень
    b.append(f'<g class="level"><rect x="200" y="1400" width="560" height="46" rx="8" fill="#e8b23a" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="440" y="1408" width="120" height="30" rx="6" fill="#eaf6ff" stroke="{INK}" stroke-width="3"/>'
             f'<circle class="bubble" cx="500" cy="1423" r="12" fill="#4f9f4a"/></g>')
    b.append(txt(60, 180, "ШАГ 3 · ПЕРВЫЙ РЯД", 42))
    b.append(txt(60, 980, "по уровню, кирпич за кирпичом", 26, "#7a5a3a"))
    b.append(txt(60, 1560, "ПРОВЕРЯТЬ КАЖДЫЙ РЯД", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(5)]
    b.append(badge_num(4, col="#8a5a9a"))
    b.append(f'<rect x="180" y="1560" width="720" height="120" fill="#cfc3a8" stroke="{INK}" stroke-width="4"/>')
    b.append(stove(10, cls="grow"))
    b.append(firebox(420, 1258, 240, 182))
    b.append(txt(60, 180, "ШАГ 4 · СТЕНКИ", 42))
    b.append(txt(60, 800, "ряд за рядом, с перевязкой", 26, "#7a5a3a"))
    b.append(txt(60, 1560, "ШОВ 3–5 ММ, ГЛИНА С ПЕСКОМ", 24, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(6)]
    b.append(badge_num(5, col=ACC))
    b.append(stove(10))
    b.append(firebox(420, 1258, 240, 182))
    # дымоход
    b.append(f'<g class="chimney"><rect x="470" y="520" width="160" height="300" fill="{BRICK2}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 470 600 l 160 0 M 470 680 l 160 0 M 470 760 l 160 0" stroke="{MORTAR}" stroke-width="6"/></g>')
    # путь дыма
    b.append(f'<path class="smokepath" d="M 440 1000 q 120 40 120 -90 q 0 -140 60 -120" stroke="{RED}" stroke-width="9" '
             f'fill="none" stroke-dasharray="16 12" opacity="0.85"/>')
    b.append(txt(60, 180, "ШАГ 5 · ДЫМОХОД", 42))
    b.append(txt(700, 560, "путь дыма", 26, RED))
    b.append(txt(60, 1560, "ТЯГА ЗАВИСИТ ОТ СЕЧЕНИЯ КАНАЛА", 24, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(7)]
    b.append(badge_num(6, col=GREEN))
    b.append(stove(10))
    b.append(firebox(420, 1258, 240, 182))
    b.append(f'<rect x="470" y="520" width="160" height="300" fill="{BRICK2}" stroke="{INK}" stroke-width="5"/>')
    # лупа
    b.append(f'<g class="lens"><circle cx="700" cy="900" r="86" fill="#eaf6ff" opacity="0.7" stroke="{INK}" stroke-width="8"/>'
             f'<path d="M 760 960 L 830 1030" stroke="{INK}" stroke-width="18" stroke-linecap="round"/></g>')
    b.append(f'<path class="smoke" d="M 550 500 q 20 -40 0 -70 q -18 -30 0 -60" stroke="#b9b0a4" stroke-width="9" fill="none" opacity="0.8"/>')
    b.append(txt(60, 180, "ШАГ 6 · ПРОВЕРКА", 42))
    b.append(txt(60, 1560, "ТЯГА · ТРЕЩИНЫ · ПРОГРЕВ", 26, "#7a5a3a"))
    return b


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', grain(8)]
    b.append(stove(10))
    b.append(chimney())
    b.append(firebox(420, 1258, 240, 182))
    b.append(f'<g class="clock"><circle cx="840" cy="320" r="110" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
             f'<path d="M 840 320 L 840 240 M 840 320 L 900 350" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
             f'<circle cx="840" cy="320" r="10" fill="{INK}"/></g>')
    b.append(txt(60, 200, "НЕ СПЕШИТЬ", 52))
    b.append(txt(60, 268, "печь не любит спешки", 26, "#7a5a3a"))
    b.append(txt(60, 1640, "КАЖДЫЙ РЯД — ПРОВЕРКА", 26, BRICK3))
    return b


# ---------------------------------------------------------------- s9
def s9():
    b = [f'<rect width="1080" height="1920" fill="#fdecea"/>', grain(9)]
    b.append(f'<path d="M 540 380 l 250 430 l -500 0 z" fill="#f4c25a" stroke="{INK}" stroke-width="8"/>')
    b.append(f'<text x="540" y="740" font-family="Nunito" font-size="120" font-weight="900" fill="{INK}" text-anchor="middle">!</text>')
    b.append(txt(540, 940, "ТОЛЬКО СПЕЦИАЛИСТ", 44, "#8a2a1e", "middle"))
    b.append(txt(100, 1060, "Кладка и ремонт печи —", 32, INK))
    b.append(txt(100, 1110, "работа взрослых профессионалов.", 32, INK))
    b.append(txt(100, 1210, "Огонь, тяга и угарный газ", 28, "#8a2a1e"))
    b.append(txt(100, 1260, "не прощают ошибок.", 28, "#8a2a1e"))
    b.append(f'<rect x="100" y="1400" width="880" height="120" rx="16" fill="{CREAM}" stroke="{INK}" stroke-width="4"/>')
    b.append(txt(540, 1475, "ХОРОШАЯ ПЕЧЬ = ТОЧНЫЙ РАСЧЁТ + АККУРАТНОСТЬ", 26, INK, "middle"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
ANIM = [
    'tl.fromTo(".stoveG", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.to(".smoke", {y:-40, opacity:0.2, duration:2.0, stagger:0.3, yoyo:true, repeat:3}, 0.4);'
    'tl.fromTo(".firebox", {opacity:0}, {opacity:1, duration:0.6}, 0.6);',
    'tl.fromTo(".numG", {scale:0, transformOrigin:"50% 50%"}, {scale:1, duration:0.4, ease:"back.out(3)"}, 0.1);'
    'tl.to(".draw", {attr:{"stroke-dashoffset":0}, duration:1.2, stagger:0.25}, 0.3);'
    'tl.fromTo(".pencil", {opacity:0, x:40}, {opacity:1, x:0, duration:0.5}, 1.2);',
    'tl.fromTo(".pile0, .pile1, .pile2, .pile3", {opacity:0, y:-20}, {opacity:1, y:0, duration:0.4, stagger:0.15}, 0.2);'
    'tl.fromTo(".bucket", {opacity:0, x:40}, {opacity:1, x:0, duration:0.5}, 0.9);'
    'tl.fromTo(".door, .grate", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.2}, 1.1);',
    'tl.fromTo(".firstRow", {opacity:0, y:-30}, {opacity:1, y:0, duration:0.6, stagger:0.12}, 0.2);'
    'tl.fromTo(".level", {opacity:0, y:-40}, {opacity:1, y:0, duration:0.6}, 0.7);'
    'tl.to(".bubble", {x:-24, duration:0.8, yoyo:true, repeat:3, ease:"sine.inOut"}, 1.2);',
    'tl.fromTo(".br0, .br1, .br2, .br3, .br4, .br5, .br6, .br7, .br8", {opacity:0, y:20}, '
    '{opacity:1, y:0, duration:0.35, stagger:0.14}, 0.2);'
    'tl.fromTo(".firebox", {opacity:0}, {opacity:1, duration:0.5}, 1.2);',
    'tl.fromTo(".chimney", {scaleY:0, transformOrigin:"50% 100%"}, {scaleY:1, duration:0.9, ease:"power2.out"}, 0.3);'
    'tl.to(".smokepath", {strokeDashoffset:0, duration:1.4, repeat:3, ease:"none"}, 0.9);'
    'tl.fromTo(".firebox", {opacity:0}, {opacity:1, duration:0.5}, 1.0);',
    'tl.fromTo(".lens", {opacity:0, scale:0.6, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.6}, 0.4);'
    'tl.to(".lens", {x:40, y:40, duration:1.2, yoyo:true, repeat:2, ease:"sine.inOut"}, 1.0);'
    'tl.to(".smoke", {y:-30, opacity:0.2, duration:1.4, yoyo:true, repeat:3}, 0.3);',
    'tl.fromTo(".clock", {opacity:0, rotate:-20}, {opacity:1, rotate:0, duration:0.7, transformOrigin:"840px 320px"}, 0.2);'
    'tl.to(".smoke", {y:-40, opacity:0.2, duration:1.8, stagger:0.3, yoyo:true, repeat:3}, 0.5);',
    'tl.fromTo(".num", {scale:0}, {scale:1, duration:0.4}, 0);'
    'tl.fromTo("path", {opacity:0}, {opacity:1, duration:0.6}, 0.1);',
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.03, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:16 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
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
