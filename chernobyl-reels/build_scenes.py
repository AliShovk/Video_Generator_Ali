#!/usr/bin/env python3
"""Сборка сцен «Чернобыльская арка»."""
from pathlib import Path

from make_scenes import SCENES

OUT = Path("/root/video-gen/chernobyl-reels/compositions")
OUT.mkdir(parents=True, exist_ok=True)

CHIP = {
    "s1": "Чернобыль · 2016",
    "s2": "Размеры",
    "s3": "План",
    "s4": "Домкраты",
    "s5": "Перемещение",
    "s6": "Результат",
    "s7": "Февраль 2025",
}

HEAD = {
    "s1": ("36 000<br>ТОНН", 0.2),
    "s5": ("327 М", 0.3),
}

FOOT = {
    "s1": ("Построили в стороне — и передвинули", 1.1),
    "s2": ("Арка перекрывает четвёртый энергоблок", 1.2),
    "s3": ("Сборка в 300 метрах от реактора", 1.0),
    "s4": ("Гидравлика толкает по рельсам", 1.0),
    "s5": ("Ноябрь 2016 · две недели", 0.8),
    "s6": ("Конфайнмент рассчитан на 100 лет", 1.0),
    "s7": ("История стройки ≠ объект в строю", 1.4),
}

EXTRA = {
    "s5": 'tl_s5.fromTo("#arch-move", { x: 0 }, { x: 390, duration: 6.9, ease: "power1.inOut" }, 0.7);',
    "s2": 'tl_s2.fromTo("#s2 .world > line", { opacity: 0 }, { opacity: 1, duration: 0.6, stagger: 0.12 }, 0.6);',
    "s4": 'tl_s4.fromTo("#s4 .world rect[stroke=\'#6fd3f2\']", { opacity: 0.2 }, { opacity: 1, duration: 0.5, stagger: 0.12, repeat: 3, yoyo: true }, 1.0);',
}


def page(comp_id, body, duration):
    chip = CHIP[comp_id]
    head_html, head_at = HEAD.get(comp_id, ("", 0))
    foot, foot_at = FOOT[comp_id]
    head_block = f'<div class="head" id="{comp_id}-head">{head_html}</div>' if head_html else ""
    head_anim = (
        f'tl_{comp_id}.fromTo("#{comp_id}-head", {{opacity:0, y:24}}, {{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, {head_at});'
        if head_html else ""
    )
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; background: #05080c; }}
    .world {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .top {{ position: absolute; left: 48px; top: 120px; }}
    .chip {{
      display: inline-block; border: 1px solid rgba(111,211,242,0.45); color: #8fd8ef;
      font: 500 28px/1 "JetBrains Mono", monospace; letter-spacing: 0.2em; text-transform: uppercase;
      padding: 12px 18px; background: rgba(6,12,18,0.6);
    }}
    .head {{
      position: absolute; left: 48px; top: 230px;
      font: 700 118px/0.92 "Oswald", sans-serif; text-transform: uppercase; color: #f1ece2;
    }}
    .foot {{
      position: absolute; left: 48px; right: 48px; bottom: 430px;
      font: 700 50px/1.1 "Oswald", sans-serif; text-transform: uppercase; color: #f6f1e7;
      text-shadow: 0 3px 14px rgba(0,0,0,0.9);
    }}
    .foot::before {{ content: ""; display: block; width: 74px; height: 4px; background: #ff7a1a; margin-bottom: 16px; }}
    .scrim {{
      position: absolute; left: 0; right: 0; bottom: 0; height: 640px;
      background: linear-gradient(to top, rgba(4,7,10,0.96) 34%, rgba(4,7,10,0.75) 62%, rgba(4,7,10,0) 100%);
    }}
  </style>
  <div id="root" data-composition-id="{comp_id}" data-width="1080" data-height="1920">
    <div class="clip" id="{comp_id}-clip" data-start="0" data-duration="{duration}">
      <div id="{comp_id}-in">
        {body}
        <div class="scrim"></div>
        <div class="top"><div class="chip" id="{comp_id}-chip">{chip}</div></div>
        {head_block}
        <div class="foot" id="{comp_id}-foot">{foot}</div>
      </div>
    </div>
  </div>
  <script>
    const tl_{comp_id} = gsap.timeline({{ paused: true }});
    tl_{comp_id}.fromTo("#{comp_id} .world", {{ scale: 1.0 }}, {{ scale: 1.05, duration: {duration}, ease: "none" }}, 0);
    tl_{comp_id}.fromTo("#{comp_id}-chip", {{ opacity: 0, x: -14 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 0.05);
    {head_anim}
    tl_{comp_id}.fromTo("#{comp_id}-foot", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {foot_at});
    {EXTRA.get(comp_id, "")}
    window.__timelines["{comp_id}"] = tl_{comp_id};
  </script>
</template>
"""


def main():
    for name, body, dur in SCENES:
        (OUT / f"{name}.html").write_text(page(name, body, dur), encoding="utf-8")
        print("ok", name, dur)


if __name__ == "__main__":
    main()
