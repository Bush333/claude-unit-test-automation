"""Regression tests for KAN-5: calculate_discount fails with Decimal input."""
from decimal import Decimal

from src.shopping_cart import calculate_discount


def test_kan_5_decimal_total_with_float_percent():
    result = calculate_discount(Decimal("100.00"), 12.5)
    assert isinstance(result, Decimal)
    assert result == Decimal("87.50")


def test_kan_5_decimal_total_with_int_percent():
    result = calculate_discount(Decimal("49.99"), 10)
    assert isinstance(result, Decimal)
    assert result == Decimal("44.99")


def test_kan_5_int_total_behaviour_preserved():
    result = calculate_discount(100, 10)
    assert isinstance(result, float)
    assert result == 90.0


def test_kan_5_float_total_behaviour_preserved():
    result = calculate_discount(99.99, 33)
    assert isinstance(result, float)
    assert result == round(99.99 * (1 - 33 / 100), 2)
