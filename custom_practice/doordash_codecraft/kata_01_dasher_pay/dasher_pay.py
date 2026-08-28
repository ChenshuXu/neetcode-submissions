"""Base: calculate pay for completed deliveries.

Evolution role:
- Establish the simple row-based payout calculation.
- Filter completed deliveries and sum each duration independently.
- Later Follow-ups keep this pay rule and add one new concern at a time.

Timestamps are whole-minute integers and money is integer cents so the
interview version needs no Decimal or rounding library.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


RATE_CENTS_PER_MINUTE = 30


class DeliveryStatus(Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ACTIVE = "active"


@dataclass
class Delivery:
    delivery_id: str
    accepted_at: int
    completed_at: Optional[int]
    status: DeliveryStatus


@dataclass
class PayoutResponse:
    dasher_id: str
    amount_cents: int
    completed_delivery_count: int


class DeliveryClientError(RuntimeError):
    pass


class InvalidDeliveryError(ValueError):
    pass


class PayoutUnavailableError(RuntimeError):
    pass


class PayoutService:
    def __init__(self, delivery_client):
        self.delivery_client = delivery_client

    def get_payout(self, dasher_id):
        if not isinstance(dasher_id, str) or not dasher_id.strip():
            raise ValueError("dasher_id must not be blank")

        try:
            deliveries = self.delivery_client.list_deliveries(dasher_id)
        except DeliveryClientError as error:
            raise PayoutUnavailableError("delivery service unavailable") from error

        # Base algorithm: each completed delivery contributes its own duration.
        # Overlapping deliveries are counted independently.
        amount_cents = 0
        completed_count = 0

        for delivery in deliveries:
            if delivery.status is not DeliveryStatus.COMPLETED:
                continue
            if (
                delivery.completed_at is None
                or delivery.completed_at <= delivery.accepted_at
            ):
                raise InvalidDeliveryError(delivery.delivery_id)

            minutes = delivery.completed_at - delivery.accepted_at
            amount_cents += minutes * RATE_CENTS_PER_MINUTE
            completed_count += 1

        return PayoutResponse(dasher_id, amount_cents, completed_count)


class FakeDeliveryClient:
    def __init__(self, deliveries):
        self.deliveries = deliveries

    def list_deliveries(self, dasher_id):
        return self.deliveries


def main():
    deliveries = [
        Delivery("d1", 0, 15, DeliveryStatus.COMPLETED),
        Delivery("d2", 5, 15, DeliveryStatus.COMPLETED),
        Delivery("d3", 0, None, DeliveryStatus.ACTIVE),
    ]
    result = PayoutService(FakeDeliveryClient(deliveries)).get_payout("dasher-1")
    assert result == PayoutResponse("dasher-1", 750, 2)
    print(result)


if __name__ == "__main__":
    main()
