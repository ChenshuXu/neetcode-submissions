"""Follow-up 1: merge duplicate cart lines before base validation."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class CartLine:
    item_id: str
    quantity: object


@dataclass
class InventoryItem:
    item_id: str
    available_quantity: int
    min_quantity: int
    max_quantity: int


class ValidationCode(Enum):
    EMPTY_CART = "empty_cart"
    INVALID_QUANTITY = "invalid_quantity"
    ITEM_UNAVAILABLE = "item_unavailable"
    BELOW_MINIMUM = "below_minimum"
    ABOVE_MAXIMUM = "above_maximum"
    INSUFFICIENT_INVENTORY = "insufficient_inventory"


@dataclass
class CartValidationError:
    code: ValidationCode
    item_id: Optional[str] = None
    requested_quantity: Optional[object] = None
    allowed_quantity: Optional[int] = None


@dataclass
class CartValidationResult:
    errors: tuple[CartValidationError, ...]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def merge_duplicate_lines(lines: list[CartLine]) -> list[CartLine]:
    totals = {}
    for line in lines:
        if type(line.quantity) is not int or line.quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        totals[line.item_id] = totals.get(line.item_id, 0) + line.quantity

    return [CartLine(item_id, quantity) for item_id, quantity in totals.items()]


class CartValidator:
    def validate_cart(
        self,
        lines: list[CartLine],
        inventory: dict[str, InventoryItem],
    ) -> CartValidationResult:
        if not lines:
            return CartValidationResult(
                (CartValidationError(ValidationCode.EMPTY_CART),)
            )

        errors = []
        for line in lines:
            quantity = line.quantity
            if type(quantity) is not int or quantity <= 0:
                errors.append(
                    CartValidationError(
                        ValidationCode.INVALID_QUANTITY,
                        line.item_id,
                        quantity,
                    )
                )
                continue

            item = inventory.get(line.item_id)
            if item is None:
                errors.append(
                    CartValidationError(
                        ValidationCode.ITEM_UNAVAILABLE,
                        line.item_id,
                        quantity,
                    )
                )
                continue

            if quantity < item.min_quantity:
                errors.append(
                    CartValidationError(
                        ValidationCode.BELOW_MINIMUM,
                        line.item_id,
                        quantity,
                        item.min_quantity,
                    )
                )
            if quantity > item.max_quantity:
                errors.append(
                    CartValidationError(
                        ValidationCode.ABOVE_MAXIMUM,
                        line.item_id,
                        quantity,
                        item.max_quantity,
                    )
                )
            if quantity > item.available_quantity:
                errors.append(
                    CartValidationError(
                        ValidationCode.INSUFFICIENT_INVENTORY,
                        line.item_id,
                        quantity,
                        item.available_quantity,
                    )
                )

        return CartValidationResult(tuple(errors))


def main() -> None:
    lines = [CartLine("apple", 1), CartLine("soup", 2), CartLine("apple", 3)]
    merged = merge_duplicate_lines(lines)
    assert merged == [CartLine("apple", 4), CartLine("soup", 2)]

    inventory = {
        "apple": InventoryItem("apple", 8, 1, 5),
        "soup": InventoryItem("soup", 2, 2, 4),
    }
    result = CartValidator().validate_cart(merged, inventory)
    assert result.is_valid
    print(merged)


if __name__ == "__main__":
    main()
