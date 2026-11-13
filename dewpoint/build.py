#!/usr/bin/env python3
"""«Точка росы» — 8 сцен, светлая объёмная иллюстрация."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/dewpoint")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

BG1 = "#eef4f8"; BG2 = "#dfe9f0"
INK = "#33404a"; INK2 = "#5f7079"
SNOW = "#f8fcfe"
TARP = "#3f74a8"; TARP_D = "#2c5580"; TARP_L = "#6f9fc9"
CANVAS = "#c8b18a"; CANVAS_D = "#a68f68"; CANVAS_L = "#dfcba6"
BAG = "#9db6c4"; BAG_D = "#7d97a6"
SKIN = "#e8b48c"; HAT = "#3f5f7a"
FROST = "#bfe6f5"; WARM = "#e8a04a"; RED = "#c0503c"


def t(x, y, s, size=40, col=INK, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def title(x, y, s, size=36, cls="hl", col=INK):
    w = len(s) * size * 0.62 + 34
    return (f'<g class="{cls}"><rect x="{x-12}" y="{y-size*1.1:.0f}" width="{w:.0f}" height="{size*1.6:.0f}" rx="{size*0.3:.0f}" '
            f'fill="#ffffff" opacity="0.85"/>'
            f'<text x="{x}" y="{y}" font-family="Nunito" font-size="{size}" font-weight="900" fill="{col}" letter-spacing="1">{s}</text></g>')


def scene_bg():
    return ('<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#bg)"/>')


def snow_ground(y=1300, cls="sn"):
    r = random.Random(3)
    dots = "".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(y+20,1880):.0f}" r="{r.uniform(2,5):.0f}" '
                   f'fill="#ffffff" opacity="{r.uniform(0.4,0.9):.2f}"/>' for _ in range(70))
    return (f'<g class="{cls}"><path d="M 0 {y} q 270 -40 540 0 t 540 0 l 0 {1920-y} l -1080 0 z" fill="{SNOW}"/>'
            f'{dots}<path d="M 0 {y} q 270 -40 540 0 t 540 0" stroke="#cfe0ea" stroke-width="4" fill="none"/></g>')


def person(x, y, s=1.0, cls="ps"):
    """Человек в спальнике: мешок-кокон, капюшон, лицо."""
    b = [f'<g class="{cls}"><g transform="translate({x} {y}) rotate(-6) scale({s})">']
    b.append(f'<rect x="-210" y="-62" width="400" height="124" rx="62" fill="{BAG}" stroke="{BAG_D}" stroke-width="5"/>')
    b.append(f'<path d="M -120 -58 q 14 60 0 116" stroke="{BAG_D}" stroke-width="4" fill="none" opacity="0.45"/>')
    b.append(f'<path d="M -30 -58 q 14 60 0 116" stroke="{BAG_D}" stroke-width="4" fill="none" opacity="0.45"/>')
    b.append(f'<path d="M 60 -58 q 14 60 0 116" stroke="{BAG_D}" stroke-width="4" fill="none" opacity="0.45"/>')
    # капюшон
    b.append(f'<circle cx="-186" cy="-40" r="56" fill="{BAG_D}"/>')
    b.append(f'<circle cx="-186" cy="-40" r="40" fill="{SKIN}"/>')
    b.append(f'<path d="M -226 -50 q 40 -34 80 0 q -40 18 -80 0 z" fill="{HAT}"/>')
    b.append(f'<path d="M -202 -34 l 0 7 M -170 -34 l 0 7" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    b.append('</g></g>')
    return "".join(b)


def tarp_tent(cx, by, w=520, h=300, col=TARP, dark=TARP_D, light=TARP_L, cls="tt", open_side=True):
    """Полуоткрытый тент: купол + срез."""
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {cx-w/2} {by} q 0 {-h} {w/2} {-h} q {w/2} 0 {w/2} {h} l 0 20 l {-w} 0 z" fill="{col}" stroke="{dark}" stroke-width="5"/>')
    b.append(f'<path d="M {cx-w/2+18} {by+10} q 0 {-h+34} {w/2-18} {-h+34} q {w/2-18} 0 {w/2-18} {h-34} l 0 10 l {-w+36} 0 z" fill="{light}" opacity="0.35"/>')
    # срез (внутренняя поверхность)
    b.append(f'<ellipse cx="{cx}" cy="{by-10}" rx="{w/2-24}" ry="34" fill="#eaf4fa" stroke="{dark}" stroke-width="3" opacity="0.9"/>')
    b.append('</g>')
    return "".join(b)


def ice_blocks(x, y, cls="ic", n=5):
    r = random.Random(7)
    b = [f'<g class="{cls}">']
    for i in range(n):
        px = x + i * 46 + r.uniform(-6, 6)
        py = y + r.uniform(-10, 10)
        b.append(f'<rect x="{px:.0f}" y="{py:.0f}" width="38" height="34" rx="6" fill="{FROST}" stroke="#8fc4d8" stroke-width="2" opacity="0.95"/>')
    b.append('</g>')
    return "".join(b)


def crystals(x, y, cls="cr", n=7):
    b = [f'<g class="{cls}">']
    for i in range(n):
        px = x + i * 46
        py = y + (i % 2) * 14
        for a in (0, 60, 120):
            b.append(f'<path d="M {px} {py} l 0 -26" stroke="{FROST}" stroke-width="5" stroke-linecap="round" '
                     f'transform="rotate({a} {px} {py})"/>')
    b.append('</g>')
    return "".join(b)


def vapor(n=12, seed=2, cls="vp"):
    r = random.Random(seed)
    return "".join(f'<circle class="v{i}" cx="{r.uniform(320,760):.0f}" cy="{r.uniform(1000,1300):.0f}" r="{r.uniform(5,11):.0f}" '
                   f'fill="#ffffff" opacity="{r.uniform(0.25,0.6):.2f}"/>' for i in range(n))


def inset(cx, cy, r=200, cls="ins", title_text="", tint="#e9f4fa"):
    return (f'<g class="{cls}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{tint}" stroke="{INK2}" stroke-width="4"/>'
            + (f'<text x="{cx}" y="{cy-r-18}" font-family="Nunito" font-size="24" font-weight="900" fill="{INK}" '
               f'text-anchor="middle">{title_text}</text>' if title_text else "")
            + '</g>')


def snowflakes(n=9, seed=5, cls="sf"):
    r = random.Random(seed)
    out = [f'<g class="{cls}">']
    for i in range(n):
        x, y = r.uniform(60, 1020), r.uniform(200, 1000)
        out.append(f'<g class="fl{i}" transform="translate({x:.0f} {y:.0f})">'
                   f'<path d="M 0 -12 l 0 24 M -10 -6 l 20 12 M 10 -6 l -20 12" stroke="{FROST}" stroke-width="3" stroke-linecap="round"/></g>')
    out.append('</g>')
    return "".join(out)


# ---------------------------------------------------------------- 1
def s1():
    b = [scene_bg(), snow_ground(1250, "sn1"), snowflakes(10, 3)]
    b.append(tarp_tent(540, 1200, 800, 450, TARP, TARP_D, TARP_L, "tt1"))
    b.append(person(500, 1190, 1.5, "ps1"))
    b.append(ice_blocks(360, 1080, "ic1", 6))
    b.append(title(60, 190, "ПЛАСТИК — ЛОВУШКА", 36))
    b.append(t(64, 250, "лёд образуется внутри", 24, INK2, w=700))
    b.append(f'<circle cx="880" cy="520" r="48" fill="{RED}" opacity="0.12"/>')
    b.append(t(880, 536, "!", 52, RED, "middle", 900))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [scene_bg(), snow_ground(1300, "sn2")]
    b.append(tarp_tent(540, 1200, 800, 440, TARP, TARP_D, TARP_L, "tt2"))
    b.append(person(500, 1190, 1.55, "ps2"))
    b.append(vapor(10, 4))
    b.append(title(60, 190, "ТЕЛО ИСПАРЯЕТ ВЛАГУ", 32))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [scene_bg(), snow_ground(1450, "sn3")]
    b.append(inset(540, 760, 250, "ins3", ""))
    # плёнка
    b.append(f'<path d="M 540 520 l 0 480" stroke="{TARP_D}" stroke-width="16"/>')
    b.append(f'<text x="640" y="600" font-family="Nunito" font-size="22" font-weight="800" fill="{TARP_D}">ПЛАСТИК</text>')
    for i in range(4):
        b.append(f'<path class="hit{i}" d="M {420-i*30} {700+i*40} q 90 -20 120 0" stroke="#ffffff" stroke-width="6" fill="none" stroke-dasharray="10 10"/>')
    b.append(f'<path d="M 620 760 q 40 -30 70 0" stroke="{RED}" stroke-width="5" fill="none"/>')
    b.append(title(60, 190, "ПАР НЕ ПРОХОДИТ", 34))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [scene_bg()]
    b.append(f'<rect x="80" y="420" width="920" height="900" rx="26" fill="#e7f3f9" stroke="{INK2}" stroke-width="3"/>')
    b.append(f'<path d="M 80 620 l 920 0" stroke="{TARP_D}" stroke-width="14"/>')
    b.append(f'<text x="120" y="580" font-family="Nunito" font-size="24" font-weight="800" fill="{TARP_D}">ХОЛОДНАЯ ПЛЁНКА</text>')
    b.append(crystals(160, 700, "cr4", 9))
    b.append(crystals(160, 830, "cr4b", 9))
    b.append(f'<path d="M 120 1000 q 400 -60 800 0" stroke="{BAG_D}" stroke-width="10" fill="none"/>')
    b.append(title(60, 200, "ИНЕЙ НАД СПАЛЬНИКОМ", 32))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [scene_bg(), snow_ground(1350, "sn5")]
    b.append(person(540, 1180, 1.9, "ps5"))
    b.append(f'<path d="M 420 1330 q 20 90 60 120" stroke="#5b8fb9" stroke-width="8" fill="none" stroke-dasharray="8 12"/>')
    b.append(f'<circle cx="470" cy="1370" r="10" fill="#5b8fb9"/><circle cx="500" cy="1400" r="8" fill="#5b8fb9"/>')
    b.append(title(60, 200, "СПАЛЬНИК МОКРЫЙ", 34))
    b.append(t(64, 258, "тепло уходит", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [scene_bg(), snow_ground(1250, "sn6"), snowflakes(8, 9)]
    b.append(tarp_tent(540, 1200, 820, 460, CANVAS, CANVAS_D, CANVAS_L, "tt6"))
    b.append(person(500, 1190, 1.5, "ps6"))
    b.append(title(60, 190, "ДЫШАЩИЙ ЧЕХОЛ", 36))
    b.append(t(64, 250, "свободный, с запасом", 24, INK2, w=700))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [scene_bg()]
    b.append(inset(540, 800, 260, "ins7", ""))
    # ткань
    b.append(f'<path d="M 540 540 l 0 520" stroke="{CANVAS_D}" stroke-width="20" stroke-dasharray="6 6"/>')
    b.append(f'<text x="640" y="600" font-family="Nunito" font-size="22" font-weight="800" fill="{CANVAS_D}">ТКАНЬ</text>')
    for i in range(4):
        b.append(f'<path class="pas{i}" d="M 400 {700+i*60} l 130 0" stroke="#ffffff" stroke-width="6" stroke-dasharray="12 12"/>')
    b.append(f'<path class="out0" d="M 560 760 q 60 0 110 40" stroke="#ffffff" stroke-width="6" fill="none" stroke-dasharray="10 10"/>')
    b.append(crystals(620, 860, "cr7", 4))
    b.append(t(720, 980, "ИНЕЙ СНАРУЖИ", 20, INK, w=800))
    b.append(title(60, 190, "ПАР ВЫХОДИТ", 34))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [scene_bg(), snow_ground(1300, "sn8")]
    b.append(tarp_tent(540, 1200, 820, 460, CANVAS, CANVAS_D, CANVAS_L, "tt8"))
    b.append(person(500, 1190, 1.55, "ps8"))
    b.append(f'<circle cx="540" cy="560" r="120" fill="{WARM}" opacity="0.12"/>')
    b.append(title(60, 200, "СУХОЙ ПУХ ГРЕЕТ", 40))
    b.append(t(64, 262, "мокрый — почти не греет", 24, INK2, w=700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".tt1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".ic1", {opacity:0, y:10}, {opacity:1, y:0, duration:0.6}, 0.5);'
    'tl.to(".fl0, .fl1, .fl2", {y:40, duration:3, repeat:-1, ease:"none"}, 0);'
    'tl.fromTo(".hl", {opacity:0, y:10}, {opacity:1, y:0, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".tt2", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".ps2", {opacity:0}, {opacity:1, duration:0.6}, 0.25);'
    'tl.to(".v0, .v1, .v2, .v3, .v4, .v5, .v6, .v7, .v8, .v9", {y:-90, duration:2.2, stagger:0.15, repeat:-1, ease:"sine.out"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".ins3", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.7}, 0.1);'
    'tl.to(".hit0, .hit1, .hit2, .hit3", {x:24, duration:0.8, stagger:0.15, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".cr4", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.8}, 0.1);'
    'tl.fromTo(".cr4b", {opacity:0}, {opacity:1, duration:0.8}, 0.6);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".ps5", {opacity:0}, {opacity:1, duration:0.7}, 0.1);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".tt6", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".ps6", {opacity:0}, {opacity:1, duration:0.6}, 0.4);'
    'tl.to(".fl3, .fl4", {y:40, duration:3.4, repeat:-1, ease:"none"}, 0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.1);',
    'tl.fromTo(".ins7", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.7}, 0.1);'
    'tl.to(".pas0, .pas1, .pas2, .pas3", {x:30, duration:1.2, stagger:0.15, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.5);'
    'tl.fromTo(".cr7", {opacity:0}, {opacity:1, duration:0.7}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.12}, 0.2);',
    'tl.fromTo(".tt8", {opacity:0, y:16}, {opacity:1, y:0, duration:0.7}, 0.1);'
    'tl.fromTo(".ps8", {opacity:0}, {opacity:1, duration:0.6}, 0.35);'
    'tl.fromTo(".hl", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG1}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    {anim}
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, fn in enumerate(SCENES):
        sid = f"s{i+1}"
        st, dur = B[i]
        (OUT / f"{sid}.html").write_text(page(sid, fn(), dur, ANIM[i]), encoding="utf-8")
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
    print("ok", TOTAL, B)


if __name__ == "__main__":
    build()
