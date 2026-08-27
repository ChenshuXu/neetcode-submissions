"""Starter code for the DoorDash-style Bootstrap Aggregator kata.

Implement BootstrapService.get_bootstrap. The client interfaces are supplied
ports; no HTTP framework or real network calls are required for this exercise.
"""

from dataclasses import dataclass
from typing import Optional, Protocol, Sequence, Tuple


@dataclass(frozen=True)
class User:
    user_id: str
    consumer_id: str
    display_name: str


@dataclass(frozen=True)
class Address:
    line1: str
    city: str
    region: str


@dataclass(frozen=True)
class PaymentProfile:
    default_method_id: str
    wallet_balance_cents: int


@dataclass(frozen=True)
class Order:
    order_id: str
    status: str


@dataclass(frozen=True)
class BootstrapWarning:
    dependency: str
    code: str


@dataclass(frozen=True)
class BootstrapResponse:
    user: User
    payment: PaymentProfile
    address: Optional[Address]
    recent_orders: Tuple[Order, ...]
    warnings: Tuple[BootstrapWarning, ...]


class UserClient(Protocol):
    def get_user(self, user_id: str) -> User:
        """Resolve a public user ID to core user and consumer data."""


class AddressClient(Protocol):
    def get_default_address(self, consumer_id: str) -> Address:
        """Return the consumer's default address."""


class PaymentClient(Protocol):
    def get_payment_profile(self, consumer_id: str) -> PaymentProfile:
        """Return required payment data for bootstrap."""


class OrderClient(Protocol):
    def list_recent_orders(self, consumer_id: str) -> Sequence[Order]:
        """Return recent orders, possibly empty."""


class ClientNotFoundError(RuntimeError):
    """The requested resource does not exist."""


class ClientUnavailableError(RuntimeError):
    """A downstream dependency is unavailable."""


class ClientTimeoutError(ClientUnavailableError):
    """A downstream dependency exceeded its deadline."""


class InvalidRequestError(ValueError):
    """The endpoint-like request is invalid."""


class UserNotFoundError(RuntimeError):
    """The requested user does not exist."""


class BootstrapUnavailableError(RuntimeError):
    """A required dependency prevents a bootstrap response."""


class BootstrapService:
    def __init__(
        self,
        user_client: UserClient,
        address_client: AddressClient,
        payment_client: PaymentClient,
        order_client: OrderClient,
    ) -> None:
        # Store the injected dependency clients so tests can supply deterministic
        # fakes instead of making real network calls.
        self._user_client = user_client
        self._address_client = address_client
        self._payment_client = payment_client
        self._order_client = order_client

    def get_bootstrap(self, user_id: str) -> BootstrapResponse:
        """Assemble a stable response from required and optional dependencies."""
        raise NotImplementedError("Implement BootstrapService.get_bootstrap")
