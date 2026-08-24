# Snowflake Custom — Closest Bathroom for Each Desk

This is an answer-free, runnable practice package derived from the recovered Snowflake interview
description.

## Recovered interview contract

The reported input is a grid containing:

- `B`: a bathroom
- `D`: a desk
- `.`: an empty position

Return the distance from every desk to its nearest bathroom. Movement is between vertically or
horizontally adjacent positions.

One recovered March 2026 report explicitly supplies the `B`, `D`, and empty-position representation.
A separate April 2026 report confirms the Bathroom/Desk shortest-distance family. No same-round
follow-up was recovered from either report.

## Practice harness decisions

The reports do not expose a function signature, output container, empty-grid behavior, or a sentinel
for a desk when there is no bathroom. This package fixes only those details so the tests are
deterministic:

```python
def closest_bathroom_distances(
    grid: Sequence[str],
) -> dict[tuple[int, int], int]:
    ...
```

- `grid` is rectangular and contains only `B`, `D`, and `.`.
- Coordinates are zero-indexed `(row, column)` pairs.
- Return one dictionary entry for every desk and no entries for other positions.
- A desk with no bathroom in the grid maps to `-1`.
- An empty grid or a grid with no desks returns `{}`.

These are deterministic practice assumptions, not claimed wording from the interview report.

Example:

```text
grid = [
    "D..B",
    "....",
    "..D.",
    "B...",
]

result = {
    (0, 0): 3,
    (2, 2): 3,
}
```

## Evidence boundary

A different commercial/mock source describes `H` positions finding the nearest `P` with obstacles.
That version supports obstacle and unreachable-state practice, but it is not merged into this base
contract and is not labeled as a follow-up to the `B` / `D` interview.

The one-dimensional Person/Cake problem and its global one-to-one assignment follow-up are also a
separate problem family, not part of this exercise.

## Run it

Implement only `closest_bathroom_distances` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/closest_bathroom_for_each_desk/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/closest_bathroom_for_each_desk/run_tests.py --list
python3 custom_practice/snowflake/closest_bathroom_for_each_desk/run_tests.py --case multiple
```

The supplied starter intentionally raises `NotImplementedError`.

## Interview target

- Finish within 35 minutes from a blank starter without AI.
- Explain why starting a separate search from every desk does unnecessary repeated work.
- State the invariant that makes the first discovered distance final.
- Test multiple bathrooms, a tie, no bathroom, no desk, and the empty grid.
- Target `O(rows * columns)` time and state the actual auxiliary-space bound.

## Sources and provenance

- Snowflake report `1167395`: recovered as the `B` / `D` / empty-position grid contract.
- Snowflake report `1173123`: independently confirms the Bathroom/Desk shortest-distance family.
- Canonical local evidence inventory:
  `/Users/Newton/Documents/job search/projects/context/Interview/snowflake/snowflake-interview-question-bank-2016-2026.md`
- Canonical local execution card:
  `/Users/Newton/Documents/job search/projects/context/Interview/snowflake/snowflake-ic2-coding-preparation-plan.md`
