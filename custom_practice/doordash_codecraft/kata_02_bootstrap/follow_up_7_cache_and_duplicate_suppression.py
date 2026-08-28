"""Card 7: keep Card 6 and share simultaneous address reads."""

import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from threading import Event, Lock
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
class GiftCard:
    card_id: str
    remaining_balance_cents: int


@dataclass
class AccountConfigData:
    locale: str
    currency_code: str
    gift_cards: list[GiftCard]


@dataclass
class AccountConfig:
    locale: str
    currency_code: str


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
    account_config: Optional[AccountConfig]
    gift_card_balance_cents: int
    warnings: list[BootstrapWarning]


@dataclass
class HttpResponse:
    status_code: int
    body: dict


class ClientError(RuntimeError):
    pass


class ClientNotFoundError(ClientError):
    pass


class ClientTimeoutError(ClientError):
    pass


class AddressCall:
    def __init__(self):
        self.done = Event()
        self.result = None
        self.error = None


class SingleFlightAddressClient:
    def __init__(
        self,
        address_client,  # Real address client called by the leader.
    ):
        self.address_client = address_client
        self.lock = Lock()
        self.in_flight = {}

    def get_default_address(
        self,
        consumer_id,  # Consumer whose address is requested.
    ):
        with self.lock:
            call = self.in_flight.get(consumer_id)
            if call is None:
                call = AddressCall()
                self.in_flight[consumer_id] = call
                is_leader = True
            else:
                is_leader = False

        if not is_leader:
            call.done.wait()
            if call.error is not None:
                raise call.error
            return call.result

        try:
            call.result = self.address_client.get_default_address(
                consumer_id
            )
        except Exception as error:
            call.error = error
        finally:
            call.done.set()
            with self.lock:
                self.in_flight.pop(consumer_id, None)

        if call.error is not None:
            raise call.error
        return call.result


class BootstrapService:
    def __init__(
        self,
        user_client,  # Reads the required user.
        address_client,  # Reads the optional address.
        payment_client,  # Reads the payment profile.
        order_client,  # Reads the optional recent orders.
        account_config_client,  # Reads optional account config.
        payment_required=True,  # False enables guest mode.
        max_retries=1,  # Extra attempts after the first call.
        base_delay_seconds=0.05,  # Delay before the first retry.
        request_timeout_seconds=1.0,  # Total time for the request.
    ):
        self.user_client = user_client
        self.address_client = SingleFlightAddressClient(address_client)
        self.payment_client = payment_client
        self.order_client = order_client
        self.account_config_client = account_config_client
        self.payment_required = payment_required
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

    def _get_payment(
        self,
        future,  # Concurrent payment read to resolve.
        deadline,  # Shared absolute deadline.
        warnings,  # Warning list for the response.
    ):
        try:
            return future.result(timeout=self._remaining_time(deadline))
        except ClientNotFoundError as error:
            if self.payment_required:
                raise ClientError("payment unavailable") from error
            return None
        except (ClientError, FutureTimeoutError) as error:
            if self.payment_required:
                raise ClientError("payment unavailable") from error
            warnings.append(
                BootstrapWarning("payment", "dependency_unavailable")
            )
            return None

    def _build_account_config(
        self,
        data,  # Account config returned by the client.
    ):
        total_balance = 0
        for gift_card in data.gift_cards:
            total_balance += gift_card.remaining_balance_cents

        config = AccountConfig(data.locale, data.currency_code)
        return config, total_balance

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

        executor = ThreadPoolExecutor(max_workers=4)
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
        config_future = executor.submit(
            self._call_with_retry,
            self.account_config_client.get_account_config,
            user.consumer_id,
            deadline,
        )
        futures = [
            payment_future,
            address_future,
            orders_future,
            config_future,
        ]

        try:
            warnings = []
            payment = self._get_payment(
                payment_future,
                deadline,
                warnings,
            )
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
            config_data = self._get_optional_future(
                config_future,
                deadline,
                None,
                "account_config",
                warnings,
            )

            account_config = None
            gift_card_balance = 0
            if config_data is not None:
                account_config, gift_card_balance = (
                    self._build_account_config(config_data)
                )

            return BootstrapResponse(
                user,
                payment,
                address,
                list(recent_orders),
                account_config,
                gift_card_balance,
                warnings,
            )
        finally:
            for future in futures:
                future.cancel()
            executor.shutdown(wait=False)


class BootstrapEndpoint:
    def __init__(
        self,
        service,  # Bootstrap service used by this endpoint.
    ):
        self.service = service

    def _success_body(
        self,
        response,  # Successful BootstrapResponse to serialize.
    ):
        orders = []
        for order in response.recent_orders:
            orders.append(
                {
                    "order_id": order.order_id,
                    "status": order.status,
                }
            )

        warnings = []
        for warning in response.warnings:
            field = warning.dependency
            if field == "orders":
                field = "recent_orders"
            warnings.append({"field": field, "code": warning.code})

        payment = None
        if response.payment is not None:
            payment = {
                "default_method_id": response.payment.default_method_id,
                "wallet_balance_cents": (
                    response.payment.wallet_balance_cents
                ),
            }

        address = None
        if response.address is not None:
            address = {
                "line1": response.address.line1,
                "city": response.address.city,
                "region": response.address.region,
            }

        account_config = None
        if response.account_config is not None:
            account_config = {
                "locale": response.account_config.locale,
                "currency_code": response.account_config.currency_code,
            }

        return {
            "user": {
                "user_id": response.user.user_id,
                "consumer_id": response.user.consumer_id,
                "display_name": response.user.display_name,
            },
            "payment": payment,
            "address": address,
            "recent_orders": orders,
            "account_config": account_config,
            "gift_card_balance_cents": (
                response.gift_card_balance_cents
            ),
            "warnings": warnings,
        }

    def get_bootstrap(
        self,
        user_id,  # Public user ID from the HTTP request.
    ):
        try:
            response = self.service.get_bootstrap(user_id)
            return HttpResponse(200, self._success_body(response))
        except ValueError:
            return HttpResponse(400, {"error": "invalid_request"})
        except ClientNotFoundError:
            return HttpResponse(404, {"error": "user_not_found"})
        except ClientError:
            return HttpResponse(503, {"error": "bootstrap_unavailable"})
        except Exception:
            return HttpResponse(500, {"error": "internal_error"})


USER = User("user-1", "consumer-9", "Avery")
ADDRESS = Address("123 Pine Street", "Seattle", "WA")
PAYMENT = PaymentProfile("card-7", 1250)
ORDERS = [Order("order-1", "delivered")]
CONFIG_DATA = AccountConfigData(
    "en-US",
    "USD",
    [
        GiftCard("gift-1", 300),
        GiftCard("gift-2", 700),
        GiftCard("gift-3", 0),
    ],
)


class MockClient:
    def __init__(self, *results):
        self.results = list(results)

    def _read(self):
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

    def get_account_config(self, consumer_id):
        return self._read()


class SlowAddressClient:
    def __init__(self):
        self.call_count = 0
        self.started = Event()

    def get_default_address(self, consumer_id):
        self.call_count += 1
        self.started.set()
        time.sleep(0.05)
        return ADDRESS


def main():
    address_client = SlowAddressClient()
    service = BootstrapService(
        MockClient(USER, USER),
        address_client,
        MockClient(PAYMENT, PAYMENT),
        MockClient(ORDERS, ORDERS),
        MockClient(CONFIG_DATA, CONFIG_DATA),
        base_delay_seconds=0.01,
    )

    endpoint = BootstrapEndpoint(service)
    executor = ThreadPoolExecutor(max_workers=2)
    first_future = executor.submit(endpoint.get_bootstrap, "user-1")
    address_client.started.wait()
    second_future = executor.submit(endpoint.get_bootstrap, "user-1")
    first_response = first_future.result()
    second_response = second_future.result()
    executor.shutdown()

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert address_client.call_count == 1
    print(first_response)
    print("real address calls:", address_client.call_count)


if __name__ == "__main__":
    main()
