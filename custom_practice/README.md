# Custom Coding Practice

This folder provides a small, standard-library-only runner for interview questions that are not on
LeetCode. It is designed for VS Code: fill in `solution.py`, run `run_tests.py`, and inspect every
visible input, expected value, actual value, and PASS/FAIL result.

## Folder hierarchy

Company-specific exercises live under one company folder. A follow-up that extends one base problem
lives under that problem's `follow_ups/` folder; a related problem with different semantics lives under
`variants/` instead.

```text
custom_practice/
├── snowflake/
│   ├── ordered_nary_tree_deletion/
│   │   ├── follow_ups/
│   │   └── variants/
│   └── <other Snowflake problems>/
├── stripe/
│   └── <Stripe problems and OA map>/
├── microsoft_screen_custom_bank/
└── doordash_codecraft/
```

See `snowflake/README.md` and `stripe/README.md` for the complete company indexes.

## Current practice

DoorDash Round 1 Code Craft (two 60-minute service/API katas):

```bash
cd custom_practice/doordash_codecraft
python3 new_attempt.py dasher-pay guided-dasher-01
```

See `doordash_codecraft/README.md` for the guided, solo, and cold-run workflows.

Ordered n-ary tree deletion:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py
```

Snowflake N-ary follow-ups:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/multiple_deletions/run_tests.py
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/forest_height/run_tests.py
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/minimum_deletions_for_height/run_tests.py
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/parent_index_forest/run_tests.py
```

Separate N-ary deletion variant:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/variants/subtree_deletion/run_tests.py
```

Report-based height-limit greedy (fresh blank attempt; preserves the completed DP version):

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/reported_height_limit_greedy/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py --list
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py --case middle
```

Bounded event-frequency tracker:

```bash
python3 custom_practice/snowflake/bounded_event_frequency_tracker/run_tests.py
```

This stateful Snowflake-style exercise combines rolling-window eviction with dynamic frequency
queries. Its exact cutoff and tie behavior are explicit practice assumptions because the public
interview report exposes only a partial contract.

Snowflake Person / Cake family:

```bash
python3 custom_practice/snowflake/person_cake/run_tests.py
python3 custom_practice/snowflake/person_cake/variants/grid_nearest_cake/run_tests.py
python3 custom_practice/snowflake/person_cake/follow_ups/global_assignment/run_tests.py
```

Three packages for one reported family: the 1-D `{0,1,2}` minimum person/cake distance, the 2-D
nearest-cake round, and the one-to-one assignment follow-up that breaks the nearest-first answer.
The `{0,1,2}` encoding comes from the reports; the signatures, the missing-kind sentinel, and the
line geometry used in the assignment follow-up are explicit practice assumptions.

Snowflake two-problem mechanics — LC362 and LC635:

```bash
python3 custom_practice/snowflake/hit_counter/run_tests.py
python3 custom_practice/snowflake/log_storage/run_tests.py
```

These are exact-contract speed drills for the reported Backend IC1/IC2 families. Hit Counter targets
compressed sliding-window state and the 300-second boundary. Log Storage targets fixed-width timestamp
prefixes and granularity-aware inclusive range queries. Each folder includes an interviewer packet for
post-run review and follow-ups.

Transactional key-value store:

```bash
python3 custom_practice/snowflake/transactional_kv/run_tests.py
```

This repeated Snowflake custom family covers `get/put/delete/begin/commit/rollback`, nested commit
and rollback semantics, missing-value handling, and ten visible state-transition cases. The delivered
solution remains an intentional cold-practice starter.

Task executor OOD:

```bash
python3 custom_practice/snowflake/task_executor_ood/run_tests.py
```

This reported onsite OOD family fixes only `addTask(taskId, priority, timestamp)` / `executeTask()`
and leaves the version semantics to the candidate. The pack freezes one contract — latest add wins per
task ID, ties by earlier timestamp then task ID, cancel returns whether the task was pending — and
tests it against stale heap entries, re-add-lower-priority, and cancel-then-re-add across 15 visible
cases. The solution is a worked lazy-deletion heap.

Microsoft screen custom question bank:

```bash
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py --list-problems
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py tagged_sequence_assembly
```

This seven-problem bank converts publicly reported Microsoft custom-question families into explicit,
runnable contracts with 58 visible cases. The delivered solution remains an intentional blank starter;
the contracts are practice reconstructions rather than claims about exact leaked prompts.

Stripe Linked Merchant / Entity Clustering:

```bash
python3 custom_practice/stripe/linked_merchant_clustering/run_tests.py
```

This reconstructed three-day graph exercise covers expiring shared attributes, component splits and
merges, stateful pin selection, and deterministic output. Its simultaneous split-and-merge and duplicate
record behavior are explicit practice assumptions because the public report does not expose every line
of the original contract.

Stripe OA 2024–2026 complete map:

```text
custom_practice/stripe/oa_question_map/README.md
```

The map covers every main and reserve family in the Stripe question bank, links the closest official
LeetCode problems, and routes uncovered contracts to nine runnable custom packs. All nine custom test
suites were verified with temporary reference implementations (71/71 total) before their solution files
were restored to intentional cold-practice starters.

You can also open `run_tests.py` in VS Code and use **Run Python File**. The script works whether the
terminal is at the repository root or inside the exercise folder.

## Create another custom practice

1. Copy `_template/` to `custom_practice/<company>/<problem_name>/`.
2. Edit the copied `solution.py` and give `solve` the desired function signature.
3. Edit `test_cases.py`. Add each visible test as `Case(name=..., args=(...), expected=...)`.
4. Run the copied `run_tests.py`.

The runner deep-copies each case's arguments before calling the solution, so an in-place solution does
not pollute the next case. For trees, graphs, or stateful classes, keep the shared runner unchanged and
put construction/serialization or operation replay in the exercise's `run_tests.py` adapter.
