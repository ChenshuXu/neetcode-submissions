# LC635 interviewer packet

Candidate: do not read this during a cold run. Use it for review after time is called.

## Clarification answers

- Timestamp fields are valid, fixed-width, and zero-padded.
- IDs are unique, but timestamps need not be unique.
- `put` calls are not guaranteed to be chronological.
- Range endpoints are inclusive at the requested granularity.
- Output order is not graded.
- The base constraints are small enough for a linear scan.

## Expected invariant and reference

The prefix ending at the requested field is a sortable representation of that timestamp at the
requested precision.

```python
from typing import List


class LogSystem:
    _PREFIX_LENGTH = {
        "Year": 4,
        "Month": 7,
        "Day": 10,
        "Hour": 13,
        "Minute": 16,
        "Second": 19,
    }

    def __init__(self) -> None:
        self._logs = []

    def put(self, log_id: int, timestamp: str) -> None:
        self._logs.append((log_id, timestamp))

    def retrieve(
        self,
        start: str,
        end: str,
        granularity: str,
    ) -> List[int]:
        prefix_length = self._PREFIX_LENGTH[granularity]
        lower = start[:prefix_length]
        upper = end[:prefix_length]
        return [
            log_id
            for log_id, timestamp in self._logs
            if lower <= timestamp[:prefix_length] <= upper
        ]
```

Complexity: `put` is `O(1)`. `retrieve` is `O(n)` plus the returned output. Space is `O(n)`.

## Strong spoken explanation

> Before I parse dates, I want to use a property of the input. The fields are fixed-width,
> zero-padded, and ordered from year down to second. That means lexicographic order of the prefix is
> chronological order at the requested granularity. I can map each granularity to a prefix length,
> truncate the log and both inclusive endpoints to that length, and scan. With at most a few hundred
> calls, that is simpler and less error-prone than maintaining an index.

## Follow-up card A: query-heavy scale

> There are now millions of immutable logs and range queries dominate writes. How would you change
> the representation?

Expected answer: keep a sorted index by full timestamp and stable ID, then use two binary searches to
find the requested range. Retrieval is `O(log n + k)`, where returning `k` IDs is unavoidable. The
candidate should name the write trade-off: insertion into a flat sorted array is `O(n)`, so use
batch-sort/merge, a balanced tree, or an LSM-style index depending on workload.

## Follow-up card B: open-ended log service

> This API is now a multi-tenant audit-log service. Sketch the production design.

Expected answer, in order: clarify retention and query filters; define append and paginated range-query
APIs; partition primarily by tenant plus time; write to a durable append path; build asynchronous time
and secondary indexes; store immutable segments in object storage; define freshness and consistency;
handle hot tenants, backpressure, retries/idempotency, retention deletion, access control, encryption,
and observability. Do not accept a list of technologies without contracts or trade-offs.
