# Stripe-style Custom — Credit Card Validation / Luhn

This runnable package covers all four publicly reported parts: known-network validation, valid checksum
with unknown network, redacted-digit counting, and repairing one corrupted digit.

## Contract

Implement `CardValidator` in `solution.py`:

```python
class CardValidator:
    def classify(self, number: str) -> str: ...
    def count_redacted(self, pattern: str) -> int: ...
    def repair_one_digit(self, number: str) -> List[str]: ...
```

Network rules:

- `VISA`: prefix `4`, length 13, 16, or 19.
- `MASTERCARD`: length 16 and prefix `51..55` or `2221..2720`.
- `AMEX`: length 15 and prefix `34` or `37`.

`classify` first requires a digit-only string and valid Luhn checksum. Return the recognized network,
`UNKNOWN` for a valid Luhn number outside the three networks, or `INVALID` otherwise.

`count_redacted` replaces every `?` with a digit and counts substitutions classified as a recognized
network. At most four characters are redacted; leading zero is allowed during enumeration.

`repair_one_digit` replaces exactly one position with a different digit and returns every recognized,
Luhn-valid candidate, deduplicated and lexicographically sorted. The original string is never included.

## Related LeetCode

No meaningful LeetCode equivalent was found; checksum parity, network-prefix recognition, wildcard
enumeration, and one-digit repair are the core of this custom.

## Run

```bash
python3 custom_practice/stripe/credit_card_validation/run_tests.py
```
