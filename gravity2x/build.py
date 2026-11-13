#!/usr/bin/env python3
"""«Гравитация вдвое сильнее» — персонаж 6 голов, шаг из четырёх поз."""
import json
import random
from pathlib import Path

from rig_kid import kid

OUT = Path("/root/video-gen/gravity2x/compositions")
OUT.mkdir(parents=True, exist_ok=True)

DEFS = """<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8fcdf2"/><stop offset="0.6" stop-color="#cfeafd"/><stop offset="1" stop-color="#eaf7ff"/>
  </linearGradient>
  <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#6cc24a"/><stop offset="1" stop-color="#4ea336"/>
  </linearGradient>
  <radialGradient id="sun" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#fff3b0" stop-opacity="0.9"/><stop offset="1" stop-color="#fff3b0" stop-opacity="0"/>
  </radialGradient>
</defs>"""


def bg(elements=""):
    b = ['<rect width="1080" height="1920" fill="url(#sky)"/>',
         '<circle cx="880" cy="260" r="180" fill="url(#sun)"/>',
         '<circle cx="880" cy="260" r="70" fill="#ffe08a"/>',
         '<g opacity="0.9"><ellipse cx="220" cy="300" rx="90" ry="38" fill="#fff"/><ellipse cx="170" cy="312" rx="55" ry="26" fill="#fff"/><ellipse cx="280" cy="314" rx="62" ry="28" fill="#fff"/></g>',
         '<g opacity="0.75"><ellipse cx="700" cy="180" rx="70" ry="30" fill="#fff"/><ellipse cx="660" cy="192" rx="44" ry="20" fill="#fff"/></g>',
         '<rect x="40" y="1120" width="220" height="320" rx="14" fill="#e9e2d2"/><path d="M 20 1120 L 150 1030 L 280 1120 Z" fill="#b0503f"/>',
         '<rect x="820" y="1160" width="220" height="280" rx="14" fill="#dfe7ef"/><path d="M 800 1160 L 930 1080 L 1060 1160 Z" fill="#8a5a4a"/>',
         '<rect x="0" y="1400" width="1080" height="520" fill="url(#grass)"/>',
         '<path d="M 0 1420 Q 300 1370 560 1410 Q 840 1450 1080 1400 L 1080 1480 L 0 1480 Z" fill="#7ad155" opacity="0.7"/>']
    return "".join(b) + elements


SCALE = 0.75
GROUND_PX = 1560
MOVER_Y = round(GROUND_PX / SCALE - 191)   # ступни на траве

# позы шага: contact → down → passing → up (по одной ноге на полный цикл)
LEG_POSES = [(24, 0.10), (12, 0.13), (-2, 0.16), (-18, 0.13),
             (-24, 0.10), (-12, 0.13), (0, 0.16), (16, 0.13), (24, 0.10)]
KNEE_POSES = [(8, 0.10), (30, 0.13), (55, 0.16), (20, 0.13),
              (8, 0.10), (32, 0.13), (48, 0.16), (16, 0.13), (8, 0.10)]
ARM_POSES = [(-26, 0.10), (-12, 0.13), (4, 0.16), (20, 0.13),
             (26, 0.10), (12, 0.13), (-4, 0.16), (-20, 0.13), (-26, 0.10)]
ELBOW_POSES = [(10, 0.10), (16, 0.13), (24, 0.16), (20, 0.13),
               (12, 0.10), (18, 0.13), (22, 0.16), (14, 0.13), (10, 0.10)]
BOB_POSES = [(0, 0.10), (-6, 0.13), (-2, 0.16), (4, 0.13),
             (0, 0.10), (-6, 0.13), (-2, 0.16), (4, 0.13), (0, 0.10)]


def kf(values, ease="sine.inOut"):
    return json.dumps([{"rotation": v, "duration": d, "ease": ease} for v, d in values])


def kf_y(values):
    return json.dumps([{"y": v, "duration": d, "ease": "sine.inOut"} for v, d in values])


def walk(start=0.2, cycles=5, amp_scale=1.0, slow=1.0):
    leg = [(v * amp_scale, d * slow) for v, d in LEG_POSES]
    arm = [(v * amp_scale, d * slow) for v, d in ARM_POSES]
    knee = [(v, d * slow) for v, d in KNEE_POSES]
    elb = [(v, d * slow) for v, d in ELBOW_POSES]
    bob = [(v, d * slow) for v, d in BOB_POSES]
    step = 0.52 * slow
    return f"""
tl.to("#legNear", {{keyframes: {kf(leg)}, repeat: {cycles-1}}}, {start});
tl.to("#legFar",  {{keyframes: {kf(leg)}, repeat: {cycles-1}}}, {start + step});
tl.to("#kneeNear", {{keyframes: {kf(knee)}, repeat: {cycles-1}}}, {start});
tl.to("#kneeFar",  {{keyframes: {kf(knee)}, repeat: {cycles-1}}}, {start + step});
tl.to("#armNear",  {{keyframes: {kf(arm)}, repeat: {cycles-1}}}, {start});
tl.to("#armFar",   {{keyframes: {kf(arm)}, repeat: {cycles-1}}}, {start + step});
tl.to("#elbowNear",{{keyframes: {kf(elb)}, repeat: {cycles-1}}}, {start});
tl.to("#elbowFar", {{keyframes: {kf(elb)}, repeat: {cycles-1}}}, {start + step});
tl.to("#torso", {{keyframes: {kf_y(bob)}, repeat: {cycles-1}}}, {start});
"""


TL_SET = f"""
gsap.set("#mover", {{ x: %(x0)s, y: {MOVER_Y} }});
gsap.set("#legNear", {{ x: 7, y: 0 }});
gsap.set("#legFar", {{ x: -7, y: 0 }});
gsap.set("#kneeNear", {{ x: 0, y: 99 }});
gsap.set("#kneeFar", {{ x: 0, y: 98 }});
gsap.set("#torso", {{ x: 0, y: 0 }});
gsap.set("#head", {{ x: 2, y: -162 }});
gsap.set("#armNear", {{ x: 16, y: -112 }});
gsap.set("#armFar", {{ x: -6, y: -112 }});
gsap.set("#elbowNear", {{ x: 0, y: 90 }});
gsap.set("#elbowFar", {{ x: 0, y: 88 }});
"""


IDS = ["mover","legNear","legFar","kneeNear","kneeFar","torso","head",
       "armNear","armFar","elbowNear","elbowFar","ballG"]


def sanitize(js: str, name: str) -> str:
    for i in IDS:
        js = js.replace(f'"#{i}"', f'"#{name}_{i}"')
    return js


def scene_html(name, dur, body, tl_extra, caption, x0=-200):
    body = body.replace('id="', f'id="{name}_')
    tl_extra = sanitize(tl_extra, name)
    page = f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#bfe4f8; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
    .cap {{ position:absolute; left:44px; right:44px; top:150px; text-align:center;
      font:900 50px/1.15 "Nunito", Arial, sans-serif; color:#1f2740;
      background:rgba(255,255,255,0.86); border-radius:26px; padding:22px 26px; }}
  </style>
  <div id="root" data-composition-id="{name}" data-width="1080" data-height="1920">
    <div class="clip" id="{name}-clip" data-start="0" data-duration="{dur}">
      <div id="{name}-in">
        <svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>
        <div class="cap" id="{name}-cap">{caption}</div>
      </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{name} .world", {{ scale:1.0 }}, {{ scale:1.04, duration:{dur}, ease:"none" }}, 0);
    {sanitize(TL_SET % {"x0": x0}, name)}
    {tl_extra}
    tl.fromTo("#{name}-cap", {{ opacity:0, y:18 }}, {{ opacity:1, y:0, duration:0.5 }}, 0.2);
    window.__timelines["{name}"] = tl;
  </script>
</template>
"""
    (OUT / f"{name}.html").write_text(page, encoding="utf-8")


def build():
    kid_svg = f'<g transform="scale({SCALE})">{kid()}</g>'

    s1 = bg(kid_svg)
    scene_html("s1", 6, s1, walk() + '\ntl.to("#mover", { x: 330, duration: 5.6, ease:"none" }, 0.2);',
               "Что, если гравитация станет <b>вдвое сильнее</b>?")

    s2 = bg(kid_svg)
    scene_html("s2", 6, s2, walk(slow=1.35, cycles=3, amp_scale=0.75) +
               '\ntl.to("#mover", { x: 190, duration: 5.4, ease:"none" }, 0.2);'
               '\ntl.to("#torso", { rotation: 12, duration: 0.8 }, 0.3);',
               "Вес удваивается: каждый шаг — с рюкзаком", x0=-140)

    s3 = bg(kid_svg)
    jump = f"""
tl.to("#mover", {{ y: {MOVER_Y+34}, duration:0.5, ease:"power2.in" }}, 0.5);
tl.to("#kneeNear", {{ rotation: 58, duration:0.5 }}, 0.5);
tl.to("#kneeFar", {{ rotation: 58, duration:0.5 }}, 0.5);
tl.to("#armNear", {{ rotation: 30, duration:0.5 }}, 0.5);
tl.to("#mover", {{ y: {MOVER_Y-110}, duration:0.34, ease:"power2.out" }}, 1.0);
tl.to("#kneeNear", {{ rotation: 16, duration:0.34 }}, 1.0);
tl.to("#kneeFar", {{ rotation: 16, duration:0.34 }}, 1.0);
tl.to("#mover", {{ y: {MOVER_Y}, duration:0.42, ease:"power2.in" }}, 1.35);
tl.to("#kneeNear", {{ rotation: 40, duration:0.2 }}, 1.7);
tl.fromTo("#ballG", {{ y: 0 }}, {{ y: 900, duration:0.62, ease:"power2.in" }}, 1.05);
"""
    scene_html("s3", 6, s3, jump, "Прыжок станет вдвое ниже", x0=60)

    s4 = bg(kid_svg)
    dizzy = f"""
tl.to("#torso", {{ rotation: 10, duration:1.4, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0.4);
tl.to("#head", {{ rotation: -9, duration:1.2, yoyo:true, repeat:3, ease:"sine.inOut" }}, 0.5);
tl.to("#mover", {{ y: {MOVER_Y+44}, duration:1.6, ease:"sine.inOut" }}, 2.0);
tl.to("#legNear", {{ rotation: -86, duration:1.0 }}, 2.2);
tl.to("#legFar", {{ rotation: -94, duration:1.0 }}, 2.2);
tl.to("#kneeNear", {{ rotation: 128, duration:1.0 }}, 2.2);
tl.to("#kneeFar", {{ rotation: 138, duration:1.0 }}, 2.2);
tl.to("#armNear", {{ rotation: -26, duration:0.8 }}, 2.3);
"""
    scene_html("s4", 6, s4, dizzy, "Сердцу труднее гнать кровь вверх", x0=60)

    s5 = bg(kid_svg)
    final = f"""
tl.to("#mover", {{ y: {MOVER_Y+44}, duration:0.7 }}, 0.2);
tl.to("#legNear", {{ rotation: -86, duration:0.7 }}, 0.2);
tl.to("#legFar", {{ rotation: -94, duration:0.7 }}, 0.2);
tl.to("#kneeNear", {{ rotation: 128, duration:0.7 }}, 0.2);
tl.to("#kneeFar", {{ rotation: 138, duration:0.7 }}, 0.2);
tl.to("#torso", {{ rotation: 6, duration:2.2, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 0.9);
tl.to("#armNear", {{ rotation: -24, duration:2.0, yoyo:true, repeat:-1, ease:"sine.inOut" }}, 1.0);
"""
    scene_html("s5", 6, s5, final, "Вдвое тяжелее — <b>навсегда</b>", x0=60)

    hosts, start = [], 0
    for i, n in enumerate(["s1", "s2", "s3", "s4", "s5"]):
        hosts.append(f'<div id="{n}" class="scene" data-composition-id="{n}" data-composition-src="compositions/{n}.html" '
                     f'data-start="{start}" data-duration="6" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        start += 6
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    Path("/root/video-gen/gravity2x/index.html").write_text(html, encoding="utf-8")
    print("ok", start)


if __name__ == "__main__":
    build()
