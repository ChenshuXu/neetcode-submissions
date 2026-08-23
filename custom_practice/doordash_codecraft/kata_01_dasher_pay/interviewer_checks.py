"""Held-back contract checks.

Candidate: do not open or run this file during a cold attempt. The interviewer
runs it after time is called. These checks contain no undisclosed requirements;
they exercise the clarification answers in INTERVIEWER_PACKET.md.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import unittest

from dasher_pay import (
    Delivery,
    DeliveryClientError,
    DeliveryStatus,
    InvalidRequestError,
    PayoutService,
    PayoutUnavailableError,
)


BASE_TIME = datetime(2026, 8, 18, 12, 0, tzinfo=timezone.utc)


def completed(delivery_id, accepted_minute, completed_minute):
    return Delivery(
        delivery_id=delivery_id,
        accepted_at=BASE_TIME + timedelta(minutes=accepted_minute),
        completed_at=BASE_TIME + timedelta(minutes=completed_minute),
        status=DeliveryStatus.COMPLETED,
    )


class FakeDeliveryClient:
    def __init__(self, deliveries=(), error=None):
        self.deliveries = tuple(deliveries)
        self.error = error
        self.calls = []

    def list_deliveries(self, dasher_id):
        self.calls.append(dasher_id)
        if self.error is not None:
            raise self.error
        return self.deliveries


class HeldBackPayoutChecks(unittest.TestCase):
    def test_two_non_overlapping_deliveries(self):
        result = PayoutService(
            FakeDeliveryClient(
                [
                    completed("d-1", 0, 10),
                    completed("d-2", 20, 25),
                ]
            )
        ).get_payout("dasher-1")

        self.assertEqual(Decimal("4.50"), result.amount)
        self.assertEqual(2, result.completed_delivery_count)

    def test_non_completed_delivery_is_not_paid(self):
        active = Delivery(
            delivery_id="d-active",
            accepted_at=BASE_TIME,
            completed_at=None,
            status=DeliveryStatus.ACTIVE,
        )
        cancelled = Delivery(
            delivery_id="d-cancelled",
            accepted_at=BASE_TIME,
            completed_at=BASE_TIME + timedelta(minutes=4),
            status=DeliveryStatus.CANCELLED,
        )

        result = PayoutService(
            FakeDeliveryClient([active, cancelled])
        ).get_payout("dasher-1")

        self.assertEqual(Decimal("0.00"), result.amount)
        self.assertEqual(0, result.completed_delivery_count)

    def test_blank_dasher_id_is_rejected_before_calling_upstream(self):
        client = FakeDeliveryClient()

        with self.assertRaises(InvalidRequestError):
            PayoutService(client).get_payout("   ")

        self.assertEqual([], client.calls)

    def test_upstream_failure_maps_to_stable_service_error(self):
        client = FakeDeliveryClient(
            error=DeliveryClientError("delivery service timed out")
        )

        with self.assertRaises(PayoutUnavailableError) as raised:
            PayoutService(client).get_payout("dasher-1")

        self.assertIsInstance(raised.exception.__cause__, DeliveryClientError)


if __name__ == "__main__":
    unittest.main()

