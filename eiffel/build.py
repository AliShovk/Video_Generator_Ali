#!/usr/bin/env python3
"""Сборка «Эйфелева башня растёт за день»."""
import random
from pathlib import Path

from scene import (DEFS, IRON, IRON_D, IRON_L, SKY1, SUN, cloud, ground, person, scene_bg, tower, trees, bird)

OUT = Path("/root/video-gen/eiffel/compositions")
OUT.mkdir(parents=True, exist_ok=True)


def svg(body):
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>')


def elevator(x, base, h=760):
    return (f'<g id="lift"><rect x="{x-16}" y="{base-h*0.55-20}" width="32" height="26" rx="6" fill="#e6402f"/>'
            f'<rect x="{x-10}" y="{base-h*0.55-14}" width="20" height="12" rx="3" fill="#fff3e2" opacity="0.85"/></g>')


def scene1():
    b = [scene_bg(10)]
    b.append(tower(540, 1560, 780, 320))
    b.append(elevator(540, 1560, 780))
    return svg("".join(b))


def scene2():
    # крупный план решётки
    b = ['<rect width="1080" height="1920" fill="#f0e6d8"/>']
    b.append('<circle cx="820" cy="260" r="300" fill="url(#sunGlow)"/>')
    b.append('<circle cx="820" cy="260" r="90" fill="#ffd166"/>')
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
    # "атомы"
    for i in range(26):
        r = random.Random(i)
        b.append(f'<circle class="atom" cx="{r.uniform(80,1000):.0f}" cy="{r.uniform(800,1700):.0f}" r="{r.uniform(6,12):.1f}" fill="#e6402f" opacity="0.55"/>')
    # лучи
    for i in range(5):
        b.append(f'<line class="ray" x1="{700+i*30}" y1="320" x2="{420+i*40}" y2="900" stroke="#ffcf7a" stroke-width="12" opacity="0.35" stroke-linecap="round"/>')
    return svg("".join(b))


def scene3():
    b = ['<rect width="1080" height="1920" fill="#eef6ff"/>']
    b.append(tower(420, 1700, 1000, 300))
    # линейка
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
    b.append('<circle cx="880" cy="200" r="120" fill="url(#sunGlow)"/><circle cx="880" cy="200" r="54" fill="#ffd166"/>')
    return svg("".join(b))


def scene4():
    b = [scene_bg(8)]
    b.append(tower(540, 1560, 780, 320))
    # маляры на верёвках
    b.append('<g id="painter1"><line x1="540" y1="880" x2="470" y2="1180" stroke="#3a3a3a" stroke-width="3"/>'
             '<circle cx="470" cy="1190" r="14" fill="#f2c39d"/><rect x="458" y="1202" width="24" height="30" rx="8" fill="#ffd166"/>'
             '<rect x="452" y="1232" width="36" height="10" rx="4" fill="#8a5a34"/></g>')
    b.append('<g id="painter2"><line x1="540" y1="930" x2="620" y2="1260" stroke="#3a3a3a" stroke-width="3"/>'
             '<circle cx="620" cy="1270" r="14" fill="#f2c39d"/><rect x="608" y="1282" width="24" height="30" rx="8" fill="#ffd166"/>'
             '<rect x="602" y="1312" width="36" height="10" rx="4" fill="#8a5a34"/></g>')
    # ведро и кисти
    b.append('<g id="bucket"><rect x="250" y="1400" width="70" height="62" rx="10" fill="#8a5a34"/>'
             '<ellipse cx="285" cy="1400" rx="35" ry="10" fill="#a9713f"/>'
             '<rect x="300" y="1360" width="8" height="52" rx="3" fill="#6b4a2f" transform="rotate(12 304 1386)"/></g>')
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo("#{sid} .hl", {{ opacity:0, y:26 }}, {{ opacity:1, y:0, duration:0.5, stagger:0.16, ease:"power3.out" }}, 0.2);
    tl.to(".cloud", {{ x:"+=70", duration:14, ease:"none" }}, 0);
    tl.to(".c2", {{ x:"-=90", duration:18, ease:"none" }}, 0);
    tl.to(".c3", {{ x:"+=50", duration:11, ease:"none" }}, 0);
    tl.to(".bird", {{ x:"+=180", y:"-=26", duration:12, ease:"none" }}, 0);
    tl.to(".bird", {{ y:"+=10", duration:0.9, yoyo:true, repeat:12, ease:"sine.inOut" }}, 0);
    tl.to(".walker", {{ x:"+=26", duration:9, ease:"none" }}, 0);
    tl.to(".atom", {{ y:-8, duration:0.5, yoyo:true, repeat:21, stagger:{{each:0.04, from:"random"}}, ease:"sine.inOut" }}, 0.2);
    tl.to(".ray", {{ opacity:0.15, duration:0.8, yoyo:true, repeat:12, stagger:0.1 }}, 0);
    tl.to("#lift", {{ y:-330, duration:7, ease:"sine.inOut" }}, 0.5);
    tl.to("#painter1", {{ y:-60, duration:3.4, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0.4);
    tl.to("#painter2", {{ y:-90, duration:4.0, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0.8);
    tl.to("#bucket", {{ rotation:3, duration:1.4, yoyo:true, repeat:5, ease:"sine.inOut" }}, 0.5);
    {"tl.to('#marker', { y:-780, duration:5.2, ease:'power1.inOut' }, 1.0);".replace("'", '"')
     if sid == "s3" else ""}
    {"tl.to('#txt0', { opacity:0, duration:0.3 }, 4.2);tl.to('#txt15', { opacity:1, duration:0.3 }, 4.2);".replace("'", '"')
     if sid == "s3" else ""}
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
