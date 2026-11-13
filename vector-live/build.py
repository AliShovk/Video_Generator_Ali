#!/usr/bin/env python3
"""Живая сцена: горит костёр, двигается человек, идёт снег. 9:16, 12 с."""
import random
from pathlib import Path

OUT = Path("/root/video-gen/vector-live/compositions")
OUT.mkdir(parents=True, exist_ok=True)


def stars(n=70, seed=2):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(80,700):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#dfe8ff" opacity="{r.uniform(0.2,0.8):.2f}"/>' for _ in range(n))


def snow_layer(n, y0, y1, rmin, rmax, op, seed):
    r = random.Random(seed)
    return "".join(
        f'<circle class="flake" cx="{r.uniform(-40,1120):.0f}" cy="{r.uniform(y0,y1):.0f}" '
        f'r="{r.uniform(rmin,rmax):.1f}" fill="#ffffff" opacity="{r.uniform(op[0],op[1]):.2f}"/>'
        for _ in range(n))


def pines(y=1420):
    out = []
    for x, h, o in [(60, 240, 0.55), (170, 300, 0.45), (960, 280, 0.5), (1040, 220, 0.6), (300, 180, 0.35)]:
        out.append(f'<path d="M {x} {y} L {x-h*0.2:.0f} {y-h*0.55:.0f} L {x-h*0.08:.0f} {y-h*0.52:.0f} '
                   f'L {x-h*0.3:.0f} {y-h*0.8:.0f} L {x:.0f} {y-h} L {x+h*0.3:.0f} {y-h*0.8:.0f} '
                   f'L {x+h*0.08:.0f} {y-h*0.52:.0f} L {x+h*0.2:.0f} {y-h*0.55:.0f} Z" fill="#0c1324" opacity="{o}"/>')
    return "".join(out)


def person(x, y, s=1.0):
    """Сидящий человек: голова, торс, две руки, ноги — каждая часть отдельно."""
    return f'''<g id="person" transform="translate({x} {y}) scale({s})">
      <ellipse cx="0" cy="6" rx="120" ry="22" fill="#0a1020" opacity="0.45"/>
      <!-- ноги -->
      <g id="legs">
        <rect x="-90" y="-40" width="230" height="44" rx="22" fill="#6b452a"/>
        <rect x="-90" y="-40" width="230" height="12" rx="6" fill="#82573a" opacity="0.8"/>
        <rect x="20" y="-8" width="34" height="30" rx="10" fill="#1f2740"/>
        <rect x="70" y="-8" width="34" height="30" rx="10" fill="#1f2740"/>
      </g>
      <!-- торс -->
      <g id="torso" transform="translate(0 -60)">
        <path d="M -58 0 q -6 -96 52 -104 q 62 8 60 104 q -56 26 -112 0 z" fill="#6b5bd2"/>
        <path d="M -52 -8 q 52 18 104 0 l 0 20 q -52 18 -104 0 z" fill="#5a4bc0"/>
      </g>
      <!-- задняя рука -->
      <g id="arm-back" transform="translate(-40 -146)">
        <rect x="-14" y="0" width="28" height="96" rx="14" fill="#5a4bc0"/>
        <circle cx="0" cy="100" r="15" fill="#f2c39d"/>
      </g>
      <!-- голова -->
      <g id="head" transform="translate(6 -186)">
        <circle cx="0" cy="0" r="34" fill="#f2c39d"/>
        <path d="M -36 -6 a 36 30 0 0 1 72 0 q -36 -14 -72 0 z" fill="#241f3a"/>
        <rect x="-4" y="-6" width="14" height="4" rx="2" fill="#241f3a" opacity="0.75"/>
        <g id="lid"><rect x="-4" y="-8" width="14" height="6" fill="#f2c39d"/></g>
        <path d="M 26 6 q 8 6 0 12" stroke="#c98f6a" stroke-width="4" fill="none"/>
      </g>
      <!-- передняя рука (тянется к огню) -->
      <g id="arm-front" transform="translate(44 -150)">
        <rect x="-15" y="-2" width="30" height="104" rx="15" fill="#7a6ae0"/>
        <circle cx="4" cy="106" r="16" fill="#f2c39d"/>
      </g>
    </g>'''


def fire(x, y, s=1.0):
    return f'''<g id="fire" transform="translate({x} {y}) scale({s})">
      <ellipse id="pool" cx="0" cy="30" rx="300" ry="90" fill="url(#warm)" opacity="0.75"/>
      <g id="logs">
        <rect x="-140" y="-26" width="280" height="54" rx="26" fill="#6b452a"/>
        <rect x="-120" y="-46" width="240" height="44" rx="22" fill="#7d5232"/>
        <path d="M -120 -26 q 120 16 240 0" stroke="#ff5a2b" stroke-width="6" fill="none" opacity="0.8"/>
      </g>
      <g id="flames">
        <path id="f1" d="M -78 0 q 14 -84 54 -120 q 12 52 30 70 q 14 -64 46 -86 q 26 86 -8 136 z" fill="#ff6a1a"/>
        <path id="f2" d="M -50 0 q 12 -62 38 -88 q 8 38 22 50 q 10 -44 32 -62 q 18 62 -6 100 z" fill="#ff9f3a"/>
        <path id="f3" d="M -26 0 q 8 -42 24 -58 q 4 24 14 32 q 6 -28 20 -40 q 12 42 -4 66 z" fill="#ffd166"/>
        <path id="f4" d="M -12 0 q 4 -26 12 -36 q 2 14 8 20 q 4 -16 10 -24 q 6 26 -2 40 z" fill="#fff3c4"/>
      </g>
      <g id="embers"></g>
    </g>'''


def ember_circles(n=26, seed=8):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        x = r.uniform(-90, 90); y = r.uniform(-40, 10); rad = r.uniform(2, 5)
        out.append(f'<circle class="ember" cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}" fill="#ffb066" opacity="{r.uniform(0.5,0.95):.2f}"/>')
    return "".join(out)


DEFS = """<defs>
  <radialGradient id="warm" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ff9a3d" stop-opacity="0.75"/><stop offset="1" stop-color="#ff9a3d" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#070c1c"/><stop offset="0.62" stop-color="#101a36"/><stop offset="1" stop-color="#182444"/>
  </linearGradient>
  <linearGradient id="snow" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#e9f1fb"/><stop offset="1" stop-color="#cddcf0"/>
  </linearGradient>
</defs>"""


def scene():
    b = ['<rect width="1080" height="1920" fill="url(#sky)"/>', stars()]
    # дальний лес
    b.append(f'<g opacity="0.85">{pines(1440)}</g>')
    # снег
    b.append('<path d="M 0 1560 Q 240 1470 520 1520 Q 820 1580 1080 1460 L 1080 1920 L 0 1920 Z" fill="url(#snow)"/>')
    b.append('<path d="M 0 1650 Q 300 1560 560 1620 Q 830 1680 1080 1590 L 1080 1920 L 0 1920 Z" fill="#ffffff" opacity="0.85"/>')
    b.append(person(330, 1560, 1.05))
    b.append(fire(720, 1560, 1.0).replace('<g id="embers"></g>', f'<g id="embers">{ember_circles()}</g>'))
    # передний снег
    b.append(snow_layer(45, 900, 1500, 4, 8, (0.5, 0.9), 11))
    b.append(snow_layer(70, 400, 1400, 2.4, 5, (0.35, 0.8), 12))
    b.append(snow_layer(60, -200, 900, 1.2, 3, (0.25, 0.7), 13))
    inner = "".join(b)
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            f'<g transform="translate(-250 -890) scale(1.5)">{inner}</g></svg>')


def main() -> None:
    body = scene()
    tl = """
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#s1 .world", { scale:1.0 }, { scale:1.04, duration:12, ease:"none" }, 0);
    // огонь: каждый язык живёт в своём ритме
    tl.to("#f1", { scaleY:1.18, scaleX:0.94, skewX:2, transformOrigin:"50% 100%", duration:0.23, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
    tl.to("#f2", { scaleY:1.26, skewX:-3, transformOrigin:"50% 100%", duration:0.17, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.04);
    tl.to("#f3", { scaleY:1.34, scaleX:0.9, transformOrigin:"50% 100%", duration:0.12, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.02);
    tl.to("#f4", { scaleY:1.4, opacity:0.75, transformOrigin:"50% 100%", duration:0.09, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.06);
    tl.to("#pool", { opacity:0.95, scale:1.06, transformOrigin:"50% 50%", duration:0.9, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
    tl.to(".ember", { y:-320, x:"+=26", opacity:0, duration:1.9, ease:"sine.out", repeat:-1, stagger:{each:0.06, from:"random"} }, 0);
    // человек: дыхание, покачивание головы, рука тянется к огню
    tl.to("#torso", { scaleY:1.03, transformOrigin:"50% 100%", duration:2.4, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
    tl.to("#head", { rotate:3, transformOrigin:"50% 100%", duration:3.2, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
    tl.fromTo("#lid", { scaleY:1 }, { scaleY:0.05, transformOrigin:"50% 50%", duration:0.09, yoyo:true, repeat:1, repeatDelay:3.2, ease:"none" }, 1.6);
    tl.to("#arm-front", { rotate:10, transformOrigin:"50% 0%", duration:1.8, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
    tl.to("#arm-back", { rotate:-4, transformOrigin:"50% 0%", duration:2.2, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.2);
    // снег: три слоя с разной скоростью
    tl.to(".flake", { y:"+=900", x:"+=40", duration:6, ease:"none", repeat:-1, stagger:{each:0.02, from:"random"} }, 0);
    window.__timelines["s1"] = tl;
    """
    page = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#070c1c; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
    .scrim {{ position:absolute; left:0; right:0; bottom:0; height:380px;
      background:linear-gradient(to top, rgba(5,9,20,0.7) 20%, rgba(5,9,20,0) 100%); }}
    .head {{ position:absolute; left:64px; right:64px; top:250px; text-align:left;
      font:900 54px/1.12 "Nunito", Arial, sans-serif; color:#ffffff; }}
    .head .big {{ display:block; font-size:92px; line-height:.95; margin-bottom:10px; color:#ffb066; }}
  </style>
  <div id="root" data-composition-id="s1" data-width="1080" data-height="1920">
    <div class="clip" id="s1-clip" data-start="0" data-duration="12">
      <div id="s1-in">
        {body}
        <div class="scrim"></div>
        <div class="head" id="s1-head"><span class="big">−40°</span>Огонь горит. Человек дышит</div>
      </div>
    </div>
  </div>
  <script>
    {tl}
  </script>
</template>
"""
    (OUT / "s1.html").write_text(page, encoding="utf-8")
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="12" data-width="1080" data-height="1920">
<div id="s1" class="scene" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0" data-duration="12" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    Path("/root/video-gen/vector-live/index.html").write_text(html, encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
