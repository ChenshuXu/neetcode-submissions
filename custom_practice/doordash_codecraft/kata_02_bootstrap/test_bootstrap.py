import unittest

from bootstrap import (
    Address,
    BootstrapResponse,
    BootstrapService,
    BootstrapUnavailableError,
    BootstrapWarning,
    ClientTimeoutError,
    ClientUnavailableError,
    InvalidRequestError,
    Order,
    PaymentProfile,
    User,
)


USER = User(
    user_id="user-1",
    consumer_id="consumer-9",
    display_name="Avery",
)
ADDRESS = Address(
    line1="123 Pine Street",
    city="Seattle",
    region="WA",
)
PAYMENT = PaymentProfile(
    default_method_id="card-7",
    wallet_balance_cents=1250,
)
ORDERS = (
    Order(order_id="order-1", status="delivered"),
    Order(order_id="order-2", status="preparing"),
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


class BootstrapServiceTests(unittest.TestCase):
    def test_all_dependencies_succeed(self):
        user_client = FakeClient(result=USER)
        address_client = FakeClient(result=ADDRESS)
        payment_client = FakeClient(result=PAYMENT)
        order_client = FakeClient(result=ORDERS)
        service = build_service(
            user_client=user_client,
            address_client=address_client,
            payment_client=payment_client,
            order_client=order_client,
        )

        result = service.get_bootstrap("user-1")

        self.assertEqual(
            BootstrapResponse(
                user=USER,
                payment=PAYMENT,
                address=ADDRESS,
                recent_orders=ORDERS,
                warnings=(),
            ),
            result,
        )
        self.assertEqual(["user-1"], user_client.calls)
        self.assertEqual(["consumer-9"], address_client.calls)
        self.assertEqual(["consumer-9"], payment_client.calls)
        self.assertEqual(["consumer-9"], order_client.calls)

    def test_blank_user_id_is_rejected_before_any_dependency_call(self):
        user_client = FakeClient(result=USER)
        address_client = FakeClient(result=ADDRESS)
        payment_client = FakeClient(result=PAYMENT)
        order_client = FakeClient(result=ORDERS)
        service = build_service(
            user_client=user_client,
            address_client=address_client,
            payment_client=payment_client,
            order_client=order_client,
        )

        with self.assertRaises(InvalidRequestError):
            service.get_bootstrap(" ")

        self.assertEqual([], user_client.calls)
        self.assertEqual([], address_client.calls)
        self.assertEqual([], payment_client.calls)
        self.assertEqual([], order_client.calls)

    def test_address_timeout_returns_partial_response_with_warning(self):
        service = build_service(
            address_client=FakeClient(error=ClientTimeoutError("address timeout"))
        )

        result = service.get_bootstrap("user-1")

        self.assertIsNone(result.address)
        self.assertEqual(PAYMENT, result.payment)
        self.assertEqual(ORDERS, result.recent_orders)
        self.assertEqual(
            (
                BootstrapWarning(
                    dependency="address",
                    code="dependency_unavailable",
                ),
            ),
            result.warnings,
        )

    def test_required_payment_failure_fails_the_whole_request(self):
        service = build_service(
            payment_client=FakeClient(error=ClientUnavailableError("payment down"))
        )

        with self.assertRaises(BootstrapUnavailableError) as raised:
            service.get_bootstrap("user-1")

        self.assertIsInstance(raised.exception.__cause__, ClientUnavailableError)

if __name__ == "__main__":
    unittest.main()
