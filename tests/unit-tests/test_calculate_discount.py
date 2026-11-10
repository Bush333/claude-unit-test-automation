import pytest

from src.shopping_cart import calculate_discount


def test_calculate_discount_normal_case():
    assert calculate_discount(100, 10) == 90.0


def test_calculate_discount_zero_percent():
    assert calculate_discount(100, 0) == 100.0


def test_calculate_discount_full_percent():
    assert calculate_discount(100, 100) == 0.0


def test_calculate_discount_zero_total():
    assert calculate_discount(0, 50) == 0.0


def test_calculate_discount_rounding():
    assert calculate_discount(99.99, 33) == round(99.99 * (1 - 33 / 100), 2)


def test_calculate_discount_float_total():
    assert calculate_discount(49.5, 20) == round(49.5 * 0.8, 2)


def test_calculate_discount_negative_total_raises():
    with pytest.raises(ValueError, match="Total cannot be negative"):
        calculate_discount(-1, 10)


def test_calculate_discount_negative_percent_raises():
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        calculate_discount(100, -1)


def test_calculate_discount_percent_over_100_raises():
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        calculate_discount(100, 101)


def test_calculate_discount_boundary_percent_values():
    assert calculate_discount(200, 0) == 200.0
    assert calculate_discount(200, 100) == 0.0
