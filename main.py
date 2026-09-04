# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from calculator import Calculator

# app = FastAPI(title="Calculator Server API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class CalculationRequest(BaseModel):
#     num1: float
#     num2: float
#     operation: str

# @app.get("/")
# def root():
#     return {"status": "ok", "message": "Calculator Server is running"}

# @app.post("/calculate")
# def calculate(payload: CalculationRequest):
#     try:
#         op = payload.operation.lower()
#         if op == "add":
#             res = Calculator.add(payload.num1, payload.num2)
#         elif op == "subtract":
#             res = Calculator.subtract(payload.num1, payload.num2)
#         elif op == "multiply":
#             res = Calculator.multiply(payload.num1, payload.num2)
#         elif op == "divide":
#             res = Calculator.divide(payload.num1, payload.num2)
#         else:
#             raise HTTPException(status_code=400, detail="Invalid operation")
#         return {"result": res}
#     except ValueError as err:
#         raise HTTPException(status_code=400, detail=str(err))
import math
from collections import deque
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter

from calculator import expand_percent

HISTORY_MAX = 1000
# HISTORY (in-memory for now)
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Safe evaluator ----------
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.post("/calculate")
def calculate(expr: str):
    try:
        code = expand_percent(expr)
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}
        # TODO: Add history
        return {"ok": True, "expr": expr, "result": result, "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}

# TODO GET /hisory

# TODO DELETE /history

