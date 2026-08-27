"""Held-back checks for the fixed training contract.

Candidate: do not open or run this file during a cold attempt. These checks do
not add undisclosed rules; they exercise the clarification answers in
INTERVIEWER_PACKET.md.
"""

import unittest

from validate_cart import (
    CartLine,
    CartValidationError,
    CartValidator,
    InventoryItem,
    ValidationCode,
)


INVENTORY = {
    "apple": InventoryItem("apple", available_quantity=8, min_quantity=1, max_quantity=5),
    "soup": InventoryItem("soup", available_quantity=2, min_quantity=2, max_quantity=4),
}


class HeldBackValidateCartChecks(unittest.TestCase):
    def setUp(self):
        self.validator = CartValidator()

    def test_boolean_and_float_quantities_are_not_integers_for_this_contract(self):
        for quantity in (True, 1.0):
            with self.subTest(quantity=quantity):
                result = self.validator.validate_cart(
                    [CartLine("apple", quantity)],
                    INVENTORY,
                )

                self.assertEqual(ValidationCode.INVALID_QUANTITY, result.errors[0].code)

    def test_three_occurrences_still_produce_one_duplicate_error(self):
        result = self.validator.validate_cart(
            [
                CartLine("apple", 1),
                CartLine("apple", 2),
                CartLine("apple", 3),
            ],
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

    def test_duplicate_precedence_avoids_guessing_a_quantity_to_validate(self):
        result = self.validator.validate_cart(
            [CartLine("apple", 0), CartLine("apple", 20)],
            INVENTORY,
        )

        self.assertEqual([ValidationCode.DUPLICATE_ITEM], [error.code for error in result.errors])

    def test_rule_order_is_minimum_then_maximum_then_inventory(self):
        constrained = {
            "apple": InventoryItem(
                "apple",
                available_quantity=0,
                min_quantity=2,
                max_quantity=5,
            )
        }

        result = self.validator.validate_cart([CartLine("apple", 1)], constrained)

        self.assertEqual(
            [ValidationCode.BELOW_MINIMUM, ValidationCode.INSUFFICIENT_INVENTORY],
            [error.code for error in result.errors],
        )

    def test_validation_does_not_mutate_inputs(self):
        lines = [CartLine("apple", 2)]
        inventory = dict(INVENTORY)
        original_lines = list(lines)
        original_inventory = dict(inventory)

        self.validator.validate_cart(lines, inventory)

        self.assertEqual(original_lines, lines)
        self.assertEqual(original_inventory, inventory)

    def test_unreferenced_inventory_items_do_not_affect_the_result(self):
        result = self.validator.validate_cart([CartLine("apple", 2)], INVENTORY)

        self.assertTrue(result.is_valid)
        self.assertEqual((), result.errors)


if __name__ == "__main__":
    unittest.main()
