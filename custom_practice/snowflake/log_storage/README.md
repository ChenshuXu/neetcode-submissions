# Snowflake Drill — LC635 Design Log Storage System

This is the heavier design problem from a reported Snowflake Backend IC1/IC2 two-problem round. It
was paired with LC588 in a 60-minute coding interview, so the base LC635 implementation should take
**15 minutes or less**.

This problem is not the same as the open-ended distributed log-storage system-design question also
reported at Snowflake. The base task here is LC635's in-memory API.

## Contract

Implement `LogSystem` in `solution.py`:

```python
class LogSystem:
    def __init__(self) -> None:
        ...

    def put(self, log_id: int, timestamp: str) -> None:
        ...

    def retrieve(
        self,
        start: str,
        end: str,
        granularity: str,
    ) -> List[int]:
        ...
```

- Every log ID is unique.
- Timestamps use fixed-width `Year:Month:Day:Hour:Minute:Second` format, such as
  `2017:01:01:23:59:59`.
- `put` calls need not be in timestamp order.
- `retrieve` returns IDs whose timestamps fall in the inclusive range at the requested granularity.
- Granularity is one of `Year`, `Month`, `Day`, `Hour`, `Minute`, or `Second`.
- Components finer than the requested granularity are ignored for the log, start, and end.
- Result order is not graded by this practice runner.
- Inputs are valid; do not spend interview time building a date validator.

## Run it

```bash
python3 custom_practice/snowflake/log_storage/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/log_storage/run_tests.py --list
python3 custom_practice/snowflake/log_storage/run_tests.py --case granularities
```

## Interview target

The hidden decision is whether you notice and safely exploit the data representation. Because every
component is zero-padded and ordered from largest to smallest, timestamp prefixes have the same order
as time at that granularity. No calendar math is needed.

- Minute 0–2: confirm fixed width, inclusive endpoints, valid inputs, and output-order requirements.
- Minute 2–4: explain the prefix comparison.
- Minute 4–10: implement `put` plus the `O(n)` retrieval scan.
- Minute 10–13: test Year, Day, and exact Second boundaries.
- Minute 13–15: state complexity and discuss how indexing changes the trade-off.

For the given small operation bound, `O(1)` insertion, `O(n)` retrieval, and `O(n)` space is the
right base answer. Do not introduce date libraries, a fake integer calendar, or a distributed store
before the simple solution passes.

## Follow-ups

1. Optimize for millions of logs and frequent range queries.
2. Support pagination without skipping or duplicating logs while new writes arrive.
3. Add deletion or mutable log metadata.
4. Define a thread-safe atomic boundary for `put` and `retrieve`.
5. Turn the API into a distributed audit-log service with retention, partitioning, indexes, and a
   clear consistency contract.

Read `INTERVIEWER_PACKET.md` only after a cold run, or let a mock interviewer use it.
