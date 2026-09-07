import math
from collections import deque
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sympy as sp
from asteval import Interpreter
from calculator import expand_percent

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

app = FastAPI(title="Photomath Scientific Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ประกาศตัวแปรสัญลักษณ์สำหรับ SymPy
x, y, z, n = sp.symbols("x y z n")

SYMPY_CONTEXT = {
    "x": x,
    "y": y,
    "z": z,
    "n": n,
    "pi": sp.pi,
    "e": sp.E,
    "oo": sp.oo,
    "I": sp.I,
    # Calculus
    "diff": sp.diff,
    "integrate": sp.integrate,
    "limit": sp.limit,
    "Sum": sp.Sum,
    # Trigonometry & Hyperbolic
    "sin": lambda v: sp.sin(sp.rad(v)),
    "cos": lambda v: sp.cos(sp.rad(v)),
    "tan": lambda v: sp.tan(sp.rad(v)),
    "cot": lambda v: sp.cot(sp.rad(v)),
    "sec": lambda v: sp.sec(sp.rad(v)),
    "csc": lambda v: sp.csc(sp.rad(v)),
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "acot": sp.acot,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "coth": sp.coth,
    "asinh": sp.asinh,
    "acosh": sp.acosh,
    "atanh": sp.atanh,
    "arcoth": sp.acoth,
    # Algebra & Logs
    "sqrt": sp.sqrt,
    "cbrt": sp.cbrt,
    "root": sp.root,
    "log": sp.log,
    "ln": sp.log,
    "log10": lambda v: sp.log(v, 10),
    "log2": lambda v: sp.log(v, 2),
    "exp": sp.exp,
    "Abs": sp.Abs,
    "factorial": sp.factorial,
    "sign": sp.sign,
}

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})


@app.get("/")
def root():
    return {"status": "ok", "message": "Photomath Server is running"}


@app.post("/calculate")
def calculate(expr: str):
    if not expr or not expr.strip():
        return {"ok": False, "expr": "", "error": "Expression cannot be empty"}

    try:
        clean_code = expand_percent(expr.strip())
        clean_code = clean_code.replace("∞", "oo")

        # 1. พยายามคำนวณผ่าน SymPy ก่อน เพื่อรองรับแคลคูลัส ตัวแปร x และฟังก์ชันขั้นสูง
        try:
            parsed = sp.sympify(clean_code, locals=SYMPY_CONTEXT)
            if hasattr(parsed, "doit"):
                parsed = parsed.doit()
            result_val = str(parsed)
            # ปรับแต่งเครื่องหมายให้อ่านง่าย
            result_val = result_val.replace("**", "^").replace("*", "")
            return {"ok": True, "expr": expr, "result": result_val, "error": ""}
        except Exception:
            pass

        # 2. Fallback กลับมา asteval หากเป็นตัวเลขพีชคณิตธรรมดา
        result = aeval(clean_code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return {"ok": False, "expr": expr, "result": "", "error": msg}

        if isinstance(result, float):
            result = round(result, 8)

        return {"ok": True, "expr": expr, "result": str(result), "error": ""}
    except Exception as e:
        return {"ok": False, "expr": expr, "error": str(e)}