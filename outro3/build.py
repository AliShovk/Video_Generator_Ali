#!/usr/bin/env python3
"""Концовка: макет шапки профиля Hoztovariy + CTA «ГАЙД»."""
import json
import shutil
from pathlib import Path

ROOT = Path("/root/video-gen/outro3")
OUT = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)
ROOT.mkdir(parents=True, exist_ok=True)

T = json.load(open("/root/video-gen/outro3/timings.json"))
DUR = T["total"]

BG = "#0a0c0e"
CARD = "#12161a"
WHITE = "#eef1f2"
GREY = "#8b969b"
DIM = "#5a656b"
YEL = "#ffd23f"
BLUE = "#5aa9e6"
RED = "#d94a2b"

body = f'''
<rect width="1080" height="1920" fill="{BG}"/>
<defs>
  <radialGradient id="gl" cx="50%" cy="30%" r="60%">
    <stop offset="0" stop-color="#2a2417" stop-opacity="0.8"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.95"/>
  </radialGradient>
  <linearGradient id="ava" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffe066"/><stop offset="1" stop-color="#f0a72c"/>
  </linearGradient>
</defs>
<rect width="1080" height="1920" fill="url(#gl)"/>

<!-- макет шапки профиля -->
<g class="profcard">
  <rect x="60" y="170" width="960" height="640" rx="26" fill="{CARD}" stroke="#232b30" stroke-width="2"/>

  <!-- аватар -->
  <circle cx="190" cy="300" r="86" fill="url(#ava)"/>
  <circle cx="163" cy="278" r="9" fill="#2a2015"/><circle cx="217" cy="278" r="9" fill="#2a2015"/>
  <path d="M 160 322 q 30 26 60 0" stroke="#2a2015" stroke-width="8" fill="none" stroke-linecap="round"/>
  <circle cx="252" cy="362" r="26" fill="{CARD}" stroke="#2b343a" stroke-width="2"/>
  <path d="M 252 352 l 0 20 M 242 362 l 20 0" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>

  <!-- имя -->
  <text x="310" y="268" font-family="Nunito" font-size="46" font-weight="900" fill="{WHITE}">Gaid</text>

  <!-- статистика -->
  <text x="312" y="330" font-family="Nunito" font-size="34" font-weight="900" fill="{WHITE}">20</text>
  <text x="312" y="362" font-family="Nunito" font-size="20" font-weight="700" fill="{GREY}">публикации</text>
  <text x="500" y="330" font-family="Nunito" font-size="34" font-weight="900" fill="{WHITE}">122</text>
  <text x="500" y="362" font-family="Nunito" font-size="20" font-weight="700" fill="{GREY}">подписчики</text>
  <text x="740" y="330" font-family="Nunito" font-size="34" font-weight="900" fill="{WHITE}">189</text>
  <text x="740" y="362" font-family="Nunito" font-size="20" font-weight="700" fill="{GREY}">подписки</text>

  <!-- описание и ссылка -->
  <text x="100" y="452" font-family="Nunito" font-size="24" font-weight="700" fill="{GREY}">Товар/услуга · Профиль, сгенерированный ИИ</text>
  <g class="linkrow">
    <path d="M 104 512 l 26 0 M 130 512 l -6 -10 M 130 522 l -6 10" stroke="{BLUE}" stroke-width="5" stroke-linecap="round" fill="none"/>
    <circle cx="104" cy="502" r="7" fill="none" stroke="{BLUE}" stroke-width="4"/>
    <circle cx="104" cy="522" r="7" fill="none" stroke="{BLUE}" stroke-width="4"/>
    <text x="156" y="524" font-family="Nunito" font-size="36" font-weight="800" fill="{BLUE}">qantcore.space/gptunnel</text>
  </g>

  <!-- тег -->
  <rect x="96" y="560" width="190" height="52" rx="26" fill="#1b2227" stroke="#2b343a" stroke-width="2"/>
  <text x="191" y="594" font-family="Nunito" font-size="22" font-weight="800" fill="#c9d1d5" text-anchor="middle">gaikavint</text>
  <rect x="300" y="560" width="220" height="52" rx="26" fill="#1b2227" stroke="#2b343a" stroke-width="2"/>
  <text x="410" y="594" font-family="Nunito" font-size="22" font-weight="800" fill="#c9d1d5" text-anchor="middle">+ Добавить</text>
</g>

<!-- рука указывает на ссылку -->
<g class="hand">
  <rect x="836" y="404" width="150" height="132" rx="42" fill="#f5b52a" stroke="#c98a16" stroke-width="4"/>
  <rect x="716" y="432" width="140" height="52" rx="26" fill="#f5b52a" stroke="#c98a16" stroke-width="4"/>
  <rect x="846" y="520" width="58" height="46" rx="22" fill="#f5b52a" stroke="#c98a16" stroke-width="4"/>
  <path d="M 760 470 l 60 0" stroke="#d99a1c" stroke-width="5" opacity="0.6"/>
  <rect x="964" y="404" width="42" height="132" rx="14" fill="#2b6fd6" opacity="0.9"/>
</g>

<!-- CTA -->
<g class="cta">
  <text x="540" y="1110" font-family="Nunito" font-size="40" font-weight="900" fill="{WHITE}" text-anchor="middle" letter-spacing="2">ССЫЛКА В ШАПКЕ</text>
  <text x="540" y="1166" font-family="Nunito" font-size="40" font-weight="900" fill="{WHITE}" text-anchor="middle" letter-spacing="2">ПРОФИЛЯ</text>
</g>

<text x="540" y="1280" font-family="Nunito" font-size="28" font-weight="800" fill="{GREY}" text-anchor="middle" letter-spacing="4">ИЛИ НАПИШИ</text>

<g class="pill">
  <rect x="300" y="1330" width="480" height="140" rx="70" fill="{YEL}"/>
  <text x="540" y="1426" font-family="Nunito" font-size="72" font-weight="900" fill="#161a1d" text-anchor="middle" letter-spacing="6">ГАЙД</text>
</g>

<text x="540" y="1550" font-family="Nunito" font-size="32" font-weight="800" fill="{WHITE}" text-anchor="middle" letter-spacing="2">В КОММЕНТАРИЯХ</text>

<text x="540" y="1700" font-family="Nunito" font-size="24" font-weight="800" fill="{GREY}" text-anchor="middle">ГАЙКАВИНТ · строительные разборы</text>
<text x="540" y="1752" font-family="Nunito" font-size="22" font-weight="700" fill="{DIM}" text-anchor="middle">новые видео каждую неделю</text>
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
    tl.fromTo(".profcard", {{opacity:0, y:-16}}, {{opacity:1, y:0, duration:0.6}}, 0.05);
    tl.fromTo(".linkrow", {{opacity:0, x:-12}}, {{opacity:1, x:0, duration:0.4}}, 0.5);
    tl.fromTo(".hand", {{opacity:0, x:40}}, {{opacity:1, x:0, duration:0.5}}, 0.8);
    tl.to(".hand", {{x:-10, duration:0.7, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 1.3);
    tl.fromTo(".cta", {{opacity:0, y:12}}, {{opacity:1, y:0, duration:0.5}}, 1.2);
    tl.fromTo(".pill", {{opacity:0, scale:0.75}}, {{opacity:1, scale:1, duration:0.5, ease:"back.out(2)"}}, 2.0);
    tl.to(".pill", {{scale:1.04, duration:0.7, yoyo:true, repeat:-1, ease:"sine.inOut"}}, 2.6);
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
