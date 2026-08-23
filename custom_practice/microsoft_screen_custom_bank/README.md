# Microsoft Screen Custom Question Bank

This package turns seven publicly reported Microsoft custom-question families into deterministic,
runnable Python exercises. They do not have a confirmed one-to-one LeetCode contract.

`solution.py` intentionally contains blank starters. The tests are visible and standard-library-only.
Passing a temporary reference implementation proves the harness, not candidate readiness.

## Evidence boundary

The source inventory is:

`/Users/Newton/Documents/job search/projects/context/Interview/microsoft/microsoft-screen-interview-experiences-and-question-bank-2024-2026.md`

- `tagged_sequence_assembly` combines two independent DNA/tag-chain reports (#19 and #27).
- `bidirectional_movie_index` comes from the Senior user↔movie data-structure prompt (#4).
- `extensible_calculator` comes from the live-screen calculator + OOP prompt (#23).
- `find_work_schedules` comes from the publicly exposed work-schedule contract (#15).
- `shortest_weighted_string` uses the reported factorial-like character-weight family (#15). A
  [public analogue](https://gist.github.com/WennderSantos/2256be4706a4f3cd6121ab322116a918)
  preserves the recurrence; the deterministic tie rule below is an explicit reconstruction choice.
- `two_minimum_values` comes from the one-pass `O(n)` prompt (#18).
- `distinct_nonempty_subsequences` comes from the public string-subsequence prompt (#17).

These are practice contracts, not leaked exact prompts. Incomplete reports about a dice random source,
the positive/negative “longest sequence,” generic DFS/array questions, prime factors, and hidden prompts
are intentionally excluded rather than guessed.

## Run

From the repository root:

```bash
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py --list-problems
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py tagged_sequence_assembly
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py find_work_schedules --list
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py extensible_calculator --case invalid
```

A blank starter should fail with `NotImplementedError`. That confirms the selected problem reached the
candidate code. It is not a readiness result.

## Contracts

### `tagged_sequence_assembly`

Implement:

```python
assemble_tagged_sequences(
    sequences: Sequence[Tuple[str, str, str, str]],
) -> List[Tuple[Tuple[str, ...], str]]
```

Each tuple is `(sequence_id, start_tag, end_tag, payload)` and represents a directed fragment. Arrange
every fragment into one or more chains where one fragment's `end_tag` equals the next fragment's
`start_tag`. Return `(ordered_ids, concatenated_payload)` for each chain, sorted by its first ID.

Assumptions fixed for this drill:

- sequence IDs are unique;
- the graph is a collection of directed, non-branching, non-merging, acyclic chains;
- every fragment must appear exactly once;
- empty input returns `[]`;
- duplicate IDs, branching, merging, or a cycle must raise `ValueError`.

Reverse-direction output and ambiguous branching policies remain follow-ups.

### `bidirectional_movie_index`

Implement `UserMovieIndex`:

```python
index.add(user_id, movie_id)
index.movies_for_user(user_id) -> List[str]
index.users_for_movie(movie_id) -> List[str]
```

`add` is idempotent. Queries return sorted IDs, and missing IDs return `[]`. The visible runner replays
`add`, `movies_for_user`, and `users_for_movie` operations. Removal, concurrency, and persistence are
follow-ups.

### `extensible_calculator`

Implement `evaluate_expression(expression) -> int` for non-negative decimal integers, spaces, `+`, and
`*`. Multiplication has standard precedence over addition. Parentheses, unary operators, and other
characters are outside the base contract. Empty or malformed expressions must raise `ValueError`.
Do not use `eval` or `exec`. Explain how the design would add more operators.

### `find_work_schedules`

Implement `find_work_schedules(total_hours, daily_limit, pattern) -> List[str]`.

`pattern` contains fixed decimal digits and `?` placeholders. Replace each `?` with one digit in
`0..daily_limit` so all digits sum to `total_hours`. Return every valid schedule in lexicographic order;
return `[]` if none exists. This drill requires `0 <= daily_limit <= 9` and rejects invalid characters,
negative totals, or fixed digits above the daily limit with `ValueError`.

### `shortest_weighted_string`

Implement `shortest_weighted_string(target_weight) -> str`.

Character weights are:

```text
weight('a') = 1
weight(letter[i]) = (i + 2) * weight(letter[i - 1])  for i = 1..25
```

The first weights are `a=1, b=3, c=12, d=60, e=360`. A string's weight is the sum of its character
weights. Return the shortest string with exactly `target_weight`; among equally short strings, return
the lexicographically smallest. `0` returns the empty string, and a negative target raises `ValueError`.

### `two_minimum_values`

Implement `two_minimum_values(values) -> Tuple[int, int]` using one pass and `O(1)` auxiliary space.
Repeated values at different positions count separately, so `[1, 1]` returns `(1, 1)`. Return values
in ascending order. Fewer than two inputs must raise `ValueError`. Do not sort or use a heap.

### `distinct_nonempty_subsequences`

Implement `distinct_nonempty_subsequences(text) -> List[str]`. Return every distinct, non-empty
subsequence while preserving source-character order inside each subsequence. Return the final list in
lexicographic order. The empty string returns `[]`; repeated input characters must not create duplicate
outputs.

## Suggested order

1. `tagged_sequence_assembly` — highest-value repeated custom family.
2. `bidirectional_movie_index` — Senior data-structure design and complexity discussion.
3. `extensible_calculator` — implementation plus extensibility follow-up.
4. `find_work_schedules` — complete backtracking contract.
5. `shortest_weighted_string` — greedy reasoning under a reconstructed deterministic contract.
6. `two_minimum_values` and `distinct_nonempty_subsequences` — 15–20 minute warmups.

These drills supplement the required timed no-AI LeetCode rehearsals; they do not replace them.
