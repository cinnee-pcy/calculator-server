import math
from collections import deque
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from models import Expression, CalculatorLog

HISTORY_MAX = 1000
history: deque = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.get("/")
def root():
    return {"status": "ok", "message": "Mini Calculator API is running"}


@app.post("/calculate")
def calculate(data: Expression):
    expr_str = data.expr
    if not expr_str or not expr_str.strip():
        return {"ok": False, "expr": "", "error": "Expression cannot be empty"}

    try:
        code = data.expand_percent()
        result = aeval(code)

        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr_str, "result": "", "error": msg}

        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_entry = CalculatorLog(
            timestamp=now_utc,
            expr=expr_str.strip(),
            result=result
        )
        history.append(log_entry)

        return {"ok": True, "expr": expr_str.strip(), "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr_str, "error": str(e)}


@app.get("/history", response_model=List[CalculatorLog])
def get_history(limit: int = Query(default=50, ge=1)):
    items = list(history)
    if limit > 0:
        return items[-limit:]
    return []


@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True, "message": "History cleared"}