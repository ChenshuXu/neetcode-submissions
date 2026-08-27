"""Starter code for the DoorDash-style Validate Cart kata.

Implement CartValidator.validate_cart. The base exercise is intentionally a
pure validator: it reports user-correctable problems but does not mutate or
reserve inventory.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Sequence, Tuple


@dataclass(frozen=True)
class CartLine:
    item_id: str
    quantity: object


@dataclass(frozen=True)
class InventoryItem:
    item_id: str
    available_quantity: int
    min_quantity: int
    max_quantity: int


class ValidationCode(Enum):
    EMPTY_CART = "empty_cart"
    INVALID_QUANTITY = "invalid_quantity"
    DUPLICATE_ITEM = "duplicate_item"
    ITEM_UNAVAILABLE = "item_unavailable"
    BELOW_MINIMUM = "below_minimum"
    ABOVE_MAXIMUM = "above_maximum"
    INSUFFICIENT_INVENTORY = "insufficient_inventory"


@dataclass(frozen=True)
class CartValidationError:
    code: ValidationCode
    item_id: Optional[str] = None
    requested_quantity: Optional[object] = None
    allowed_quantity: Optional[int] = None


@dataclass(frozen=True)
class CartValidationResult:
    errors: Tuple[CartValidationError, ...]

    @property
    def is_valid(self) -> bool:
        return not self.errors


class CartValidator:
    def validate_cart(
        self,
        lines: Sequence[CartLine],
        inventory: Mapping[str, InventoryItem],
    ) -> CartValidationResult:
        """Return every applicable validation error in deterministic order."""
        raise NotImplementedError("Implement CartValidator.validate_cart")
