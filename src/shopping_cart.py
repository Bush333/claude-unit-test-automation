# CI notification verification
from decimal import Decimal


def calculate_total(items, discount_percent=0, tax_percent=0):
    """
    Calculate the total price of a shopping cart.

    items: list of dictionaries with price and quantity.
    discount_percent: discount applied before tax.
    tax_percent: tax applied after discount.
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    if tax_percent < 0:
        raise ValueError("Tax cannot be negative")

    subtotal = Decimal("0")

    for item in items:
        price = Decimal(str(item["price"]))
        quantity = item["quantity"]

        if price < 0:
            raise ValueError("Price cannot be negative")

        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        subtotal += price * quantity

    discount = subtotal * Decimal(str(discount_percent)) / 100
    discounted_total = subtotal - discount

    tax = discounted_total * Decimal(str(tax_percent)) / 100

    return round(discounted_total + tax, 2)

def calculate_shipping(order_total, express=False):
    """
    Calculate shipping cost.

    Standard shipping:
      - Free for orders >= 100
      - 10 for orders below 100

    Express shipping:
      - 25 for all orders

    Negative order totals are invalid.
    """
    order_total = Decimal(str(order_total))

    if order_total < 0:
        raise ValueError("Order total cannot be negative")

    if express:
        return Decimal("25.00")

    if order_total >= 100:
        return Decimal("0.00")

    return Decimal("10.00")
def apply_coupon(total, coupon_code):
    """Apply a coupon to the cart total."""
    coupons = {
        "SAVE10": Decimal("0.10"),
        "SAVE20": Decimal("0.20"),
        "FLAT50": Decimal("50"),
    }

    total = Decimal(str(total))
    coupon_code = coupon_code.upper()

    if coupon_code not in coupons:
        raise ValueError("Invalid coupon code")

    if coupon_code == "FLAT50":
        return max(Decimal("0"), total - coupons[coupon_code])

    return round(total * (1 - coupons[coupon_code]), 2)
def calculate_discount(total, discount_percent):
    if total < 0:
        raise ValueError("Total cannot be negative")

    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    return round(total * (1 - discount_percent / 100), 2)

def calculate_tax(subtotal, tax_rate):
    """Calculate tax amount for a subtotal and percentage rate."""
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")

    if not 0 <= tax_rate <= 100:
        raise ValueError("Tax rate must be between 0 and 100")

    return round(subtotal * tax_rate / 100, 2)

def apply_store_credit(total, credit):
    """Apply store credit without allowing a negative payable amount."""
    if total < 0:
        raise ValueError("Total cannot be negative")

    if credit < 0:
        raise ValueError("Store credit cannot be negative")

    return round(max(total - credit, 0), 2)


