import pytest
from calculator import Calculator

def test_add():
    assert Calculator.add(5, 3) == 8
    assert Calculator.add(-2, 2) == 0

def test_subtract():
    assert Calculator.subtract(10, 4) == 6
    assert Calculator.subtract(2, 5) == -3

def test_multiply():
    assert Calculator.multiply(6, 7) == 42
    assert Calculator.multiply(-3, 4) == -12

def test_divide():
    assert Calculator.divide(20, 4) == 5
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Calculator.divide(10, 0)
