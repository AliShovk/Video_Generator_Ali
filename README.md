# Video Generator Ali

Генератор вертикальных роликов **1080×1920 (9:16), 30 fps** для канала MasterHacks: сцены — HTML/SVG + GSAP, рендер — HyperFrames, озвучка — локальный Silero TTS, в конце каждого ролика приклеивается общая концовка.

## Что внутри

- `vg.py` — единая CLI (`vg list|new|voice|build|render|final|make|push`)
- `<проект>/voice.py` — сценарий + синтез озвучки → `voice.wav`, `timings.json`
- `<проект>/build.py` — генератор сцен → `compositions/*.html`, `index.html`
- `scripts/append_outro.py` — нормализация в 1080×1920/30 fps и склейка с концовкой
- `assets/outro/outro.mp4` — утверждённая концовка (5,8 с, карточка «Gaid» + озвучка)
- 60+ готовых проектов-примеров (шахта, цунами, «Титаник», солнечный насос и т.д.)

## Установка

```bash
npm i                     # hyperframes и зависимости рендера
# нужны: ffmpeg, python3 + Pillow, локальный TTS-мост /root/tts-bridge (127.0.0.1:8123)
```

## Быстрый старт

```bash
vg list                            # что уже собрано
vg new myclip --from solarfence    # шаблон нового ролика
# правим myclip/voice.py (текст) и myclip/build.py (сцены)
vg make myclip                     # озвучка → сцены → рендер → звук → концовка
```

По шагам:

```bash
vg voice myclip
vg build myclip
vg render myclip high
vg final myclip
vg push                            # залить исходники в GitHub
```

Для Instagram Reels:

```bash
vg make myclip --reels             # без 5,8 с концовки, звук -14 LUFS, сразу instagram.md
vg meta myclip                     # подпись, хештеги, UTM-ссылка на qantcore, проверка хука
```

Правила сценария и воронки на сайт — `AGENTS.md`.

## Второй движок: Animation Studio (рисованные ролики + музыка кодом)

`engines/animation-studio/` — вендоренный движок `i-afaqrashid/claude-animation-studio` (v1.0.1): каждый кадр рисуется кодом на canvas, музыка синтезируется в JS, один `score.js` синхронизирует картинку и звук. Выход 1080p MP4 в 16:9, 9:16, 1:1 или 4:5. Зависимостей нет: Node 22+, ffmpeg, Chrome.

```bash
vg studio list
vg studio new myclip --format 9:16 --from app-promo   # стартовые точки: app-promo, product-launch, lyric-video, birthday-card, wedding-invite, gully-cricket, qawwali-night, world-cup-2026
vg studio make myclip --draft                          # музыка + draft-рендер + склейка (~2 мин на 20 с)
vg studio make myclip                                  # финал в полном разрешении
vg studio render myclip verify                         # замер синхро-точек, звука и картинки
vg studio outro myclip                                 # приклеить утверждённую концовку MasterHacks
```

Стиль канала: `vg studio render myclip video --style flat`. Полный API движка — `engines/animation-studio/SKILL.md`.

## Правила стиля (утверждены)

- 9:16, 1080×1920, 30 fps, 25–35 с контента + 5,8 с концовки.
- Яркая плоская иллюстрация: тёплое небо-градиент, насыщенная трава, контур 4 px, крупный заголовок слева в две строки.
- Движение в каждом кадре: лучи, блики, искры по кабелю, качание травы, вращение механизмов.
- Хук в первые 1,5 секунды, крупный текст 70–110 px, петля в конце.
- Название без хештегов, 12–18 тегов — в описании.

## Требования к сцене

- Каждая сцена — отдельный HTML в `<template>`, регистрирует `window.__timelines["<id>"]`.
- Таймлайн только `paused: true`, анимации через `fromTo`.
- Не анимировать `rotate` на `<g>` со своим `transform` — GSAP перезапишет и объект улетит в угол.

## Лицензия

Внутренний проект. Все права у владельца репозитория.
