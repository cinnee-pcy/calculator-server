# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_health_check():
#     res = client.get("/")
#     assert res.status_code == 200
#     assert res.json()["status"] == "ok"

# def test_api_add():
#     res = client.post("/calculate", json={"num1": 15, "num2": 25, "operation": "add"})
#     assert res.status_code == 200
#     assert res.json()["result"] == 40

# def test_api_divide_by_zero():
#     res = client.post("/calculate", json={"num1": 8, "num2": 0, "operation": "divide"})
#     assert res.status_code == 400
#     assert res.json()["detail"] == "Cannot divide by zero"
from fastapi.testclient import TestClient
from main import app  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# TODO Add more tests