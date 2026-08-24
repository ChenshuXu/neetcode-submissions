# Snowflake Custom — Binary Search with Repeated Queries

This is a runnable cold-practice reconstruction of a reported Snowflake coding-screen family. The
recoverable evidence identifies two stages: ordinary binary search / lower bound, followed by a
request to preprocess data that is queried many times and changes rarely.

This is not a verbatim private prompt, and the exact query API was not recovered. This exercise
therefore fixes one concrete contract that trains the reported mechanism without claiming that
these exact return values appeared in the interview.

## Contract

Implement both stages in `solution.py`.

### Part 1: lower bound

```python
def lower_bound(values: Sequence[int], target: int) -> int:
    ...
```

`values` is sorted in nondecreasing order. Return the smallest index `i` such that
`values[i] >= target`. Return `len(values)` if no such index exists.

Examples:

```text
lower_bound([1, 2, 2, 5], 2) -> 1
lower_bound([1, 2, 2, 5], 3) -> 3
lower_bound([1, 2, 2, 5], 8) -> 4
lower_bound([], 8)            -> 0
```

### Part 2: repeated exact-value queries

The same sorted data will now receive a very large number of exact-value queries and will not
change after construction.

```python
class RepeatedQueryIndex:
    def __init__(self, values: Sequence[int]) -> None:
        ...

    def query(self, target: int) -> tuple[int, int]:
        ...
```

For each `target`, return:

```text
(first_index, occurrence_count)
```

Rules:

- `values` is sorted in nondecreasing order and may be empty.
- Duplicate and negative values are allowed.
- If `target` exists, `first_index` is its first position in `values` and `occurrence_count` is its
  total number of occurrences.
- If `target` does not exist, return `(-1, 0)`. Do not return its lower-bound insertion position.
- Construction may preprocess the entire input once.
- After construction, each `query` must run in worst-case `O(1)` time.
- Do not mutate the caller's input.

Example:

```text
index = RepeatedQueryIndex([1, 2, 2, 2, 5])

index.query(2) -> (1, 3)
index.query(5) -> (4, 1)
index.query(3) -> (-1, 0)
```

## Run it

Implement `lower_bound` and `RepeatedQueryIndex` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/binary_search_repeated_queries/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/binary_search_repeated_queries/run_tests.py --list
python3 custom_practice/snowflake/binary_search_repeated_queries/run_tests.py --case duplicates
```

The supplied starter intentionally raises `NotImplementedError` and contains no reference
solution.

## Interview target

- 0–4 minutes: clarify sortedness, duplicate semantics, missing-target behavior, update frequency,
  query volume, and the allowed memory budget.
- 4–12 minutes: implement and test `lower_bound` with a half-open search interval.
- 12–18 minutes: compare serving `q` queries directly with performing one preprocessing pass.
- 18–28 minutes: implement the repeated-query index.
- 28–35 minutes: test empty input, first and last values, duplicates, negatives, missing values, and
  repeated queries for the same target.

Target costs:

- Part 1: `O(log n)` time and `O(1)` extra space.
- Part 2 construction: `O(n)` time and `O(u)` extra space, where `u` is the number of distinct
  values.
- Part 2 query: worst-case `O(1)` time.

## Follow-ups to discuss after the base passes

1. When is `O(q log n)` preferable to paying the preprocessing and memory cost?
2. What changes if the data receives occasional insertions or deletions?
3. How would the design change if every query supplied `[left, right]` and asked for the frequency
   of `target` only inside that index range?
4. If memory is limited, which preprocessing information can be removed while preserving correct
   queries at a higher runtime cost?

