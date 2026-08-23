# Snowflake Drill — LC362 Design Hit Counter

This is the fast-opener drill for a reported Snowflake Backend IC1/IC2 two-problem round. The
candidate report paired an easy tax calculation with LC362 in one 60-minute interview. Treat this
as a **20-minute maximum** problem so a second question still has room.

## Contract

Implement `HitCounter` in `solution.py`:

```python
class HitCounter:
    def __init__(self) -> None:
        ...

    def hit(self, timestamp: int) -> None:
        ...

    def getHits(self, timestamp: int) -> int:
        ...
```

- Timestamps are integer seconds and calls are monotonically nondecreasing.
- `hit(timestamp)` records one hit. Multiple hits may share a timestamp.
- `getHits(timestamp)` returns hits in the past 300 seconds.
- The exact active interval is `[timestamp - 299, timestamp]`.
- The long-running implementation should not retain expired history forever.

Example:

```text
hit(1)
hit(2)
hit(3)
getHits(4)   -> 3
hit(300)
getHits(300) -> 4
getHits(301) -> 3
```

## Run it

```bash
python3 custom_practice/snowflake_hit_counter/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake_hit_counter/run_tests.py --list
python3 custom_practice/snowflake_hit_counter/run_tests.py --case boundary
```

## Interview target

The hidden decision is not whether you know a queue. It is whether you can turn an exact time-window
contract into a small stateful API with correct expiry and bounded memory.

- Minute 0–2: confirm monotonic calls, multiple hits per second, and the exact left boundary.
- Minute 2–5: state the representation and invariant.
- Minute 5–12: implement both methods.
- Minute 12–16: test empty, duplicate-second, timestamp 300, and timestamp 301.
- Minute 16–20: state complexity and answer the high-volume follow-up.

Passing target: amortized `O(1)` per API and `O(300)` timestamp buckets. A queue containing every
individual hit is correct for the base constraints but does not answer the high-volume follow-up.

## Follow-ups

1. What changes if millions of hits arrive in one second?
2. Compare a deque of `(timestamp, count)` buckets with a fixed 300-slot circular array.
3. How would you make the API linearizable under concurrent calls?
4. What changes if events can arrive out of order?
5. How would you distribute the counter across many servers, and what consistency would the query
   promise?

Read `INTERVIEWER_PACKET.md` only after a cold run, or let a mock interviewer use it.
