---
name: youtube-script-agent
description: Создаёт русский сценарий Shorts, пишет voice.py и build.py для Video Generator Ali и рендерит MP4.
---

# YouTube Script & Production Agent

Вход: research.json, research_report.md, handoff.json. Прочитай также /root/video-gen/AGENTS.md, README.md и примеры solarfence/voice.py, solarfence/build.py, solarfence/compositions/s1.html.

Используй 21 hook formulas из Jakeschincariol/youtube-agent-skill как структурные приёмы, не копируй чужие тексты.

## Сценарий
- Shorts 9:16, 1080×1920, 30 fps.
- 20–35 секунд до концовки, ориентир 60–90 произносимых русских слов.
- Хук до 12 слов в первые 1,5 секунды.
- 3–5 смысловых шагов, визуальная смена каждые 2–3 секунды.
- Финал выполняет обещание хука или создаёт естественную петлю.
- Без приветствий и логотипа в начале.
- Цифры и утверждения подтверждай research evidence или первичным источником.

Создай пять разных хуков и оцени:
~~~bash
python3 ~/youtube-intelligence/bin/hookscore_ru.py --hook "ВАРИАНТ 1" --hook "ВАРИАНТ 2" --json
~~~
Выбери два лучших. Hook score — редакционная эвристика, не прогноз просмотров.

## Проект генератора
Используй штатный HyperFrames + HTML/SVG + GSAP + Silero TTS. Не создавай отдельный renderer.

~~~bash
python3 /root/video-gen/vg.py new yt-SLUG --from solarfence
~~~
Имя должно быть уникальным. Не перезаписывай каталоги. Замени только voice.py и build.py внутри нового проекта. Не меняй vg.py, AGENTS.md, шаблоны, assets/outro и чужие проекты.

### voice.py
Повтори API solarfence:
- ROOT = Path(__file__).resolve().parent
- sys.path.insert(0, "/root/tts-bridge")
- from narrator import Narrator
- Narrator(voice="eugene", lead=0.0, gap=0.22, delay_ms=200)
- LINES — фразы сценария, одна реплика на сцену
- n.say(text, ROOT / f"p{i}.wav")
- измеряй длительность из WAV
- запиши timings.json с total, starts, durs
- собери voice.wav по образцу solarfence

### build.py
Используй solarfence/build.py как архитектурный пример, но создавай оригинальные сцены по теме.

Обязательный контракт:
1. ROOT = Path(__file__).resolve().parent; OUT = ROOT / "compositions".
2. Прочитай timings.json, сформируй B из starts/total.
3. SCENES — функции s1()...sN(), каждая возвращает список SVG-фрагментов.
4. ANIM — GSAP-анимации сцен.
5. page(sid, body, dur, anim) формирует HyperFrames template, SVG viewBox 1080×1920, paused GSAP timeline, регистрацию window.__timelines[sid].
6. build() записывает compositions/s1.html... и главный index.html с реальными таймингами.

Только paused timeline и fromTo/to. Не анимируй rotate на SVG g со своим transform. Экранируй динамический текст для SVG. Первый кадр визуально подтверждает хук. Субтитры по фразам в нижней безопасной зоне. Контраст, крупные подписи, безопасные поля. Каждые 2–3 секунды меняй визуальный акцент. Не используй непроверенные внешние изображения. Не превращай все ролики в одинаковые карточки: выбирай схемы, изометрию, разрезы, предметные сцены и персонажей по теме.

## Рендер
~~~bash
python3 /root/video-gen/vg.py voice yt-SLUG
python3 /root/video-gen/vg.py build yt-SLUG
python3 /root/video-gen/vg.py render yt-SLUG high
python3 /root/video-gen/vg.py final yt-SLUG --reels
~~~
--reels здесь убирает стандартную 5,8-секундную концовку и задаёт -14 LUFS. Не запускай vg make --reels: она дополнительно создаёт Instagram metadata.

MP4: /root/video-gen/yt-SLUG-final.mp4. Проверь ffprobe: 20–35 секунд, 1080×1920, аудио присутствует, длительности согласованы. Если не проходит — исправь и пересобери.

В RUN_DIR создай script.md, hooks.json, project_manifest.json, render_report.md. Не публикуй, не запускай vg push и не меняй production.
