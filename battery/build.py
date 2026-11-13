#!/usr/bin/env python3
"""«Батарея холодная» — 8 сцен, крупный текст, петля."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/battery")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#102a3d"
BG2 = "#0b1f2e"
CREAM = "#f6efe0"
HOT = "#ff6b35"
COLD = "#3fa9f5"
MUST = "#f2b134"
INK = "#0d1a24"


def t(x, y, s, size=50, col=CREAM, anchor="start", w=900, ls=0, cls="hl", stroke=None):
    st = f' stroke="{INK}" stroke-width="10" paint-order="stroke" stroke-linejoin="round"' if stroke else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}"{st}>{s}</text>')


def rad(x, y, w=520, h=420, hot_from=0.55, cls="rad", col_hot=HOT, col_cold=COLD):
    """Радиатор: секции, сверху/снизу трубы. hot_from — доля высоты, ниже которой горячо."""
    b = [f'<g class="{cls}">']
    b.append(f'<rect x="{x-20}" y="{y+h*0.12}" width="20" height="{h*0.76}" rx="8" fill="{col_cold}"/>')
    b.append(f'<rect x="{x+w}" y="{y+h*0.12}" width="20" height="{h*0.76}" rx="8" fill="{col_cold}"/>')
    n = 9
    fw = w / n
    for i in range(n):
        fx = x + i * fw + 6
        b.append(f'<rect x="{fx:.0f}" y="{y}" width="{fw-12:.0f}" height="{h}" rx="12" fill="{col_cold}"/>')
    # горячая часть — по секциям, чтобы рёбра читались
    yh = y + h * hot_from
    if hot_from < 1:
        for i in range(n):
            fx = x + i * fw + 6
            b.append(f'<rect x="{fx:.0f}" y="{yh:.0f}" width="{fw-12:.0f}" height="{max(0, h-(yh-y)):.0f}" rx="12" fill="{col_hot}"/>')
        b.append(f'<rect x="{x-20}" y="{yh:.0f}" width="20" height="{max(0, h-(yh-y)):.0f}" rx="8" fill="{col_hot}"/>')
        b.append(f'<rect x="{x+w}" y="{yh:.0f}" width="20" height="{max(0, h-(yh-y)):.0f}" rx="8" fill="{col_hot}"/>')
    b.append(f'<rect x="{x-24}" y="{y+h*0.10}" width="{w+48}" height="26" rx="13" fill="{col_hot}"/>')
    b.append('</g>')
    return "".join(b)


def ico_valve(cx, cy, r=70, col=MUST, cls="valve"):
    b = [f'<g class="{cls}">']
    for i in range(6):
        b.append(f'<rect x="{cx-10}" y="{cy-r}" width="20" height="{r*0.5}" rx="8" fill="{col}" '
                 f'transform="rotate({i*60} {cx} {cy})"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.28}" fill="{col}"/>')
    b.append('</g>')
    return "".join(b)


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="470" fill="{BG2}"/>')
    b.append(rad(180, 620, 720, 700, 0.52, "rad1"))
    b.append(t(540, 200, "БАТАРЕЯ", 92, CREAM, "middle", 900, stroke=INK))
    b.append(t(540, 300, "ХОЛОДНАЯ?", 92, HOT, "middle", 900, stroke=INK))
    b.append(t(540, 400, "сверху холодно · снизу горячо", 30, COLD, "middle", 800))
    b.append(t(540, 1480, "это не поломка", 30, MUST, "middle", 800))
    b.append(t(540, 1536, "это воздух", 40, CREAM, "middle", 900))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG2}"/>']
    b.append(f'<rect x="120" y="760" width="840" height="240" rx="120" fill="{BG}" stroke="{CREAM}" stroke-width="8" opacity="0.9"/>')
    # вода с двух сторон
    b.append(f'<rect x="130" y="772" width="250" height="216" rx="108" fill="{COLD}" opacity="0.85"/>')
    b.append(f'<rect x="700" y="772" width="250" height="216" rx="108" fill="{COLD}" opacity="0.85"/>')
    # пробка
    b.append('<g class="bubble2">')
    b.append(f'<circle cx="520" cy="880" r="92" fill="{CREAM}" opacity="0.95"/>')
    b.append(f'<circle cx="488" cy="850" r="26" fill="{BG2}" opacity="0.15"/>')
    b.append(t(520, 900, "ВОЗДУХ", 34, INK, "middle", 900))
    b.append('</g>')
    b.append(t(540, 220, "ВОЗДУШНАЯ", 84, CREAM, "middle", 900))
    b.append(t(540, 310, "ПРОБКА", 84, HOT, "middle", 900))
    b.append(t(540, 390, "вода не проходит по кругу", 28, COLD, "middle", 800))
    b.append(t(540, 1300, "кружок воды остановился", 30, CREAM, "middle", 700))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(rad(240, 780, 560, 620, 0.5, "rad3", HOT, COLD))
    # кран Маевского на верхней трубе
    b.append(f'<rect x="800" y="822" width="96" height="44" rx="10" fill="{MUST}"/>')
    b.append(f'<g class="knob3"><circle cx="878" cy="800" r="34" fill="{MUST}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M 878 776 l 0 48 M 854 800 l 48 0" stroke="{INK}" stroke-width="7"/>'
             f'<circle cx="878" cy="800" r="8" fill="{INK}"/></g>')
    # струйки воздуха
    for i, (dx, dy) in enumerate(((0, -40), (26, -70), (-22, -72))):
        b.append(f'<circle class="puff{i}" cx="{880+dx}" cy="{740+dy}" r="{10+i*4}" fill="{CREAM}" opacity="0.7"/>')
    b.append(t(540, 220, "КРАН", 84, CREAM, "middle", 900))
    b.append(t(540, 310, "МАЕВСКОГО", 84, MUST, "middle", 900))
    b.append(t(540, 390, "спусти воздух — вода пойдёт", 28, COLD, "middle", 800))
    b.append(t(540, 1620, "ключ или отвёртка", 30, CREAM, "middle", 700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG2}"/>']
    b.append(f'<circle cx="540" cy="960" r="300" fill="{BG}" stroke="{CREAM}" stroke-width="10"/>')
    for i in range(11):
        a = -210 + i * 24
        b.append(f'<rect x="532" y="700" width="16" height="40" rx="6" fill="{CREAM}" transform="rotate({a} 540 960)"/>')
    b.append(f'<g class="needle"><rect x="532" y="790" width="16" height="190" rx="8" fill="{HOT}" transform="rotate(-58 540 960)"/></g>')
    b.append(f'<circle cx="540" cy="960" r="26" fill="{CREAM}"/>')
    b.append(f'<rect x="360" y="1080" width="360" height="26" rx="13" fill="{COLD}" opacity="0.5"/>')
    b.append(t(540, 220, "ДАВЛЕНИЕ", 84, CREAM, "middle", 900))
    b.append(t(540, 310, "НИЖЕ НОРМЫ", 84, HOT, "middle", 900))
    b.append(t(540, 390, "насос не продавит дальние радиаторы", 24, COLD, "middle", 800))
    b.append(t(540, 1500, "норма — полторы атмосферы", 32, MUST, "middle", 800))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # труба обратки и закрытый кран
    b.append(f'<rect x="0" y="1200" width="1080" height="70" fill="{COLD}" opacity="0.55"/>')
    b.append(f'<rect x="380" y="1140" width="80" height="190" fill="{MUST}"/>')
    b.append(ico_valve(420, 1140, 74, HOT, "knob5"))
    b.append(f'<path class="x5" d="M 340 1030 l 160 0 M 420 950 l 0 160" stroke="{HOT}" stroke-width="16" stroke-linecap="round"/>')
    b.append(t(540, 220, "КРАН", 84, CREAM, "middle", 900))
    b.append(t(540, 310, "НА ОБРАТКЕ", 84, MUST, "middle", 900))
    b.append(t(540, 390, "летом закрыли — и забыли открыть", 26, COLD, "middle", 800))
    b.append(t(540, 1560, "вода не возвращается в котёл", 30, CREAM, "middle", 700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG2}"/>']
    b.append(rad(80, 760, 380, 420, 0.95, "r6a", HOT, HOT))
    b.append(rad(600, 760, 380, 420, 0.95, "r6b", COLD, COLD))
    b.append(t(270, 720, "БЛИЖНИЙ", 32, HOT, "middle", 900))
    b.append(t(790, 720, "ДАЛЬНИЙ", 32, COLD, "middle", 900))
    b.append(f'<path d="M 470 940 L 590 940" stroke="{CREAM}" stroke-width="10" stroke-dasharray="18 14"/>')
    b.append(t(540, 220, "БАЛАНСИРОВКА", 68, CREAM, "middle", 900))
    b.append(t(540, 300, "весь поток ушёл в одну комнату", 26, COLD, "middle", 800))
    b.append(t(540, 1420, "прикрой ближние вентили", 34, MUST, "middle", 800))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(rad(300, 700, 480, 520, 0.6, "r7", "#7a4a2a", COLD))
    b.append(f'<g class="dirt">')
    b.append(f'<path d="M 520 1220 q -10 120 20 200 l 60 0 q 30 -90 20 -200 z" fill="#6b4a2a" opacity="0.9"/>')
    b.append(f'<ellipse cx="560" cy="1440" rx="90" ry="24" fill="#6b4a2a" opacity="0.5"/>')
    b.append('</g>')
    b.append(t(540, 220, "НИЗ ХОЛОДНЫЙ", 72, CREAM, "middle", 900))
    b.append(t(540, 300, "ГОДАМИ?", 72, HOT, "middle", 900))
    b.append(t(540, 380, "внутри ил и накипь", 30, COLD, "middle", 800))
    b.append(t(540, 1620, "нужна промывка системы", 34, MUST, "middle", 800))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG2}"/>']
    b.append(f'<circle cx="540" cy="980" r="380" fill="{HOT}" opacity="0.12"/>')
    b.append(rad(230, 700, 620, 620, 0.0, "r8", HOT, HOT))
    b.append(f'<path class="heat" d="M 300 660 q 30 -50 60 0 M 420 640 q 30 -50 60 0 M 540 660 q 30 -50 60 0" stroke="{MUST}" stroke-width="8" fill="none" opacity="0.8"/>')
    b.append(t(540, 240, "ПЯТЬ МИНУТ", 84, CREAM, "middle", 900))
    b.append(t(540, 330, "И ОНА ГОРЯЧАЯ", 84, HOT, "middle", 900))
    b.append(t(540, 1640, "а если снова холодная — начни сначала", 26, COLD, "middle", 800))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".rad1", {opacity:0, y:30}, {opacity:1, y:0, duration:0.6}, 0.05);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.35, stagger:0.08}, 0);',
    'tl.fromTo(".bubble2", {opacity:0, x:-160}, {opacity:1, x:0, duration:0.7, ease:"back.out(1.5)"}, 0.1);'
    'tl.to(".bubble2", {x:-14, duration:0.9, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".knob3", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}, 0.1);'
    'tl.to(".knob3", {rotate:-40, duration:0.7, ease:"power2.out"}, 0.4);'
    'tl.fromTo(".puff0, .puff1, .puff2", {opacity:0, y:20}, {opacity:0.8, y:-40, duration:0.9, stagger:0.15}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".needle", {opacity:0}, {opacity:1, duration:0.5}, 0.3);'
    'tl.to(".needle", {opacity:0.55, duration:0.7, yoyo:true, repeat:2}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".knob5", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}, 0.1);'
    'tl.fromTo(".x5", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.4}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".r6a", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.6}, 0.1);'
    'tl.fromTo(".r6b", {opacity:0, x:30}, {opacity:1, x:0, duration:0.6}, 0.3);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".r7", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".dirt", {opacity:0}, {opacity:1, duration:0.5}, 0.7);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0);',
    'tl.fromTo(".r8", {opacity:0, scale:0.95}, {opacity:1, scale:1, duration:0.7}, 0.05);'
    'tl.to(".heat", {y:-14, duration:1.1, stagger:0.15, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.4);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.4, stagger:0.12}, 0);',
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
