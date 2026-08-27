# Snowflake Custom — Query History Window

This is a runnable cold-practice package for Snowflake preparation-plan card `P1-15`. The archived
source describes the business problem and the required `sort + sliding window + per-user aggregate`
shape, but it does not recover every API and tie rule from an interview.

The dataclasses, integer-second timestamps, positive integer credits, deterministic ties, and output
ordering below are explicit practice choices. They are not claims about verbatim interview wording.

## Contract

Implement `find_peak_query_windows` in `solution.py`:

```python
def find_peak_query_windows(
    queries: Sequence[QueryRecord],
) -> list[WindowSummary]:
    ...
```

Each `QueryRecord` contains:

```text
query_id / warehouse_id / user_id / start_time / end_time / credits_used
```

For each warehouse, return the 30-minute half-open window `[t, t + 1800)` with the largest sum of
credits:

- A query belongs to a window only by `start_time`; its entire `credits_used` value counts there,
  even if the query ends after the window.
- Input order is arbitrary.
- Timestamps are integer seconds, `start_time <= end_time`, and credits are positive integers.
- IDs are non-empty strings. `query_id` values are unique.
- Multiple queries may have the same `start_time`.
- If multiple windows have the same maximum total, keep the earliest `window_start`.
- Within the winning window, the top user is the user with the greatest credit sum. Break a tie by
  lexicographically smaller `user_id`.
- Return summaries in lexicographic `warehouse_id` order.
- `top_user_credits / total_credits` is the winning user's share; the output keeps the two integers
  rather than introducing floating-point rounding.
- Empty input returns `[]`.
- Do not mutate the input records or collection.

## Example

```text
queries = [
    QueryRecord("q1", "wh-a", "u1", 0,    300,  5),
    QueryRecord("q2", "wh-a", "u2", 600,  900,  4),
    QueryRecord("q3", "wh-a", "u1", 1700, 2000, 3),
    QueryRecord("q4", "wh-a", "u2", 1800, 2100, 10),
]

find_peak_query_windows(queries) == [
    WindowSummary("wh-a", 600, 2400, 17, "u2", 14),
]
```

The window `[600, 2400)` contains `q2`, `q3`, and `q4`. It uses 17 credits total, and `u2`
contributes 14.

## Run it

```bash
python3 custom_practice/snowflake/query_history_window/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/query_history_window/run_tests.py --list
python3 custom_practice/snowflake/query_history_window/run_tests.py --case boundary
```

The normal command runs all visible cases and a deterministic randomized differential suite. The
starter intentionally raises `NotImplementedError` and contains no reference solution.

## Interview target

- Clarify the half-open boundary, start-time attribution, input ordering, credit sign, tie rules, and
  output ordering before coding.
- State why an optimal window can start at a query's `start_time` when every credit value is
  positive.
- Handle equal timestamps as one group so a candidate window never drops only part of that time.
- Avoid rescanning every user for every window; keep per-user credit totals and a max structure with
  deterministic ties.
- Reach `O(n log n)` time and `O(n)` auxiliary space across all warehouses.

## Follow-ups to discuss after the base passes

1. Support late, out-of-order records in a streaming service.
2. Split a query's credits proportionally across every window it overlaps instead of using only
   `start_time`.
3. Return the top `k` users in each winning window.
4. Merge partial per-warehouse results computed on different machines.
5. Discuss exact versus approximate answers when the history no longer fits in memory.
