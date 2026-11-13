#!/usr/bin/env python3
"""Сборка флэт-ролика про гравитацию (30 с)."""
from pathlib import Path

from scenes import SCENES

OUT = Path("/root/video-gen/gravity-flat/compositions")
OUT.mkdir(parents=True, exist_ok=True)

PILL = {"s1": "10 секунд", "s2": "всё вверх", "s3": "мелочи", "s4": "улица", "s5": "падение"}

FOOT = {
    "s1": ("Что будет, если гравитация исчезнет?", 0.5),
    "s2": ("Всё, что не закреплено, поднимется", 0.5),
    "s3": ("Кофе, телефон, растения — в воздухе", 0.5),
    "s4": ("Машины отрываются от дороги", 0.5),
    "s5": ("А потом всё падает обратно", 0.5),
}

EXTRA = {
    "s1": 'tl_s1.to("#s1 .world", {y:-10, duration:2.4, yoyo:true, repeat:1, ease:"sine.inOut"}, 0.3);',
    "s2": 'tl_s2.fromTo("#s2 .world", {y:26, opacity:0.55}, {y:0, opacity:1, duration:1.6, ease:"power2.out"}, 0.15);'
          'tl_s2.to("#s2 .world", {y:-16, duration:1.7, yoyo:true, repeat:2, ease:"sine.inOut"}, 1.4);',
    "s3": 'tl_s3.fromTo("#s3 .world", {y:40, opacity:0.5, rotate:-1.2}, {y:0, opacity:1, rotate:0, duration:1.8, ease:"power2.out"}, 0.15);'
          'tl_s3.to("#s3 .world", {rotate:1.0, duration:4, yoyo:true, repeat:1, ease:"sine.inOut"}, 0.4);',
    "s4": 'tl_s4.fromTo("#s4 .world", {y:34}, {y:0, duration:1.8, ease:"power2.out"}, 0.15);'
          'tl_s4.to("#s4 .world", {y:-14, duration:1.8, yoyo:true, repeat:2, ease:"sine.inOut"}, 1.2);',
    "s5": 'tl_s5.fromTo("#s5 .world", {y:-40, opacity:0.6}, {y:0, opacity:1, duration:1.2, ease:"power2.out"}, 0.1);'
          'tl_s5.to("#s5 .world", {x:0, duration:0.05, repeat:8, yoyo:true, ease:"none"}, 1.5);',
}

def page(comp_id, body, duration):
    foot, foot_at = FOOT[comp_id]
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#ffffff; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
    .pill {{
      position:absolute; left:50%; top:110px; transform:translateX(-50%);
      background:#ffffff; color:#7a4dff; border:4px solid #e6dcff; border-radius:999px;
      font:900 44px/1 "Nunito", Arial, sans-serif; padding:20px 40px; white-space:nowrap;
      box-shadow:0 12px 26px rgba(122,77,255,0.16);
    }}
    .foot {{
      position:absolute; left:60px; right:60px; bottom:330px;
      font:900 54px/1.12 "Nunito", Arial, sans-serif; color:#2b2340;
    }}
    .foot::before {{ content:""; display:block; width:96px; height:10px; border-radius:6px; background:#7a4dff; margin-bottom:22px; }}
  </style>
  <div id="root" data-composition-id="{comp_id}" data-width="1080" data-height="1920">
    <div class="clip" id="{comp_id}-clip" data-start="0" data-duration="{duration}">
      <div id="{comp_id}-in">
        {body}
        <div class="pill" id="{comp_id}-pill">{PILL[comp_id]}</div>
        <div class="foot" id="{comp_id}-foot">{foot}</div>
      </div>
    </div>
  </div>
  <script>
    const tl_{comp_id} = gsap.timeline({{ paused: true }});
    tl_{comp_id}.fromTo("#{comp_id} .world", {{ scale:1.0 }}, {{ scale:1.05, duration:{duration}, ease:"none" }}, 0);
    tl_{comp_id}.fromTo("#{comp_id}-pill", {{ opacity:0, y:-16 }}, {{ opacity:1, y:0, duration:0.45, ease:"back.out(1.7)" }}, 0.05);
    tl_{comp_id}.fromTo("#{comp_id}-foot", {{ opacity:0, y:14 }}, {{ opacity:1, y:0, duration:0.45, ease:"power2.out" }}, {foot_at});
    {EXTRA.get(comp_id, "")}
    window.__timelines["{comp_id}"] = tl_{comp_id};
  </script>
</template>
"""


def main() -> None:
    for name, body, dur in SCENES:
        (OUT / f"{name}.html").write_text(page(name, body, dur), encoding="utf-8")
        print("ok", name, dur)


if __name__ == "__main__":
    main()
