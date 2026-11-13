#!/usr/bin/env python3
"""«5 ошибок с плиткой» — 7 сцен, 30 с, 9:16."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/tile-errors")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
BOUNDS = []
for i in range(7):
    end = STARTS[i + 1] if i + 1 < 7 else TOTAL
    BOUNDS.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG = "#eef1f3"
WALL = "#d8d2c6"
WALL_D = "#c2bbac"
TILE = "#f8f6f1"
TILE_D = "#dcd7cb"
GLUE = "#b3ab9c"
GLUE_D = "#8f8778"
RED = "#c0392b"
GREEN = "#2f8f5b"
INK = "#26313a"
GREY = "#6c7a86"

DEFS = """<defs>
<linearGradient id="tileG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e8e4da"/></linearGradient>
<linearGradient id="glueG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bdb5a6"/><stop offset="1" stop-color="#948c7d"/></linearGradient>
<linearGradient id="metalG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9aa6b0"/><stop offset="0.5" stop-color="#cfd8de"/><stop offset="1" stop-color="#8b97a1"/></linearGradient>
<radialGradient id="dropG"><stop offset="0" stop-color="#9fd8ff"/><stop offset="1" stop-color="#5aa9d6"/></radialGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=200, size=72):
    return "".join(
        f'<text class="hl" x="54" y="{y + i*(size+18)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def badge(n, y=560, cls=""):
    return (f'<g class="{cls}"><circle cx="120" cy="{y}" r="56" fill="{INK}"/>'
            f'<text x="120" y="{y+20}" font-family="Nunito, Arial" font-size="46" font-weight="900" fill="#fff" text-anchor="middle">{n}</text></g>')


def tile(x, y, w, h, rotate=0, ident="", crack=False):
    c = (f'<path class="crackT" d="M {x+w*0.2} {y+h*0.4} l {w*0.16} {h*0.12} l {-w*0.06} {h*0.14} l {w*0.2} {h*0.1}" '
         f'stroke="{RED}" stroke-width="6" fill="none" opacity="0.85"/>') if crack else ""
    return (f'<g id="{ident}" transform="rotate({rotate} {x+w/2} {y+h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="url(#tileG)" stroke="{TILE_D}" stroke-width="4"/>'
            f'<rect x="{x+10}" y="{y+10}" width="{w-20}" height="{h-20}" rx="4" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.7"/>'
            f'{c}</g>')


def comb(x, y, teeth=8, height=120, gap=26):
    """Гребёнка: зубцы вверх."""
    out = [f'<rect x="{x}" y="{y}" width="{teeth*gap}" height="18" fill="url(#metalG)"/>']
    for i in range(teeth):
        out.append(f'<rect class="tooth" x="{x + i*gap}" y="{y-height}" width="{gap*0.55}" height="{height}" fill="url(#metalG)"/>')
    out.append(f'<rect x="{x+teeth*gap/2-16}" y="{y+18}" width="32" height="90" rx="10" fill="#5b4a3a"/>')
    return "".join(out)


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="#c9c0b0"/>')
    b.append(f'<ellipse class="shadow" cx="530" cy="1350" rx="170" ry="34" fill="#8a8172" opacity="0.35"/>')
    for r in range(6):
        for c in range(5):
            b.append(tile(120 + c * 170, 760 + r * 170, 160, 160))
    b.append(tile(400, 1080, 260, 260, rotate=14, ident="falling", crack=True))
    b.append(f'<g class="dustF">' + "".join(
        f'<circle class="dustc" cx="{340 + (i*53) % 380}" cy="{1240 + (i%5)*40}" r="{10 + i%4*7}" fill="{WALL_D}" opacity="0.55"/>' for i in range(14)) + '</g>')
    b.append(title([("5 ОШИБОК", INK), ("ИЗ-ЗА КОТОРЫХ", INK), ("ПЛИТКА ОТВАЛИВАЕТСЯ", RED)], 200, 62))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # разрез: стена / клей / плитка
    b.append(f'<rect x="0" y="700" width="1080" height="900" fill="{WALL}"/>')
    b.append(f'<rect x="0" y="700" width="1080" height="900" fill="url(#glueG)" opacity="0"/>')
    for i in range(40):
        b.append(f'<circle cx="{40 + (i*97) % 1000}" cy="{740 + (i*131) % 820}" r="{5 + i%4}" fill="{WALL_D}"/>')
    b.append(f'<rect x="0" y="1180" width="1080" height="120" fill="url(#glueG)"/>')
    b.append(tile(120, 1120, 840, 120))
    # капли, уходящие в стену
    for i in range(9):
        b.append(f'<path class="drop" d="M {150 + i*95} 1200 q 18 46 0 86 q -18 -40 0 -86" fill="url(#dropG)" opacity="0.9"/>')
        b.append(f'<path class="suck" d="M {150 + i*95} 1300 l 0 60" stroke="#5aa9d6" stroke-width="6" opacity="0.55"/>')
    b.append(badge(1, 520, "b1"))
    b.append(f'<g class="noRoller"><rect x="700" y="520" width="300" height="24" rx="10" fill="{GREY}"/>'
             f'<rect x="780" y="544" width="140" height="60" rx="10" fill="#e8e4da"/></g>')
    b.append(f'<path class="cross" d="M 760 470 l 180 180 M 940 470 l -180 180" stroke="{RED}" stroke-width="16" stroke-linecap="round" opacity="0.9"/>')
    b.append(title([("НЕТ ГРУНТОВКИ", RED)], 250, 60))
    b.append(f'<text x="54" y="330" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">клей ушёл в стену</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(tile(120, 700, 400, 500))
    b.append(tile(520, 700, 400, 500))
    b.append(f'<rect x="518" y="700" width="4" height="500" fill="{WALL_D}"/>')
    # стрелки навстречу
    b.append(f'<g class="arrows"><path d="M 300 950 l 120 0" stroke="{RED}" stroke-width="14"/>'
             f'<path d="M 420 950 l -34 -26 l 0 52 z" fill="{RED}"/>'
             f'<path d="M 900 950 l -120 0" stroke="{RED}" stroke-width="14"/>'
             f'<path d="M 780 950 l 34 -26 l 0 52 z" fill="{RED}"/></g>')
    # волны тепла
    b.append(f'<g class="heat3">' + "".join(
        f'<path d="M {180 + i*120} 1300 q 20 -40 0 -80 q -20 -40 0 -80" stroke="#ff9a5a" stroke-width="8" fill="none" opacity="0.8"/>'
        for i in range(7)) + '</g>')
    b.append(tile(520, 700, 400, 500, rotate=0, ident="lift3"))
    b.append(badge(2, 520, "b2"))
    b.append(title([("НЕТ ЗАЗОРА", RED)], 250, 60))
    b.append(f'<text x="54" y="330" font-family="Nunito, Arial" font-size="34" font-weight="800" fill="{INK}">плитка упирается и отрывается</text>')
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(tile(100, 760, 880, 760))
    # плюхи клея (просвечивают)
    for i, (x, y, r) in enumerate([(250, 900, 90), (520, 980, 110), (760, 900, 80), (330, 1300, 100), (700, 1330, 95)]):
        b.append(f'<ellipse class="blob" cx="{x}" cy="{y}" rx="{r}" ry="{r*0.7}" fill="{GLUE}" opacity="0.75"/>')
    b.append(f'<text x="540" y="1640" font-family="Nunito, Arial" font-size="32" font-weight="800" fill="{INK}" text-anchor="middle" opacity="0.75">пустота под плиткой</text>')
    # молоток и стук
    b.append('<g class="hammer"><rect x="500" y="560" width="20" height="150" fill="#8a5a34"/>'
             '<rect x="446" y="520" width="128" height="46" rx="10" fill="#5f6b74"/></g>')
    b.append(f'<g class="ripple"><circle cx="540" cy="760" r="60" fill="none" stroke="{RED}" stroke-width="6" opacity="0.8"/></g>')
    b.append(badge(3, 420, "b3"))
    b.append(title([("КЛЕЙ ПЛЮХАМИ", RED)], 250, 60))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="100" y="620" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{INK}">6 ММ</text>')
    b.append(comb(100, 700, teeth=9, height=70, gap=40))
    b.append(f'<text x="600" y="900" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="{GREEN}">10–12 ММ</text>')
    b.append(comb(600, 980, teeth=8, height=130, gap=46))
    b.append(f'<g class="bigTile"><rect x="120" y="1150" width="380" height="380" rx="8" fill="none" stroke="{RED}" stroke-width="8" stroke-dasharray="18 12"/>'
             f'<text x="310" y="1360" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{RED}" text-anchor="middle">60×60</text></g>')
    b.append(badge(4, 430, "b4"))
    b.append(title([("ГРЕБЁНКА НЕ ПО РАЗМЕРУ", RED)], 250, 46))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="#dfeaf0"/>']
    b.append(tile(140, 620, 800, 900))
    b.append(f'<rect x="140" y="620" width="800" height="900" fill="none" stroke="{TILE_D}" stroke-width="6"/>')
    # душ
    b.append(f'<g class="shower"><rect x="820" y="360" width="18" height="180" fill="{GREY}"/>'
             f'<path d="M 760 540 l 140 0 l -30 -60 l -80 0 z" fill="{GREY}"/></g>')
    for i in range(12):
        b.append(f'<path class="wdrop" d="M {790 + (i%4)*18} {560 + (i//4)*26} q 8 40 0 62" stroke="#7fc4e8" stroke-width="7" fill="none" opacity="0.9"/>')
    # вода под плиткой
    b.append(f'<g class="under"><path d="M 200 1500 q 300 -80 700 0 l 0 40 l -700 0 z" fill="#7fc4e8" opacity="0.55"/></g>')
    b.append(f'<g class="arrows6"><path d="M 300 1440 l 0 -220" stroke="{RED}" stroke-width="12"/>'
             f'<path d="M 300 1220 l -26 40 l 52 0 z" fill="{RED}"/></g>')
    b.append(badge(5, 400, "b5"))
    b.append(title([("НЕТ ГИДРОИЗОЛЯЦИИ", RED)], 210, 52))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="300" font-family="Nunito, Arial" font-size="64" font-weight="900" fill="{INK}" text-anchor="middle">ПРОВЕРЬ СЕБЯ</text>')
    items = ["грунтовка", "зазор", "клей без пустот", "гребёнка по размеру", "гидроизоляция"]
    for i, t in enumerate(items):
        y = 520 + i * 220
        b.append(f'<g class="row row{i}"><circle cx="170" cy="{y}" r="46" fill="{GREEN}"/>'
                 f'<path d="M 148 {y} l 14 16 l 30 -34" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/>'
                 f'<text x="250" y="{y+14}" font-family="Nunito, Arial" font-size="44" font-weight="900" fill="{INK}">{t}</text></g>')
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
    tl.fromTo(".hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.1, ease:"power2.out" }}, 0.05);
    tl.fromTo(".b1,.b2,.b3,.b4,.b5", {{ scale:0.6, opacity:0, transformOrigin:"50% 50%" }}, {{ scale:1, opacity:1, duration:0.45, ease:"back.out(2)" }}, 0.2);
    tl.fromTo("#falling", {{ y:-40, rotation:-4 }}, {{ y:180, rotation:26, duration:2.2, ease:"power2.in" }}, 0.3);
    tl.to(".dustF", {{ y:-40, opacity:0.2, duration:2.2, stagger:0.06 }}, 0.4);
    tl.to(".drop", {{ y:150, opacity:0, duration:1.8, stagger:0.12, repeat:1, ease:"power1.in" }}, 0.2);
    tl.fromTo(".cross", {{ opacity:0, scale:0.6, transformOrigin:"50% 50%" }}, {{ opacity:1, scale:1, duration:0.4, ease:"back.out(3)" }}, 0.5);
    tl.to(".arrows", {{ x:-18, duration:0.8, yoyo:true, repeat:6, ease:"sine.inOut" }}, 0);
    tl.to("#lift3", {{ rotation:-7, svgOrigin:"720 950", duration:2.2, ease:"power2.out" }}, 0.6);
    tl.to(".heat3", {{ y:-24, opacity:0.4, duration:1.4, yoyo:true, repeat:5 }}, 0);
    tl.to(".blob", {{ scale:1.05, transformOrigin:"50% 50%", duration:1.0, yoyo:true, repeat:5, stagger:0.1 }}, 0);
    tl.fromTo(".hammer", {{ y:-60 }}, {{ y:0, duration:0.4, ease:"power2.in" }}, 0.2);
    tl.to(".hammer", {{ y:-50, duration:0.4, yoyo:true, repeat:7, ease:"power2.out" }}, 0.6);
    tl.to(".ripple", {{ scale:2.2, opacity:0, transformOrigin:"50% 50%", duration:1.2, stagger:0.3, repeat:3 }}, 0.6);
    tl.fromTo(".tooth", {{ scaleY:0.6, transformOrigin:"50% 100%" }}, {{ scaleY:1, duration:0.5, stagger:0.03, ease:"back.out(2)" }}, 0.2);
    tl.to(".bigTile", {{ scale:1.04, transformOrigin:"50% 50%", duration:1.4, yoyo:true, repeat:2 }}, 0.4);
    tl.to(".wdrop", {{ y:420, opacity:0, duration:2.0, stagger:0.08, repeat:2, ease:"power1.in" }}, 0.2);
    tl.to(".under", {{ y:-12, duration:1.2, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0);
    tl.to(".arrows6", {{ y:-20, duration:0.9, yoyo:true, repeat:5, ease:"sine.inOut" }}, 0);
    tl.fromTo(".row", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.35 }}, 0.2);
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
