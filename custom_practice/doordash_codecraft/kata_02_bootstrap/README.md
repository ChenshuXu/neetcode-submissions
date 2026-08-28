# Bootstrap Aggregator API

Implement:

```python
BootstrapService.get_bootstrap(user_id)
```

This practice is based on recurring public DoorDash Code Craft reports, not a
verbatim DoorDash prompt. The exact Python models and required/optional policy
below are deterministic training choices.

## Base problem

The supplied clients expose four reads:

- `UserClient.get_user(user_id)` returns the required user and `consumer_id`.
- `PaymentClient.get_payment_profile(consumer_id)` returns required payment
  data.
- `AddressClient.get_default_address(consumer_id)` returns an optional address.
- `OrderClient.list_recent_orders(consumer_id)` returns optional recent orders.

Implement `get_bootstrap` with this contract:

1. Reject a blank or whitespace-only `user_id` before any client call.
2. Fetch the user first because the other calls need its `consumer_id`.
3. Fetch payment, address, and recent orders. Sequential calls are acceptable
   for the Base.
4. User and payment are required. Their failure fails the whole request.
5. Address and orders are optional:
   - not found means `None` or an empty list, without a warning;
   - unavailable means the same empty value plus a stable
     `dependency_unavailable` warning.
6. Return one `BootstrapResponse`. Warning order must not depend on client
   completion order.
7. Preserve the original required-payment error as the cause of the stable
   service error.

No HTTP framework, network access, third-party package, or large unit-test
harness is required. Use small fake clients and a few `assert` or `print`
checks in `main()`.

## Files and run order

In the canonical kata directory:

- `bootstrap_starter.py` is the answer-free source.
- `bootstrap.py` is the reviewed sequential Base.
- `follow_up_1_*.py` through `follow_up_7_*.py` are cumulative reviewed
  examples.

Run the reviewed progression only from the canonical kata directory:

```bash
python3 bootstrap.py
for file in follow_up_*.py; do python3 "$file" || exit 1; done
```

During a real practice attempt, implement only the Base and the one follow-up
the interviewer asks for. Reuse supplied classes instead of rewriting them.

## Follow-up 1: remove duplication

Refactor repeated optional-client error handling without hiding which
dependencies are required or optional. Preserve the Base response and failure
behavior.

Reference: `follow_up_1_remove_duplication.py`

## Follow-up 2: concurrent fan-out and one deadline

After user lookup returns `consumer_id`, fetch payment, address, and orders
concurrently. Keep deterministic response and warning order. One total deadline
must bound the entire fan-out; a separate full timeout per future is not enough.

Reference: `follow_up_2_concurrent_fanout.py`

## Follow-up 3: transient retry

Keep Follow-up 2's concurrency and add one shared retry helper for the four
read calls. Retry `ClientTimeoutError` only, use bounded exponential backoff,
and keep every attempt and delay inside the original total deadline. Do not
retry not-found or permanent errors.

Reference: `follow_up_3_transient_retry.py`

## Follow-up 4: account config transformation

Add an optional `AccountConfigClient`. Convert its upstream DTO into stable
public config fields and sum `remaining_balance_cents` across gift cards.
Missing config is normal; unavailable config adds a warning. Do not expose the
upstream DTO directly.

Reference: `follow_up_4_account_config.py`

## Follow-up 5: configurable guest policy

Make payment optional in guest mode without duplicating the orchestration
method. Normal mode still fails closed on payment, while guest mode returns a
partial response and warning. User identity remains required in both modes.

Reference: `follow_up_5_configurable_guest_policy.py`

## Follow-up 6: HTTP mapping

Add a thin endpoint adapter around the service:

- blank request -> `400`;
- missing required user -> `404`;
- required dependency unavailable -> `503`;
- usable partial response -> `200` with warnings;
- unexpected error -> `500` without internal exception text.

Reference: `follow_up_6_http_mapping.py`

## Follow-up 7: cache and duplicate suppression

Define the cache key and staleness policy first. For the coding version,
coalesce simultaneous address reads for one `consumer_id` with a small
single-flight wrapper. Sharing in-progress work is not the same as retaining a
completed value in a TTL cache.

Reference: `follow_up_7_cache_and_duplicate_suppression.py`
