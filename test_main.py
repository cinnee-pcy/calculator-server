from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_api_add():
    res = client.post("/calculate", json={"num1": 15, "num2": 25, "operation": "add"})
    assert res.status_code == 200
    assert res.json()["result"] == 40

def test_api_divide_by_zero():
    res = client.post("/calculate", json={"num1": 8, "num2": 0, "operation": "divide"})
    assert res.status_code == 400
    assert res.json()["detail"] == "Cannot divide by zero"
