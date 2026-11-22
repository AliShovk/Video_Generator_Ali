---
name: youtube-shorts-pipeline
description: Полный процесс Shorts: YouTube Scout → исследование → русский сценарий и SVG-сцены → Video Generator Ali → MP4.
---

# YouTube Shorts Pipeline

1. Создай уникальный RUN_DIR в /root/youtube-intelligence/runs/<slug>-<timestamp>.
2. Запусти YouTube Research Agent. Он должен выполнить Scout и создать research.json, research_report.md, handoff.json. Если API key отсутствует или Scout завершился ошибкой — остановись, не выдумывай данные.
3. Передай три файла YouTube Script Agent. Он выбирает концепцию, создаёт пять хуков, сценарий, новый проект yt-<slug> через vg.py new --from solarfence, проектные voice.py и build.py, затем выполняет штатные voice/build/render/final --reels.
4. Успех только если MP4 существует, ffprobe подтверждает 1080×1920, аудио есть, длительность 20–35 секунд.
5. Верни концепцию, два лучших хука, сценарий, ссылки на референсы, MP4, папку исходников и отчёт проверки.

Не загружай на YouTube, не запускай vg push, не копируй в /var/www, не меняй vg.py, AGENTS.md, основной README, outro и чужие проекты.

Если тема требует фотореалистичных кадров, которых нет в SVG/GSAP-генераторе, сообщи о необходимости отдельного image/video-generation этапа.
