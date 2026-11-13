#!/usr/bin/env python3
"""«33» — Чили, 2010. 8 сцен, персонажи, движение по словам озвучки."""
import json
import math
from pathlib import Path

ROOT = Path("/root/video-gen/chile")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, DURS, TOTAL = T["starts"], T["durs"], T["total"]
N = 8
BOUNDS = []
for i in range(N):
    st = STARTS[i]
    end = STARTS[i + 1] if i + 1 < N else TOTAL
    BOUNDS.append((round(st, 3), round(end - st, 3)))

DARK = "#080c0e"
NIGHT = "#0d1418"
ROCK = "#3a352f"
ROCK_L = "#4a443c"
SUIT = "#2b4a63"
SUIT2 = "#3a5a70"
HELM = "#e0a33e"
HELM2 = "#c9d4de"
SKIN = "#f2c9a4"
RED = "#c0392b"
CREAM = "#f0e6d2"
AMBER = "#ffd98a"

DEFS = f"""<defs>
<linearGradient id="rockG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f3a33"/><stop offset="1" stop-color="#221f1b"/></linearGradient>
<linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22303c"/><stop offset="1" stop-color="#121a20"/></linearGradient>
<radialGradient id="lampG"><stop offset="0" stop-color="#ffe6b0" stop-opacity="0.85"/><stop offset="1" stop-color="#ffe6b0" stop-opacity="0"/></radialGradient>
<linearGradient id="shaftG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#12100e"/><stop offset="0.5" stop-color="#1b1814"/><stop offset="1" stop-color="#12100e"/></linearGradient>
</defs>"""


def svg(body):
    return f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>'


def person(cx, by, s=1.0, helmet=HELM, suit=SUIT, pose="stand", cls="", no_helmet=False, hair="#3b2a20"):
    """Фигура с суставами; координаты абсолютные, без transform."""
    hh = 200 * s
    hip = by - 78 * s
    sh = by - 148 * s
    head = by - 176 * s
    r = 15 * s
    legs, arms = "", ""
    if pose == "kneel":
        hip = by - 52 * s
        sh = by - 104 * s
        head = by - 132 * s
        legs = (f'<path d="M {cx-8*s} {hip} L {cx-26*s} {by-8*s} L {cx-6*s} {by}" stroke="{suit}" stroke-width="{16*s}" fill="none" stroke-linecap="round"/>'
                f'<path d="M {cx+8*s} {hip} L {cx+20*s} {by-30*s} L {cx+44*s} {by-30*s}" stroke="{suit}" stroke-width="{16*s}" fill="none" stroke-linecap="round"/>')
        arms = (f'<path d="M {cx-16*s} {sh+10*s} L {cx-30*s} {sh+52*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>'
                f'<path d="M {cx+16*s} {sh+10*s} L {cx+34*s} {sh+46*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>')
    else:
        spread = 22 * s if pose == "walk" else 12 * s
        kx1, kx2 = -spread, spread
        legs = (f'<path d="M {cx-6*s} {hip} L {cx+kx1} {by-40*s} L {cx+kx1-4*s} {by}" stroke="{suit}" stroke-width="{16*s}" fill="none" stroke-linecap="round"/>'
                f'<path d="M {cx+6*s} {hip} L {cx+kx2} {by-40*s} L {cx+kx2+4*s} {by}" stroke="{suit}" stroke-width="{16*s}" fill="none" stroke-linecap="round"/>')
        if pose == "armsup":
            arms = (f'<path d="M {cx-16*s} {sh+8*s} L {cx-40*s} {sh-40*s} L {cx-46*s} {sh-80*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>'
                    f'<path d="M {cx+16*s} {sh+8*s} L {cx+40*s} {sh-40*s} L {cx+46*s} {sh-80*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>')
        elif pose == "point":
            arms = (f'<path d="M {cx-16*s} {sh+8*s} L {cx-26*s} {sh+44*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>'
                    f'<path d="M {cx+16*s} {sh+8*s} L {cx+58*s} {sh+16*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>')
        else:
            arms = (f'<path d="M {cx-16*s} {sh+8*s} L {cx-26*s} {sh+46*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>'
                    f'<path d="M {cx+16*s} {sh+8*s} L {cx+26*s} {sh+46*s}" stroke="{suit}" stroke-width="{12*s}" fill="none" stroke-linecap="round"/>')
    torso = (f'<path d="M {cx-18*s} {sh} L {cx+18*s} {sh} L {cx+14*s} {hip} L {cx-14*s} {hip} Z" fill="{suit}"/>'
             f'<rect x="{cx-18*s}" y="{sh+18*s}" width="{36*s}" height="{6*s}" fill="{AMBER}" opacity="0.55"/>')
    if no_helmet:
        headg = (f'<circle cx="{cx}" cy="{head}" r="{r}" fill="{SKIN}"/>'
                 f'<path d="M {cx-r-2} {head+2} a {r+2} {r+2} 0 0 1 {2*(r+2)} 0 z" fill="{hair}"/>')
    else:
        headg = (f'<circle cx="{cx}" cy="{head}" r="{r}" fill="{SKIN}"/>'
                 f'<path d="M {cx-r-1} {head-2} a {r+1} {r+1} 0 0 1 {2*(r+1)} 0 z" fill="{helmet}"/>'
                 f'<rect x="{cx-r-6}" y="{head-3}" width="{2*r+12}" height="{4*s}" rx="{2*s}" fill="{helmet}" opacity="0.9"/>')
    return f'<g class="{cls}">{legs}{torso}{arms}{headg}</g>'


def helmet_big(cx, cy, s=1.0, num="33"):
    return (f'<g class="helmBig"><path d="M {cx-70*s} {cy} a {70*s} {70*s} 0 0 1 {140*s} 0 z" fill="{HELM}"/>'
            f'<rect x="{cx-86*s}" y="{cy-6*s}" width="{172*s}" height="{16*s}" rx="{8*s}" fill="{HELM}"/>'
            f'<rect x="{cx-18*s}" y="{cy-56*s}" width="{36*s}" height="{6*s}" fill="#000" opacity="0.25"/>'
            f'<text x="{cx}" y="{cy-22*s}" font-family="Nunito, Arial" font-size="{26*s}" font-weight="900" fill="#1a1208" text-anchor="middle">{num}</text></g>')


def head_txt(lines, y=170, size=74):
    return "".join(
        f'<text class="hl" x="54" y="{y + i*(size+20)}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="{size}" font-weight="900" letter-spacing="-1">{t}</text>' for i, (t, c) in enumerate(lines))


def tag(x, y, t, size=34, col=AMBER):
    return (f'<text class="tag" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" font-size="{size}" '
            f'font-weight="900" fill="{col}" opacity="0.9">{t}</text>')


# ---------------------------------------------------------------- S1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{DARK}"/>']
    b.append(f'<path class="beam" d="M 540 520 L 190 1500 L 890 1500 Z" fill="url(#lampG)" opacity="0.85"/>')
    b.append(f'<ellipse cx="540" cy="520" rx="26" ry="16" fill="#fff3d0" opacity="0.9"/>')
    b.append(helmet_big(540, 1290, 2.3))
    b.append(f'<rect x="0" y="1560" width="1080" height="360" fill="#05080a"/>')
    for i in range(26):
        b.append(f'<circle class="dust" cx="{150 + (i*97) % 780}" cy="{640 + (i*163) % 780}" r="{2 + i%4}" fill="{AMBER}" opacity="0.35"/>')
    b.append(head_txt([("33 ПОД ЗЕМЛЁЙ", "#ffffff"), ("69 ДНЕЙ", HELM)], 190, 70))
    return svg("".join(b))


# ---------------------------------------------------------------- S2
def s2():
    b = [f'<rect width="1080" height="1920" fill="url(#rockG)"/>']
    # ствол и выработки
    b.append(f'<rect x="450" y="120" width="180" height="1800" fill="url(#shaftG)"/>')
    b.append(f'<rect x="450" y="120" width="10" height="1800" fill="#0c0a08" opacity="0.6"/>')
    b.append(f'<rect x="60" y="900" width="420" height="110" fill="#141210"/>')
    b.append(f'<rect x="600" y="900" width="420" height="110" fill="#141210"/>')
    b.append(f'<rect x="60" y="1310" width="900" height="110" fill="#141210"/>')
    b.append(f'<rect x="150" y="1520" width="360" height="120" fill="#141210"/>')
    # крепь
    for x in (470, 600):
        b.append(f'<rect class="beamB" x="{x}" y="300" width="12" height="1500" fill="#6b4a2a" opacity="0.85"/>')
    b.append(f'<rect class="beamB" x="450" y="700" width="180" height="10" fill="#6b4a2a" opacity="0.7"/>')
    # падающая порода
    for i in range(22):
        b.append(f'<rect class="rock" x="{410 + (i*47) % 280}" y="{150 + (i*61) % 520}" width="{14 + i%4*9}" height="{12 + i%3*8}" rx="3" fill="{ROCK_L}"/>')
    b.append(f'<g class="dust2">' + "".join(
        f'<circle cx="{300 + (i*71) % 600}" cy="{700 + (i*97) % 700}" r="{4 + i%5}" fill="#8a7a68" opacity="0.35"/>' for i in range(18)) + '</g>')
    # люди бегут к убежищу
    for i, x in enumerate((600, 665, 730, 795, 860)):
        b.append(person(x, 1520, 0.92, HELM if i % 2 == 0 else HELM2, SUIT if i % 3 else SUIT2, "walk", f"runner r{i}"))
    b.append(f'<rect x="70" y="1340" width="160" height="200" fill="#1a1a18" stroke="#2a2a26" stroke-width="4"/>')
    b.append(tag(78, 1570, "УБЕЖИЩЕ", 26, HELM))
    b.append(head_txt([("5 АВГУСТА", "#ffffff"), ("ВЫХОД ЗАВАЛЕН", RED)], 170, 58))
    return svg("".join(b))


# ---------------------------------------------------------------- S3
def s3():
    b = [f'<rect width="1080" height="1920" fill="#12100e"/>']
    b.append(f'<rect x="60" y="300" width="960" height="1300" fill="#1a1815" stroke="#2a2620" stroke-width="6"/>')
    b.append(f'<rect x="60" y="300" width="960" height="40" fill="#242019"/>')
    # 33 человека рядами
    n = 0
    for row in range(4):
        for col in range(9):
            if n >= 33:
                break
            x = 130 + col * 100
            y = 1250 - row * 150
            b.append(person(x, y, 0.55, HELM if n % 4 else HELM2, SUIT if n % 5 else SUIT2, "stand", f"p{n}"))
            n += 1
    # Марио с камерой
    b.append(person(300, 1480, 1.0, HELM2, SUIT2, "point", "mario"))
    b.append(f'<circle class="camlight" cx="360" cy="1400" r="150" fill="url(#lampG)" opacity="0.35"/>')
    # Урсуа считает
    b.append(person(760, 1480, 1.05, HELM, SUIT, "point", "urzu"))
    b.append(head_txt([("УБЕЖИЩЕ", "#ffffff"), ("50 М² · 33 ЧЕЛОВЕКА", HELM)], 150, 56))
    b.append(tag(70, 1640, "ЕДА: 3 ДНЯ   ВОДА: ПО ГЛОТКУ", 26, CREAM))
    return svg("".join(b))


# ---------------------------------------------------------------- S4
def s4():
    b = [f'<rect width="1080" height="1920" fill="url(#skyG)"/>']
    b.append(f'<rect x="0" y="1440" width="1080" height="480" fill="#1a1f24"/>')
    # буровая
    b.append(f'<g class="rig"><rect x="760" y="980" width="16" height="460" fill="#5f6b74"/>'
             f'<rect x="700" y="1420" width="140" height="30" fill="#3a4650"/>'
             f'<rect class="mast" x="762" y="700" width="20" height="290" fill="#8d99a3"/>'
             f'<path d="M 742 1420 L 772 760 L 802 1420" stroke="#8d99a3" stroke-width="6" fill="none" opacity="0.7"/></g>')
    # палатки
    for i, x in enumerate((90, 230, 370)):
        b.append(f'<path d="M {x} 1440 l 70 -90 l 70 90 z" fill="#4a545c"/><rect x="{x+30}" y="1440" width="80" height="8" fill="#2a3038"/>')
    # ограждение
    b.append(f'<rect x="0" y="1500" width="1080" height="6" fill="#8d99a3" opacity="0.6"/>')
    for i in range(14):
        b.append(f'<rect x="{20 + i*78}" y="1440" width="6" height="120" fill="#8d99a3" opacity="0.5"/>')
    # толпа
    for i in range(12):
        x = 60 + i * 85
        b.append(person(x, 1660, 0.75, HELM2 if i % 3 else "#b0b8c0", "#3a4a58" if i % 2 else "#4a3a3a", "stand" if i % 2 else "point", f"crowd c{i}"))
    b.append(person(640, 1500, 1.05, suit="#1f2a33", pose="point", cls="minister", no_helmet=True))
    b.append(person(300, 1570, 1.0, suit="#6b3a3a", pose="stand", cls="wife", no_helmet=True, hair="#4a3323"))
    b.append(f'<g class="signWife"><rect x="250" y="1390" width="120" height="80" rx="4" fill="{CREAM}"/>'
             f'<text x="310" y="1446" font-family="Nunito, Arial" font-size="40" font-weight="900" fill="{RED}" text-anchor="middle">33</text></g>')
    b.append(head_txt([("17 ДНЕЙ", "#ffffff"), ("БЕЗ СИГНАЛА", RED)], 160, 66))
    b.append(tag(70, 1830, "СЕМЬИ ЖИВУТ У ВОРОТ", 28, CREAM))
    return svg("".join(b))


# ---------------------------------------------------------------- S5
def s5():
    b = [f'<rect width="1080" height="1920" fill="#0f1214"/>']
    b.append(f'<rect x="380" y="200" width="320" height="1200" fill="url(#shaftG)"/>')
    b.append(f'<rect class="drill" x="490" y="260" width="100" height="1100" fill="#5f6b74"/>')
    for i in range(12):
        b.append(f'<rect x="470" y="{300 + i*88}" width="140" height="10" fill="#8d99a3" opacity="0.5"/>')
    b.append(f'<g class="capsule"><rect x="470" y="980" width="140" height="180" rx="14" fill="#c9a24a"/>'
             f'<rect x="486" y="1004" width="108" height="60" rx="8" fill="#8d99a3"/>'
             f'<circle cx="540" cy="1120" r="16" fill="{AMBER}"/></g>')
    # руки и записка
    b.append(f'<g class="note"><rect x="330" y="1280" width="420" height="240" rx="6" fill="#efe6d2" transform="rotate(-4 540 1400)"/>'
             f'<text x="540" y="1390" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#2a2118" text-anchor="middle">ESTAMOS BIEN</text>'
             f'<text x="540" y="1440" font-family="Nunito, Arial" font-size="34" font-weight="900" fill="#2a2118" text-anchor="middle">LOS 33</text></g>')
    for i, x in enumerate((330, 750)):
        b.append(person(x, 1700, 1.0, HELM2 if i else HELM, SUIT2 if i else SUIT, "point", f"hand{i}"))
    b.append(head_txt([("22 АВГУСТА", "#ffffff"), ("ЗАПИСКА", HELM)], 150, 60))
    return svg("".join(b))


# ---------------------------------------------------------------- S6
def s6():
    b = [f'<rect width="1080" height="1920" fill="#0a0e10"/>']
    b.append(f'<rect x="430" y="300" width="220" height="1200" fill="url(#shaftG)"/>')
    b.append(f'<rect x="430" y="300" width="8" height="1200" fill="#2a3038"/>')
    b.append(f'<rect x="642" y="300" width="8" height="1200" fill="#2a3038"/>')
    b.append(f'<g class="capsule2"><rect x="470" y="1180" width="140" height="200" rx="16" fill="#c9a24a"/>'
             f'<rect x="486" y="1206" width="108" height="70" rx="8" fill="#8d99a3"/>'
             f'<circle cx="540" cy="1330" r="16" fill="{AMBER}"/>'
             f'<line x1="540" y1="1180" x2="540" y2="120" stroke="#c9d4de" stroke-width="4"/></g>')
    b.append(f'<text class="counter" x="700" y="1300" font-family="Nunito, Arial" font-size="54" font-weight="900" fill="{AMBER}">700</text>')
    b.append(f'<text x="700" y="1348" font-family="Nunito, Arial" font-size="24" font-weight="800" fill="#8d99a3">МЕТРОВ</text>')
    # верх: площадка, люди
    b.append(f'<rect x="280" y="300" width="520" height="26" fill="#5f6b74"/>')
    b.append(f'<rect x="352" y="338" width="70" height="24" rx="4" fill="#8d99a3"/>')
    b.append(person(300, 372, 0.72, HELM2, "#2b6f8a", "armsup", "manuel"))
    b.append(person(420, 376, 0.7, HELM, SUIT, "kneel", "first"))
    for i in range(4):
        b.append(person(520 + i * 70, 372, 0.6, HELM, SUIT, "armsup" if i % 2 else "stand", f"top{i}"))
    b.append(head_txt([("13 ОКТЯБРЯ", "#ffffff"), ("ПОДЪЁМ", HELM)], 60, 54))
    return svg("".join(b))


# ---------------------------------------------------------------- S7
def s7():
    b = [f'<rect width="1080" height="1920" fill="#0a0e10"/>']
    b.append(f'<rect x="0" y="0" width="1080" height="1920" fill="#101417"/>')
    b.append(f'<rect x="0" y="1500" width="1080" height="420" fill="#1a2024"/>')
    b.append(f'<g class="capsule3"><rect x="430" y="1080" width="220" height="300" rx="20" fill="#c9a24a"/>'
             f'<rect x="456" y="1120" width="168" height="90" rx="10" fill="#1a2024"/>'
             f'<circle cx="540" cy="1290" r="24" fill="{AMBER}"/></g>')
    b.append(person(540, 1500, 1.9, HELM, SUIT, "stand", "urzu"))
    b.append(f'<g class="helmOff"><path d="M 620 1180 a 40 40 0 0 1 80 0 z" fill="{HELM}"/>'
             f'<rect x="608" y="1178" width="104" height="10" rx="5" fill="{HELM}"/></g>')
    for i in range(9):
        b.append(person(80 + i * 115, 1760, 0.8, HELM2 if i % 2 else HELM, "#3a4a58", "armsup" if i % 3 == 0 else "stand", f"cr{i}"))
    b.append(head_txt([("33 ИЗ 33", HELM), ("ДОМОЙ", "#ffffff")], 150, 72))
    return svg("".join(b))


# ---------------------------------------------------------------- S8
def s8():
    b = [f'<rect width="1080" height="1920" fill="#05080a"/>']
    for i in range(33):
        row, col = divmod(i, 11)
        x = 110 + col * 86
        y = 700 + row * 300
        b.append(f'<g class="helmItem h{i}"><path d="M {x-34} {y} a 34 34 0 0 1 68 0 z" fill="{HELM}" opacity="0.25"/>'
                 f'<rect x="{x-42}" y="{y-3}" width="84" height="8" rx="4" fill="{HELM}" opacity="0.25"/>'
                 f'<text x="{x}" y="{y+34}" font-family="Nunito, Arial" font-size="18" font-weight="900" fill="#8a7a50" text-anchor="middle">{i+1}</text></g>')
    b.append(f'<text class="fin1" x="540" y="1720" font-family="Nunito, Arial" font-size="58" font-weight="900" fill="#ffffff" text-anchor="middle" opacity="0">САН-ХОСЕ · 2010</text>')
    b.append(f'<text class="fin2" x="540" y="1790" font-family="Nunito, Arial" font-size="36" font-weight="800" fill="{HELM}" text-anchor="middle" opacity="0">33 · ВСЕ ЖИВЫ</text>')
    return svg("".join(b))


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
NAMES = [f"s{i+1}" for i in range(8)]


def page(sid, body, dur):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{DARK}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">{body}</div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:24 }}, {{ opacity:1, y:0, duration:0.5, stagger:0.12, ease:"power3.out" }}, 0.05);
    tl.fromTo(".tag", {{ opacity:0 }}, {{ opacity:0.9, duration:0.6 }}, 0.6);
    tl.to(".dust", {{ y:-120, opacity:0, duration:4.0, stagger:{{each:0.08, from:"random"}}, repeat:2, ease:"none" }}, 0);
    tl.to(".beam", {{ opacity:0.55, duration:1.6, yoyo:true, repeat:5, ease:"sine.inOut" }}, 0);
    tl.to(".helmBig", {{ rotation:6, svgOrigin:"540 1290", duration:2.4, yoyo:true, repeat:4, ease:"sine.inOut" }}, 0.2);
    tl.to(".rock", {{ y:700, opacity:0, duration:3.4, stagger:0.16, ease:"power1.in" }}, 0);
    tl.to(".beamB", {{ rotation:3, svgOrigin:"480 900", duration:2.0, yoyo:true, repeat:3, ease:"sine.inOut" }}, 0.2);
    tl.to(".runner", {{ x:180, duration:2.2, stagger:0.08, ease:"power1.in" }}, 0.1);
    tl.to(".dust2", {{ y:-60, duration:3.0, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0);
    tl.to(".camlight", {{ x:300, y:-60, duration:3.4, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0);
    tl.to(".mario", {{ x:-40, duration:3.0, yoyo:true, repeat:1, ease:"sine.inOut" }}, 0);
    tl.to(".urzu", {{ y:-6, duration:1.4, yoyo:true, repeat:3, ease:"sine.inOut" }}, 0);
    tl.to(".mast", {{ y:-120, duration:2.6, ease:"power2.out" }}, 0.2);
    tl.to(".crowd", {{ x:26, duration:2.0, stagger:0.06, yoyo:true, repeat:2, ease:"sine.inOut" }}, 0);
    tl.to(".drill", {{ y:9, duration:0.16, yoyo:true, repeat:24, ease:"none" }}, 0);
    tl.to(".capsule", {{ y:-90, duration:2.4, ease:"power1.inOut" }}, 0.4);
    tl.to(".note", {{ y:-30, rotation:-2, svgOrigin:"540 1400", duration:2.2, ease:"power2.out" }}, 0.8);
    tl.to(".capsule2", {{ y:-940, duration:{dur-1.2}, ease:"none" }}, 0.6);
    tl.to(".capsule3", {{ y:-40, duration:2.0, ease:"power2.out" }}, 0.1);
    tl.to(".helmOff", {{ y:-230, rotation:24, svgOrigin:"660 1180", duration:1.8, ease:"power2.out" }}, 1.0);
    tl.to(".helmItem", {{ opacity:1, duration:0.35, stagger:0.06 }}, 1.4);
    tl.to(".fin1", {{ opacity:1, duration:0.6 }}, 3.0);
    tl.to(".fin2", {{ opacity:1, duration:0.6 }}, 3.4);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build():
    hosts = []
    for i, sid in enumerate(NAMES):
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
