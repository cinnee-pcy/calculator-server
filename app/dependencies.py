from collections import deque
from typing import Callable
from calculator import expand_percent as calc_expand_percent

HISTORY_MAX = 1000
_history: deque = deque(maxlen=HISTORY_MAX)


def get_history() -> deque:
    return _history


def expand_percent(expr: str) -> str:
    clean = (
        expr.strip()
        .replace("×", "*")
        .replace("÷", "/")
        .replace("−", "-")
    )
    return calc_expand_percent(clean)


def get_expand_percent() -> Callable[[str], str]:
    return expand_percent