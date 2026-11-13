#!/usr/bin/env python3
"""Локальная библиотека векторных иллюстраций: unDraw + Iconify.

    python3 vectorlib.py build "fire,night,snow,forest,camping" --pages 2
    python3 vectorlib.py search "костёр"
    python3 vectorlib.py icon mdi:campfire
    python3 vectorlib.py stats
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("/root/video-gen/assets/vectors")
INDEX = ROOT / "index.json"
UNDRAW_SEARCH = "https://undraw.co/api/search?q={q}&page={page}"
ICONIFY = "https://api.iconify.design/{name}.svg"


def _get(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 vectorlib"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def load_index() -> dict:
    if INDEX.exists():
        return json.loads(INDEX.read_text(encoding="utf-8"))
    return {"items": {}}


def save_index(idx: dict) -> None:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")


def slugify(s: str) -> str:
    s = s.lower().replace(" ", "-")
    return re.sub(r"[^a-z0-9\-]", "", s)[:60] or "item"


def search_undraw(query: str, page: int = 1) -> list[dict]:
    url = UNDRAW_SEARCH.format(q=urllib.parse.quote(query), page=page)
    data = json.loads(_get(url).decode("utf-8"))
    return data.get("results", []), bool(data.get("hasMore"))


def build(queries: list[str], pages: int = 1) -> dict:
    idx = load_index()
    added = 0
    for q in queries:
        for page in range(1, pages + 1):
            try:
                items, more = search_undraw(q, page)
            except Exception as exc:  # noqa: BLE001
                print(f"[skip] {q} p{page}: {exc}")
                break
            for it in items:
                slug = it.get("newSlug") or slugify(it.get("title", "item"))
                media = it.get("media")
                if not media or slug in idx["items"]:
                    continue
                folder = ROOT / "undraw"
                folder.mkdir(parents=True, exist_ok=True)
                path = folder / f"{slug}.svg"
                try:
                    raw = _get(media)
                except Exception as exc:  # noqa: BLE001
                    print(f"[warn] {slug}: {exc}")
                    continue
                path.write_bytes(raw)
                idx["items"][slug] = {
                    "title": it.get("title", slug), "slug": slug, "query": q,
                    "path": str(path.relative_to(ROOT)), "source": media,
                    "type": "undraw", "bytes": len(raw),
                }
                added += 1
            if not more:
                break
    save_index(idx)
    print(f"добавлено {added}, всего {len(idx['items'])}")
    return idx


def icon(name: str, color: str | None = None) -> Path:
    safe = name.replace(":", "-")
    folder = ROOT / "icons"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{safe}{'' if not color else '-' + color.lstrip('#')}.svg"
    if path.exists():
        return path
    url = ICONIFY.format(name=name.replace(":", "/"))
    if color:
        url += "?color=" + urllib.parse.quote(color)
    path.write_bytes(_get(url))
    idx = load_index()
    idx["items"][f"icon:{safe}"] = {"title": name, "type": "icon", "path": str(path.relative_to(ROOT)),
                                    "query": "icon", "source": url, "bytes": path.stat().st_size}
    save_index(idx)
    return path


def search(query: str) -> list[dict]:
    idx = load_index()
    q = query.lower()
    hits = []
    for item in idx["items"].values():
        hay = f"{item.get('title','')} {item.get('slug','')} {item.get('query','')}".lower()
        if q in hay:
            hits.append(item)
    return sorted(hits, key=lambda x: x.get("title", ""))


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("queries")
    b.add_argument("--pages", type=int, default=1)
    s = sub.add_parser("search")
    s.add_argument("query")
    i = sub.add_parser("icon")
    i.add_argument("name")
    i.add_argument("--color", default=None)
    sub.add_parser("stats")
    a = ap.parse_args()

    if a.cmd == "build":
        build([x.strip() for x in a.queries.split(",") if x.strip()], a.pages)
    elif a.cmd == "search":
        for item in search(a.query)[:40]:
            print(f"{item['title'][:44]:<46} {item['path']}")
    elif a.cmd == "icon":
        print(icon(a.name, a.color))
    else:
        idx = load_index()
        by_type: dict[str, int] = {}
        for it in idx["items"].values():
            by_type[it.get("type", "?")] = by_type.get(it.get("type", "?"), 0) + 1
        print(json.dumps({"total": len(idx["items"]), "by_type": by_type}, ensure_ascii=False))


if __name__ == "__main__":
    main()
