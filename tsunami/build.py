#!/usr/bin/env python3
"""«Цунами» — 8 сцен, изометрия как в референсе."""
import json
import math
import random
from pathlib import Path

ROOT = Path("/root/video-gen/tsunami")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)

T = json.load(open(ROOT / "timings.json"))
STARTS, TOTAL = T["starts"], T["total"]
B = []
for i in range(len(STARTS)):
    end = STARTS[i + 1] if i + 1 < len(STARTS) else TOTAL
    B.append((round(STARTS[i], 3), round(end - STARTS[i], 3)))

WHITE = "#ffffff"
NAVY = "#1e3d63"
YELLOW = "#f7e3a1"
SAND = "#e8c98a"
GREEN = "#6fae4a"
GREEN_D = "#4f8a35"
ORANGE = "#d9762f"
ORANGE_D = "#b4562a"
CRUST_TOP = "#3b3b3b"
BLUE1 = "#8fd3e8"
BLUE2 = "#2a94b5"
BLUE3 = "#1d6f8c"
BLUE4 = "#124f66"


def t(x, y, s, size=46, col=WHITE, anchor="start", w=900, ls=0, cls="hl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial" font-size="{size}" font-weight="{w}" '
            f'fill="{col}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def banner(cx, cy, w, h, text, size=64, cls="ban"):
    """Жёлтая лента с рваными краями."""
    return (f'<g class="{cls}"><path d="M {cx-w/2-30} {cy-h/2} l {w+60} 0 l -26 {h/2} l 26 {h/2} l {-w-60} 0 l 26 {-h/2} z" fill="{YELLOW}" opacity="0.95"/>'
            f'<text x="{cx}" y="{cy+size*0.36:.0f}" font-family="Nunito" font-size="{size}" font-weight="900" fill="{NAVY}" '
            f'text-anchor="middle" letter-spacing="4">{text}</text></g>')


def callout(x, y, w, text, size=24, cls="co", h=96):
    return (f'<g class="{cls}"><path d="M {x} {y} l {w} 0 l 0 {h-18} l -18 18 l {-w+18} 0 l -18 -18 z" fill="{NAVY}"/>'
            f'<text x="{x+w/2}" y="{y+h/2+size*0.34:.0f}" font-family="Nunito" font-size="{size}" font-weight="800" fill="{WHITE}" '
            f'text-anchor="middle">{text}</text></g>')


def ocean(sy=640, cls="oc"):
    """Водный блок в перспективе: верхняя грань + толстая передняя стенка."""
    return (f'<g class="{cls}">'
            f'<path d="M 40 {sy} L 1080 {sy-190} L 1080 {sy+300} L 40 {sy+520} Z" fill="{BLUE2}"/>'
            f'<path d="M 40 {sy+520} L 1080 {sy+300} L 1080 {sy+720} L 40 {sy+940} Z" fill="{BLUE3}"/>'
            f'<path d="M 40 {sy} L 1080 {sy-190} L 1080 {sy+60} L 40 {sy+250} Z" fill="{BLUE1}" opacity="0.30"/>'
            f'<path d="M 40 {sy+250} L 1080 {sy+60} L 1080 {sy+300} L 40 {sy+520} Z" fill="{BLUE4}" opacity="0.25"/>'
            f'</g>')


def crust(sy=640, cls="cr"):
    top = sy + 520
    top2 = sy + 300
    return (f'<g class="{cls}">'
            f'<path d="M 40 {top+180} L 1080 {top2+180} L 1080 {top2+620} L 40 {top+800} Z" fill="{ORANGE}"/>'
            f'<path d="M 40 {top+180} L 1080 {top2+180} L 1080 {top2+260} L 40 {top+260} Z" fill="{CRUST_TOP}"/>'
            f'<path d="M 40 {top+180} L 1080 {top2+180} L 1080 {top2+260} L 40 {top+260} Z" fill="none" stroke="{ORANGE_D}" stroke-width="3" opacity="0.5"/>'
            f'</g>')


def wave_crest(x, y, w, h, cls="wc", col=BLUE1, deep=BLUE3):
    """Длинный гребень: два асимметричных горба + пена."""
    return (f'<g class="{cls}">'
            f'<path d="M {x} {y+h} q {w*0.10} {-h*1.25} {w*0.30} {-h*1.05} q {w*0.18} {h*0.15} {w*0.34} {-h*0.55} '
            f'q {w*0.14} {-h*0.45} {w*0.36} {-h*0.10} l 0 {h*1.55} z" fill="{col}"/>'
            f'<path d="M {x} {y+h} q {w*0.10} {-h*1.25} {w*0.30} {-h*1.05} q {w*0.18} {h*0.15} {w*0.34} {-h*0.55} '
            f'q {w*0.14} {-h*0.45} {w*0.36} {-h*0.10}" fill="none" stroke="{WHITE}" stroke-width="5" opacity="0.9"/>'
            f'<path d="M {x+w*0.05:.0f} {y+h*0.55:.0f} q {w*0.3} {h*0.28} {w*0.66} {-h*0.05}" fill="none" stroke="{deep}" '
            f'stroke-width="6" opacity="0.28"/>'
            f'</g>')


def city(x, y, s=1.0, cls="ct"):
    b = [f'<g class="{cls}">']
    b.append(f'<path d="M {x-150*s} {y} q {150*s} {-90*s} {300*s} 0 z" fill="{GREEN}"/>')
    b.append(f'<path d="M {x-150*s} {y} l 0 {40*s} l {300*s} 0 l 0 {-40*s} z" fill="{GREEN_D}"/>')
    # дома
    b.append(f'<rect x="{x-110*s}" y="{y-90*s}" width="{46*s}" height="{90*s}" fill="#cfd8dd"/>')
    b.append(f'<rect x="{x-58*s}" y="{y-130*s}" width="{52*s}" height="{130*s}" fill="#b9c6cc"/>')
    b.append(f'<rect x="{x+4*s}" y="{y-70*s}" width="{40*s}" height="{70*s}" fill="#dde6ea"/>')
    b.append(f'<rect x="{x+52*s}" y="{y-110*s}" width="{46*s}" height="{110*s}" fill="#c4d0d6"/>')
    for i in range(3):
        b.append(f'<rect x="{x-100*s}" y="{y-78*s+i*24}" width="{10*s}" height="{10*s}" fill="{BLUE3}" opacity="0.6"/>')
        b.append(f'<rect x="{x-48*s}" y="{y-118*s+i*24}" width="{10*s}" height="{10*s}" fill="{BLUE3}" opacity="0.6"/>')
    # пальма
    b.append(f'<path d="M {x+112*s} {y} q {4*s} {-50*s} {16*s} {-70*s}" stroke="#8a6a45" stroke-width="{5*s}" fill="none"/>')
    for a in (-40, -10, 20, 50):
        b.append(f'<path d="M {x+128*s} {y-70*s} q {30*s} {-8*s} {44*s} {10*s}" stroke="{GREEN_D}" stroke-width="{6*s}" fill="none" '
                 f'transform="rotate({a} {x+128*s} {y-70*s})"/>')
    b.append('</g>')
    return "".join(b)


def arrow(x1, y1, x2, y2, cls="ar", col=WHITE, w=22):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    hx, hy = x2 - ux * 46, y2 - uy * 46
    return (f'<g class="{cls}"><path d="M {x1+px*w/2:.0f} {y1+py*w/2:.0f} L {hx+px*w/2:.0f} {hy+py*w/2:.0f} '
            f'L {hx+px*w:.0f} {hy+py*w:.0f} L {x2:.0f} {y2:.0f} L {hx-px*w:.0f} {hy-py*w:.0f} '
            f'L {hx-px*w/2:.0f} {hy-py*w/2:.0f} L {x1-px*w/2:.0f} {y1-py*w/2:.0f} Z" fill="{col}"/></g>')


# ---------------------------------------------------------------- 1
def s1():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(banner(540, 240, 620, 150, "ЦУНАМИ", 76, "ban1"))
    b.append(ocean(640, "oc1"))
    b.append(crust(640, "cr1"))
    b.append(city(830, 470, 1.05, "ct1"))
    b.append(wave_crest(120, 760, 560, 210, "wc1"))
    b.append(wave_crest(430, 830, 420, 150, "wc2"))
    b.append(callout(60, 1080, 380, "ВОЛНА РАСТЁТ У БЕРЕГА", 22, "co1"))
    b.append(t(60, 1620, "одна волна — и целый город", 26, NAVY, w=700))
    return b


# ---------------------------------------------------------------- 2
def s2():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(t(60, 170, "ЗЕМЛЕТРЯСЕНИЕ", 46, NAVY, w=900))
    b.append(ocean(620, "oc2"))
    b.append(crust(620, "cr2"))
    # очаг и волны от него
    b.append(f'<circle cx="520" cy="1300" r="26" fill="{WHITE}"/>')
    for i in range(4):
        b.append(f'<circle class="ring{i}" cx="520" cy="1300" r="{60+i*62}" fill="none" stroke="{WHITE}" stroke-width="3" opacity="{0.7-i*0.14:.2f}"/>')
    # разлом
    b.append(f'<path d="M 200 1170 L 420 1290 L 640 1150" stroke="{CRUST_TOP}" stroke-width="10" fill="none"/>')
    b.append(f'<path class="fault" d="M 300 1240 l 40 -60" stroke="{YELLOW}" stroke-width="10"/>')
    b.append(callout(560, 1420, 440, "ОЧАГ · ФОКУС", 22, "co2"))
    b.append(callout(120, 1500, 360, "ЭПИЦЕНТР", 22, "co3"))
    b.append(t(60, 1780, "дно сдвигается — вода получает толчок", 22, NAVY, w=700))
    return b


# ---------------------------------------------------------------- 3
def s3():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(t(60, 170, "ВОЛНЫ РАСХОДЯТСЯ", 44, NAVY, w=900))
    b.append(ocean(600, "oc3"))
    b.append(crust(600, "cr3"))
    b.append(f'<circle cx="540" cy="1120" r="20" fill="{WHITE}"/>')
    for i in range(3):
        b.append(f'<ellipse class="elp{i}" cx="540" cy="1120" rx="{120+i*150}" ry="{40+i*50}" fill="none" '
                 f'stroke="{YELLOW}" stroke-width="4" opacity="{0.8-i*0.18:.2f}"/>')
    b.append(arrow(540, 1120, 200, 900, "ar3a"))
    b.append(arrow(540, 1120, 900, 900, "ar3b"))
    b.append(callout(300, 1500, 480, "ВО ВСЕ СТОРОНЫ", 24, "co4"))
    return b


# ---------------------------------------------------------------- 4
def s4():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(t(60, 170, "В ОТКРЫТОМ ОКЕАНЕ", 40, NAVY, w=900))
    b.append(ocean(680, "oc4"))
    b.append(crust(680, "cr4"))
    # маленькая волна и корабль
    b.append(wave_crest(120, 800, 420, 70, "wc4"))
    b.append(f'<path d="M 700 780 l 150 0 l -22 44 l -106 0 z" fill="{NAVY}"/>')
    b.append(f'<rect x="760" y="720" width="10" height="60" fill="{NAVY}"/>')
    b.append(f'<path d="M 770 726 l 50 40 l -50 0 z" fill="{WHITE}" stroke="{NAVY}" stroke-width="3"/>')
    b.append(banner(540, 1220, 560, 130, "800 КМ/Ч", 68, "ban4"))
    b.append(t(60, 1400, "быстрее самолёта · высота всего 1 м", 24, NAVY, w=700))
    b.append(t(60, 1700, "корабли такую волну не замечают", 22, NAVY, w=700))
    return b


# ---------------------------------------------------------------- 5
def s5():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(t(60, 170, "ГЛУБИНА И ВЫСОТА", 40, NAVY, w=900))
    b.append(ocean(620, "oc5"))
    b.append(crust(620, "cr5"))
    b.append(f'<g class="meter"><rect x="120" y="980" width="60" height="300" rx="10" fill="{WHITE}" stroke="{NAVY}" stroke-width="4"/>'
             f'<rect x="126" y="1140" width="48" height="134" rx="6" fill="{BLUE2}"/>'
             f'<text x="210" y="1010" font-family="Nunito" font-size="30" font-weight="900" fill="{NAVY}">ВОЛНА</text>'
             f'<text x="210" y="1050" font-family="Nunito" font-size="30" font-weight="900" fill="{BLUE3}">1 М</text></g>')
    b.append(f'<g class="depth"><rect x="760" y="980" width="60" height="300" rx="10" fill="{WHITE}" stroke="{NAVY}" stroke-width="4"/>'
             f'<rect x="766" y="994" width="48" height="280" rx="6" fill="{BLUE3}"/>'
             f'<text x="620" y="1010" font-family="Nunito" font-size="30" font-weight="900" fill="{NAVY}" text-anchor="end">ГЛУБИНА</text>'
             f'<text x="620" y="1050" font-family="Nunito" font-size="30" font-weight="900" fill="{BLUE3}" text-anchor="end">4 КМ</text></g>')
    b.append(t(60, 1600, "вся энергия спрятана в толще воды", 22, NAVY, w=700))
    return b


# ---------------------------------------------------------------- 6
def s6():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(t(60, 170, "МЕЛЬЧЕЕТ — ТОРМОЗИТ", 38, NAVY, w=900))
    b.append(ocean(680, "oc6"))
    b.append(crust(680, "cr6"))
    # поднимающееся дно
    b.append(f'<path class="floor" d="M 640 1180 q 220 -40 420 -20 l 0 120 l -420 20 z" fill="{SAND}"/>')
    b.append(wave_crest(420, 900, 420, 170, "wc6"))
    b.append(wave_crest(700, 940, 300, 120, "wc6b"))
    b.append(arrow(300, 980, 480, 880, "ar6", WHITE, 18))
    b.append(callout(120, 1380, 420, "СКОРОСТЬ ПАДАЕТ", 22, "co5"))
    b.append(callout(600, 1480, 400, "ВЫСОТА РАСТЁТ", 22, "co6"))
    b.append(t(60, 1760, "дно работает как клин", 22, NAVY, w=700))
    return b


# ---------------------------------------------------------------- 7
def s7():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(ocean(730, "oc7"))
    b.append(crust(730, "cr7"))
    # стена воды над городом
    b.append(f'<path d="M 120 1180 q 120 -420 300 -380 q 160 40 160 260 q 0 120 120 120 l 0 220 l -580 0 z" fill="{BLUE2}"/>')
    b.append(f'<path d="M 120 1180 q 120 -420 300 -380 q 160 40 160 260 q 0 120 120 120" fill="none" stroke="{WHITE}" stroke-width="7" opacity="0.8"/>')
    b.append(city(780, 560, 0.85, "ct7"))
    b.append(banner(540, 300, 520, 130, "10–30 М", 66, "ban7"))
    b.append(t(60, 1400, "у берега волна встаёт стеной", 24, NAVY, w=700))
    b.append(t(60, 1720, "минуты до удара", 24, NAVY, w=800))
    return b


# ---------------------------------------------------------------- 8
def s8():
    b = [f'<rect width="1080" height="1920" fill="{WHITE}"/>']
    b.append(ocean(620, "oc8"))
    b.append(crust(620, "cr8"))
    b.append(f'<path d="M 120 900 q 200 -60 380 0 l 0 60 q -200 50 -380 0 z" fill="{SAND}"/>')
    b.append(city(820, 520, 0.9, "ct8"))
    b.append(arrow(420, 1180, 160, 1450, "ar8", NAVY, 26))
    b.append(banner(540, 1330, 520, 150, "БЕГИ", 84, "ban8"))
    b.append(t(540, 1560, "если море отступило — это не отлив", 26, NAVY, "middle", 800))
    b.append(callout(240, 1640, 600, "ДО БЕРЕГА — СЕКУНДЫ", 24, "co7"))
    return b


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8]
ANIM = [
    'tl.fromTo(".ban1", {opacity:0, scale:0.9}, {opacity:1, scale:1, duration:0.6, ease:"back.out(1.5)"}, 0.05);'
    'tl.fromTo(".oc1, .cr1", {opacity:0, y:30}, {opacity:1, y:0, duration:0.7, stagger:0.1}, 0.2);'
    'tl.fromTo(".wc1", {opacity:0, x:-60}, {opacity:1, x:0, duration:0.8}, 0.5);'
    'tl.to(".wc1", {y:-16, duration:1.4, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.to(".wc2", {y:14, duration:1.1, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".ct1", {opacity:0, y:20}, {opacity:1, y:0, duration:0.6}, 0.7);'
    'tl.fromTo(".co1", {opacity:0, x:-20}, {opacity:1, x:0, duration:0.5}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 1.2);',
    'tl.fromTo(".oc2, .cr2", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".ring0, .ring1, .ring2, .ring3", {opacity:0, scale:0.6}, {opacity:0.7, scale:1, duration:0.9, stagger:0.12}, 0.3);'
    'tl.fromTo(".fault", {opacity:0}, {opacity:1, duration:0.4}, 0.6);'
    'tl.fromTo(".co2, .co3", {opacity:0, y:14}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.1}, 0.2);',
    'tl.fromTo(".oc3, .cr3", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".elp0, .elp1, .elp2", {opacity:0, scale:0.7}, {opacity:0.8, scale:1, duration:0.8, stagger:0.15}, 0.3);'
    'tl.fromTo(".ar3a, .ar3b", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.6, stagger:0.15}, 0.7);'
    'tl.fromTo(".co4", {opacity:0}, {opacity:1, duration:0.5}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".oc4, .cr4", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".wc4", {opacity:0, x:-40}, {opacity:1, x:0, duration:0.7}, 0.3);'
    'tl.to(".wc4", {y:-10, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".ban4", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.12}, 0.2);',
    'tl.fromTo(".meter rect", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.2);'
    'tl.fromTo(".depth rect", {opacity:0}, {opacity:1, duration:0.5, stagger:0.1}, 0.4);'
    'tl.to(".meter", {y:-10, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.8);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".oc6, .cr6", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".floor", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.3);'
    'tl.fromTo(".wc6", {opacity:0, y:20}, {opacity:1, y:0, duration:0.7}, 0.5);'
    'tl.to(".wc6", {y:-14, duration:1.2, yoyo:true, repeat:-1, ease:"sine.inOut"}, 1.0);'
    'tl.fromTo(".ar6", {opacity:0}, {opacity:1, duration:0.5}, 0.9);'
    'tl.fromTo(".co5, .co6", {opacity:0, y:12}, {opacity:1, y:0, duration:0.5, stagger:0.15}, 1.0);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4}, 0.2);',
    'tl.fromTo(".oc7, .cr7", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.to(".city, .ct7", {x:6, duration:0.12, yoyo:true, repeat:9}, 0.6);'
    'tl.fromTo(".ban7", {opacity:0, scale:0.85}, {opacity:1, scale:1, duration:0.5, ease:"back.out(1.6)"}, 0.4);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.12}, 0.2);',
    'tl.fromTo(".oc8, .cr8", {opacity:0}, {opacity:1, duration:0.6}, 0.05);'
    'tl.fromTo(".ban8", {opacity:0, scale:0.8}, {opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}, 0.3);'
    'tl.to(".ban8", {scale:1.04, duration:0.6, yoyo:true, repeat:-1, ease:"sine.inOut"}, 0.9);'
    'tl.fromTo(".ar8", {opacity:0, x:20}, {opacity:1, x:0, duration:0.6}, 0.6);'
    'tl.fromTo(".co7", {opacity:0}, {opacity:1, duration:0.5}, 0.9);'
    'tl.fromTo(".hl", {opacity:0}, {opacity:1, duration:0.4, stagger:0.12}, 0.2);',
]


def page(sid, body, dur, anim):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{WHITE}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
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
