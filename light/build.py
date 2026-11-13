#!/usr/bin/env python3
"""«Разводка освещения» — 9 сцен, электрическая палитра."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/light")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(9):
    end = STARTS[i + 1] if i + 1 < 9 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#0c1116"
INK = "#f2f6f8"
YEL = "#ffd60a"
COPPER = "#c07a3a"
BLUE = "#4da3ff"
RED = "#e03e2f"
GREY = "#8fa3b1"
DARK = "#151d24"

DEFS = """<defs>
<linearGradient id="cableG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3a3f45"/><stop offset="1" stop-color="#23282d"/></linearGradient>
<radialGradient id="bulbG"><stop offset="0" stop-color="#fff3b0" stop-opacity="0.95"/><stop offset="1" stop-color="#ffd60a" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def txt(x, y, s, size=58, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="900" fill="{col}" text-anchor="{anchor}" letter-spacing="-1">{s}</text>')


def wire(x1, y1, x2, y2, col=YEL, w=8, cls="wire", dash=False):
    extra = f' stroke-dasharray="2000" stroke-dashoffset="2000"' if dash else ""
    return (f'<path class="{cls}" d="M {x1} {y1} L {x2} {y2}" stroke="{col}" stroke-width="{w}" '
            f'fill="none" stroke-linecap="round"{extra}/>')


def lamp(x, y, s=1.0, on=True, cls="lamp"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<path d="M -60 -40 q 30 -70 60 -70 q 30 0 60 70 z" fill="{GREY if not on else "#3d4a52"}"/>'
            f'<rect x="-8" y="-118" width="16" height="20" fill="{GREY}"/>'
            f'<circle class="bulbGlow" cx="0" cy="0" r="150" fill="url(#bulbG)" opacity="{0.9 if on else 0.15}"/>'
            f'<ellipse cx="0" cy="-4" rx="52" ry="14" fill="{YEL if on else "#5a656d"}" opacity="{0.95 if on else 0.6}"/></g>')


def switch(x, y, s=1.0, on=False, cls="switchG", double=False):
    keys = 1 if not double else 2
    body = f'<rect x="-46" y="-70" width="92" height="140" rx="14" fill="#e8eef2" stroke="{GREY}" stroke-width="4"/>'
    for k in range(keys):
        ky = -52 + k * 52
        body += (f'<rect class="key" x="-32" y="{ky}" width="64" height="44" rx="8" fill="{"#d7dee3" if not on else YEL}"/>')
    return f'<g class="{cls}" transform="translate({x} {y}) scale({s})">{body}</g>'


def breaker(x, y, s=1.0, on=True, cls="brk"):
    return (f'<g class="{cls}" transform="translate({x} {y}) scale({s})">'
            f'<rect x="-70" y="-100" width="140" height="200" rx="12" fill="#dfe6ea" stroke="{GREY}" stroke-width="4"/>'
            f'<rect class="lever" x="-26" y="{-30 if on else 20}" width="52" height="70" rx="8" fill="{YEL if on else GREY}"/>'
            f'<text x="0" y="-66" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="#2a333a" text-anchor="middle">{cls[-1] if cls[-1].isdigit() else "10"}</text></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="#0a0f14"/>')
    b.append(lamp(540, 520, 2.0, True, "lamp1"))
    b.append(f'<path d="M 540 420 l 0 -160" stroke="{GREY}" stroke-width="6"/>')
    b.append(breaker(860, 1250, 1.4, True, "brk1"))
    b.append(f'<path class="spark1" d="M 800 1360 l 40 40 M 840 1360 l -40 40" stroke="{RED}" stroke-width="8" opacity="0.9"/>')
    b.append(txt(60, 1700, "СВЕТ МИГАЕТ?", 62, INK))
    b.append(txt(60, 1780, "ошибка может быть в щитке", 32, YEL))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(breaker(140, 700, 1.1, True, "brk2"))
    b.append(wire(210, 700, 420, 700, YEL, 9, "w2a"))
    b.append(switch(470, 700, 1.3, True, "sw2"))
    b.append(wire(510, 700, 760, 700, YEL, 9, "w2b"))
    b.append(wire(820, 700, 820, 980, YEL, 9, "w2c"))
    b.append(lamp(820, 1060, 1.9, True, "lamp2"))
    b.append(wire(820, 1080, 820, 1330, BLUE, 8, "w2d"))
    b.append(wire(820, 1330, 210, 1330, BLUE, 8, "w2e"))
    b.append(wire(210, 1330, 210, 760, BLUE, 8, "w2f"))
    for i in range(6):
        b.append(f'<circle class="cur2" cx="{240 + i*80}" cy="700" r="7" fill="{YEL}"/>')
    b.append(txt(60, 200, "СХЕМА", 64, INK))
    b.append(txt(60, 1640, "щиток → автомат → кабель → выключатель → лампа", 28, GREY))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(txt(60, 190, "ВЫКЛЮЧАТЕЛЬ — НА ФАЗУ", 44, INK))
    # правильно
    b.append(f'<rect x="60" y="330" width="460" height="560" rx="18" fill="{DARK}"/>')
    b.append(wire(110, 620, 230, 620, RED, 9, "w3a"))
    b.append(switch(290, 640, 1.05, False, "sw3a"))
    b.append(wire(320, 620, 460, 620, YEL, 9, "w3b"))
    b.append(lamp(410, 800, 1.2, False, "lamp3a"))
    b.append(txt(290, 960, "ФАЗА", 40, YEL, "middle"))
    b.append(txt(290, 1000, "правильно", 28, "#4ad07a", "middle"))
    # неправильно
    b.append(f'<rect x="560" y="330" width="460" height="560" rx="18" fill="{DARK}"/>')
    b.append(wire(610, 620, 730, 620, YEL, 9, "w3c"))
    b.append(switch(790, 640, 1.05, True, "sw3b"))
    b.append(wire(820, 620, 960, 620, RED, 9, "w3d"))
    b.append(lamp(910, 800, 1.2, False, "lamp3b"))
    b.append(f'<path class="danger3" d="M 640 760 l 0 -60" stroke="{RED}" stroke-width="10"/>')
    b.append(txt(790, 960, "НОЛЬ", 40, RED, "middle"))
    b.append(txt(790, 1000, "провод под напряжением", 24, RED, "middle"))
    b.append(txt(60, 1240, "лампа не горит, но она под током", 30, GREY))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(txt(60, 220, "СЕЧЕНИЕ И АВТОМАТ", 52, INK))
    rows = [("1,5 мм²", "10 А", "до 2 кВт"), ("2,5 мм²", "16 А", "до 3,5 кВт")]
    for i, (s1_, s2_, s3_) in enumerate(rows):
        y = 460 + i * 300
        b.append(f'<g class="row4"><rect x="70" y="{y}" width="940" height="240" rx="18" fill="{DARK}"/>'
                 f'<text x="120" y="{y+90}" font-family="Nunito, Arial" font-size="56" font-weight="900" fill="{YEL}">{s1_}</text>'
                 f'<text x="120" y="{y+160}" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">кабель</text>'
                 f'<text x="560" y="{y+90}" font-family="Nunito, Arial" font-size="56" font-weight="900" fill="{INK}">{s2_}</text>'
                 f'<text x="560" y="{y+160}" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{GREY}">автомат</text>'
                 f'<text x="900" y="{y+130}" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="{YEL}" text-anchor="end">{s3_}</text></g>')
    b.append(txt(60, 1500, "освещение — отдельная группа", 30, GREY))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(switch(230, 760, 1.6, True, "sw5", double=True))
    b.append(wire(300, 660, 620, 520, YEL, 8, "w5a"))
    b.append(wire(300, 740, 620, 700, YEL, 8, "w5b"))
    b.append(lamp(700, 470, 1.5, True, "lamp5a"))
    b.append(lamp(820, 760, 1.5, True, "lamp5b"))
    for i in range(5):
        b.append(f'<circle class="cur5" cx="{340 + i*60}" cy="660" r="7" fill="{YEL}"/>')
    b.append(txt(60, 220, "ДВЕ ГРУППЫ", 60, INK))
    b.append(txt(60, 300, "две клавиши — два провода", 30, GREY))
    b.append(txt(60, 1500, "люстра: 1-я и 2-я группа ламп", 30, GREY))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="60" y="420" width="960" height="160" fill="{DARK}"/>')
    b.append(switch(210, 500, 1.2, False, "sw6a"))
    b.append(switch(860, 500, 1.2, True, "sw6b"))
    b.append(wire(240, 500, 480, 500, YEL, 6, "w6a"))
    b.append(wire(480, 500, 840, 500, YEL, 6, "w6b"))
    b.append(wire(480, 470, 480, 500, BLUE, 6, "w6c"))
    b.append(txt(60, 300, "ПРОХОДНЫЕ ВЫКЛЮЧАТЕЛИ", 40, INK))
    b.append(txt(60, 760, "включил у входа — выключил у двери", 30, GREY))
    b.append(txt(60, 1300, "коридор · лестница · спальня", 44, YEL))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(txt(60, 220, "СОЕДИНЕНИЯ", 60, INK))
    # клеммы — правильно
    b.append(f'<rect x="80" y="420" width="420" height="300" rx="18" fill="{DARK}"/>')
    b.append(f'<rect x="140" y="520" width="300" height="90" rx="10" fill="#e8eef2"/>')
    for i in range(3):
        b.append(f'<circle cx="{180 + i*90}" cy="565" r="22" fill="{GREY}"/><circle cx="{180 + i*90}" cy="565" r="10" fill="#1c242a"/>')
    b.append(txt(290, 700, "КЛЕММЫ", 32, "#4ad07a", "middle"))
    # скрутка — нельзя
    b.append(f'<rect x="580" y="420" width="420" height="300" rx="18" fill="{DARK}"/>')
    b.append(f'<path class="twist" d="M 640 560 q 60 -40 120 0 q 60 40 120 0" stroke="{COPPER}" stroke-width="12" fill="none"/>')
    b.append(f'<path d="M 660 540 l 40 60 M 720 540 l 40 60" stroke="{RED}" stroke-width="6"/>')
    b.append(txt(790, 700, "СКРУТКА", 32, RED, "middle"))
    b.append(txt(60, 900, "медь + алюминий = нагрев", 34, YEL))
    b.append(txt(60, 960, "и пожар", 34, RED))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="#0a1a22"/>')
    b.append(lamp(540, 620, 1.8, True, "lamp8"))
    for i in range(8):
        b.append(f'<path class="drop8" d="M {380 + i*40} 760 l 0 30" stroke="#7fd0f2" stroke-width="6" opacity="0.6"/>')
    b.append(txt(60, 1300, "ВАННАЯ", 60, INK))
    b.append(txt(60, 1370, "влагозащищённый светильник", 30, "#9fd8ee"))
    b.append(txt(60, 1440, "УЗО 30 мА", 44, YEL))
    b.append(txt(60, 1520, "IP44 и выше", 30, GREY))
    return svg("".join(b))


# ---------------------------------------------------------------- s9
def s9():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(txt(540, 240, "ПРОВЕРЬ", 60, INK, "middle"))
    items = ["фаза на выключателе", "автомат 10 А", "кабель 1,5 мм²", "клеммы, не скрутки", "УЗО и IP в ванной"]
    for i, s_ in enumerate(items):
        y = 470 + i * 220
        b.append(f'<g class="row9"><circle cx="140" cy="{y}" r="40" fill="{YEL}"/>'
                 f'<text x="140" y="{y+14}" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#1a1a1a" text-anchor="middle">{i+1}</text>'
                 f'<text x="220" y="{y+12}" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="{INK}">{s_}</text></g>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
BGS = [BG, BG, BG, BG, BG, BG, BG, "#0a1a22", BG]
ANIM = [
    'tl.to(".lamp1 .bulbGlow", {opacity:0.25, duration:0.18, yoyo:true, repeat:14}, 0);'
    'tl.to(".spark1", {opacity:0.2, duration:0.15, yoyo:true, repeat:12}, 0.2);'
    'tl.to(".brk1 .lever", {fill:"#ff8a7a", duration:0.4, yoyo:true, repeat:6}, 0);',

    'tl.to(".wire", {strokeDashoffset:0, duration:1.2, stagger:0.25, ease:"power2.out"}, 0.1);'
    'tl.to(".cur2", {x:400, duration:1.6, stagger:0.08, repeat:6, ease:"none"}, 0.4);'
    'tl.to(".lamp2 .bulbGlow", {opacity:0.5, duration:0.9, yoyo:true, repeat:4}, 0.6);',

    'tl.to(".wire", {strokeDashoffset:0, duration:0.9, stagger:0.15}, 0.1);'
    'tl.to(".sw3b .key", {fill:"#ff8a7a", duration:0.5, yoyo:true, repeat:5}, 0.6);'
    'tl.to(".danger3", {opacity:0.3, duration:0.4, yoyo:true, repeat:8}, 0.5);',

    'tl.fromTo(".row4", {opacity:0, x:-50}, {opacity:1, x:0, duration:0.5, stagger:0.25}, 0.1);',

    'tl.to(".cur5", {x:280, duration:1.4, stagger:0.1, repeat:6, ease:"none"}, 0.3);'
    'tl.to(".lamp5a .bulbGlow, .lamp5b .bulbGlow", {opacity:0.45, duration:0.8, yoyo:true, repeat:4}, 0.4);',

    'tl.fromTo(".sw6b .key", {fill:"#d7dee3"}, {fill:"#ffd60a", duration:0.5}, 0.5);'
    'tl.fromTo(".sw6a .key", {fill:"#d7dee3"}, {fill:"#ffd60a", duration:0.5}, 1.2);',

    'tl.to(".twist", {opacity:0.4, duration:0.5, yoyo:true, repeat:6}, 0.3);',

    'tl.to(".drop8", {y:120, opacity:0, duration:1.4, stagger:0.1, repeat:3, ease:"power1.in"}, 0.2);'
    'tl.to(".lamp8 .bulbGlow", {opacity:0.5, duration:1.2, yoyo:true, repeat:5}, 0);',

    'tl.fromTo(".row9", {opacity:0, x:-50}, {opacity:1, x:0, duration:0.5, stagger:0.3}, 0.1);',
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.04, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
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
