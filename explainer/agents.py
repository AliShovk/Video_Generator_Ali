#!/usr/bin/env python3
"""Агенты конвейера: research → engineering → script → storyboard → factcheck."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Fact:
    id: str
    value: float | int
    unit: str
    claim: str
    source: str


@dataclass
class Brief:
    slug: str
    title: str
    subtitle: str
    hook: str
    structure: str
    dims: dict
    principle: str
    load_path: list[str]
    flows: list[str]
    details: list[str]
    facts: list[Fact]
    sources: list[str]

    @classmethod
    def load(cls, path: Path) -> "Brief":
        d = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            slug=d["slug"], title=d["title"], subtitle=d.get("subtitle", ""),
            hook=d["hook"], structure=d.get("structure", "arch"), dims=d.get("dims", {}),
            principle=d["principle"], load_path=d["load_path"], flows=d["flows"],
            details=d["details"],
            facts=[Fact(**f) for f in d["facts"]],
            sources=d.get("sources", []),
        )


def fmt_num(v: float | int) -> str:
    if isinstance(v, int) or float(v).is_integer():
        n = int(v)
        return f"{n:,}".replace(",", " ")
    return str(v).replace(".", ",")


def fact_by_id(facts: list[Fact], fid: str) -> Fact:
    for f in facts:
        if f.id == fid:
            return f
    raise KeyError(fid)


# ---------------------------------------------------------------- research
def research(brief: Brief) -> str:
    lines = [f"# Research — {brief.title}", ""]
    lines.append("## Проверенные факты")
    lines.append("| id | значение | формулировка | источник |")
    lines.append("|---|---|---|---|")
    for f in brief.facts:
        lines.append(f"| {f.id} | {fmt_num(f.value)} {f.unit} | {f.claim} | {f.source} |")
    lines += ["", "## Источники"]
    for s in brief.sources:
        lines.append(f"- {s}")
    lines += ["", "## Ограничения",
              "- Размеры и массы взяты из перечисленных источников; внутреннее устройство не додумывается.",
              "- Если число не подтверждено источником, оно не попадает в озвучку (см. factcheck.json)."]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------- engineering
def engineering(brief: Brief) -> str:
    lines = [f"# Engineering — {brief.title}", "", "## Принцип"]
    lines.append(brief.principle)
    lines += ["", "## Передача нагрузки"]
    for i, step in enumerate(brief.load_path, 1):
        lines.append(f"{i}. {step}")
    lines += ["", "## Движение сред и механизмов"]
    for f in brief.flows:
        lines.append(f"- {f}")
    lines += ["", "## Обязательные детали"]
    for d in brief.details:
        lines.append(f"- {d}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ script
def script(brief: Brief) -> tuple[str, list[dict]]:
    """Возвращает markdown и список реплик по сценам."""
    f = {x.id: x for x in brief.facts}
    w = f.get("weight")
    h, s, ln = f.get("height"), f.get("span"), f.get("length")
    jacks, move, year = f.get("jacks"), f.get("move"), f.get("year")
    dmg = f.get("damage")

    lines = [
        {"id": "s1", "text": brief.hook},
        {"id": "s2", "text": "Вес идёт вниз. Дальше опоры. Опоры стоят на рельсах."},
    ]
    if h and s and ln:
        lines.append({"id": "s3", "text":
            f"Высота — {fmt_num(h.value)} метров, пролёт — {fmt_num(s.value)}, длина — {fmt_num(ln.value)}."})
    if jacks and move:
        lines.append({"id": "s4", "text":
            f"Арка стоит на рельсах. Домкратов {fmt_num(jacks.value)}. "
            f"Они толкают арку вперёд. Путь {fmt_num(move.value)} метров."})
    if year:
        done = {"id": "s5", "text": "Перемещение завершили в " + fmt_num(year.value) + " году. Арка накрыла четвёртый энергоблок."}
        lines.append(done)
    if dmg:
        lines.append({"id": "s6", "text":
            "Но в " + fmt_num(dmg.value) + " году оболочка получила повреждения. Восстановление ещё не завершено."})

    md = [f"# Script — {brief.title}", "", f"**Хук (0–4 с):** {brief.hook}", "", "## Дикторский текст"]
    for i, ln_ in enumerate(lines, 1):
        md.append(f"{i}. [{ln_['id']}] {ln_['text']}")
    md += ["", f"## Источники фактов", *[f"- {x.claim} — {x.source}" for x in brief.facts]]
    return "\n".join(md) + "\n", lines


# -------------------------------------------------------------- storyboard
KIND_BY_SCENE = {"s1": "hero", "s2": "section", "s3": "dimensions",
                 "s4": "detail", "s5": "move", "s6": "note"}
DUR = {"s1": 7, "s2": 10, "s3": 9, "s4": 11, "s5": 9, "s6": 7}


def storyboard(brief: Brief, lines: list[dict]) -> list[dict]:
    scenes = []
    for item in lines:
        sid = item["id"]
        kind = KIND_BY_SCENE[sid]
        scenes.append({
            "id": sid,
            "kind": kind,
            "duration": DUR[sid],
            "narration": item["text"],
            "camera": {"hero": "медленный наезд", "section": "панорама слева направо",
                       "dimensions": "фиксация, размеры проявляются",
                       "detail": "крупный план узла", "move": "слежение за аркой",
                       "note": "статичный кадр"}[kind],
            "objects": {
                "hero": ["арка", "энергоблок", "техника у основания"],
                "section": ["оболочка", "ферменные рёбра", "опорные балки", "стрелки нагрузки"],
                "dimensions": ["арка", "размерные линии", "подписи 108 / 257 / 162"],
                "detail": ["рельс", "опорная плита", "домкраты", "гидролинии"],
                "move": ["арка на рельсах", "линия пути", "метка 327 м"],
                "note": ["повреждённая панель", "штамп 2025"],
            }[kind],
        })
    return scenes


# --------------------------------------------------------------- factcheck
NUM_RE = re.compile(r"\d[\d\s]{0,12}")


def numbers_in(text: str) -> set[int]:
    out = set()
    for m in NUM_RE.finditer(text):
        raw = m.group(0).replace(" ", "")
        if raw.isdigit():
            out.add(int(raw))
    return out


def factcheck(brief: Brief, lines: list[dict], scenes: list[dict]) -> dict:
    allowed = {int(f.value) for f in brief.facts}
    problems = []
    for ln in lines:
        for n in numbers_in(ln["text"]):
            if n not in allowed:
                problems.append({"scene": ln["id"], "number": n, "reason": "числа нет в research.md"})
    total = sum(s["duration"] for s in scenes)
    if not 45 <= total <= 60:
        problems.append({"scene": "timeline", "number": total, "reason": "длительность вне 45–60 с"})
    return {"ok": not problems, "checked_numbers": sorted(allowed), "problems": problems,
            "duration_s": total}
