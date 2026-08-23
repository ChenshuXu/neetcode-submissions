from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from dasher_pay import (
    Delivery,
    DeliveryStatus,
    InvalidDeliveryError,
    PayoutResponse,
    PayoutService,
)


BASE_TIME = datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc)


def completed(
    delivery_id: str,
    accepted_minute: int,
    completed_minute: int,
) -> Delivery:
    return Delivery(
        delivery_id=delivery_id,
        accepted_at=BASE_TIME + timedelta(minutes=accepted_minute),
        completed_at=BASE_TIME + timedelta(minutes=completed_minute),
        status=DeliveryStatus.COMPLETED,
    )


class FakeDeliveryClient:
    def __init__(self, deliveries=(), error=None) -> None:
        self.deliveries = tuple(deliveries)
        self.error = error
        self.calls = []

    def list_deliveries(self, dasher_id):
        self.calls.append(dasher_id)
        if self.error is not None:
            raise self.error
        return self.deliveries


class PayoutServiceTests(unittest.TestCase):
    def test_one_completed_delivery(self):
        client = FakeDeliveryClient([completed("d-1", 0, 10)])

        result = PayoutService(client).get_payout("dasher-1")

        self.assertEqual(
            PayoutResponse(
                dasher_id="dasher-1",
                amount=Decimal("3.00"),
                completed_delivery_count=1,
            ),
            result,
        )
        self.assertEqual(["dasher-1"], client.calls)

    def test_overlapping_deliveries_pay_for_each_active_delivery_minute(self):
        client = FakeDeliveryClient(
            [
                completed("d-1", 0, 15),
                completed("d-2", 5, 15),
            ]
        )

        result = PayoutService(client).get_payout("dasher-1")

        self.assertEqual(Decimal("7.50"), result.amount)

    def test_zero_deliveries(self):
        result = PayoutService(FakeDeliveryClient()).get_payout("dasher-1")

        self.assertEqual(Decimal("0.00"), result.amount)
        self.assertEqual(0, result.completed_delivery_count)

    def test_completed_delivery_requires_a_positive_interval(self):
        client = FakeDeliveryClient([completed("d-1", 10, 10)])

        with self.assertRaises(InvalidDeliveryError):
            PayoutService(client).get_payout("dasher-1")

if __name__ == "__main__":
    unittest.main()
