#!/usr/bin/env python3
"""«Почему радиатор холодный» — 8 сцен, объяснение по шагам."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/heating")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(8):
    end = STARTS[i + 1] if i + 1 < 8 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#eef2f5"
INK = "#22303a"
STEEL = "#8fa3b1"
STEEL_D = "#6d8290"
HOT = "#d1502f"
HOT_L = "#f08a5d"
COLD = "#5d8fae"
WATER = "#3f9fd4"
RED = "#c0392b"
GREEN = "#2f8f5b"

DEFS = """<defs>
<linearGradient id="steelG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8c7d1"/><stop offset="0.5" stop-color="#e2ebf0"/><stop offset="1" stop-color="#8fa3b1"/></linearGradient>
<linearGradient id="hotG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4a07a"/><stop offset="1" stop-color="#c9542f"/></linearGradient>
<linearGradient id="coldG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8cde2"/><stop offset="1" stop-color="#4d7f9e"/></linearGradient>
<radialGradient id="flameG"><stop offset="0" stop-color="#fff0b0"/><stop offset="0.5" stop-color="#ffb03a"/><stop offset="1" stop-color="#d1502f" stop-opacity="0"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=150, size=62):
    return "".join(
        f'<text class="hl" x="52" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=470):
    return (f'<g class="b"><circle cx="112" cy="{y}" r="50" fill="{INK}"/>'
            f'<text x="112" y="{y+16}" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def boiler(x, y, w=230, h=300, hot=True):
    return (f'<g class="boiler"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="5"/>'
            f'<rect x="{x+18}" y="{y+24}" width="{w-36}" height="96" rx="10" fill="#1f2a33"/>'
            f'<text x="{x+w/2}" y="{y+108}" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{HOT_L}" text-anchor="middle">КОТЁЛ</text>'
            f'<g class="flameG"><ellipse cx="{x+w/2}" cy="{y+h-70}" rx="62" ry="76" fill="url(#flameG)"/></g>'
            f'<rect x="{x+w/2-8}" y="{y-30}" width="16" height="34" fill="{STEEL_D}"/></g>')


def radiator(x, y, fins=7, w=42, h=280, hot=True):
    g = f'<g class="rad">'
    g += f'<rect x="{x-10}" y="{y-14}" width="{fins*w+20}" height="18" rx="8" fill="{STEEL_D}"/>'
    for i in range(fins):
        fill = "url(#hotG)" if hot else "url(#coldG)"
        g += f'<rect x="{x + i*w}" y="{y}" width="{w-8}" height="{h}" rx="10" fill="{fill}" stroke="{STEEL_D}" stroke-width="3"/>'
    g += f'<rect x="{x-10}" y="{y+h-4}" width="{fins*w+20}" height="18" rx="8" fill="{STEEL_D}"/></g>'
    return g


def valve(cx, cy, r=46, cls="valve"):
    return (f'<g class="{cls}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{HOT}" stroke-width="12"/>'
            f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}" stroke="{HOT}" stroke-width="10"/>'
            f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}" stroke="{HOT}" stroke-width="10"/>'
            f'<circle cx="{cx}" cy="{cy}" r="9" fill="{STEEL_D}"/></g>')


def manometer(cx, cy, r=120, needle=-30, cls="mn"):
    ticks = "".join(
        f'<line x1="{cx}" y1="{cy-r+12}" x2="{cx}" y2="{cy-r+28}" stroke="#5b6b76" stroke-width="5" transform="rotate({a} {cx} {cy})"/>'
        for a in range(-120, 121, 30))
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{STEEL_D}" stroke-width="9"/>{ticks}'
            f'<g class="{cls}" transform="rotate({needle} {cx} {cy})"><rect x="{cx-4}" y="{cy-r+22}" width="8" height="{r-34}" rx="4" fill="{RED}"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="10" fill="{INK}"/></g>')


def flow(x1, x2, y, n=6, cls="flowH"):
    return "".join(f'<circle class="{cls}" cx="{x1 + i*(x2-x1)/n}" cy="{y}" r="10" fill="{WATER}"/>' for i in range(n))


def footnote(text, y=1580, size=34):
    return (f'<g class="fn"><rect x="52" y="{y-56}" width="976" height="{size*2+40}" rx="18" fill="#ffffff" opacity="0.75"/>'
            f'<text x="80" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" font-weight="800" fill="{INK}">{text}</text></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(boiler(100, 700))
    b.append(f'<path d="M 215 670 L 215 520 L 760 520" stroke="{HOT}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M 330 1000 L 330 1180 L 760 1180" stroke="{COLD}" stroke-width="26" fill="none" stroke-linecap="round"/>')
    b.append(radiator(760, 470, 6, 44, 360, hot=False))
    b.append(f'<text x="900" y="890" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{COLD}" text-anchor="middle">ХОЛОДНАЯ</text>')
    b.append(f'<text x="215" y="660" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{HOT}" text-anchor="middle">ГОРЯЧО</text>')
    b.append(title([("КОТЁЛ РАБОТАЕТ,", INK), ("БАТАРЕЯ ХОЛОДНАЯ", RED)], 150, 56))
    b.append(f'<text x="52" y="330" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}">пять причин — по порядку</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(boiler(90, 820, 200, 250))
    b.append(f'<path d="M 290 900 L 400 900" stroke="{HOT}" stroke-width="24"/>')
    b.append(f'<circle cx="460" cy="900" r="52" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="5"/>')
    b.append(f'<g class="imp"><path d="M 460 862 l 30 26 l -30 26 l -30 -26 z" fill="{HOT}"/></g>')
    b.append(f'<text x="460" y="1010" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{INK}" text-anchor="middle">НАСОС</text>')
    b.append(f'<path d="M 512 900 L 720 900 L 720 700" stroke="{HOT}" stroke-width="24" fill="none"/>')
    b.append(radiator(700, 430, 5, 40, 240, hot=True))
    b.append(f'<path d="M 700 760 L 700 1180 L 400 1180 L 400 1070" stroke="{COLD}" stroke-width="24" fill="none"/>')
    b.append(f'<text x="560" y="1240" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{COLD}" text-anchor="middle">ОБРАТКА</text>')
    b.append(flow(300, 420, 900, 3, "f1"))
    b.append(flow(540, 700, 900, 3, "f2"))
    b.append(flow(450, 690, 1180, 3, "f3"))
    b.append(title([("КАК ЭТО", INK), ("РАБОТАЕТ", GREEN)], 140, 62))
    b.append(footnote("котёл → насос → радиатор → обратка"))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(radiator(200, 540, 7, 52, 520, hot=True))
    b.append(f'<rect x="210" y="546" width="350" height="96" fill="#ffffff" opacity="0.5"/>')
    b.append(f'<text x="385" y="606" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{COLD}" text-anchor="middle">ВОЗДУХ</text>')
    b.append(valve(540, 580, 40, "bleed"))
    for i in range(6):
        b.append(f'<circle class="bub" cx="{520 + i*8}" cy="{520 - i*26}" r="{6 + i%3*3}" fill="#ffffff" stroke="{STEEL_D}" stroke-width="2"/>')
    b.append(f'<g class="hiss">' + "".join(
        f'<path d="M {560 + i*36} 520 q 14 -18 0 -36" stroke="{STEEL}" stroke-width="5" fill="none" opacity="0.7"/>' for i in range(5)) + '</g>')
    b.append(badge(1))
    b.append(title([("ВОЗДУХ", INK), ("В РАДИАТОРЕ", RED)], 140, 60))
    b.append(f'<text x="52" y="300" font-family="Nunito, Arial" font-size="30" font-weight="800" fill="{INK}">кран Маевского → спустить воздух</text>')
    b.append(footnote("воздух собирается сверху и запирает воду"))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<circle cx="420" cy="900" r="150" fill="url(#steelG)" stroke="{STEEL_D}" stroke-width="6"/>')
    b.append(f'<g class="imp2"><path d="M 420 810 l 60 50 l -60 50 l -60 -50 z" fill="{HOT}"/></g>')
    b.append(f'<text x="420" y="1100" font-family="Nunito, Arial" font-size="30" font-weight="900" fill="{INK}" text-anchor="middle">НАСОС</text>')
    # шкала скоростей
    for i in range(3):
        y = 620 + i * 90
        b.append(f'<rect x="700" y="{y}" width="{120 + i*60}" height="46" rx="10" fill="{HOT if i < 1 else "#c9d4dc"}"/>')
        b.append(f'<text x="880" y="{y+34}" font-family="Nunito, Arial" font-size="26" font-weight="900" fill="{INK}">{"I"*(i+1)}</text>')
    b.append(f'<text x="700" y="580" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{RED}">СКОРОСТЬ</text>')
    b.append(f'<path class="arrowW" d="M 540 960 L 660 960" stroke="{WATER}" stroke-width="10"/>')
    b.append(badge(2))
    b.append(title([("НАСОС НА", INK), ("МИНИМУМЕ", RED)], 140, 60))
    b.append(footnote("на первой скорости поток не доходит до конца"))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<path d="M 120 520 L 900 520 L 900 700" stroke="{HOT}" stroke-width="22" fill="none"/>')
    b.append(f'<path d="M 900 700 L 900 1120" stroke="{HOT}" stroke-width="22"/>')
    b.append(radiator(160, 560, 4, 44, 220, hot=True))
    b.append(radiator(820, 760, 4, 44, 220, hot=False))
    b.append(valve(360, 560, 36, "v1"))
    b.append(valve(960, 800, 36, "v2"))
    b.append(f'<text x="260" y="880" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{HOT}">БЛИЖНИЙ: ГОРЯЧИЙ</text>')
    b.append(f'<text x="700" y="1120" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{COLD}">ДАЛЬНИЙ: ХОЛОДНЫЙ</text>')
    b.append(badge(3))
    b.append(title([("РАЗБАЛАНСИРОВКА", INK)], 140, 56))
    b.append(footnote("ближний радиатор забирает почти весь поток"))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="120" y="620" width="840" height="120" rx="60" fill="#dbe6ec" stroke="{STEEL_D}" stroke-width="6"/>')
    b.append(f'<rect class="mud" x="140" y="660" width="800" height="40" rx="20" fill="#8a6a3a" opacity="0.85"/>')
    for i in range(14):
        b.append(f'<circle class="sed" cx="{160 + (i*63) % 760}" cy="{676 + (i%3)*12}" r="{5 + i%4}" fill="#6b4a2a"/>')
    b.append(f'<rect x="380" y="820" width="320" height="380" rx="18" fill="#dbe6ec" stroke="{STEEL_D}" stroke-width="6"/>')
    b.append(f'<rect x="410" y="860" width="260" height="300" rx="10" fill="#a97b4a" class="cartr"/>')
    b.append(f'<text x="540" y="1260" font-family="Nunito, Arial" font-size="28" font-weight="900" fill="{INK}" text-anchor="middle">ФИЛЬТР</text>')
    b.append(badge(4))
    b.append(title([("ГРЯЗЬ И ИЛ", INK)], 140, 60))
    b.append(f'<text x="52" y="300" font-family="Nunito, Arial" font-size="30" font-weight="800" fill="{INK}">проход сужается, поток падает</text>')
    b.append(footnote("ил оседает внизу и сужает проход"))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="120" y="380" width="840" height="620" rx="20" fill="#f7fafc" stroke="{STEEL_D}" stroke-width="5"/>')
    for i in range(3):
        b.append(f'<rect x="160" y="{420 + i*190}" width="760" height="10" fill="{STEEL}" opacity="0.5"/>')
        b.append(radiator(680, 440 + i*190, 3, 34, 120, hot=(i < 2)))
    b.append(manometer(340, 800, 120, -95, "mn7"))
    b.append(f'<text x="340" y="980" font-family="Nunito, Arial" font-size="32" font-weight="900" fill="{RED}" text-anchor="middle">0,8 бар</text>')
    b.append(badge(5))
    b.append(title([("НИЗКОЕ", INK), ("ДАВЛЕНИЕ", RED)], 140, 60))
    b.append(footnote("0,8 бар мало для двух этажей"))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="260" font-family="Nunito, Arial" font-size="58" font-weight="900" fill="{INK}" text-anchor="middle">ПРОВЕРЬ ПО ПОРЯДКУ</text>')
    items = ["воздух — кран Маевского", "насос — скорость II–III", "балансировка радиаторов", "грязь — промыть, почистить фильтр", "давление — подпитка и утечки"]
    for i, t in enumerate(items):
        y = 430 + i * 205
        b.append(f'<g class="row r{i}"><circle cx="150" cy="{y}" r="44" fill="{GREEN}"/>'
                 f'<text x="150" y="{y+14}" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="#fff" text-anchor="middle">{i+1}</text>'
                 f'<text x="230" y="{y+12}" font-family="Nunito, Arial" font-size="38" font-weight="900" fill="{INK}">{t}</text></g>')
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
    tl.fromTo(".b", {{ scale:0.6, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.4, ease:"back.out(2)" }}, 0.2);
    tl.to(".flameG", {{ scaleY:1.12, transformOrigin:"50% 100%", duration:0.4, yoyo:true, repeat:14, ease:"sine.inOut" }}, 0);
    tl.to(".f1", {{ x:150, duration:1.6, stagger:0.1, repeat:8, ease:"none" }}, 0);
    tl.to(".f2", {{ x:170, duration:1.6, stagger:0.12, repeat:8, ease:"none" }}, 0);
    tl.to(".f3", {{ x:-190, duration:1.8, stagger:0.12, repeat:8, ease:"none" }}, 0);
    tl.to(".imp", {{ rotation:360, svgOrigin:"460 900", duration:2.4, repeat:6, ease:"none" }}, 0);
    tl.to(".imp2", {{ rotation:360, svgOrigin:"420 900", duration:6.0, repeat:2, ease:"none" }}, 0);
    tl.to(".bleed", {{ rotation:90, svgOrigin:"540 580", duration:1.4, ease:"power2.out" }}, 0.3);
    tl.to(".bub", {{ y:-200, opacity:0, duration:1.6, stagger:0.1, repeat:2, ease:"power1.out" }}, 0.3);
    tl.to(".hiss", {{ opacity:0.2, duration:0.5, yoyo:true, repeat:8 }}, 0.4);
    tl.to(".v1", {{ rotation:-40, svgOrigin:"360 560", duration:2.0, ease:"power2.out" }}, 0.3);
    tl.to(".v2", {{ rotation:60, svgOrigin:"960 800", duration:2.2, ease:"power2.out" }}, 0.5);
    tl.to(".sed", {{ x:40, y:6, duration:2.2, yoyo:true, repeat:2, stagger:0.05, ease:"sine.inOut" }}, 0);
    tl.to(".mud", {{ opacity:0.95, duration:2.0, yoyo:true, repeat:1 }}, 0);
    tl.to(".cartr", {{ fill:"#7d5630", duration:4.0, ease:"none" }}, 0);
    tl.to(".mn7", {{ rotation:-85, svgOrigin:"340 800", duration:1.6, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0);
    tl.fromTo(".row", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.3 }}, 0.2);
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
