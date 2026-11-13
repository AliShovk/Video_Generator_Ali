#!/usr/bin/env python3
"""Демо: оживление статичных иллюстраций — снег, огонь, искры, камера."""
import random
from pathlib import Path

OUT = Path("/root/video-gen/vector-anim/compositions")
OUT.mkdir(parents=True, exist_ok=True)


def snow(n=90, seed=3):
    r = random.Random(seed)
    return "".join(
        f'<circle class="flake" cx="{r.uniform(-40,1120):.0f}" cy="{r.uniform(-260,1100):.0f}" '
        f'r="{r.uniform(2,6):.1f}" fill="#ffffff" opacity="{r.uniform(0.25,0.9):.2f}"/>' for _ in range(n))


def embers(n=26, seed=7):
    r = random.Random(seed)
    return "".join(
        f'<circle class="ember" cx="{r.uniform(300,470):.0f}" cy="{r.uniform(1140,1290):.0f}" '
        f'r="{r.uniform(2,5):.1f}" fill="#ffb066" opacity="{r.uniform(0.5,0.95):.2f}"/>' for _ in range(n))


def flames(x, y, s=1.0):
    return (f'<g id="fire-g" transform="translate({x} {y}) scale({s})">'
            f'<ellipse cx="0" cy="-10" rx="190" ry="100" fill="url(#glow)"/>'
            f'<path class="f1" d="M -70 0 q 14 -64 48 -92 q 10 40 26 54 q 12 -50 40 -66 q 20 66 -6 104 z" fill="#ff7a1a"/>'
            f'<path class="f2" d="M -40 0 q 10 -44 30 -62 q 6 26 18 36 q 8 -30 24 -42 q 12 44 -4 68 z" fill="#ffc845"/>'
            f'<path class="f3" d="M -16 0 q 6 -26 18 -38 q 4 16 12 22 q 6 -18 16 -26 q 8 28 -2 42 z" fill="#fff3c4"/>'
            f'</g>')


TEMPLATE = """<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{bg}; }}
    .world {{ position:absolute; inset:0; transform-origin:50% 50%; }}
    .bg {{ position:absolute; inset:0; width:100%; height:100%; }}
    .art {{ position:absolute; left:50%; transform:translateX(-50%); width:{w}px; top:{top}px; }}
    .fx {{ position:absolute; inset:0; width:100%; height:100%; }}
    .head {{ position:absolute; left:60px; right:60px; bottom:320px; text-align:center;
      font:900 58px/1.12 "Nunito", Arial, sans-serif; color:{fg}; }}
    .head .big {{ display:block; font-size:100px; line-height:.95; margin-bottom:14px; color:{accent}; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">
        <div class="world" id="{sid}-world">
          <svg class="bg" viewBox="0 0 1080 1920" preserveAspectRatio="none">
            <defs><radialGradient id="glow" cx="50%" cy="50%" r="50%">
              <stop offset="0" stop-color="#ffb347" stop-opacity="0.7"/>
              <stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient></defs>
            {bgfx}
          </svg>
          <img class="art" id="{sid}-art" src="assets/{img}" alt=""/>
          <svg class="fx" viewBox="0 0 1080 1920">{fx}</svg>
        </div>
        <div class="head" id="{sid}-head"><span class="big">{big}</span>{cap}</div>
      </div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    tl_{sid}.fromTo("#{sid}-world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    tl_{sid}.fromTo("#{sid}-art", {{ opacity:0, y:40 }}, {{ opacity:1, y:0, duration:0.9, ease:"power3.out" }}, 0.05);
    tl_{sid}.fromTo("#{sid}-head", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.6, ease:"power3.out" }}, 0.35);
    tl_{sid}.to(".flake", {{ y:"+=640", x:"+=30", duration:3.2, ease:"none", repeat:-1, stagger:{{ each:0.02, from:"random" }} }}, 0);
    tl_{sid}.to(".ember", {{ y:-460, x:"+=22", opacity:0, duration:2.0, ease:"sine.out", repeat:-1, stagger:{{ each:0.05, from:"random" }} }}, 0);
    tl_{sid}.to("#fireg", {{ opacity:0.85, duration:0.55, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 0);
    tl_{sid}.to(".f1", {{ scaleY:1.16, scaleX:0.95, transformOrigin:"50% 100%", duration:0.18, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 0);
    tl_{sid}.to(".f2", {{ scaleY:1.22, transformOrigin:"50% 100%", duration:0.14, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 0.04);
    tl_{sid}.to(".f3", {{ scaleY:1.3, transformOrigin:"50% 100%", duration:0.11, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 0.02);
    tl_{sid}.to("#fire-g ellipse", {{ opacity:0.65, duration:0.7, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 0);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""

SCENES = [
    dict(sid="s1", img="into-the-night_nd84.svg", dur=4, bg="#0d1530", fg="#eaf0ff", accent="#8ab6ff",
         big="−40°", cap="Ночь. Ты один у костра", top=600, w=1220,
         bgfx='<rect width="1080" height="1920" fill="#0d1530"/>'
              '<circle cx="290" cy="390" r="300" fill="#1b2a55" opacity="0.55"/>'
              '<circle cx="850" cy="310" r="220" fill="#22336a" opacity="0.5"/>',
         fx=snow(120, 4)),
    dict(sid="s2", img="campfire_42p5.svg", dur=4, bg="#1a1230", fg="#ffffff", accent="#ffb066",
         big="два бревна", cap="Огонь тлеет по щели до утра", top=620, w=1180,
         bgfx='<rect width="1080" height="1920" fill="#1a1230"/>'
              '<circle cx="540" cy="1380" r="420" fill="#3a2150" opacity="0.6"/>',
         fx=embers(34) + '<ellipse id="fireg" cx="352" cy="1210" rx="150" ry="110" fill="url(#glow)" opacity="0.55"/>'),
    dict(sid="s3", img="winter-walk_m5sd.svg", dur=4, bg="#eef3fb", fg="#241f3a", accent="#7a4dff",
         big="утро", cap="Земля греет снизу, как печь", top=560, w=1160,
         bgfx='<rect width="1080" height="1920" fill="#eef3fb"/>'
              '<circle cx="540" cy="520" r="380" fill="#dfe8fb" opacity="0.9"/>',
         fx=snow(80, 9)),
]


def main() -> None:
    hosts, start = [], 0
    for i, sc in enumerate(SCENES):
        (OUT / f"{sc['sid']}.html").write_text(TEMPLATE.format(**sc), encoding="utf-8")
        hosts.append(f'<div id="{sc["sid"]}" class="scene" data-composition-id="{sc["sid"]}" '
                     f'data-composition-src="compositions/{sc["sid"]}.html" data-start="{start}" '
                     f'data-duration="{sc["dur"]}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        start += sc["dur"]
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    Path("/root/video-gen/vector-anim/index.html").write_text(html, encoding="utf-8")
    print("ok", start)


if __name__ == "__main__":
    main()
