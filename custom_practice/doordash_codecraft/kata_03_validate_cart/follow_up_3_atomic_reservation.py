"""Follow-up 3: atomically reserve every item or reserve nothing."""

from dataclasses import dataclass
from enum import Enum
from threading import Lock
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
    BELOW_CART_MINIMUM = "below_cart_minimum"
    ABOVE_CART_MAXIMUM = "above_cart_maximum"


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


@dataclass
class ReservationResult:
    state: str
    errors: tuple[CartValidationError, ...] = ()


@dataclass
class CartResponse:
    validation: CartValidationResult
    reservation: Optional[ReservationResult]


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
        min_cart_quantity: int,
        max_cart_quantity: int,
    ) -> CartValidationResult:
        if not lines:
            return CartValidationResult(
                (CartValidationError(ValidationCode.EMPTY_CART),)
            )

        errors = []
        total_quantity = 0

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

            total_quantity += quantity
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

        if total_quantity < min_cart_quantity:
            errors.append(
                CartValidationError(
                    ValidationCode.BELOW_CART_MINIMUM,
                    requested_quantity=total_quantity,
                    allowed_quantity=min_cart_quantity,
                )
            )
        if total_quantity > max_cart_quantity:
            errors.append(
                CartValidationError(
                    ValidationCode.ABOVE_CART_MAXIMUM,
                    requested_quantity=total_quantity,
                    allowed_quantity=max_cart_quantity,
                )
            )

        return CartValidationResult(tuple(errors))


class InventoryGateway:
    def __init__(self, inventories: dict[str, dict[str, InventoryItem]]) -> None:
        self._inventories = {}
        for restaurant_id, items in inventories.items():
            self._inventories[restaurant_id] = {
                item_id: InventoryItem(
                    item.item_id,
                    item.available_quantity,
                    item.min_quantity,
                    item.max_quantity,
                )
                for item_id, item in items.items()
            }
        # ponytail: process-local lock; use a DB transaction across instances.
        self._lock = Lock()

    def snapshot(self, restaurant_id: str) -> dict[str, InventoryItem]:
        with self._lock:
            items = self._inventories.get(restaurant_id, {})
            return {
                item_id: InventoryItem(
                    item.item_id,
                    item.available_quantity,
                    item.min_quantity,
                    item.max_quantity,
                )
                for item_id, item in items.items()
            }

    def reserve(
        self,
        restaurant_id: str,
        quantities: dict[str, int],
    ) -> ReservationResult:
        if not restaurant_id or not quantities or any(
            not item_id or type(quantity) is not int or quantity <= 0
            for item_id, quantity in quantities.items()
        ):
            raise ValueError("reservation quantities are invalid")

        with self._lock:
            inventory = self._inventories.get(restaurant_id, {})
            errors = []

            for item_id, requested in quantities.items():
                item = inventory.get(item_id)
                available = item.available_quantity if item else 0
                if requested > available:
                    errors.append(
                        CartValidationError(
                            ValidationCode.INSUFFICIENT_INVENTORY,
                            item_id,
                            requested,
                            available,
                        )
                    )

            if errors:
                return ReservationResult("rejected", tuple(errors))

            for item_id, requested in quantities.items():
                inventory[item_id].available_quantity -= requested

            return ReservationResult("held")


class CartService:
    def __init__(self, gateway: InventoryGateway) -> None:
        self._gateway = gateway
        self._validator = CartValidator()

    def reserve_cart(
        self,
        restaurant_id: str,
        lines: list[CartLine],
        min_cart_quantity: int,
        max_cart_quantity: int,
    ) -> CartResponse:
        lines = merge_duplicate_lines(lines)
        snapshot = self._gateway.snapshot(restaurant_id)
        validation = self._validator.validate_cart(
            lines,
            snapshot,
            min_cart_quantity,
            max_cart_quantity,
        )
        if not validation.is_valid:
            return CartResponse(validation, None)

        quantities = {line.item_id: line.quantity for line in lines}
        reservation = self._gateway.reserve(restaurant_id, quantities)
        if reservation.state == "rejected":
            validation = CartValidationResult(reservation.errors)
        return CartResponse(validation, reservation)


def main() -> None:
    inventory = {
        "apple": InventoryItem("apple", 1, 1, 5),
        "soup": InventoryItem("soup", 0, 1, 5),
    }
    gateway = InventoryGateway({"restaurant-1": inventory})
    result = gateway.reserve("restaurant-1", {"apple": 1, "soup": 1})

    assert result.state == "rejected"
    assert gateway.snapshot("restaurant-1")["apple"].available_quantity == 1
    print(result)


if __name__ == "__main__":
    main()
