#!/usr/bin/env python3
"""Зеркала и слепые зоны — тёмная кинетическая инфографика, 9:16, 64 с."""
from pathlib import Path

OUT = Path("/root/video-gen/mirrors/compositions")
OUT.mkdir(parents=True, exist_ok=True)

BG = "#080d16"
ROAD = "#111a26"
LINE = "#dfe7f0"
RED = "#e6402f"
BLUE = "#2f9fd8"
GREY = "#8b98a8"
YEL = "#f2c14e"

DEFS = """<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#080d16" stop-opacity="1"/><stop offset="0.5" stop-color="#080d16" stop-opacity="0"/>
    <stop offset="1" stop-color="#080d16" stop-opacity="1"/>
  </linearGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#eaf2ff" stop-opacity="0.30"/><stop offset="1" stop-color="#eaf2ff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="beamRed" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff8a7a" stop-opacity="0.35"/><stop offset="1" stop-color="#ff8a7a" stop-opacity="0"/>
  </linearGradient>
</defs>"""


def svg(body) -> str:
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}'
            f'<rect width="1080" height="1920" fill="{BG}"/>{body}</svg>')


def road(y0=0, y1=1920, lanes=3, x0=60, x1=1020):
    w = (x1 - x0) / lanes
    out = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{ROAD}"/>']
    for i in range(1, lanes):
        x = x0 + i * w
        out.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{LINE}" stroke-width="4" stroke-dasharray="46 40" opacity="0.5"/>"')
    return "".join(out)


def car(x, y, color=BLUE, w=150, h=250, rotate=0, ident="", beam=True, flip=False):
    b = (f'<g id="{ident}" transform="translate({x} {y}) rotate({rotate})">')
    if beam:
        b += (f'<path d="M -{w*0.4} {-h/2} L {w*0.4} {-h/2} L {w*1.1} {-h*1.7} L -{w*1.1} {-h*1.7} Z" fill="url(#beam)"/>')
    b += (f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" rx="26" fill="{color}"/>'
          f'<rect x="{-w/2+16}" y="{-h/2+34}" width="{w-32}" height="{h*0.34}" rx="14" fill="#0d1620" opacity="0.75"/>'
          f'<rect x="{-w/2+16}" y="{h*0.16}" width="{w-32}" height="{h*0.2}" rx="12" fill="#0d1620" opacity="0.45"/>')
    if flip:
        b += f'<circle cx="{-w/2+26}" cy="{-h/2+16}" r="7" fill="#ffe9a8"/><circle cx="{w/2-26}" cy="{-h/2+16}" r="7" fill="#ffe9a8"/>'
    else:
        b += f'<circle cx="{-w/2+26}" cy="{-h/2+16}" r="7" fill="#ffe9a8"/><circle cx="{w/2-26}" cy="{-h/2+16}" r="7" fill="#ffe9a8"/>'
    b += '</g>'
    return b


def chip(x, y, text, color=RED, w=250, size=24):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="52" rx="10" fill="#0b121c" stroke="{color}" stroke-width="2"/>'
            f'<text x="{x+16}" y="{y+34}" fill="{color}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="800" letter-spacing="1">{text}</text></g>')


def mirror_view(x, y, w=760, h=420, door_share=0.45, note="ТВОЯ ДВЕРЬ", note_color=RED):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="#0e1724" stroke="#26313f" stroke-width="6"/>']
    # отражение: дорога + своя дверь
    out.append(f'<rect x="{x+8}" y="{y+8}" width="{w*(1-door_share)-8}" height="{h-16}" rx="20" fill="#16202e"/>')
    for i in range(1, 4):
        out.append(f'<line x1="{x+8+ i*(w*(1-door_share)-8)/4}" y1="{y+8}" x2="{x+8+i*(w*(1-door_share)-8)/4}" y2="{y+h-8}" stroke="{LINE}" stroke-width="3" opacity="0.25"/>')
    out.append(f'<rect x="{x+w*(1-door_share)}" y="{y+8}" width="{w*door_share-8}" height="{h-16}" rx="20" fill="{RED}" opacity="0.85"/>')
    out.append(f'<text x="{x+w*(1-door_share)+24}" y="{y+h/2}" fill="#fff" font-family="Nunito, Arial" font-size="30" font-weight="800" opacity="0.9">{note}</text>')
    return "".join(out)


def txt(x, y, s, size=64, color="#fff", anchor="start", weight="900", op=1.0):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" opacity="{op}" letter-spacing="0.5">{s}</text>')


SCENES = {}

# ---------------------------------------------------------------- 1: хук
def s1():
    b = [road(), mirror_view(160, 620, 760, 420, 0.42)]
    b.append(chip(160, 560, "ВИДИШЬ В ЗЕРКАЛЕ", RED, 330, 24))
    b.append(chip(600, 1080, "ЭТО НЕ ДОРОГА", GREY, 300, 22))
    return svg("".join(b))


# ---------------------------------------------------------------- 2: удар
def s2():
    b = [road()]
    b.append(car(420, 1150, BLUE, 160, 260, ident="c1"))
    b.append(car(560, 980, RED, 160, 260, ident="c2", rotate=8))
    b.append(chip(120, 1420, "УДАР В БОК", RED, 260))
    b.append(chip(430, 1420, "ШТРАФ 500 ₽", RED, 300))
    return svg("".join(b))


# ---------------------------------------------------------------- 3: слепая зона
def s3():
    b = [road(), car(420, 1300, BLUE, 160, 260, ident="hero")]
    b.append('<g id="shadow"><path d="M 300 1150 L 540 1150 L 640 620 L 200 620 Z" fill="#e6402f" opacity="0.10"/></g>')
    b.append(car(300, 900, RED, 150, 240, ident="red", rotate=-4))
    b.append(chip(620, 760, "НЕ ВИДНО В ЗЕРКАЛЕ", RED, 380, 22))
    return svg("".join(b))


# ---------------------------------------------------------------- 4: что показывает зеркало
def s4():
    b = [mirror_view(120, 700, 840, 460, 0.5, "ТВОЯ ДВЕРЬ")]
    b.append(chip(140, 640, "БОКОВОЕ ЗЕРКАЛО", GREY, 340, 22))
    b.append(chip(140, 1200, "МАШИНА СБОКУ — ВНЕ КАДРА", RED, 520, 22))
    return svg("".join(b))


# ---------------------------------------------------------------- 5: настройка
def s5():
    b = [road(0, 1920)]
    b.append(mirror_view(120, 620, 840, 440, 0.22, "КРАЙ КУЗОВА", YEL))
    b.append(chip(140, 560, "НАКЛОНИ ГОЛОВУ К СТЕКЛУ", GREY, 520, 22))
    b.append(chip(140, 1090, "ПОВЕРНИ ЗЕРКАЛО", YEL, 380, 22))
    b.append('<path d="M 820 1180 q 90 -30 40 -110" stroke="#f2c14e" stroke-width="8" fill="none" marker-end=""/>')
    b.append('<polygon points="852,1052 826,1104 880,1096" fill="#f2c14e"/>')
    return svg("".join(b))


# ---------------------------------------------------------------- 6: результат
def s6():
    b = [road(), car(420, 1350, BLUE, 160, 260, ident="hero2")]
    b.append('<path d="M 300 1180 L 540 1180 L 660 560 L 180 560 Z" fill="#40c07a" opacity="0.12"/>')
    b.append(chip(600, 700, "СЛЕПАЯ ЗОНА ПЕРЕКРЫТА", "#40c07a", 430, 22))
    b.append(chip(160, 1500, "ПРОВЕРЬ ОБА ЗЕРКАЛА", GREY, 420, 22))
    return svg("".join(b))


SCENERY = {"s1": s1, "s2": s2, "s3": s3, "s4": s4, "s5": s5, "s6": s6}

HEAD = {
    "s1": [("ВИДИШЬ В ЗЕРКАЛЕ", "#fff"), ("СВОЮ ДВЕРЬ?", RED)],
    "s2": [("ПЕРЕСТРОИЛСЯ —", "#fff"), ("УДАР В БОК", RED)],
    "s3": [("МАШИНА", "#fff"), ("ИСЧЕЗЛА", RED)],
    "s4": [("ЗЕРКАЛО", "#fff"), ("СМОТРИТ НЕ ТУДА", RED)],
    "s5": [("РАЗВЕРНИ", "#fff"), ("ЗЕРКАЛО", YEL)],
    "s6": [("ЗОНА", "#fff"), ("ПЕРЕКРЫТА", "#40c07a")],
}
DUR = {"s1": 10, "s2": 8, "s3": 12, "s4": 10, "s5": 12, "s6": 8}
ANIM = {
    "s1": 'tl.fromTo("#s1 .world", {opacity:0.4, y:30}, {opacity:1, y:0, duration:0.9, ease:"power2.out"}, 0.15);',
    "s2": 'tl.fromTo("#c2", {opacity:0}, {opacity:1, duration:0.6, ease:"power2.out"}, 1.0);',
    "s3": 'tl.fromTo("#red", {opacity:0}, {opacity:1, duration:1.2}, 0.6);tl.to("#shadow", {opacity:0.35, duration:2.0, yoyo:true, repeat:2}, 1.0);',
    "s4": 'tl.fromTo("#s4 .world", {scale:1.02}, {scale:1.06, duration:10, ease:"none"}, 0);',
    "s5": 'tl.fromTo("#s5 .world", {opacity:0.6}, {opacity:1, duration:0.6}, 0.2);',
    "s6": 'tl.fromTo("#s6 .world", {opacity:0.5}, {opacity:1, duration:0.8}, 0.2);',
}


def page(sid, body, dur):
    lines = HEAD[sid]
    head = "".join(
        f'<text class="hl" x="56" y="{240 + i*92}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="76" font-weight="900" letter-spacing="-1">{s}</text>' for i, (s, c) in enumerate(lines)
    )
    body = body.replace('</svg>', head + '</svg>')
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{BG}; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
    .head {{ position:absolute; left:56px; right:56px; top:150px; font-family:"Nunito",Arial,sans-serif;
      font-weight:900; font-size:78px; line-height:0.98; text-transform:uppercase; letter-spacing:-1px; }}
    .line {{ opacity:1; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">
        {body}
      </div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl_{sid}.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    tl_{sid}.fromTo("#{sid} .hl", {{ opacity:0, y:22 }}, {{ opacity:1, y:0, duration:0.45, stagger:0.16, ease:"power3.out" }}, 0.15);
    {ANIM[sid]}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts, start = [], 0
    for i, sid in enumerate(["s1", "s2", "s3", "s4", "s5", "s6"]):
        body = SCENERY[sid]()

        (OUT / f"{sid}.html").write_text(page(sid, body, DUR[sid]), encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{start}" data-duration="{DUR[sid]}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        start += DUR[sid]
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{BG}}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    Path("/root/video-gen/mirrors/index.html").write_text(html, encoding="utf-8")
    print("ok", start)


if __name__ == "__main__":
    build()
