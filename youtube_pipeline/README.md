# YouTube Shorts Intelligence — Video Generator Ali

Интеграция для AliShovk/Video_Generator_Ali.

## Архитектура
1. YouTube Research Agent — YouTube Scout, публичная аналитика, outlier-видео, доступные транскрипты и комментарии.
2. YouTube Script & Production Agent — методики youtube-agent-skill, русские сценарии, проектные voice.py и build.py.
3. Video Generator Ali — HyperFrames + HTML/SVG + GSAP + Silero TTS + FFmpeg.

Новый проект создаётся отдельно на основе solarfence с именем yt-<slug>. Основной vg.py и другие проекты не меняются.

## Установка
Из корня клона:
~~~bash
bash youtube_pipeline/install.sh
~~~

Требуется Python 3.10+, git, YouTube Data API v3 key, ffmpeg/ffprobe, Node.js, HyperFrames и рабочий локальный TTS bridge /root/tts-bridge.

Ключ из Google Cloud Console сохранить в ~/.config/scout/.env:
YOUTUBE_API_KEY=...
Права: chmod 600 ~/.config/scout/.env. Не добавлять ключ в Git.

## Проверка Scout
~~~bash
source ~/youtube-intelligence/pipeline.env
python3 ~/youtube-intelligence/bin/scout_to_research.py --topic "инженерные эксперименты" --run-dir ~/youtube-intelligence/runs/test-001 --since month --max 30 --comments 5 --hooks 12
~~~
Выход: research.json, scout-research.xlsx. Research Agent дополнительно пишет research_report.md и handoff.json.

## Рендер
~~~bash
python3 /root/video-gen/vg.py new yt-example --from solarfence
python3 /root/video-gen/vg.py voice yt-example
python3 /root/video-gen/vg.py build yt-example
python3 /root/video-gen/vg.py render yt-example high
python3 /root/video-gen/vg.py final yt-example --reels
~~~
Файл: /root/video-gen/yt-example-final.mp4. --reels нужен для отключения стандартной 5,8-секундной концовки и нормализации -14 LUFS. Не вызывай vg make --reels: она создаёт Instagram metadata.

## Ограничения
- Scout --length short — фильтр до 4 минут, не доказательство Shorts. Проверка: Format=Short, Vertical=true, duration <=180s.
- Публичные данные конкурентов не раскрывают impressions, CTR и приватное удержание.
- Hook score — эвристика, не predictor.
- SVG/GSAP генератор не является text-to-video и не создаёт фотореалистичные AI-сцены.
- Автопубликация, vg push и production deploy отключены.

Источники:
- https://github.com/AgriciDaniel/youtube-scout (MIT)
- https://github.com/Jakeschincariol/youtube-agent-skill (MIT)
