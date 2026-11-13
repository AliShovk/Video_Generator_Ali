#!/usr/bin/env python3
"""«Гидроудар» — 8 сцен, 41 с, 9:16."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/hammer")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#0d1720"
INK = "#e9f3f9"
STEEL = "#93a8b6"
STEEL_D = "#5a6f7d"
WATER = "#2f8fc4"
WATER_L = "#8fdcff"
RED = "#e0452f"
AMBER = "#ffb247"

DEFS = """<defs>
<linearGradient id="steelG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c2d2dc"/><stop offset="0.5" stop-color="#8fa4b2"/><stop offset="1" stop-color="#546874"/></linearGradient>
<linearGradient id="waterG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1f6f9c"/><stop offset="1" stop-color="#7fd0f2"/></linearGradient>
<radialGradient id="bangG"><stop offset="0" stop-color="#ffd9a8" stop-opacity="0.9"/><stop offset="1" stop-color="#ffd9a8" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=150, size=66):
    return "".join(
        f'<text class="hl" x="52" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=460):
    return (f'<g class="b"><circle cx="108" cy="{y}" r="46" fill="{RED}"/>'
            f'<text x="108" y="{y+14}" font-family="Nunito, Arial" font-size="36" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def pipe_h(x, y, w, h=86):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/>'
            f'<rect x="{x+8}" y="{y+16}" width="{w-16}" height="{h-32}" rx="10" fill="url(#waterG)" opacity="0.85"/>')


def pipe_v(x, y, h, w=86):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/>'
            f'<rect x="{x+16}" y="{y+8}" width="{w-32}" height="{h-16}" rx="10" fill="url(#waterG)" opacity="0.85"/>')


def rings(cx, cy, n=4, cls="ring"):
    return "".join(
        f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{50 + i*55}" fill="none" stroke="{AMBER}" stroke-width="{9-i}" opacity="0.8"/>'
        for i in range(n))


def bgc():
    grid = "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#ffffff" stroke-width="1" opacity="0.04"/>' for y in range(0, 1920, 80))
    grid += "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1920" stroke="#ffffff" stroke-width="1" opacity="0.04"/>' for x in range(0, 1080, 80))
    return (f'<g>{grid}<circle cx="540" cy="960" r="620" fill="#1b3346" opacity="0.35"/>'
            f'<rect x="0" y="0" width="1080" height="260" fill="#000" opacity="0.25"/>'
            f'<rect x="0" y="1660" width="1080" height="260" fill="#000" opacity="0.35"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append('<rect x="0" y="0" width="1080" height="1920" fill="#101c26"/>')
    b.append(pipe_h(60, 900, 960, 100))
    b.append(pipe_v(60, 700, 220, 100))
    b.append(f'<rect x="40" y="860" width="140" height="180" fill="{STEEL_D}" opacity="0.5"/>')
    for i in range(5):
        b.append(f'<path class="vib" d="M {180 + i*160} 860 q -20 -30 0 -60" stroke="{AMBER}" stroke-width="7" fill="none" opacity="0.7"/>')
    b.append(f'<circle class="bang" cx="150" cy="880" r="180" fill="url(#bangG)" opacity="0"/>')
    b.append(title([("СТУК", INK), ("В ТРУБЕ", RED)], 160, 78))
    b.append(f'<text x="54" y="420" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}" opacity="0.8">ночью дрожит стена</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append(pipe_h(80, 700, 620))
    b.append(pipe_v(620, 700, 560))
    b.append(f'<rect x="600" y="1240" width="120" height="120" fill="{STEEL_D}"/>')
    b.append(f'<g class="slug"><rect x="120" y="716" width="240" height="54" rx="12" fill="{WATER_L}" opacity="0.75"/></g>')
    b.append(f'<path class="speed" d="M 380 743 l 120 0" stroke="{WATER_L}" stroke-width="10"/>')
    b.append(rings(660, 1300, 5, "ring2"))
    b.append(f'<circle class="impact" cx="660" cy="1300" r="60" fill="{AMBER}" opacity="0.5"/>')
    b.append(badge(0, 430))
    b.append(title([("ВОДА", INK), ("НЕ СЖИМАЕТСЯ", RED)], 140, 60))
    b.append(f'<text x="54" y="480" font-family="Nunito, Arial" font-size="30" font-weight="800" fill="{INK}" opacity="0.75">вся энергия — в одну точку</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append(pipe_h(80, 760, 900, 110))
    b.append(f'<ellipse class="airP" cx="520" cy="815" rx="110" ry="40" fill="#eaf8ff" opacity="0.9"/>')
    b.append(f'<text x="520" y="828" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{STEEL_D}" text-anchor="middle">ВОЗДУХ</text>')
    b.append(f'<path class="squeeze" d="M 380 815 l 40 0" stroke="{RED}" stroke-width="8"/>')
    b.append(f'<path class="squeeze" d="M 660 815 l -40 0" stroke="{RED}" stroke-width="8"/>')
    b.append(rings(520, 815, 3, "ring3"))
    b.append(badge(1, 470))
    b.append(title([("ВОЗДУШНЫЙ", INK), ("КАРМАН", RED)], 140, 62))
    b.append(f'<text x="54" y="360" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}" opacity="0.8">сжимается и хлопает</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append(pipe_h(80, 720, 560, 96))
    b.append(f'<circle class="v4" cx="700" cy="768" r="66" fill="none" stroke="{RED}" stroke-width="12"/>')
    b.append(f'<line x1="646" y1="768" x2="754" y2="768" stroke="{RED}" stroke-width="10"/>')
    b.append(f'<line x1="700" y1="714" x2="700" y2="822" stroke="{RED}" stroke-width="10"/>')
    for i in range(4):
        b.append(f'<circle class="wave4" cx="{740 + i*40}" cy="768" r="{30 + i*14}" fill="none" stroke="{WATER_L}" stroke-width="7" opacity="0.7"/>')
    b.append(f'<text x="860" y="700" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{AMBER}">ВОЛНА</text>')
    b.append(badge(2, 450))
    b.append(title([("КРАН ЗАКРЫЛИ", INK), ("СЛИШКОМ БЫСТРО", RED)], 140, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append(f'<circle cx="360" cy="900" r="140" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="6"/>')
    b.append(f'<g class="imp5"><path d="M 360 820 l 60 50 l -60 50 l -60 -50 z" fill="{WATER_L}"/></g>')
    b.append(f'<text x="360" y="1090" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">НАСОС · MAX</text>')
    b.append(f'<path d="M 500 900 L 900 900" stroke="{STEEL}" stroke-width="70" stroke-linecap="round"/>')
    b.append(f'<path class="narrow" d="M 780 870 L 840 930" stroke="{RED}" stroke-width="12"/>')
    b.append(f'<text x="810" y="1010" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{RED}" text-anchor="middle">УЗКО</text>')
    for i in range(8):
        b.append(f'<path class="turb" d="M {520 + i*40} 880 q 14 -30 0 -60" stroke="{WATER_L}" stroke-width="6" fill="none" opacity="0.5"/>')
    b.append(badge(3, 440))
    b.append(title([("ПОТОК", INK), ("РВЁТСЯ", RED)], 140, 64))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append(pipe_h(80, 700, 760, 96))
    b.append(f'<rect x="700" y="690" width="120" height="120" fill="{STEEL_D}"/>')
    b.append(f'<path class="crack6" d="M 760 690 l 20 40 l -14 40 l 24 40" stroke="{RED}" stroke-width="9" fill="none"/>')
    b.append(f'<path class="jet6" d="M 780 790 q 60 120 40 240" stroke="{WATER_L}" stroke-width="16" fill="none" opacity="0.85"/>')
    b.append(f'<ellipse cx="700" cy="1500" rx="340" ry="46" fill="{WATER}" opacity="0.45"/>')
    for i in range(10):
        b.append(f'<circle class="sp6" cx="{640 + (i*43) % 300}" cy="{900 + (i*47) % 260}" r="{4 + i%4}" fill="{WATER_L}" opacity="0.8"/>')
    b.append(badge(4, 430))
    b.append(title([("ТРЕЩИНА", INK), ("И РАЗРЫВ", RED)], 140, 64))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>', bgc()]
    b.append(pipe_h(80, 780, 920, 96))
    # кран Маевского
    b.append(f'<circle cx="300" cy="760" r="40" fill="none" stroke="{AMBER}" stroke-width="10"/>')
    b.append(f'<text x="300" y="660" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{AMBER}" text-anchor="middle">ВОЗДУХ</text>')
    # гаситель
    b.append(f'<rect x="560" y="700" width="90" height="180" rx="20" fill="{STEEL}" stroke="{STEEL_D}" stroke-width="5"/>')
    b.append(f'<text x="605" y="950" font-family="Nunito, Arial" font-size="24" font-weight="900" fill="{INK}" text-anchor="middle">ГАСИТЕЛЬ</text>')
    # крепления
    for x in (820, 940):
        b.append(f'<rect x="{x}" y="740" width="16" height="180" fill="{STEEL_D}"/>')
    b.append(badge(5, 430))
    b.append(title([("УБРАТЬ", INK), ("ПРИЧИНУ", RED)], 140, 62))
    b.append(f'<text x="54" y="360" font-family="Nunito, Arial" font-size="30" font-weight="800" fill="{INK}" opacity="0.8">воздух · плавно · гаситель · крепления</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="#070f15"/>']
    b.append(pipe_h(100, 900, 880, 90))
    for i in range(4):
        b.append(f'<circle class="ring8" cx="540" cy="945" r="{60 + i*70}" fill="none" stroke="{RED}" stroke-width="6" opacity="0.5"/>')
    b.append(f'<text x="540" y="700" font-family="Nunito, Arial" font-size="52" font-weight="900" fill="{INK}" text-anchor="middle">СТУК — ЭТО УДАР</text>')
    b.append(f'<text x="540" y="1400" font-family="Nunito, Arial" font-size="38" font-weight="800" fill="{AMBER}" text-anchor="middle">он повторяется каждую ночь</text>')
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
    tl.fromTo(".b", {{ scale:0.5, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.35, ease:"back.out(3)" }}, 0.15);
    tl.to(".vib", {{ y:-12, duration:0.12, yoyo:true, repeat:24, stagger:0.04, ease:"none" }}, 0);
    tl.to(".bang", {{ opacity:0.9, scale:1.3, transformOrigin:"50% 50%", duration:0.25, yoyo:true, repeat:10 }}, 0.2);
    tl.to(".slug", {{ x:200, duration:0.9, ease:"power2.in" }}, 0.3);
    tl.to(".slug", {{ x:0, duration:0.5, ease:"power2.out" }}, 1.3);
    tl.to(".speed", {{ x:60, duration:0.5, yoyo:true, repeat:8 }}, 0);
    tl.to(".ring2, .ring3, .ring8", {{ scale:2.2, opacity:0, transformOrigin:"50% 50%", duration:1.6, stagger:0.25, repeat:4, ease:"power2.out" }}, 0);
    tl.to(".impact", {{ scale:1.6, opacity:0, transformOrigin:"50% 50%", duration:0.9, repeat:5 }}, 0);
    tl.to(".airP", {{ scaleX:0.7, scaleY:0.8, transformOrigin:"50% 50%", duration:0.5, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0);
    tl.to(".squeeze", {{ x:14, duration:0.35, yoyo:true, repeat:10 }}, 0);
    tl.to(".v4", {{ rotation:-110, svgOrigin:"700 768", duration:0.5, ease:"power2.in" }}, 0.3);
    tl.to(".wave4", {{ x:120, opacity:0, duration:1.2, stagger:0.1, repeat:4, ease:"power1.out" }}, 0.7);
    tl.to(".imp5", {{ rotation:360, svgOrigin:"360 900", duration:0.8, repeat:20, ease:"none" }}, 0);
    tl.to(".turb", {{ y:-16, opacity:0.2, duration:0.4, stagger:0.05, repeat:20 }}, 0);
    tl.to(".narrow", {{ opacity:0.3, duration:0.4, yoyo:true, repeat:12 }}, 0);
    tl.to(".crack6", {{ opacity:0.3, duration:0.3, yoyo:true, repeat:14 }}, 0);
    tl.to(".jet6", {{ scaleY:1.1, transformOrigin:"0% 0%", duration:0.18, yoyo:true, repeat:18 }}, 0);
    tl.to(".sp6", {{ y:-140, opacity:0, duration:1.2, stagger:0.06, repeat:4 }}, 0);
    tl.to(".ring8", {{ opacity:0, duration:1.8, stagger:0.3, repeat:6 }}, 0);
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
