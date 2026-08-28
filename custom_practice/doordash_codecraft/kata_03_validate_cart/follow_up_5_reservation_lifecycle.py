"""Follow-up 5: confirm, release, or expire an idempotent hold."""

from dataclasses import dataclass
from datetime import datetime, timedelta
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
    request_id: str
    reservation_id: Optional[str]
    state: str
    errors: tuple[CartValidationError, ...] = ()
    expires_at: Optional[datetime] = None


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
    def __init__(
        self,
        inventories: dict[str, dict[str, InventoryItem]],
        lease_minutes: int = 5,
    ) -> None:
        if lease_minutes <= 0:
            raise ValueError("lease_minutes must be positive")
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
        self._requests = {}
        self._reservations = {}
        self._reserved_quantities = {}
        self._next_reservation_id = 1
        self._lease_duration = timedelta(minutes=lease_minutes)
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
        request_id: str,
        restaurant_id: str,
        quantities: dict[str, int],
        now: datetime,
    ) -> ReservationResult:
        if not request_id or not restaurant_id or not quantities or any(
            not item_id or type(quantity) is not int or quantity <= 0
            for item_id, quantity in quantities.items()
        ):
            raise ValueError("reservation request is invalid")
        fingerprint = (restaurant_id, tuple(sorted(quantities.items())))

        with self._lock:
            previous = self._requests.get(request_id)
            if previous is not None:
                previous_fingerprint, previous_result = previous
                if previous_fingerprint != fingerprint:
                    raise ValueError("request_id was reused with different data")
                return previous_result

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
                result = ReservationResult(
                    request_id,
                    None,
                    "rejected",
                    tuple(errors),
                )
                self._requests[request_id] = (fingerprint, result)
                return result

            for item_id, requested in quantities.items():
                inventory[item_id].available_quantity -= requested

            reservation_id = f"reservation-{self._next_reservation_id}"
            self._next_reservation_id += 1
            result = ReservationResult(
                request_id,
                reservation_id,
                "held",
                expires_at=now + self._lease_duration,
            )
            self._requests[request_id] = (fingerprint, result)
            self._reservations[reservation_id] = result
            self._reserved_quantities[reservation_id] = (
                restaurant_id,
                dict(quantities),
            )
            return result

    def confirm(self, reservation_id: str, now: datetime) -> ReservationResult:
        with self._lock:
            reservation = self._get_reservation(reservation_id)
            self._expire_if_due(reservation, now)

            if reservation.state == "confirmed":
                return reservation
            if reservation.state == "held":
                reservation.state = "confirmed"
                return reservation
            if reservation.state == "expired":
                return reservation
            raise ValueError(f"cannot confirm a {reservation.state} reservation")

    def release(self, reservation_id: str) -> ReservationResult:
        with self._lock:
            reservation = self._get_reservation(reservation_id)
            if reservation.state in ("released", "expired"):
                return reservation
            if reservation.state == "confirmed":
                raise ValueError("confirmed inventory cannot be released")

            self._restore_inventory(reservation_id)
            reservation.state = "released"
            return reservation

    def expire_due(self, now: datetime) -> list[ReservationResult]:
        expired = []
        with self._lock:
            for reservation in self._reservations.values():
                old_state = reservation.state
                self._expire_if_due(reservation, now)
                if old_state == "held" and reservation.state == "expired":
                    expired.append(reservation)
        return expired

    def _get_reservation(self, reservation_id: str) -> ReservationResult:
        reservation = self._reservations.get(reservation_id)
        if reservation is None:
            raise KeyError(reservation_id)
        return reservation

    def _expire_if_due(
        self,
        reservation: ReservationResult,
        now: datetime,
    ) -> None:
        if (
            reservation.state == "held"
            and reservation.expires_at is not None
            and now >= reservation.expires_at
        ):
            self._restore_inventory(reservation.reservation_id)
            reservation.state = "expired"

    def _restore_inventory(self, reservation_id: str) -> None:
        restaurant_id, quantities = self._reserved_quantities.pop(reservation_id)
        inventory = self._inventories[restaurant_id]
        for item_id, quantity in quantities.items():
            inventory[item_id].available_quantity += quantity


class CartService:
    def __init__(self, gateway: InventoryGateway) -> None:
        self._gateway = gateway
        self._validator = CartValidator()

    def reserve_cart(
        self,
        request_id: str,
        restaurant_id: str,
        lines: list[CartLine],
        min_cart_quantity: int,
        max_cart_quantity: int,
        now: datetime,
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
        reservation = self._gateway.reserve(
            request_id,
            restaurant_id,
            quantities,
            now,
        )
        if reservation.state == "rejected":
            validation = CartValidationResult(reservation.errors)
        return CartResponse(validation, reservation)


def main() -> None:
    now = datetime(2026, 8, 28, 12, 0)
    inventory = {
        "apple": InventoryItem("apple", 3, 1, 5),
    }
    gateway = InventoryGateway({"restaurant-1": inventory})
    first = gateway.reserve("request-1", "restaurant-1", {"apple": 2}, now)
    gateway.release(first.reservation_id)
    gateway.release(first.reservation_id)
    assert gateway.snapshot("restaurant-1")["apple"].available_quantity == 3

    second = gateway.reserve("request-2", "restaurant-1", {"apple": 2}, now)
    gateway.confirm(second.reservation_id, now + timedelta(minutes=5))
    assert second.state == "expired"
    assert gateway.snapshot("restaurant-1")["apple"].available_quantity == 3

    third = gateway.reserve(
        "request-3",
        "restaurant-1",
        {"apple": 2},
        now + timedelta(minutes=6),
    )
    gateway.confirm(third.reservation_id, now + timedelta(minutes=7))
    gateway.expire_due(now + timedelta(minutes=20))
    assert third.state == "confirmed"
    assert gateway.snapshot("restaurant-1")["apple"].available_quantity == 1
    print(first.state, second.state, third.state)


if __name__ == "__main__":
    main()
