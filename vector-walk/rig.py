#!/usr/bin/env python3
"""Человечек в профиль: правильный шаг, руки и ноги в противофазе."""
from pathlib import Path

SKIN = "#f2c39d"
JACKET, JACKET_D = "#6b5bd2", "#4a3cae"
PANTS, PANTS_D = "#2b3560", "#1f2745"
BOOT = "#141b30"
MITT = "#ffb066"
HAT = "#ff5a2b"


def walker(detail: str = "medium") -> str:
    """Возвращает группы без transform-атрибутов: позиции задаёт GSAP."""
    return f'''
<g id="mover">
  <!-- дальняя нога -->
  <g id="legFar">
    <rect x="-11" y="0" width="22" height="92" rx="11" fill="{PANTS_D}"/>
    <g id="kneeFar">
      <rect x="-10" y="0" width="20" height="86" rx="10" fill="{PANTS_D}"/>
      <path d="M -16 80 q 16 -6 32 0 l 6 20 q -20 8 -42 0 z" fill="#101728"/>
    </g>
  </g>
  <!-- дальняя рука -->
  <g id="armFar">
    <rect x="-10" y="0" width="20" height="60" rx="10" fill="#3f3390"/>
    <g id="elbowFar">
      <rect x="-9" y="0" width="18" height="54" rx="9" fill="#3f3390"/>
      <ellipse cx="0" cy="60" rx="13" ry="11" fill="#e09a4f"/>
    </g>
  </g>
  <!-- торс -->
  <g id="torso">
    <path d="M -24 4 q -6 -96 8 -126 q 18 -10 34 0 q 14 30 8 126 q -26 12 -50 0 z" fill="{JACKET}"/>
    <path d="M 6 -118 l 0 122" stroke="{JACKET_D}" stroke-width="3" opacity="0.85"/>
    <path d="M -18 -96 q 20 8 40 0" stroke="{JACKET_D}" stroke-width="3" fill="none" opacity="0.7"/>
    <path d="M -14 -124 q 16 8 32 0 l -2 -10 q -14 6 -28 0 z" fill="#e8e2ff" opacity="0.65"/>
  </g>
  <!-- ближняя нога -->
  <g id="legNear">
    <rect x="-12" y="0" width="24" height="94" rx="12" fill="{PANTS}"/>
    <g id="kneeNear">
      <rect x="-11" y="0" width="22" height="88" rx="11" fill="{PANTS}"/>
      <path d="M -17 82 q 17 -6 34 0 l 7 21 q -22 9 -45 0 z" fill="{BOOT}"/>
      <path d="M -18 92 q 20 7 40 0" stroke="#0b1020" stroke-width="4"/>
    </g>
  </g>
  <!-- голова в профиль -->
  <g id="head">
    <circle cx="0" cy="0" r="27" fill="{SKIN}"/>
    <path d="M 22 2 q 10 3 0 9 q -6 3 -8 -1 z" fill="{SKIN}"/>
    <path d="M -28 -2 a 28 24 0 0 1 56 0 q -28 -14 -56 0 z" fill="{HAT}"/>
    <rect x="-30" y="-8" width="60" height="10" rx="5" fill="#fff3e2"/>
    <circle cx="-30" cy="-3" r="6" fill="#fff3e2"/>
    <circle cx="12" cy="1" r="3.4" fill="#2b2340"/>
    <path d="M 8 10 q 6 3 10 0" stroke="#b87a58" stroke-width="2.5" fill="none"/>
    <path d="M -22 20 q 22 12 44 -2 l 6 16 q -28 14 -56 2 z" fill="#2aa9c9"/>
  </g>
  <!-- ближняя рука -->
  <g id="armNear">
    <rect x="-11" y="0" width="22" height="62" rx="11" fill="#8f80f2"/>
    <g id="elbowNear">
      <rect x="-10" y="0" width="20" height="56" rx="10" fill="#8f80f2"/>
      <ellipse cx="0" cy="62" rx="14" ry="12" fill="{MITT}"/>
      <path d="M -9 58 q 9 8 18 0" stroke="#e09a4f" stroke-width="3" fill="none"/>
    </g>
  </g>
</g>'''


def sitter() -> str:
    return f'''
<g id="sitter" opacity="0">
  <rect x="-70" y="-6" width="190" height="36" rx="18" fill="#5f3d24"/>
  <rect x="-70" y="-6" width="190" height="9" rx="4" fill="#7a5232"/>
  <path d="M -8 0 q 66 -8 96 4 l -6 18 q -46 -10 -88 -6 z" fill="{PANTS}"/>
  <g id="sitLeg">
    <rect x="66" y="12" width="24" height="70" rx="12" fill="{PANTS_D}"/>
    <path d="M 60 74 q 18 -6 36 0 l 6 22 q -24 8 -48 0 z" fill="{BOOT}"/>
  </g>
  <g id="sitTorso">
    <path d="M -28 2 q -6 -96 10 -122 q 18 -10 32 0 q 12 26 8 122 q -26 12 -50 0 z" fill="{JACKET}"/>
    <path d="M 4 -116 l 0 118" stroke="{JACKET_D}" stroke-width="3" opacity="0.8"/>
    <g id="sitArmNear">
      <rect x="-10" y="0" width="20" height="58" rx="10" fill="#8f80f2"/>
      <g id="sitElbowNear">
        <rect x="-9" y="0" width="18" height="50" rx="9" fill="#8f80f2"/>
        <ellipse cx="0" cy="56" rx="13" ry="11" fill="{MITT}"/>
      </g>
    </g>
  </g>
  <g id="sitHead">
    <circle cx="0" cy="0" r="26" fill="{SKIN}"/>
    <path d="M 21 2 q 9 3 0 9 q -6 2 -8 -1 z" fill="{SKIN}"/>
    <path d="M -27 -2 a 27 23 0 0 1 54 0 q -27 -13 -54 0 z" fill="{HAT}"/>
    <rect x="-29" y="-8" width="58" height="10" rx="5" fill="#fff3e2"/>
    <circle cx="11" cy="1" r="3.2" fill="#2b2340"/>
    <path d="M 7 10 q 6 3 10 0" stroke="#b87a58" stroke-width="2.5" fill="none"/>
    <path d="M -20 18 q 20 12 40 -2 l 6 15 q -26 13 -52 2 z" fill="#2aa9c9"/>
  </g>
</g>'''
