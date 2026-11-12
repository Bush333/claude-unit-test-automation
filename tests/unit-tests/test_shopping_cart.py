import pytest

from src.shopping_cart import calculate_discount


from decimal import Decimal

import pytest

from src.shopping_cart import calculate_shipping
from src.shopping_cart import calculate_tax
from src.shopping_cart import apply_store_credit
from src.shopping_cart import calculate_bogo_discount


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


class TestCalculateTax:
    def test_normal_case(self):
        assert calculate_tax(100, 10) == 10.0

    def test_zero_tax_rate(self):
        assert calculate_tax(100, 0) == 0.0

    def test_full_tax_rate(self):
        assert calculate_tax(100, 100) == 100.0

    def test_zero_subtotal(self):
        assert calculate_tax(0, 50) == 0.0

    def test_rounding(self):
        assert calculate_tax(99.99, 33) == round(99.99 * 33 / 100, 2)

    def test_float_subtotal(self):
        assert calculate_tax(49.5, 20) == round(49.5 * 20 / 100, 2)

    def test_boundary_tax_rate_values(self):
        assert calculate_tax(200, 0) == 0.0
        assert calculate_tax(200, 100) == 200.0

    def test_negative_subtotal_raises(self):
        with pytest.raises(ValueError, match="Subtotal cannot be negative"):
            calculate_tax(-1, 10)

    def test_negative_tax_rate_raises(self):
        with pytest.raises(ValueError, match="Tax rate must be between 0 and 100"):
            calculate_tax(100, -1)

    def test_tax_rate_over_100_raises(self):
        with pytest.raises(ValueError, match="Tax rate must be between 0 and 100"):
            calculate_tax(100, 101)


class TestApplyStoreCredit:
    def test_normal_case_credit_less_than_total(self):
        assert apply_store_credit(100, 30) == 70.0

    def test_credit_equal_to_total_results_in_zero(self):
        assert apply_store_credit(100, 100) == 0.0

    def test_credit_greater_than_total_floors_at_zero(self):
        assert apply_store_credit(50, 100) == 0.0

    def test_zero_credit_returns_total_unchanged(self):
        assert apply_store_credit(100, 0) == 100.0

    def test_zero_total_with_credit_returns_zero(self):
        assert apply_store_credit(0, 50) == 0.0

    def test_zero_total_and_zero_credit(self):
        assert apply_store_credit(0, 0) == 0.0

    def test_rounding_behavior(self):
        assert apply_store_credit(99.995, 10) == round(max(99.995 - 10, 0), 2)

    def test_float_inputs(self):
        assert apply_store_credit(49.5, 20.25) == round(49.5 - 20.25, 2)

    def test_negative_total_raises_value_error(self):
        with pytest.raises(ValueError, match="Total cannot be negative"):
            apply_store_credit(-1, 10)

    def test_negative_credit_raises_value_error(self):
        with pytest.raises(ValueError, match="Store credit cannot be negative"):
            apply_store_credit(100, -5)

    def test_both_negative_raises_total_error_first(self):
        with pytest.raises(ValueError, match="Total cannot be negative"):
            apply_store_credit(-10, -5)

    def test_large_credit_still_floors_at_zero(self):
        assert apply_store_credit(10, 1000) == 0.0


class TestCalculateBogoDiscount:
    def test_example_buy2_get1_free(self):
        assert calculate_bogo_discount(100, 6) == 200

    def test_default_buy_qty_and_free_qty(self):
        assert calculate_bogo_discount(50, 3) == 50

    def test_quantity_exact_multiple_of_group_size(self):
        assert calculate_bogo_discount(10, 9) == 30

    def test_quantity_not_multiple_of_group_size_partial_group_no_discount(self):
        assert calculate_bogo_discount(10, 8) == 20

    def test_quantity_less_than_group_size_no_discount(self):
        assert calculate_bogo_discount(100, 2) == 0

    def test_zero_quantity_no_discount(self):
        assert calculate_bogo_discount(100, 0) == 0

    def test_zero_unit_price_no_discount_amount(self):
        assert calculate_bogo_discount(0, 6) == 0

    def test_custom_buy_qty_and_free_qty(self):
        assert calculate_bogo_discount(10, 10, buy_qty=3, free_qty=2) == 40

    def test_custom_buy1_get1_free(self):
        assert calculate_bogo_discount(20, 5, buy_qty=1, free_qty=1) == 40

    def test_rounding_behavior(self):
        assert calculate_bogo_discount(10.555, 3) == round(10.555, 2)

    def test_float_unit_price(self):
        assert calculate_bogo_discount(9.99, 6) == round(9.99 * 2, 2)

    def test_large_quantity(self):
        assert calculate_bogo_discount(5, 300) == 500

    def test_negative_unit_price_raises_value_error(self):
        with pytest.raises(ValueError, match="Unit price cannot be negative"):
            calculate_bogo_discount(-1, 6)

    def test_negative_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bogo_discount(100, -1)

    def test_float_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bogo_discount(100, 6.5)

    def test_bool_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bogo_discount(100, True)

    def test_zero_buy_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Buy quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, buy_qty=0)

    def test_negative_buy_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Buy quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, buy_qty=-2)

    def test_float_buy_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Buy quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, buy_qty=2.5)

    def test_bool_buy_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Buy quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, buy_qty=True)

    def test_zero_free_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Free quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, free_qty=0)

    def test_negative_free_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Free quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, free_qty=-1)

    def test_float_free_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Free quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, free_qty=1.5)

    def test_bool_free_qty_raises_value_error(self):
        with pytest.raises(ValueError, match="Free quantity must be a positive integer"):
            calculate_bogo_discount(100, 6, free_qty=True)
