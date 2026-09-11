from pydantic import BaseModel
from typing import Union
from calculator import expand_percent as calc_expand_percent


class Expression(BaseModel):
    expr: str

    def expand_percent(self) -> str:
        clean = (
            self.expr.strip()
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )
        return calc_expand_percent(clean)


class CalculatorLog(BaseModel):
    timestamp: str
    expr: str
    result: Union[int, float, str]