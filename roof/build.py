#!/usr/bin/env python3
"""«Правильное утепление кровли» — 12 сцен, каждое слово в кадре."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/roof")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
ITEMS, TOTAL = T["items"], T["total"]
BOUNDS = []
for i, it in enumerate(ITEMS):
    end = ITEMS[i + 1]["start"] if i + 1 < len(ITEMS) else TOTAL
    BOUNDS.append((round(it["start"], 3), round(end - it["start"], 3)))

BG = "#f1f5f7"
INK = "#1e2b35"
WOOD = "#b98a55"
WOOD_D = "#8a6338"
INSUL = "#f4c860"
INSUL_D = "#d9a63a"
VAPOR = "#6fa8c9"
GAP = "#cfe6f2"
ROOF = "#7d4b3a"
STEEL = "#8fa3b1"
HOT = "#d9532f"
COLD = "#3f8fb8"
GREEN = "#2c8a58"
RED = "#c0392b"

DEFS = """<defs>
<linearGradient id="insG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset="1" stop-color="#d9a63a"/></linearGradient>
<linearGradient id="roofG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9c6046"/><stop offset="1" stop-color="#6d3f30"/></linearGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def title(lines, y=150, size=60):
    return "".join(
        f'<text class="hl" x="52" y="{y + i*(size+16)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def lab(x, y, t, size=30, col=INK, anchor="start", cls="lab"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="900" fill="{col}" text-anchor="{anchor}">{t}</text>')


def rafter(x, y, h=420, w=42):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="3"/>'
            f'<line x1="{x+8}" y1="{y}" x2="{x+8}" y2="{y+h}" stroke="{WOOD_D}" stroke-width="2" opacity="0.4"/>')


def band(x, y, w, h, fill, cls="", opacity=1):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{opacity}"/>'


def up_arrow(x, y, cls="up", col=HOT, h=110):
    return (f'<g class="{cls}"><line x1="{x}" y1="{y}" x2="{x}" y2="{y-h}" stroke="{col}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M {x} {y-h-18} l -16 24 l 32 0 z" fill="{col}"/></g>')


# ---------------------------------------------------------------- s1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    # дом в разрезе
    b.append(f'<path d="M 140 1200 L 540 900 L 940 1200" stroke="{ROOF}" stroke-width="46" fill="none" stroke-linejoin="round"/>')
    b.append(f'<rect x="200" y="1200" width="680" height="380" fill="#e6ecf0" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="470" y="1380" width="140" height="200" fill="{WOOD}"/>')
    for i in range(5):
        b.append(up_arrow(300 + i * 130, 1180 + (i % 2) * 40, f"heat h{i}", HOT, 150))
    b.append(f'<path d="M 540 900 l 0 -60" stroke="{INK}" stroke-width="6"/>')
    b.append(title([("ТЕПЛО", INK), ("УХОДИТ ЧЕРЕЗ КРЫШУ", RED)], 160, 52))
    return svg("".join(b))


# ---------------------------------------------------------------- s2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    x, w = 90, 900
    b.append(band(x, 1175, w, 40, VAPOR, "lyr vapour"))
    b.append(band(x, 915, w, 260, "url(#insG)", "lyr insul"))
    b.append(band(x, 835, w, 80, GAP, "lyr gap", 0.9))
    b.append(band(x, 785, w, 50, WOOD, "lyr counter"))
    b.append(band(x, 740, w, 45, "#c9a06a", "lyr batten"))
    b.append(band(x, 660, w, 80, "url(#roofG)", "lyr roof"))
    for i in range(4):
        b.append(f'<g class="lyr">{rafter(210 + i*210, 860, 330, 34)}</g>')
    b.append(lab(120, 1205, "ПАРОИЗОЛЯЦИЯ", 26, "#ffffff", "start", "lb l0"))
    b.append(lab(120, 1060, "УТЕПЛИТЕЛЬ 200–250 ММ", 28, "#5c4308", "start", "lb l1"))
    b.append(lab(120, 883, "ВЕНТЗАЗОР 50 ММ", 24, "#1d5d7d", "start", "lb l2"))
    b.append(lab(120, 818, "КОНТРБРУС", 22, "#ffffff", "start", "lb l3"))
    b.append(lab(120, 770, "ОБРЕШЁТКА", 22, "#5a4420", "start", "lb l4"))
    b.append(lab(120, 712, "КРОВЛЯ", 26, "#ffffff", "start", "lb l5"))
    b.append(title([("ПИРОГ", INK), ("КРОВЛИ", GREEN)], 150, 60))
    return svg("".join(b))


# ---------------------------------------------------------------- s3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 1100, 900, 300, "url(#insG)", "insul3"))
    # щель
    b.append(f'<rect class="gap3" x="470" y="1100" width="60" height="300" fill="{BG}"/>')
    for i in range(3):
        b.append(up_arrow(500 + i * 6, 1100, f"leak l{i}", HOT, 220))
    b.append(f'<rect class="plug" x="470" y="1100" width="60" height="300" fill="url(#insG)" opacity="0"/>')
    b.append(lab(540, 1520, "ЩЕЛЬ = МОСТИК ТЕПЛА", 34, RED, "middle"))
    b.append(title([("БЕЗ", INK), ("ЩЕЛЕЙ", GREEN)], 150, 70))
    return svg("".join(b))


# ---------------------------------------------------------------- s4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 900, 900, 330, "url(#insG)", "insul4"))
    b.append(f'<line x1="1030" y1="900" x2="1030" y2="1230" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<line x1="1010" y1="900" x2="1050" y2="900" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<line x1="1010" y1="1230" x2="1050" y2="1230" stroke="{INK}" stroke-width="5"/>')
    b.append(lab(1000, 1080, "200–250 ММ", 34, INK, "end"))
    for i in range(9):
        b.append(f'<line x1="120" y1="{930 + i*32}" x2="240" y2="{930 + i*32}" stroke="#8a6410" stroke-width="3" opacity="0.6"/>')
    b.append(lab(120, 1290, "толщина слоя", 28, "#8a6410"))
    b.append(title([("ТОЛЩИНА", INK), ("НЕ МЕНЬШЕ 200", GREEN)], 150, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- s5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 760, 900, 300, "url(#insG)"))
    b.append(f'<rect class="vap" x="60" y="1082" width="560" height="26" fill="{VAPOR}" opacity="0"/>')
    b.append(f'<rect class="vap2" x="580" y="1092" width="420" height="26" fill="{VAPOR}" opacity="0"/>')
    b.append(f'<rect x="60" y="1120" width="960" height="8" fill="{VAPOR}" opacity="0.35"/>')
    b.append(f'<rect class="tape" x="540" y="1070" width="120" height="60" rx="6" fill="#efe6d2" opacity="0"/>')
    b.append(f'<text x="540" y="1160" font-family="Nunito, Arial" font-size="24" font-weight="900" fill="{INK}" text-anchor="middle">НАХЛЁСТ + СКОТЧ</text>')
    for i in range(4):
        b.append(f'<path class="vapArr" d="M {220 + i*200} 1400 l 0 -120" stroke="{COLD}" stroke-width="8" opacity="0.8"/>')
    b.append(f'<path d="M 205 1290 l 15 22 l 15 -22" fill="{COLD}" opacity="0.8"/>')
    b.append(title([("ПАРОИЗОЛЯЦИЯ", INK), ("СНИЗУ", GREEN)], 150, 50))
    return svg("".join(b))


# ---------------------------------------------------------------- s6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 980, 900, 300, "url(#insG)"))
    b.append(band(60, 900, 960, 80, GAP, "gapband", 0.95))
    b.append(f'<rect x="60" y="880" width="960" height="18" fill="{WOOD}" opacity="0.7"/>')
    for i in range(6):
        b.append(f'<g class="air6"><circle cx="{140 + i*150}" cy="940" r="13" fill="{COLD}"/>'
                 f'<path d="M {160 + i*150} 940 l -12 -6 l 0 12 z" fill="{COLD}"/></g>')
    b.append(lab(540, 1040, "50 ММ", 40, COLD, "middle"))
    b.append(title([("ВЕНТЗАЗОР", INK), ("50 ММ", GREEN)], 150, 58))
    return svg("".join(b))


# ---------------------------------------------------------------- s7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 1000, 900, 260, "url(#insG)"))
    b.append(band(60, 930, 960, 70, GAP, "gap7", 0.9))
    for i in range(5):
        b.append(f'<g class="cb"><rect x="{130 + i*190}" y="900" width="40" height="130" fill="{WOOD}" stroke="{WOOD_D}" stroke-width="3"/></g>')
    for i in range(4):
        b.append(f'<path class="flow7" d="M {180 + i*190} 965 l 90 0" stroke="{COLD}" stroke-width="8"/>')
    b.append(title([("КОНТРБРУС", INK), ("ВДОЛЬ СТРОПИЛ", GREEN)], 150, 50))
    b.append(lab(540, 1290, "держит зазор, не даёт утеплителю прижаться", 26, INK, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 1180, 900, 150, "url(#insG)"))
    b.append(f'<g class="top8">' + band(90, 1030, 900, 150, "url(#insG)") + '</g>')
    for i in range(4):
        b.append(f'<line x1="{200 + i*220}" y1="1180" x2="{200 + i*220}" y2="1330" stroke="#8a6410" stroke-width="4" opacity="0.7"/>')
    b.append(f'<g class="seams"><line class="seamTop" x1="300" y1="1030" x2="300" y2="1180" stroke="{RED}" stroke-width="6"/>'
             f'<line class="seamTop" x1="740" y1="1030" x2="740" y2="1180" stroke="{RED}" stroke-width="6"/>'
             f'<line class="seamBot" x1="520" y1="1180" x2="520" y2="1330" stroke="{RED}" stroke-width="6" opacity="0.6"/></g>')
    b.append(title([("ДВА СЛОЯ", INK), ("С ПЕРЕХЛЁСТОМ", GREEN)], 150, 54))
    b.append(lab(540, 1450, "стыки верхнего слоя — над серединой нижнего", 26, INK, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s9
def s9():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 850, 900, 120, "url(#roofG)"))
    b.append(band(90, 970, 900, 240, "url(#insG)", "insul9"))
    b.append(f'<g class="cond">' + "".join(
        f'<circle class="drop9" cx="{180 + i*110}" cy="{970 + (i%3)*30}" r="{10 + i%3*3}" fill="{COLD}"/>' for i in range(8)) + '</g>')
    for i in range(6):
        b.append(f'<circle class="mold" cx="{200 + i*120}" cy="{1230}" r="16" fill="#4a5a3a" opacity="0.7"/>')
    b.append(f'<path d="M 540 970 l 0 -40" stroke="{RED}" stroke-width="8" stroke-dasharray="10 8"/>')
    b.append(lab(540, 1420, "нет зазора → конденсат → гниль", 32, RED, "middle"))
    b.append(title([("ПРИЖАТ", INK), ("К КРОВЛЕ", RED)], 150, 56))
    return svg("".join(b))


# ---------------------------------------------------------------- s10
def s10():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 1100, 900, 220, "url(#insG)"))
    b.append(f'<rect class="beam" x="470" y="850" width="60" height="700" fill="{STEEL}" stroke="#5f6b74" stroke-width="4"/>')
    b.append(f'<path class="coldLine" d="M 500 880 l 0 640" stroke="{COLD}" stroke-width="14" opacity="0.6"/>')
    b.append(f'<rect class="wrap" x="270" y="1080" width="200" height="260" fill="url(#insG)" opacity="0"/>')
    b.append(f'<rect class="wrap" x="610" y="1080" width="200" height="260" fill="url(#insG)" opacity="0"/>')
    b.append(title([("МОСТИК", INK), ("ХОЛОДА", RED)], 150, 60))
    b.append(lab(540, 1620, "металл промерзает — закрываем утеплителем", 26, INK, "middle"))
    return svg("".join(b))


# ---------------------------------------------------------------- s11
def s11():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(band(90, 900, 900, 260, "url(#insG)"))
    b.append(band(60, 830, 960, 70, GAP, "gap11", 0.95))
    b.append(f'<path d="M 60 830 l 0 -90 l 60 0" stroke="{ROOF}" stroke-width="20" fill="none"/>')
    b.append(f'<path d="M 960 830 l 0 -110 l -70 0" stroke="{ROOF}" stroke-width="20" fill="none"/>')
    b.append(lab(150, 700, "ПРОДУХ", 26, COLD))
    b.append(lab(900, 690, "КОНЁК", 26, COLD, "end"))
    for i in range(5):
        b.append(f'<g class="air11"><circle cx="{160 + i*170}" cy="865" r="12" fill="{COLD}"/></g>')
    b.append(title([("ВЕНТИЛЯЦИЯ", INK), ("КАРНИЗ → КОНЁК", GREEN)], 150, 48))
    return svg("".join(b))


# ---------------------------------------------------------------- s12
def s12():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']
    b.append(f'<text x="540" y="290" font-family="Nunito, Arial" font-size="52" font-weight="900" fill="{INK}" text-anchor="middle">ПРОВЕРЬ</text>')
    items = ["без щелей", "200–250 мм", "пароизоляция снизу", "вентзазор 50 мм", "продухи и конёк"]
    for i, t in enumerate(items):
        y = 500 + i * 230
        b.append(f'<g class="row r{i}"><circle cx="150" cy="{y}" r="44" fill="{GREEN}"/>'
                 f'<path d="M 130 {y} l 14 16 l 30 -34" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/>'
                 f'<text x="235" y="{y+14}" font-family="Nunito, Arial" font-size="42" font-weight="900" fill="{INK}">{t}</text></g>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12]


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
    tl.fromTo(".heat", {{ y:0, opacity:0.55 }}, {{ y:-120, opacity:1, duration:1.1, stagger:0.15, yoyo:true, repeat:12, ease:"sine.inOut" }}, 0);
    tl.fromTo(".lyr", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.32 }}, 0.1);
    tl.fromTo(".lb", {{ opacity:0 }}, {{ opacity:1, duration:0.4, stagger:0.32 }}, 0.3);
    tl.fromTo(".plug", {{ opacity:0 }}, {{ opacity:1, duration:0.6 }}, {dur} * 0.55);
    tl.to(".leak", {{ y:-220, opacity:0, duration:1.0, stagger:0.1, repeat:3 }}, 0);
    tl.fromTo(".vap", {{ opacity:0, x:-60 }}, {{ opacity:0.95, x:0, duration:1.2 }}, 0.2);
    tl.fromTo(".tape", {{ opacity:0, scaleX:0.4, transformOrigin:"50% 50%" }}, {{ opacity:1, scaleX:1, duration:0.5 }}, {dur} * 0.55);
    tl.to(".vapArr", {{ y:-30, opacity:0.3, duration:1.0, yoyo:true, repeat:4 }}, 0);
    tl.to(".air6", {{ x:120, duration:1.6, stagger:0.12, repeat:3, ease:"none" }}, 0);
    tl.to(".flow7", {{ x:80, duration:1.4, stagger:0.1, repeat:4, ease:"none" }}, 0);
    tl.fromTo(".cb", {{ opacity:0, y:-30 }}, {{ opacity:1, y:0, duration:0.4, stagger:0.2 }}, 0.1);
    tl.to(".top8", {{ x:110, duration:1.6, ease:"power2.inOut" }}, 0.4);
    tl.to(".seamTop", {{ opacity:0.3, duration:0.5, yoyo:true, repeat:6 }}, 1.0);
    tl.to(".drop9", {{ y:120, opacity:0, duration:1.4, stagger:0.15, repeat:3, ease:"power1.in" }}, 0.3);
    tl.to(".mold", {{ opacity:0.9, duration:1.2, yoyo:true, repeat:3 }}, 0.6);
    tl.fromTo(".wrap", {{ opacity:0, scaleY:0.6, transformOrigin:"50% 100%" }}, {{ opacity:1, scaleY:1, duration:0.8 }}, {dur} * 0.35);
    tl.to(".coldLine", {{ opacity:0.2, duration:0.8, yoyo:true, repeat:5 }}, 0);
    tl.to(".air11", {{ x:150, duration:2.0, stagger:0.15, repeat:3, ease:"none" }}, 0);
    tl.fromTo(".row", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.4, stagger:0.3 }}, 0.2);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, it in enumerate(ITEMS):
        sid = it["scene"]
        st, dur = BOUNDS[i]
        (OUT / f"{sid}.html").write_text(page(sid, SCENES[i](), dur), encoding="utf-8")
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
