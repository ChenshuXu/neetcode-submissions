# Follow-up — Constrained Person → Cake Global Assignment

The one follow-up the archive attributes to a named round. A February 2026 mid-level report states
that the 2-D person/cake round was extended to a constrained person-to-cake global assignment.

## Contract

Every person must receive exactly one cake, and every cake feeds at most one person. Minimize the
total distance travelled across the whole assignment.

```python
def min_total_assignment_distance(
    people: Sequence[int],
    cakes: Sequence[int],
) -> int:
    ...
```

## Practice harness decisions

The report names the constraint and the objective but exposes no signature, no geometry, and no
infeasibility behavior. This package fixes those:

- `people` and `cakes` are positions on a line, in any order, and may repeat.
- The cost of one pair is the difference of its two positions.
- The answer is the smallest total cost over all valid one-to-one assignments.
- More people than cakes returns `-1`.
- No people returns `0`, whatever the cakes are.
- Spare cakes are simply left unused.

The reported round sat on a grid. Minimizing total distance over grid positions is the general
assignment problem, which needs Hungarian matching in `O(n^3)` and is not a 20-minute answer. This
package uses positions on a line, which is the version the preparation plan trains and the version
an interviewer can expect to be finished. Say that trade-off out loud rather than starting a
Hungarian implementation on a whiteboard.

These are deterministic practice assumptions, not claimed wording from the interview report.

Example:

```text
people = [4, 0]
cakes  = [3, 5]

Nearest-first in input order: 4 → 3 (1), then 0 → 5 (5), total 6.
Optimal:                      0 → 3 (3), then 4 → 5 (1), total 4.
```

## Evidence boundary

- `ties`, `stable allocation`, and `streaming` appear in the question bank as family variants from
  other sources. They are not implemented here and must not be described as part of this round's
  follow-up chain.
- Capacities greater than one are not part of this contract. That generalization is LeetCode 2463
  `[P1-S04]`, which the preparation plan already lists as the proxy for it.

## Run it

```bash
python3 custom_practice/snowflake/person_cake/follow_ups/global_assignment/run_tests.py
```

## Interview target

- Lead with the counterexample above: it is the shortest proof that the base answer does not extend,
  and it is the thing the follow-up is testing.
- State the exchange argument that makes sorting safe. If a left person takes a right cake while a
  right person takes a left cake, swapping the two cakes never increases the total, so some optimal
  assignment matches both lists in sorted order and no pair ever crosses.
- Give the recurrence over sorted lists: after `matched` people and the cakes seen so far, each new
  cake is either skipped or given to the next unmatched person.
- Test no people, more people than cakes, duplicate positions, a spare cake, and negative positions.
- Target `O(P log P + C log C + P * C)` time and `O(P)` space, and name `P * C` as the part that
  grows.
