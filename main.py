from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from calculator import Calculator

app = FastAPI(title="Calculator Server API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalculationRequest(BaseModel):
    num1: float
    num2: float
    operation: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Calculator Server is running"}

@app.post("/calculate")
def calculate(payload: CalculationRequest):
    try:
        op = payload.operation.lower()
        if op == "add":
            res = Calculator.add(payload.num1, payload.num2)
        elif op == "subtract":
            res = Calculator.subtract(payload.num1, payload.num2)
        elif op == "multiply":
            res = Calculator.multiply(payload.num1, payload.num2)
        elif op == "divide":
            res = Calculator.divide(payload.num1, payload.num2)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        return {"result": res}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
