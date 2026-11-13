#!/usr/bin/env python3
"""«Волна патоки», Бостон 1919 — 50 с, 9:16."""
from pathlib import Path

from scene import (BRICK, BRICK_L, CREAM, DEFS, GOLD, MOL, MOL_L, NIGHT, RED, SKY, STEEL,
                   STEEL_D, building, label, person, tank, wave)

OUT = Path("/root/video-gen/molasses/compositions")
OUT.mkdir(parents=True, exist_ok=True)
ROOT = Path("/root/video-gen/molasses")


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


# ------------------------------------------------------------------ 1: крюк
def s1():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append('<rect x="0" y="1500" width="1080" height="420" fill="#1a2430"/>')
    b.append(building(0, 1500, 300, 520, "#2a3a44", 3))
    b.append(building(760, 1500, 320, 600, "#26343d", 4))
    b.append(tank(120, 1500, 300, 620))
    # трещина и выброс
    b.append(f'<path class="burst" d="M 330 1000 l 26 40 l -14 34 l 30 30 l -12 40" stroke="{RED}" stroke-width="8" fill="none"/>')
    b.append(f'<g class="spray">' + "".join(
        f'<ellipse cx="{300 + i*22}" cy="{980 - (i%4)*26}" rx="{16 + i%5*6}" ry="{10 + i%3*5}" fill="{MOL_L}" opacity="0.9"/>'
        for i in range(9)) + '</g>')
    b.append(f'<g class="debris"><rect x="520" y="1180" width="70" height="12" rx="4" fill="#6b4a2a" transform="rotate(24 555 1186)"/>'
             f'<rect x="640" y="1230" width="54" height="10" rx="4" fill="#7a5738" transform="rotate(-18 667 1235)"/>'
             f'<ellipse cx="720" cy="1264" rx="22" ry="30" fill="#5a3a1e"/></g>')
    b.append(wave(-120, 1500, 1320, 760, "wave"))
    b.append(person(700, 1830, 2.2, "#f0e6d2", True) + person(830, 1810, 1.9, "#e8dcc4", True)
             + person(930, 1840, 1.7, "#d9cdb6", True))
    return svg("".join(b))


# ------------------------------------------------------------------ 2: бак
def s2():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append(building(0, 1600, 1080, 420, "#20303a", 8))
    b.append('<rect x="0" y="1600" width="1080" height="320" fill="#1b2830"/>')
    b.append(tank(300, 1600, 480, 900, "tank2"))
    b.append(f'<rect x="300" y="1600" width="480" height="34" fill="{MOL}" opacity="0.9"/>')
    b.append(f'<path class="puddle" d="M 200 1610 q 340 -40 700 0 q 40 26 -30 40 q -300 30 -640 0 q -60 -14 -30 -40 z" fill="{MOL}"/>')
    b.append(person(880, 1600, 1.5, "#20262c") + person(960, 1600, 1.4, "#2b333b"))
    b.append('<g class="crates"><rect x="60" y="1500" width="90" height="70" fill="#6b4a2a"/><rect x="70" y="1420" width="70" height="70" fill="#7a5738"/></g>')
    return svg("".join(b))


# ------------------------------------------------------------------ 3: разрез стенки
def s3():
    b = ['<rect width="1080" height="1920" fill="#eef2f4"/>']
    b.append('<rect x="0" y="1560" width="1080" height="360" fill="#dbe4e8"/>')
    # нормальная стенка
    b.append(f'<g><rect x="90" y="420" width="300" height="240" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/>'
             f'<text x="240" y="380" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#20303a" text-anchor="middle">НУЖНО</text></g>')
    # фактическая стенка — вдвое тоньше
    b.append(f'<g><rect x="620" y="420" width="150" height="240" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/>'
             f'<text x="695" y="380" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{RED}" text-anchor="middle">БЫЛО</text></g>')
    # трещины
    for i, (x0, y0) in enumerate([(150, 470), (250, 520), (700, 470), (660, 560)]):
        b.append(f'<path class="crack" d="M {x0} {y0} l 18 26 l -10 24 l 22 22" stroke="{RED}" stroke-width="5" fill="none"/>')
    b.append(f'<line x1="90" y1="740" x2="390" y2="740" stroke="#20303a" stroke-width="4"/>')
    b.append(label(240, 790, "25 ММ", 34, "#20303a", 900, "middle"))
    b.append(f'<line x1="620" y1="740" x2="770" y2="740" stroke="{RED}" stroke-width="4"/>')
    b.append(label(695, 790, "12 ММ", 34, RED, 900, "middle"))
    # мороз
    b.append(f'<g class="frost"><circle cx="900" cy="1050" r="90" fill="#dceaf5" stroke="#8fb6cd" stroke-width="6"/>'
             f'<rect x="890" y="976" width="20" height="86" rx="10" fill="#4a90c2"/>'
             f'<circle cx="900" cy="1074" r="26" fill="#4a90c2"/>'
             f'<text x="900" y="1200" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#2b5f86" text-anchor="middle">−14 °C</text></g>')
    # трещины в металле крупно
    b.append(f'<g class="grain">' + "".join(
        f'<circle cx="{760 + (i%7)*26}" cy="{1000 + (i//7)*26}" r="4" fill="#8d99a3"/>' for i in range(42)) + '</g>')
    return svg("".join(b))


# ------------------------------------------------------------------ 4: волна по улице
def s4():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append('<rect x="0" y="1560" width="1080" height="360" fill="#222d36"/>')
    b.append(building(0, 1560, 260, 700, "#2a3a44", 3))
    b.append(building(820, 1560, 260, 760, "#243440", 3))
    # эстакада
    b.append(f'<g class="rails">' + "".join(
        f'<rect x="{60 + i*120}" y="820" width="14" height="740" fill="#3a4650"/>' for i in range(9)) + '</g>')
    b.append('<rect x="0" y="780" width="1080" height="34" fill="#46525c"/>')
    b.append('<rect x="0" y="700" width="1080" height="14" fill="#5a6670"/>')
    b.append(wave(-80, 1560, 1320, 900, "wave4"))
    b.append(person(700, 1840, 2.3, "#f0e6d2", True) + person(840, 1820, 1.9, "#e8dcc4", True))
    return svg("".join(b))


# ------------------------------------------------------------------ 5: итог
def s5():
    b = ['<rect width="1080" height="1920" fill="#101a1f"/>']
    b.append('<g class="paper"><rect x="70" y="520" width="940" height="1080" rx="10" fill="#efe6d2"/></g>')
    b.append('<text x="540" y="700" font-family="Nunito, Arial" font-size="52" font-weight="900" fill="#2a2118" text-anchor="middle">БОСТОН, 15 ЯНВАРЯ 1919</text>')
    b.append('<text class="big" x="540" y="960" font-family="Nunito, Arial" font-size="220" font-weight="900" fill="#c0392b" text-anchor="middle">21</text>')
    b.append('<text x="540" y="1030" font-family="Nunito, Arial" font-size="46" font-weight="800" fill="#2a2118" text-anchor="middle">погибший</text>')
    b.append('<text class="big2" x="540" y="1190" font-family="Nunito, Arial" font-size="150" font-weight="900" fill="#2a2118" text-anchor="middle">150</text>')
    b.append('<text x="540" y="1250" font-family="Nunito, Arial" font-size="42" font-weight="800" fill="#2a2118" text-anchor="middle">раненых</text>')
    b.append('<line x1="200" y1="1330" x2="880" y2="1330" stroke="#b9ab8f" stroke-width="4"/>')
    b.append('<text x="540" y="1420" font-family="Nunito, Arial" font-size="38" font-weight="800" fill="#5a4a36" text-anchor="middle">после этого дела в США ввели</text>')
    b.append('<text x="540" y="1480" font-family="Nunito, Arial" font-size="38" font-weight="800" fill="#5a4a36" text-anchor="middle">обязательные расчёты прочности</text>')
    return svg("".join(b))


SCENES = {"s1": (s1, 9), "s2": (s2, 10), "s3": (s3, 11), "s4": (s4, 11), "s5": (s5, 9)}
HEAD = {
    "s1": [("8 МЕТРОВ", "#e0a33e"), ("60 КМ/Ч", "#ffffff")],
    "s2": [("БАК", "#e0a33e"), ("С ПАТОКОЙ", "#ffffff")],
    "s3": [("ВДВОЕ", "#c0392b"), ("ТОНЬШЕ", "#20303a")],
    "s4": [("ШЕСТЬ", "#e0a33e"), ("КВАРТАЛОВ", "#ffffff")],
    "s5": [("21", "#c0392b"), ("И 150", "#2a2118")],
}


def page(sid, body, dur):
    head = "".join(
        f'<text class="hl" x="56" y="{228 + i*92}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="72" font-weight="900" letter-spacing="-1">{s}</text>' for i, (s, c) in enumerate(HEAD[sid]))
    if sid != "s5":
        body = body.replace('</svg>', f'<g class="head">{head}</g></svg>')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{'#101a1f' if sid=='s5' else '#1b2a33'}; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">{body}</div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.02 }}, {{ scale:1.07, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".wave", {{ x:-260 }}, {{ x:120, duration:{dur}, ease:"power1.in" }}, 0);
    tl.to(".wave4", {{ x:"+=180", duration:{dur}, ease:"power1.in" }}, 0);
    tl.fromTo(".spray", {{ opacity:0.4, y:20 }}, {{ opacity:1, y:-18, duration:2.4, ease:"power2.out" }}, 0);
    tl.to(".burst", {{ opacity:0.4, duration:0.5, yoyo:true, repeat:16 }}, 0);
    tl.to(".debris", {{ y:-40, x:26, duration:3.2, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0);
    tl.to(".leak", {{ opacity:0.35, duration:1.1, yoyo:true, repeat:12, stagger:0.12, ease:"sine.inOut" }}, 0);
    tl.to(".puddle", {{ scaleX:1.04, transformOrigin:"50% 50%", duration:2.2, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0);
    tl.to(".crack", {{ opacity:0.25, duration:0.6, yoyo:true, repeat:20, stagger:0.15 }}, 0);
    tl.to(".grain", {{ x:"+=10", y:"-=8", duration:2.4, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0);
    tl.to(".frost", {{ y:-10, duration:1.6, yoyo:true, repeat:6, ease:"sine.inOut" }}, 0);
    tl.to(".rails", {{ rotation:0.6, svgOrigin:"540 1560", duration:3, yoyo:true, repeat:3, ease:"sine.inOut" }}, 0);
    tl.to(".crates", {{ rotation:2, svgOrigin:"100 1570", duration:1.8, yoyo:true, repeat:5, ease:"sine.inOut" }}, 0);
    tl.fromTo(".paper", {{ y:40, opacity:0 }}, {{ y:0, opacity:1, duration:0.6, ease:"power2.out" }}, 0.1);
    tl.fromTo(".big", {{ scale:0.4, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.7, ease:"back.out(2)" }}, 0.3);
    tl.fromTo(".big2", {{ scale:0.5, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.7, ease:"back.out(2)" }}, 0.8);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts, start = [], 0
    for i, (sid, (fn, dur)) in enumerate(SCENES.items()):
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur), encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        start += dur
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("ok", start)


if __name__ == "__main__":
    build()
