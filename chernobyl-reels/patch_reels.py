from pathlib import Path

# --- 1. сцены: длительности под Reels
p = Path('/root/video-gen/chernobyl-reels/make_scenes.py')
s = p.read_text(encoding='utf-8')
s = s.replace('("s1", scene1(), 5),', '("s1", scene1(), 5),')
s = s.replace('("s2", scene2(), 8),', '("s2", scene2(), 7),')
s = s.replace('("s3", scene3(), 10),', '("s3", scene3(), 7),')
s = s.replace('("s4", scene4(), 12),', '("s4", scene4(), 8),')
s = s.replace('("s5", scene5(), 11),', '("s5", scene5(), 8),')
s = s.replace('("s6", scene6(), 8),', '("s6", scene6(), 7),')
s = s.replace('("s7", scene7(), 6),', '("s7", scene7(), 5),')
p.write_text(s, encoding='utf-8')

# --- 2. типографика в безопасной зоне Reels (низ ~420 px занят интерфейсом)
b = Path('/root/video-gen/chernobyl-reels/build_scenes.py')
t = b.read_text(encoding='utf-8')
t = t.replace('''    .foot {{
      position: absolute; left: 56px; right: 56px; bottom: 230px;
      font: 700 52px/1.12 "Oswald", sans-serif; text-transform: uppercase; color: #f1ece2;
      text-shadow: 0 4px 18px rgba(0,0,0,0.8);
    }}''','''    .foot {{
      position: absolute; left: 48px; right: 48px; bottom: 430px;
      font: 700 50px/1.1 "Oswald", sans-serif; text-transform: uppercase; color: #f6f1e7;
      text-shadow: 0 3px 14px rgba(0,0,0,0.9);
    }}''')
t = t.replace('''    .head {{
      position: absolute; left: 56px; top: 210px;''','''    .head {{
      position: absolute; left: 48px; top: 230px;''')
t = t.replace('''    .top {{ position: absolute; left: 56px; top: 136px; }}''','''    .top {{ position: absolute; left: 48px; top: 120px; }}''')
b.write_text(t, encoding='utf-8')

# --- 3. index.html: новые длительности
idx = Path('/root/video-gen/chernobyl-reels/index.html')
h = idx.read_text(encoding='utf-8')
starts = {'s1': (0, 5), 's2': (5, 7), 's3': (12, 7), 's4': (19, 8), 's5': (27, 8), 's6': (35, 7), 's7': (42, 5)}
import re
for sid, (st, du) in starts.items():
    h = re.sub(rf'(id="{sid}"[^>]*data-start=")\d+(" data-duration=")\d+(")', rf'\g<1>{st}\g<2>{du}\g<3>', h)
h = h.replace('data-duration="60"', 'data-duration="47"')
idx.write_text(h, encoding='utf-8')
print('ok')
