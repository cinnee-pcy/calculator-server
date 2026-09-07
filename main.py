import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent

HISTORY_MAX = 1000
# In-memory history queue
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safe mathematical evaluator with constants
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.get("/")
def root():
    return {"status": "ok", "message": "Mini Calculator API is running"}


@app.post("/calculate")
def calculate(expr: str):
    if not expr or not expr.strip():
        return {"ok": False, "expr": "", "error": "Expression cannot be empty"}

    try:
        code = expand_percent(expr.strip())
        result = aeval(code)

        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}

        # บันทึกลงประวัติการคำนวณ
        history.append({
            "expr": expr,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}


@app.get("/history")
def get_history():
    return list(history)


@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True, "message": "History cleared"}