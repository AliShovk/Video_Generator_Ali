#!/usr/bin/env python3
"""«Мясной фарш» — 8 сцен, досье-нуар."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/mincemeat")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

SEA = "#0b242d"
SEA2 = "#123742"
CREAM = "#f0e4c8"
PAPER = "#e6d8b8"
RUST = "#b5462b"
BRASS = "#c9a227"
INK = "#131f1e"
FOG = "#6f9a9a"


def t(x, y, s, size=46, col=CREAM, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def waves(y, col=FOG, op=0.35, cls="wv"):
    out = [f'<g class="{cls}" opacity="{op}">']
    for i in range(0, 1080, 120):
        out.append(f'<path d="M {i} {y} q 30 -18 60 0 q 30 18 60 0" fill="none" stroke="{col}" stroke-width="4"/>')
    out.append('</g>')
    return "".join(out)


def bubbles(n=14, seed=2, cls="bub"):
    r = random.Random(seed)
    return "".join(f'<circle class="{cls} c{i}" cx="{r.uniform(120,960):.0f}" cy="{r.uniform(900,1700):.0f}" '
                   f'r="{r.uniform(4,14):.1f}" fill="{CREAM}" opacity="{r.uniform(0.15,0.5):.2f}"/>' for i in range(n))


def briefcase(x, y, s=1.0, cls="case", open_=False):
    b = [f'<g class="{cls}">']
    if open_:
        b.append(f'<rect x="{x}" y="{y-90*s}" width="{420*s}" height="{150*s}" rx="{12*s}" fill="#5b3a22"/>')
        b.append(f'<rect x="{x+20*s}" y="{y-70*s}" width="{380*s}" height="{110*s}" fill="{PAPER}"/>')
    b.append(f'<rect x="{x}" y="{y}" width="{420*s}" height="{270*s}" rx="{18*s}" fill="#6b4326"/>')
    b.append(f'<rect x="{x+18*s}" y="{y+18*s}" width="{384*s}" height="{234*s}" rx="{12*s}" fill="none" stroke="{BRASS}" stroke-width="3" opacity="0.5"/>')
    b.append(f'<rect x="{x+150*s}" y="{y+120*s}" width="{120*s}" height="{26*s}" rx="{6*s}" fill="{BRASS}"/>')
    b.append('</g>')
    return "".join(b)


def map_panel(x, y, w, h, cls="map"):
    g = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#0f3038" stroke="{BRASS}" stroke-width="3"/>']
    for i in range(1, 6):
        g.append(f'<path d="M {x} {y+h*i/6:.0f} L {x+w} {y+h*i/6:.0f}" stroke="{BRASS}" stroke-width="1" opacity="0.12"/>')
        g.append(f'<path d="M {x+w*i/6:.0f} {y} L {x+w*i/6:.0f} {y+h}" stroke="{BRASS}" stroke-width="1" opacity="0.12"/>')
    g.append('</g>')
    return "".join(g)


def node(x, y, label, col=BRASS, cls="nd"):
    return (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="12" fill="{col}"/>'
            f'<circle cx="{x}" cy="{y}" r="24" fill="none" stroke="{col}" stroke-width="2" opacity="0.5"/>'
            f'<text x="{x+34}" y="{y+9}" font-family="Nunito" font-size="24" font-weight="800" fill="{CREAM}">{label}</text></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(f'<circle cx="540" cy="900" r="520" fill="{SEA2}" opacity="0.75"/>')
    b.append(waves(1180, FOG, 0.18, "w1"))
    b.append(waves(1240, FOG, 0.12, "w2"))
    b.append(briefcase(300, 900, 1.15, "case1"))
    # наручники
    b.append('<g class="cuff">')
    b.append(f'<circle cx="380" cy="860" r="46" fill="none" stroke="#b9c2c4" stroke-width="12"/>')
    b.append(f'<circle cx="470" cy="846" r="40" fill="none" stroke="#b9c2c4" stroke-width="12"/>')
    b.append(f'<rect x="420" y="846" width="42" height="16" rx="8" fill="#b9c2c4"/>')
    b.append(f'<path d="M 330 892 q -40 60 10 90" stroke="#b9c2c4" stroke-width="8" fill="none"/>')
    b.append('</g>')
    b.append(t(70, 250, "ОПЕРАЦИЯ", 40, BRASS, ls=6))
    b.append(t(70, 366, "МЯСНОЙ", 96, CREAM, ls=2))
    b.append(t(70, 466, "ФАРШ", 96, RUST, ls=2))
    b.append(t(70, 540, "1943 · Средиземное море", 26, FOG, w=700))
    b.append(t(70, 1720, "труп, который выиграл кампанию", 24, CREAM, w=600))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(f'<circle cx="820" cy="420" r="120" fill="{CREAM}" opacity="0.75"/>')
    b.append(f'<path d="M 0 900 L 240 780 L 380 900 Z" fill="#0a1a20"/>')
    b.append(f'<rect x="0" y="880" width="1080" height="1040" fill="{SEA2}"/>')
    # подлодка
    b.append('<g class="sub">')
    b.append(f'<ellipse cx="560" cy="1000" rx="300" ry="70" fill="#1d3438"/>')
    b.append(f'<rect x="420" y="900" width="120" height="110" rx="18" fill="#1d3438"/>')
    b.append(f'<rect x="470" y="760" width="14" height="150" fill="#1d3438"/>')
    b.append(f'<rect x="440" y="820" width="80" height="10" fill="#1d3438"/>')
    b.append(f'<circle cx="840" cy="1000" r="10" fill="{BRASS}" opacity="0.7"/>')
    b.append('</g>')
    for i in range(4):
        b.append(waves(1100 + i * 90, FOG, 0.28 - i * 0.05, f"w{i}"))
    b.append(t(70, 250, "ИСПАНИЯ · 1943", 40, BRASS, ls=4))
    b.append(t(70, 320, "море у берега", 34, CREAM, w=800))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="#082028"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="520" fill="{SEA}"/>')
    b.append(waves(520, FOG, 0.4, "surf"))
    # тело
    b.append('<g class="body">')
    b.append(f'<ellipse cx="560" cy="1120" rx="60" ry="150" fill="#20343a" transform="rotate(18 560 1120)"/>')
    b.append(f'<circle cx="610" cy="950" r="52" fill="#20343a"/>')
    b.append(f'<rect x="600" y="880" width="90" height="26" rx="12" fill="#2a444a"/>')
    b.append(f'<path d="M 500 1080 q 60 40 120 0" stroke="{BRASS}" stroke-width="6" fill="none" opacity="0.5"/>')
    b.append('</g>')
    b.append(bubbles(16, 4))
    b.append(f'<path d="M 300 520 q 260 70 520 0" stroke="{FOG}" stroke-width="3" fill="none" opacity="0.4"/>')
    b.append(t(70, 250, "ТЕЛО В ГИДРОКОСТЮМЕ", 34, BRASS, ls=1))
    b.append(t(70, 1680, "спуск в воду", 28, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(f'<rect x="0" y="600" width="1080" height="1320" fill="#123742"/>')
    # бумаги
    b.append('<g class="paperA">')
    b.append(f'<rect x="120" y="700" width="520" height="700" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>')
    b.append(t(160, 790, "СОВЕРШЕННО СЕКРЕТНО", 22, RUST, w=900, ls=1))
    b.append(t(160, 890, "МАЙОР", 30, INK, w=900))
    b.append(t(160, 950, "У. МАРТИН", 42, INK, w=900))
    for i in range(6):
        b.append(f'<rect x="160" y="{1020+i*46}" width="{430-i*30}" height="14" fill="#8a7a5a" opacity="0.5"/>')
    b.append('</g>')
    b.append('<g class="paperB">')
    b.append(f'<rect x="560" y="820" width="420" height="560" fill="#f7edd6" stroke="{INK}" stroke-width="3"/>')
    b.append(t(600, 900, "ПЛАН", 26, RUST, w=900))
    b.append(t(600, 960, "ГРЕЦИЯ", 40, INK, w=900))
    b.append(f'<path d="M 600 1010 l 340 0 M 600 1060 l 300 0 M 600 1110 l 340 0" stroke="#8a7a5a" stroke-width="12" opacity="0.45"/>')
    b.append('</g>')
    b.append('<g class="stamp4">')
    b.append(f'<rect x="640" y="1180" width="300" height="90" rx="6" fill="none" stroke="{RUST}" stroke-width="6"/>')
    b.append(t(790, 1240, "ПОДБРОШЕНО", 28, RUST, "middle", 900))
    b.append('</g>')
    b.append(t(70, 250, "ПОРТФЕЛЬ", 44, BRASS, ls=4))
    b.append(t(70, 320, "майор Уильям Мартин", 26, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(map_panel(70, 620, 940, 900))
    # суша (условная)
    b.append(f'<path d="M 140 1080 q 120 -160 260 -140 q 60 90 -40 160 q -120 80 -220 -20 z" fill="#1c3e40" stroke="{BRASS}" stroke-width="2" opacity="0.9"/>')
    b.append(f'<path d="M 560 1020 q 60 120 20 260 q -40 60 -90 10 q -30 -140 20 -270 z" fill="#1c3e40" stroke="{BRASS}" stroke-width="2" opacity="0.9"/>')
    b.append(f'<path d="M 760 1000 q 120 30 150 120 q -20 90 -120 70 q -70 -80 -30 -190 z" fill="#1c3e40" stroke="{BRASS}" stroke-width="2" opacity="0.9"/>')
    b.append(node(250, 1100, "ИСПАНИЯ", FOG))
    b.append(node(600, 1180, "САРДИНИЯ", "#d98b2b"))
    b.append(f'<path d="M 640 1250 l 120 20 l -40 110 l -70 -20 z" fill="#1c3e40" stroke="{BRASS}" stroke-width="2" opacity="0.9"/>')
    b.append(node(700, 1310, "СИЦИЛИЯ", RUST))
    b.append(node(830, 1060, "ГРЕЦИЯ", BRASS))
    # ложная стрелка на Грецию
    b.append(f'<path class="arrowG" d="M 330 1120 q 240 -40 470 -30" stroke="{BRASS}" stroke-width="6" fill="none" stroke-dasharray="16 12"/>')
    b.append(f'<path class="headG" d="M 790 1082 l 22 8 l -14 20" fill="none" stroke="{BRASS}" stroke-width="6"/>')
    # реальная — Сардиния/Сицилия
    b.append(f'<path class="arrowS" d="M 900 1490 q -110 -90 -180 -140" stroke="{RUST}" stroke-width="7" fill="none" stroke-dasharray="18 12"/>')
    b.append(f'<path class="headG2" d="M 720 1350 l 2 -46 l 40 22" fill="none" stroke="{RUST}" stroke-width="7"/>')
    b.append(t(520, 1462, "ВЫСАДКА", 22, RUST, "middle", 900))
    b.append(t(70, 250, "КАРТА", 44, BRASS, ls=6))
    b.append(t(70, 320, "куда на самом деле", 26, CREAM, w=700))
    b.append(t(540, 1660, "немцы ждали удар по Греции", 26, CREAM, "middle", 700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(f'<rect x="0" y="1180" width="1080" height="740" fill="#20504f"/>')
    b.append(f'<rect x="0" y="1180" width="1080" height="40" fill="{CREAM}" opacity="0.25"/>')
    # десантный катер
    b.append('<g class="boat">')
    b.append(f'<path d="M 260 1180 L 820 1180 L 760 1300 L 320 1300 Z" fill="#243b3d"/>')
    b.append(f'<rect x="420" y="1100" width="240" height="80" fill="#2d4a4c"/>')
    b.append(f'<path d="M 700 1180 l 40 -110 l 20 0 l -20 110 z" fill="#2d4a4c"/>')
    b.append('</g>')
    for i, x in enumerate((340, 430, 520, 610)):
        b.append(f'<g class="sold"><circle cx="{x}" cy="1110" r="24" fill="{INK}"/><rect x="{x-20}" y="1136" width="40" height="48" fill="{INK}"/></g>')
    b.append(f'<path d="M 540 900 q 0 -140 0 -220" stroke="{RUST}" stroke-width="8" fill="none" stroke-dasharray="18 14"/>')
    b.append(f'<path d="M 540 660 l -26 34 l 52 0 z" fill="{RUST}"/>')
    b.append(t(70, 250, "СИЦИЛИЯ", 56, CREAM, ls=2))
    b.append(t(70, 320, "10 июля 1943", 26, BRASS, w=700))
    b.append(t(70, 1720, "высадка союзников", 26, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="#10222a"/>']
    # карточка
    b.append('<g class="card7">')
    b.append(f'<rect x="120" y="620" width="840" height="900" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>')
    b.append(f'<rect x="120" y="620" width="840" height="90" fill="{SEA}"/>')
    b.append(t(160, 680, "ЛИЧНОСТЬ НЕ УСТАНОВЛЕНА", 30, CREAM, w=900))
    b.append(f'<rect x="170" y="760" width="240" height="300" fill="#cfc2a2" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<path d="M 220 1040 q 40 -160 80 -180 q 40 20 60 180 z" fill="#9c8f70"/>')
    b.append(f'<circle cx="290" cy="880" r="42" fill="#9c8f70"/>')
    b.append(t(450, 800, "БЕЗДОМНЫЙ", 34, INK, w=900))
    b.append(t(450, 850, "имя неизвестно", 24, "#5a4a34", w=700))
    for i in range(4):
        b.append(f'<rect x="450" y="{900+i*50}" width="400" height="14" fill="#8a7a5a" opacity="0.55"/>')
    # отпечаток
    b.append('<g class="finger">')
    for i in range(5):
        b.append(f'<ellipse cx="700" cy="1180" rx="{70-i*12}" ry="{50-i*8}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.55"/>')
    b.append('</g>')
    b.append(t(160, 1260, "№ дела", 22, "#5a4a34", w=800))
    b.append(t(160, 1300, "OP. MINCEMEAT", 26, INK, w=900))
    b.append('</g>')
    b.append(t(70, 250, "ТЕЛО", 44, BRASS, ls=6))
    b.append(t(70, 320, "бездомный, которого не опознали", 24, CREAM, w=700))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{SEA}"/>']
    b.append(f'<circle cx="540" cy="900" r="440" fill="{SEA2}"/>')
    b.append(waves(1500, FOG, 0.2, "wf"))
    b.append(t(540, 700, "МЯСНОЙ", 86, CREAM, "middle", 900, ls=3))
    b.append(t(540, 800, "ФАРШ", 86, RUST, "middle", 900, ls=8))
    b.append(f'<rect x="330" y="860" width="420" height="3" fill="{BRASS}" opacity="0.7"/>')
    b.append(t(540, 930, "операция, которая сработала", 28, FOG, "middle", 700))
    b.append(t(540, 1660, "National Archives, UK", 26, BRASS, "middle", 700))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".case1", {opacity:0, y:40}, {opacity:1, y:0, duration:0.8, ease:"back.out(1.3)"}, 0.05);'
    'tl.fromTo(".cuff", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6}, 0.5);'
    'tl.fromTo(".hl", {opacity:0, y:14}, {opacity:1, y:0, duration:0.45, stagger:0.1}, 0.1);'
    'tl.to(".w1", {x:-40, duration:5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.to(".w2", {x:40, duration:6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);',
    'tl.fromTo(".sub", {opacity:0, y:30}, {opacity:1, y:0, duration:0.9}, 0.1);'
    'tl.to(".sub", {y:-10, duration:2.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.to(".w0, .w1, .w2, .w3", {x:30, duration:2.2, stagger:0.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".body", {opacity:0, y:-90}, {opacity:1, y:0, duration:1.2, ease:"power2.out"}, 0.1);'
    'tl.to(".bub", {y:-220, opacity:0, duration:2.4, stagger:0.12, repeat:-1, ease:"sine.out"}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5}, 0.2);',
    'tl.fromTo(".paperA", {opacity:0, x:-60}, {opacity:1, x:0, duration:0.8}, 0.1);'
    'tl.fromTo(".paperB", {opacity:0, x:60}, {opacity:1, x:0, duration:0.8}, 0.4);'
    'tl.fromTo(".stamp4", {opacity:0, scale:1.6}, {opacity:1, scale:1, duration:0.35, ease:"power4.out"}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".map", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.1);'
    'tl.fromTo(".nd", {opacity:0}, {opacity:1, duration:0.4, stagger:0.15}, 0.4);'
    'tl.fromTo(".arrowG", {opacity:0}, {opacity:1, duration:0.5}, 0.9);'
    'tl.to(".arrowG", {strokeDashoffset:-84, duration:1.6, repeat:-1, ease:"none"}, 1.0);'
    'tl.fromTo(".arrowS, .headG2", {opacity:0}, {opacity:1, duration:0.6}, 1.3);'
    'tl.to(".arrowS", {strokeDashoffset:-90, duration:2, repeat:-1, ease:"none"}, 1.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".boat", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.1);'
    'tl.to(".boat", {y:-8, duration:1.8, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".sold", {opacity:0, y:20}, {opacity:1, y:0, duration:0.5, stagger:0.1}, 0.5);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".card7", {opacity:0, y:30}, {opacity:1, y:0, duration:0.8}, 0.1);'
    'tl.fromTo(".finger", {opacity:0}, {opacity:1, duration:0.8}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.5, stagger:0.15}, 0.2);',
    'tl.fromTo(".hl", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7, stagger:0.2}, 0.2);'
    'tl.to(".wf", {x:-30, duration:5, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{SEA}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.02 }}, {{ scale:1.07, duration:{dur}, ease:"none" }}, 0);
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
