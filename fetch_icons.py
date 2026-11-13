#!/usr/bin/env python3
"""Скачивает набор иконок Iconify в локальный кэш (SVG)."""
import json
import urllib.request
from pathlib import Path

OUT = Path("/root/video-gen/assets/icons")
OUT.mkdir(parents=True, exist_ok=True)

ICONS = [
    "mdi:radiator", "mdi:water-boiler", "mdi:pipe", "mdi:pipe-valve", "mdi:water-pump",
    "mdi:thermometer", "mdi:thermostat", "mdi:home-thermometer", "mdi:floor-plan",
    "mdi:ruler-square", "mdi:hammer-wrench", "mdi:check-circle", "mdi:alert-circle",
    "mdi:valve", "mdi:gauge", "mdi:fire", "mdi:snowflake", "mdi:home", "mdi:layers",
    "mdi:square-outline", "mdi:arrow-right", "mdi:information", "mdi:water",
    "mdi:format-list-numbered", "mdi:clock-outline", "mdi:cash", "mdi:tools",
    "mdi:heat-wave", "mdi:radiator-off", "mdi:pipe-disconnected", "mdi:valve-open",
    "mdi:valve-closed", "mdi:thermometer-high", "mdi:thermometer-low", "mdi:home-thermometer-outline",
]


def fetch(name: str) -> bool:
    set_name, icon = name.split(":", 1)
    url = f"https://api.iconify.design/{set_name}/{icon}.svg?height=256"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            svg = r.read().decode()
    except Exception as e:  # noqa: BLE001
        print("fail", name, e)
        return False
    (OUT / f"{set_name}-{icon}.svg").write_text(svg, encoding="utf-8")
    return True


ok = sum(fetch(n) for n in ICONS)
print("скачано", ok, "из", len(ICONS), "→", OUT)
