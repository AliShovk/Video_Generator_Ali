#!/usr/bin/env python3
"""Демо: unDraw-иллюстрации в вертикальном ролике 9:16."""
from pathlib import Path

OUT = Path("/root/video-gen/vector-demo/compositions")
OUT.mkdir(parents=True, exist_ok=True)

SCENES = [
    ("s1", "into-the-night_nd84.svg", "−40°", "Ночь. Ты один у костра", 6, "#0f1730", "#dfe6ff"),
    ("s2", "campfire_42p5.svg", "два бревна", "Огонь тлеет по щели до утра", 6, "#f7f5f0", "#241f3a"),
    ("s3", "winter-walk_m5sd.svg", "экран", "Баннер за спиной возвращает тепло", 6, "#eef2fb", "#241f3a"),
    ("s4", "snow-globe_xrk9.svg", "утро", "Земля греет снизу, как печь", 6, "#f7f5f0", "#241f3a"),
]

TEMPLATE = """<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:{bg}; }}
    .world {{ position:absolute; inset:0; }}
    .kicker {{
      position:absolute; left:0; right:0; top:150px; text-align:center;
      font:800 34px/1 "Nunito", Arial, sans-serif; letter-spacing:.18em; text-transform:uppercase; color:{fg}; opacity:.6;
    }}
    .art {{ position:absolute; left:50%; top:42%; transform:translate(-50%,-50%); width:1040px; }}
    .art img {{ width:100%; height:auto; display:block; }}
    .head {{
      position:absolute; left:70px; right:70px; bottom:330px; text-align:center;
      font:900 62px/1.1 "Nunito", Arial, sans-serif; color:{fg};
    }}
    .head .big {{ display:block; font-size:104px; line-height:.95; margin-bottom:18px; color:{accent}; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in">
        <div class="kicker" id="{sid}-kicker">{kicker}</div>
        <div class="art" id="{sid}-art"><img src="assets/{img}" alt=""/></div>
        <div class="head" id="{sid}-head"><span class="big">{big}</span>{cap}</div>
      </div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    tl_{sid}.fromTo("#{sid}-art", {{opacity:0, y:60, scale:0.94}}, {{opacity:1, y:0, scale:1, duration:1.2, ease:"power3.out"}}, 0.1);
    tl_{sid}.to("#{sid}-art", {{y:-14, duration:{dur}, ease:"none"}}, 0.1);
    tl_{sid}.fromTo("#{sid}-kicker", {{opacity:0, y:-12}}, {{opacity:0.6, y:0, duration:0.5}}, 0.3);
    tl_{sid}.fromTo("#{sid}-head", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, 0.45);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def main() -> None:
    hosts = []
    start = 0
    for i, (sid, img, big, cap, dur, bg, fg) in enumerate(SCENES):
        accent = "#7a4dff" if fg == "#241f3a" else "#ffb066"
        (OUT / f"{sid}.html").write_text(
            TEMPLATE.format(sid=sid, img=img, big=big, cap=cap, dur=dur,
                            bg=bg, fg=fg, accent=accent, kicker="как выжить в −40"),
            encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" '
                     f'data-composition-src="compositions/{sid}.html" data-start="{start}" '
                     f'data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')
        start += dur
    html = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{start}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    (Path("/root/video-gen/vector-demo") / "index.html").write_text(html, encoding="utf-8")
    print("ok", start)


if __name__ == "__main__":
    main()
