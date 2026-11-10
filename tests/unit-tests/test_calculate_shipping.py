from decimal import Decimal

import pytest

from src.shopping_cart import calculate_shipping


class TestCalculateShippingStandard:
    def test_order_total_above_threshold_is_free(self):
        assert calculate_shipping(150) == Decimal("0.00")

    def test_order_total_well_above_threshold_is_free(self):
        assert calculate_shipping(1000) == Decimal("0.00")

    def test_order_total_below_threshold_charges_standard_fee(self):
        assert calculate_shipping(50) == Decimal("10.00")

    def test_order_total_just_below_threshold_charges_standard_fee(self):
        assert calculate_shipping(99.99) == Decimal("10.00")

    def test_order_total_at_threshold_boundary_is_free(self):
        assert calculate_shipping(100) == Decimal("0.00")

    def test_order_total_zero_charges_standard_fee(self):
        assert calculate_shipping(0) == Decimal("10.00")

    def test_express_defaults_to_false(self):
        assert calculate_shipping(150) == calculate_shipping(150, express=False)


class TestCalculateShippingExpress:
    def test_express_shipping_below_threshold(self):
        assert calculate_shipping(50, express=True) == Decimal("25.00")

    def test_express_shipping_above_threshold(self):
        assert calculate_shipping(150, express=True) == Decimal("25.00")

    def test_express_shipping_at_threshold(self):
        assert calculate_shipping(100, express=True) == Decimal("25.00")

    def test_express_shipping_zero_total(self):
        assert calculate_shipping(0, express=True) == Decimal("25.00")


class TestCalculateShippingInputTypes:
    def test_accepts_decimal_input(self):
        assert calculate_shipping(Decimal("150")) == Decimal("0.00")

    def test_accepts_string_numeric_input(self):
        assert calculate_shipping("150") == Decimal("0.00")

    def test_accepts_float_input(self):
        assert calculate_shipping(99.5) == Decimal("10.00")


class TestCalculateShippingInvalid:
    def test_negative_order_total_raises_value_error(self):
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_shipping(-1)

    def test_negative_order_total_with_express_raises_value_error(self):
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_shipping(-50, express=True)

    def test_large_negative_order_total_raises_value_error(self):
        with pytest.raises(ValueError, match="Order total cannot be negative"):
            calculate_shipping(-1000)
