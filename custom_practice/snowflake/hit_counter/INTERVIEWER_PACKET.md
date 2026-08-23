# LC362 interviewer packet

Candidate: do not read this during a cold run. Use it for review after time is called.

## Clarification answers

- Calls, including queries, use monotonically nondecreasing timestamps.
- A hit at `t - 299` is active at time `t`; a hit at `t - 300` is expired.
- Several hits may share the same second.
- The base implementation is in-memory and single-process.
- The follow-up asks for bounded memory when the number of hits per second is very large.

## Expected invariant

Keep a deque of active `(timestamp, count)` buckets and a running total. Before either public
operation finishes, remove every bucket with `bucket_timestamp <= now - 300`. Therefore the deque
contains only active seconds and the total equals the sum of their counts.

```python
from collections import deque


class HitCounter:
    def __init__(self) -> None:
        self._buckets = deque()
        self._total = 0

    def _expire(self, timestamp: int) -> None:
        cutoff = timestamp - 300
        while self._buckets and self._buckets[0][0] <= cutoff:
            _, count = self._buckets.popleft()
            self._total -= count

    def hit(self, timestamp: int) -> None:
        self._expire(timestamp)
        if self._buckets and self._buckets[-1][0] == timestamp:
            old_timestamp, count = self._buckets[-1]
            self._buckets[-1] = (old_timestamp, count + 1)
        else:
            self._buckets.append((timestamp, 1))
        self._total += 1

    def getHits(self, timestamp: int) -> int:
        self._expire(timestamp)
        return self._total
```

Complexity: each bucket enters and leaves once, so both APIs are amortized `O(1)`. Space is at most
one bucket per active second, hence `O(300)`.

## Strong spoken explanation

> The boundary is the part I want to make explicit. At query time `t`, timestamp `t - 299` counts
> and `t - 300` does not. I will compress all hits from the same second into one deque bucket and
> maintain a running total. I evict from the front on both writes and reads, so time advancing via a
> query cannot leave stale hits in the answer. Each bucket is added and removed once, giving
> amortized constant time and at most 300 active buckets.

## Follow-up card

Ask only after the base passes:

> Calls may now come from multiple threads. Define the consistency promise and make the smallest
> safe change.

Expected answer: `hit` and `getHits` each need one atomic boundary covering expiry plus mutation or
read. A single lock around each public method is the simplest linearizable answer. A distributed
version is a different contract: shard-local buckets can be summed for exact reads with coordination,
or aggregated asynchronously for lower latency with explicit staleness.
