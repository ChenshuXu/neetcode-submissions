"""Card 2: keep Card 1 and read consumer data concurrently."""

import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: str
    consumer_id: str
    display_name: str


@dataclass
class Address:
    line1: str
    city: str
    region: str


@dataclass
class PaymentProfile:
    default_method_id: str
    wallet_balance_cents: int


@dataclass
class Order:
    order_id: str
    status: str


@dataclass
class BootstrapWarning:
    dependency: str
    code: str


@dataclass
class BootstrapResponse:
    user: User
    payment: Optional[PaymentProfile]
    address: Optional[Address]
    recent_orders: list[Order]
    warnings: list[BootstrapWarning]


class ClientError(RuntimeError):
    pass


class ClientNotFoundError(ClientError):
    pass


class BootstrapService:
    def __init__(
        self,
        user_client,  # Reads the required user.
        address_client,  # Reads the optional address.
        payment_client,  # Reads the required payment profile.
        order_client,  # Reads the optional recent orders.
        fanout_timeout_seconds=1.0,  # Total time for concurrent reads.
    ):
        self.user_client = user_client
        self.address_client = address_client
        self.payment_client = payment_client
        self.order_client = order_client
        self.fanout_timeout_seconds = fanout_timeout_seconds

    def _remaining_time(
        self,
        deadline,  # Absolute deadline from time.time().
    ):
        remaining = deadline - time.time()
        if remaining < 0:
            return 0
        return remaining

    def _get_optional_future(
        self,
        future,  # Concurrent read to resolve.
        deadline,  # Shared absolute deadline.
        default,  # Value used when the read fails.
        dependency,  # Dependency name used in the warning.
        warnings,  # Warning list for the response.
    ):
        try:
            return future.result(timeout=self._remaining_time(deadline))
        except ClientNotFoundError:
            return default
        except (ClientError, FutureTimeoutError):
            warnings.append(
                BootstrapWarning(dependency, "dependency_unavailable")
            )
            return default

    def get_bootstrap(
        self,
        user_id,  # Public user ID from the request.
    ):
        if not user_id or not user_id.strip():
            raise ValueError("user_id must not be blank")

        user = self.user_client.get_user(user_id)
        deadline = time.time() + self.fanout_timeout_seconds
        executor = ThreadPoolExecutor(max_workers=3)

        payment_future = executor.submit(
            self.payment_client.get_payment_profile,
            user.consumer_id,
        )
        address_future = executor.submit(
            self.address_client.get_default_address,
            user.consumer_id,
        )
        orders_future = executor.submit(
            self.order_client.list_recent_orders,
            user.consumer_id,
        )
        futures = [payment_future, address_future, orders_future]

        try:
            try:
                payment = payment_future.result(
                    timeout=self._remaining_time(deadline)
                )
            except (ClientError, FutureTimeoutError) as error:
                raise ClientError("payment unavailable") from error

            warnings = []
            address = self._get_optional_future(
                address_future,
                deadline,
                None,
                "address",
                warnings,
            )
            recent_orders = self._get_optional_future(
                orders_future,
                deadline,
                [],
                "orders",
                warnings,
            )

            return BootstrapResponse(
                user,
                payment,
                address,
                list(recent_orders),
                warnings,
            )
        finally:
            for future in futures:
                future.cancel()
            executor.shutdown(wait=False)


USER = User("user-1", "consumer-9", "Avery")
ADDRESS = Address("123 Pine Street", "Seattle", "WA")
PAYMENT = PaymentProfile("card-7", 1250)
ORDERS = [Order("order-1", "delivered")]


class MockClient:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def _read(self):
        if self.error is not None:
            raise self.error
        return self.result

    def get_user(self, user_id):
        return self._read()

    def get_default_address(self, consumer_id):
        return self._read()

    def get_payment_profile(self, consumer_id):
        return self._read()

    def list_recent_orders(self, consumer_id):
        return self._read()


def main():
    service = BootstrapService(
        MockClient(USER),
        MockClient(ADDRESS),
        MockClient(PAYMENT),
        MockClient(ORDERS),
    )

    response = service.get_bootstrap("user-1")
    assert response.payment == PAYMENT
    assert response.address == ADDRESS
    print(response)


if __name__ == "__main__":
    main()
