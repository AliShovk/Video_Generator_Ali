#!/usr/bin/env python3
"""Пакет публикации Reels: проверка хука, подпись, UTM-ссылка, закреп-комментарий.

usage: reels_meta.py <project_dir>

Читает LINES из <project>/voice.py и необязательный <project>/reel.json:
  {"topic": "LM Studio", "page": "/product/lm-studio/", "keyword": "LM",
   "hashtags": ["нейросети", "ai"], "partner": "timeweb-cloud"}
Пишет <project>/instagram.md. Если заданы VG_LLM_BASE_URL и VG_LLM_API_KEY,
подпись дописывает модель (OpenAI-совместимый API, по умолчанию deepseek-v4.1-flash).
"""
import ast
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SITE = "https://qantcore.space"
HOOK_MAX_WORDS = 12
MAX_HASHTAGS = 5


def read_lines(voice_py: Path) -> list[str]:
    tree = ast.parse(voice_py.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "LINES" for t in node.targets):
            return [spoken(x) for x in ast.literal_eval(node.value)]
    return []


def spoken(item) -> str:
    """Строка или кортеж ("v1", start, end, ["фраза", ...]) -> произносимый текст."""
    if isinstance(item, str):
        return item
    phrases = [s for part in item if isinstance(part, (list, tuple)) for s in part if isinstance(s, str)]
    if phrases:
        return " ".join(phrases)
    strs = [part for part in item if isinstance(part, str)]
    return strs[-1] if strs else ""


def utm_link(page: str, campaign: str) -> str:
    page = page if page.startswith("/") else "/" + page
    u = urllib.parse.urlsplit(SITE + page)
    utm = urllib.parse.urlencode({"utm_source": "instagram", "utm_medium": "reels", "utm_campaign": campaign})
    query = f"{u.query}&{utm}" if u.query else utm
    return urllib.parse.urlunsplit(u._replace(query=query))


def hook_report(lines: list[str]) -> list[str]:
    if not lines:
        return ["нет LINES в voice.py"]
    hook = lines[0]
    words = len(hook.split())
    notes = []
    if words > HOOK_MAX_WORDS:
        notes.append(f"хук {words} слов — сократить до {HOOK_MAX_WORDS}, он должен влезть в 1,5 с")
    if not re.search(r"\d|\?|!|не |нельзя|бесплатн|никто|хватит|ошибк", hook, re.I):
        notes.append("в хуке нет цифры, вопроса, запрета или обещания — добавить один триггер")
    if re.match(r"(привет|сегодня|в этом видео|давайте)", hook, re.I):
        notes.append("хук начинается с приветствия — сразу к сути")
    total_words = sum(len(x.split()) for x in lines)
    if total_words > 110:
        notes.append(f"{total_words} слов ≈ {total_words / 2.6:.0f} с речи — для Reels лучше 60–90 слов")
    return notes or ["хук ок"]


def llm_caption(lines: list[str], cfg: dict) -> str | None:
    base, key = os.environ.get("VG_LLM_BASE_URL"), os.environ.get("VG_LLM_API_KEY")
    if not (base and key):
        return None
    prompt = (
        "Напиши подпись к Instagram Reels на русском, до 300 символов: первая строка — повтор хука "
        "другими словами, затем 2 строки пользы без воды, затем призыв: "
        f"«Напиши {cfg['keyword']} в комментариях — пришлю ссылку». Без хештегов и эмодзи-спама. "
        "Не добавляй фактов, которых нет в тексте ролика.\n\nТекст ролика:\n" + "\n".join(lines)
    )
    body = json.dumps({
        "model": os.environ.get("VG_LLM_MODEL", "deepseek-v4.1-flash"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 400,
    }).encode()
    req = urllib.request.Request(base.rstrip("/") + "/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("LLM недоступна, беру шаблон:", e, file=sys.stderr)
        return None


def build(project: Path) -> Path:
    lines = read_lines(project / "voice.py")
    cfg_path = project / "reel.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    cfg.setdefault("topic", project.name)
    cfg.setdefault("page", "/")
    cfg.setdefault("keyword", "AI")
    tags = ["#" + t.lstrip("#") for t in cfg.get("hashtags", ["нейросети", "ии", "ai"])][:MAX_HASHTAGS]
    link = utm_link(cfg["page"], project.name)
    caption = llm_caption(lines, cfg) or "\n".join([
        lines[0] if lines else cfg["topic"],
        "",
        f"Полный разбор {cfg['topic']} — по ссылке в шапке профиля.",
        f"Напиши {cfg['keyword']} в комментариях — пришлю ссылку в директ.",
    ])
    md = [
        f"# {cfg['topic']} — пакет публикации",
        "",
        "## Проверка хука",
        *[f"- {n}" for n in hook_report(lines)],
        "",
        "## Подпись",
        caption,
        "",
        " ".join(tags),
        "",
        "## Ссылка (шапка профиля / автоответ в директ)",
        link,
        "",
        "## Закреплённый комментарий",
        f"Ссылка на разбор {cfg['topic']} — в шапке профиля. Или напиши {cfg['keyword']}, пришлю в директ.",
        "",
        "## Перед публикацией",
        "- обложка: крупный текст хука, лицо или результат в центре кадра 4:5",
        "- сначала Trial Reel (показ только не подписчикам), через 24 ч — в профиль, если досмотры выше среднего",
        "- автоответ на ключевое слово в комментариях — ссылка выше",
    ]
    out = project / "instagram.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    return out


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    print("готово:", build(Path(sys.argv[1])))


if __name__ == "__main__":
    main()
