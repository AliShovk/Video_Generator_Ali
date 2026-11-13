# ENGINEERING EXPLAINER GENERATOR

Конвейер для вертикальных инженерных роликов 1080×1920, 45–60 с: от брифа с проверенными
фактами до готового `final.mp4` с озвучкой и субтитрами.

```
brief.json
  → research.py      research.md         (факты, источники, ограничения)
  → engineering.py   engineering.md      (принцип, передача нагрузок, механизмы)
  → script.py        script.md           (хук + текст диктора)
  → storyboard.py    storyboard.json     (сцены, ракурсы, объекты)
  → factcheck.py     factcheck.json      (числа сверяются с research.md; иначе стоп)
  → visual.py        assets/             (SVG-слои, HTML-сцены HyperFrames)
  → voice.py         voice.wav, subtitles.srt, timings.json
  → pipeline.py      final.mp4           (FFmpeg: видео + голос + субтитры)
```

## Запуск

```bash
cd /root/video-gen/explainer
/usr/local/lib/hermes-agent/venv/bin/python pipeline.py briefs/chernobyl.json
# быстрый прогон без рендера:
/usr/local/lib/hermes-agent/venv/bin/python pipeline.py briefs/chernobyl.json --skip-render
```

Результат: `out/<slug>/` со всеми артефактами и `manifest.json`.

## Бриф

Обязательные поля: `slug, title, hook, principle, load_path[], flows[], details[],
facts[{id,value,unit,claim,source}], sources[]`; опционально `dims{span_m,height_m,length_m,weight_t}`.

Правило: **число попадает в озвучку только если оно есть в `facts`.** `factcheck` возвращает
exit code 2 и останавливает конвейер, если в тексте появилось неподтверждённое число или
длительность вышла за 45–60 с.

## Стиль

Тёмная техническая инфографика: сетка, стальные градиенты, циан `#6fd3f2`, оранжевый
акцент `#ff7a1a`. Подписи — JetBrains Mono, заголовки — Oswald. Текст держится выше
`bottom: 420px`, чтобы не попадать в интерфейс Reels.

## Расширение

- Новый тип сцены: функция в `visual.py` + запись в `BUILDERS`, `CAPTION`, `CHIP`, `ANIM`.
- Другая структура: `structure` в брифе + ветка в `agents.KIND_BY_SCENE`.
- Голос: Silero (`aidar`) с откатом на Piper (`ru_denis`) в `voice.py`.
