"""Card 3: keep Card 2 and retry timeout errors with backoff."""

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


class ClientTimeoutError(ClientError):
    pass


class BootstrapService:
    def __init__(
        self,
        user_client,  # Reads the required user.
        address_client,  # Reads the optional address.
        payment_client,  # Reads the required payment profile.
        order_client,  # Reads the optional recent orders.
        max_retries=1,  # Extra attempts after the first call.
        base_delay_seconds=0.05,  # Delay before the first retry.
        request_timeout_seconds=1.0,  # Total time for the request.
    ):
        self.user_client = user_client
        self.address_client = address_client
        self.payment_client = payment_client
        self.order_client = order_client
        self.max_retries = max_retries
        self.base_delay_seconds = base_delay_seconds
        self.request_timeout_seconds = request_timeout_seconds

    def _remaining_time(
        self,
        deadline,  # Absolute deadline from time.time().
    ):
        remaining = deadline - time.time()
        if remaining < 0:
            return 0
        return remaining

    def _call_with_retry(
        self,
        fetch,  # Bound client method to call.
        key,  # User ID or consumer ID passed to the method.
        deadline,  # Shared absolute deadline.
    ):
        delay = self.base_delay_seconds

        for attempt in range(self.max_retries + 1):
            if time.time() >= deadline:
                raise ClientTimeoutError("request deadline exceeded")

            try:
                return fetch(key)
            except ClientTimeoutError:
                if attempt == self.max_retries:
                    raise
                if time.time() + delay >= deadline:
                    raise
                time.sleep(delay)
                delay = delay * 2

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

        deadline = time.time() + self.request_timeout_seconds
        user = self._call_with_retry(
            self.user_client.get_user,
            user_id,
            deadline,
        )

        executor = ThreadPoolExecutor(max_workers=3)
        payment_future = executor.submit(
            self._call_with_retry,
            self.payment_client.get_payment_profile,
            user.consumer_id,
            deadline,
        )
        address_future = executor.submit(
            self._call_with_retry,
            self.address_client.get_default_address,
            user.consumer_id,
            deadline,
        )
        orders_future = executor.submit(
            self._call_with_retry,
            self.order_client.list_recent_orders,
            user.consumer_id,
            deadline,
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
    def __init__(self, *results):
        self.results = list(results)
        self.call_count = 0

    def _read(self):
        self.call_count += 1
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    def get_user(self, user_id):
        return self._read()

    def get_default_address(self, consumer_id):
        return self._read()

    def get_payment_profile(self, consumer_id):
        return self._read()

    def list_recent_orders(self, consumer_id):
        return self._read()


def main():
    payment_client = MockClient(
        ClientTimeoutError("first call timed out"),
        PAYMENT,
    )
    service = BootstrapService(
        MockClient(USER),
        MockClient(ADDRESS),
        payment_client,
        MockClient(ORDERS),
        max_retries=1,
        base_delay_seconds=0.01,
    )

    response = service.get_bootstrap("user-1")
    assert payment_client.call_count == 2
    assert response.payment == PAYMENT
    print(response)
    print("payment calls:", payment_client.call_count)


if __name__ == "__main__":
    main()
