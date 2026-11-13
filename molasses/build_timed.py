#!/usr/bin/env python3
"""Сборка ролика с движением, привязанным к словам озвучки."""
import json
import math
from pathlib import Path

from story import PHRASES, SCENE_ORDER

ROOT = Path("/root/video-gen/molasses")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

NIGHT = "#101a20"
SKY = "#1b2a33"
STEEL = "#8d99a3"
STEEL_D = "#5f6b74"
MOL = "#4a2b12"
MOL_L = "#6b3f1a"
CREAM = "#f0e6d2"
RED = "#c0392b"
GOLD = "#e0a33e"

DEFS = f"""
<defs>
  <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#243642"/><stop offset="1" stop-color="#0f181e"/></linearGradient>
  <linearGradient id="molG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MOL_L}"/><stop offset="1" stop-color="#2a1808"/></linearGradient>
  <linearGradient id="steelG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6d7881"/><stop offset="0.45" stop-color="#a9b4bd"/><stop offset="1" stop-color="#5a636b"/></linearGradient>
</defs>
"""

T = json.load(open(ROOT / "timings.json"))
PHRASE = {p["id"]: p for p in T["phrases"]}
TOTAL = T["total"]


def scene_bounds():
    starts = {}
    for sid in SCENE_ORDER:
        starts[sid] = min(p["start"] for p in T["phrases"] if p["scene"] == sid)
    ordered = sorted(starts.items(), key=lambda kv: kv[1])
    bounds = {}
    for i, (sid, st) in enumerate(ordered):
        end = ordered[i + 1][1] if i + 1 < len(ordered) else TOTAL
        bounds[sid] = (st, round(end - st, 3))
    return bounds


BOUNDS = scene_bounds()


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def head(lines, y0=210):
    return "".join(
        f'<text class="hl" x="56" y="{y0 + i*92}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="70" font-weight="900">{s}</text>' for i, (s, c) in enumerate(lines))


# ---------------------------------------------------------------- s1
def s1():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append('<rect x="0" y="1440" width="1080" height="480" fill="#161f26"/>')
    b.append('<g class="speed" opacity="0">' + "".join(
        f'<rect x="{40 + i*90}" y="{900 + (i%4)*70}" width="{120 + i*14}" height="7" rx="3" fill="#e0a33e" opacity="0.75"/>'
        for i in range(9)) + '</g>')
    b.append('<g class="wave"><path d="M -260 1500 q 300 -420 620 -300 q 220 80 460 -60 l 0 660 l -1080 0 z" fill="url(#molG)"/>'
             '<path d="M -260 1500 q 300 -420 620 -300 q 220 80 460 -60" stroke="#8a5a2a" stroke-width="12" fill="none"/></g>')
    b.append('<g class="crest" opacity="0"><rect x="470" y="1010" width="300" height="76" rx="12" fill="#0e1418" opacity="0.85"/>'
             f'<text x="620" y="1064" font-family="Nunito, Arial" font-size="46" font-weight="900" fill="{GOLD}" text-anchor="middle">8 МЕТРОВ</text></g>')
    b.append('<g class="burst" opacity="0.35">' + "".join(
        f'<circle cx="{300 + i*40}" cy="{1200 - (i%3)*50}" r="{8 + i%4*4}" fill="{MOL_L}"/>' for i in range(8)) + '</g>')
    for i, x in enumerate((740, 830, 910)):
        b.append(f'<g class="runner" transform="translate({x} {1780}) scale(1.9)">'
                 f'<circle cx="0" cy="-52" r="9" fill="#e8c9a8"/>'
                 f'<rect x="-9" y="-44" width="18" height="30" rx="6" fill="#f0e6d2"/>'
                 f'<rect x="-9" y="-14" width="6" height="18" fill="#1a1f24"/><rect x="3" y="-14" width="6" height="18" fill="#1a1f24"/></g>')
    b.append(head([("ВОЛНА", GOLD), ("ПАТОКИ", "#ffffff")]))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append('<rect x="0" y="1560" width="1080" height="360" fill="#16212a"/>')
    b.append('<g class="cold" opacity="0" transform="translate(0 -30)"><rect x="830" y="300" width="190" height="64" rx="10" fill="#0e1418" opacity="0.8"/>'
             f'<text x="925" y="346" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="#8fd4ff" text-anchor="middle">−14 °C</text></g>')
    b.append('<g class="snow" opacity="0.25">' + "".join(
        f'<circle cx="{(i*97) % 1080}" cy="{(i*163) % 1500}" r="{3 + i%3}" fill="#dff0ff" opacity="0.7"/>' for i in range(40)) + '</g>')
    b.append('<g class="tankwrap" opacity="1" transform="translate(0 0)"><g>'
             f'<ellipse cx="540" cy="560" rx="250" ry="34" fill="{STEEL}"/>'
             f'<rect x="290" y="560" width="500" height="1000" fill="url(#steelG)"/>'
             f'<ellipse cx="540" cy="1560" rx="250" ry="34" fill="{STEEL_D}"/>'
             + "".join(f'<circle cx="{320 + (i%10)*50}" cy="{600 + (i//10)*60}" r="5" fill="{STEEL_D}"/>' for i in range(120))
             + '</g></g>')
    b.append('<rect class="liquid" x="290" y="1560" width="500" height="0" fill="url(#molG)" opacity="0.92"/>')
    b.append('<g class="hmark" opacity="0"><line x1="150" y1="560" x2="150" y2="1560" stroke="#ffffff" stroke-width="4"/>'
             f'<text x="120" y="1060" font-family="Nunito, Arial" font-size="44" font-weight="900" fill="#ffffff" text-anchor="middle" transform="rotate(-90 120 1060)">15 М</text></g>')
    b.append('<g class="litres" opacity="0"><rect x="640" y="1180" width="330" height="80" rx="10" fill="#0e1418" opacity="0.85"/>'
             f'<text x="805" y="1236" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{GOLD}" text-anchor="middle">9 МЛН ЛИТРОВ</text></g>')
    b.append(head([("БАК", GOLD), ("В ПОРТУ", "#ffffff")]))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = ['<rect width="1080" height="1920" fill="#0d1519"/>']
    b.append('<g class="zoom"><g class="shake">')
    b.append(f'<rect x="0" y="300" width="1080" height="1620" fill="url(#steelG)"/>')
    b.append('<g>' + "".join(f'<circle cx="{60 + (i%12)*88}" cy="{960 + (i//12)*80}" r="6" fill="{STEEL_D}"/>' for i in range(84)) + '</g>')
    b.append(f'<path class="crackbig" opacity="0.15" d="M 470 340 l 40 180 l -26 160 l 52 160 l -18 200 l 44 190" '
             f'stroke="{RED}" stroke-width="16" fill="none"/>')
    b.append('</g></g>')
    b.append('<g class="spray" opacity="0">' + "".join(
        f'<ellipse cx="{500 + i*22}" cy="{520 - (i%4)*40}" rx="{18 + i%5*8}" ry="{12 + i%3*6}" fill="{MOL_L}"/>' for i in range(10)) + '</g>')
    b.append('<g class="barrel"><ellipse cx="220" cy="1820" rx="70" ry="24" fill="#5a3a1e"/>'
             '<rect x="150" y="1700" width="140" height="60" fill="#6b4a2a"/><ellipse cx="220" cy="1700" rx="70" ry="22" fill="#7a5738"/></g>')
    b.append(head([("МЕТАЛЛ", "#ffffff"), ("УСТАЛ", RED)]))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append('<rect x="0" y="1500" width="1080" height="420" fill="#1a242c"/>')
    for i in range(6):
        b.append(f'<g class="block" opacity="0.35"><rect x="{40 + i*172}" y="{1180 - (i%3)*40}" width="150" height="{320 + (i%3)*40}" fill="#2a3a44"/>'
                 + "".join(f'<rect x="{54 + i*172 + c*40}" y="{1210 - (i%3)*40 + r*70}" width="24" height="34" fill="#ffd98a" opacity="0.5"/>'
                           for r in range(3) for c in range(3)) + '</g>')
    b.append('<g class="wave4"><path d="M -300 1560 q 340 -520 700 -380 q 260 100 520 -80 l 0 820 l -1080 0 z" fill="url(#molG)"/></g>')
    b.append('<g class="railfall"><rect x="0" y="880" width="1080" height="26" fill="#46525c"/>'
             + "".join(f'<rect x="{60 + i*120}" y="900" width="14" height="640" fill="#3a4650"/>' for i in range(9)) + '</g>')
    b.append('<g class="car"><rect x="700" y="1500" width="180" height="80" rx="14" fill="#8a2f2a"/>'
             '<circle cx="740" cy="1584" r="22" fill="#1a1f24"/><circle cx="840" cy="1584" r="22" fill="#1a1f24"/></g>')
    for i, x in enumerate((260, 360, 460)):
        b.append(f'<g class="rescuer" transform="translate({x} 1780) scale(1.6)">'
                 f'<circle cx="0" cy="-52" r="9" fill="#e8c9a8"/><rect x="-9" y="-44" width="18" height="34" rx="6" fill="#2b6f8a"/>'
                 f'<rect x="-9" y="-10" width="6" height="16" fill="#1a1f24"/><rect x="3" y="-10" width="6" height="16" fill="#1a1f24"/></g>')
    b.append(head([("6", GOLD), ("КВАРТАЛОВ", "#ffffff")]))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = ['<rect width="1080" height="1920" fill="#0f181d"/>']
    b.append('<rect x="60" y="520" width="960" height="1000" rx="12" fill="#efe6d2"/>')
    b.append('<text x="540" y="640" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="#5a4a36" text-anchor="middle">ИТОГ</text>')
    b.append('<g class="n21" opacity="1" transform-origin="540 860"><text x="540" y="900" font-family="Nunito, Arial" font-size="240" font-weight="900" fill="#c0392b" text-anchor="middle">21</text>'
             '<text x="540" y="960" font-family="Nunito, Arial" font-size="40" font-weight="800" fill="#2a2118" text-anchor="middle">погибший</text></g>')
    b.append('<g class="n150" opacity="1" transform-origin="540 1150"><text x="540" y="1180" font-family="Nunito, Arial" font-size="150" font-weight="900" fill="#2a2118" text-anchor="middle">150</text>'
             '<text x="540" y="1240" font-family="Nunito, Arial" font-size="38" font-weight="800" fill="#2a2118" text-anchor="middle">раненых</text></g>')
    b.append('<g class="money" opacity="0" transform="translate(0 30)"><rect x="150" y="1330" width="780" height="110" rx="10" fill="#dccfb4"/>'
             '<text x="540" y="1400" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="#4a3a28" text-anchor="middle">600 000 $ ВЫПЛАТ</text></g>')
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = ['<rect width="1080" height="1920" fill="#eef2f4"/>']
    b.append('<g class="blueprint" opacity="0.15">' + "".join(
        f'<line x1="0" y1="{i*60}" x2="1080" y2="{i*60}" stroke="#5b86a8" stroke-width="1"/>' for i in range(32)) + '</g>')
    b.append('<g class="need" opacity="0" transform="translate(-30 0)"><text x="120" y="640" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="#20303a">НУЖНО 25 ММ</text>'
             f'<rect x="120" y="680" width="300" height="260" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/></g>')
    b.append('<g class="was" opacity="0" transform="translate(-30 0)"><text x="620" y="640" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="#c0392b">БЫЛО 12 ММ</text>'
             f'<rect class="wasrect" x="620" y="680" width="300" height="260" fill="url(#steelG)" stroke="{RED}" stroke-width="4"/></g>')
    b.append('<g class="minus" opacity="0"><text x="540" y="1060" font-family="Nunito, Arial" font-size="120" font-weight="900" fill="#c0392b" text-anchor="middle">×2</text>'
             '<text x="540" y="1120" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="#5a4a36" text-anchor="middle">тоньше нормы</text></g>')
    b.append('<g class="cracks6" opacity="0"><path d="M 660 720 l 26 46 l -14 40 l 30 36" stroke="#c0392b" stroke-width="7" fill="none"/>'
             '<path d="M 760 800 l 24 40 l -12 34" stroke="#c0392b" stroke-width="6" fill="none"/></g>')
    b.append('<g class="paint" opacity="0"><rect x="694" y="700" width="52" height="230" fill="#6b4227"/></g>')
    b.append('<g class="paintbrush" transform="translate(300 760)"><rect x="-90" y="-16" width="120" height="32" rx="10" fill="#8a5a34"/>'
             '<rect x="20" y="-12" width="80" height="24" rx="6" fill="#4a2b12"/></g>')
    b.append('<g class="stamp" opacity="0" transform="translate(-100 0)"><rect x="180" y="1330" width="720" height="180" rx="12" fill="none" stroke="#1f6f4a" stroke-width="9"/>'
             '<text x="540" y="1420" font-family="Nunito, Arial" font-size="46" font-weight="900" fill="#1f6f4a" text-anchor="middle">ОБЯЗАТЕЛЬНЫЙ РАСЧЁТ</text>'
             '<text x="540" y="1478" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="#1f6f4a" text-anchor="middle">ПРОЧНОСТИ · США, 1919+</text></g>')
    b.append('<g class="yrs" opacity="0"><text x="540" y="1150" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="#5a4a36" text-anchor="middle">ТРЕЩИНЫ ВИДЕЛИ ДВА ГОДА</text></g>')
    b.append(head([("МОЖНО БЫЛО", "#20303a"), ("ИЗБЕЖАТЬ", RED)]))
    return svg("".join(b))


SCENE_FN = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6)
HEADLINE = dict(s1=True, s2=True, s3=True, s4=True, s5=False, s6=True)


def cue_lines(sid):
    out = []
    for ph in PHRASES:
        if ph["scene"] != sid:
            continue
        st = PHRASE[ph["id"]]["start"]
        local = st - BOUNDS[ph["scene"]][0]
        for sel, props, off, dur in ph["cues"]:
            props = dict(props)
            props.setdefault("duration", dur)
            props.setdefault("ease", "power2.out")
            body = ", ".join(f'{k}:{json.dumps(v) if isinstance(v, str) else v}' for k, v in props.items())
            out.append(f'  tl.to("{sel}", {{{body}}}, {local + off:.2f});')
    return "\n".join(out)


BASE = """
    tl.fromTo("#{sid} .world", {{ scale:1.02 }}, {{ scale:1.06, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:20 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1, ease:"power2.out" }}, 0.05);
"""


def page(sid, body, dur):
    extra = ""
    if sid == "s1":
        extra = 'tl.to(".runner", {x:"+=140", duration:1.4, stagger:0.12, ease:"power1.in"}, 0);'
    elif sid == "s2":
        extra = 'tl.to(".snow", {y:300, duration:6, ease:"none"}, 0);'
    elif sid == "s4":
        extra = 'tl.to(".rescuer", {x:"+=40", duration:1.6, stagger:0.15, yoyo:true, repeat:3, ease:"sine.inOut"}, 0);'
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#101a20; }}
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
{BASE.format(sid=sid, dur=dur)}{extra}
{cue_lines(sid)}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts, start = [], 0
    for i, sid in enumerate(SCENE_ORDER):
        st, dur = BOUNDS[sid]
        html = page(sid, SCENE_FN[sid](), dur)
        (OUT / f"{sid}.html").write_text(html, encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st:.3f}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        start = max(start, st + dur)
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
