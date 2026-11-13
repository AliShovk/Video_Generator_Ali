#!/usr/bin/env python3
"""«Уклон канализации» — 8 сцен, 47 с, 9:16."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/sewer")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#eef4f7"
INK = "#1f2c36"
PIPE = "#7f97a6"
PIPE_D = "#546a78"
WATER = "#2f8fc4"
WATER_L = "#8fdcff"
RED = "#c93a26"
GREEN = "#2c8a58"
AMBER = "#e0a33e"

DEFS = """<defs>
<linearGradient id="pipeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c2d2dc"/><stop offset="0.5" stop-color="#93a8b6"/><stop offset="1" stop-color="#5d7280"/></linearGradient>
<linearGradient id="waterG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2b7fa8"/><stop offset="1" stop-color="#7fd0f2"/></linearGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=150, size=62):
    return "".join(
        f'<text class="hl" x="52" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=440):
    return (f'<g class="b"><circle cx="106" cy="{y}" r="44" fill="{INK}"/>'
            f'<text x="106" y="{y+14}" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def seg(x1, y1, x2, y2, w=86, water=True):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{PIPE}" stroke-width="{w}" stroke-linecap="round"/>'
    if water:
        s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{WATER}" stroke-width="{w-30}" stroke-linecap="round" opacity="0.9"/>'
    return s


def flow_dots(x1, y1, x2, y2, n=5, cls="fd"):
    out = []
    for i in range(n):
        t = i / n
        out.append(f'<circle class="{cls}" cx="{x1 + (x2-x1)*t:.0f}" cy="{y1 + (y2-y1)*t:.0f}" r="10" fill="{WATER_L}"/>')
    return "".join(out)


def dim(x1, y1, x2, y2, label, col=INK, size=30):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="3" stroke-dasharray="10 8"/>'
            f'<text x="{(x1+x2)/2:.0f}" y="{(y1+y2)/2 - 14:.0f}" font-family="Nunito, Arial" font-size="{size}" '
            f'font-weight="900" fill="{col}" text-anchor="middle">{label}</text>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(seg(120, 760, 900, 980, 120))
    # застой воды
    b.append(f'<ellipse cx="620" cy="900" rx="180" ry="46" fill="{WATER}" opacity="0.35"/>')
    b.append(f'<ellipse class="still" cx="620" cy="890" rx="120" ry="26" fill="{WATER_L}" opacity="0.55"/>')
    # запах
    for i in range(6):
        b.append(f'<path class="smell" d="M {760 + i*26} 800 q 20 -70 0 -140 q -20 -70 0 -140" stroke="{RED}" stroke-width="7" fill="none" opacity="0.5"/>')
    b.append(f'<text x="54" y="1200" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">вода стоит · запах из трапа</text>')
    b.append(title([("ВИНОВАТ", INK), ("УКЛОН", RED)], 160, 78))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<line x1="120" y1="820" x2="960" y2="820" stroke="{PIPE_D}" stroke-width="3" stroke-dasharray="12 10"/>')
    b.append(seg(120, 800, 960, 890, 100))
    b.append(dim(120, 700, 960, 700, "1 МЕТР"))
    b.append(dim(980, 800, 980, 890, "3 СМ", RED, 34))
    b.append(f'<path d="M 960 890 l -46 0 l 0 -18" stroke="{RED}" stroke-width="5" fill="none"/>')
    b.append(f'<text x="540" y="1120" font-family="Nunito, Arial" font-size="42" font-weight="900" fill="{INK}" text-anchor="middle">перепад высоты на метр трубы</text>')
    b.append(badge(0, 430))
    b.append(title([("ЧТО ТАКОЕ", INK), ("УКЛОН", GREEN)], 150, 64))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    rows = [("50 мм", "3,5 см", 0), ("110 мм", "2 см", 1), ("160 мм", "0,8 см", 2)]
    for txt, val, i in rows:
        y = 700 + i * 300
        b.append(f'<g class="row3 r{i}"><rect x="70" y="{y}" width="940" height="230" rx="18" fill="#ffffff" opacity="0.9"/>'
                 f'<text x="120" y="{y+90}" font-family="Nunito, Arial" font-size="54" font-weight="900" fill="{INK}">{txt}</text>'
                 f'<text x="120" y="{y+170}" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{PIPE_D}">диаметр трубы</text>'
                 f'<text x="900" y="{y+140}" font-family="Nunito, Arial" font-size="76" font-weight="900" fill="{GREEN}" text-anchor="end">{val}</text>'
                 f'<text x="900" y="{y+190}" font-family="Nunito, Arial" font-size="28" font-weight="800" fill="{PIPE_D}" text-anchor="end">на метр</text></g>')
    b.append(title([("ТРИ ЦИФРЫ", INK)], 150, 64))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<line x1="120" y1="760" x2="960" y2="760" stroke="{PIPE_D}" stroke-width="3" stroke-dasharray="12 10"/>')
    b.append(seg(120, 750, 960, 770, 110))
    for i in range(9):
        b.append(f'<circle class="silt" cx="{180 + i*85}" cy="{758 + i*2}" r="{9 + i%4}" fill="#8a6a3a" opacity="0.85"/>')
    b.append(f'<rect x="700" y="700" width="90" height="110" rx="8" fill="#8a6a3a" opacity="0.9"/>')
    b.append(f'<text x="745" y="680" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{RED}" text-anchor="middle">ЗАСОР</text>')
    b.append(f'<text x="120" y="1020" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">уклон меньше нормы</text>')
    b.append(dim(980, 750, 980, 770, "1–2 см", RED, 30))
    b.append(badge(1, 420))
    b.append(title([("МЕНЬШЕ НОРМЫ", INK), ("ИЛ ОСЕДАЕТ", RED)], 150, 56))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect x="0" y="0" width="1080" height="1920" fill="{BG}"/>']
    b.append(seg(120, 760, 960, 1250, 110))
    b.append(flow_dots(180, 790, 900, 1220, 6, "fast"))
    for i in range(7):
        b.append(f'<circle class="left" cx="{300 + i*90}" cy="{830 + i*60}" r="{8 + i%3}" fill="#8a6a3a" opacity="0.9"/>')
    b.append(f'<text x="120" y="1420" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">вода убегает, твёрдое остаётся</text>')
    b.append(badge(2, 420))
    b.append(title([("БОЛЬШЕ НОРМЫ", INK), ("ТОЖЕ ПЛОХО", RED)], 150, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # 90°
    b.append(f'<text x="270" y="620" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{RED}" text-anchor="middle">90° — ПЛОХО</text>')
    b.append(seg(150, 700, 400, 700, 96))
    b.append(seg(400, 700, 400, 980, 96))
    b.append(f'<circle class="elb" cx="400" cy="700" r="48" fill="none" stroke="{RED}" stroke-width="10"/>')
    # два по 45
    b.append(f'<text x="800" y="1120" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{GREEN}" text-anchor="middle">2×45° — ХОРОШО</text>')
    b.append(seg(620, 700, 800, 830, 96))
    b.append(seg(800, 830, 940, 1000, 96))
    b.append(f'<circle class="elb2" cx="800" cy="830" r="48" fill="none" stroke="{GREEN}" stroke-width="10"/>')
    b.append(badge(3, 420))
    b.append(title([("ПОВОРОТЫ", INK), ("ПЛАВНО", GREEN)], 150, 62))
    b.append(f'<text x="54" y="1500" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">на длинных участках — ревизия</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="440" y="500" width="200" height="1100" rx="20" fill="url(#pipeG)" stroke="{PIPE_D}" stroke-width="5"/>')
    b.append(f'<rect x="470" y="520" width="140" height="1060" rx="14" fill="#dceaf2" opacity="0.8"/>')
    for i in range(6):
        b.append(f'<circle class="air7" cx="540" cy="{620 + i*120}" r="{12 + i%4}" fill="{WATER_L}" opacity="0.7"/>')
    # вентиляция сверху
    b.append(f'<rect x="500" y="380" width="80" height="130" fill="{PIPE}" opacity="0.7"/>')
    b.append(f'<path class="smell7" d="M 540 370 q 30 -60 0 -120 q -30 -60 0 -120" stroke="{RED}" stroke-width="7" fill="none" opacity="0.5"/>')
    b.append(f'<text x="540" y="240" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{RED}" text-anchor="middle">ВЕНТИЛЯЦИЯ</text>')
    b.append(badge(4, 420))
    b.append(title([("БЕЗ ВЕНТИЛЯЦИИ", INK), ("ПАХНЕТ", RED)], 150, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="270" font-family="Nunito, Arial" font-size="56" font-weight="900" fill="{INK}" text-anchor="middle">ПРОВЕРЬ</text>')
    items = ["уклон по уровню", "50 мм — 3,5 см/м", "110 мм — 2 см/м", "два отвода по 45°", "ревизия и вентиляция"]
    for i, t in enumerate(items):
        y = 470 + i * 200
        b.append(f'<g class="row r{i}"><circle cx="150" cy="{y}" r="42" fill="{GREEN}"/>'
                 f'<path d="M 132 {y} l 12 14 l 28 -32" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round"/>'
                 f'<text x="225" y="{y+12}" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{INK}">{t}</text></g>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]


def page(sid, body, dur):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
    tl.fromTo(".b", {{ scale:0.5, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.35, ease:"back.out(3)" }}, 0.15);
    tl.to(".still", {{ scaleY:1.12, transformOrigin:"50% 50%", duration:1.6, yoyo:true, repeat:3, ease:"sine.inOut" }}, 0);
    tl.to(".smell", {{ y:-60, opacity:0, duration:2.2, stagger:0.15, repeat:2 }}, 0);
    tl.to(".silt", {{ y:12, x:20, duration:2.4, stagger:0.08, ease:"sine.inOut" }}, 0);
    tl.to(".fast", {{ x:120, y:100, duration:1.4, stagger:0.1, repeat:6, ease:"none" }}, 0);
    tl.to(".left", {{ x:-20, opacity:0.4, duration:1.6, stagger:0.12, repeat:3 }}, 0);
    tl.to(".elb", {{ rotation:12, svgOrigin:"400 700", duration:1.2, yoyo:true, repeat:3 }}, 0);
    tl.to(".elb2", {{ rotation:-8, svgOrigin:"800 830", duration:1.4, yoyo:true, repeat:3 }}, 0);
    tl.to(".air7", {{ y:-40, duration:2.0, stagger:0.12, repeat:4 }}, 0);
    tl.to(".smell7", {{ y:-30, opacity:0.2, duration:2.0, repeat:4 }}, 0);
    tl.fromTo(".row, .row3", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.3 }}, 0.2);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, fn in enumerate(SCENES):
        sid = f"s{i+1}"
        st, dur = BOUNDS[i]
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur), encoding="utf-8")
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
