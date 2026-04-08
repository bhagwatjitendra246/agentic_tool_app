from __future__ import annotations
import re
from typing import List

NUMBER_PATTERN = r"[-+]?\d*\.?\d+"


def split_instructions(query: str) -> List[str]:
    normalized = query.strip()
    normalized = re.sub(r"\s+", " ", normalized)
    parts = re.split(r",\s*(?=(?:add|subtract|multiply|divide|uppercase|lowercase|reverse|replace|take|start)\b)|\s+then\s+|\s+and\s+(?=(?:add|subtract|multiply|divide|uppercase|lowercase|reverse|replace|take|start)\b)", normalized, flags=re.IGNORECASE)
    cleaned = []
    for part in parts:
        if not part:
            continue
        piece = str(part).strip(" ,")
        if piece and piece.lower() not in {"add", "subtract", "multiply", "divide", "uppercase", "lowercase", "reverse", "replace", "take", "start"}:
            cleaned.append(piece)
    return cleaned

def extract_numbers(text: str) -> List[float]:
    return [float(match) for match in re.findall(NUMBER_PATTERN, text)]