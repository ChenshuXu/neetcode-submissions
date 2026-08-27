"""Starter code for the DoorDash-style Dasher Pay kata.

Implement PayoutService.get_payout. Keep the public contract stable unless you
first agree on a change with the interviewer.
"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Protocol, Sequence


class DeliveryStatus(Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ACTIVE = "active"


@dataclass(frozen=True)
class Delivery:
    delivery_id: str
    accepted_at: datetime
    completed_at: Optional[datetime]
    status: DeliveryStatus


@dataclass(frozen=True)
class PayoutResponse:
    dasher_id: str
    amount: Decimal
    completed_delivery_count: int


class DeliveryClient(Protocol):
    def list_deliveries(self, dasher_id: str) -> Sequence[Delivery]:
        """Return deliveries associated with one dasher."""


class DeliveryClientError(RuntimeError):
    """The upstream delivery service could not serve the request."""


class InvalidRequestError(ValueError):
    """The endpoint-like request is invalid."""


class InvalidDeliveryError(ValueError):
    """A completed delivery contains an invalid time interval."""


class PayoutUnavailableError(RuntimeError):
    """A stable service-level error for an unavailable payout calculation."""


class PayoutService:
    def __init__(
        self,
        delivery_client: DeliveryClient,
        rate_per_active_minute: Decimal = Decimal("0.30"),
    ) -> None:
        if rate_per_active_minute < Decimal("0"):
            raise ValueError("rate_per_active_minute must be non-negative")

        # Injected upstream port used to load this dasher's delivery records.
        self._delivery_client = delivery_client

        # Exact Decimal dollars paid for one active delivery-minute.
        self._rate_per_active_minute = rate_per_active_minute

    def get_payout(self, dasher_id: str) -> PayoutResponse:
        """Calculate payout for completed deliveries.

        Start with the smallest correct vertical slice. Add private helpers only
        when they make a named rule easier to test or explain.
        """
        raise NotImplementedError("Implement PayoutService.get_payout")
