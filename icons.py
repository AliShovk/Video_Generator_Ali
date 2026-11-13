#!/usr/bin/env python3
"""Помощник: иконки Iconify из локального кэша."""
from pathlib import Path

CACHE = Path("/root/video-gen/assets/icons")


def icon(name: str, x: float, y: float, size: float = 96, color: str = "#1f2c36",
         opacity: float = 1.0, cls: str = "") -> str:
    """name: 'mdi-radiator' или 'mdi:radiator'."""
    key = name.replace(":", "-")
    path = CACHE / f"{key}.svg"
    if not path.exists():
        return f'<!-- нет иконки {key} -->'
    svg = path.read_text(encoding="utf-8")
    inner = svg[svg.index(">") + 1: svg.rindex("</svg>")]
    inner = inner.replace("currentColor", color)
    s = size / 24.0
    return (f'<g class="ico {cls}" transform="translate({x} {y}) scale({s})" opacity="{opacity}">{inner}</g>')
