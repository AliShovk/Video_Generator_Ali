from pathlib import Path

p = Path('/root/video-gen/chernobyl-reels/make_scenes.py')
s = p.read_text(encoding='utf-8')

# ---------- s1: арка крупнее, блок уходит под неё
s = s.replace('''    b.append(ground(1560))
    b.append(reactor(350, 1560, 300, 210))
    b.append(arch(540, 1560, 760, 620, 54, ribs=22))''', '''    b.append(ground(1640))
    b.append(reactor(390, 1640, 300, 210))
    b.append(arch(540, 1640, 940, 800, 64, ribs=30))''')

# ---------- s3 и s4 переписаны
start3 = s.index('def scene3():')
end3 = s.index('def scene4():')
start4 = end3
end4 = s.index('def scene5():')

new3 = '''def scene3():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    # рамка площадки
    b.append('<rect x="80" y="520" width="920" height="980" fill="none" stroke="#1d3746" stroke-width="2"/>')
    for i in range(1, 6):
        b.append(f'<line x1="{80+i*153}" y1="520" x2="{80+i*153}" y2="1500" stroke="#0f1f2a" stroke-width="1"/>')
        b.append(f'<line x1="80" y1="{520+i*163}" x2="1000" y2="{520+i*163}" stroke="#0f1f2a" stroke-width="1"/>')
    # площадка сборки
    b.append('<rect x="150" y="1080" width="360" height="280" fill="rgba(111,211,242,0.05)" stroke="#6fd3f2" stroke-width="3" stroke-dasharray="14 10"/>')
    b.append(text(330, 1160, "СБОРКА", 34, "#8fd8ef", "middle"))
    b.append(text(330, 1210, "здесь арку собрали", 22, "#5f7280", "middle"))
    # реактор
    b.append('<circle cx="770" cy="760" r="92" fill="rgba(255,122,26,0.08)" stroke="#ff7a1a" stroke-width="3"/>')
    b.append(text(770, 750, "4", 46, "#ffb066", "middle"))
    b.append(text(770, 800, "БЛОК", 20, "#ffb066", "middle"))
    # путь
    b.append('<path d="M 512 1200 Q 640 1120 720 870" fill="none" stroke="#ff7a1a" stroke-width="7" stroke-dasharray="20 14"/>')
    b.append('<polygon points="726,852 706,890 744,884" fill="#ff7a1a"/>')
    b.append(text(560, 1330, "327 м", 40, "#ffb066", "middle"))
    # масштабная линейка
    b.append('<line x1="150" y1="1440" x2="390" y2="1440" stroke="#5f7280" stroke-width="3"/>')
    b.append('<line x1="150" y1="1430" x2="150" y2="1450" stroke="#5f7280" stroke-width="3"/>')
    b.append('<line x1="390" y1="1430" x2="390" y2="1450" stroke="#5f7280" stroke-width="3"/>')
    b.append(text(270, 1424, "100 м", 22, "#5f7280", "middle"))
    return svg("".join(b))


'''
new4 = '''def scene4():
    b = [f'<rect width="1080" height="1920" fill="#060a0e"/>']
    b.append(ground(1560))
    # рельс
    b.append('<rect x="0" y="1560" width="1080" height="30" fill="#2f3941"/>')
    b.append('<rect x="0" y="1548" width="1080" height="14" fill="#6b7d8a"/>')
    for x in range(30, 1080, 120):
        b.append(f'<rect x="{x}" y="1540" width="60" height="10" fill="#8b9aa6" opacity="0.65"/>')
    # нога арки (в разрезе)
    b.append('<path d="M 330 1548 L 330 760 Q 330 700 390 700 L 520 700 Q 580 700 580 760 L 580 1548 Z" fill="url(#steelDark)" stroke="#8b9aa6" stroke-width="4"/>')
    b.append('<path d="M 350 1548 L 350 780 L 560 780 L 560 1548 Z" fill="#151d24" opacity="0.55"/>')
    # домкраты
    for i, x in enumerate([610, 700, 790, 880]):
        b.append(f'<rect x="{x}" y="1400" width="72" height="148" fill="#243039" stroke="#6fd3f2" stroke-width="3"/>')
        b.append(f'<rect x="{x+10}" y="1330" width="52" height="76" fill="#3d4d59" stroke="#8fd8ef" stroke-width="2"/>')
        b.append(f'<line x1="{x+36}" y1="1330" x2="{x+36}" y2="1290" stroke="#ff7a1a" stroke-width="5"/>')
        b.append(f'<polygon points="{x+36},1262 {x+24},1292 {x+48},1292" fill="#ff7a1a"/>')
    b.append(text(756, 1636, "224 ДОМКРАТА", 26, "#8fd8ef", "middle"))
    # усилие
    b.append(text(540, 1120, "ТОЛКАЮТ ВПЕРЁД", 30, "#5f7280", "middle"))
    b.append('<path d="M 640 1170 L 930 1170" stroke="#ff7a1a" stroke-width="4" stroke-dasharray="12 10"/>')
    b.append('<polygon points="946,1170 918,1158 918,1182" fill="#ff7a1a"/>')
    return svg("".join(b))


'''
s = s[:start3] + new3 + new4 + s[end4:]

# scrim для читаемости подписей — добавим в build_scenes
p.write_text(s, encoding='utf-8')

b = Path('/root/video-gen/chernobyl-reels/build_scenes.py')
t = b.read_text(encoding='utf-8')
t = t.replace('''    .foot::before {{ content: ""; display: block; width: 74px; height: 4px; background: #ff7a1a; margin-bottom: 16px; }}''',
'''    .foot::before {{ content: ""; display: block; width: 74px; height: 4px; background: #ff7a1a; margin-bottom: 16px; }}
    .scrim {{
      position: absolute; left: 0; right: 0; bottom: 0; height: 640px;
      background: linear-gradient(to top, rgba(4,7,10,0.96) 34%, rgba(4,7,10,0.75) 62%, rgba(4,7,10,0) 100%);
    }}''')
t = t.replace('''        {body}
        <div class="top">''', '''        {body}
        <div class="scrim"></div>
        <div class="top">''')
b.write_text(t, encoding='utf-8')
print('ok')
