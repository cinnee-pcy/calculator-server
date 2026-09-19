from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import calculator, history

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator.router)
app.include_router(history.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Mini Calculator API is running"}