"""Card 1: move repeated optional-read handling into one helper."""

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
    ):
        self.user_client = user_client
        self.address_client = address_client
        self.payment_client = payment_client
        self.order_client = order_client

    def _get_optional(
        self,
        fetch,  # Bound client method to call.
        key,  # Consumer ID passed to the method.
        default,  # Value used when the read fails.
        dependency,  # Dependency name used in the warning.
        warnings,  # Warning list for the response.
    ):
        try:
            return fetch(key)
        except ClientNotFoundError:
            return default
        except ClientError:
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

        try:
            payment = self.payment_client.get_payment_profile(
                user.consumer_id
            )
        except ClientError as error:
            raise ClientError("payment unavailable") from error

        warnings = []
        address = self._get_optional(
            self.address_client.get_default_address,
            user.consumer_id,
            None,
            "address",
            warnings,
        )
        recent_orders = self._get_optional(
            self.order_client.list_recent_orders,
            user.consumer_id,
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
        MockClient(error=ClientError("address down")),
        MockClient(PAYMENT),
        MockClient(ORDERS),
    )

    response = service.get_bootstrap("user-1")
    assert response.address is None
    assert len(response.warnings) == 1
    print(response)


if __name__ == "__main__":
    main()
