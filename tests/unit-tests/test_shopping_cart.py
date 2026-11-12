import pytest

from src.shopping_cart import calculate_discount


from decimal import Decimal

import pytest

from src.shopping_cart import calculate_shipping
from src.shopping_cart import calculate_tax
from src.shopping_cart import apply_store_credit
from src.shopping_cart import calculate_bulk_discount

def test_slack_failure_notification():
    """Temporary test to verify Slack failure notifications."""
    assert False, "Intentional failure to test Slack notification"


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


class TestCalculateBulkDiscount:
    def test_no_discount_for_one_item(self):
        assert calculate_bulk_discount(10, 1) == 10.0

    def test_no_discount_just_below_five_items(self):
        assert calculate_bulk_discount(10, 4) == 40.0

    def test_five_percent_discount_at_lower_boundary(self):
        assert calculate_bulk_discount(10, 5) == round(10 * 5 * 0.95, 2)

    def test_five_percent_discount_just_below_ten_items(self):
        assert calculate_bulk_discount(10, 9) == round(10 * 9 * 0.95, 2)

    def test_ten_percent_discount_at_lower_boundary(self):
        assert calculate_bulk_discount(10, 10) == round(10 * 10 * 0.90, 2)

    def test_ten_percent_discount_just_below_twenty_items(self):
        assert calculate_bulk_discount(10, 19) == round(10 * 19 * 0.90, 2)

    def test_fifteen_percent_discount_at_lower_boundary(self):
        assert calculate_bulk_discount(10, 20) == round(10 * 20 * 0.85, 2)

    def test_fifteen_percent_discount_well_above_boundary(self):
        assert calculate_bulk_discount(10, 100) == round(10 * 100 * 0.85, 2)

    def test_zero_quantity_returns_zero(self):
        assert calculate_bulk_discount(10, 0) == 0.0

    def test_zero_unit_price_returns_zero_regardless_of_quantity(self):
        assert calculate_bulk_discount(0, 25) == 0.0

    def test_float_unit_price_rounding(self):
        assert calculate_bulk_discount(9.99, 5) == round(9.99 * 5 * 0.95, 2)

    def test_negative_unit_price_raises_value_error(self):
        with pytest.raises(ValueError, match="Unit price cannot be negative"):
            calculate_bulk_discount(-1, 5)

    def test_negative_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bulk_discount(10, -1)

    def test_non_integer_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bulk_discount(10, 5.5)

    def test_boolean_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bulk_discount(10, True)

    def test_string_quantity_raises_value_error(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
            calculate_bulk_discount(10, "5")
