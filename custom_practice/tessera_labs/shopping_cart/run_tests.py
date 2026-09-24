"""Visible regression checks: python3 custom_practice/tessera_labs/shopping_cart/run_tests.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runner import Case, run_cli
from shopping_cart import ShoppingCartService


def expect_error(message, operation, *args):
    try:
        operation(*args)
    except ValueError as error:
        assert message in str(error), str(error)
    else:
        raise AssertionError("Expected ValueError")


def check(scenario):
    service = ShoppingCartService()
    catalog = service.product_service

    if scenario == "invalid and empty":
        expect_error("User not found", service.add_to_cart, "missing", "prod-1")
        expect_error("Product not found", service.add_to_cart, "user-1", "missing")
        expect_error("User not found", service.get_cart, "missing")
        expect_error("User not found", service.checkout, "missing")
        expect_error("Cart is empty", service.checkout, "user-1")
        assert service.cart_data == {}
        assert service.get_cart("user-1").items == []
        assert service.get_cart("user-1").total_price == 0.0
        return True

    if scenario == "exact stock and repeat checkout":
        for _ in range(5):
            assert service.add_to_cart("user-1", "prod-1")
        expect_error("Insufficient stock", service.add_to_cart, "user-1", "prod-1")
        assert catalog.get_product("prod-1").stock == 5
        assert service.get_cart("user-1").items[0].count == 5
        order = service.checkout("user-1")
        assert order.total_price == 4999.95
        assert order.items[0].count == 5
        assert catalog.get_product("prod-1").stock == 0
        assert service.get_cart("user-1").items == []
        assert service.get_cart("user-1").total_price == 0.0
        expect_error("Insufficient stock", service.add_to_cart, "user-2", "prod-1")
        expect_error("Cart is empty", service.checkout, "user-1")
        assert catalog.get_product("prod-1").stock == 0
        return True

    service.add_to_cart("user-1", "prod-1")
    service.add_to_cart("user-1", "prod-1")
    service.add_to_cart("user-1", "prod-2")

    if scenario == "total and snapshot isolation":
        cart = service.get_cart("user-1")
        assert cart.total_price == 2149.97
        assert [item.count for item in cart.items] == [2, 1]
        cart.items[0].product.price = 0
        cart.items[0].product.stock = 0
        cart.items[0].count = 100
        order = service.checkout("user-1")
        assert order.total_price == 2149.97
        assert [item.product.id for item in order.items] == ["prod-1", "prod-2"]
        assert [item.count for item in order.items] == [2, 1]
        catalog.add_product("prod-1", "New laptop", 1.0, 20)
        assert order.items[0].product.price == 999.99
        order.items[0].product.stock = 100
        assert catalog.get_product("prod-1").stock == 20
        assert catalog.get_product("prod-2").stock == 9
        return True

    if scenario == "user cart isolation":
        service.add_to_cart("user-2", "prod-1")
        second_cart = service.get_cart("user-2")
        assert second_cart.items[0].count == 1
        assert second_cart.total_price == 999.99
        service.checkout("user-1")
        assert service.get_cart("user-2").items[0].count == 1
        assert service.get_cart("user-2").total_price == second_cart.total_price
        assert service.checkout("user-2").total_price == 999.99
        assert catalog.get_product("prod-1").stock == 2
        return True

    if scenario == "current catalog price":
        catalog.get_product("prod-1").price = 0.1
        catalog.get_product("prod-2").price = 0.2
        assert service.get_cart("user-1").total_price == 0.4
        assert service.checkout("user-1").total_price == 0.4
        return True

    if scenario == "stock changed by another user":
        for _ in range(10):
            service.add_to_cart("user-2", "prod-2")
        service.checkout("user-2")
        cart = service.get_cart("user-1")
        assert cart.total_price == 2149.97
        assert cart.items[1].count == 1
        assert cart.items[1].product.stock == 0
        message = "Insufficient stock"
    elif scenario == "missing catalog product":
        del catalog._products["prod-2"]
        expect_error("Product not found", service.get_cart, "user-1")
        message = "Product not found"
    else:
        raise AssertionError(f"Unknown scenario: {scenario}")

    before = service.cart_data["user-1"].copy()
    stocks = {product.id: product.stock for product in catalog.get_all_products()}
    expect_error(message, service.checkout, "user-1")
    assert {product.id: product.stock for product in catalog.get_all_products()} == stocks
    assert service.cart_data["user-1"] == before
    # Restocking/relisting allows retry without losing the original quantities.
    catalog.add_product("prod-2", "Headphones", 149.99, 10)
    assert service.checkout("user-1").total_price == 2149.97
    assert catalog.get_product("prod-1").stock == 3
    assert catalog.get_product("prod-2").stock == 9
    return True


if __name__ == "__main__":
    scenarios = [
        "invalid and empty",
        "exact stock and repeat checkout",
        "total and snapshot isolation",
        "user cart isolation",
        "current catalog price",
        "stock changed by another user",
        "missing catalog product",
    ]
    raise SystemExit(run_cli(check, [Case(name, True, (name,)) for name in scenarios]))
