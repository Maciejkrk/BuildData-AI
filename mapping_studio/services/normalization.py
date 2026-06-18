from __future__ import annotations

import re
import unicodedata
from typing import Any


def normalize(value: Any) -> str:
    text = str(value or "").strip().casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.replace("ł", "l").replace("Ł", "l")
    text = text.replace("µ", "mu").replace("μ", "mu").replace("λ", "lambda")
    text = re.sub(r"[_\-/]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def lookup_key(value: Any) -> str:
    return normalize(value).replace(" ", "")


def first_present(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return None


def int_value(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def text_value(value: Any) -> str:
    return "" if value is None else str(value).strip()

