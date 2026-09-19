from collections import deque
from typing import List

from fastapi import APIRouter, Depends, Query
from app.schemas import ExpressionOut
from app.dependencies import get_history

router = APIRouter()


@router.get("/history", response_model=List[ExpressionOut])
def read_history(
    limit: int = Query(default=50, ge=1),
    history: deque = Depends(get_history)
):
    items = list(history)
    if limit > 0:
        return items[-limit:]
    return []


@router.delete("/history")
def clear_history(history: deque = Depends(get_history)):
    history.clear()
    return {"ok": True, "message": "History cleared"}