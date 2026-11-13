#!/usr/bin/env python3
"""«Плёнка на окно» — 8 сцен, 29 с."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/film-window")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#e8f2fa"
INK = "#17303d"
GLASS = "#c9e2f0"
GLASS_D = "#8fb8cf"
COLD = "#2f7fa8"
WARM = "#f0a63c"
RED = "#c0392b"
WHITE = "#ffffff"

DEFS = """<defs>
<linearGradient id="glassG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e6f4fc"/><stop offset="0.5" stop-color="#c3e0f0"/><stop offset="1" stop-color="#9cc4da"/></linearGradient>
<linearGradient id="warmG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd08a"/><stop offset="1" stop-color="#f0a63c"/></linearGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def t(x, y, s, size=58, col=INK, anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="900" fill="{col}" text-anchor="{anchor}" letter-spacing="-1">{s}</text>')


def window(x=120, y=380, w=840, h=900):
    return (f'<g class="win"><rect x="{x-24}" y="{y-24}" width="{w+48}" height="{h+48}" rx="18" fill="#ffffff"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#glassG)"/>'
            f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="#ffffff" stroke-width="22"/>'
            f'<line x1="{x}" y1="{y+h/2}" x2="{x+w}" y2="{y+h/2}" stroke="#ffffff" stroke-width="22"/></g>')


def bubble_grid(x, y, w, h, cols=12, rows=13, r=11, cls="bubG", col="#ffffff"):
    out = [f'<g class="{cls}" opacity="0">']
    for i in range(cols):
        for j in range(rows):
            cx = x + i * (w / (cols - 1))
            cy = y + j * (h / (rows - 1))
            out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{col}" opacity="0.75"/>')
    out.append("</g>")
    return "".join(out)


def spraybottle(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-40" y="0" width="80" height="150" rx="18" fill="#dff0f8" stroke="{COLD}" stroke-width="4"/>'
            f'<rect x="-22" y="-46" width="44" height="50" fill="{COLD}"/>'
            f'<path d="M 22 -40 l 46 18 l 0 14 l -46 -10 z" fill="{COLD}"/>'
            f'<rect x="-40" y="60" width="80" height="60" rx="10" fill="#8fd0ee" opacity="0.7"/></g>')


def roll(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-30" y="-120" width="60" height="240" rx="30" fill="#f3f8fb" stroke="{GLASS_D}" stroke-width="4"/>'
            + "".join(f'<circle cx="{-14 + (i%3)*14}" cy="{-96 + (i//3)*24}" r="6" fill="#d7ecf7"/>' for i in range(30))
            + '</g>')


def scissors(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M -50 40 l 90 -80" stroke="#5d7280" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M -50 40 l 90 40" stroke="#5d7280" stroke-width="10" stroke-linecap="round"/>'
            f'<circle cx="-58" cy="48" r="16" fill="none" stroke="{COLD}" stroke-width="7"/>'
            f'<circle cx="-52" cy="6" r="16" fill="none" stroke="{COLD}" stroke-width="7"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(window())
    b.append(f'<g class="frostF" opacity="0.8">' + "".join(
        f'<path d="M {200 + i*70} {420 + (i%4)*60} l 20 40 l -10 40 l 30 40" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.7"/>' for i in range(10)) + '</g>')
    for i in range(5):
        b.append(f'<path class="coldA" d="M {180 + i*180} 1400 l 0 -220" stroke="{COLD}" stroke-width="10" opacity="0.6"/>')
        b.append(f'<path d="M {180 + i*180} 1180 l -14 30 l 28 0 z" fill="{COLD}" opacity="0.6"/>')
    b.append(t(60, 220, "ОДИН РУЛОН", 66, INK))
    b.append(t(60, 292, "ВМЕСТО ОБОГРЕВАТЕЛЯ", 52, COLD))
    b.append(t(60, 1780, "окно тянет холод — комната мёрзнет", 32, "#5d7280"))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="#f3f8fb"/>']
    b.append(f'<rect x="0" y="1200" width="1080" height="720" fill="#dceaf2"/>')
    b.append(roll(240, 1080, 1.1))
    b.append(spraybottle(540, 980, 1.3))
    b.append(scissors(820, 1080, 1.3))
    for i, (x, s) in enumerate((("ПЛЁНКА", 240), ("ВОДА", 540), ("НОЖНИЦЫ", 820))):
        b.append(t(s, 1420, x, 34, INK, "middle"))
    b.append(t(60, 260, "ЧТО НУЖНО", 64, INK))
    b.append(t(60, 330, "плёнка · пульверизатор · ножницы", 32, "#5d7280"))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(window())
    b.append(spraybottle(880, 1120, 1.2))
    for i in range(16):
        b.append(f'<circle class="sprayD" cx="{560 + (i*37) % 380}" cy="{700 + (i*53) % 500}" r="{4 + i%4}" fill="#9fd8f2" opacity="0.9"/>')
    b.append(t(60, 220, "ВОДА", 62, COLD))
    b.append(t(60, 290, "вместо клея", 34, "#5d7280"))
    b.append(t(60, 1780, "смочить стекло — плёнка ляжет ровно", 30, "#5d7280"))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(window())
    b.append(bubble_grid(130, 390, 820, 880, 12, 13, 11, "bubG"))
    b.append(f'<g class="squeegee"><rect x="300" y="700" width="120" height="18" rx="9" fill="#5d7280"/>'
             f'<rect x="336" y="718" width="48" height="120" rx="10" fill="#8fa3b1"/></g>')
    b.append(t(60, 220, "ПУЗЫРЯМИ", 60, INK))
    b.append(t(60, 288, "К СТЕКЛУ", 60, COLD))
    b.append(t(60, 1780, "разглаживать от центра к краям", 30, "#5d7280"))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(window())
    b.append(bubble_grid(130, 390, 820, 880, 12, 13, 11, "bubG2", "#eafaff"))
    b.append(f'<path class="cutL" d="M 120 380 l 840 0 l 0 900 l -840 0 z" stroke="{RED}" stroke-width="8" fill="none" stroke-dasharray="24 16"/>')
    b.append(scissors(600, 1180, 1.1))
    b.append(t(60, 220, "ОБРЕЗАТЬ", 60, INK))
    b.append(t(60, 1780, "по периметру, с запасом 1–2 см", 30, "#5d7280"))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="#f7fbfd"/>']
    b.append(f'<rect x="0" y="1000" width="1080" height="920" fill="#fff4e2"/>')
    b.append(f'<rect x="120" y="760" width="120" height="900" fill="url(#glassG)" stroke="{GLASS_D}" stroke-width="6"/>')
    b.append(f'<rect x="240" y="760" width="90" height="900" fill="#eaf7ff" opacity="0.9"/>')
    for i in range(9):
        b.append(f'<circle class="airB" cx="285" cy="{800 + i*96}" r="20" fill="#ffffff" stroke="{GLASS_D}" stroke-width="3"/>')
    b.append(f'<rect x="330" y="760" width="60" height="900" fill="#ffffff" opacity="0.6"/>')
    for i in range(4):
        b.append(f'<path class="warmA" d="M 700 1200 l 0 -120" stroke="{WARM}" stroke-width="10" opacity="0.8"/>')
    b.append(f'<path class="blockA" d="M 420 1150 l 70 0" stroke="{RED}" stroke-width="10"/>')
    b.append(t(60, 220, "ПОЧЕМУ РАБОТАЕТ", 56, INK))
    b.append(t(60, 300, "воздух в пузырях — изолятор", 32, "#5d7280"))
    b.append(t(470, 980, "ТЕПЛО В КОМНАТЕ", 30, WARM))
    b.append(t(60, 1400, "СТЕКЛО", 28, COLD))
    b.append(t(250, 1400, "ВОЗДУХ", 28, "#5d7280"))
    b.append(t(360, 1400, "ПЛЁНКА", 28, COLD))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(window(160, 420, 760, 780))
    b.append(bubble_grid(170, 430, 740, 760, 11, 12, 10, "bubG3", "#f2fbff"))
    b.append(f'<rect x="760" y="1320" width="220" height="420" rx="30" fill="#ffffff" stroke="{COLD}" stroke-width="5"/>')
    b.append(f'<rect class="therm" x="800" y="1500" width="60" height="200" rx="30" fill="{WARM}"/>')
    b.append(f'<circle cx="830" cy="1700" r="46" fill="{WARM}"/>')
    for i in range(6):
        b.append(f'<line x1="790" y1="{1480 - i*40}" x2="816" y2="{1480 - i*40}" stroke="#8fa3b1" stroke-width="4"/>')
    b.append(t(60, 240, "+2 °C", 92, WARM))
    b.append(t(60, 330, "у окна теплее", 34, "#5d7280"))
    b.append(t(60, 1800, "и меньше конденсата", 32, "#5d7280"))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="#fbeeea"/>']
    b.append(f'<rect x="240" y="700" width="420" height="420" rx="40" fill="#c0392b" opacity="0.15"/>')
    b.append(f'<rect x="300" y="760" width="300" height="300" rx="24" fill="#e8eef2" stroke="#8fa3b1" stroke-width="5"/>')
    for i in range(6):
        b.append(f'<line x1="{330 + i*44}" y1="790" x2="{330 + i*44}" y2="1030" stroke="#b9c6ce" stroke-width="8"/>')
    b.append(f'<rect class="filmW" x="700" y="700" width="180" height="420" rx="10" fill="#eaf7ff" stroke="{COLD}" stroke-width="5"/>')
    b.append(f'<path class="noW" d="M 700 1100 l 180 -400" stroke="{RED}" stroke-width="14" opacity="0.9"/>')
    b.append(t(60, 300, "НЕЛЬЗЯ", 72, RED))
    b.append(t(60, 380, "над обогревателем", 40, INK))
    b.append(t(60, 1760, "плёнка — не для нагрева", 30, "#7a4a3a"))
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
BGS = ["#e8f2fa", "#f3f8fb", "#e8f2fa", "#e8f2fa", "#e8f2fa", "#f7fbfd", "#e8f2fa", "#fbeeea"]
ANIM = [
    'tl.to(".coldA", {y:-30, opacity:0.3, duration:1.2, stagger:0.1, yoyo:true, repeat:5}, 0);'
    'tl.to(".frostF", {opacity:0.4, duration:1.6, yoyo:true, repeat:3}, 0);',
    'tl.fromTo(".hl", {opacity:0, y:20}, {opacity:1, y:0, duration:0.4, stagger:0.1}, 0.05);',
    'tl.to(".sprayD", {x:-120, y:80, opacity:0, duration:1.2, stagger:0.05, repeat:2, ease:"power1.in"}, 0.2);'
    'tl.to(".win", {opacity:0.95, duration:0.1}, 0);',
    'tl.fromTo(".bubG", {opacity:0, scaleY:0.3, transformOrigin:"50% 0%"}, {opacity:1, scaleY:1, duration:1.2, ease:"power2.out"}, 0.1);'
    'tl.to(".squeegee", {y:420, x:180, duration:1.6, ease:"sine.inOut"}, 0.6);',
    'tl.fromTo(".bubG2", {opacity:0, scale:0.9, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.5}, 0.05);'
    'tl.to(".cutL", {opacity:0.4, duration:0.6, yoyo:true, repeat:5}, 0.4);',
    'tl.to(".airB", {scale:1.12, transformOrigin:"50% 50%", duration:0.8, stagger:0.08, yoyo:true, repeat:4}, 0);'
    'tl.to(".warmA", {y:-40, opacity:0.4, duration:1.2, stagger:0.1, repeat:3}, 0);',
    'tl.fromTo(".bubG3", {opacity:0}, {opacity:1, duration:0.6}, 0.1);'
    'tl.fromTo(".therm", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.8, ease:"power2.out"}, 0.3);',
    'tl.to(".noW", {opacity:0.4, duration:0.5, yoyo:true, repeat:8}, 0.2);'
    'tl.to(".filmW", {rotation:4, svgOrigin:"790 910", duration:1.2, yoyo:true, repeat:3}, 0.2);',
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
    tl.fromTo(".hl", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.4, stagger:0.1 }}, 0.05);
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
