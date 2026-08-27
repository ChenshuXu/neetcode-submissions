"""Held-back contract checks.

Candidate: do not open or run this file during a cold attempt. The interviewer
runs it after time is called. These checks contain no undisclosed requirements;
they exercise the clarification answers in INTERVIEWER_PACKET.md.
"""

import unittest

from bootstrap import (
    Address,
    BootstrapService,
    BootstrapUnavailableError,
    BootstrapWarning,
    ClientNotFoundError,
    ClientUnavailableError,
    Order,
    PaymentProfile,
    User,
    UserNotFoundError,
)


USER = User("user-1", "consumer-9", "Avery")
ADDRESS = Address("123 Pine Street", "Seattle", "WA")
PAYMENT = PaymentProfile("card-7", 1250)
ORDERS = (
    Order("order-1", "delivered"),
    Order("order-2", "preparing"),
)


class FakeClient:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def _call(self, key):
        self.calls.append(key)
        if self.error is not None:
            raise self.error
        return self.result

    def get_user(self, user_id):
        return self._call(user_id)

    def get_default_address(self, consumer_id):
        return self._call(consumer_id)

    def get_payment_profile(self, consumer_id):
        return self._call(consumer_id)

    def list_recent_orders(self, consumer_id):
        return self._call(consumer_id)


def build_service(
    *,
    user_client=None,
    address_client=None,
    payment_client=None,
    order_client=None,
):
    return BootstrapService(
        user_client or FakeClient(result=USER),
        address_client or FakeClient(result=ADDRESS),
        payment_client or FakeClient(result=PAYMENT),
        order_client or FakeClient(result=ORDERS),
    )


class HeldBackBootstrapChecks(unittest.TestCase):
    def test_missing_user_maps_to_stable_not_found_error(self):
        service = build_service(
            user_client=FakeClient(error=ClientNotFoundError("missing"))
        )

        with self.assertRaises(UserNotFoundError) as raised:
            service.get_bootstrap("user-missing")

        self.assertIsInstance(raised.exception.__cause__, ClientNotFoundError)

    def test_unavailable_user_dependency_fails_the_whole_request(self):
        user_client = FakeClient(error=ClientUnavailableError("user down"))
        address_client = FakeClient(result=ADDRESS)
        payment_client = FakeClient(result=PAYMENT)
        order_client = FakeClient(result=ORDERS)
        service = build_service(
            user_client=user_client,
            address_client=address_client,
            payment_client=payment_client,
            order_client=order_client,
        )

        with self.assertRaises(BootstrapUnavailableError) as raised:
            service.get_bootstrap("user-1")

        self.assertIsInstance(raised.exception.__cause__, ClientUnavailableError)
        self.assertEqual(["user-1"], user_client.calls)
        self.assertEqual([], address_client.calls)
        self.assertEqual([], payment_client.calls)
        self.assertEqual([], order_client.calls)

    def test_missing_required_payment_fails_the_whole_request(self):
        service = build_service(
            payment_client=FakeClient(error=ClientNotFoundError("no payment"))
        )

        with self.assertRaises(BootstrapUnavailableError) as raised:
            service.get_bootstrap("user-1")

        self.assertIsInstance(raised.exception.__cause__, ClientNotFoundError)

    def test_missing_address_is_a_normal_empty_field_without_warning(self):
        result = build_service(
            address_client=FakeClient(error=ClientNotFoundError("no address"))
        ).get_bootstrap("user-1")

        self.assertIsNone(result.address)
        self.assertEqual((), result.warnings)

    def test_generic_address_unavailability_returns_warning(self):
        result = build_service(
            address_client=FakeClient(
                error=ClientUnavailableError("address unavailable")
            )
        ).get_bootstrap("user-1")

        self.assertIsNone(result.address)
        self.assertEqual(
            (
                BootstrapWarning(
                    dependency="address",
                    code="dependency_unavailable",
                ),
            ),
            result.warnings,
        )

    def test_empty_recent_orders_is_a_successful_response(self):
        result = build_service(
            order_client=FakeClient(result=())
        ).get_bootstrap("user-1")

        self.assertEqual((), result.recent_orders)
        self.assertEqual((), result.warnings)

    def test_missing_recent_orders_is_a_normal_empty_collection(self):
        result = build_service(
            order_client=FakeClient(error=ClientNotFoundError("no orders"))
        ).get_bootstrap("user-1")

        self.assertEqual((), result.recent_orders)
        self.assertEqual((), result.warnings)

    def test_recent_order_sequence_is_normalized_to_tuple(self):
        result = build_service(
            order_client=FakeClient(result=list(ORDERS))
        ).get_bootstrap("user-1")

        self.assertIsInstance(result.recent_orders, tuple)
        self.assertEqual(ORDERS, result.recent_orders)

    def test_order_dependency_failure_returns_partial_response_with_warning(self):
        result = build_service(
            order_client=FakeClient(error=ClientUnavailableError("orders down"))
        ).get_bootstrap("user-1")

        self.assertEqual((), result.recent_orders)
        self.assertEqual(
            (
                BootstrapWarning(
                    dependency="orders",
                    code="dependency_unavailable",
                ),
            ),
            result.warnings,
        )

    def test_optional_failure_warnings_have_deterministic_order(self):
        result = build_service(
            address_client=FakeClient(
                error=ClientUnavailableError("address down")
            ),
            order_client=FakeClient(
                error=ClientUnavailableError("orders down")
            ),
        ).get_bootstrap("user-1")

        self.assertEqual(
            (
                BootstrapWarning(
                    dependency="address",
                    code="dependency_unavailable",
                ),
                BootstrapWarning(
                    dependency="orders",
                    code="dependency_unavailable",
                ),
            ),
            result.warnings,
        )


if __name__ == "__main__":
    unittest.main()
