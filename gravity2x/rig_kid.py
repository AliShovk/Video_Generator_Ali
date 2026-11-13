#!/usr/bin/env python3
"""Мальчик: ближе к реальной анатомии, 6.5 голов, плоская заливка."""
SKIN, SKIN_D = "#f6c9a3", "#e3b189"
HAIR, HAIR_D = "#6b4527", "#573820"
TEE, TEE_D = "#e04b3a", "#c0392b"
SHORTS, SHORTS_D = "#3f6fb5", "#31578f"
SOCK = "#f2efe8"
SHOE, SHOE_D = "#2f5fa8", "#22467d"


def kid() -> str:
    return f'''
<g id="mover">
  <!-- дальняя нога -->
  <g id="legFar">
    <path d="M -15 -4 q -3 46 -4 100 q 0 6 6 6 l 16 0 q 6 0 6 -6 q -2 -54 4 -100 z" fill="{SKIN_D}"/>
    <g id="kneeFar">
      <path d="M -12 0 q -2 40 -3 82 q 0 5 5 5 l 14 0 q 5 0 5 -5 q -1 -42 3 -82 z" fill="{SKIN_D}"/>
      <rect x="-12" y="74" width="26" height="14" rx="6" fill="{SOCK}"/>
      <path d="M -13 86 q 13 -3 26 0 l 1 6 q 0 8 -8 8 l -16 0 q -6 0 -6 -6 z" fill="{SHOE_D}"/>
      <path d="M -13 98 q 14 4 27 0 l 0 5 q -14 4 -27 0 z" fill="#182f52"/>
    </g>
  </g>
  <!-- дальняя рука -->
  <g id="armFar">
    <path d="M -10 -4 q -4 30 -5 52 q -1 18 3 36 l 16 0 q -5 -18 -4 -36 q 1 -22 4 -52 z" fill="{SKIN_D}"/>
    <g id="elbowFar">
      <path d="M -8 0 q -2 34 -2 62 q 0 8 4 16 l 12 0 q -5 -8 -4 -16 q 1 -28 3 -62 z" fill="{SKIN_D}"/>
      <path d="M -6 78 q 4 -6 10 0 q 3 10 -2 16 q -6 4 -10 -2 q -3 -8 2 -14 z" fill="{SKIN_D}"/>
    </g>
  </g>
  <!-- торс и шорты -->
  <g id="torso">
    <path d="M -46 -118 q 8 -12 22 -14 q 12 -2 24 -2 q 12 0 24 2 q 14 2 22 14 q 6 30 4 62 q -2 26 -8 46 q -20 10 -42 10 q -22 0 -42 -10 q -6 -20 -8 -46 q -2 -32 4 -62 z" fill="{TEE}"/>
    <path d="M -46 -118 q 10 16 0 34 q -6 26 -6 50 l 14 4 q 2 -30 6 -52 q 4 -22 2 -36 z" fill="{TEE_D}" opacity="0.55"/>
    <path d="M 46 -118 q -10 16 0 34 q 6 26 6 50 l -14 4 q -2 -30 -6 -52 q -4 -22 -2 -36 z" fill="{TEE_D}" opacity="0.55"/>
    <path d="M -22 -132 q 22 10 44 0 l -2 -10 q -20 8 -40 0 z" fill="{TEE_D}" opacity="0.7"/>
    <path d="M -34 -22 q 34 10 68 0 l -4 46 q -30 10 -60 0 z" fill="{SHORTS}"/>
    <path d="M -30 24 q 30 8 60 0 l -2 16 q -28 8 -56 0 z" fill="{SHORTS_D}" opacity="0.75"/>
  </g>
  <!-- ближняя нога -->
  <g id="legNear">
    <path d="M -16 -4 q -3 48 -4 102 q 0 6 6 6 l 18 0 q 6 0 6 -6 q -2 -56 4 -102 z" fill="{SKIN}"/>
    <g id="kneeNear">
      <path d="M -13 0 q -2 42 -3 84 q 0 5 5 5 l 16 0 q 5 0 5 -5 q -1 -44 3 -84 z" fill="{SKIN}"/>
      <rect x="-13" y="76" width="28" height="15" rx="7" fill="{SOCK}"/>
      <path d="M -14 88 q 14 -3 28 0 l 1 7 q 0 8 -8 8 l -18 0 q -6 0 -6 -6 z" fill="{SHOE}"/>
      <path d="M -14 100 q 15 4 29 0 l 0 6 q -15 4 -29 0 z" fill="{SOCK}"/>
    </g>
  </g>
  <!-- голова -->
  <g id="head">
    <path d="M -20 -12 q 0 22 10 30 q 10 8 20 8 q 12 0 22 -8 q 10 -8 10 -30 q 0 -32 -31 -32 q -31 0 -31 32 z" fill="{SKIN}"/>
    <path d="M 30 2 q 12 5 1 11 q -8 3 -11 -2 z" fill="{SKIN}"/>
    <path d="M 22 12 q 6 1 8 -3" stroke="#b87a58" stroke-width="2.6" fill="none"/>
    <path d="M 2 18 q 8 5 16 -1" stroke="#c98f6a" stroke-width="2.4" fill="none"/>
    <circle cx="14" cy="-2" r="4.4" fill="#2b2340"/>
    <circle cx="15.6" cy="-3.2" r="1.5" fill="#fff"/>
    <path d="M 8 -12 q 8 -4 14 0" stroke="{HAIR_D}" stroke-width="3" fill="none"/>
    <circle cx="6" cy="12" r="6" fill="#e58f7a" opacity="0.28"/>
    <path d="M -32 -6 q -3 -30 32 -32 q 35 2 32 32 q -6 -16 -32 -16 q -26 0 -32 16 z" fill="{HAIR}"/>
    <path d="M -32 -6 q 4 -14 16 -18 q -6 10 -4 20 z" fill="{HAIR_D}"/>
    <path d="M -12 -34 q 14 -6 28 -2 q 10 4 12 12 q -16 -10 -40 -10 z" fill="{HAIR_D}" opacity="0.8"/>
    <path d="M -20 30 q 20 8 40 0 l 0 8 q -20 8 -40 0 z" fill="{SKIN_D}" opacity="0.5"/>
  </g>
  <!-- ближняя рука -->
  <g id="armNear">
    <path d="M -11 -4 q -4 32 -5 54 q -1 18 3 38 l 18 0 q -5 -20 -4 -38 q 1 -22 4 -54 z" fill="{SKIN}"/>
    <g id="elbowNear">
      <path d="M -9 0 q -2 36 -2 64 q 0 8 4 16 l 14 0 q -5 -8 -4 -16 q 1 -28 3 -64 z" fill="{SKIN}"/>
      <path d="M -7 80 q 5 -6 11 0 q 3 10 -2 17 q -7 4 -11 -2 q -3 -9 2 -15 z" fill="{SKIN}"/>
      <path d="M -4 88 q 5 3 10 0" stroke="{SKIN_D}" stroke-width="2" fill="none"/>
    </g>
  </g>
</g>'''
