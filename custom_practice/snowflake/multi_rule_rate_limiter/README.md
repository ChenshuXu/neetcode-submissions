# Snowflake Custom — Multi-Rule Rate Limiter

This is a runnable cold-practice contract based on a repeatedly reported Snowflake coding-screen
family. Public reports identify a per-key sliding-window limiter with multiple simultaneous rules;
one concrete example uses at most 3 accepted requests per 1 second and at most 20 accepted requests
per 10 seconds. A recent report explicitly names thread safety as the follow-up.

This is not a verbatim copy of a private prompt. The reports do not expose every boundary and state
rule, so this exercise fixes those details below to make the visible tests deterministic.

## Contract

Implement `MultiRuleRateLimiter` in `solution.py`:

```python
class MultiRuleRateLimiter:
    def __init__(self, rules: Sequence[tuple[int, int]]) -> None:
        ...

    def allow(self, key: str, timestamp: int) -> bool:
        ...
```

Each rule is `(max_requests, window_seconds)`. For example, `((3, 1), (20, 10))` means that every
key may have at most 3 accepted requests in a 1-second window and at most 20 accepted requests in a
10-second window.

Rules:

- `rules` is non-empty. Every maximum and window length is a positive integer.
- Timestamps are positive integer seconds (`timestamp >= 1`), and calls are monotonically
  nondecreasing. Multiple requests may share the same timestamp.
- Limits are independent per key. Activity for one key never consumes another key's quota.
- At time `timestamp`, a rule counts accepted requests in the integer-second interval
  `[timestamp - window_seconds + 1, timestamp]`. Equivalently, a request is expired when
  `accepted_timestamp <= timestamp - window_seconds`.
- The current request is allowed only when accepting it would keep the count within **every** rule.
- An allowed request is recorded for every rule and `allow` returns `True`.
- A rejected request is not recorded by any rule and `allow` returns `False`.
- Stale requests must be evicted. Memory should depend on requests still active in at least one
  configured window, not on the complete request history.

Example:

```text
limiter = MultiRuleRateLimiter(((3, 1), (20, 10)))

allow("search", 1) -> True
allow("search", 1) -> True
allow("search", 1) -> True
allow("search", 1) -> False
allow("upload", 1) -> True   # a different key has independent quota
allow("search", 2) -> True   # timestamp 1 is outside the 1-second window
```

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/multi_rule_rate_limiter/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/multi_rule_rate_limiter/run_tests.py --list
python3 custom_practice/snowflake/multi_rule_rate_limiter/run_tests.py --case cutoff
```

The runner creates a fresh limiter for every case and records the Boolean result of every `allow`
call. The supplied starter intentionally raises `NotImplementedError`.

## Interview target

- 0–5 minutes: clarify whether rejected requests count, the exact left boundary, timestamp ordering,
  and whether rules are fixed.
- 5–8 minutes: state the representation, invariant, and expected complexity.
- 8–28 minutes: finish the per-key multi-rule implementation.
- 28–35 minutes: test same-timestamp traffic, exact cutoffs, independent keys, overlapping rules,
  rejection atomicity, and cleanup after a long idle period.
- 35–45 minutes: explain or implement the thread-safety boundary.

For `r` fixed rules, target amortized `O(r)` time per request. State the actual space bound of your
representation; do not claim bounded memory if expired entries are never removed.

## Follow-ups to discuss after the base passes

1. Which steps inside `allow` must be one atomic operation under concurrency?
2. What changes if a single global lock is too contended and you introduce per-key locks?
3. How will you remove locks and histories for inactive keys without racing a new request?
4. How would you support dynamic rule updates?
5. When would a token bucket be preferable to an exact sliding-window limiter?
