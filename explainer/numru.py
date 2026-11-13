#!/usr/bin/env python3
"""Русские числительные без внешних зависимостей (0 … 999 999 999)."""

UNITS_M = ["ноль", "один", "два", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
UNITS_F = ["ноль", "одна", "две", "три", "четыре", "пять", "шесть", "семь", "восемь", "девять"]
TEENS = ["десять", "одиннадцать", "двенадцать", "тринадцать", "четырнадцать",
         "пятнадцать", "шестнадцать", "семнадцать", "восемнадцать", "девятнадцать"]
TENS = ["", "", "двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят",
        "семьдесят", "восемьдесят", "девяносто"]
HUNDREDS = ["", "сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот",
            "семьсот", "восемьсот", "девятьсот"]


def _triple(n: int, feminine: bool = False) -> list[str]:
    out: list[str] = []
    h, rest = divmod(n, 100)
    if h:
        out.append(HUNDREDS[h])
    if 10 <= rest < 20:
        out.append(TEENS[rest - 10])
        return out
    t, u = divmod(rest, 10)
    if t:
        out.append(TENS[t])
    if u:
        out.append((UNITS_F if feminine else UNITS_M)[u])
    return out


def _plural(n: int, forms: tuple[str, str, str]) -> str:
    n = abs(n) % 100
    if 11 <= n <= 19:
        return forms[2]
    n %= 10
    if n == 1:
        return forms[0]
    if 2 <= n <= 4:
        return forms[1]
    return forms[2]


def ru_number(n: int) -> str:
    if n == 0:
        return "ноль"
    parts: list[str] = []
    millions, rest = divmod(n, 1_000_000)
    thousands, units = divmod(rest, 1000)
    if millions:
        parts += _triple(millions)
        parts.append(_plural(millions, ("миллион", "миллиона", "миллионов")))
    if thousands:
        parts += _triple(thousands, feminine=True)
        parts.append(_plural(thousands, ("тысяча", "тысячи", "тысяч")))
    if units:
        parts += _triple(units)
    return " ".join(parts)
