#!/usr/bin/env python3
"""Чернобыльская арка — реалистичная подача: материалы, свет, воздух, масштаб."""
import math
from pathlib import Path

OUT = Path("/root/video-gen/chernobyl-real/compositions")
OUT.mkdir(parents=True, exist_ok=True)

DEFS = """
<defs>
  <linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#05080d"/><stop offset="0.45" stop-color="#0b1622"/>
    <stop offset="0.78" stop-color="#1a2634"/><stop offset="1" stop-color="#2a3138"/>
  </linearGradient>
  <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ff9a4d" stop-opacity="0.55"/><stop offset="1" stop-color="#ff9a4d" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="steel" x1="0" y1="0" x2="0.2" y2="1">
    <stop offset="0" stop-color="#dfe9f1"/><stop offset="0.22" stop-color="#9fb2c1"/>
    <stop offset="0.55" stop-color="#61727f"/><stop offset="0.8" stop-color="#3a4852"/><stop offset="1" stop-color="#212b33"/>
  </linearGradient>
  <linearGradient id="steelDark" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#4c5b67"/><stop offset="0.5" stop-color="#2b353d"/><stop offset="1" stop-color="#151c22"/>
  </linearGradient>
  <linearGradient id="concrete" x1="0" y1="0" x2="0.3" y2="1">
    <stop offset="0" stop-color="#5b6167"/><stop offset="0.5" stop-color="#3a4046"/><stop offset="1" stop-color="#232a30"/>
  </linearGradient>
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3a3a36"/><stop offset="0.35" stop-color="#232421"/><stop offset="1" stop-color="#0c0e0f"/>
  </linearGradient>
  <linearGradient id="rail" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#b9c6cf"/><stop offset="0.5" stop-color="#6f808c"/><stop offset="1" stop-color="#2f3a42"/>
  </linearGradient>
  <radialGradient id="warm" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="#ffb066" stop-opacity="0.85"/><stop offset="1" stop-color="#ff6a1a" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vignette" cx="50%" cy="45%" r="72%">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.72"/>
  </radialGradient>
  <linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8fa6b8" stop-opacity="0"/><stop offset="1" stop-color="#8fa6b8" stop-opacity="0.16"/>
  </linearGradient>
  <filter id="soft8"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="soft24"><feGaussianBlur stdDeviation="24"/></filter>
  <filter id="soft60"><feGaussianBlur stdDeviation="60"/></filter>
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000" flood-opacity="0.55"/>
  </filter>
  <filter id="metalNoise">
    <feTurbulence type="fractalNoise" baseFrequency="0.02 0.6" numOctaves="2" seed="3" result="n"/>
    <feColorMatrix in="n" type="saturate" values="0" result="g"/>
    <feComposite in="g" in2="SourceGraphic" operator="in" result="c"/>
    <feBlend in="SourceGraphic" in2="c" mode="overlay"/>
  </filter>
</defs>
"""


def svg(body, bg="#060a0e"):
    return (f'<svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            f'{DEFS}<rect width="1080" height="1920" fill="{bg}"/>{body}</svg>')


def text(x, y, s, size=28, color="#e8e3d9", anchor="start", mono=True, ls=2, weight="400", opacity=1):
    fam = "JetBrains Mono, monospace" if mono else "Inter, sans-serif"
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{fam}" font-size="{size}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}" font-weight="{weight}" opacity="{opacity}">{s}</text>')


def grain(opacity=0.05):
    return f'<rect width="1080" height="1920" filter="url(#grain)" opacity="{opacity}" style="mix-blend-mode:overlay"/>'


def vignette():
    return '<rect width="1080" height="1920" fill="url(#vignette)"/>'


def dust(n=90, y0=900, y1=1600, seed=11, color="#cfd8de", op=0.35):
    rnd = __import__("random").Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(0, 1080); y = rnd.uniform(y0, y1); r = rnd.uniform(0.6, 2.4)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{color}" opacity="{rnd.uniform(0.08, op):.2f}"/>')
    return "".join(out)


def human(x, y, s=1.0, color="#0d1114", helmet="#ffb066"):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<ellipse cx="0" cy="2" rx="16" ry="4" fill="#000" opacity="0.35"/>'
            f'<rect x="-7" y="-52" width="14" height="34" rx="3" fill="{color}"/>'
            f'<rect x="-9" y="-20" width="7" height="20" fill="{color}"/><rect x="2" y="-20" width="7" height="20" fill="{color}"/>'
            f'<circle cx="0" cy="-58" r="7" fill="{color}"/><path d="M-8 -60 q8 -8 16 0" fill="{helmet}"/>'
            f'</g>')


def truck(x, y, s=1.0, flip=False):
    f = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return (f'<g transform="{f}">'
            f'<ellipse cx="0" cy="4" rx="46" ry="6" fill="#000" opacity="0.4"/>'
            f'<rect x="-44" y="-30" width="30" height="26" rx="4" fill="#2b3944"/>'
            f'<rect x="-16" y="-24" width="60" height="20" rx="3" fill="#1c262e"/>'
            f'<rect x="-46" y="-6" width="92" height="10" rx="2" fill="#0f1519"/>'
            f'<circle cx="-30" cy="2" r="8" fill="#0a0e11"/><circle cx="26" cy="2" r="8" fill="#0a0e11"/>'
            f'<circle cx="-46" cy="-22" r="3" fill="#ffe0a8"/><circle cx="-46" cy="-14" r="3" fill="#ffe0a8"/>'
            f'</g>')


def crane(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" opacity="0.9">'
            f'<rect x="-4" y="-260" width="8" height="260" fill="#6d7a84"/>'
            f'<path d="M-4 -250 L-150 -250 L-4 -210 Z" fill="none" stroke="#6d7a84" stroke-width="4"/>'
            f'<path d="M0 -250 L120 -250" stroke="#8b98a2" stroke-width="5"/>'
            f'<line x1="120" y1="-250" x2="120" y2="-190" stroke="#8b98a2" stroke-width="2"/>'
            f'<rect x="112" y="-192" width="16" height="12" fill="#3a4750"/>'
            f'</g>')
