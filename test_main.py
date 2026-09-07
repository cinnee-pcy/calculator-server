import math
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ==========================================
# 1. Arithmetic & Precedence Tests
# ==========================================

def test_basic_addition():
    r = client.post("/calculate", params={"expr": "12 + 8"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 20) < 1e-9


def test_basic_subtraction_negative():
    r = client.post("/calculate", params={"expr": "5 - 15"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - (-10)) < 1e-9


def test_basic_multiplication():
    r = client.post("/calculate", params={"expr": "7 * 6"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 42) < 1e-9


def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9


def test_operator_precedence():
    r1 = client.post("/calculate", params={"expr": "2 + 3 * 4"})
    assert r1.json()["ok"] is True
    assert abs(r1.json()["result"] - 14) < 1e-9

    r2 = client.post("/calculate", params={"expr": "(2 + 3) * 4"})
    assert r2.json()["ok"] is True
    assert abs(r2.json()["result"] - 20) < 1e-9


def test_power_operation():
    r = client.post("/calculate", params={"expr": "2 ** 4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 16) < 1e-9


# ==========================================
# 2. Percentage Operations Tests
# ==========================================

def test_percent_addition():
    r = client.post("/calculate", params={"expr": "50 + 10%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 55.0) < 1e-9


def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9


def test_percent_multiplication():
    r = client.post("/calculate", params={"expr": "20 * 50%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 10.0) < 1e-9


def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9


# ==========================================
# 3. Math Constants (pi, e) Tests
# ==========================================

def test_math_constants():
    r_pi = client.post("/calculate", params={"expr": "pi * 2"})
    assert r_pi.status_code == 200
    assert r_pi.json()["ok"] is True
    assert abs(r_pi.json()["result"] - (math.pi * 2)) < 1e-9

    r_e = client.post("/calculate", params={"expr": "e + 1"})
    assert r_e.status_code == 200
    assert r_e.json()["ok"] is True
    assert abs(r_e.json()["result"] - (math.e + 1)) < 1e-9


# ==========================================
# 4. Error Handling & Edge Cases
# ==========================================

def test_division_by_zero():
    r = client.post("/calculate", params={"expr": "10 / 0"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "ZeroDivisionError" in data["error"] or "division" in data["error"]


def test_invalid_syntax():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert data["error"] != ""


def test_empty_expression():
    r = client.post("/calculate", params={"expr": "   "})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "cannot be empty" in data["error"]


def test_security_injection_blocked():
    r = client.post("/calculate", params={"expr": "__import__('os').system('ls')"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False


# ==========================================
# 5. History API Workflow Tests
# ==========================================

def test_history_workflow():
    # 1. ล้างประวัติก่อนเริ่ม
    del_r = client.delete("/history")
    assert del_r.status_code == 200
    assert del_r.json()["ok"] is True

    # 2. คำนวณ 2 ค่า
    client.post("/calculate", params={"expr": "10 + 20"})
    client.post("/calculate", params={"expr": "5 * 4"})

    # 3. ดึงประวัติมาตรวจสอบ
    get_r = client.get("/history")
    assert get_r.status_code == 200
    items = get_r.json()
    assert len(items) == 2
    assert items[0]["expr"] == "10 + 20"
    assert items[0]["result"] == 30
    assert items[1]["expr"] == "5 * 4"
    assert items[1]["result"] == 20

    # 4. ล้างประวัติและตรวจว่าว่างเปล่า
    client.delete("/history")
    empty_r = client.get("/history")
    assert empty_r.status_code == 200
    assert len(empty_r.json()) == 0