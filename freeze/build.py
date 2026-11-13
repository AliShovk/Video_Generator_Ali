#!/usr/bin/env python3
"""«Замёрзшая система» — 8 сцен, экшн."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/freeze")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#0f1b24"
INK = "#e8f2f8"
STEEL = "#9db2c0"
STEEL_D = "#5d7280"
WATER = "#3fa6d8"
WATER_L = "#9fe0ff"
ICE = "#bfeaff"
RED = "#e04a35"
WARM = "#ffa24d"
WHITE = "#ffffff"

DEFS = """<defs>
<linearGradient id="steelG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c3d3dd"/><stop offset="0.5" stop-color="#8ea4b2"/><stop offset="1" stop-color="#5d7280"/></linearGradient>
<linearGradient id="iceG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8fbff"/><stop offset="1" stop-color="#8fd4f0"/></linearGradient>
<linearGradient id="waterG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fd0f2"/><stop offset="1" stop-color="#2b7fa8"/></linearGradient>
<linearGradient id="warmG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd9a8"/><stop offset="1" stop-color="#ff8a3d"/></linearGradient>
<radialGradient id="glowW"><stop offset="0" stop-color="#ffcf8a" stop-opacity="0.55"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=150, size=64):
    return "".join(
        f'<text class="hl" x="52" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=470):
    return (f'<g class="b"><circle cx="110" cy="{y}" r="48" fill="{RED}"/>'
            f'<text x="110" y="{y+15}" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def pipe_h(x, y, w, h=70, cls="p"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/>'
            f'<rect x="{x+6}" y="{y+14}" width="{w-12}" height="{h-28}" rx="8" fill="#2b6d8f" opacity="0.55"/></g>')


def pipe_v(x, y, h, w=70, cls="p"):
    return (f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="4"/>'
            f'<rect x="{x+14}" y="{y+6}" width="{w-28}" height="{h-12}" rx="8" fill="#2b6d8f" opacity="0.55"/></g>')


def jet(x, y, cls="jet", k=1.0):
    arcs = [(60, -140, 22), (10, -190, 16), (120, -100, 14), (-40, -170, 12), (170, -60, 10)]
    out = [f'<g class="{cls}">']
    for dx, dy, wd in arcs:
        out.append(f'<path d="M {x} {y} q {dx*k} {dy*k*0.6} {dx*2.2*k} {dy*k}" stroke="{WATER_L}" '
                   f'stroke-width="{wd}" fill="none" opacity="0.9" stroke-linecap="round"/>')
    out.append('</g>')
    return "".join(out)


def steam(n=8, cls="steam"):
    return "".join(
        f'<circle class="{cls}" cx="{300 + (i*97) % 520}" cy="{500 + (i*83) % 400}" r="{40 + i%4*16}" fill="{WHITE}" opacity="0.10"/>'
        for i in range(n))


def gauge(cx, cy, r=120, needle=-90, cls="needle"):
    ticks = "".join(
        f'<line x1="{cx}" y1="{cy-r+12}" x2="{cx}" y2="{cy-r+26}" stroke="#8fa3b1" stroke-width="5" transform="rotate({a} {cx} {cy})"/>'
        for a in range(-130, 131, 26))
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#0d161c" stroke="{STEEL_D}" stroke-width="8"/>{ticks}'
            f'<path d="M {cx+r*0.62} {cy-r*0.62} A {r*0.9} {r*0.9} 0 0 1 {cx+r*0.9} {cy+r*0.2}" stroke="{RED}" stroke-width="10" fill="none"/>'
            f'<g class="{cls}" transform="rotate({needle} {cx} {cy})"><rect x="{cx-4}" y="{cy-r+20}" width="8" height="{r-32}" rx="4" fill="{RED}"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="{INK}"/>')


def valve(cx, cy, r=44, cls="valve"):
    return (f'<g class="{cls}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{RED}" stroke-width="12"/>'
            f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{RED}" stroke-width="10"/>'
            f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}" stroke="{RED}" stroke-width="10"/>'
            f'<circle cx="{cx}" cy="{cy}" r="8" fill="{STEEL_D}"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # окно с морозом
    b.append(f'<rect x="60" y="240" width="420" height="420" rx="12" fill="#16323f" stroke="{STEEL_D}" stroke-width="8"/>')
    b.append(f'<text x="270" y="420" font-family="Nunito, Arial" font-size="90" font-weight="900" fill="{ICE}" text-anchor="middle">−20°</text>')
    for i in range(10):
        b.append(f'<circle class="snow" cx="{80 + (i*47) % 380}" cy="{260 + (i*61) % 360}" r="{3 + i%3}" fill="#dff4ff"/>')
    # стена и труба
    b.append(pipe_h(60, 1000, 900))
    b.append(pipe_v(890, 1000, 700))
    b.append(f'<rect x="880" y="990" width="90" height="90" fill="{STEEL_D}" opacity="0.6"/>')
    b.append(jet(900, 1010, "jet1", 1.15))
    b.append(f'<ellipse cx="900" cy="1690" rx="240" ry="40" fill="{WATER}" opacity="0.5"/>')
    b.append(steam(6, "steam1"))
    for i in range(14):
        b.append(f'<circle class="splash" cx="{900 + (i*37) % 260}" cy="{500 + (i*53) % 380}" r="{4 + i%4}" fill="{WATER_L}" opacity="0.7"/>')
    b.append(f'<rect x="0" y="1700" width="1080" height="220" fill="{WATER}" opacity="0.35"/>')
    b.append(title([("ТРУБА", INK), ("ЛОПНУЛА", RED)], 150, 72))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(pipe_h(80, 700, 920, 120))
    b.append(f'<rect x="360" y="700" width="300" height="120" fill="url(#iceG)" opacity="0.95"/>')
    for i in range(12):
        b.append(f'<path d="M {380 + i*24} 700 l 12 60 l -12 60" stroke="{WHITE}" stroke-width="4" fill="none" opacity="0.6"/>')
    for i in range(3):
        b.append(f'<path class="arrowOut" d="M 390 {760 + i*22} l -70 -26" stroke="{RED}" stroke-width="9"/>')
        b.append(f'<path class="arrowOut" d="M 640 {760 + i*22} l 70 -26" stroke="{RED}" stroke-width="9"/>')
    b.append(badge(1))
    b.append(title([("ВОДА", INK), ("РАСШИРЯЕТСЯ", RED)], 140, 60))
    b.append(f'<text x="540" y="1150" font-family="Nunito, Arial" font-size="150" font-weight="900" fill="{ICE}" text-anchor="middle">+9%</text>')
    b.append(f'<text x="540" y="1230" font-family="Nunito, Arial" font-size="36" font-weight="800" fill="{INK}" text-anchor="middle">лёд распирает трубу изнутри</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # угол трубы
    b.append(pipe_h(80, 760, 380))
    b.append(pipe_v(390, 760, 420))
    b.append(f'<rect x="330" y="700" width="140" height="140" fill="url(#iceG)" opacity="0.95"/>')
    for i in range(10):
        b.append(f'<path class="iceCrack" d="M {340 + i*12} 710 l 8 40 l -6 36" stroke="{WHITE}" stroke-width="3" fill="none" opacity="0.7"/>')
    b.append(gauge(800, 640, 140, -100, "needle3"))
    b.append(f'<text x="800" y="850" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{RED}" text-anchor="middle">ДАВЛЕНИЕ</text>')
    b.append(f'<text x="120" y="1300" font-family="Nunito, Arial" font-size="64" font-weight="900" fill="{ICE}">−20 °C</text>')
    b.append(badge(2, 470))
    b.append(title([("ЛЁД ВСТАЛ", INK), ("НА ПОВОРОТЕ", RED)], 140, 58))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(pipe_v(300, 300, 900, 80))
    b.append(f'<rect x="292" y="880" width="96" height="130" fill="{STEEL_D}"/>')
    b.append(jet(390, 900, "jet4", 1.35))
    b.append(jet(390, 1000, "jet4b", 0.9))
    b.append(f'<ellipse cx="520" cy="1620" rx="420" ry="60" fill="{WATER}" opacity="0.55"/>')
    b.append(steam(9, "steam4"))
    for i in range(20):
        b.append(f'<circle class="splash4" cx="{420 + (i*41) % 420}" cy="{700 + (i*57) % 500}" r="{4 + i%5}" fill="{WATER_L}" opacity="0.8"/>')
    b.append(f'<rect x="0" y="1560" width="1080" height="360" fill="{WATER}" opacity="0.45"/>')
    b.append(f'<ellipse cx="540" cy="1600" rx="520" ry="70" fill="{WATER_L}" opacity="0.25"/>')
    b.append(badge(3, 420))
    b.append(title([("РАЗРЫВ", RED), ("И ФОНТАН", INK)], 140, 70))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(pipe_h(80, 620, 420))
    b.append(pipe_v(430, 620, 380))
    b.append(valve(500, 580, 56, "v5"))
    b.append(f'<circle class="hand5" cx="620" cy="500" r="70" fill="#f2c9a4"/>')
    b.append(f'<path class="hand5" d="M 620 430 q 90 -40 140 20" stroke="#f2c9a4" stroke-width="34" fill="none" stroke-linecap="round"/>')
    # котёл выключен
    b.append(f'<rect x="700" y="1000" width="260" height="300" rx="16" fill="{STEEL}" stroke="{STEEL_D}" stroke-width="5"/>')
    b.append(f'<circle class="power" cx="830" cy="1150" r="46" fill="none" stroke="{RED}" stroke-width="8"/>')
    b.append(f'<line x1="830" y1="1110" x2="830" y2="1160" stroke="{RED}" stroke-width="8"/>')
    # слив
    b.append(f'<path class="drain" d="M 500 1000 l 0 300 q 0 40 40 40 l 200 0" stroke="{WATER}" stroke-width="14" fill="none" opacity="0.9"/>')
    for i in range(6):
        b.append(f'<circle class="drainD" cx="{545 + i*30}" cy="{1360 + i*14}" r="7" fill="{WATER_L}"/>')
    b.append(badge(4, 380))
    b.append(title([("ПЕРЕКРЫТЬ", INK), ("И СЛИТЬ", RED)], 140, 60))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(pipe_h(120, 800, 840, 100))
    b.append(f'<rect x="380" y="790" width="240" height="120" fill="url(#iceG)"/>')
    b.append(f'<g class="heater"><rect x="700" y="1080" width="280" height="220" rx="20" fill="{STEEL}" stroke="{STEEL_D}" stroke-width="5"/>'
             f'<g class="coil">' + "".join(f'<line x1="{730 + i*22}" y1="1120" x2="{730 + i*22}" y2="1260" stroke="{WARM}" stroke-width="12"/>' for i in range(9)) + '</g>'
             f'<circle cx="840" cy="1330" r="150" fill="url(#glowW)"/></g>')
    for i in range(7):
        b.append(f'<path class="warmAir" d="M {700 - i*70} 1000 q -40 -60 0 -120" stroke="{WARM}" stroke-width="8" fill="none" opacity="0.6"/>')
    b.append(f'<g class="melt">' + "".join(
        f'<circle cx="{400 + i*30}" cy="{930 + i*18}" r="8" fill="{WATER_L}" opacity="0.9"/>' for i in range(6)) + '</g>')
    b.append(badge(5, 400))
    b.append(title([("ПРОГРЕВ", INK), ("БЕЗ ОГНЯ", RED)], 140, 62))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(pipe_h(100, 760, 880, 100))
    b.append(f'<rect x="100" y="740" width="880" height="140" rx="30" fill="{WARM}" opacity="0.25"/>')
    for i in range(9):
        b.append(f'<path d="M {140 + i*100} 740 q 20 -26 40 0" stroke="{WARM}" stroke-width="6" fill="none" opacity="0.6"/>')
    b.append(f'<rect x="360" y="980" width="360" height="220" rx="24" fill="{STEEL}" stroke="{STEEL_D}" stroke-width="5"/>')
    b.append(f'<text x="540" y="1070" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{INK}" text-anchor="middle">ТЕРМОСТАТ</text>')
    b.append(f'<text x="540" y="1150" font-family="Nunito, Arial" font-size="64" font-weight="900" fill="{WARM}" text-anchor="middle">+15°</text>')
    b.append(badge(6, 380))
    b.append(title([("НЕ ВЫКЛЮЧАТЬ", INK), ("В МОРОЗ", RED)], 140, 56))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="260" font-family="Nunito, Arial" font-size="54" font-weight="900" fill="{INK}" text-anchor="middle">ДО МОРОЗОВ</text>')
    items = ["утеплить трубы", "держать +15 в доме", "не выключать котёл", "проверить краны и слив"]
    for i, t in enumerate(items):
        y = 470 + i * 200
        b.append(f'<g class="row r{i}"><circle cx="150" cy="{y}" r="42" fill="{WATER}"/>'
                 f'<text x="150" y="{y+14}" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#fff" text-anchor="middle">{i+1}</text>'
                 f'<text x="225" y="{y+12}" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{INK}">{t}</text></g>')
    b.append(f'<text x="540" y="1470" font-family="Nunito, Arial" font-size="44" font-weight="900" fill="{RED}" text-anchor="middle">ПЕРЕКРОЙ · СЛЕЙ · ПРОГРЕЙ</text>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]


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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
    tl.fromTo(".b", {{ scale:0.5, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.35, ease:"back.out(3)" }}, 0.2);
    tl.to(".snow", {{ y:120, x:14, duration:3.0, stagger:0.05, repeat:3, ease:"none" }}, 0);
    tl.to(".jet1", {{ scaleY:1.12, transformOrigin:"0% 100%", duration:0.18, yoyo:true, repeat:20, ease:"none" }}, 0);
    tl.to(".splash", {{ y:-140, x:30, opacity:0, duration:1.4, stagger:0.05, repeat:4, ease:"power1.out" }}, 0);
    tl.to(".steam1, .steam4", {{ y:-120, opacity:0, duration:2.4, stagger:0.08, repeat:4 }}, 0);
    tl.to(".arrowOut", {{ x:-10, duration:0.5, yoyo:true, repeat:10 }}, 0);
    tl.to(".iceCrack", {{ opacity:0.25, duration:0.6, yoyo:true, repeat:10, stagger:0.05 }}, 0);
    tl.to(".needle3", {{ rotation:-10, svgOrigin:"800 640", duration:0.5, yoyo:true, repeat:12, ease:"none" }}, 0);
    tl.to(".jet4", {{ scaleX:1.1, transformOrigin:"0% 0%", duration:0.16, yoyo:true, repeat:22 }}, 0);
    tl.to(".jet4b", {{ scaleY:1.08, transformOrigin:"0% 0%", duration:0.2, yoyo:true, repeat:18 }}, 0);
    tl.to(".splash4", {{ y:-180, x:40, opacity:0, duration:1.2, stagger:0.04, repeat:5, ease:"power1.out" }}, 0);
    tl.to(".v5", {{ rotation:180, svgOrigin:"500 580", duration:1.0, ease:"power2.inOut" }}, 0.2);
    tl.to(".hand5", {{ x:-40, y:20, duration:1.0, ease:"power2.inOut" }}, 0.2);
    tl.to(".power", {{ scale:0.85, transformOrigin:"50% 50%", duration:0.3, yoyo:true, repeat:4 }}, 0.6);
    tl.to(".drainD", {{ y:120, opacity:0, duration:1.6, stagger:0.15, repeat:3 }}, 0.8);
    tl.to(".warmAir", {{ x:120, opacity:0.2, duration:1.6, stagger:0.12, repeat:3 }}, 0);
    tl.to(".coil", {{ opacity:0.6, duration:0.6, yoyo:true, repeat:8 }}, 0);
    tl.to(".melt", {{ y:70, opacity:0, duration:2.0, repeat:2 }}, 0.4);
    tl.fromTo(".row", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.25 }}, 0.2);
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
