#!/usr/bin/env python3
"""Генератор серии: 4 сцены на историю, движение по словам озвучки."""
from __future__ import annotations

import json
import math
import random
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, "/root/tts-bridge")
from narrator import Narrator

from data import STORIES

ROOT = Path("/root/video-gen/stories")
NODE = "/root/video-gen/node_modules/hyperframes/bin/hyperframes.mjs"
PY = sys.executable


def head_text(lines, y=210):
    return "".join(
        f'<text class="hl" x="56" y="{y + i*96}" fill="{c}" font-family="Nunito, Arial, sans-serif" '
        f'font-size="76" font-weight="900" letter-spacing="-1">{s}</text>' for i, (s, c) in enumerate(lines))


# ---------------------------------------------------------------- subjects
def ship(x, y, s, hull, deck="#f2ede0"):
    ports = "".join(f'<circle cx="{-190 + i*52}" cy="-70" r="9" fill="#0d1216" opacity="0.75"/>' for i in range(8))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M -280 -20 q 20 96 120 112 l 320 0 q 110 -20 140 -112 z" fill="{hull}"/>'
            f'<path d="M -280 -20 l 580 0 l 0 -18 l -580 0 z" fill="#000000" opacity="0.25"/>'
            f'<rect x="-210" y="-104" width="330" height="86" fill="{hull}" opacity="0.92"/>'
            f'<rect x="-120" y="-150" width="240" height="48" fill="#e9e2d2" opacity="0.85"/>'
            f'{ports}'
            f'<rect x="60" y="-236" width="34" height="86" fill="#3a3f44"/>'
            f'<rect x="60" y="-244" width="34" height="12" fill="{deck}" opacity="0.9"/>'
            f'<rect x="-70" y="-330" width="9" height="230" fill="#6b4a2a"/>'
            f'<rect x="120" y="-300" width="8" height="190" fill="#6b4a2a"/>'
            f'<path d="M -60 -320 q 74 34 0 96 z" fill="{deck}"/>'
            f'<path d="M 128 -290 q 62 28 0 84 z" fill="{deck}" opacity="0.9"/>'
            f'<path class="smokeP" d="M 78 -250 q 22 -30 6 -56 q 26 6 14 -34" stroke="#c9d4de" stroke-width="10" fill="none" opacity="0.35"/></g>')


def dam(x, y, s, accent):
    """Арочная плотина между скалами, вода за ней."""
    joints = "".join(f'<line x1="{-120 + i*80}" y1="-420" x2="{-120 + i*80}" y2="0" stroke="#6f7a82" stroke-width="3" opacity="0.6"/>' for i in range(4))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M -420 0 l 40 -520 l 120 0 l -30 520 z" fill="#3c4348"/>'
            f'<path d="M 300 0 l -40 -520 l 120 0 l 40 520 z" fill="#3c4348"/>'
            f'<path d="M -270 0 q 20 -470 270 -470 q 250 0 270 470 z" fill="#9aa4ab"/>'
            f'<path d="M -250 -30 q 20 -400 250 -400 q 230 0 250 400" stroke="#6f7a82" stroke-width="6" fill="none" opacity="0.7"/>'
            f'{joints}'
            f'<rect x="-300" y="-470" width="600" height="46" fill="#c7d0d6"/>'
            f'<path d="M -250 -470 q 250 -60 500 0 l 0 -120 q -250 -60 -500 0 z" fill="#2f6f96" opacity="0.85"/>'
            f'<path d="M 20 -420 q 30 90 0 170 q -26 80 20 160" stroke="{accent}" stroke-width="9" fill="none" opacity="0.7"/>'
            f'</g>')


def bridge(x, y, s, accent):
    """Ферменный мост с башнями над водой."""
    truss = "".join(
        f'<path d="M {-360 + i*60} -120 l 30 -46 l 30 46 z" stroke="#8d99a3" stroke-width="5" fill="none"/>' for i in range(12))
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-380" y="-120" width="760" height="18" fill="#5f6b74"/>'
            f'{truss}'
            f'<rect x="-380" y="-102" width="760" height="10" fill="#8d99a3"/>'
            f'<rect x="-330" y="-330" width="26" height="330" fill="#5f6b74"/>'
            f'<rect x="304" y="-330" width="26" height="330" fill="#5f6b74"/>'
            f'<rect x="-350" y="-346" width="66" height="18" fill="#8d99a3"/>'
            f'<rect x="284" y="-346" width="66" height="18" fill="#8d99a3"/>'
            + "".join(f'<line x1="{-310 + i*70}" y1="-330" x2="{-310 + i*70}" y2="-120" stroke="#9aa4ab" stroke-width="7" opacity="0.8"/>' for i in range(10))
            + "<g><rect x='-150' y='-176' width='120' height='46' rx='6' fill='#20262c'/>"
              "<rect x='-20' y='-170' width='90' height='40' rx='4' fill='#2a3038'/>"
              "<rect x='80' y='-170' width='90' height='40' rx='4' fill='#2a3038'/>"
              "<circle cx='-120' cy='-126' r='12' fill='#111'/><circle cx='-60' cy='-126' r='12' fill='#111'/>"
              "<circle cx='120' cy='-126' r='12' fill='#111'/></g>"
            + f'<rect x="-420" y="0" width="840" height="10" fill="#2f6f96" opacity="0.8"/></g>')


def mine(x, y, s, accent):
    """Шахтный отвал над посёлком."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M -430 0 q 210 -360 430 -360 q 220 0 430 360 z" fill="#3a352f"/>'
            f'<path d="M -300 -60 q 150 -240 300 -240 q 150 0 300 240" stroke="#4a443c" stroke-width="10" fill="none" opacity="0.6"/>'
            f'<rect x="-150" y="-120" width="300" height="120" fill="#4a443c" opacity="0.55"/>'
            + "".join(f'<line x1="{-140 + i*40}" y1="-120" x2="{-140 + i*40}" y2="0" stroke="#2b2722" stroke-width="4" opacity="0.5"/>' for i in range(8))
            + f'<g><rect x="-110" y="18" width="220" height="110" fill="#6b5b4a"/>'
              f'<path d="M -130 18 l 130 -60 l 130 60 z" fill="#8a7460"/>'
              + "".join(f'<rect x="{-92 + c*58}" y="{40 + r*44}" width="34" height="28" fill="#ffd98a" opacity="0.7"/>' for r in range(2) for c in range(4))
              + '</g></g>')


def forest(x, y, s, tree):
    out = [f'<g transform="translate({x} {y}) scale({s})">']
    for i in range(11):
        tx = -420 + i * 84
        out.append(f'<path d="M {tx} 0 l 0 -150" stroke="#4a3a2a" stroke-width="12"/>')
        out.append(f'<path d="M {tx} -120 l -40 -120 l 40 80 l 40 -80 z" fill="{tree}"/>')
    out.append('</g>')
    return "".join(out)


def plant(x, y, s, accent):
    """Химзавод: цистерны, трубы, факел."""
    tanks = "".join(
        f'<g><rect x="{-260 + i*150}" y="{-220 - (i%2)*40}" width="110" height="{220 + (i%2)*40}" rx="12" fill="#8d99a3"/>'
        f'<ellipse cx="{-205 + i*150}" cy="{-220 - (i%2)*40}" rx="55" ry="16" fill="#a9b4bd"/></g>' for i in range(3))
    pipes = ("<path d='M -280 -160 L 200 -160' stroke='#5f6b74' stroke-width='12'/>"
             "<path d='M -280 -80 L 120 -80 L 120 -420' stroke='#5f6b74' stroke-width='10'/>")
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'{tanks}{pipes}'
            f'<rect x="180" y="-520" width="26" height="520" fill="#5f6b74"/>'
            f'<ellipse class="flare" cx="193" cy="-540" rx="34" ry="46" fill="{accent}" opacity="0.55"/>'
            f'<rect x="-330" y="-40" width="660" height="40" fill="#4a545c"/></g>')


def building(x, y, s, brick):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-180" y="-520" width="360" height="520" fill="{brick}"/>'
            + "".join(f'<rect x="{-150 + c*70}" y="{-480 + r*90}" width="40" height="56" fill="#ffd98a" opacity="0.45"/>'
                      for r in range(5) for c in range(4))
            + '</g>')


SUBJ = dict(ship=ship, dam=dam, bridge=bridge, mine=mine, forest=forest, plant=plant, building=building)


# ---------------------------------------------------------------- events
def ev_blast(accent):
    return (f'<g class="flash"><circle cx="540" cy="980" r="420" fill="{accent}" opacity="0.10"/></g>'
            f'<g class="rings">' + "".join(
        f'<circle class="ring" cx="540" cy="980" r="{100 + i*90}" fill="none" stroke="{accent}" stroke-width="{10 - i}" opacity="0.7"/>'
        for i in range(4)) + '</g>'
            + '<g class="debris">' + "".join(
        f'<rect x="{300 + i*47}" y="{700 + (i%5)*60}" width="16" height="16" fill="#20262c" transform="rotate({i*23} {308+i*47} {708+(i%5)*60})"/>'
        for i in range(14)) + '</g>')


def ev_fire(accent):
    flames = "".join(
        f'<path class="flame" d="M {x} 1500 q 30 -160 0 -260 q -40 120 -70 260 z" fill="{accent}" opacity="0.85"/>'
        for x in range(180, 980, 90))
    return (f'<g>{flames}</g><g class="smokeG">' + "".join(
        f'<circle class="smoke" cx="{220 + i*70}" cy="{1180 - (i%4)*60}" r="{40 + i%3*18}" fill="#2a2f34" opacity="0.6"/>'
        for i in range(9)) + '</g>')


def ev_wave(accent):
    return (f'<g class="wave"><path d="M -400 1560 q 380 -640 760 -460 q 300 130 760 -120 l 0 900 l -1520 0 z" fill="{accent}" opacity="0.9"/>'
            f'<path d="M -400 1560 q 380 -640 760 -460 q 300 130 760 -120" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.5"/></g>')


def ev_flood(accent):
    return (f'<g class="flood"><rect x="-200" y="1500" width="1600" height="600" fill="{accent}" opacity="0.9"/>'
            f'<g class="waves">' + "".join(
        f'<path d="M {-100 + i*220} 1500 q 60 -40 120 0" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.5"/>' for i in range(8)) + '</g></g>')


def ev_collapse(steel="#3a4650"):
    return ('<g class="pieces">' + "".join(
        f'<rect class="piece" x="{260 + i*70}" y="{820 + (i%4)*80}" width="{40 + i%3*30}" height="18" fill="{steel}" '
        f'transform="rotate({i*17} {260+i*70} {820+(i%4)*80})"/>' for i in range(10)) + '</g>')


def ev_cloud(accent):
    return ('<g class="cloudG">' + "".join(
        f'<ellipse class="gas" cx="{240 + i*90}" cy="{1180 - (i%4)*70}" rx="{120 + i%3*40}" ry="{80 + i%3*30}" '
        f'fill="{accent}" opacity="0.45"/>' for i in range(9)) + '</g>')


EV = dict(blast=ev_blast, fire=ev_fire, wave=ev_wave, flood=ev_flood, collapse=ev_collapse, cloud=ev_cloud)


def scene1(st):
    a = st["accent"]
    b = [f'<rect width="1080" height="1920" fill="{st["bg"]}"/>']
    b.append(f'<rect x="0" y="1500" width="1080" height="420" fill="#000000" opacity="0.35"/>')
    b.append(f'<rect x="0" y="1460" width="1080" height="460" fill="#000000" opacity="0.45"/>')
    b.append('<rect x="0" y="1560" width="1080" height="30" fill="#ffffff" opacity="0.08"/>')
    b.append('<g class="wline">' + "".join(
        f'<path d="M {-40 + i*140} {1620 + (i%3)*70} q 50 -22 100 0" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.25"/>'
        for i in range(9)) + '</g>')
    b.append(SUBJ[st["subject"]](540, 1560, 1.55, a))

    b.append(head_text([(st["hook"][0], a), (st["hook"][1], "#ffffff")]))
    b.append(f'<text class="sub" x="56" y="520" font-family="Nunito, Arial" font-size="40" font-weight="800" '
             f'fill="#ffffff" opacity="0.75">{st["hook_sub"]}</text>')
    return "".join(b)


def scene2(st):
    a = st["accent"]
    b = [f'<rect width="1080" height="1920" fill="{st["bg"]}"/>']
    b.append(SUBJ[st["subject"]](430, 1500, 1.15, a))
    b.append('<g class="callouts">')
    for i, (num, txt) in enumerate(st["callouts"]):
        y = 380 + i * 190
        b.append(f'<g class="call c{i}" opacity="0"><rect x="60" y="{y}" width="420" height="150" rx="14" fill="#000000" opacity="0.45"/>'
                 f'<text x="90" y="{y+80}" font-family="Nunito, Arial" font-size="62" font-weight="900" fill="{a}">{num}</text>'
                 f'<text x="90" y="{y+126}" font-family="Nunito, Arial" font-size="30" font-weight="800" fill="#ffffff" opacity="0.8">{txt}</text></g>')
    b.append('</g>')
    return "".join(b)


def scene3(st):
    a = st["accent"]
    b = [f'<rect width="1080" height="1920" fill="{st["bg"]}"/>']
    b.append(SUBJ[st["subject"]](540, 1560, 1.45, a))
    b.append(EV[st["event"]](a))
    return "".join(b)


def scene4(st):
    a = st["accent"]
    b = [f'<rect width="1080" height="1920" fill="#0b0f12"/>']
    b.append(f'<rect x="70" y="700" width="10" height="220" fill="{a}"/>')
    b.append(f'<text class="big" x="540" y="780" font-family="Nunito, Arial" font-size="150" font-weight="900" fill="{a}" text-anchor="middle">{st["callouts"][0][0]}</text>')
    b.append(f'<text x="540" y="860" font-family="Nunito, Arial" font-size="40" font-weight="800" fill="#ffffff" opacity="0.75" text-anchor="middle">{st["callouts"][0][1]}</text>')
    b.append(f'<text class="cap1" x="540" y="1180" font-family="Nunito, Arial" font-size="58" font-weight="900" fill="#ffffff" text-anchor="middle" opacity="0">{st["caption"][0]}</text>')
    b.append(f'<text class="cap2" x="540" y="1260" font-family="Nunito, Arial" font-size="58" font-weight="900" fill="{a}" text-anchor="middle" opacity="0">{st["caption"][1]}</text>')
    return "".join(b)


SCENES = dict(s1=scene1, s2=scene2, s3=scene3, s4=scene4)


def page(sid, body, dur, st):
    return f"""<template>
  <style>#root{{position:absolute;inset:0;overflow:hidden;background:{st['bg']}}}.world{{position:absolute;inset:0;width:100%;height:100%}}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="clip" id="{sid}-clip" data-start="0" data-duration="{dur}">
      <div id="{sid}-in"><svg class="world" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">{body}</svg></div>
    </div>
  </div>
  <script>
    const tl_{sid} = gsap.timeline({{ paused: true }});
    const tl = tl_{sid};
    tl.fromTo("#{sid} .world", {{ scale:1.0 }}, {{ scale:1.07, duration:{dur}, ease:"none" }}, 0);
    tl.fromTo(".hl", {{ opacity:0, y:26 }}, {{ opacity:1, y:0, duration:0.5, stagger:0.14, ease:"power3.out" }}, 0.1);
    tl.fromTo(".sub", {{ opacity:0 }}, {{ opacity:0.75, duration:0.7 }}, 0.7);
    tl.fromTo(".call", {{ opacity:0, x:-40 }}, {{ opacity:1, x:0, duration:0.45, stagger:0.5 }}, 0.3);
    tl.to(".ring", {{ scale:1.6, opacity:0, duration:2.2, transformOrigin:"50% 50%", stagger:0.4, repeat:2, ease:"power2.out" }}, 0);
    tl.to(".flash", {{ opacity:0.28, duration:0.4, yoyo:true, repeat:8 }}, 0);
    tl.to(".debris", {{ y:-90, x:30, duration:2.0, stagger:0.05, repeat:3, ease:"power1.out" }}, 0);
    tl.to(".flame", {{ scaleY:1.15, transformOrigin:"50% 100%", duration:0.5, yoyo:true, repeat:16, stagger:0.08 }}, 0);
    tl.to(".smoke", {{ y:-160, opacity:0.15, duration:3.2, stagger:0.15, repeat:2 }}, 0);
    tl.to(".wave", {{ x:"+=160", duration:{dur}, ease:"power1.in" }}, 0);
    tl.to(".gas", {{ y:-120, x:"+=40", duration:4.5, stagger:0.12, ease:"sine.inOut" }}, 0);
    tl.to(".piece", {{ y:260, rotation:40, duration:1.8, stagger:0.12, ease:"power2.in" }}, 0.3);
    tl.fromTo(".big", {{ scale:0.5, opacity:0 }}, {{ scale:1, opacity:1, duration:0.7, ease:"back.out(2)" }}, 0.2);
    tl.to(".cap1", {{ opacity:1, duration:0.5 }}, 0.8);
    tl.to(".cap2", {{ opacity:1, duration:0.5 }}, 1.2);
    window.__timelines["{sid}"] = tl_{sid};
  </script>
</template>
"""


def build_project(st: dict) -> Path:
    proj = ROOT / st["slug"]
    comps = proj / "compositions"
    comps.mkdir(parents=True, exist_ok=True)

    # озвучка
    n = Narrator(voice="eugene", lead=0.0, gap=0.10, delay_ms=250)
    vdir = proj / "voice"
    vdir.mkdir(exist_ok=True)
    starts, durs, t = [], [], 0.2
    for i, text in enumerate(st["voice"]):
        p = n.say(text, vdir / f"p{i}.wav")
        with wave.open(str(p)) as f:
            d = f.getnframes() / f.getframerate()
        starts.append(t)
        durs.append(d)
        t += d + 0.10
    total = round(t + 0.5, 2)

    # 8 фраз -> 4 сцены по 2 фразы
    per = max(1, len(st["voice"]) // 4)
    cuts = [0, per, 2 * per, 3 * per, len(st["voice"])]
    bounds = []
    for i in range(4):
        st_t = starts[cuts[i]]
        end = starts[cuts[i + 1]] if cuts[i + 1] < len(st["voice"]) else total
        bounds.append((round(st_t, 3), round(end - st_t, 2)))

    hosts = []
    for i, sid in enumerate(SCENES):
        st_t, dur = bounds[i]
        (comps / f"{sid}.html").write_text(page(sid, SCENES[sid](st), dur, st), encoding="utf-8")
        hosts.append(f'<div id="{sid}" class="scene" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" '
                     f'data-start="{st_t}" data-duration="{dur}" data-track-index="{i+1}" data-track-kind="graphics" '
                     f'data-width="1080" data-height="1920"></div>')

    index = f"""<!doctype html><html lang="ru"><head><meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden}}
#root{{position:relative;width:100%;height:100%;overflow:hidden}}.scene{{position:absolute;inset:0}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
{''.join(hosts)}</div>
<script>window.__timelines=window.__timelines||{{}};window.__timelines["main"]=gsap.timeline({{paused:true}});</script>
</body></html>"""
    (proj / "index.html").write_text(index, encoding="utf-8")

    # дорожка
    import numpy as np
    SR = 48000
    mix = np.zeros(int(total * SR), dtype=np.float32)
    for i in range(len(st["voice"])):
        with wave.open(str(vdir / f"p{i}.wav")) as f:
            a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int(starts[i] * SR)
        mix[s:s + len(a)] += a
    peak = float(np.max(np.abs(mix))) or 1.0
    mix = mix / peak * 0.9
    with wave.open(str(proj / "voice.wav"), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((mix * 32767).astype(np.int16).tobytes())

    json.dump(dict(total=total, starts=starts, durs=durs), open(proj / "timings.json", "w"), indent=2)
    return proj


def render(st: dict) -> str:
    proj = build_project(st)
    out = proj / "final.mp4"
    subprocess.run(["node", NODE, "render", "-o", "render.mp4", "--quality", "high"],
                   cwd=proj, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total = json.load(open(proj / "timings.json"))["total"]
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(proj / "render.mp4"),
                    "-i", str(proj / "voice.wav"), "-c:v", "libx264", "-profile:v", "main", "-preset", "medium",
                    "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-t", str(total),
                    "-movflags", "+faststart", "-aspect", "9:16", str(out)], check=True)
    return str(out)


if __name__ == "__main__":
    only = sys.argv[1:] or None
    for st in STORIES:
        if only and st["slug"] not in only:
            continue
        print("start", st["slug"], flush=True)
        print("done", render(st), flush=True)
