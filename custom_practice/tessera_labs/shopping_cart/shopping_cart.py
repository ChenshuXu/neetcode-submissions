"""
Shopping Cart Service - Technical Interview

REQUIREMENTS:
Build a shopping cart service that supports the methods listed below.
All users are pre-authenticated. Focus on clean code, error handling, and edge cases.
We'll discuss extensions and design decisions afterward.
"""
from dataclasses import dataclass, replace
from decimal import Decimal
from typing import Dict, List, Optional

# ============================================================
# PROVIDED MODELS
# ============================================================

@dataclass
class User:
    id: str
    name: str
    email: str

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int


# ============================================================
# YOUR MODELS - Design these as you see fit
# ============================================================

@dataclass
class CartItem:
    product: Product
    count: int


@dataclass
class CartSummary:
    items: List[CartItem]
    total_price: float


@dataclass
class OrderSummary:
    items: List[CartItem]
    total_price: float


# ============================================================
# PROVIDED SERVICES (Do not modify)
# ============================================================


class ProductService:
    """Handles product catalog and inventory."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}
        self._setup_sample_products()

    def _setup_sample_products(self) -> None:
        self.add_product("prod-1", "Laptop", 999.99, stock=5)
        self.add_product("prod-2", "Headphones", 149.99, stock=10)
        self.add_product("prod-3", "USB Cable", 12.99, stock=50)
        self.add_product("prod-4", "Monitor", 399.99, stock=3)

    def add_product(
        self, product_id: str, name: str, price: float, stock: int
    ) -> Product:
        product = Product(id=product_id, name=name, price=price, stock=stock)
        self._products[product_id] = product
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def get_all_products(self) -> List[Product]:
        return list(self._products.values())

    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        """
        Update product stock. Use negative values to decrease.
        Returns True if successful, False if product not found.
        Does not validate if stock goes negative. The caller must check.
        """
        product = self._products.get(product_id)
        if not product:
            return False
        product.stock += quantity_change
        return True


class UserService:
    """Handles user management."""

    def __init__(self) -> None:
        self._users: Dict[str, User] = {}
        self._setup_sample_users()

    def _setup_sample_users(self) -> None:
        self._users["user-1"] = User(id="user-1", name="John", email="john@example.com")
        self._users["user-2"] = User(
            id="user-2", name="Peter", email="peter@example.com"
        )

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)


# ============================================================
# YOUR IMPLEMENTATION
# ============================================================


class ShoppingCartService:
    """
    Single-threaded, in-memory cart service; adding does not reserve stock.
    Invalid users/products and failed checkouts raise ValueError.
    Reads return snapshots with quantities and current catalog prices.
    Checkout either purchases the entire cart or leaves it unchanged.

    Required methods:
    add_to_cart - Add a product to user's cart (validate against inventory)
    get_cart - Get user's cart with items and total price
    checkout - Complete purchase, deduct inventory, return order summary
    """

    def __init__(self) -> None:
        self.product_service = ProductService()
        self.user_service = UserService()
        # key: user id
        # value: dict { product_id -> count }
        self.cart_data: Dict[str, Dict[str, int]] = {}

    def add_to_cart(self, user_id: str, product_id: str) -> bool:
        if not self.user_service.get_user(user_id):
            raise ValueError(f"User not found: {user_id}")

        product = self.product_service.get_product(product_id)
        if product is None:
            raise ValueError(f"Product not found: {product_id}")

        count = self.cart_data.get(user_id, {}).get(product_id, 0)
        if count >= product.stock:
            raise ValueError(f"Insufficient stock: {product_id}")

        self.cart_data.setdefault(user_id, {})[product_id] = count + 1
        return True

    def get_cart(self, user_id: str) -> CartSummary:
        """Show requested quantities and current stock without changing the cart."""
        if not self.user_service.get_user(user_id):
            raise ValueError(f"User not found: {user_id}")

        cart = self.cart_data.get(user_id, {})
        items = []
        total_price = Decimal("0")
        for product_id, count in cart.items():
            product = self.product_service.get_product(product_id)
            if product is None:
                raise ValueError(f"Product not found: {product_id}")
            items.append(CartItem(replace(product), count))
            total_price += Decimal(str(product.price)) * count

        return CartSummary(items, float(total_price))

    def checkout(self, user_id: str) -> OrderSummary:
        """Validate the entire cart before deducting stock; clear it on success."""
        summary = self.get_cart(user_id)
        if not summary.items:
            raise ValueError("Cart is empty")

        # ponytail: single-threaded; synchronize validation and deduction if shared.
        for item in summary.items:
            if item.count > item.product.stock:
                raise ValueError(f"Insufficient stock: {item.product.id}")

        for item in summary.items:
            self.product_service.update_stock(item.product.id, -item.count)

        del self.cart_data[user_id]
        return OrderSummary(summary.items, summary.total_price)

if __name__ == "__main__":
    service = ShoppingCartService()
    service.add_to_cart("user-1", "prod-1")
    service.add_to_cart("user-1", "prod-1")
    service.add_to_cart("user-1", "prod-2")
    print(service.get_cart("user-1"))
    print(service.checkout("user-1"))
