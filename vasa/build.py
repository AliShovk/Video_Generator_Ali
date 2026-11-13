#!/usr/bin/env python3
"""Сборка ролика «Васа»: 5 сцен, 50 с."""
from pathlib import Path

from scene import (DEFS, GOLD, HULL, HULL_D, INK, RED, SEA, crowd, cloud, gull, label,
                   person, sea, ship)

OUT = Path("/root/video-gen/vasa/compositions")
OUT.mkdir(parents=True, exist_ok=True)
ROOT = Path("/root/video-gen/vasa")


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


# ------------------------------------------------------------------ scene 1
def s1():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append(cloud(230, 250, 1.0, "cloud c1") + cloud(820, 170, 0.7, "cloud c2") + cloud(560, 330, 0.5, "cloud c3"))
    b.append(gull(300, 430, 1.1) + gull(380, 470, 0.8) + gull(250, 500, 0.9) + gull(880, 380, 0.7))
    b.append('<rect x="0" y="1230" width="1080" height="120" fill="#8a9aa5"/>')  # набережная
    b.append('<rect x="0" y="1230" width="1080" height="18" fill="#a9b7c0"/>')
    b.append(sea(1340, 580))
    b.append(crowd(16, 1190))
    b.append(ship(600, 1330, 1.0, -2, "ship1"))
    b.append('<g class="dock"><rect x="60" y="1250" width="180" height="26" fill="#6b4a2a"/><rect x="80" y="1276" width="16" height="70" fill="#5a3d22"/><rect x="200" y="1276" width="16" height="70" fill="#5a3d22"/></g>')
    return svg("".join(b))


# ------------------------------------------------------------------ scene 2
def s2():
    b = ['<rect width="1080" height="1920" fill="#eef4f8"/>']
    b.append('<rect x="0" y="1500" width="1080" height="420" fill="#dbe7ef"/>')
    b.append(ship(540, 1380, 1.28, 0, "ship2"))
    # размеры
    b.append(f'<line x1="120" y1="1600" x2="960" y2="1600" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<line x1="120" y1="1570" x2="120" y2="1630" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<line x1="960" y1="1570" x2="960" y2="1630" stroke="{INK}" stroke-width="4"/>')
    b.append(label(540, 1660, "69 МЕТРОВ", 46, INK, 900, "middle", "lbl dim"))
    b.append(f'<line x1="1010" y1="880" x2="1010" y2="1560" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<line x1="982" y1="1560" x2="1038" y2="1560" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<line x1="982" y1="880" x2="1038" y2="880" stroke="{INK}" stroke-width="4"/>')
    b.append(label(1000, 900, "52 М", 38, INK, 900, "middle", "lbl dim"))
    # счётчик пушек
    for i in range(64):
        r, c = divmod(i, 16)
        b.append(f'<circle class="gun" cx="{120 + c*54}" cy="{430 + r*54}" r="17" fill="{RED}"/>')
    return svg("".join(b))


# ------------------------------------------------------------------ scene 3
def s3():
    b = ['<rect width="1080" height="1920" fill="#f3f0e8"/>']
    b.append('<rect x="0" y="1560" width="1080" height="360" fill="#dfe8ee"/>')
    # разрез корпуса
    b.append(f'<g id="section" transform="translate(540 1180) scale(1.24)">')
    b.append(f'<path d="M -280 0 q 30 120 110 140 l 340 0 q 90 -20 120 -140 z" fill="{HULL}" stroke="{HULL_D}" stroke-width="5"/>')
    b.append(f'<rect x="-270" y="-30" width="540" height="30" fill="{HULL_D}"/>')
    # балласт
    for i in range(16):
        b.append(f'<ellipse class="stone" cx="{-240 + (i%8)*70}" cy="{70 + (i//8)*34}" rx="26" ry="16" fill="#8d8d8d" stroke="#6f6f6f" stroke-width="2"/>')
    # пушки высоко
    for i in range(8):
        b.append(f'<rect x="{-250 + i*64}" y="-120" width="34" height="30" rx="4" fill="{RED}"/>')
        b.append(f'<rect x="{-244 + i*64}" y="-112" width="20" height="10" rx="4" fill="#2a1b12"/>')
    # центр тяжести
    b.append(f'<g class="cg"><circle cx="0" cy="-40" r="16" fill="{RED}"/><line x1="0" y1="-40" x2="0" y2="-210" stroke="{RED}" stroke-width="6"/><text x="16" y="-200" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{RED}">центр тяжести</text></g>')
    b.append(f'<g class="cl"><circle cx="0" cy="110" r="16" fill="#2f6f96"/><line x1="0" y1="110" x2="0" y2="250" stroke="#2f6f96" stroke-width="6"/><text x="16" y="250" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="#2f6f96">балласт</text></g>')
    b.append('</g>')
    # бегущие люди на палубе
    for i in range(6):
        b.append(f'<g class="runner" transform="translate({360 + i*54} 700)"><circle cx="0" cy="-24" r="6" fill="#f0c8a0"/><rect x="-5" y="-18" width="10" height="20" rx="4" fill="#b83227"/></g>')
    return svg("".join(b))


# ------------------------------------------------------------------ scene 4
def s4():
    b = ['<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append(cloud(250, 300, 0.8, "cloud c1") + cloud(850, 240, 0.6, "cloud c2"))
    b.append(gull(300, 500, 0.9) + gull(360, 540, 0.7))
    b.append(sea(1300, 620))
    b.append('<g class="gust">' + "".join(
        f'<path d="M -60 {760 + i*80} q 180 -30 340 0" stroke="#ffffff" stroke-width="7" fill="none" opacity="0.7" stroke-linecap="round"/>'
        for i in range(5)) + '</g>')
    b.append(ship(560, 1290, 1.0, -16, "ship4"))
    # дым выстрелов
    for i in range(4):
        b.append(f'<circle class="smoke" cx="{300 + i*120}" cy="1050" r="{26 + i*6}" fill="#f0efe9" opacity="0.85"/>')
    # вода в портах
    for i in range(6):
        b.append(f'<path class="inflow" d="M {330 + i*60} 1120 q -18 60 6 100" stroke="#bfe0f5" stroke-width="10" fill="none" opacity="0"/>')
    # пузыри
    for i in range(18):
        b.append(f'<circle class="bubble" cx="{220 + i*42}" cy="{1500 + (i%4)*40}" r="{5 + i%5}" fill="#ffffff" opacity="0.7"/>')
    return svg("".join(b))


# ------------------------------------------------------------------ scene 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="#0e2a3a"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="url(#deep)"/>')
    b.append("""
<defs><linearGradient id="deep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d5b77"/><stop offset="0.6" stop-color="#0e3548"/><stop offset="1" stop-color="#08222f"/></linearGradient></defs>""")
    b.append('<rect x="0" y="1620" width="1080" height="300" fill="#0a2b3a"/>')
    b.append('<g class="raysUnder" opacity="0.18">' + "".join(
        f'<path d="M {i*140} 0 L {i*140 + 90} 0 L {i*140 + 210} 1400 L {i*140 + 90} 1400 Z" fill="#9fe0ff"/>' for i in range(9)) + '</g>')
    b.append(ship(560, 1580, 1.2, 26, "wreck"))
    for i in range(24):
        b.append(f'<circle class="bubble" cx="{120 + i*38}" cy="{1300 + (i%6)*70}" r="{4 + i%6}" fill="#9fe0ff" opacity="0.5"/>')
        return svg("".join(b))


SCENES = {"s1": (s1, 9), "s2": (s2, 11), "s3": (s3, 11), "s4": (s4, 10), "s5": (s5, 9)}
HEAD = {
    "s1": [("1300 МЕТРОВ", "#b83227"), ("И ЗАТОНУЛ", "#1d2733")],
    "s2": [("64 ПУШКИ", "#b83227"), ("69 МЕТРОВ", "#1d2733")],
    "s3": [("СЛИШКОМ", "#1d2733"), ("ТЯЖЁЛЫЙ ВЕРХ", "#b83227")],
    "s4": [("ОДИН ПОРЫВ", "#1d2733"), ("ВЕТРА", "#b83227")],
    "s5": [("333 ГОДА", "#7fd4ff"), ("НА ДНЕ", "#ffffff")],
}


def page(sid, body, dur):
    dark = sid == "s5"
    head = "".join(
        f'<text class="hl" x="56" y="{228 + i*92}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="74" font-weight="900" letter-spacing="-1">{s}</text>' for i, (s, c) in enumerate(HEAD[sid]))
    body = body.replace('</svg>', f'<g class="head">{head}</g></svg>')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{'#08222f' if dark else '#bfe0f2'}; }}
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
    tl.fromTo("#{sid} .world", {{ scale:1.02 }}, {{ scale:1.08, duration:{dur}, ease:"none" }}, 0);
    tl.to(".cloud", {{ x:"+=110", duration:14, ease:"none" }}, 0);
    tl.to(".c3", {{ x:"-=80", duration:12, ease:"none" }}, 0);
    tl.to(".gull", {{ x:"+=220", y:"-=24", duration:10, ease:"none" }}, 0);
    tl.to(".gull", {{ y:"+=10", duration:0.7, yoyo:true, repeat:12, ease:"sine.inOut" }}, 0);
    tl.to(".wave", {{ x:"+=30", duration:2.2, yoyo:true, repeat:5, ease:"sine.inOut" }}, 0);
    tl.to(".walker", {{ x:"+=40", duration:8, ease:"none" }}, 0);
    tl.to(".sail", {{ scaleX:1.04, transformOrigin:"50% 100%", duration:1.6, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0);
    tl.to(".flag", {{ skewX:-8, duration:1.0, yoyo:true, repeat:10, ease:"sine.inOut" }}, 0);
    tl.to("#ship1", {{ rotation:-4, svgOrigin:"0 0", duration:2.4, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0);
    tl.to("#ship2", {{ rotation:2, svgOrigin:"0 0", duration:3.0, yoyo:true, repeat:3, ease:"sine.inOut" }}, 0);
    tl.fromTo(".dim", {{ opacity:0, scale:0.9 }}, {{ opacity:1, scale:1, duration:0.5, stagger:0.3 }}, 0.2);
    tl.fromTo(".gun", {{ scale:0, transformOrigin:"50% 50%" }}, {{ scale:1, duration:0.35, stagger:{{each:0.02}}, ease:"back.out(2)" }}, 0.3);
    tl.to(".runner", {{ x:"+=120", duration:1.1, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0.4);
    tl.to("#section", {{ rotation:8, svgOrigin:"0 300", duration:3.2, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0.6);
    tl.to(".stone", {{ x:"+=14", duration:1.2, yoyo:true, repeat:6, stagger:0.04, ease:"sine.inOut" }}, 0.4);
    tl.to(".cg", {{ y:-8, duration:0.9, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0.3);
    tl.to(".cl", {{ y:6, duration:1.1, yoyo:true, repeat:7, ease:"sine.inOut" }}, 0.3);
    tl.fromTo("#ship4", {{ rotation:-2 }}, {{ rotation:-19, svgOrigin:"0 0", duration:5, ease:"sine.in" }}, 1.0);
    tl.fromTo(".smoke", {{ opacity:0, scale:0.4, transformOrigin:"50% 50%" }}, {{ opacity:0.85, scale:1, duration:0.7, stagger:0.25 }}, 1.2);
    tl.to(".smoke", {{ x:"+=70", y:"-=40", opacity:0.15, duration:3.5, stagger:0.2, ease:"power1.out" }}, 2.2);
    tl.fromTo(".inflow", {{ opacity:0 }}, {{ opacity:1, duration:0.5, stagger:0.15 }}, 4.6);
    tl.to(".bubble", {{ y:"-=420", opacity:0, duration:3.4, stagger:{{each:0.06, from:"random"}}, repeat:1, ease:"power1.in" }}, 0.5);
    tl.to(".gust", {{ x:"+=80", duration:3, stagger:0.15, ease:"none" }}, 0.6);
    tl.to(".raysUnder", {{ opacity:0.28, duration:2.4, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0);
    tl.to("#wreck", {{ rotation:28, y:"+=10", duration:{dur}, ease:"sine.inOut" }}, 0);
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
