#!/usr/bin/env python3
"""Сборка ретро-ролика про камин."""
from pathlib import Path

from scenes import SCENES

OUT = Path("/root/video-gen/fireplace/compositions")
OUT.mkdir(parents=True, exist_ok=True)

STAMP = {"s1": "схема · 1954", "s2": "шамот", "s3": "тяга", "s4": "труба", "s5": "правила"}

FOOT = {
    "s1": ("Камин: разрез и главные части", 0.4),
    "s2": ("Топка: шамот и наклонная стенка", 0.4),
    "s3": ("Дымосборник: зуб и задвижка", 0.4),
    "s4": ("Труба: выше конька на 0,5 м", 0.4),
    "s5": ("Разделка 38 см и приток воздуха", 0.4),
}

EXTRA = {
    "s1": """
    tl_s1.fromTo("#fp-body", {scaleY:0.05, y:60, transformOrigin:"50% 100%", svgOrigin:"540 1310"},
                 {scaleY:1, y:0, duration:1.5, ease:"power2.out"}, 0.1);
    tl_s1.fromTo("#fire", {opacity:0, scaleY:0.5, transformOrigin:"50% 100%", svgOrigin:"540 1240"},
                 {opacity:1, scaleY:1, duration:0.7, ease:"power2.out"}, 1.3);
    tl_s1.to("#fire", {scaleY:1.14, duration:0.32, yoyo:true, repeat:16, ease:"sine.inOut"}, 2.0);
    tl_s1.fromTo("#labels1 > *", {opacity:0, y:12}, {opacity:1, y:0, duration:0.45, stagger:0.4, ease:"power2.out"}, 1.7);
    tl_s1.fromTo(".puff", {y:60, opacity:0}, {y:-240, opacity:0.32, duration:2.8, stagger:0.55, repeat:2, ease:"sine.out"}, 1.6);
    """,
    "s2": """
    tl_s2.to("#s2 .world", {y:-8, duration:2.8, yoyo:true, repeat:1, ease:"sine.inOut"}, 0);
    tl_s2.fromTo("#flow", {strokeDashoffset:64}, {strokeDashoffset:0, duration:1.1, repeat:5, ease:"none"}, 0.35);
    tl_s2.fromTo("#labels2 > *", {opacity:0, y:10}, {opacity:1, y:0, duration:0.4, stagger:0.5, ease:"power2.out"}, 0.7);
    tl_s2.to("#s2 .world > g:first-of-type", {opacity:0.92, duration:1.6, yoyo:true, repeat:2, ease:"sine.inOut"}, 1.2);
    """,
    "s3": """
    tl_s3.fromTo("#damper", {rotate:-30, svgOrigin:"560 800"}, {rotate:0, duration:1.0, ease:"back.out(1.7)"}, 0.7);
    tl_s3.fromTo(".puff3", {y:40, opacity:0}, {y:-180, opacity:0.38, duration:2.2, stagger:0.5, repeat:2, ease:"sine.out"}, 1.2);
    tl_s3.fromTo("#labels3 > *", {opacity:0, y:8}, {opacity:1, y:0, duration:0.4, stagger:0.45}, 1.6);
    """,
    "s4": """
    tl_s4.fromTo("#flue", {scaleY:0.04, svgOrigin:"605 1020"}, {scaleY:1, duration:1.4, ease:"power2.out"}, 0.4);
    tl_s4.fromTo("#ridge", {strokeDashoffset:820}, {strokeDashoffset:0, duration:1.3, ease:"power1.out"}, 1.5);
    tl_s4.to("#s4 .world", {y:-9, duration:3.0, yoyo:true, repeat:1, ease:"sine.inOut"}, 0);
    """,
    "s5": """
    tl_s5.to("#air", {x:30, duration:0.75, yoyo:true, repeat:7, ease:"sine.inOut"}, 0.3);
    tl_s5.to("#s5 .world", {y:-7, duration:2.8, yoyo:true, repeat:1, ease:"sine.inOut"}, 0);
    tl_s5.fromTo("#s5 .world", {opacity:0.75}, {opacity:1, duration:0.7}, 0.05);
    """,
}

def page(comp_id, body, duration):
    foot, foot_at = FOOT[comp_id]
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #f2e4c8; }}
    .world {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .stamp {{
      position: absolute; left: 72px; top: 238px;
      border: 3px solid #c1442e; color: #c1442e; border-radius: 6px;
      font: 700 24px/1 "Oswald", Arial, sans-serif; letter-spacing: 4px; text-transform: uppercase;
      padding: 9px 14px; transform: rotate(-2deg); opacity: 0.9;
    }}
    .foot {{
      position: absolute; left: 72px; right: 72px; bottom: 300px;
      font: 700 46px/1.16 "Playfair Display", Georgia, serif; color: #3a2a1e; text-align: left;
    }}
    .foot::before {{ content: ""; display: block; width: 120px; height: 6px; background: #c1442e; margin-bottom: 20px; }}
  </style>
  <div id="root" data-composition-id="{comp_id}" data-width="1080" data-height="1920">
    <div class="clip" id="{comp_id}-clip" data-start="0" data-duration="{duration}">
      <div id="{comp_id}-in">
        {body}
        <div class="stamp" id="{comp_id}-stamp">{STAMP[comp_id]}</div>
        <div class="foot" id="{comp_id}-foot">{foot}</div>
      </div>
    </div>
  </div>
  <script>
    const tl_{comp_id} = gsap.timeline({{ paused: true }});
    tl_{comp_id}.fromTo("#{comp_id} .world", {{ scale: 1.0 }}, {{ scale: 1.04, duration: {duration}, ease: "none" }}, 0);
    tl_{comp_id}.fromTo("#{comp_id}-stamp", {{ opacity: 0, rotate: -8 }}, {{ opacity: 0.9, rotate: -2, duration: 0.5, ease: "back.out(1.6)" }}, 0.15);
    tl_{comp_id}.fromTo("#{comp_id}-foot", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, {foot_at});
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
