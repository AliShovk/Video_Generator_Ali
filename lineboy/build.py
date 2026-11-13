#!/usr/bin/env python3
"""Минималистичная линейная анимация: мастер, кирпичная стена и розовый мяч."""
from pathlib import Path

ROOT = Path("/root/video-gen/lineboy")
ROOT.mkdir(parents=True, exist_ok=True)
DUR = 11.0

INK = "#141414"
ACC = "#ec3f7f"
BG = "#ffffff"
GROUND = 1500
LW = 15


def L(d, w=LW, col=INK, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def build():
    b = [f'<rect width="1080" height="1920" fill="{BG}"/>']

    # земля
    b.append(f'<line x1="70" y1="{GROUND}" x2="1010" y2="{GROUND}" stroke="{ACC}" stroke-width="18" stroke-linecap="round"/>')

    # стена: 6 рядов по 3 кирпича
    y = GROUND - 70
    row = 0
    while y > 1080:
        for c in range(3):
            x = 150 + c * 120 + (60 if row % 2 else 0)
            if x + 112 > 520:
                continue
            b.append(L(f"M {x} {y} l 112 0 M {x} {y} l 0 64 M {x+112} {y} l 0 64", 11))
            b.append(L(f"M {x} {y+64} l 112 0", 11))
        y -= 68
        row += 1

    # мастер: обёртка без transform (её двигает GSAP), внутри — статичный сдвиг
    b.append(f'''<g class="manWrap">
      <g transform="translate(860 {GROUND})">
        <circle class="head" cx="0" cy="-300" r="34" fill="{BG}" stroke="{INK}" stroke-width="{LW}"/>
        <path class="torso" d="M 0 -264 L 0 -160" stroke="{INK}" stroke-width="{LW}" fill="none" stroke-linecap="round"/>
        <path class="armL" d="M 0 -240 L -44 -186" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>
        <path class="armR" d="M 0 -240 L 42 -190" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>
        <path class="legL" d="M 0 -160 L -32 0" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>
        <path class="legR" d="M 0 -160 L 32 0" stroke="{INK}" stroke-width="{LW}" stroke-linecap="round"/>
      </g>
    </g>''')

    # мяч: обёртка, внутри круг в нуле
    b.append(f'<g class="ballWrap"><circle class="ball" cx="0" cy="0" r="34" fill="{ACC}"/></g>')
    b.append(f'<rect class="pinkBrick" x="390" y="1026" width="112" height="64" fill="{ACC}" opacity="0"/>')
    b.append('<g class="ping" opacity="0"><circle cx="0" cy="0" r="14" fill="none" stroke="#ec3f7f" stroke-width="9"/></g>')

    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{BG}}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}svg{{position:absolute;inset:0;width:100%;height:100%}}
</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<svg viewBox="120 334 800 1422" xmlns="http://www.w3.org/2000/svg">{''.join(b)}</svg>
</div>
<script>
const tl = gsap.timeline({{paused:true}});
window.__timelines = {{}};

gsap.set(".ballWrap", {{x:600, y:1100}});
gsap.set(".ping", {{x:446, y:1096}});

// мяч падает на землю и скачет
tl.to(".ballWrap", {{y:1466, duration:0.42, ease:"power2.in"}}, 0.15);
tl.to(".ballWrap", {{y:1340, duration:0.34, ease:"power2.out"}}, 0.57);
tl.to(".ballWrap", {{y:1466, duration:0.32, ease:"power2.in"}}, 0.91);
tl.to(".ballWrap", {{y:1396, duration:0.24, ease:"power2.out"}}, 1.23);
tl.to(".ballWrap", {{y:1466, duration:0.22, ease:"power2.in"}}, 1.47);
tl.to(".ballWrap", {{y:1428, duration:0.17, ease:"power2.out"}}, 1.69);
tl.to(".ballWrap", {{y:1466, duration:0.15, ease:"power2.in"}}, 1.86);
tl.to(".ballWrap", {{x:560, duration:0.6, ease:"power1.out"}}, 2.0);

// человек идёт к мячу: 860 -> 640
tl.to(".manWrap", {{x:-220, duration:2.5, ease:"none"}}, 1.6);
function gait(t0, reps) {{
  for (let i=0;i<reps;i++) {{
    const t = t0 + i*0.32;
    tl.to(".legL", {{rotation:24, svgOrigin:"0 -160", duration:0.16, ease:"sine.inOut"}}, t);
    tl.to(".legR", {{rotation:-24, svgOrigin:"0 -160", duration:0.16, ease:"sine.inOut"}}, t);
    tl.to(".armL", {{rotation:-20, svgOrigin:"0 -240", duration:0.16, ease:"sine.inOut"}}, t);
    tl.to(".armR", {{rotation:20, svgOrigin:"0 -240", duration:0.16, ease:"sine.inOut"}}, t);
    tl.to(".legL", {{rotation:0, svgOrigin:"0 -160", duration:0.16, ease:"sine.inOut"}}, t+0.16);
    tl.to(".legR", {{rotation:0, svgOrigin:"0 -160", duration:0.16, ease:"sine.inOut"}}, t+0.16);
    tl.to(".armL", {{rotation:0, svgOrigin:"0 -240", duration:0.16, ease:"sine.inOut"}}, t+0.16);
    tl.to(".armR", {{rotation:0, svgOrigin:"0 -240", duration:0.16, ease:"sine.inOut"}}, t+0.16);
  }}
}}
gait(1.6, 7);

// наклон, мяч прыгает в руку
tl.to(".manWrap", {{y:38, duration:0.34, ease:"power2.out"}}, 4.25);
tl.to(".armR", {{rotation:36, svgOrigin:"0 -240", duration:0.34}}, 4.25);
tl.to(".ballWrap", {{x:620, y:1330, duration:0.45, ease:"power2.inOut"}}, 4.35);
tl.to(".manWrap", {{y:0, duration:0.4, ease:"power2.out"}}, 4.9);
tl.to(".armR", {{rotation:-14, svgOrigin:"0 -240", duration:0.4}}, 4.9);

// несёт к стене: 640 -> 520
tl.to(".manWrap", {{x:-340, duration:2.0, ease:"none"}}, 5.2);
gait(5.2, 6);
tl.to(".ballWrap", {{x:580, y:1300, duration:2.0, ease:"none"}}, 5.2);

// поднимает и ставит кирпич на стену
tl.to(".manWrap", {{x:-270, duration:0.35}}, 7.3);
tl.to(".armR", {{rotation:-132, svgOrigin:"0 -240", duration:0.6, ease:"power2.out"}}, 7.35);
tl.to(".armL", {{rotation:96, svgOrigin:"0 -240", duration:0.6, ease:"power2.out"}}, 7.45);
tl.to(".ballWrap", {{x:446, y:1058, duration:0.65, ease:"power2.out"}}, 7.35);
tl.to(".armR", {{rotation:0, svgOrigin:"0 -240", duration:0.35}}, 8.0);
tl.to(".armL", {{rotation:0, svgOrigin:"0 -240", duration:0.35}}, 8.05);
tl.to(".ballWrap", {{scaleX:1.75, scaleY:0.72, duration:0.24, ease:"power2.out"}}, 8.02);
tl.to(".ballWrap", {{opacity:0, duration:0.12}}, 8.24);
tl.to(".pinkBrick", {{opacity:1, duration:0.12}}, 8.24);
tl.to(".ping", {{opacity:1, scale:2.4, duration:0.5, ease:"power2.out"}}, 8.15);
tl.to(".ping", {{opacity:0, duration:0.28}}, 8.65);

// шаг назад, любуется
tl.to(".manWrap", {{x:-330, duration:0.7, ease:"power2.out"}}, 8.6);
gait(8.6, 2);
tl.to(".head", {{y:-6, duration:0.35, yoyo:true, repeat:2}}, 9.5);

window.__timelines["main"] = tl;
</script>
</body></html>"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("ok", DUR)


if __name__ == "__main__":
    build()
