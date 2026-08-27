# Snowflake Custom — Parallel Courses III with Limited Workers

This practice keeps the contract of LeetCode 2050, Parallel Courses III, and adds one resource
constraint: at most `worker_count` courses may run at the same time.

The recovered Snowflake evidence confirms only a Parallel Schedule / DAG base with a limited-worker
follow-up. It does not recover the exact private prompt. This exercise uses LC2050 as the explicit
base contract without adding schedule output, worker identities, tie-breaking rules, duplicate-edge
behavior, or cycle behavior.

## Contract

Implement:

```python
class Solution:
    def minimumTime(
        self,
        n: int,
        relations: List[List[int]],
        time: List[int],
        workerCount: int,
    ) -> int:
        ...
```

The LC2050 rules remain unchanged:

- There are `n` courses labeled from `1` through `n`.
- `relations[i] = (previous, next_course)` means `previous` must finish before `next_course`
  may start.
- Every relation is unique, and the relations form a directed acyclic graph.
- `time[i]` is the positive integer duration of course `i + 1`.
- A course may start as soon as all of its prerequisites have finished.
- A running course occupies one worker for its entire duration.
- Courses cannot be paused or moved between workers.
- At most `workerCount` courses may run simultaneously.
- Return only the minimum possible time needed to finish every course.
- Do not mutate the input collections.

Practice constraints:

```text
1 <= n <= 12
1 <= workerCount <= n
0 <= len(relations) <= n * (n - 1) / 2
1 <= time[i] <= 10^4
```

The smaller `n` is intentional. Once finite workers are added, finding the exact minimum makespan is
NP-hard in general, even though the unlimited-worker LC2050 problem has a linear-time DAG dynamic
programming solution.

## Example

```python
n = 3
relations = []
time = [3, 2, 4]
workerCount = 2
```

The optimal assignment runs durations `3` and `2` on one worker and duration `4` on the other, so:

```text
Solution().minimumTime(3, [], [3, 2, 4], 2) -> 5
```

## Exact approach

Start with the same adjacency list, indegree map, queue, and Kahn traversal as LC2050. The original
`finishTime[course]` is no longer a complete state because ready courses can wait for a worker. Replace
that one-dimensional DP with event-driven state dynamic programming.

A memoized state contains:

```text
(completed_courses, running_courses_with_remaining_times)
```

At each task-completion event:

1. Find every unscheduled course whose prerequisite set is contained in the completed-course set.
2. If more courses are ready than there are free workers, enumerate every possible subset that can
   start now. Workers are identical, so worker IDs do not belong in the state.
3. Start the chosen courses and jump directly to the next completion event.
4. Mark every course completing at that event and recursively compute the best remaining time.
5. Store completed courses in a `frozenset` so the normalized state can be memoized.

Enumerating every possible priority choice covers the dominant set of non-delay list schedules for
identical workers and makespan minimization. The algorithm is exact but exponential, which is why the
exercise uses `n <= 12`.

## Run it

```bash
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py --list
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py --case greedy
```

## Interview clarification

Before solving the follow-up, say explicitly:

```text
Should I still return the globally minimum completion time after adding worker_count?
What is the new maximum n?
```

Keeping LC2050's original `n <= 5 * 10^4` while also requiring an exact finite-worker optimum would
not be a realistic polynomial-time extension.
