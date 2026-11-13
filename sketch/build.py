#!/usr/bin/env python3
"""«Как рисуется дом» — 30 с, один таймлайн: линии рисуются, заливки проявляются."""
import json
import random
from pathlib import Path

ROOT = Path("/root/video-gen/sketch")
TOTAL = 30.0
PAPER = "#f2ece1"
INK = "#2b2b2b"
WOOD = "#8b5a3c"
GLASS = "#cfe6f2"
ROOF = "#39474f"
TERR = "#d8c7a8"
GREEN = "#7d9b6a"
GUIDE = "#a9c7d8"


def S(d, w=4, col=INK, cls="draw", extra=""):
    """Штрих, который «рисуется» (pathLength=1)."""
    return (f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" pathLength="1" '
            f'stroke-dasharray="1" stroke-dashoffset="1" {extra}/>')


def F(d, col, op=1.0, cls=""):
    return f'<path class="fillshape {cls}" d="{d}" fill="{col}" opacity="0"/>'


def build():
    rnd = random.Random(4)
    grain = "".join(
        f'<circle cx="{rnd.uniform(0,1080):.0f}" cy="{rnd.uniform(0,1920):.0f}" r="{rnd.uniform(0.6,1.8):.1f}" '
        f'fill="#8a7f6a" opacity="{rnd.uniform(0.05,0.16):.2f}"/>' for _ in range(260))

    body = [f'<rect width="1080" height="1920" fill="{PAPER}"/>', f'<g>{grain}</g>']

    # ---------- заливки (появляются на 4-м этапе) ----------
    body.append('<g class="fills">')
    body.append(F("M 150 1260 L 330 600 L 510 1260 Z", GLASS, 0.55, "glass"))
    body.append(F("M 480 790 L 760 790 L 760 1260 L 480 1260 Z", WOOD, 0.9, "wood"))
    body.append(F("M 760 800 L 900 800 A 120 120 0 0 1 900 1260 L 760 1260 Z", WOOD, 0.85, "wood"))
    body.append(F("M 150 1260 L 330 600 L 510 1260 L 480 1260 L 330 660 L 180 1260 Z", ROOF, 0.9, "roof"))
    body.append(F("M 480 790 L 1010 790 L 1010 830 L 480 830 Z", ROOF, 0.85, "roof"))
    body.append(F("M 600 840 L 745 840 L 745 1110 L 600 1110 Z", GLASS, 0.85, "glass"))
    body.append(F("M 820 880 L 900 880 L 940 920 L 940 1100 L 820 1100 Z", GLASS, 0.8, "glass"))
    body.append(F("M 150 1260 L 1020 1260 L 1020 1300 L 150 1300 Z", TERR, 0.95, "terr"))
    body.append('</g>')

    # ---------- 1 этап: габариты ----------
    body.append('<g class="stage1">')
    body.append(S("M 70 1260 L 1010 1260", 3, GUIDE))
    body.append(S("M 90 1300 L 1030 1300", 2, GUIDE, "draw g2"))
    body.append(S("M 150 1260 L 150 600", 2, GUIDE))
    body.append(S("M 510 1260 L 510 600", 2, GUIDE))
    body.append(S("M 760 1260 L 760 780", 2, GUIDE))
    body.append(S("M 1020 1260 L 1020 800", 2, GUIDE))
    body.append(S("M 330 620 L 330 1260", 2, GUIDE))
    body.append('</g>')

    # ---------- 2 этап: контур ----------
    body.append('<g class="stage2">')
    body.append(S("M 150 1260 L 330 600 L 510 1260", 7))
    body.append(S("M 176 1260 L 330 664 L 484 1260", 4))
    body.append(S("M 480 790 L 760 790 L 760 1260", 7))
    body.append(S("M 760 800 L 900 800 A 120 120 0 0 1 900 1260 L 760 1260", 7))
    body.append(S("M 480 790 L 1010 790 L 1010 830", 5))
    body.append(S("M 150 1260 L 1020 1260", 6))
    body.append('</g>')

    # ---------- 3 этап: окна, двери, перила ----------
    body.append('<g class="stage3">')
    body.append(S("M 600 840 L 745 840 L 745 1110 L 600 1110 Z", 4))
    body.append(S("M 672 840 L 672 1110", 3))
    body.append(S("M 600 975 L 745 975", 3))
    body.append(S("M 700 1140 L 760 1140 L 760 1260", 4))
    body.append(S("M 820 880 L 900 880 L 940 920 L 940 1100", 4))
    body.append(S("M 150 1150 L 1010 1150", 4))
    for x in range(160, 1011, 68):
        body.append(S(f"M {x} 1150 L {x} 1260", 3))
    body.append(S("M 560 1260 L 560 1330 L 640 1330 L 640 1260", 4))
    body.append(S("M 560 1300 L 640 1300", 3))
    body.append('</g>')

    # ---------- 5 этап: дерево, кусты, тень ----------
    body.append('<g class="stage5">')
    body.append(S("M 560 1240 L 560 800", 9, "#4a3120"))
    body.append(S("M 560 1090 L 486 1006 M 560 1040 L 636 952 M 560 990 L 506 908 M 560 950 L 610 874", 5, "#4a3120"))
    body.append(S("M 560 900 L 516 836 M 560 880 L 600 820", 4, "#4a3120"))
    for cx, cy, rx, ry, rot in ((508, 742, 66, 50, -18), (592, 726, 58, 46, 14), (546, 668, 72, 54, -6),
                                 (470, 800, 48, 36, 8), (626, 790, 46, 34, -12), (546, 792, 60, 40, 0)):
        body.append(f'<ellipse class="draw" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" '
                    f'fill="none" stroke="{GREEN}" stroke-width="4" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
        body.append(f'<ellipse class="fillshape" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" '
                    f'fill="{GREEN}" opacity="0"/>')
    body.append(F("M 470 1250 q 90 -60 180 0 z", GREEN, 0.25))
    for i, x in enumerate(range(80, 1030, 68)):
        rr = 22 + (i % 4) * 5
        body.append(S(f"M {x-rr} 1332 a {rr} {rr} 0 1 0 {2*rr} 0 a {rr} {rr} 0 1 0 {-2*rr} 0", 2.5, "#6f8f5c"))
        body.append(F(f"M {x-rr} 1332 a {rr} {rr} 0 1 0 {2*rr} 0 a {rr} {rr} 0 1 0 {-2*rr} 0", "#8fae74", 0.75))
    for yy in range(860, 1250, 34):
        body.append(S(f"M 492 {yy} L 748 {yy}", 2, "#6f452c"))
    for yy in range(850, 1250, 40):
        body.append(S(f"M 790 {yy} L 930 {yy}", 2, "#6f452c"))
    body.append(S("M 90 1310 L 1010 1310", 3, "#9a8f7a"))
    body.append('</g>')

    # ---------- 6 этап: акценты ----------
    body.append('<g class="stage6">')
    body.append(S("M 330 664 L 330 600", 5))
    body.append(S("M 480 790 L 480 830", 4))
    body.append(S("M 150 1260 L 1020 1260", 5))
    body.append('<text class="sig" x="930" y="1660" font-family="Caveat, Nunito, cursive" font-size="46" '
                'fill="#5a5a5a" text-anchor="middle" opacity="0">terrasa</text>')
    body.append('</g>')

    # заголовок
    body.append('<text class="ttl" x="70" y="300" font-family="Nunito, Arial" font-size="54" font-weight="900" '
                'fill="#2b2b2b" opacity="0">КАК РИСУЕТСЯ ДОМ</text>')
    body.append('<text class="ttl2" x="70" y="360" font-family="Nunito, Arial" font-size="30" font-weight="800" '
                'fill="#7a6a52" opacity="0">скетч за 30 секунд</text>')

    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=Caveat:wght@600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{PAPER}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.world{{position:absolute;inset:0;width:100%;height:100%}}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{''.join(body)}</svg>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
window.__timelines = {{}};
tl.fromTo(".world", {{scale:1.05}}, {{scale:1.0, duration:{TOTAL}, ease:"none"}}, 0);
// 1 этап — габариты
tl.to(".stage1 .draw", {{attr:{{"stroke-dashoffset":0}}, duration:0.9, stagger:0.35, ease:"none"}}, 0.6);
// 2 этап — контур
tl.to(".stage2 .draw", {{attr:{{"stroke-dashoffset":0}}, duration:1.4, stagger:0.5, ease:"none"}}, 4.9);
// 3 этап — детали
tl.to(".stage3 .draw", {{attr:{{"stroke-dashoffset":0}}, duration:0.7, stagger:0.06, ease:"none"}}, 9.6);
// 4 этап — заливки
tl.to(".fills .fillshape", {{opacity:1, duration:0.9, stagger:0.22}}, 14.2);
tl.to(".wood", {{opacity:0.9, duration:0.01}}, 14.2);
// 5 этап — дерево и кусты
tl.to(".stage5 .draw", {{attr:{{"stroke-dashoffset":0}}, duration:0.9, stagger:0.08, ease:"none"}}, 18.8);
tl.to(".stage5 .fillshape", {{opacity:0.35, duration:0.8, stagger:0.1}}, 20.2);
// 6 этап — акценты
tl.to(".stage6 .draw", {{attr:{{"stroke-dashoffset":0}}, duration:0.8, stagger:0.3}}, 25.4);
tl.to(".sig", {{opacity:1, duration:0.8}}, 26.8);
tl.to(".ttl", {{opacity:1, y:0, duration:0.7}}, 27.0);
tl.to(".ttl2", {{opacity:1, duration:0.7}}, 27.4);
tl.to(".world", {{scale:1.0, duration:0.1}}, 0);
window.__timelines["main"] = tl;
</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    build()
