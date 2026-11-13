#!/usr/bin/env python3
"""Детализированный человечек: суставы, куртка, рукавицы, ботинки, лицо."""
from pathlib import Path

OUT = Path("/root/video-gen/vector-char/compositions")
OUT.mkdir(parents=True, exist_ok=True)
SKIN = "#f2c39d"
JACKET, JACKET_D = "#6b5bd2", "#5a4bc0"
PANTS, PANTS_D = "#2b3560", "#232c50"
BOOT = "#1a2138"
MITT = "#ffb066"
HAT = "#ff5a2b"


def figure(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">
  <g id="fig">
    <!-- дальняя рука -->
    <g id="armL" transform="translate(-30 -138)">
      <rect x="-12" y="-4" width="24" height="70" rx="12" fill="#463a9e"/>
      <g id="elbowL" transform="translate(0 66)">
        <rect x="-11" y="-2" width="22" height="62" rx="11" fill="#463a9e"/>
        <ellipse cx="0" cy="70" rx="15" ry="13" fill="{MITT}"/>
        <path d="M -10 66 q 10 10 20 0" stroke="#e09a4f" stroke-width="3" fill="none"/>
      </g>
    </g>
    <!-- ноги -->
    <g id="legL" transform="translate(-14 0)">
      <rect x="-13" y="-4" width="26" height="98" rx="13" fill="{PANTS_D}"/>
      <g id="kneeL" transform="translate(0 94)">
        <rect x="-12" y="-2" width="24" height="92" rx="12" fill="{PANTS_D}"/>
        <path d="M -14 88 q 14 -6 28 0 l 4 22 q -18 8 -36 0 z" fill="{BOOT}"/>
        <path d="M -16 96 q 18 6 36 0" stroke="#0f1526" stroke-width="4"/>
      </g>
    </g>
    <g id="legR" transform="translate(14 0)">
      <rect x="-13" y="-4" width="26" height="98" rx="13" fill="{PANTS}"/>
      <g id="kneeR" transform="translate(0 94)">
        <rect x="-12" y="-2" width="24" height="92" rx="12" fill="{PANTS}"/>
        <path d="M -14 88 q 14 -6 28 0 l 4 22 q -18 8 -36 0 z" fill="#222a45"/>
        <path d="M -16 96 q 18 6 36 0" stroke="#0f1526" stroke-width="4"/>
      </g>
    </g>
    <!-- торс -->
    <g id="torso" transform="translate(0 0)">
      <path d="M -56 4 q -10 -120 22 -150 q 34 -14 68 0 q 32 30 22 150 q -56 22 -112 0 z" fill="{JACKET}"/>
      <path d="M -6 -140 l 0 144" stroke="{JACKET_D}" stroke-width="4" opacity="0.8"/>
      <path d="M -46 -110 q 46 16 92 0" stroke="{JACKET_D}" stroke-width="4" fill="none" opacity="0.8"/>
      <circle cx="0" cy="-118" r="5" fill="#ffd166"/>
      <path d="M -30 -146 q 30 12 60 0 l 0 -12 q -30 10 -60 0 z" fill="#e8e2ff" opacity="0.6"/>
    </g>
    <!-- передняя рука -->
    <g id="armR" transform="translate(30 -138)">
      <rect x="-12" y="-4" width="24" height="70" rx="12" fill="#8f80f2"/>
      <g id="elbowR" transform="translate(0 66)">
        <rect x="-11" y="-2" width="22" height="62" rx="11" fill="#8f80f2"/>
        <ellipse cx="0" cy="70" rx="15" ry="13" fill="{MITT}"/>
        <path d="M -10 66 q 10 10 20 0" stroke="#e09a4f" stroke-width="3" fill="none"/>
      </g>
    </g>
    <!-- голова -->
    <g id="headBall" transform="translate(0 -190)">
      <circle cx="0" cy="0" r="38" fill="{SKIN}"/>
      <path d="M -38 -6 a 38 30 0 0 1 76 0 q -38 -18 -76 0 z" fill="{HAT}"/>
      <rect x="-40" y="-12" width="80" height="12" rx="6" fill="#fff3e2"/>
      <circle cx="-40" cy="-6" r="7" fill="#fff3e2"/>
      <circle cx="-12" cy="6" r="4.5" fill="#2b2340"/>
      <circle cx="12" cy="6" r="4.5" fill="#2b2340"/>
      <path d="M 2 16 q 6 5 -2 8" stroke="#c98f6a" stroke-width="3" fill="none"/>
      <path d="M -8 26 q 8 5 16 0" stroke="#b87a58" stroke-width="3" fill="none"/>
      <circle cx="-22" cy="20" r="7" fill="#e58f7a" opacity="0.35"/>
      <circle cx="22" cy="20" r="7" fill="#e58f7a" opacity="0.35"/>
      <g id="scarf">
        <path d="M -34 30 q 34 16 68 0 l 4 22 q -38 16 -76 0 z" fill="#2aa9c9"/>
        <path d="M 30 44 q 16 20 6 44 l -16 -6 q 8 -20 -4 -32 z" fill="#2aa9c9"/>
      </g>
    </g>
  </g>
</g>'''


def sitter(x, y, s=1.0):
    return f'''<g transform="translate({x} {y}) scale({s})">
  <g id="sitter" opacity="0">
    <rect x="-56" y="-10" width="180" height="40" rx="20" fill="#5f3d24"/>
    <rect x="-56" y="-10" width="180" height="10" rx="5" fill="#7a5232"/>
    <!-- ноги -->
    <path d="M -6 0 q 55 -6 78 6 l -4 16 q -40 -8 -74 -4 z" fill="{PANTS}"/>
    <!-- торс -->
    <g id="sitTorso" transform="translate(0 0)">
    <path d="M -46 2 q -8 -104 18 -128 q 30 -12 60 0 q 26 24 18 128 q -48 18 -96 0 z" fill="{JACKET}"/>
      <path d="M 0 -122 l 0 122" stroke="{JACKET_D}" stroke-width="4" opacity="0.8"/>
      <g id="sitArmL" transform="translate(-26 -108) rotate(16)">
        <rect x="-11" y="-6" width="22" height="62" rx="11" fill="#7a6ae0"/>
        <g transform="translate(0 56)">
          <rect x="-10" y="-2" width="20" height="54" rx="10" fill="{JACKET_D}"/>
          <ellipse cx="0" cy="60" rx="16" ry="14" fill="{MITT}"/>
        </g>
      </g>
      <g id="sitArmR" transform="translate(26 -108) rotate(30)">
        <rect x="-11" y="-6" width="22" height="62" rx="11" fill="#8a7bf0"/>
        <g transform="translate(0 56)">
          <rect x="-10" y="-2" width="20" height="54" rx="10" fill="{JACKET}"/>
          <ellipse cx="0" cy="60" rx="16" ry="14" fill="{MITT}"/>
        </g>
      </g>
      <g id="sitHead" transform="translate(0 -156)">
        <circle cx="0" cy="0" r="34" fill="{SKIN}"/>
        <path d="M -34 -4 a 34 28 0 0 1 68 0 q -34 -16 -68 0 z" fill="{HAT}"/>
        <rect x="-36" y="-10" width="72" height="10" rx="5" fill="#fff3e2"/>
        <circle cx="-11" cy="6" r="4" fill="#2b2340"/>
        <circle cx="11" cy="6" r="4" fill="#2b2340"/>
        <path d="M -7 24 q 7 4 14 0" stroke="#b87a58" stroke-width="3" fill="none"/>
        <path d="M -30 26 q 30 14 60 0 l 4 20 q -34 14 -68 0 z" fill="#2aa9c9"/>
      </g>
    </g>
  </g>
</g>'''
