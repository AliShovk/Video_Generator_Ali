#!/usr/bin/env python3
"""«Тёплый пол» — 8 сцен, 45 с, 9:16. Иконки из локального кэша Iconify."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/root/video-gen")
from icons import icon

ROOT = Path("/root/video-gen/warmfloor")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#f2f5f7"
INK = "#1f2c36"
GREY = "#d7dee4"
GREY_D = "#a9b6c0"
TILE = "#e9e2d4"
SCREED = "#cfc7b8"
INSUL = "#f2c14e"
PIPE = "#c0392b"
HOT = "#e0642f"
COLD = "#4d8fae"
GREEN = "#2c8a58"
RED = "#c0392b"

DEFS = """<defs>
<linearGradient id="hotG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffb37a"/><stop offset="1" stop-color="#e0642f"/></linearGradient>
<linearGradient id="insG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd98a"/><stop offset="1" stop-color="#e8a63a"/></linearGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=150, size=62):
    return "".join(
        f'<text class="hl" x="52" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=440):
    return (f'<g class="b"><circle cx="106" cy="{y}" r="44" fill="{INK}"/>'
            f'<text x="106" y="{y+14}" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def coil(x, y, w, rows=6, gap=46, color=PIPE):
    """Змеевик: горизонтальные ряды + повороты."""
    out = [f'<g class="coilG" stroke="{color}" stroke-width="10" fill="none" stroke-linecap="round">']
    for i in range(rows):
        yy = y + i * gap
        x1, x2 = (x, x + w) if i % 2 == 0 else (x + w, x)
        out.append(f'<line x1="{x1}" y1="{yy}" x2="{x2}" y2="{yy}"/>')
        if i < rows - 1:
            xr = x + w if i % 2 == 0 else x
            out.append(f'<path d="M {xr} {yy} q {28 if i%2==0 else -28} {gap/2} 0 {gap}"/>')
    out.append("</g>")
    return "".join(out)


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="0" y="900" width="1080" height="1020" fill="{GREY}"/>')
    b.append(f'<rect x="0" y="900" width="1080" height="40" fill="{GREY_D}"/>')
    # ступни
    b.append(f'<g class="feet"><ellipse cx="470" cy="1040" rx="46" ry="86" fill="#f2c9a4"/>'
             f'<ellipse cx="600" cy="1050" rx="46" ry="86" fill="#f2c9a4"/>'
             f'<circle cx="470" cy="960" r="26" fill="#f2c9a4"/><circle cx="600" cy="968" r="26" fill="#f2c9a4"/></g>')
    b.append(icon("mdi-thermometer-low", 800, 980, 150, COLD))
    b.append(f'<text x="875" y="1180" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{COLD}" text-anchor="middle">+18°</text>')
    for i in range(6):
        b.append(f'<path class="coldWave" d="M {180 + i*130} 1120 q 24 -40 0 -80" stroke="{COLD}" stroke-width="7" fill="none" opacity="0.5"/>')
    b.append(title([("ПОЛ", INK), ("ХОЛОДНЫЙ", RED)], 160, 76))
    b.append(f'<text x="54" y="380" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">а счёт за отопление растёт</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    layers = [
        ("плитка", TILE, 120, 130, INK),
        ("стяжка с трубой", SCREED, 120, 230, INK),
        ("утеплитель", INSUL, 120, 200, "#7a5a10"),
        ("плита-основание", GREY_D, 120, 170, "#ffffff"),
    ]
    y = 560
    for name, col, x, h, tc in layers:
        b.append(f'<g class="lay"><rect x="{x}" y="{y}" width="840" height="{h}" rx="6" fill="{col}" stroke="#ffffff" stroke-width="4"/>'
                 f'<text x="{x+30}" y="{y+h/2+12}" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{tc}">{name}</text></g>')
        y += h
    b.append(coil(300, 700, 480, 3, 46, PIPE))
    b.append(icon("mdi-layers", 60, 470, 92, INK))
    b.append(f'<g class="heatUp">' + "".join(
        f'<path d="M {200 + i*120} 1500 q 26 -46 0 -92" stroke="{HOT}" stroke-width="9" fill="none" opacity="0.8"/>' for i in range(7)) + '</g>')
    b.append(f'<text x="540" y="1640" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{INK}" text-anchor="middle">без утеплителя греем подвал</text>')
    b.append(title([("ПИРОГ", INK), ("ПОЛА", GREEN)], 150, 64))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="90" y="620" width="900" height="760" rx="12" fill="#e4e9ee"/>')
    b.append(coil(160, 700, 760, 9, 74, PIPE))
    b.append(f'<line x1="160" y1="1600" x2="310" y2="1600" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<line x1="160" y1="1580" x2="160" y2="1620" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<line x1="310" y1="1580" x2="310" y2="1620" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<text x="235" y="1660" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="{INK}" text-anchor="middle">10–15 СМ</text>')
    b.append(badge(1, 430))
    b.append(title([("ШАГ", INK), ("ТРУБЫ", GREEN)], 150, 64))
    b.append(f'<text x="54" y="360" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">у окон — 10 см, в центре — 15 см</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="120" y="640" width="840" height="90" rx="14" fill="{GREY_D}"/>')
    for i in range(4):
        x = 190 + i * 200
        b.append(f'<circle cx="{x}" cy="685" r="30" fill="#ffffff" stroke="{INK}" stroke-width="4"/>')
        b.append(f'<line x1="{x}" y1="685" x2="{x+14}" y2="672" stroke="{RED}" stroke-width="4"/>')
    for i in range(3):
        y = 800 + i * 170
        b.append(coil(200, y, 400, 2, 40, PIPE if i else HOT))
        b.append(f'<text x="680" y="{y+50}" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{INK}">контур {i+1}</text>')
    b.append(icon("mdi-gauge", 700, 560, 90, INK))
    b.append(badge(2, 430))
    b.append(title([("КОЛЛЕКТОР", INK), ("ПЕТЛИ", GREEN)], 150, 56))
    b.append(f'<text x="54" y="1560" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">длина петли — 80–100 м, не больше</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="0" y="520" width="200" height="1200" fill="{GREY_D}"/>')
    b.append(f'<rect x="200" y="700" width="760" height="260" rx="8" fill="{SCREED}"/>')
    b.append(f'<rect x="200" y="700" width="760" height="18" fill="#bdb4a4"/>')
    b.append(f'<path class="crack5" d="M 210 720 l 30 90 l -14 80 l 40 70" stroke="{RED}" stroke-width="10" fill="none"/>')
    b.append(f'<text x="420" y="620" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{RED}">НЕТ ЛЕНТЫ → ТРЕЩИНА</text>')
    b.append(icon("mdi-alert-circle", 60, 420, 90, RED))
    b.append(badge(3, 420))
    b.append(title([("ДЕМПФЕРНАЯ", INK), ("ЛЕНТА", RED)], 150, 58))
    b.append(f'<text x="240" y="1120" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">по периметру, у стен и колонн</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="80" y="560" width="920" height="820" rx="12" fill="#e4e9ee"/>')
    for i in range(9):
        y = 580 + i * 88
        col = HOT if i % 2 == 0 else "#8fb8cc"
        b.append(f'<rect class="stripe" x="100" y="{y}" width="880" height="60" fill="{col}" opacity="{0.75 if i%2==0 else 0.45}"/>')
    b.append(f'<text x="540" y="1460" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{RED}" text-anchor="middle">тепло · холодно · тепло</text>')
    b.append(badge(4, 420))
    b.append(title([("ШАГ 30 СМ", INK), ("ПОЛОСАТЫЙ ПОЛ", RED)], 150, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="120" y="520" width="300" height="200" rx="16" fill="#ffffff" stroke="{GREY_D}" stroke-width="5"/>')
    b.append(icon("mdi-thermostat", 160, 545, 110, INK))
    b.append(f'<text x="290" y="620" font-family="Nunito, Arial" font-size="56" font-weight="900" fill="{INK}">+24°</text>')
    b.append(f'<path d="M 270 720 l 0 180" stroke="{GREY_D}" stroke-width="10"/>')
    b.append(f'<rect x="120" y="1100" width="840" height="240" rx="12" fill="{SCREED}"/>')
    b.append(f'<path d="M 130 1220 q 40 -30 80 0 q 40 30 80 0 q 40 -30 80 0 q 40 30 80 0 q 40 -30 80 0 q 40 30 80 0 q 40 -30 80 0 q 40 30 80 0" stroke="{GREY_D}" stroke-width="18" fill="none"/>')
    b.append(f'<circle class="sensor" cx="560" cy="1220" r="16" fill="{RED}"/>')
    b.append(f'<text x="700" y="1300" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{INK}">датчик в гофре</text>')
    b.append(badge(5, 420))
    b.append(title([("ТЕРМОСТАТ", INK), ("И ДАТЧИК", GREEN)], 150, 56))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="280" font-family="Nunito, Arial" font-size="54" font-weight="900" fill="{INK}" text-anchor="middle">ЗАПУСК</text>')
    days = [15, 20, 25, 30, 35, 40]
    for i, t in enumerate(days):
        h = 60 + i * 90
        x = 120 + i * 140
        b.append(f'<g class="day"><rect x="{x}" y="{1300 - h}" width="100" height="{h}" rx="8" fill="{HOT}" opacity="{0.35 + i*0.1}"/>'
                 f'<text x="{x+50}" y="{1340}" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">{t}°</text></g>')
    b.append(f'<text x="540" y="1460" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{INK}" text-anchor="middle">+5° в день, шесть дней</text>')
    b.append(icon("mdi-check-circle", 430, 1540, 90, GREEN))
    b.append(f'<text x="540" y="1690" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}" text-anchor="middle">резкий прогрев = трещины в стяжке</text>')
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
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.04, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1 }}, 0.05);
    tl.fromTo(".b", {{ scale:0.5, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.35, ease:"back.out(3)" }}, 0.15);
    tl.to(".coldWave", {{ y:-20, opacity:0.25, duration:1.4, yoyo:true, repeat:6, stagger:0.08 }}, 0);
    tl.to(".feet", {{ y:6, duration:1.0, yoyo:true, repeat:8, ease:"sine.inOut" }}, 0);
    tl.to(".heatUp", {{ y:-24, opacity:0.5, duration:1.6, yoyo:true, repeat:4 }}, 0);
    tl.to(".lay", {{ x:10, duration:0.6, yoyo:true, repeat:6, stagger:0.12 }}, 0);
    tl.to(".coilG", {{ opacity:0.75, duration:1.2, yoyo:true, repeat:4 }}, 0);
    tl.to(".crack5", {{ opacity:0.3, duration:0.5, yoyo:true, repeat:10 }}, 0);
    tl.to(".stripe", {{ opacity:0.9, duration:1.0, yoyo:true, repeat:4, stagger:0.05 }}, 0);
    tl.to(".sensor", {{ scale:1.6, transformOrigin:"50% 50%", duration:0.8, yoyo:true, repeat:5 }}, 0);
    tl.fromTo(".day", {{ scaleY:0, transformOrigin:"50% 100%" }}, {{ scaleY:1, duration:0.5, stagger:0.25, ease:"power2.out" }}, 0.2);
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
