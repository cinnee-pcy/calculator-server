# import pytest
# from calculator import Calculator

# def test_add():
#     assert Calculator.add(5, 3) == 8
#     assert Calculator.add(-2, 2) == 0

# def test_subtract():
#     assert Calculator.subtract(10, 4) == 6
#     assert Calculator.subtract(2, 5) == -3

# def test_multiply():
#     assert Calculator.multiply(6, 7) == 42
#     assert Calculator.multiply(-3, 4) == -12

# def test_divide():
#     assert Calculator.divide(20, 4) == 5
#     with pytest.raises(ValueError, match="Cannot divide by zero"):
#         Calculator.divide(10, 0)
import pytest
from calculator import expand_percent  # import your function

def test_add_percent():
    """Test addition where B% means 'B percent of A'."""
    assert expand_percent("5 + 10%") == "5 + ((10/100)*5)"

def test_subtract_percent():
    """Test subtraction where B% means 'B percent of A'."""
    assert expand_percent("20 - 30%") == "20 - ((30/100)*20)"

def test_multiply_percent():
    """Test multiplication where B% means 'B divided by 100'."""
    assert expand_percent("15 * 25%") == "15 * (25/100)"

def test_divide_percent():
    """Test division where B% means 'B divided by 100'."""
    assert expand_percent("40 / 50%") == "40 / (50/100)"

def test_multiple_operations():
    """Test expressions with multiple A op B% operations."""
    assert expand_percent("3 * 4% + 2 / 1%") == "3 * (4/100) + 2 / (1/100)"

def test_standalone_100_percent():
    """Test standalone percentage (100%)."""
    assert expand_percent("100%") == "(100/100)"

def test_two_standalone_percents():
    """Test expression with two standalone percentages."""
    assert expand_percent("10% + 20%") == "(10/100) + (20/100)"
