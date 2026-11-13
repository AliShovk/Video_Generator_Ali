#!/usr/bin/env python3
"""Сборка мультяшной версии: жёлтая плашка сверху, белая подпись снизу."""
from pathlib import Path

from scenes import SCENES

OUT = Path("/root/video-gen/chernobyl-cartoon/compositions")
OUT.mkdir(parents=True, exist_ok=True)

PILL = {
    "s1": "36 000 тонн",
    "s2": "108 м · 257 м",
    "s3": "300 м",
    "s4": "224 домкрата",
    "s5": "327 м",
    "s6": "100 лет",
    "s7": "2025",
}

FOOT = {
    "s1": ("Построили в стороне — и передвинули", 0.7),
    "s2": ("Высота 108 м, пролёт 257 м", 0.8),
    "s3": ("Сборка в 300 метрах от блока", 0.8),
    "s4": ("Гидравлика толкает по рельсам", 0.8),
    "s5": ("327 метров за две недели", 0.7),
    "s6": ("Арка накрыла четвёртый блок", 0.8),
    "s7": ("Февраль 2025 — арка повреждена", 0.9),
}

EXTRA = {
    "s1": """
    tl_s1.fromTo("#sky-layer", {x:-34}, {x:34, duration:5, ease:"none"}, 0);
    tl_s1.fromTo("#sun", {y:0}, {y:-14, duration:2.4, yoyo:true, repeat:1, ease:"sine.inOut"}, 0);
    tl_s1.fromTo("#arch-main", {y:56, opacity:0}, {y:0, opacity:1, duration:0.9, ease:"back.out(1.25)"}, 0.2);
    tl_s1.fromTo("#truck1", {x:-170}, {x:0, duration:1.2, ease:"power2.out"}, 0.1);
    tl_s1.to("#crowd", {y:-7, duration:0.7, yoyo:true, repeat:5, ease:"sine.inOut"}, 1.1);
    """,
    "s2": """
    tl_s2.fromTo("#dims", {opacity:0, x:-26}, {opacity:1, x:0, duration:0.7, ease:"power2.out"}, 0.35);
    tl_s2.to("#s2 .world", {y:-6, duration:3.5, yoyo:true, repeat:1, ease:"sine.inOut"}, 0.4);
    """,
    "s3": """
    tl_s3.fromTo("#route", {opacity:0}, {opacity:1, duration:0.5}, 0.3);
    tl_s3.to("#route path", {strokeDashoffset:-92, duration:1.6, repeat:5, ease:"none"}, 0.4);
    tl_s3.fromTo("#unit4", {opacity:0.3}, {opacity:1, duration:0.6, ease:"power2.out"}, 0.8);
    tl_s3.to("#unit4", {scale:1.05, transformOrigin:"50% 50%", duration:1.2, yoyo:true, repeat:3, ease:"sine.inOut"}, 1.0);
    """,
    "s4": """
    tl_s4.to(".piston", {y:-14, duration:0.44, yoyo:true, repeat:6, stagger:0.1, ease:"sine.inOut"}, 0.3);
    tl_s4.fromTo("#pipes", {opacity:0.4}, {opacity:1, duration:0.5, yoyo:true, repeat:5, ease:"sine.inOut"}, 0.5);
    tl_s4.to("#jacks", {y:-4, duration:0.9, yoyo:true, repeat:3, ease:"sine.inOut"}, 0.2);
    """,
    "s5": """
    tl_s5.fromTo("#arch-move", {x:0}, {x:400, duration:6.9, ease:"power1.inOut"}, 0.55);
    tl_s5.to("#s5 .world", {y:-10, duration:4, yoyo:true, repeat:1, ease:"sine.inOut"}, 0);
    """,
    "s6": """
    tl_s6.fromTo("#checks", {opacity:0, y:24}, {opacity:1, y:0, duration:0.5, ease:"back.out(1.6)"}, 0.7);
    tl_s6.to("#s6 .world", {y:-8, duration:3, yoyo:true, repeat:1, ease:"sine.inOut"}, 0);
    """,
    "s7": """
    tl_s7.to("#crack", {strokeDashoffset:0, duration:1.1, ease:"power2.out"}, 0.35);
    tl_s7.fromTo("#warn", {opacity:0}, {opacity:1, duration:0.45, ease:"power2.out"}, 1.3);
    tl_s7.to("#warn", {opacity:0.55, duration:0.5, yoyo:true, repeat:4, ease:"sine.inOut"}, 1.75);
    """,
}

def page(comp_id, body, duration):
    foot, foot_at = FOOT[comp_id]
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #bfe4f8; }}
    .world {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .pill {{
      position: absolute; left: 50%; top: 118px; transform: translateX(-50%);
      background: #f7c93f; color: #241f1a; border-radius: 999px;
      font: 800 46px/1 "Nunito", Arial, sans-serif; letter-spacing: 0.5px;
      padding: 22px 40px; white-space: nowrap;
      box-shadow: 0 8px 0 rgba(0,0,0,0.12);
    }}
    .foot {{
      position: absolute; left: 44px; right: 44px; bottom: 400px;
      font: 800 54px/1.1 "Nunito", Arial, sans-serif; color: #ffffff; text-align: center;
      -webkit-text-stroke: 10px rgba(20,26,30,0.85); paint-order: stroke fill;
      text-shadow: 0 4px 0 rgba(20,26,30,0.35);
    }}
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
    tl_{comp_id}.fromTo("#{comp_id} .world", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {duration}, ease: "none" }}, 0);
    tl_{comp_id}.fromTo("#{comp_id}-pill", {{ opacity: 0, y: -18 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)" }}, 0.05);
    tl_{comp_id}.fromTo("#{comp_id}-foot", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }}, {foot_at});
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
