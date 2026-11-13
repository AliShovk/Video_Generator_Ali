#!/usr/bin/env python3
"""Анимация: дом-башня едет, быки идут, пыль, флажки."""
from pathlib import Path
import re

ROOT = Path("/root/video-gen/towerhouse")
svg = (ROOT / "tower.svg").read_text(encoding="utf-8")

# вырезаем внутренности svg
inner = svg.split(">", 1)[1].rsplit("</svg>", 1)[0]
# убираем непрозрачный фон рисунка, чтобы был виден горизонт
inner = re.sub(r'^\s*<rect[^>]*fill="#fdfaf3"[^>]*/>', "", inner, count=1)

DUR = 14.0

html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#fdfaf3}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.sky{{position:absolute;inset:0;background:linear-gradient(#e8f3f7 0%, #f7f2e6 42%, #eef3dc 74%, #e4ecd0 100%)}}
.stage{{position:absolute;left:-35px;top:190px;width:1150px}}
.stage svg{{width:1150px;height:auto;display:block;overflow:visible}}
.dust{{position:absolute;left:0;top:0}}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div class="sky"></div>
<div class="stage">
<svg viewBox="0 0 830 1000" xmlns="http://www.w3.org/2000/svg">
  <g class="far">
    <path d="M -40 880 q 120 -60 240 -10 q 120 50 240 0 q 120 -50 240 0 q 120 50 240 -10 L 920 1000 L -40 1000 Z"
          fill="#e7edd4" stroke="none"/>
  </g>
  <g class="near">
    <path d="M -40 940 q 130 -34 260 0 q 130 34 260 0 q 130 -34 260 0 q 130 34 260 0 L 920 1010 L -40 1010 Z"
          fill="#dfe8c6" stroke="none"/>
  </g>
  {inner}
  <g class="dustG"></g>
</svg>
</div>
</div>
<script>
const tl = gsap.timeline({{paused:true, repeat:-1}});
window.__timelines = {{}};

// фон едет навстречу
gsap.set(".far", {{x:0}});
gsap.set(".near", {{x:0}});

// корпус покачивается
tl.to(".cart", {{y:-6, rotation:0.5, svgOrigin:"420 860", duration:0.55, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 0);

// колёса крутятся
const wheels = [["58","842",30],["196","842",30],["292","850",26],["430","850",26]];
document.querySelectorAll(".whl").forEach((el,i) => {{
  const [cx, cy] = [el.dataset.cx, el.dataset.cy];
  tl.to(el, {{rotation:360, svgOrigin:`${{cx}} ${{cy}}`, duration:2.4, repeat:-1, ease:"none"}}, 0);
}});

// быки шагают в такт
document.querySelectorAll(".ox").forEach((el,i) => {{
  tl.to(el, {{y:6, duration:0.42, yoyo:true, repeat:-1, ease:"sine.inOut"}}, i*0.14);
  tl.to(el, {{rotation:i%2 ? 0.8 : -0.8, svgOrigin:"0 40", duration:0.42, yoyo:true, repeat:-1, ease:"sine.inOut"}}, i*0.14);
}});

// флажки трепещут
tl.to(".flags", {{skewX:4, duration:0.9, yoyo:true, repeat:-1, ease:"sine.inOut", svgOrigin:"244 470"}}, 0);

// флюгер гуляет
tl.to(".vane", {{rotation:12, svgOrigin:"360 190", duration:3.2, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 0);

// пыль из-под колёс
const dust = document.querySelector(".dustG");
const NS = "http://www.w3.org/2000/svg";
for (let i=0;i<10;i++) {{
  const c = document.createElementNS(NS, "circle");
  c.setAttribute("cx", 260 + Math.random()*180);
  c.setAttribute("cy", 880 + Math.random()*20);
  c.setAttribute("r", 10 + Math.random()*14);
  c.setAttribute("fill", "#cbb894");
  c.setAttribute("opacity", "0");
  dust.appendChild(c);
  tl.fromTo(c, {{opacity:0.55, scale:0.5, x:0, y:0}},
    {{opacity:0, scale:1.9, x:-70-Math.random()*60, y:-24-Math.random()*30,
      duration:1.6+Math.random()*0.8, repeat:-1, ease:"power1.out", svgOrigin:"50% 50%"}}, i*0.25);
}}

// горизонт ползёт
tl.fromTo(".near", {{x:0}}, {{x:-260, duration:7, repeat:-1, ease:"none"}}, 0);
tl.fromTo(".far", {{x:0}}, {{x:-120, duration:9, repeat:-1, ease:"none"}}, 0);

// лёгкий наезд камеры
tl.fromTo(".stage", {{scale:1.0}}, {{scale:1.04, duration:{DUR}, ease:"none"}}, 0);

window.__timelines["main"] = tl;
</script>
</body></html>"""

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("ok", DUR)
