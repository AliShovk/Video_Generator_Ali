from pathlib import Path

p = Path('/root/video-gen/chernobyl/make_scenes.py')
s = p.read_text(encoding='utf-8')

# --- s2: размеры выше, чтобы не лезли под подпись
s = s.replace('''    b.append(arch(540, 1480, 780, 640, 60, ribs=26))
    # размеры
    b.append(dim_h(150, 930, 1600, "257 м — пролёт"))
    b.append(dim_v(1480, 840, 985, "108 м"))
    b.append(f'<line x1="150" y1="1480" x2="985" y2="1480" stroke="#6fd3f2" stroke-width="1.5" opacity="0.35"/>')
    b.append(text(540, 640, "СТАЛЬНАЯ АРКА", 30, "#8f9aa4", "middle"))''','''    b.append(arch(540, 1440, 780, 640, 60, ribs=30))
    b.append(dim_h(150, 930, 1520, "257 м — пролёт"))
    b.append(dim_v(1440, 800, 1000, ""))
    b.append(f'<g transform="translate(1040 1120) rotate(90)">{text(0, 0, "108 м", 30, "#6fd3f2", "middle")}</g>')
    b.append(text(540, 640, "СТАЛЬНАЯ АРКА", 30, "#8f9aa4", "middle"))''')

# --- s5: без дублей текста, арка целиком в кадре
s = s.replace('''    b.append(arch(cx=300, base_y=1500, span=560, height=460, thickness=44, ribs=16))''', '''    b.append(arch(250, 1500, 420, 340, 38, ribs=18))''')
s = s.replace('''    b.append(f'<g id="arch-move">{arch(300, 1500, 560, 460, 44, ribs=16)}</g>')''', '''    b.append(f'<g id="arch-move">{arch(250, 1500, 420, 340, 38, ribs=18)}</g>')''')
s = s.replace('''    b.append(text(540, 470, "327 МЕТРОВ", 58, "#e9e4da", "middle"))
    b.append(text(540, 520, "ЗА ДВЕ НЕДЕЛИ, НОЯБРЬ 2016", 24, "#7f93a3", "middle"))''', '''    b.append(text(540, 760, "СБОРКА → РЕАКТОР", 26, "#7f93a3", "middle"))''')
# рельс по всей ширине
s = s.replace('''    # рельсы
    b.append('<rect x="0" y="1500" width="1080" height="18" fill="#39434c"/>')''','''    # рельсы
    b.append('<rect x="0" y="1500" width="1080" height="18" fill="#39434c"/>')
    for x in range(40, 1080, 90):
        b.append(f'<rect x="{x}" y="1494" width="46" height="8" fill="#5a6b78" opacity="0.7"/>')''')
p.write_text(s, encoding='utf-8')

# --- анимация s5: движение в кадре
b = Path('/root/video-gen/chernobyl/build_scenes.py')
t = b.read_text(encoding='utf-8')
t = t.replace('''tl_s5.fromTo("#arch-move", { x: -300 }, { x: 300, duration: 10.4, ease: "power1.inOut" }, 0.6);''',
              '''tl_s5.fromTo("#arch-move", { x: 0 }, { x: 430, duration: 9.6, ease: "power1.inOut" }, 0.8);''')
b.write_text(t, encoding='utf-8')
print('ok')
