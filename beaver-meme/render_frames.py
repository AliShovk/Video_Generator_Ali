#!/usr/bin/env python3
"""Мем-ролик 9:16: картинка «боберштыль» + зум, тряска, подписи. Кадры -> PNG."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path('/root/video-gen/beaver-meme')
FR = OUT / 'frames'
FR.mkdir(parents=True, exist_ok=True)
if __name__ == '__main__':
    for f in list(FR.glob('*.png')) + list(FR.glob('*.jpg')):
        f.unlink()

W, H = 1080, 1920
FPS = 30
DUR = 21.0
N = int(DUR * FPS)
LANCZOS = Image.LANCZOS

SRC = Image.open('/root/.hermes/cache/images/img_4cbd80196bc1.jpg').convert('RGB')
SRC = SRC.crop((0, 58, SRC.width, SRC.height))
FONTS = Path('/root/video-gen/carousel-irrigation/fonts')
f800 = lambda s: ImageFont.truetype(str(FONTS / 'Inter-800.ttf'), s)
f700 = lambda s: ImageFont.truetype(str(FONTS / 'Inter-700.ttf'), s)

# фон
bg = SRC.resize((int(W * 1.6), int(W * 1.6 * SRC.height / SRC.width)), LANCZOS)
bg = bg.filter(ImageFilter.GaussianBlur(26))
bw, bh = bg.size
bg = bg.crop(((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W, (bh - H) // 2 + H))
bg = Image.blend(bg, Image.new('RGB', (W, H), (18, 13, 8)), 0.62)

PIC_W = 1000
PIC_H = int(PIC_W * SRC.height / SRC.width)

SEGS = [
    (0.5, 3.4, 'БЕНЗОПИЛА', 'изобретена до бензина', True),
    (3.4, 5.6, '', 'Задолго до бензина.', False),
    (5.6, 9.2, '', 'Вместо двигателя — четыре бобра.', False),
    (9.2, 12.4, '', 'Ручка, ремень, и пила готова.', False),
    (12.4, 15.4, 'БОБЕРШТЫЛЬ', 'пила первобытная, 4 л.с.', True),
    (15.4, 16.4, '', 'Пилит тише бензопилы.', False),
    (16.4, 18.0, '', '...но дерево всё равно падает.', False),
    (18.0, 21.0, 'ПОДПИШИСЬ', 'если тоже инженер', True),
]


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease_out(x):
    return 1 - (1 - x) ** 3


def seg_alpha(t, t0, t1):
    return min(clamp((t - t0) / 0.3), clamp((t1 - t) / 0.25))


def make_frame(i):
    t = i / FPS
    img = bg.copy()

    zoom = 1.0 + 0.10 * (t / DUR)
    if 12.6 <= t < 15.4:
        zoom += 0.07 * ease_out(clamp((t - 12.6) / 0.6))
    shake = 14 * (1 - (t - 16.4)) if 16.4 <= t < 17.4 else 0.0
    dx = int(math.sin(t * 90) * shake)
    dy = int(math.cos(t * 70) * shake * 0.7)

    sw = int(SRC.width / zoom)
    sh = int(SRC.height / zoom)
    x0 = (SRC.width - sw) // 2
    y0 = (SRC.height - sh) // 2
    pic = SRC.crop((x0, y0, x0 + sw, y0 + sh)).resize((PIC_W, PIC_H), LANCZOS)

    px = (W - PIC_W) // 2 + dx
    py = 384 + dy

    # рамка
    d0 = ImageDraw.Draw(img)
    d0.rounded_rectangle([px - 16, py - 16, px + PIC_W + 16, py + PIC_H + 16], 20, fill=(236, 226, 206))
    d0.rounded_rectangle([px - 6, py - 6, px + PIC_W + 6, py + PIC_H + 6], 12, outline=(58, 42, 26), width=5)
    img.paste(pic, (px, py))

    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    for (t0, t1, title, sub, big) in SEGS:
        if not (t0 <= t < t1):
            continue
        a = seg_alpha(t, t0, t1)
        if a <= 0.02:
            continue
        if title:
            d.rectangle([0, 0, W, 360], fill=(12, 8, 4, int(150 * a)))
            fs = 120 if big else 96
            if len(title) > 8: fs = 92
            while fs > 48 and d.textlength(title, font=f800(fs)) > W - 130:
                fs -= 2
            d.text((W // 2, 190), title, font=f800(fs), fill=(247, 238, 222, int(255 * a)),
                   anchor='mm', stroke_width=6, stroke_fill=(15, 10, 6, int(255 * a)))
            d.text((W // 2, 306), sub, font=f700(40), fill=(236, 206, 156, int(255 * a)),
                   anchor='mm', stroke_width=5, stroke_fill=(15, 10, 6, int(255 * a)))
        else:
            fnt = f700(46)
            tw = d.textlength(sub, font=fnt)
            half = tw / 2 + 38
            d.rounded_rectangle([W // 2 - half, 1348, W // 2 + half, 1460], 26,
                                fill=(15, 10, 6, int(205 * a)))
            d.text((W // 2, 1404), sub, font=fnt, fill=(247, 238, 222, int(255 * a)), anchor='mm')

    # верхний кикер
    ka = int(150 * clamp((t - 0.3) / 0.5))
    if ka > 0:
        d.text((W // 2, 120), 'ПЕРВОБЫТНЫЕ ТЕХНОЛОГИИ', font=f700(26), fill=(190, 170, 140, ka), anchor='mm')
        d.rectangle([W // 2 - 40, 164, W // 2 + 40, 168], fill=(224, 122, 42, ka))

    # фичи
    fa = clamp((t - 3.6) / 0.5)
    if fa > 0.02:
        feats = ['не требует бензина', 'тише бензопилы', 'расход: 2 бобра в смену']
        for j, ftxt in enumerate(feats):
            yy = 1520 + j * 84
            a2 = int(235 * fa)
            d.ellipse([120, yy - 22, 164, yy + 22], fill=(224, 122, 42, a2))
            d.line([132, yy, 142, yy + 11, 154, yy - 9], fill=(20, 14, 8, a2), width=6)
            d.text((186, yy), ftxt, font=f700(40), fill=(240, 230, 214, a2), anchor='lm')

    # прогресс
    k = t / DUR
    d.rounded_rectangle([120, H - 98, W - 120, H - 90], 4, fill=(255, 255, 255, 40))
    d.rounded_rectangle([120, H - 98, 120 + int((W - 240) * k), H - 90], 4, fill=(224, 122, 42, 220))

    img = Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')
    img.save(FR / f'f_{i:04d}.jpg', quality=92)


if __name__ == '__main__':
    import sys
    only = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else None
    if only:
        for i in only:
            make_frame(i)
        print('test frames', only)
    else:
        for i in range(N):
            make_frame(i)
            if i % 60 == 0:
                print('frame', i, '/', N, flush=True)
        print('done', N)
