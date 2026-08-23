# Stripe-style Custom — Catch Me If You Can / Merchant Fraud Thresholds

This runnable exercise captures the repeatedly reported count thresholds, ratio thresholds, fraudulent
response codes, charge events, and dispute reversal. Exact live schemas vary, so this package declares
one deterministic contract.

## Contract

Implement:

```python
def fraudulent_merchants(
    merchant_config: Sequence[str],
    fraudulent_codes: Sequence[str],
    non_fraudulent_codes: Sequence[str],
    events: Sequence[str],
) -> List[str]:
    ...
```

Merchant configuration is `merchant_id,mcc,COUNT|RATIO,threshold`. Events are:

```text
CHARGE,charge_id,merchant_id,amount,response_code
DISPUTE,charge_id
```

- A unique charge whose response is in either configured code set is eligible and increments the
  merchant's total. Fraudulent codes also increment its fraud count.
- Unknown response codes are stored but excluded from both counts.
- A duplicate `charge_id` is ignored without mutation.
- The first dispute for a known, undisputed charge reverses that charge's count contribution. Unknown
  and duplicate disputes are ignored.
- `COUNT,n` flags when `fraud_count >= n`.
- `RATIO,r` flags when `total > 0` and `fraud_count / total >= r`.
- Return the final flagged merchant IDs in lexicographic order.

## Related LeetCode

- [LC 2043 — Simple Bank System](https://leetcode.com/problems/simple-bank-system/)
- [LC 1396 — Design Underground System](https://leetcode.com/problems/design-underground-system/)

They practice validated state mutation and event aggregation, but not reversible fraud thresholds.

## Run

```bash
python3 custom_practice/stripe/merchant_fraud_thresholds/run_tests.py
```
