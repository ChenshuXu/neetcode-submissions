# Stripe-style Custom — Payment Reconciliation

The Stripe bank describes transaction matching and discrepancy reporting, but this family is more often
reported in live/integration rounds and its exact current contract is incomplete. This runnable exercise
declares a deterministic reconciliation contract instead of claiming verbatim recovery.

## Contract

Implement:

```python
def reconcile_payments(
    internal_rows: Sequence[str],
    processor_rows: Sequence[str],
) -> List[str]:
    ...
```

Every row is:

```text
transaction_id,merchant_id,amount,currency,status
```

- `transaction_id` is unique within each input and is the match key.
- A row appearing only internally emits `transaction_id,MISSING_PROCESSOR`.
- A row appearing only at the processor emits `transaction_id,MISSING_INTERNAL`.
- For matched IDs, compare `merchant_id`, numeric decimal `amount`, `currency`, and `status`.
- Exact matches emit nothing. Differences emit
  `transaction_id,MISMATCH,field1|field2|...` using field order
  `merchant_id, amount, currency, status`.
- Return discrepancy rows sorted lexicographically by `transaction_id`.
- Rows are valid and field text contains no commas.

## Related LeetCode

[LC 350 — Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/)
practices matching two collections, but not keyed record comparison and discrepancy classification.

## Run

```bash
python3 custom_practice/stripe/payment_reconciliation/run_tests.py
```
