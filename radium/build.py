#!/usr/bin/env python3
"""«Девушки, которые светились» — 50 с, 9:16."""
from pathlib import Path

from scene import (BRASS, DARK, DEFS, DRESS, GLOW, GLOW_D, PAPER, RED, SKIN, TEAL, TEAL_L,
                   bench, brush, dial, dust, label, woman)

OUT = Path("/root/video-gen/radium/compositions")
OUT.mkdir(parents=True, exist_ok=True)
ROOT = Path("/root/video-gen/radium")


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


# ------------------------------------------------------------------ 1: крюк
def s1():
    b = [f'<rect width="1080" height="1920" fill="url(#roomG)"/>']
    b.append(f'<rect x="0" y="1500" width="1080" height="420" fill="#0a1416"/>')
    b.append(f'<circle cx="540" cy="900" r="520" fill="url(#glowG)" opacity="0.35" class="roomGlow"/>')
    b.append(bench(120, 1400, 840))
    b.append(woman(470, 1400, 1.35, "girl1", arm=True))
    b.append(dial(760, 1330, 74, True))
    b.append(brush(560, 1150, -34, 1.5, "brush1"))
    b.append(dust(30, 4))
    b.append(f'<g class="lamp"><rect x="880" y="520" width="10" height="330" fill="{BRASS}"/>'
             f'<path d="M 830 520 l 120 0 l -20 -60 l -80 0 z" fill="{BRASS}"/>'
             f'<ellipse cx="890" cy="528" rx="60" ry="10" fill="#ffe9a8"/></g>')
    return svg("".join(b))


# ------------------------------------------------------------------ 2: фабрика
def s2():
    b = [f'<rect width="1080" height="1920" fill="#101d20"/>']
    b.append(f'<rect x="0" y="1560" width="1080" height="360" fill="#0b1416"/>')
    b.append(f'<rect x="0" y="300" width="1080" height="180" fill="#16292d"/>')
    for i in range(4):
        b.append(f'<rect x="{90 + i*240}" y="330" width="120" height="120" rx="8" fill="#0e1c20" stroke="{TEAL_L}" stroke-width="4"/>')
    b.append(bench(40, 1430, 1000))
    for i in range(6):
        x = 130 + i * 155
        b.append(woman(x, 1690, 1.0, f"w{i}", arm=True))
        b.append(f'<g class="dialRow"><circle cx="{x+52}" cy="1408" r="34" fill="#12252a" stroke="{GLOW}" stroke-width="3"/>'
                 f'<circle class="halo" cx="{x+52}" cy="1408" r="60" fill="url(#glowG)"/></g>')
    b.append(f'<g class="foreman"><rect x="880" y="1330" width="120" height="160" rx="10" fill="#20343a"/>'
             f'<circle cx="940" cy="1306" r="26" fill="{SKIN}"/><rect x="905" y="1344" width="70" height="20" rx="6" fill="{BRASS}"/></g>')
    b.append(dust(36, 9))
    return svg("".join(b))


# ------------------------------------------------------------------ 3: привычка
def s3():
    b = [f'<rect width="1080" height="1920" fill="#0a1214"/>']
    b.append(f'<circle cx="520" cy="820" r="520" fill="url(#glowG)" opacity="0.45" class="roomGlow"/>')
    # плечи и шея
    b.append(f'<path d="M 190 1560 q 90 -220 250 -250 l 160 0 q 160 30 250 250 z" fill="{DRESS}"/>')
    b.append(f'<path d="M 494 1210 l 72 0 l 10 130 l -92 0 z" fill="{SKIN}"/>')
    # волосы сзади
    b.append(f'<ellipse cx="530" cy="900" rx="230" ry="270" fill="#3b2a20"/>')
    b.append(f'<circle cx="530" cy="640" r="86" fill="#3b2a20"/>')
    # лицо
    b.append(f'<ellipse cx="530" cy="960" rx="196" ry="238" fill="{SKIN}"/>')
    # чёлка
    b.append(f'<path d="M 334 900 q 10 -250 196 -250 q 186 0 196 250 q -70 -120 -196 -120 q -126 0 -196 120 z" fill="#3b2a20"/>')
    # брови
    b.append(f'<path d="M 400 862 q 46 -26 92 -4" stroke="#3b2a20" stroke-width="14" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M 570 858 q 46 -22 92 4" stroke="#3b2a20" stroke-width="14" fill="none" stroke-linecap="round"/>')
    # глаза
    b.append(f'<ellipse cx="440" cy="930" rx="34" ry="24" fill="#fff"/>')
    b.append(f'<ellipse cx="620" cy="930" rx="34" ry="24" fill="#fff"/>')
    b.append(f'<circle cx="446" cy="932" r="14" fill="#2a1d18"/><circle cx="626" cy="932" r="14" fill="#2a1d18"/>')
    b.append(f'<path d="M 406 926 q 34 -26 68 0" stroke="#2a1d18" stroke-width="5" fill="none"/>')
    b.append(f'<path d="M 586 926 q 34 -26 68 0" stroke="#2a1d18" stroke-width="5" fill="none"/>')
    # нос
    b.append(f'<path d="M 530 960 q -14 54 6 62" stroke="#c98f6a" stroke-width="7" fill="none" stroke-linecap="round"/>')
    # губы
    b.append(f'<path d="M 470 1074 q 30 -22 60 0 q 30 -22 60 0 q -30 40 -60 40 q -30 0 -60 -40 z" fill="#c0473f"/>')
    b.append(f'<path d="M 470 1074 q 60 14 120 0" stroke="#8e2f2a" stroke-width="5" fill="none"/>')
    # рука с кистью у губ
    b.append(f'<g class="armBig"><path d="M 1010 1520 q -190 -120 -300 -370" stroke="{SKIN}" stroke-width="46" fill="none" stroke-linecap="round"/>'
             f'<circle cx="702" cy="1132" r="42" fill="{SKIN}"/></g>')
    b.append(brush(702, 1132, 201, 1.34, "brush3"))
    b.append(dust(34, 12))
    return svg("".join(b))


# ------------------------------------------------------------------ 4: болезнь
def s4():
    b = [f'<rect width="1080" height="1920" fill="#0b1416"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="#0e1a1d"/>')
    b.append(f'<g transform="translate(520 980)">')
    # черепная коробка
    b.append(f'<path d="M -250 40 q -30 -150 40 -260 q 70 -110 210 -110 q 140 0 210 110 q 70 110 40 260 '
             f'q -10 46 -46 66 l 0 60 q 0 40 -40 40 l -328 0 q -40 0 -40 -40 l 0 -60 q -36 -20 -46 -66 z" '
             f'fill="#d9e8e4" opacity="0.18" stroke="#8fd9c7" stroke-width="5"/>')
    # глазницы
    b.append(f'<path d="M -150 -30 q 60 -40 110 0 q 20 44 -20 70 q -60 20 -90 -20 q -10 -30 0 -50 z" fill="#08120f"/>')
    b.append(f'<path d="M 40 -30 q 50 -40 110 0 q 10 20 0 50 q -30 40 -90 20 q -40 -26 -20 -70 z" fill="#08120f"/>')
    # носовая полость
    b.append(f'<path d="M -22 40 l 44 0 l 14 60 l -72 0 z" fill="#08120f"/>')
    # скулы
    b.append(f'<path d="M -210 90 q 40 60 90 60" stroke="#8fd9c7" stroke-width="4" fill="none" opacity="0.6"/>')
    b.append(f'<path d="M 210 90 q -40 60 -90 60" stroke="#8fd9c7" stroke-width="4" fill="none" opacity="0.6"/>')
    # верхняя челюсть с зубами
    b.append(f'<path d="M -140 150 l 280 0 l 0 50 l -280 0 z" fill="#cfe3e0" opacity="0.22"/>')
    for i in range(10):
        b.append(f'<rect x="{-132 + i*27}" y="156" width="18" height="36" rx="4" fill="#e8f5f1" opacity="0.5"/>')
    # нижняя челюсть отдельно + свечение
    b.append(f'<g class="jawGlow"><path d="M -150 216 l 300 0 l -26 96 q -124 40 -248 0 z" fill="url(#glowG)" opacity="0.9"/></g>')
    b.append(f'<path d="M -150 216 l 300 0 l -26 96 q -124 40 -248 0 z" fill="#cfe3e0" opacity="0.25" stroke="{GLOW}" stroke-width="5"/>')
    b.append(f'<path d="M -150 216 l 300 0" stroke="{GLOW}" stroke-width="5" stroke-dasharray="14 12"/>')
    b.append('</g>')
    b.append(label(520, 1590, "ЧЕЛЮСТЬ РАЗРУШАЕТСЯ", 54, GLOW, 900, "middle"))
    b.append(f'<g class="stampBox" transform="rotate(-7 810 470)">'
             f'<rect x="590" y="400" width="440" height="140" rx="8" fill="none" stroke="{RED}" stroke-width="9" opacity="0.85"/>'
             f'<text x="810" y="492" font-family="Nunito, Arial" font-size="58" font-weight="900" fill="{RED}" '
             f'text-anchor="middle" opacity="0.9">«СИФИЛИС»</text></g>')
    return svg("".join(b))


# ------------------------------------------------------------------ 5: суд
def s5():
    b = [f'<rect width="1080" height="1920" fill="#141f22"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="url(#roomG)"/>')
    b.append(f'<rect x="0" y="1420" width="1080" height="500" fill="#0d1618"/>')
    b.append(f'<rect x="120" y="1120" width="840" height="300" rx="14" fill="#243b40"/>')
    b.append(f'<rect x="120" y="1120" width="840" height="22" rx="8" fill="{BRASS}"/>')
    for i in range(5):
        b.append(woman(200 + i * 170, 1120, 0.95, f"j{i}"))
    b.append(f'<g class="gavel"><rect x="742" y="1012" width="176" height="30" rx="14" fill="#8a5a34"/>'
             f'<rect x="814" y="1040" width="30" height="58" fill="#8a5a34" transform="rotate(12 829 1069)"/>'
             f'<rect x="770" y="1096" width="120" height="24" rx="10" fill="#6b4227"/></g>')
    b.append(f'<rect x="760" y="1120" width="150" height="26" rx="10" fill="#3a2a1e"/>')
    b.append(f'<rect x="700" y="420" width="300" height="180" rx="10" fill="url(#paperG)"/>')
    b.append(label(850, 500, "ИСК", 46, "#2a2118", 900, "middle"))
    b.append(label(850, 566, "1927", 46, "#2a2118", 900, "middle"))
    b.append(dust(22, 15, 1080, 1200))
    return svg("".join(b))


SCENES = {"s1": (s1, 9), "s2": (s2, 11), "s3": (s3, 10), "s4": (s4, 10), "s5": (s5, 10)}
HEAD = {
    "s1": [("КИСТЬ", "#8affb0"), ("СВЕТИЛАСЬ", "#ffffff")],
    "s2": [("ТАК РАБОТАЛИ", "#8affb0"), ("НА ФАБРИКЕ", "#ffffff")],
    "s3": [("ОБЛИЗНУТЬ —", "#8affb0"), ("ЧТОБЫ БЫЛО ОСТРО", "#ffffff")],
    "s4": [("ВРАЧИ СКАЗАЛИ:", "#ffffff"), ("«СИФИЛИС»", "#c0392b")],
    "s5": [("СУД ВЫИГРАН", "#8affb0"), ("1928", "#ffffff")],
}


def page(sid, body, dur):
    head = "".join(
        f'<text class="hl" x="56" y="{228 + i*92}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="70" font-weight="900" letter-spacing="-1">{s}</text>' for i, (s, c) in enumerate(HEAD[sid]))
    body = body.replace('</svg>', f'<g class="head">{head}</g></svg>')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#0a1214; }}
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
    tl.to(".halo", {{ opacity:0.35, duration:1.4, yoyo:true, repeat:20, ease:"sine.inOut" }}, 0);
    tl.to(".mote", {{ y:"-=140", opacity:0, duration:6, stagger:{{each:0.09, from:"random"}}, repeat:2, ease:"none" }}, 0);
    tl.to(".tipGlow", {{ opacity:0.35, scale:1.15, transformOrigin:"50% 50%", duration:0.9, yoyo:true, repeat:20, stagger:0.1, ease:"sine.inOut" }}, 0);
    tl.to(".armBig", {{ rotation:2, svgOrigin:"1010 1520", duration:2.0, yoyo:true, repeat:9, ease:"sine.inOut" }}, 0);
    tl.to(".arm", {{ rotation:-4, svgOrigin:"22 -104", duration:2.2, yoyo:true, repeat:9, ease:"sine.inOut" }}, 0);
    tl.to(".hand", {{ rotation:360, svgOrigin:"0 0", duration:8, repeat:4, ease:"none" }}, 0);
    tl.to(".hand2", {{ rotation:360, svgOrigin:"0 0", duration:26, repeat:1, ease:"none" }}, 0);
    tl.to(".roomGlow", {{ opacity:0.5, duration:2.0, yoyo:true, repeat:10, ease:"sine.inOut" }}, 0);
    tl.to(".dialRow", {{ y:-8, duration:1.2, yoyo:true, repeat:8, stagger:0.12, ease:"sine.inOut" }}, 0);
    tl.to(".foreman", {{ x:"+=26", duration:4.5, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0);
    tl.fromTo(".jawGlow", {{ opacity:0.35 }}, {{ opacity:1, duration:1.6, yoyo:true, repeat:5, ease:"sine.inOut" }}, 0.2);
    tl.fromTo(".stampBox", {{ opacity:0, scale:1.4, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1, duration:0.6, ease:"power3.out" }}, 1.0);
    tl.to(".gavel", {{ rotation:-9, svgOrigin:"880 1130", duration:0.42, yoyo:true, repeat:9, ease:"power2.inOut" }}, 0.4);
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
