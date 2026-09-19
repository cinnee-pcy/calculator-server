from pydantic import BaseModel
from typing import Union


# 1. คลาสแม่เก็บ attribute ร่วม
class BaseExpression(BaseModel):
    expr: str


# 2. คลาสลูกสำหรับ Input (Request Body) สืบทอดจาก BaseExpression
class ExpressionIn(BaseExpression):
    pass


# 3. คลาสลูกสำหรับ Output (Response Body) สืบทอดจาก BaseExpression และเพิ่ม timestamp, result
class ExpressionOut(BaseExpression):
    timestamp: str
    result: Union[int, float, str]


# 4. Alias ชื่อเดิมตามข้อกำหนดของโจทย์
Expression = ExpressionIn
CalculatorLog = ExpressionOut