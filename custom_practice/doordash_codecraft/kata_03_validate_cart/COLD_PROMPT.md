# DoorDash Code Craft mini-kata — Inventory / Validate Cart

You have 30 minutes. Implement `CartValidator.validate_cart` in
`validate_cart.py`, add or improve tests, and keep the result runnable.

## Evidence boundary

- Recovered from a first-hand public report: validate quantity, inventory
  availability, and minimum/maximum purchase rules.
- Fixed training semantics, not recovered verbatim: duplicate handling, exact
  error schema/order, inclusive boundaries, and the pure snapshot API below.
- A separate, lower-confidence report motivates the atomic-reservation
  follow-up. It is not part of the base validator.

## Base contract

`validate_cart(lines, inventory)` returns a `CartValidationResult` and never
mutates either input.

Rules:

1. An empty cart returns one `EMPTY_CART` error.
2. Quantity must be a positive integer. For this contract, `bool` and `float`
   are not valid integers.
3. The same `item_id` may appear only once. If it appears multiple times,
   return one `DUPLICATE_ITEM` error for that item and do not guess whether the
   lines should be merged.
4. A unique line whose `item_id` is absent from the inventory snapshot returns
   `ITEM_UNAVAILABLE`.
5. `min_quantity` and `max_quantity` are inclusive.
6. Quantity must not exceed `available_quantity`.
7. Return all applicable errors, not only the first one. Preserve first-seen
   item order. For one valid unique item, emit errors in this order:
   `BELOW_MINIMUM`, `ABOVE_MAXIMUM`, `INSUFFICIENT_INVENTORY`.

Duplicate and invalid-quantity errors take precedence for that item because no
unambiguous quantity remains for later business-rule checks. A missing
inventory record likewise ends that item's checks.

Assume inventory configuration is valid: quantities are non-negative integers
and `1 <= min_quantity <= max_quantity`.

## Example

Given:

```text
cart = [("soup", 1), ("salad", 1), ("apple", 9)]

soup:  available=2, min=2, max=4
apple: available=8, min=1, max=5
salad: missing from inventory
```

Return, in order:

```text
BELOW_MINIMUM(soup, requested=1, allowed=2)
ITEM_UNAVAILABLE(salad, requested=1)
ABOVE_MAXIMUM(apple, requested=9, allowed=5)
INSUFFICIENT_INVENTORY(apple, requested=9, allowed=8)
```

## Run

```bash
python3 run_tests.py
```

The untouched starter should discover nine visible tests and fail with
`NotImplementedError`. That is the intended cold-practice state.
