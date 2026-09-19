import math
from collections import deque
from datetime import datetime, timezone
from typing import Callable

from fastapi import APIRouter, Depends
from asteval import Interpreter

from app.schemas import ExpressionIn, ExpressionOut
from app.dependencies import get_history, get_expand_percent

router = APIRouter()
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@router.post("/calculate")
def calculate(
    data: ExpressionIn,
    expand_fn: Callable[[str], str] = Depends(get_expand_percent),
    history: deque = Depends(get_history),
):
    expr_str = data.expr
    if not expr_str or not expr_str.strip():
        return {"ok": False, "expr": "", "error": "Expression cannot be empty"}

    try:
        code = expand_fn(expr_str)
        result = aeval(code)

        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr_str, "result": "", "error": msg}

        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_entry = ExpressionOut(
            timestamp=now_utc,
            expr=expr_str.strip(),
            result=result
        )
        history.append(log_entry)

        return {"ok": True, "expr": expr_str.strip(), "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr_str, "error": str(e)}