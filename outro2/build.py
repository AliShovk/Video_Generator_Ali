#!/usr/bin/env python3
"""Концовка: ссылка в шапке профиля / «ГАЙД» в комментариях."""
import json
from pathlib import Path

ROOT = Path("/root/video-gen/outro2")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)
T = json.load(open(ROOT / "timings.json"))
DUR = T["total"]

BG = "#0a0c0e"
WHITE = "#f4f6f7"
GREY = "#8b969b"
YEL = "#ffd23f"
RED = "#d94a2b"

body = f'''
<rect width="1080" height="1920" fill="{BG}"/>
<defs>
  <radialGradient id="gl" cx="50%" cy="42%" r="62%">
    <stop offset="0" stop-color="#3a2a12" stop-opacity="0.75"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.95"/>
  </radialGradient>
</defs>
<rect width="1080" height="1920" fill="url(#gl)"/>

<g class="brand">
  <circle cx="540" cy="250" r="46" fill="{RED}"/>
  <text x="540" y="264" font-family="Nunito" font-size="34" font-weight="900" fill="{WHITE}" text-anchor="middle">ГВ</text>
  <text x="540" y="345" font-family="Nunito" font-size="24" font-weight="800" fill="{GREY}" text-anchor="middle" letter-spacing="6">ГАЙКАВИНТ</text>
</g>

<g class="arrow">
  <path d="M 540 470 l 0 -86" stroke="{YEL}" stroke-width="8" stroke-linecap="round"/>
  <path d="M 540 384 l -24 30 l 48 0 z" fill="{YEL}"/>
</g>

<text x="540" y="580" font-family="Nunito" font-size="44" font-weight="900" fill="{WHITE}" text-anchor="middle" letter-spacing="1">ССЫЛКА В ШАПКЕ</text>
<text x="540" y="640" font-family="Nunito" font-size="44" font-weight="900" fill="{WHITE}" text-anchor="middle" letter-spacing="1">ПРОФИЛЯ</text>

<g class="chip">
  <rect x="180" y="710" width="720" height="96" rx="48" fill="#141a1d" stroke="{YEL}" stroke-width="3"/>
  <text x="540" y="772" font-family="Nunito" font-size="34" font-weight="800" fill="{YEL}" text-anchor="middle">qantcore.space/gptunnel</text>
</g>

<text x="540" y="980" font-family="Nunito" font-size="30" font-weight="800" fill="{GREY}" text-anchor="middle" letter-spacing="4">ИЛИ НАПИШИ</text>

<g class="pill">
  <rect x="290" y="1040" width="500" height="150" rx="75" fill="{YEL}"/>
  <text x="540" y="1145" font-family="Nunito" font-size="76" font-weight="900" fill="#141a1d" text-anchor="middle" letter-spacing="6">ГАЙД</text>
</g>

<text x="540" y="1290" font-family="Nunito" font-size="34" font-weight="800" fill="{WHITE}" text-anchor="middle" letter-spacing="2">В КОММЕНТАРИЯХ</text>

<g class="foot">
  <path d="M 300 1500 l 480 0" stroke="#2a3338" stroke-width="2"/>
  <text x="540" y="1570" font-family="Nunito" font-size="26" font-weight="700" fill="{GREY}" text-anchor="middle">новые разборы каждую неделю</text>
  <text x="540" y="1700" font-family="Nunito" font-size="22" font-weight="700" fill="#3f4a4f" text-anchor="middle">gaikavint</text>
</g>
'''

page = f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{BG}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="s1" data-width="1080" data-height="1920">
    <div class="clip" id="s1-clip" data-start="0" data-duration="{DUR}">
      <div id="s1-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{body}</svg></div>
    </div>
  </div>
  <script>
    const tl_s1 = gsap.timeline({{ paused: true }});
    const tl = tl_s1;
    tl.fromTo(".brand", {{opacity:0, y:-14}}, {{opacity:1, y:0, duration:0.5}}, 0.05);
    tl.fromTo(".arrow", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.45}}, 0.35);
    tl.to(".arrow", {{y:-10, duration:0.6, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 0.9);
    tl.fromTo(".chip", {{opacity:0, scale:0.94}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(1.4)"}}, 0.6);
    tl.fromTo(".pill", {{opacity:0, scale:0.75}}, {{opacity:1, scale:1, duration:0.55, ease:"back.out(2)"}}, 1.5);
    tl.to(".pill", {{scale:1.04, duration:0.7, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 2.1);
    tl.fromTo(".foot", {{opacity:0}}, {{opacity:1, duration:0.5}}, 2.4);
    window.__timelines["s1"] = tl_s1;
  </script>
</template>
"""

html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="s1" class="scene" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0"
 data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""

(OUT / "s1.html").write_text(page, encoding="utf-8")
(ROOT / "index.html").write_text(html, encoding="utf-8")
print("ok", DUR)
