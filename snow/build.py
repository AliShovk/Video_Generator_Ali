#!/usr/bin/env python3
"""«Снег — бесплатный утеплитель» — 8 сцен, 36 с."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/snow")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

NIGHT = "#0b1622"
DEEP = "#132433"
SNOW = "#eef6fb"
SNOW_D = "#c9dcea"
GROUND = "#4a3a2c"
GROUND_L = "#5d4a38"
CONCRETE = "#9aa7ae"
CYAN = "#6fd0e8"
WARM = "#f0a63c"
RED = "#d2452f"

DEFS = """<defs>
<linearGradient id="snowG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#cfe3f2"/></linearGradient>
<linearGradient id="groundG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5b4735"/><stop offset="1" stop-color="#33261c"/></linearGradient>
<radialGradient id="glowC"><stop offset="0" stop-color="#6fd0e8" stop-opacity="0.5"/><stop offset="1" stop-color="#6fd0e8" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def txt(x, y, s, size=58, col="#ffffff", anchor="start", cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="900" fill="{col}" text-anchor="{anchor}" letter-spacing="-1">{s}</text>')


def snowflakes(n=60, seed=3):
    r = random.Random(seed)
    return "".join(
        f'<circle class="flake" cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(-200, 1700):.0f}" '
        f'r="{r.uniform(2, 6):.1f}" fill="#ffffff" opacity="{r.uniform(0.4, 0.95):.2f}"/>' for _ in range(n))


def thermometer(x, y, h=360, fill=0.3, col=CYAN, label=""):
    return (f'<g><rect x="{x}" y="{y}" width="54" height="{h}" rx="27" fill="#10202c" stroke="{col}" stroke-width="4"/>'
            f'<rect class="thermFill" x="{x+9}" y="{y + h*(1-fill) + 9}" width="36" height="{h*fill - 18}" rx="18" fill="{col}"/>'
            f'<circle cx="{x+27}" cy="{y+h+30}" r="34" fill="{col}"/>'
            f'<text x="{x+27}" y="{y+h+110}" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{col}" text-anchor="middle">{label}</text></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{NIGHT}"/>', snowflakes(50)]
    # дом и фундамент
    b.append(f'<rect x="180" y="620" width="720" height="520" fill="#1b2f3f"/>')
    b.append(f'<path d="M 150 620 L 540 380 L 930 620 Z" fill="{SNOW}"/>')
    b.append(f'<rect x="200" y="1140" width="680" height="120" fill="{CONCRETE}"/>')
    b.append(f'<rect x="200" y="1260" width="680" height="360" fill="url(#groundG)"/>')
    b.append(f'<rect x="470" y="900" width="140" height="240" fill="#2b4a5f"/>')
    # человек с лопатой
    b.append(f'<g class="shovelMan"><circle cx="300" cy="1050" r="34" fill="#f2c9a4"/>'
             f'<rect x="266" y="1084" width="68" height="120" rx="20" fill="#c0392b"/>'
             f'<rect x="276" y="1204" width="16" height="90" fill="#1e2b35"/><rect x="308" y="1204" width="16" height="90" fill="#1e2b35"/>'
             f'<rect x="330" y="1040" width="16" height="230" rx="8" fill="#8a6a3a" transform="rotate(28 338 1050)"/>'
             f'<path d="M 380 1240 l 70 30 l -20 40 l -70 -30 z" fill="#8fa3b1"/></g>')
    for i in range(7):
        b.append(f'<circle class="throwF" cx="{380 + i*30}" cy="{1180 - (i%3)*40}" r="{7 + i%4}" fill="#ffffff" opacity="0.85"/>')
    b.append(txt(540, 230, "СНЕГ ОТ ФУНДАМЕНТА", 50, "#ffffff", "middle"))
    b.append(txt(540, 300, "УБИРАТЬ НЕ НАДО", 52, WARM, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(f'<circle cx="540" cy="900" r="420" fill="url(#glowC)" opacity="0.5"/>')
    # увеличенный снег: кристаллы
    r = random.Random(5)
    for i in range(26):
        cx, cy = 160 + (i % 5) * 190, 520 + (i // 5) * 220
        b.append(f'<g class="cs"><circle cx="{cx}" cy="{cy}" r="{r.uniform(30, 46):.0f}" fill="{SNOW}" opacity="0.9"/>'
                 + "".join(f'<line x1="{cx}" y1="{cy}" x2="{cx + 40*__import__("math").cos(a)}" y2="{cy + 40*__import__("math").sin(a)}" '
                           f'stroke="#ffffff" stroke-width="4" opacity="0.8"/>' for a in [j*1.2 for j in range(6)])
                 + '</g>')
    b.append(txt(540, 300, "90% ВОЗДУХА", 72, "#ffffff", "middle"))
    b.append(txt(540, 1640, "поэтому снег держит тепло", 36, "#9fb8c8", "middle"))
    b.append(txt(540, 1720, "лучше многих утеплителей", 36, CYAN, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{NIGHT}"/>', snowflakes(30, 9)]
    b.append(f'<rect x="0" y="900" width="1080" height="1020" fill="url(#groundG)"/>')
    b.append(f'<path class="snowCap" d="M 120 900 q 120 -180 320 -170 q 240 12 360 0 q 80 -6 160 60 l 0 110 l -840 0 z" fill="url(#snowG)"/>')
    b.append(f'<rect x="380" y="900" width="120" height="600" fill="{CONCRETE}"/>')
    b.append(f'<rect x="380" y="1440" width="120" height="60" fill="#7d8a93"/>')
    b.append(thermometer(820, 1080, 300, 0.15, CYAN, "−20°"))
    b.append(thermometer(230, 1120, 260, 0.55, WARM, "0°"))
    b.append(f'<path class="frostLine" d="M 120 1250 q 400 90 840 0" stroke="#8fd4ff" stroke-width="6" stroke-dasharray="16 12" fill="none"/>')
    b.append(txt(60, 240, "РАЗРЕЗ", 62, "#ffffff"))
    b.append(txt(60, 310, "снаружи −20, под снегом 0", 32, "#9fb8c8"))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(txt(540, 220, "С СНЕГОМ / БЕЗ", 56, "#ffffff", "middle"))
    # левая половина: со снегом
    b.append(f'<rect x="60" y="420" width="450" height="1100" fill="url(#groundG)"/>')
    b.append(f'<path d="M 60 420 q 120 -100 240 -90 q 140 10 210 20 l 0 120 l -450 0 z" fill="url(#snowG)"/>')
    b.append(f'<path d="M 60 700 q 220 40 450 0" stroke="{CYAN}" stroke-width="6" stroke-dasharray="14 10" fill="none"/>')
    b.append(txt(285, 1600, "промерзание", 28, "#9fb8c8", "middle"))
    b.append(txt(285, 1650, "меньше", 34, CYAN, "middle"))
    # правая: без снега
    b.append(f'<rect x="570" y="420" width="450" height="1100" fill="url(#groundG)"/>')
    b.append(f'<path d="M 570 950 q 220 40 450 0" stroke="{RED}" stroke-width="6" stroke-dasharray="14 10" fill="none"/>')
    b.append(f'<rect x="760" y="860" width="60" height="180" fill="#8fa3b1" opacity="0.7"/>')
    b.append(txt(795, 1600, "промерзание", 28, "#9fb8c8", "middle"))
    b.append(txt(795, 1650, "глубже", 34, RED, "middle"))
    b.append(f'<path class="downA" d="M 795 1080 l 0 200" stroke="{RED}" stroke-width="10"/>')
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{NIGHT}"/>', snowflakes(40, 12)]
    b.append(f'<rect x="0" y="1200" width="1080" height="720" fill="url(#groundG)"/>')
    b.append(f'<rect x="120" y="1120" width="840" height="90" fill="{CONCRETE}"/>')
    b.append(f'<path class="pile" d="M 120 1120 q 200 -140 420 -130 q 240 10 420 0 l 0 130 l -840 0 z" fill="url(#snowG)"/>')
    for i in range(6):
        b.append(f'<path class="addSnow" d="M {200 + i*140} 700 l 0 120" stroke="#ffffff" stroke-width="12" opacity="0.8"/>')
        b.append(f'<path d="M {200 + i*140} 840 l -14 -26 l 28 0 z" fill="#ffffff" opacity="0.8"/>')
    b.append(txt(60, 240, "НАКИДЫВАТЬ", 62, "#ffffff"))
    b.append(txt(60, 310, "на отмостку и вокруг труб", 32, "#9fb8c8"))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>']
    b.append(f'<rect x="0" y="900" width="1080" height="1020" fill="url(#groundG)"/>')
    b.append(f'<rect x="140" y="760" width="800" height="220" fill="#1b2f3f"/>')
    b.append(f'<rect x="420" y="860" width="120" height="80" fill="#0a1218"/>')
    b.append(f'<rect x="430" y="870" width="100" height="60" fill="{CYAN}" opacity="0.5"/>')
    b.append(f'<path class="closeS" d="M 380 940 q 200 -160 400 0 l 0 90 l -400 0 z" fill="url(#snowG)"/>')
    b.append(f'<path class="xMark" d="M 440 860 l 80 60 M 520 860 l -80 60" stroke="{RED}" stroke-width="12" opacity="0.9"/>')
    b.append(txt(60, 220, "НЕ ЗАКРЫВАТЬ", 58, "#ffffff"))
    b.append(txt(60, 290, "продухи подпола", 40, RED))
    b.append(txt(60, 1700, "иначе — сырость и плесень", 30, "#9fb8c8"))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{NIGHT}"/>', snowflakes(25, 21)]
    b.append(f'<rect x="0" y="1000" width="1080" height="920" fill="url(#groundG)"/>')
    b.append(f'<rect x="120" y="560" width="560" height="520" fill="#1b2f3f"/>')
    b.append(f'<path class="bigPile" d="M 120 1000 q 180 -420 420 -400 q 160 14 300 180 l 0 220 l -720 0 z" fill="url(#snowG)"/>')
    b.append(f'<line x1="120" y1="700" x2="880" y2="700" stroke="{RED}" stroke-width="6" stroke-dasharray="18 12"/>')
    b.append(txt(900, 690, "уровень пола", 26, RED, "end"))
    b.append(txt(60, 240, "ВЫШЕ ПОЛА", 60, "#ffffff"))
    b.append(txt(60, 310, "не наваливать", 40, WARM))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{DEEP}"/>', snowflakes(50, 33)]
    b.append(f'<circle cx="540" cy="860" r="380" fill="url(#glowC)" opacity="0.55"/>')
    b.append(f'<path d="M 300 940 q 240 -260 480 -40 q 90 80 0 160 l -480 0 z" fill="url(#snowG)"/>')
    b.append(f'<text x="540" y="1320" font-family="Nunito, Arial" font-size="64" font-weight="900" fill="#ffffff" text-anchor="middle">БЕСПЛАТНЫЙ</text>')
    b.append(f'<text x="540" y="1400" font-family="Nunito, Arial" font-size="64" font-weight="900" fill="{CYAN}" text-anchor="middle">УТЕПЛИТЕЛЬ</text>')
    b.append(f'<text x="540" y="1520" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="#9fb8c8" text-anchor="middle">просто не мешай ему работать</text>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
BGS = [NIGHT, DEEP, NIGHT, DEEP, NIGHT, DEEP, NIGHT, DEEP]
ANIM = [
    'tl.to(".flake", {y:900, x:60, duration:4.0, stagger:0.02, repeat:2, ease:"none"}, 0);'
    'tl.to(".throwF", {x:120, y:-80, opacity:0, duration:1.2, stagger:0.06, repeat:4, ease:"power1.out"}, 0.2);'
    'tl.to(".shovelMan", {rotation:4, svgOrigin:"300 1200", duration:1.2, yoyo:true, repeat:6}, 0);',
    'tl.to(".cs", {scale:1.12, transformOrigin:"50% 50%", duration:1.0, stagger:0.05, yoyo:true, repeat:4}, 0);',
    'tl.to(".flake", {y:700, duration:4.0, stagger:0.03, repeat:2, ease:"none"}, 0);'
    'tl.to(".frostLine", {opacity:0.3, duration:0.8, yoyo:true, repeat:6}, 0.4);'
    'tl.fromTo(".thermFill", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.6, ease:"power2.out"}, 0.3);',
    'tl.to(".downA", {y:40, opacity:0.4, duration:1.0, yoyo:true, repeat:5}, 0);',
    'tl.to(".flake", {y:700, duration:4.0, stagger:0.03, repeat:2, ease:"none"}, 0);'
    'tl.to(".addSnow", {y:80, opacity:0.2, duration:1.4, stagger:0.08, repeat:3}, 0);'
    'tl.fromTo(".pile", {scaleY:0.4, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.4, ease:"power2.out"}, 0.2);',
    'tl.fromTo(".closeS", {scaleY:0.2, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.2}, 0.2);'
    'tl.to(".xMark", {opacity:0.4, duration:0.5, yoyo:true, repeat:8}, 0.6);',
    'tl.fromTo(".bigPile", {scaleY:0.5, transformOrigin:"50% 100%"}, {scaleY:1, duration:1.4}, 0.2);',
    'tl.to(".flake", {y:900, duration:5.0, stagger:0.02, repeat:2, ease:"none"}, 0);'
    'tl.to("text", {opacity:0.9, duration:0.5}, 0);',
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
    tl.fromTo(".hl", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
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
