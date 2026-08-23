# Snowflake-style Custom — Bounded Event-Frequency Tracker

This is a runnable practice contract derived from a partially public Snowflake interview report. The
report exposes the `(timestamp, key)` event shape, bounded recent state, and a timestamped
most-frequent-key query, but it does not expose the exact cutoff, tie, or late-event semantics. This
exercise fixes those details explicitly so the tests are deterministic; it is not a verbatim copy of
the original question.

## Contract

Implement `BoundedEventFrequency` in `solution.py`:

```python
class BoundedEventFrequency:
    def __init__(self, window_seconds: int) -> None:
        ...

    def record(self, timestamp: int, key: str) -> None:
        ...

    def most_frequent(self, now: int) -> Optional[str]:
        ...
```

- `window_seconds` is positive.
- Timestamps across all calls are monotonically nondecreasing.
- At time `now`, an event is active exactly when `now - window_seconds < timestamp <= now`.
- `record(timestamp, key)` records one event and may expire stale state.
- `most_frequent(now)` returns the active key with the highest frequency.
- Break a frequency tie by returning the lexicographically smallest key.
- Return `None` when no event is active.
- Multiple events may have the same timestamp and key.
- Memory must depend only on active-window state, not the complete event history.

Example with a five-second window:

```text
record(1, "a")
record(2, "b")
record(3, "a")
most_frequent(3) -> "a"

record(6, "b")
most_frequent(6) -> "b"  # timestamp 1 is now outside (1, 6]
```

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/bounded_event_frequency_tracker/run_tests.py
```

Useful options:

```bash
python3 custom_practice/bounded_event_frequency_tracker/run_tests.py --list
python3 custom_practice/bounded_event_frequency_tracker/run_tests.py --case boundary
```

The runner prints every operation, expected query result, actual result, and PASS/FAIL status. It
records output only for `most_frequent` calls.

## Baseline target

A straightforward interview solution may use a queue of active events plus a key-frequency map:

- `record` and stale-event removal: amortized `O(1)`
- `most_frequent`: `O(u)`, where `u` is the number of active distinct keys
- space: `O(n + u)` for active events and keys only

Do not add an ever-growing lazy heap while claiming bounded memory. If the interviewer requires
faster queries, discuss heap compaction, an ordered frequency index, or an All-O(1)-style frequency
bucket structure.

## Follow-ups to discuss after the base passes

1. Replace the time window with “retain only the last `m` event records.”
2. Accept out-of-order event timestamps.
3. Optimize for millions of queries between writes.
4. Make both APIs safe under concurrent calls and identify the atomic boundary.
5. Return the top `k` keys instead of one key.
