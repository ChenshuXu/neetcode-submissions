# Snowflake Custom — Person / Cake `[P1-09]`

A runnable practice package for the Snowflake `Person / Cake` family. The base exercise lives here;
the reported 2-D round is under `variants/`, and the one explicitly reported follow-up is under
`follow_ups/`.

```text
person_cake/
├── solution.py, test_cases.py, run_tests.py   1-D minimum person/cake distance
├── variants/
│   └── grid_nearest_cake/                     2-D nearest cake per person
└── follow_ups/
    └── global_assignment/                     one-to-one person→cake assignment
```

## Recovered interview contract (base)

A one-dimensional row is encoded as:

- `0`: an empty position
- `1`: a person
- `2`: a cake

Return the smallest distance between any person and any cake, where distance is the difference of
two indices. A May 2026 report gives this `{0,1,2}` encoding and asks for the nearest person–cake
distance. A separate July 2025 write-up states the same encoding and asks for the global minimum in
`O(n)`.

## Practice harness decisions

The reports do not expose a function signature, an argument type, or the behavior when one of the
two kinds is missing. This package fixes only those details so the tests are deterministic:

```python
def min_person_cake_distance(cells: Sequence[int]) -> int:
    ...
```

- `cells` contains only `0`, `1`, and `2`.
- The answer is `min(|i - j|)` over every person index `i` and cake index `j`.
- A row with no person, no cake, or neither returns `-1`.
- An empty row returns `-1`.

These are deterministic practice assumptions, not claimed wording from the interview report.

Example:

```text
cells  = [1, 0, 0, 0, 2, 0, 1, 2]
people = indices 0 and 6
cakes  = indices 4 and 7
result = 1        # person 6 and cake 7
```

## Evidence boundary

- The 2-D round and the global-assignment follow-up come from one February 2026 mid-level report;
  they are packaged separately under `variants/` and `follow_ups/` rather than merged into this
  base.
- `unique consumption`, `ties`, and `streaming` are listed in the question bank as family variants
  drawn from more than one source. Only unique consumption is implemented here, inside the
  follow-up, because that is the one the February 2026 report attaches to a named round.
- The February 2026 candidate failed in the third coding round for unfinished reasoning. That
  outcome is not attributable to this problem.
- The July 2025 source is a recruiting-service account graded `C`. It corroborates the encoding; it
  does not add an independent candidate sighting.
- `Closest Bathroom / Desk` `[P0-06]` is a different problem in the same multi-source-BFS family and
  keeps its own package at `custom_practice/snowflake/closest_bathroom_for_each_desk/`.

## Run it

```bash
python3 custom_practice/snowflake/person_cake/run_tests.py
python3 custom_practice/snowflake/person_cake/variants/grid_nearest_cake/run_tests.py
python3 custom_practice/snowflake/person_cake/follow_ups/global_assignment/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/person_cake/run_tests.py --list
python3 custom_practice/snowflake/person_cake/run_tests.py --case tie
```

Each package runs its visible cases first, then a randomized differential test against a brute-force
oracle. Blank the function body in `solution.py` before a cold timed run.

## Interview target

- Finish the 1-D base within 20 minutes from a blank starter without AI, then move to the 2-D and
  global-assignment packages.
- State the invariant that makes one linear pass enough: the global minimum is always reached by a
  person and a cake that are adjacent in the order they appear, so comparing each index against the
  most recent index of the opposite kind is sufficient.
- Test a row with no person, a row with no cake, an empty row, several equally near cakes, and a
  best pair that is not the first pair found.
- Say when the locally nearest cake stops being the right answer — as soon as a cake can be eaten
  only once, per-person nearest choices can conflict, and the objective becomes a global one.
- Target `O(n)` time and `O(1)` auxiliary space for the base, and give the actual bounds for the
  other two packages.

## Related practice

- `P1-S03` LeetCode 821 Shortest Distance to a Character — 1-D nearest target.
- `P1-S04` LeetCode 2463 Minimum Total Distance Traveled — sorted assignment with capacities.

## Sources and provenance

- Snowflake report `1176393` (2026-05-11): 1-D `{0,1,2}` nearest person–cake distance.
- Snowflake report `1166549` (2026-02-26): 2-D person/cake nearest distance with a constrained
  global-assignment follow-up.
- Snowflake report `1167093` (2026-03-03): graded `C`, recovered by inference only; not counted as
  an independent sighting.
- Canonical local evidence inventory:
  `/Users/Newton/Documents/job search/projects/context/Interview/snowflake/snowflake-interview-question-bank-2016-2026.md`
- Canonical local execution card:
  `/Users/Newton/Documents/job search/projects/context/Interview/snowflake/snowflake-ic2-coding-preparation-plan.md`
