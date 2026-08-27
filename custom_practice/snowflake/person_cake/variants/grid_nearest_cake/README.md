# Variant — 2-D Nearest Cake for Each Person

A separate reported round of the `Person / Cake` family. One February 2026 mid-level report states
that the first coding round was a two-dimensional person/cake shortest-distance problem. It is kept
as a variant rather than a follow-up because it is that round's base problem, not a question asked
on top of the 1-D row.

## Contract

The grid uses the same encoding as the 1-D base:

- `0`: an empty cell
- `1`: a person
- `2`: a cake

Return the distance from every person to the nearest cake. A step moves to a vertically or
horizontally adjacent cell.

```python
def nearest_cake_distances(
    grid: Sequence[Sequence[int]],
) -> Dict[Tuple[int, int], int]:
    ...
```

## Practice harness decisions

The report exposes neither a signature nor a cell encoding for the 2-D round, so this package
reuses the 1-D `{0,1,2}` encoding and fixes the rest:

- `grid` is rectangular.
- No cell blocks movement. There are no obstacles in this contract.
- Coordinates are zero-indexed `(row, column)` pairs.
- Return one entry per person and no entry for any other cell.
- A person with no cake anywhere maps to `-1`.
- An empty grid, a grid with no columns, or a grid with no people returns `{}`.

These are deterministic practice assumptions, not claimed wording from the interview report.

Example:

```text
grid = [
    [0, 0, 2, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 2],
]

result = {
    (1, 1): 2,
    (3, 0): 4,
}
```

## Evidence boundary

- The report does not say whether the round asked for one global minimum or for every person's
  nearest cake. This package implements the per-person version, because the reported follow-up
  assigns cakes to multiple people and needs per-person distances to be meaningful.
- Obstacles and unreachable cells belong to a different commercial source attached to
  `Closest Bathroom / Desk` `[P0-06]`, and are not merged in here.

## Run it

```bash
python3 custom_practice/snowflake/person_cake/variants/grid_nearest_cake/run_tests.py
```

## Interview target

- Explain why one search started from every person repeats work, and why seeding the queue with all
  cakes at once does not.
- State the invariant that makes the first arrival final: breadth-first search expands whole
  distance levels, so the first time a cell is reached it is reached by a shortest path.
- Test no cake, no person, several equally near cakes, people sharing one cake, and the empty grid.
- Target `O(rows * columns)` time, and give the actual auxiliary-space bound.
