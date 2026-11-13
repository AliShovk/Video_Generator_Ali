#!/usr/bin/env python3
"""Детализированный персонаж: идёт к костру, садится. 16 с, 9:16."""
import random
from pathlib import Path

from rig import figure, sitter

OUT = Path("/root/video-gen/vector-char/compositions")
OUT.mkdir(parents=True, exist_ok=True)


def stars(n=80, seed=3):
    r = random.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(60,760):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#dfe8ff" opacity="{r.uniform(0.2,0.85):.2f}"/>' for _ in range(n))


def snow(n, y0, y1, rmin, rmax, seed, op=(0.25, 0.85)):
    r = random.Random(seed)
    return "".join(
        f'<circle class="flake s{seed}" cx="{r.uniform(-60,1140):.0f}" cy="{r.uniform(y0,y1):.0f}" '
        f'r="{r.uniform(rmin,rmax):.1f}" fill="#ffffff" opacity="{r.uniform(*op):.2f}"/>' for _ in range(n))


def fire(x, y, s=1.0):
    r = random.Random(5)
    embers = "".join(f'<circle class="ember" cx="{r.uniform(-100,100):.0f}" cy="{r.uniform(-30,20):.0f}" r="{r.uniform(2,5):.1f}" fill="#ffb066" opacity="0.85"/>' for _ in range(24))
    return f'''<g id="fire" transform="translate({x} {y}) scale({s})">
      <ellipse id="pool" cx="0" cy="20" rx="340" ry="110" fill="url(#warm)" opacity="0.8"/>
      <g id="logs">
        <rect x="-150" y="-22" width="300" height="52" rx="26" fill="#5f3d24"/>
        <rect x="-126" y="-44" width="252" height="40" rx="20" fill="#744a2c"/>
        <path d="M -126 -24 q 126 14 252 0" stroke="#ff5a2b" stroke-width="6" fill="none" opacity="0.85"/>
      </g>
      <g id="flames">
        <path id="fl1" d="M -82 0 q 16 -88 58 -126 q 12 54 32 72 q 14 -66 48 -90 q 28 90 -8 144 z" fill="#ff6a1a"/>
        <path id="fl2" d="M -54 0 q 12 -66 40 -94 q 8 40 24 54 q 10 -48 34 -66 q 20 66 -6 106 z" fill="#ff9f3a"/>
        <path id="fl3" d="M -28 0 q 8 -46 26 -64 q 4 26 14 34 q 6 -30 22 -42 q 12 44 -4 72 z" fill="#ffd166"/>
        <path id="fl4" d="M -10 0 q 4 -28 12 -38 q 2 14 8 20 q 4 -16 10 -26 q 6 28 -2 44 z" fill="#fff3c4"/>
      </g>
      <g id="embers">{embers}</g>
    </g>'''


DEFS = """<defs>
  <radialGradient id="warm" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ff9a3d" stop-opacity="0.85"/><stop offset="1" stop-color="#ff9a3d" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#050a18"/><stop offset="0.6" stop-color="#0d1730"/><stop offset="1" stop-color="#16224a"/>
  </linearGradient>
  <linearGradient id="snowg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#e8f0fb"/><stop offset="1" stop-color="#c9d9ee"/>
  </linearGradient>
</defs>"""


def scene():
    b = ['<rect width="1080" height="1920" fill="url(#sky)"/>', stars()]
    b.append('<path d="M 0 1560 Q 260 1480 540 1520 Q 840 1570 1080 1470 L 1080 1920 L 0 1920 Z" fill="url(#snowg)"/>')
    b.append('<path d="M 0 1640 Q 320 1560 600 1610 Q 860 1660 1080 1580 L 1080 1920 L 0 1920 Z" fill="#ffffff" opacity="0.9"/>')
    b.append(fire(870, 1560, 1.05))
    b.append(figure(-230, 1200, 2.0))
    b.append(sitter(655, 1500, 2.0))
    b.append(snow(60, 300, 1500, 2, 6, 21))
    b.append(snow(40, 600, 1550, 4, 9, 22))
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{"".join(b)}</svg>'


TL = """
const tl = gsap.timeline({ paused: true });
tl.fromTo("#s1 .world", { scale:1.0 }, { scale:1.14, duration:16, ease:"none" }, 0);
// ходьба
tl.to("#fig", { x: 380, duration: 6.0, ease:"none" }, 0.3);
tl.to("#legL", { rotate: 24, svgOrigin:"0 0", duration:0.33, yoyo:true, repeat:17, ease:"sine.inOut" }, 0.3);
tl.to("#legR", { rotate: -24, svgOrigin:"0 0", duration:0.33, yoyo:true, repeat:17, ease:"sine.inOut" }, 0.3);
tl.to("#armL", { rotate: -22, svgOrigin:"0 0", duration:0.33, yoyo:true, repeat:17, ease:"sine.inOut" }, 0.3);
tl.to("#armR", { rotate: 22, svgOrigin:"0 0", duration:0.33, yoyo:true, repeat:17, ease:"sine.inOut" }, 0.3);
tl.to("#fig", { y: -9, duration:0.33, yoyo:true, repeat:17, ease:"sine.inOut" }, 0.3);
tl.to("#headBall", { rotate: 3, svgOrigin:"0 60", duration:0.66, yoyo:true, repeat:8, ease:"sine.inOut" }, 0.3);
// садится
tl.to("#fig", { opacity: 0, duration: 0.16 }, 6.34);
tl.to("#sitter", { opacity: 1, duration: 0.2 }, 6.36);
// жизнь у костра
tl.to("#sitTorso", { scaleY:1.025, transformOrigin:"50% 100%", duration:2.2, yoyo:true, repeat:-1, ease:"sine.inOut" }, 7.2);
// огонь
tl.to("#fl1", { scaleY:1.2, scaleX:0.94, skewX:2, transformOrigin:"50% 100%", duration:0.22, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
tl.to("#fl2", { scaleY:1.28, skewX:-3, transformOrigin:"50% 100%", duration:0.17, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.03);
tl.to("#fl3", { scaleY:1.36, transformOrigin:"50% 100%", duration:0.12, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.02);
tl.to("#fl4", { scaleY:1.45, opacity:0.7, transformOrigin:"50% 100%", duration:0.09, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0.05);
tl.to("#pool", { opacity:1, scale:1.05, transformOrigin:"50% 50%", duration:0.85, yoyo:true, repeat:-1, ease:"sine.inOut" }, 0);
tl.to(".ember", { y:-360, x:"+=30", opacity:0, duration:1.8, ease:"sine.out", repeat:-1, stagger:{each:0.07, from:"random"} }, 0);
tl.to(".flake", { y:"+=900", x:"+=40", duration:6.5, ease:"none", repeat:-1, stagger:{each:0.02, from:"random"} }, 0);
window.__timelines["s1"] = tl;
"""


def main() -> None:
    page = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#050a18; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
  </style>
  <div id="root" data-composition-id="s1" data-width="1080" data-height="1920">
    <div class="clip" id="s1-clip" data-start="0" data-duration="16">
      <div id="s1-in">{scene()}</div>
    </div>
  </div>
  <script>{TL}</script>
</template>
"""
    (OUT / "s1.html").write_text(page, encoding="utf-8")
    html = """<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden}
#root{position:relative;width:100%;height:100%;overflow:hidden}.scene{position:absolute;inset:0}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="16" data-width="1080" data-height="1920">
<div id="s1" class="scene" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0" data-duration="16" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
</div><script>window.__timelines=window.__timelines||{};window.__timelines["main"]=gsap.timeline({paused:true});</script>
</body></html>"""
    Path("/root/video-gen/vector-char/index.html").write_text(html, encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
