import unittest

from validate_cart import (
    CartLine,
    CartValidationError,
    CartValidationResult,
    CartValidator,
    InventoryItem,
    ValidationCode,
)


INVENTORY = {
    "apple": InventoryItem("apple", available_quantity=8, min_quantity=1, max_quantity=5),
    "soup": InventoryItem("soup", available_quantity=2, min_quantity=2, max_quantity=4),
    "cake": InventoryItem("cake", available_quantity=10, min_quantity=1, max_quantity=3),
    "noodles": InventoryItem(
        "noodles",
        available_quantity=2,
        min_quantity=1,
        max_quantity=5,
    ),
}


class CartValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = CartValidator()

    def test_valid_cart_accepts_inclusive_minimum_and_maximum(self):
        result = self.validator.validate_cart(
            [CartLine("apple", 5), CartLine("soup", 2)],
            INVENTORY,
        )

        self.assertEqual(CartValidationResult(errors=()), result)
        self.assertTrue(result.is_valid)

    def test_empty_cart_is_invalid(self):
        result = self.validator.validate_cart([], INVENTORY)

        self.assertEqual(
            (
                CartValidationError(code=ValidationCode.EMPTY_CART),
            ),
            result.errors,
        )

    def test_quantity_must_be_a_positive_integer(self):
        result = self.validator.validate_cart([CartLine("apple", 0)], INVENTORY)

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.INVALID_QUANTITY,
                    item_id="apple",
                    requested_quantity=0,
                ),
            ),
            result.errors,
        )

    def test_duplicate_item_is_reported_once(self):
        result = self.validator.validate_cart(
            [CartLine("apple", 1), CartLine("soup", 2), CartLine("apple", 2)],
            INVENTORY,
        )

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.DUPLICATE_ITEM,
                    item_id="apple",
                ),
            ),
            result.errors,
        )

    def test_missing_inventory_item_is_unavailable(self):
        result = self.validator.validate_cart([CartLine("salad", 1)], INVENTORY)

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.ITEM_UNAVAILABLE,
                    item_id="salad",
                    requested_quantity=1,
                ),
            ),
            result.errors,
        )

    def test_quantity_below_item_minimum(self):
        result = self.validator.validate_cart([CartLine("soup", 1)], INVENTORY)

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.BELOW_MINIMUM,
                    item_id="soup",
                    requested_quantity=1,
                    allowed_quantity=2,
                ),
            ),
            result.errors,
        )

    def test_quantity_above_item_maximum(self):
        result = self.validator.validate_cart([CartLine("cake", 4)], INVENTORY)

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.ABOVE_MAXIMUM,
                    item_id="cake",
                    requested_quantity=4,
                    allowed_quantity=3,
                ),
            ),
            result.errors,
        )

    def test_quantity_above_available_inventory(self):
        result = self.validator.validate_cart([CartLine("noodles", 3)], INVENTORY)

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.INSUFFICIENT_INVENTORY,
                    item_id="noodles",
                    requested_quantity=3,
                    allowed_quantity=2,
                ),
            ),
            result.errors,
        )

    def test_returns_all_errors_in_first_seen_rule_order(self):
        result = self.validator.validate_cart(
            [
                CartLine("soup", 1),
                CartLine("salad", 1),
                CartLine("apple", 9),
            ],
            INVENTORY,
        )

        self.assertEqual(
            (
                CartValidationError(
                    code=ValidationCode.BELOW_MINIMUM,
                    item_id="soup",
                    requested_quantity=1,
                    allowed_quantity=2,
                ),
                CartValidationError(
                    code=ValidationCode.ITEM_UNAVAILABLE,
                    item_id="salad",
                    requested_quantity=1,
                ),
                CartValidationError(
                    code=ValidationCode.ABOVE_MAXIMUM,
                    item_id="apple",
                    requested_quantity=9,
                    allowed_quantity=5,
                ),
                CartValidationError(
                    code=ValidationCode.INSUFFICIENT_INVENTORY,
                    item_id="apple",
                    requested_quantity=9,
                    allowed_quantity=8,
                ),
            ),
            result.errors,
        )


if __name__ == "__main__":
    unittest.main()
