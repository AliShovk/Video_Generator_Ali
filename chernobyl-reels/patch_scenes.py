import re
from pathlib import Path

p = Path('/root/video-gen/chernobyl/make_scenes.py')
s = p.read_text(encoding='utf-8')

# паттерн панелей
s = s.replace('''  <pattern id="hatch"''', '''  <pattern id="panels" width="26" height="26" patternUnits="userSpaceOnUse">
    <rect width="26" height="26" fill="none"/>
    <line x1="0" y1="0" x2="0" y2="26" stroke="#0d151b" stroke-width="3" opacity="0.45"/>
    <line x1="0" y1="13" x2="26" y2="13" stroke="#0d151b" stroke-width="1.5" opacity="0.25"/>
  </pattern>
  <pattern id="hatch"''')

old_arch_start = s.index('def arch(')
old_arch_end = s.index('def reactor(')
new_arch = '''def arch(cx, base_y, span, height, thickness=46, fill="url(#steel)", ribs=26, opacity=1.0, panels=True):
    """Полуэллиптическая арка с ферменными рёбрами и панелями."""
    rx, ry = span / 2, height
    x0, x1 = cx - rx, cx + rx
    irx, iry = rx - thickness, ry - thickness * 0.92
    outer = f"M {x0} {base_y} A {rx} {ry} 0 0 1 {x1} {base_y}"
    inner = f"M {cx - irx} {base_y} A {irx} {iry} 0 0 1 {cx + irx} {base_y}"
    body = f"{outer} L {cx + irx} {base_y} A {irx} {iry} 0 0 0 {cx - irx} {base_y} Z"
    out = [f'<path d="{body}" fill="{fill}" opacity="{opacity}"/>']
    if panels:
        out.append(f'<path d="{body}" fill="url(#panels)" opacity="0.55"/>')
    # рёбра (радиальные линии по дуге)
    import math as _m
    for i in range(1, ribs):
        a = _m.pi * i / ribs
        ox, oy = cx - rx * _m.cos(a), base_y - ry * _m.sin(a)
        ix, iy = cx - irx * _m.cos(a), base_y - iry * _m.sin(a)
        out.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" stroke="#1a232b" stroke-width="{max(2, thickness*0.09):.1f}" opacity="0.65"/>')
    # раскосы между рёбрами
    for i in range(ribs - 1):
        a1 = _m.pi * i / ribs
        a2 = _m.pi * (i + 1) / ribs
        ox1, oy1 = cx - rx * _m.cos(a1), base_y - ry * _m.sin(a1)
        ix2, iy2 = cx - irx * _m.cos(a2), base_y - iry * _m.sin(a2)
        out.append(f'<line x1="{ox1:.1f}" y1="{oy1:.1f}" x2="{ix2:.1f}" y2="{iy2:.1f}" stroke="#22303a" stroke-width="2" opacity="0.45"/>')
    out.append(f'<path d="{outer}" fill="none" stroke="#c9d8e3" stroke-width="3.5" opacity="0.85"/>')
    out.append(f'<path d="{inner}" fill="none" stroke="#7f93a3" stroke-width="2" opacity="0.55"/>')
    # торцевые стойки
    for xx in (x0, x1):
        out.append(f'<rect x="{xx-6}" y="{base_y-40}" width="12" height="40" fill="#7f93a3" opacity="0.7"/>')
    return "".join(out)


'''
s = s[:old_arch_start] + new_arch + s[old_arch_end:]

# s2: убрать накладывающийся текст, оставить размеры
s = s.replace('''    b.append(text(540, 760, "СТАЛЬНАЯ АРКА", 34, "#cfdae4", "middle"))
    b.append(text(540, 812, "162 м в длину", 26, "#7f93a3", "middle"))''', '''    b.append(text(540, 640, "СТАЛЬНАЯ АРКА", 30, "#8f9aa4", "middle"))''')

# s5: сдвинуть заголовок, чтобы не пересекался
s = s.replace('''    b.append(text(540, 300, "327 МЕТРОВ", 64, "#e9e4da", "middle"))
    b.append(text(540, 360, "ЗА 2 НЕДЕЛИ, НОЯБРЬ 2016", 26, "#7f93a3", "middle"))''', '''    b.append(text(540, 470, "327 МЕТРОВ", 58, "#e9e4da", "middle"))
    b.append(text(540, 520, "ЗА ДВЕ НЕДЕЛИ, НОЯБРЬ 2016", 24, "#7f93a3", "middle"))''')

p.write_text(s, encoding='utf-8')
print('patched')
