#!/usr/bin/env python3
"""Сборка «ночь в −40 у костра»."""
from pathlib import Path

from scenes import SCENES

OUT = Path("/root/video-gen/fire-survival/compositions")
OUT.mkdir(parents=True, exist_ok=True)

PILL = {"s1": "−40°", "s2": "2 бревна", "s3": "тепло уходит", "s4": "экран", "s5": "земля-печь", "s6": "утро"}

FOOT = {
    "s1": ("Засыпаешь у костра. Через час — пальцы не гнутся", 0.6),
    "s2": ("Два бревна: огонь тлеет по щели до утра", 0.6),
    "s3": ("Лицо горит, а спина леденеет", 0.6),
    "s4": ("Баннер за спиной возвращает тепло", 0.6),
    "s5": ("Ложишься туда, где горел костёр", 0.6),
    "s6": ("Земля греет снизу, как печь", 0.6),
}

EXTRA = {
    "s1": 'tl_s1.to("#s1 .world", {y:-10, duration:3.6, yoyo:true, repeat:1, ease:"sine.inOut"}, 0.4);',
    "s2": 'tl_s2.fromTo("#s2 .world", {opacity:0.7, y:20}, {opacity:1, y:0, duration:1.0}, 0.2);'
          'tl_s2.to("#s2 .world", {y:-10, duration:2.4, yoyo:true, repeat:2, ease:"sine.inOut"}, 1.0);',
    "s3": 'tl_s3.to("#s3 .world", {y:-8, duration:2.6, yoyo:true, repeat:2, ease:"sine.inOut"}, 0.2);',
    "s4": 'tl_s4.fromTo("#s4 .world", {opacity:0.75, y:16}, {opacity:1, y:0, duration:1.0}, 0.2);'
          'tl_s4.to("#s4 .world", {y:-8, duration:2.4, yoyo:true, repeat:2, ease:"sine.inOut"}, 1.2);',
    "s5": 'tl_s5.fromTo("#s5 .world", {opacity:0.6}, {opacity:1, duration:1.0}, 0.15);'
          'tl_s5.to("#s5 .world", {y:-6, duration:2.6, yoyo:true, repeat:2, ease:"sine.inOut"}, 0.8);',
    "s6": 'tl_s6.fromTo("#s6 .world", {opacity:0.6, y:18}, {opacity:1, y:0, duration:1.2}, 0.1);',
}


def page(comp_id, body, duration):
    foot, foot_at = FOOT[comp_id]
    return f"""<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; background:#141b33; }}
    .world {{ position:absolute; inset:0; width:100%; height:100%; }}
    .pill {{
      position:absolute; left:50%; top:110px; transform:translateX(-50%);
      background:#ffffff; color:#ff5a2b; border-radius:999px;
      font:900 44px/1 "Nunito", Arial, sans-serif; padding:20px 42px; white-space:nowrap;
      box-shadow:0 12px 26px rgba(0,0,0,0.25);
    }}
    .scrim {{ position:absolute; left:0; right:0; bottom:0; height:520px;
      background:linear-gradient(to top, rgba(10,15,30,0.85) 30%, rgba(10,15,30,0) 100%); }}
    .foot {{ position:absolute; left:56px; right:56px; bottom:330px;
      font:900 50px/1.12 "Nunito", Arial, sans-serif; color:#ffffff; text-align:center; }}
    .foot::before {{ content:""; display:block; width:90px; height:9px; border-radius:6px; background:#ff8a3d; margin:0 auto 20px; }}
  </style>
  <div id="root" data-composition-id="{comp_id}" data-width="1080" data-height="1920">
    <div class="clip" id="{comp_id}-clip" data-start="0" data-duration="{duration}">
      <div id="{comp_id}-in">
        {body}
        <div class="scrim"></div>
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
