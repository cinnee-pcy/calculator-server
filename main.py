import math
from collections import deque
from datetime import datetime, timezone
from typing import List, Dict, Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent

HISTORY_MAX = 1000
# In-memory history queue
history: deque = deque(maxlen=HISTORY_MAX)

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
        # แปลงเครื่องหมายทางคณิตศาสตร์ให้รองรับการกดจาก UI
        clean_expr = (
            expr.strip()
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )
        
        code = expand_percent(clean_expr)
        result = aeval(code)

        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}

        # บันทึก timestamp เป็นรูปแบบ ISO UTC ลงท้ายด้วย 'Z' ตามโจทย์
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        history.append({
            "timestamp": now_utc,
            "expr": expr.strip(),
            "result": result
        })

        return {"ok": True, "expr": expr.strip(), "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}


@app.get("/history")
def get_history(limit: int = Query(default=50, ge=1)):
    """
    คืนค่าประวัติการคำนวณล่าสุดไม่เกิน limit รายการ (Default 50)
    """
    items = list(history)
    if limit > 0:
        return items[-limit:]
    return []


@app.delete("/history")
def clear_history():
    """
    ล้างประวัติการคำนวณทั้งหมด
    """
    history.clear()
    return {"ok": True, "message": "History cleared"}