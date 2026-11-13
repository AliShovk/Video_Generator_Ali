#!/usr/bin/env python3
"""«5 ошибок, из-за которых падает напор» — 7 сцен, 9:16."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/water")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(7):
    end = STARTS[i + 1] if i + 1 < 7 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#eef3f6"
INK = "#243039"
PIPE = "#8fa3b1"
PIPE_D = "#6d8290"
WATER = "#3f9fd4"
WATER_L = "#8fd0ee"
RED = "#c0392b"
GREEN = "#2f8f5b"
BRASS = "#c9a24a"

DEFS = """<defs>
<linearGradient id="pipeG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9bcc8"/><stop offset="0.45" stop-color="#cfdde6"/><stop offset="1" stop-color="#7d909d"/></linearGradient>
<linearGradient id="waterG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2f8dc0"/><stop offset="1" stop-color="#7ccbea"/></linearGradient>
<radialGradient id="glowB"><stop offset="0" stop-color="#8fd0ee" stop-opacity="0.6"/><stop offset="1" stop-color="#8fd0ee" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=190, size=66):
    return "".join(
        f'<text class="hl" x="54" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=520):
    return (f'<g class="b"><circle cx="118" cy="{y}" r="54" fill="{INK}"/>'
            f'<text x="118" y="{y+18}" font-family="Nunito, Arial" font-size="44" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def pipe_h(x, y, w, h=64, water=True):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#pipeG)" stroke="{PIPE_D}" stroke-width="3"/>']
    if water:
        out.append(f'<rect class="wflow" x="{x+6}" y="{y+14}" width="{w-12}" height="{h-28}" rx="8" fill="url(#waterG)"/>')
    return "".join(out)


def gauge(cx, cy, r=110, needle=-40, ident="needle"):
    ticks = "".join(
        f'<line x1="{cx}" y1="{cy-r+10}" x2="{cx}" y2="{cy-r+26}" stroke="#5b6b76" stroke-width="5" transform="rotate({a} {cx} {cy})"/>'
        for a in range(-120, 121, 30))
    return (f'<g class="gauge"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{PIPE_D}" stroke-width="8"/>'
            f'{ticks}<circle cx="{cx}" cy="{cy}" r="10" fill="{INK}"/>'
            f'<g id="{ident}" transform="rotate({needle} {cx} {cy})"><rect x="{cx-4}" y="{cy-r+20}" width="8" height="{r-30}" rx="4" fill="{RED}"/></g>'
            f'<text x="{cx}" y="{cy+r-18}" font-family="Nunito, Arial" font-size="26" font-weight="800" fill="{INK}" text-anchor="middle">бар</text></g>')


def dots(x, y, n=6, gap=60, cls="dropF"):
    return "".join(f'<circle class="{cls}" cx="{x + i*gap}" cy="{y}" r="9" fill="{WATER_L}"/>' for i in range(n))


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # смеситель крупно
    b.append(f'<rect x="520" y="560" width="44" height="520" fill="url(#pipeG)" stroke="{PIPE_D}" stroke-width="4"/>')
    b.append(f'<path d="M 542 560 q 0 -90 90 -90 l 150 0" stroke="{PIPE}" stroke-width="54" fill="none" stroke-linecap="round"/>')
    b.append(f'<rect x="740" y="440" width="56" height="86" rx="12" fill="{BRASS}"/>')
    b.append(f'<circle cx="542" cy="600" r="30" fill="{BRASS}"/>')
    # струйка
    for i in range(4):
        b.append(f'<path class="stream" d="M 768 526 q 4 150 0 300" stroke="{WATER_L}" stroke-width="{10 + i*2}" fill="none" opacity="0.9"/>')
    # раковина
    b.append(f'<rect x="600" y="850" width="360" height="150" rx="26" fill="#dbe6ec" stroke="{PIPE_D}" stroke-width="6"/>')
    b.append(f'<ellipse cx="780" cy="870" rx="150" ry="26" fill="#c3d3dc"/>')
    b.append(f'<ellipse cx="780" cy="872" rx="60" ry="12" fill="{WATER}" opacity="0.25"/>')
    b.append(f'<rect x="760" y="1000" width="40" height="150" fill="{PIPE}" opacity="0.7"/>')
    b.append(gauge(300, 900, 150, -80, "needle1"))
    b.append(f'<text x="300" y="1130" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{RED}" text-anchor="middle">0,5 бар</text>')
    b.append(title([("НАПОР", INK), ("УПАЛ", RED)], 190, 78))
    b.append(f'<text x="54" y="470" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">насос работает, а вода еле идёт</text>')
    b.append(f'<g class="chip"><rect x="120" y="1330" width="380" height="90" rx="45" fill="{INK}"/>'
             f'<text x="310" y="1390" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="#fff" text-anchor="middle">5 ПРИЧИН</text></g>')
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="120" y="520" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="{INK}">16 ММ</text>')
    b.append(pipe_h(120, 560, 380, 60))
    b.append(f'<text x="620" y="900" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="{GREEN}">25 ММ</text>')
    b.append(pipe_h(620, 940, 380, 130))
    b.append(dots(160, 590, 4, 80, "smallF"))
    b.append(dots(660, 1005, 4, 80, "bigF"))
    b.append(f'<path d="M 540 700 l 0 -60" stroke="{RED}" stroke-width="10"/>')
    b.append(f'<text x="560" y="660" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{RED}">узко</text>')
    b.append(badge(1))
    b.append(title([("ТРУБА", INK), ("СЛИШКОМ ТОНКАЯ", RED)], 150, 58))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    pts = [(90, 900), (300, 900), (300, 1060), (520, 1060), (520, 900), (740, 900), (740, 1100), (980, 1100)]
    for i in range(0, len(pts) - 1, 2):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        b.append(f'<rect x="{min(x1,x2)}" y="{y1-30}" width="{abs(x2-x1)+60}" height="60" rx="10" fill="url(#pipeG)" stroke="{PIPE_D}" stroke-width="3"/>')
    for i in range(1, len(pts) - 1, 2):
        x, y = pts[i]
        b.append(f'<rect x="{x-30}" y="{y-30}" width="60" height="220" rx="10" fill="url(#pipeG)" stroke="{PIPE_D}" stroke-width="3"/>')
    b.append(f'<g class="turns">' + "".join(
        f'<text x="{x}" y="{y-46}" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{RED}" text-anchor="middle">90°</text>'
        for x, y in [(300, 900), (520, 1060), (740, 900)]) + '</g>')
    b.append(badge(2))
    b.append(title([("ЛИШНИЕ", INK), ("ПОВОРОТЫ", RED)], 150, 62))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="120" y="700" width="420" height="300" rx="16" fill="#c7d3da" stroke="{PIPE_D}" stroke-width="5"/>')
    b.append(f'<text x="330" y="870" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{INK}" text-anchor="middle">НАСОС</text>')
    b.append(f'<circle class="pumpGlow" cx="330" cy="850" r="220" fill="url(#glowB)" opacity="0.4"/>')
    b.append(gauge(830, 800, 130, -100, "needle4"))
    b.append(f'<g class="tank"><rect x="700" y="1080" width="260" height="320" rx="70" fill="#dbe6ec" stroke="{PIPE_D}" stroke-width="5" opacity="0.55"/>'
             f'<text x="830" y="1250" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{PIPE_D}" text-anchor="middle">НЕТ</text></g>')
    b.append(f'<path class="cross4" d="M 760 1130 l 140 220 M 900 1130 l -140 220" stroke="{RED}" stroke-width="14" stroke-linecap="round" opacity="0.85"/>')
    b.append(badge(3))
    b.append(title([("НЕТ", INK), ("ГИДРОАККУМУЛЯТОРА", RED)], 150, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="330" y="560" width="420" height="620" rx="24" fill="#dbe6ec" stroke="{PIPE_D}" stroke-width="6"/>')
    b.append(f'<rect x="380" y="620" width="320" height="500" rx="14" fill="#a97b4a" class="cartridge"/>')
    for i in range(7):
        b.append(f'<rect x="380" y="{640 + i*70}" width="320" height="16" fill="#7d5630" opacity="0.7"/>')
    b.append(f'<path d="M 540 1180 l 0 120" stroke="{PIPE}" stroke-width="46"/>')
    b.append(f'<g class="slowflow">' + "".join(f'<circle cx="540" cy="{1320 + i*40}" r="8" fill="{WATER_L}" opacity="0.6"/>' for i in range(4)) + '</g>')
    b.append(badge(4))
    b.append(title([("ЗАБИТЫЙ", INK), ("ФИЛЬТР", RED)], 150, 62))
    b.append(f'<text x="54" y="330" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">картридж не меняли полгода</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # труба горбом
    b.append(f'<path d="M 80 1300 l 240 0 l 120 -240 l 240 0 l 120 240 l 240 0" stroke="{PIPE}" stroke-width="90" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<path d="M 80 1300 l 240 0 l 120 -240 l 240 0 l 120 240 l 240 0" stroke="{WATER}" stroke-width="52" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>')
    b.append(f'<circle class="air" cx="560" cy="1030" r="46" fill="#ffffff" stroke="{PIPE_D}" stroke-width="4" opacity="0.95"/>')
    b.append(f'<text x="560" y="1042" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{PIPE_D}" text-anchor="middle">ВОЗДУХ</text>')
    b.append(f'<g class="blocked"><path d="M 700 1180 l 60 60 M 760 1180 l -60 60" stroke="{RED}" stroke-width="12" stroke-linecap="round"/></g>')
    b.append(badge(5))
    b.append(title([("ВОЗДУШНАЯ", INK), ("ПРОБКА", RED)], 150, 62))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="300" font-family="Nunito, Arial" font-size="62" font-weight="900" fill="{INK}" text-anchor="middle">ПРОВЕРЬ</text>')
    items = ["диаметр трубы", "число поворотов", "гидроаккумулятор", "фильтр", "воздушная пробка"]
    for i, t in enumerate(items):
        y = 500 + i * 195
        b.append(f'<g class="row r{i}"><circle cx="170" cy="{y}" r="44" fill="{GREEN}"/>'
                 f'<path d="M 150 {y} l 14 16 l 30 -34" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/>'
                 f'<text x="250" y="{y+12}" font-family="Nunito, Arial" font-size="42" font-weight="900" fill="{INK}">{t}</text></g>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7]


def page(sid, body, dur):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">{body}</div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.04, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
    tl.fromTo(".b", {{ scale:0.6, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.4, ease:"back.out(2)" }}, 0.2);
    tl.to(".stream", {{ y:26, opacity:0.6, duration:0.5, yoyo:true, repeat:12, stagger:0.05 }}, 0);
    tl.to("#needle1", {{ rotation:-70, svgOrigin:"300 900", duration:1.8, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0);
    tl.to(".slow", {{ x:70, duration:3.2, stagger:0.2, ease:"none" }}, 0);
    tl.to(".smallF", {{ x:60, duration:3.0, stagger:0.15, ease:"none" }}, 0);
    tl.to(".bigF", {{ x:90, duration:2.2, stagger:0.15, ease:"none" }}, 0);
    tl.to(".wflow", {{ opacity:0.75, duration:0.8, yoyo:true, repeat:4 }}, 0);
    tl.to(".turns", {{ x:8, duration:0.9, yoyo:true, repeat:5 }}, 0);
    tl.to("#needle4", {{ rotation:0, svgOrigin:"830 800", duration:0.25, yoyo:true, repeat:18, ease:"none" }}, 0);
    tl.to(".pumpGlow", {{ opacity:0.15, duration:0.25, yoyo:true, repeat:18 }}, 0);
    tl.to(".cross4", {{ opacity:0.4, duration:0.7, yoyo:true, repeat:5 }}, 0);
    tl.to(".cartridge", {{ fill:"#8a5f34", duration:{dur}, ease:"none" }}, 0);
    tl.to(".slowflow", {{ y:40, opacity:0, duration:1.4, repeat:6, ease:"none" }}, 0);
    tl.to(".air", {{ y:-8, x:6, duration:1.2, yoyo:true, repeat:6, ease:"sine.inOut" }}, 0);
    tl.to(".blocked", {{ scale:1.1, transformOrigin:"730 1210", duration:0.6, yoyo:true, repeat:6 }}, 0);
    tl.fromTo(".row", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.32 }}, 0.2);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, fn in enumerate(SCENES):
        sid = f"s{i+1}"
        st, dur = BOUNDS[i]
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur), encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
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
