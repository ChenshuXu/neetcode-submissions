# Snowflake Custom — Timestamped / Versioned Key-Value Store

This is a runnable cold-practice contract for Snowflake P0-10. Public interview reports describe a
family of timestamped key-value questions involving versions, TTLs, point-in-time reads, and
time-bucket discussions, but they do not establish one shared method signature. This exercise freezes
one deterministic contract so it can be implemented and tested under interview conditions.

This is not a verbatim copy of one private prompt. LC981 and LC1146 are useful prerequisites, but
neither includes this complete combination of out-of-order writes, TTLs, and a point-in-time view.

## Contract

Implement `TimestampedVersionedKV` in `solution.py`:

```python
class TimestampedVersionedKV:
    def set(self, key: str, value: str, write_time: int, ttl: int) -> None:
        ...

    def get(self, key: str, query_time: int) -> Optional[str]:
        ...

    def snapshot(self, query_time: int) -> dict[str, str]:
        ...
```

Rules:

- Keys and values are strings. An empty string is a legitimate value; `None` means that a key is
  absent at the requested time.
- `write_time` and `query_time` are non-negative integer timestamps. `ttl` is a positive integer.
  Inputs satisfy these constraints, so input validation is not required.
- Writes may arrive in any order, both across different keys and for the same key.
- A version written at `write_time` with `ttl` is unexpired during the half-open interval
  `[write_time, write_time + ttl)`. It is expired exactly at `write_time + ttl`.
- For `get(key, query_time)`, first select the version of `key` with the greatest `write_time` not
  exceeding `query_time`. Return its value if it is unexpired; otherwise return `None`.
- A newer version permanently supersedes older versions from its `write_time` onward. If that newer
  version later expires, an older version does **not** become visible again.
- Calling `set` again with the same `key` and `write_time` replaces both the value and TTL of the
  existing version at that timestamp.
- `snapshot(query_time)` returns a new dictionary containing every key whose selected version is
  unexpired at `query_time`. The dictionary has no required iteration order.
- `snapshot` is a point-in-time read. It does not create or return a persistent snapshot ID.

Example:

```text
store.set("plan", "v2", 20, 10)
store.set("plan", "v1", 10, 100)   # out-of-order write

store.get("plan", 15)      -> "v1"
store.get("plan", 25)      -> "v2"
store.get("plan", 30)      -> None  # v2 expires; v1 does not reappear
store.snapshot(15)          -> {"plan": "v1"}
```

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/timestamped_versioned_kv/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/timestamped_versioned_kv/run_tests.py --list
python3 custom_practice/snowflake/timestamped_versioned_kv/run_tests.py --case "out of order"
```

The runner creates a fresh store for every case and records output only for `get` and `snapshot`.
The supplied starter intentionally raises `NotImplementedError`.

## Interview target

- 0–5 minutes: clarify timestamp ordering, the TTL boundary, same-timestamp replacement, whether an
  expired newer version revives an older value, and what `snapshot` means.
- 5–10 minutes: state the representation, invariant, and expected read/write complexity.
- 10–35 minutes: implement all three methods.
- 35–45 minutes: run normal, TTL-boundary, out-of-order, replacement, and multi-key snapshot tests.
- 45–60 minutes: discuss disk persistence, a write-ahead log, crash recovery, and time buckets.

Let `v` be the number of versions for one key, `k` the number of keys, and `n` the total number of
versions. A balanced ordered map can target `O(log v)` reads and writes. With a Python sorted list,
binary search is `O(log v)` but an out-of-order insertion is `O(v)` because elements must shift.
A straightforward snapshot is `O(k log v_max)`, and stored history uses `O(n)` space. State the
actual complexity of the representation you implement.

## Follow-ups to discuss after the base passes

1. How would time buckets change the cost of large point-in-time snapshots?
2. How would you persist large values while keeping only metadata and offsets in memory?
3. What must be written to a WAL before acknowledging `set`?
4. How would recovery rebuild ordered per-key indexes after a crash?
5. How would range/prefix queries, expiry cleanup, or thread safety change the design?
