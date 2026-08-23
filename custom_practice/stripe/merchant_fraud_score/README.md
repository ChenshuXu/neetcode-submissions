# Stripe-style Custom — Merchant Fraud Score

This runnable exercise reconstructs the public Merchant Fraud Score rule families. The screenshot is
cropped before the full original schema and rounding rules, so this package fixes a deterministic
practice contract rather than claiming to reproduce the live prompt verbatim.

## Contract

Implement:

```python
def calculate_fraud_scores(
    transactions: Sequence[str],
    merchants: Sequence[str],
    rules: Sequence[str],
) -> List[str]:
    ...
```

Merchant rows are `merchant_id,base_score`. Transaction rows are:

```text
timestamp,transaction_id,merchant_id,customer_id,amount
```

`timestamp` is ISO-like text whose first 13 characters identify its hour. Rules are processed in the
given order for every transaction:

```text
AMOUNT,min_amount,multiplicative_factor
CUSTOMER_REPEAT,min_count,additive_factor
HOURLY_COUNT,min_count,additive_factor
```

- Add the current transaction to both counters before evaluating rules.
- `AMOUNT` applies only when `amount > min_amount`.
- `CUSTOMER_REPEAT` uses the current count for `(merchant_id, customer_id)` and applies at every
  transaction whose count is at least `min_count`.
- `HOURLY_COUNT` uses `(merchant_id, timestamp[:13])` with the same cumulative rule.
- Every matching rule applies; rule order is significant.
- Use decimal arithmetic and return `merchant_id,score` with exactly two decimal places, sorted by ID.
- Every transaction references a configured merchant and every row is valid.

## Related LeetCode

[LC 1396 — Design Underground System](https://leetcode.com/problems/design-underground-system/)
practices event parsing plus keyed aggregation, but no LeetCode problem found covers the ordered mixture
of multiplicative and cumulative merchant-scoring rules.

## Run

```bash
python3 custom_practice/stripe/merchant_fraud_score/run_tests.py
```
