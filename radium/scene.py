#!/usr/bin/env python3
"""Общие элементы: «Девушки, которые светились»."""
import math
import random

DARK = "#0d1618"
TEAL = "#16323a"
TEAL_L = "#1f4750"
GLOW = "#8affb0"
GLOW_D = "#4be08a"
SKIN = "#f2c9a4"
DRESS = "#2f4a5a"
DRESS_L = "#40606f"
BRASS = "#c9a24a"
PAPER = "#efe6d2"
RED = "#c0392b"

DEFS = f"""
<defs>
  <radialGradient id="glowG"><stop offset="0" stop-color="{GLOW}" stop-opacity="0.85"/><stop offset="0.45" stop-color="{GLOW_D}" stop-opacity="0.28"/><stop offset="1" stop-color="{GLOW_D}" stop-opacity="0"/></radialGradient>
  <linearGradient id="roomG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132426"/><stop offset="1" stop-color="#0a1214"/></linearGradient>
  <linearGradient id="dressG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{DRESS_L}"/><stop offset="1" stop-color="{DRESS}"/></linearGradient>
  <linearGradient id="paperG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6efdd"/><stop offset="1" stop-color="#ddd0b6"/></linearGradient>
</defs>
"""


def woman(x, y, s=1.0, ident="", arm=False):
    """Работница 1910-х: пучок, платье, фартук."""
    arm_svg = (f'<g class="arm"><path d="M 22 -104 q 44 22 40 54" stroke="{SKIN}" stroke-width="13" '
               f'fill="none" stroke-linecap="round"/></g>') if arm else ''
    ident_attr = f' id="{ident}"' if ident else ''
    return (f'<g{ident_attr} transform="translate({x} {y}) scale({s})">'
            f'<g class="bob">'
            f'<path d="M -34 0 L -26 -110 L 26 -110 L 34 0 Z" fill="url(#dressG)"/>'
            f'<path d="M -20 -108 L -14 -150 L 14 -150 L 20 -108 Z" fill="{SKIN}"/>'
            f'<circle cx="0" cy="-168" r="25" fill="{SKIN}"/>'
            f'<path d="M -26 -172 q 4 -34 26 -34 q 22 0 26 34 q -14 -14 -26 -14 q -12 0 -26 14 z" fill="#3b2a20"/>'
            f'<circle cx="0" cy="-200" r="12" fill="#3b2a20"/>'
            f'<rect x="-26" y="-96" width="52" height="16" rx="6" fill="#e8e2d2" opacity="0.9"/>'
            f'{arm_svg}'
            f'</g></g>')


def bench(x, y, w=760, h=26):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#5a3f2a"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="#7a5738"/>'
            f'<rect x="{x+30}" y="{y+h}" width="16" height="{240}" fill="#4a3322"/>'
            f'<rect x="{x+w-46}" y="{y+h}" width="16" height="140" fill="#4a3322"/></g>')


def dial(x, y, r=54, glow=True):
    ticks = "".join(
        f'<line x1="0" y1="{-r+8}" x2="0" y2="{-r+20}" stroke="{GLOW}" stroke-width="5" '
        f'transform="rotate({a})"/>' for a in range(0, 360, 30))
    return (f'<g class="dial" transform="translate({x} {y})">'
            + (f'<circle r="{r*1.9}" fill="url(#glowG)" class="halo"/>' if glow else '')
            + f'<circle r="{r}" fill="#12252a" stroke="{GLOW}" stroke-width="4"/>{ticks}'
            f'<line class="hand" x1="0" y1="0" x2="0" y2="{-r*0.55}" stroke="{GLOW}" stroke-width="5" stroke-linecap="round"/>'
            f'<line class="hand2" x1="0" y1="0" x2="{r*0.4}" y2="0" stroke="{GLOW}" stroke-width="4" stroke-linecap="round"/>'
            f'<circle r="6" fill="{GLOW}"/></g>')


def brush(x, y, ang=-30, s=1.0, ident=""):
    ident_attr = f' id="{ident}"' if ident else ''
    return (f'<g{ident_attr} transform="translate({x} {y}) scale({s}) rotate({ang})">'
            f'<g class="brush">'
            f'<rect x="0" y="-4" width="86" height="8" rx="4" fill="{BRASS}"/>'
            f'<path class="tip" d="M 86 -5 l 26 5 l -26 5 z" fill="{GLOW}"/>'
            f'<circle class="tipGlow" cx="112" cy="0" r="22" fill="url(#glowG)"/>'
            f'</g></g>')


def dust(n=26, seed=2, w=1080, h=1400):
    r = random.Random(seed)
    return "".join(
        f'<circle class="mote" cx="{r.uniform(0, w):.0f}" cy="{r.uniform(200, h):.0f}" '
        f'r="{r.uniform(2, 6):.1f}" fill="{GLOW}" opacity="{r.uniform(0.25, 0.8):.2f}"/>' for _ in range(n))


def label(x, y, t, size=44, col=GLOW, weight=900, anchor="start", cls="lbl"):
    return (f'<text class="{cls}" x="{x}" y="{y}" font-family="Nunito, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{weight}" fill="{col}" text-anchor="{anchor}">{t}</text>')
