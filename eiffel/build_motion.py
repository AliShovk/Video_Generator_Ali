#!/usr/bin/env python3
"""Эйфелева башня: максимум движения, непрерывная озвучка. 42 с, 9:16."""
import random
from pathlib import Path

from scene import (DEFS, GROUND, IRON, IRON_D, IRON_L, SKY1, SUN, bird, cloud, ground,
                   person, scene_bg, tower, trees)

OUT = Path("/root/video-gen/eiffel/compositions")
OUT.mkdir(parents=True, exist_ok=True)


def svg(body):
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>')


def elevator(x, base, h=760):
    return (f'<g id="lift"><rect x="{x-16}" y="{base-h*0.55-20}" width="32" height="26" rx="6" fill="#e6402f"/>'
            f'<rect x="{x-10}" y="{base-h*0.55-14}" width="20" height="12" rx="3" fill="#fff3e2" opacity="0.85"/></g>')


def flag(x, y, s=1.0, color="#e6402f"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-2" y="-70" width="4" height="74" fill="{IRON_D}"/>'
            f'<path class="flag" d="M 2 -66 q 30 8 54 -4 q -6 22 0 40 q -24 12 -54 2 z" fill="{color}"/></g>')


def boat(x, y, s=1.0, color="#3f6fb5"):
    return (f'<g class="boat" transform="translate({x} {y}) scale({s})">'
            f'<path d="M -80 0 q 80 26 160 0 l -12 24 q -68 18 -136 0 z" fill="{color}"/>'
            f'<rect x="-34" y="-30" width="68" height="30" rx="8" fill="#f2efe8"/>'
            f'<rect x="-24" y="-24" width="20" height="16" rx="3" fill="#bfe4f8"/>'
            f'<rect x="2" y="-24" width="20" height="16" rx="3" fill="#bfe4f8"/>'
            f'<rect x="10" y="-52" width="8" height="24" fill="#8a5a34"/>'
            f'<path class="smoke" d="M 14 -56 q 10 -12 4 -22 q 14 4 8 -14" stroke="#e8eef4" stroke-width="7" fill="none" opacity="0.7"/></g>')


def crowd(n=16, seed=5, y=1680):
    r = random.Random(seed)
    out = []
    for i in range(n):
        x = r.uniform(20, 1060)
        s = r.uniform(0.85, 1.25)
        col = r.choice(["#2b3560", "#7a3f3f", "#3f6f5a", "#5a4a7a", "#8a6a3a"])
        cls = "walker walker-l" if i % 3 == 0 else "walker"
        out.append(f'<g class="{cls}" transform="translate({x} {y + r.uniform(-40, 60):.0f}) scale({s})">'
                   f'<circle cx="0" cy="-26" r="5" fill="#f2c39d"/>'
                   f'<rect x="-4" y="-21" width="8" height="14" rx="3" fill="{col}"/>'
                   f'<rect x="-4" y="-8" width="3" height="9" fill="#1f2740"/>'
                   f'<rect x="1" y="-8" width="3" height="9" fill="#1f2740"/></g>')
    return "".join(out)


def river(y=1740):
    return (f'<rect x="0" y="{y}" width="1080" height="{1920-y}" fill="#4f89b8"/>'
            f'<rect x="0" y="{y}" width="1080" height="12" fill="#3d729c"/>'
            + "".join(f'<ellipse class="wave" cx="{x}" cy="{y + 30 + (x % 4) * 22}" rx="{40 + x % 30}" ry="4" '
                      f'fill="#bfe0f5" opacity="0.5"/>' for x in range(40, 1080, 110)))


def scene1():
    b = ['<rect width="1080" height="1920" fill="url(#sky)"/>']
    b.append('<circle cx="880" cy="300" r="230" fill="url(#sunGlow)"/><circle cx="880" cy="300" r="66" fill="#ffd166"/>')
    b.append('<g class="rays" opacity="0.35">' + "".join(
        f'<line x1="880" y1="300" x2="{880 + 260 * __import__("math").cos(a)}" y2="{300 + 260 * __import__("math").sin(a)}" '
        f'stroke="#ffe9a8" stroke-width="9" stroke-linecap="round"/>' for a in [i * 0.785 for i in range(8)]) + '</g>')
    b.append(cloud(200, 260, 1.0, "cloud c1") + cloud(700, 170, 0.7, "cloud c2") + cloud(960, 380, 0.55, "cloud c3")
             + cloud(420, 120, 0.45, "cloud c4"))
    b.append(bird(300, 420, 1.0) + bird(360, 450, 0.8) + bird(250, 470, 0.7) + bird(430, 400, 0.6))
    b.append(ground(1560))
    b.append(trees(1560, 11))
    b.append(crowd(18))
    b.append(tower(540, 1560, 780, 320))
    b.append(flag(700, 1290, 0.9) + flag(380, 1290, 0.8, "#3f6fb5"))
    b.append(elevator(540, 1560, 780))
    b.append(river(1740))
    b.append(boat(250, 1800, 1.0) + boat(760, 1810, 0.85, "#c0392b"))
    return svg("".join(b))


def scene2():
    b = ['<rect width="1080" height="1920" fill="#f0e6d8"/>']
    b.append('<circle cx="820" cy="260" r="300" fill="url(#sunGlow)"/><circle class="sun" cx="820" cy="260" r="90" fill="#ffd166"/>')
    b.append('<g class="rays2" opacity="0.4">' + "".join(
        f'<line x1="820" y1="260" x2="{820 + 380 * __import__("math").cos(a)}" y2="{260 + 380 * __import__("math").sin(a)}" '
        f'stroke="#ffcf7a" stroke-width="14" stroke-linecap="round"/>' for a in [i * 0.7 for i in range(9)]) + '</g>')
    for i in range(0, 12):
        x = 60 + i * 90
        b.append(f'<line x1="{x}" y1="700" x2="{x}" y2="1800" stroke="{IRON_D}" stroke-width="22"/>')
    for j in range(0, 9):
        y = 760 + j * 120
        b.append(f'<line x1="40" y1="{y}" x2="1040" y2="{y}" stroke="{IRON}" stroke-width="18"/>')
        for k in range(0, 9):
            xx = 40 + k * 120
            b.append(f'<line x1="{xx}" y1="{y}" x2="{xx+60}" y2="{y-60}" stroke="{IRON_D}" stroke-width="7" opacity="0.65"/>')
            b.append(f'<line x1="{xx+60}" y1="{y}" x2="{xx}" y2="{y-60}" stroke="{IRON_D}" stroke-width="7" opacity="0.65"/>')
    r = random.Random(3)
    for i in range(40):
        b.append(f'<circle class="atom" cx="{r.uniform(80,1000):.0f}" cy="{r.uniform(800,1700):.0f}" '
                 f'r="{r.uniform(5,12):.1f}" fill="#e6402f" opacity="0.5"/>')
    b.append('<g class="sparks" opacity="0.8">' + "".join(
        f'<circle cx="{r.uniform(60,1020):.0f}" cy="{r.uniform(700,1800):.0f}" r="4" fill="#fff" opacity="0.8"/>' for _ in range(18)) + '</g>')
    return svg("".join(b))


def scene3():
    b = ['<rect width="1080" height="1920" fill="#eef6ff"/>']
    b.append(cloud(220, 240, 0.8, "cloud c1") + cloud(760, 180, 0.6, "cloud c2"))
    b.append(tower(420, 1780, 1180, 320))
    b.append('<rect x="800" y="380" width="150" height="1080" rx="14" fill="#ffffff" stroke="#c9d4de" stroke-width="4"/>')
    for i in range(0, 21):
        y = 1420 - i * 52
        ln = 46 if i % 5 == 0 else 26
        b.append(f'<line x1="800" y1="{y}" x2="{800+ln}" y2="{y}" stroke="{IRON_D}" stroke-width="3"/>')
        if i % 5 == 0:
            b.append(f'<text x="{800+ln+10}" y="{y+8}" font-family="Nunito, Arial" font-size="22" font-weight="800" fill="#4a3a2e">{i}</text>')
    b.append('<g id="marker"><rect x="788" y="1418" width="176" height="12" rx="6" fill="#e6402f"/>'
             '<text id="txt0" x="960" y="1432" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="#e6402f">0 см</text>'
             '<text id="txt15" x="960" y="1432" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="#e6402f" opacity="0">15 см</text></g>')
    b.append('<circle cx="880" cy="200" r="120" fill="url(#sunGlow)"/><circle class="sun" cx="880" cy="200" r="54" fill="#ffd166"/>')
    r = random.Random(8)
    b.append('<g class="heat">' + "".join(
        f'<path d="M {x} 1500 q 12 -30 0 -60 q -12 -30 0 -60" stroke="#ffd9a8" stroke-width="6" fill="none" opacity="0.5"/>'
        for x in range(120, 800, 90)) + '</g>')
    return svg("".join(b))


def scene4():
    b = [scene_bg(8)]
    b.append(tower(540, 1560, 780, 320))
    b.append(crowd(10, 12, 1700))
    b.append('<g id="painter1"><line x1="540" y1="880" x2="470" y2="1180" stroke="#3a3a3a" stroke-width="3"/>'
             '<circle cx="470" cy="1190" r="14" fill="#f2c39d"/><rect x="458" y="1202" width="24" height="30" rx="8" fill="#ffd166"/>'
             '<rect x="452" y="1232" width="36" height="10" rx="4" fill="#8a5a34"/>'
             '<path class="brush" d="M 452 1240 l -26 26" stroke="#8a5a34" stroke-width="8" stroke-linecap="round"/></g>')
    b.append('<g id="painter2"><line x1="540" y1="930" x2="620" y2="1260" stroke="#3a3a3a" stroke-width="3"/>'
             '<circle cx="620" cy="1270" r="14" fill="#f2c39d"/><rect x="608" y="1282" width="24" height="30" rx="8" fill="#ffd166"/>'
             '<rect x="602" y="1312" width="36" height="10" rx="4" fill="#8a5a34"/>'
             '<path class="brush" d="M 638 1322 l 22 22" stroke="#8a5a34" stroke-width="8" stroke-linecap="round"/></g>')
    b.append('<g id="bucket"><rect x="250" y="1400" width="70" height="62" rx="10" fill="#8a5a34"/>'
             '<ellipse cx="285" cy="1400" rx="35" ry="10" fill="#a9713f"/></g>')
    b.append('<g class="drips">' + "".join(
        f'<circle class="drip" cx="{320 + i*18}" cy="{1360 - i*10}" r="5" fill="#e6402f"/>' for i in range(6)) + '</g>')
    return svg("".join(b))


SCENES = {"s1": (scene1, 11), "s2": (scene2, 11), "s3": (scene3, 11), "s4": (scene4, 9)}
HEAD = {
    "s1": [("15 СМ", "#e6402f"), ("ЗА ОДИН ДЕНЬ", "#20242c")],
    "s2": [("МЕТАЛЛ", "#20242c"), ("РАСШИРЯЕТСЯ", "#e6402f")],
    "s3": [("ВЫШЕ ДНЁМ,", "#20242c"), ("НИЖЕ НОЧЬЮ", "#e6402f")],
    "s4": [("КРАСЯТ", "#20242c"), ("КАЖДЫЕ 7 ЛЕТ", "#e6402f")],
}


def page(sid, body, dur):
    head = "".join(
        f'<text class="hl" x="56" y="{228 + i*96}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="78" font-weight="900" letter-spacing="-1">{s}</text>' for i, (s, c) in enumerate(HEAD[sid]))
    body = body.replace('</svg>', head + '</svg>')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#bfe4f8; }}
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.06, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo("#{sid} .hl", {{ opacity:0, y:26 }}, {{ opacity:1, y:0, duration:0.5, stagger:0.14, ease:"power3.out" }}, 0.15);
    tl.to(".cloud", {{ x:"+=90", duration:14, ease:"none" }}, 0);
    tl.to(".c2", {{ x:"-=120", duration:18, ease:"none" }}, 0);
    tl.to(".c3", {{ x:"+=70", duration:11, ease:"none" }}, 0);
    tl.to(".c4", {{ x:"-=60", duration:16, ease:"none" }}, 0);
    tl.to(".bird", {{ x:"+=260", y:"-=30", duration:12, ease:"none" }}, 0);
    tl.to(".bird", {{ y:"+=8", duration:0.8, yoyo:true, repeat:14, ease:"sine.inOut" }}, 0);
    tl.to(".walker", {{ x:"+=46", duration:9, ease:"none" }}, 0);
    tl.to(".walker-l", {{ x:"-=60", duration:9, ease:"none" }}, 0);
    tl.to(".boat", {{ x:"+=240", duration:11, ease:"none" }}, 0);
    tl.to(".smoke", {{ opacity:0.15, duration:0.9, yoyo:true, repeat:11 }}, 0);
    tl.to(".wave", {{ x:"+=24", duration:2.4, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0);
    tl.to(".flag", {{ skewX:-10, duration:1.1, yoyo:true, repeat:9, ease:"sine.inOut" }}, 0);
    tl.to(".rays", {{ rotation:14, svgOrigin:"880 300", duration:11, ease:"none" }}, 0);
    tl.to(".rays2", {{ rotation:-16, svgOrigin:"820 260", duration:11, ease:"none" }}, 0);
    tl.to(".atom", {{ y:-10, duration:0.45, yoyo:true, repeat:23, stagger:{{each:0.03, from:"random"}}, ease:"sine.inOut" }}, 0.2);
    tl.to(".atom", {{ x:"+=6", duration:0.7, yoyo:true, repeat:15, stagger:{{each:0.04, from:"random"}}, ease:"sine.inOut" }}, 0.2);
    tl.to(".sparks", {{ opacity:0.25, duration:0.5, yoyo:true, repeat:20 }}, 0);
    tl.to(".heat", {{ y:-18, duration:1.4, yoyo:true, repeat:7, ease:"sine.inOut" }}, 0);
    tl.to(".sun", {{ scale:1.04, transformOrigin:"50% 50%", duration:2.2, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0);
    tl.to("#lift", {{ y:-330, duration:7, ease:"sine.inOut" }}, 0.5);
    tl.to("#painter1", {{ y:-70, duration:3.2, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0.3);
    tl.to("#painter2", {{ y:-100, duration:3.8, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0.7);
    tl.to(".brush", {{ rotate:16, transformOrigin:"0% 0%", duration:0.9, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0.4);
    tl.to("#bucket", {{ rotation:3, duration:1.2, yoyo:true, repeat:6, ease:"sine.inOut" }}, 0.4);
    tl.to(".drip", {{ y:"+=90", opacity:0, duration:1.6, stagger:0.3, repeat:4, ease:"power1.in" }}, 0.6);
    {"tl.to('#marker', { y:-780, duration:6.0, ease:'power1.inOut' }, 0.8); tl.to('#txt0', { opacity:0, duration:0.3 }, 4.4); tl.to('#txt15', { opacity:1, duration:0.3 }, 4.4);".replace("'", '"') if sid == "s3" else ""}
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
    Path("/root/video-gen/eiffel/index.html").write_text(html, encoding="utf-8")
    print("ok", start)


if __name__ == "__main__":
    build()
