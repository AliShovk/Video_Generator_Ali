#!/usr/bin/env python3
"""Карусель «глубинный полив» — 6 слайдов 1080×1350. Схематичная инфографика с выносками."""
from pathlib import Path

OUT = Path('/root/video-gen/carousel-irrigation')
OUT.mkdir(parents=True, exist_ok=True)

CREAM = '#F1E6CE'
SAND = '#C9A96A'
ORANGE = '#F08A24'
WATER = '#6CC5E8'
SOIL = '#123A2C'
DARK = '#0A241B'
GREY = '#9BC0A8'

CSS = """
@font-face{font-family:'Inter';src:url('fonts/Inter-400.ttf');font-weight:400}
@font-face{font-family:'Inter';src:url('fonts/Inter-700.ttf');font-weight:700}
@font-face{font-family:'Inter';src:url('fonts/Inter-800.ttf');font-weight:800}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:Inter,system-ui,sans-serif;background:#0B2A1F;color:#F4EBD9}
.slide{position:relative;width:1080px;height:1350px;padding:70px 84px 0;
  background:linear-gradient(180deg,#17452F 0%,#0E2E22 38%,#123A2C 66%,#123A2C 100%);
  display:flex;flex-direction:column;overflow:hidden}
.top{display:flex;justify-content:space-between;align-items:center;font-size:25px;letter-spacing:.16em;
  text-transform:uppercase;color:#9BC0A8;font-weight:700;flex:none}
.top .dot{width:13px;height:13px;border-radius:50%;background:#F08A24;display:inline-block;margin-right:14px;vertical-align:middle}
.num{font-size:118px;font-weight:800;color:#F08A24;line-height:.9;letter-spacing:-.03em;margin-top:18px}
h1{font-size:86px;line-height:1.0;font-weight:800;letter-spacing:-.03em;text-transform:uppercase;margin-top:4px}
h1.small{font-size:64px;margin-top:26px}
.sub{margin-top:20px;font-size:32px;line-height:1.34;color:#D3E3D8;font-weight:400;max-width:870px}
.badge{display:inline-block;margin-top:20px;padding:13px 24px;border:3px solid #F08A24;border-radius:999px;
  color:#F7C98A;font-size:25px;font-weight:700}
.art{margin:34px -84px 0;width:calc(100% + 168px);flex:none}
.art svg{display:block;width:100%;height:auto}
.big{font-size:80px;line-height:1.08;font-weight:800;text-transform:uppercase;letter-spacing:-.03em;margin-top:16px}
.accent{color:#F08A24}
"""


def slide(name, top_right, body):
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="slide">
<div class="top"><div><span class="dot"></span>САД · ПОЛИВ</div><div>{top_right}</div></div>
{body}
</div></body></html>"""
    (OUT / f'{name}.html').write_text(html, encoding='utf-8')


def ground(y, h):
    """Почва: полоса + редкая штриховка."""
    return f"""
  <rect x="0" y="{y}" width="912" height="{h}" fill="{SOIL}"/>
  <line x1="0" y1="{y}" x2="912" y2="{y}" stroke="#3C7A5B" stroke-width="5"/>
  <g stroke="#1D4E3A" stroke-width="3" opacity=".45">
    <line x1="48" y1="{y+90}" x2="210" y2="{y+90}"/><line x1="700" y1="{y+140}" x2="870" y2="{y+140}"/>
    <line x1="70" y1="{y+250}" x2="230" y2="{y+250}"/><line x1="690" y1="{y+300}" x2="860" y2="{y+300}"/>
  </g>"""


def sprout(x, y, s=1.0):
    """Росток: стебель и три листа."""
    return f"""
  <path d="M{x} {y} L{x} {y-90*s}" stroke="#8B5A2B" stroke-width="8" stroke-linecap="round"/>
  <path d="M{x} {y-92*s} C {x-44*s} {y-112*s}, {x-46*s} {y-152*s}, {x-6*s} {y-158*s} C {x-2*s} {y-126*s}, {x-3*s} {y-108*s}, {x} {y-92*s} Z" fill="#3E8A6A"/>
  <path d="M{x} {y-96*s} C {x+46*s} {y-118*s}, {x+48*s} {y-160*s}, {x+8*s} {y-166*s} C {x+3*s} {y-132*s}, {x+2*s} {y-114*s}, {x} {y-96*s} Z" fill="#4A9A77"/>
  <path d="M{x} {y-130*s} C {x-32*s} {y-158*s}, {x-34*s} {y-190*s}, {x-4*s} {y-196*s} C {x+2*s} {y-166*s}, {x+1*s} {y-148*s}, {x} {y-130*s} Z" fill="#347A5D"/>"""


def roots(x, y, h=210, w=160, sw=7):
    """Ветвящаяся корневая система: плавные дуги + короткие ответвления."""
    return f"""
  <g stroke="{SAND}" fill="none" stroke-linecap="round" opacity=".95">
    <path d="M{x} {y} C {x-w*.05} {y+h*.35}, {x-w*.3} {y+h*.55}, {x-w*.55} {y+h*.92}" stroke-width="{sw+2}"/>
    <path d="M{x} {y} C {x+w*.08} {y+h*.32}, {x+w*.34} {y+h*.6}, {x+w*.6} {y+h*.96}" stroke-width="{sw+1}"/>
    <path d="M{x} {y+10} C {x-w*.26} {y+h*.18}, {x-w*.58} {y+h*.3}, {x-w*.86} {y+h*.44}" stroke-width="{sw-1}"/>
    <path d="M{x} {y+14} C {x+w*.3} {y+h*.2}, {x+w*.62} {y+h*.34}, {x+w*.9} {y+h*.52}" stroke-width="{sw-1}"/>
    <path d="M{x} {y+22} C {x-w*.02} {y+h*.5}, {x-w*.1} {y+h*.74}, {x-w*.16} {y+h*1.02}" stroke-width="{sw-2}"/>
    <path d="M{x-w*.62} {y+h*.34} C {x-w*.7} {y+h*.42}, {x-w*.74} {y+h*.48}, {x-w*.76} {y+h*.54}" stroke-width="{sw-3}"/>
    <path d="M{x+w*.66} {y+h*.4} C {x+w*.74} {y+h*.48}, {x+w*.78} {y+h*.54}, {x+w*.8} {y+h*.62}" stroke-width="{sw-3}"/>
  </g>"""


def pipe(x, y1, y2, w=52, holes=None, cap=True):
    holes = holes or []
    h = "".join(f'<circle cx="{x+w/2}" cy="{cy}" r="6" fill="{DARK}"/>' for cy in holes)
    capr = f'<rect x="{x}" y="{y1}" width="{w}" height="24" rx="8" fill="#94AAB2"/>' if cap else ''
    return f"""
  <rect x="{x}" y="{y1}" width="{w}" height="{y2-y1}" rx="10" fill="#CBD8DC" stroke="{DARK}" stroke-width="5"/>
  {capr}
  <g opacity=".85">{h}</g>"""


def dim(x, y1, y2, label, unit='см', fs=54, side='left'):
    tx = x-22 if side == 'left' else x+22
    anchor = 'end' if side == 'left' else 'start'
    return f"""
  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{ORANGE}" stroke-width="5"/>
  <path d="M{x-12} {y1+14} L{x} {y1-8} L{x+12} {y1+14}" fill="{ORANGE}"/>
  <path d="M{x-12} {y2-14} L{x} {y2+8} L{x+12} {y2-14}" fill="{ORANGE}"/>
  <text x="{tx}" y="{(y1+y2)/2}" fill="{ORANGE}" font-family="Inter" font-size="{fs}" font-weight="800" text-anchor="{anchor}">{label}</text>
  <text x="{tx}" y="{(y1+y2)/2+34}" fill="{ORANGE}" font-family="Inter" font-size="27" font-weight="700" text-anchor="{anchor}">{unit}</text>"""


def label(x, y, text, tx=None, ty=None, anchor='start', size=25):
    """Выноска: текст + тонкая линия к точке."""
    tx = x if tx is None else tx
    ty = y if ty is None else ty
    line = f'<line x1="{tx}" y1="{ty}" x2="{x}" y2="{y}" stroke="{GREY}" stroke-width="3" opacity=".8"/>' if (tx, ty) != (x, y) else ''
    return f"""{line}
  <circle cx="{x}" cy="{y}" r="5" fill="{GREY}"/>
  <text x="{tx + (12 if anchor=='start' else -12)}" y="{ty-14}" fill="{GREY}" font-family="Inter" font-size="{size}" font-weight="700" text-anchor="{anchor}">{text}</text>"""


def mulch(x1, x2, y, text='мульча'):
    """Слой мульчи: полоса щепы на линии почвы + подпись."""
    chips = []
    x = x1
    import random
    random.seed(7)
    while x < x2:
        wch = random.randint(16, 30)
        chips.append(f'<rect x="{x}" y="{y-random.randint(6,12)}" width="{wch}" height="7" rx="3" fill="{SAND}" opacity=".85"/>')
        x += wch + random.randint(6, 14)
    return f"""
  <rect x="{x1}" y="{y-4}" width="{x2-x1}" height="8" fill="{SAND}" opacity=".25"/>
  {''.join(chips)}
  <text x="{x1-4}" y="{y-42}" fill="{GREY}" font-family="Inter" font-size="25" font-weight="700">{text}</text>"""


# ---------- 1. хук ----------
S1 = f"""
<h1 style="margin-top:52px">Поливай<br>не под ствол,<br>а <span class="accent">в трубу</span></h1>
<div class="sub">4 шага, чтобы саженец пережил первую засуху. Схема для дачи и сада.</div>
<div class="badge">на шаге 3 ошибаются чаще всего</div>
<div class="art">
<svg viewBox="0 0 912 540" xmlns="http://www.w3.org/2000/svg">
{ground(150, 390)}
  {sprout(248, 238, 1.15)}
  {roots(248, 238, 200, 130)}
  {pipe(470, 96, 486, 58, [170, 206, 242, 278, 314, 350, 386, 422], cap=True)}
  <path d="M472 452 C 430 500, 380 486, 344 438" stroke="{WATER}" stroke-width="8" fill="none" stroke-dasharray="14 11"/>
  <path d="M352 458 L326 434 L360 424" fill="{WATER}"/>
</svg>
</div>
"""

# ---------- 2. яма ----------
S2 = f"""
<div class="num">01</div>
<h1>Яма<br>60 см</h1>
<div class="sub">Глубже, чем шире. Корень должен тянуться вниз, а не стелиться под газоном.</div>
<div class="art">
<svg viewBox="0 0 912 640" xmlns="http://www.w3.org/2000/svg">
{ground(90, 550)}
  <rect x="366" y="90" width="190" height="490" fill="{DARK}" stroke="#4C8A6A" stroke-width="4" stroke-dasharray="10 8"/>
  <path d="M461 96 L461 470" stroke="#8B5A2B" stroke-width="12" stroke-linecap="round"/>
  <ellipse cx="461" cy="480" rx="74" ry="54" fill="#2E6049" opacity=".55"/>
  {roots(461, 486, 86, 62, 5)}
  {dim(316, 90, 560, '60')}
</svg>
</div>
"""

# ---------- 3. труба ----------
S3 = f"""
<div class="num">02</div>
<h1>Труба<br>у кома</h1>
<div class="sub">Перфорированная ПВХ на 50 см. Вплотную к корневому кому, а не вместо него.</div>
<div class="art">
<svg viewBox="0 0 912 640" xmlns="http://www.w3.org/2000/svg">
{ground(90, 550)}
  <path d="M330 96 L330 462" stroke="#8B5A2B" stroke-width="12" stroke-linecap="round"/>
  <ellipse cx="330" cy="472" rx="78" ry="56" fill="#2E6049" opacity=".55"/>
  {roots(330, 468, 120, 86, 5)}
  {pipe(486, 110, 520, 56, [180, 216, 252, 288, 324, 360, 396, 432, 468])}
  {dim(620, 110, 520, '50', side='right')}
  
  <line x1="414" y1="440" x2="486" y2="440" stroke="{GREY}" stroke-width="3" stroke-dasharray="8 8" opacity=".9"/>
</svg>
</div>
"""

# ---------- 4. гравий ----------
S4 = f"""
<div class="num">03</div>
<h1>Гравий<br>в трубу</h1>
<div class="sub">Щебень держит канал открытым: стенки не заплывают землёй, вода проходит годами.</div>
<div class="art">
<svg viewBox="0 0 912 640" xmlns="http://www.w3.org/2000/svg">
{ground(90, 550)}
  <path d="M440 8 L440 84" stroke="{WATER}" stroke-width="10" stroke-linecap="round"/>
  <path d="M413 78 L440 112 L467 78" fill="{WATER}"/>
  <rect x="326" y="104" width="228" height="470" rx="14" fill="{DARK}" stroke="#CBD8DC" stroke-width="8"/>
  <g fill="none" stroke="{SAND}" stroke-width="4" opacity=".9">
    <circle cx="366" cy="168" r="21"/><circle cx="420" cy="156" r="24"/><circle cx="480" cy="172" r="19"/>
    <circle cx="390" cy="218" r="23"/><circle cx="450" cy="214" r="20"/><circle cx="510" cy="228" r="17"/>
    <circle cx="362" cy="270" r="19"/><circle cx="424" cy="276" r="24"/><circle cx="488" cy="272" r="20"/>
    <circle cx="392" cy="330" r="22"/><circle cx="456" cy="334" r="23"/><circle cx="516" cy="340" r="17"/>
    <circle cx="366" cy="390" r="19"/><circle cx="430" cy="396" r="23"/><circle cx="494" cy="392" r="18"/>
    <circle cx="398" cy="452" r="22"/><circle cx="462" cy="456" r="19"/>
    <circle cx="370" cy="510" r="18"/><circle cx="434" cy="514" r="21"/>
  </g>
  {label(554, 200, 'щебень', tx=620, ty=200, anchor='start')}
</svg>
</div>
"""

# ---------- 5. вода и мульча ----------
S5 = f"""
<div class="num">04</div>
<h1>Вода<br>и мульча</h1>
<div class="sub">Льёшь прямо в трубу, сверху закрываешь. Влага идёт к корням, а не испаряется.</div>
<div class="art">
<svg viewBox="0 0 912 640" xmlns="http://www.w3.org/2000/svg">
{ground(90, 550)}
  {mulch(110, 420, 90)}
  <path d="M250 96 L250 470" stroke="#8B5A2B" stroke-width="12" stroke-linecap="round"/>
  <ellipse cx="250" cy="480" rx="76" ry="54" fill="#2E6049" opacity=".55"/>
  {roots(250, 476, 130, 92, 5)}
  {pipe(470, 110, 540, 54, [176, 212, 248, 284, 320, 356, 392, 428, 464])}
  <path d="M497 10 L497 92" stroke="{WATER}" stroke-width="10" stroke-linecap="round"/>
  <path d="M470 86 L497 120 L524 86" fill="{WATER}"/>
  <g fill="{WATER}">
    <circle cx="497" cy="146" r="6"/><circle cx="470" cy="170" r="5"/><circle cx="520" cy="176" r="4"/>
  </g>
  
</svg>
</div>
"""

# ---------- 6. схема ----------
S6 = f"""
<h1 class="small">Схема целиком</h1>
<div class="big">Корни вниз<br><span class="accent">50+ см</span></div>
<div class="sub">Сохрани, чтобы не искать в сезон посадки.</div>
<div class="art">
<svg viewBox="0 0 912 610" xmlns="http://www.w3.org/2000/svg">
{ground(80, 530)}
  {mulch(96, 392, 80)}
  <path d="M286 86 L286 186" stroke="#8B5A2B" stroke-width="12" stroke-linecap="round"/>
  {roots(286, 186, 320, 190)}
  {pipe(478, 100, 480, 52, [164, 200, 236, 272, 308, 344, 380, 416])}
  {dim(588, 100, 480, '50+', fs=46, side='right')}
  
</svg>
</div>
"""

for i, body in enumerate([S1, S2, S3, S4, S5, S6], 1):
    slide(f'slide{i}', f'0{i} / 06', body)

print('html готов:', len(list(OUT.glob('slide*.html'))))
