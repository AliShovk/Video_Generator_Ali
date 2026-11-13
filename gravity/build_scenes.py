#!/usr/bin/env python3
"""Сборка «Гравитация исчезла на 10 секунд»."""
from pathlib import Path

from scenes import SCENES

OUT = Path("/root/video-gen/gravity/compositions")
OUT.mkdir(parents=True, exist_ok=True)

PILL = {
    "s1": "10 секунд",
    "s2": "всё вверх",
    "s3": "вода и машины",
    "s4": "инерция",
    "s5": "падение",
    "s6": "катастрофа",
}

FOOT = {
    "s1": ("Что будет, если гравитация исчезнет?", 0.5),
    "s2": ("Чашка отрывается от стола", 0.6),
    "s3": ("Люди, машины и вода — в воздух", 0.7),
    "s4": ("Но инерция никуда не денется", 0.7),
    "s5": ("Гравитация вернулась — всё падает", 0.6),
    "s6": ("Десять секунд — и это катастрофа", 0.8),
}

EXTRA = {
    "s1": """
    tl_s1.to("#s1 .world", {y:-6, duration:2, ease:"sine.inOut"}, 0.4);
    tl_s1.to("#s1 .world > g:last-of-type", {y:-8, duration:0.9, yoyo:true, repeat:1, ease:"sine.inOut"}, 2.2);
    """,
    "s2": """
    tl_s2.fromTo("#cup-float", {y:200, rotate:-2}, {y:0, rotate:-12, duration:2.6, ease:"power1.out"}, 0.2);
    tl_s2.fromTo("#chair-float", {y:280, rotate:2}, {y:0, rotate:14, duration:3.0, ease:"power1.out"}, 0.4);
    tl_s2.fromTo("#person-float", {y:320}, {y:0, duration:3.2, ease:"power1.out"}, 0.3);
    tl_s2.to("#cup-float", {y:-14, duration:1.2, yoyo:true, repeat:3, ease:"sine.inOut"}, 2.8);
    tl_s2.to("#person-float", {y:-18, duration:1.4, yoyo:true, repeat:3, ease:"sine.inOut"}, 3.0);
    """,
    "s3": """
    tl_s3.fromTo("#car-float", {y:250, rotate:0}, {y:0, rotate:-8, duration:3.4, ease:"power1.out"}, 0.3);
    tl_s3.fromTo("#people-float", {y:300}, {y:0, duration:3.6, ease:"power1.out"}, 0.5);
    tl_s3.to("#car-float", {y:-20, duration:1.6, yoyo:true, repeat:4, ease:"sine.inOut"}, 3.8);
    """,
    "s4": """
    tl_s4.fromTo("#earth", {rotate:0, transformOrigin:"50% 50%"}, {rotate:8, duration:14, ease:"none"}, 0);
    tl_s4.to("#s4 .world > circle", {y:-8, duration:2, stagger:0.15, yoyo:true, repeat:5, ease:"sine.inOut"}, 1.0);
    """,
    "s5": """
    tl_s5.fromTo("#fall-cup", {y:-40}, {y:710, duration:5.2, ease:"power2.in"}, 0.4);
    tl_s5.fromTo("#fall-chair", {y:-60}, {y:780, duration:5.6, ease:"power2.in"}, 0.6);
    tl_s5.fromTo("#fall-person", {y:-80}, {y:730, duration:6.0, ease:"power2.in"}, 0.8);
    tl_s5.to("#s5 .world", {x:0, duration:0.05, repeat:7, yoyo:true, ease:"none"}, 6.6);
    """,
    "s6": """
    tl_s6.fromTo("#s6 .world", {opacity:0.6}, {opacity:1, duration:0.6}, 0.1);
    tl_s6.to("#s6 .world", {rotate:0.4, transformOrigin:"50% 50%", duration:2, yoyo:true, repeat:2, ease:"sine.inOut"}, 0.3);
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
      font: 800 46px/1 "Nunito", Arial, sans-serif;
      padding: 22px 40px; white-space: nowrap; box-shadow: 0 8px 0 rgba(0,0,0,0.12);
    }}
    .foot {{
      position: absolute; left: 44px; right: 44px; bottom: 400px;
      font: 800 52px/1.12 "Nunito", Arial, sans-serif; color: #ffffff; text-align: center;
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
    tl_{comp_id}.fromTo("#{comp_id} .world", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {duration}, ease: "none" }}, 0);
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
