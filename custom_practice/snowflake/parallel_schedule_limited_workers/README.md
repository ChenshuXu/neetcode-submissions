# Snowflake Custom — Parallel Schedule with Limited Workers

This is an answer-free practice reconstruction for the reported Snowflake `Parallel Schedule / DAG`
family. The recoverable interview evidence confirms a follow-up with a limited number of workers, but
it does not recover the original function signature, task-duration model, scheduling objective,
preemption rule, or tie behavior.

This exercise therefore fixes one deterministic contract that trains the reported mechanism. It is
not a verbatim Snowflake prompt, and its output rules must not be presented as recovered interview
facts.

## Contract

Implement:

```python
def schedule_tasks(
    durations: Sequence[int],
    dependencies: Sequence[tuple[int, int]],
    worker_count: int,
) -> tuple[int, tuple[tuple[int, int, int, int], ...]]:
    ...
```

There are `n = len(durations)` tasks with IDs `0` through `n - 1`.

- `durations[task_id]` is the positive integer execution time of that task.
- Each dependency `(before, after)` means `before` must finish before `after` may start.
- Duplicate dependency pairs may appear and represent only one dependency.
- `worker_count` is at least `1`.
- A worker executes at most one task at a time.
- A task uses exactly one worker for its entire duration and cannot be paused or moved.
- A task may start at the exact time its final prerequisite finishes.
- The input collections must not be mutated.

Whenever one or more workers are free, assign ready tasks immediately using these deterministic
rules:

1. Process every task completion at the current time before making new assignments.
2. Choose ready tasks in ascending task-ID order.
3. Choose free workers in ascending worker-ID order. Worker IDs are `0` through
   `worker_count - 1`.

Return:

```text
(completion_time, schedule)
```

Each schedule entry is:

```text
(task_id, worker_id, start_time, end_time)
```

Entries must appear in assignment order: ascending `start_time`, then ascending `worker_id` for
assignments made at the same time.

Special cases:

- If there are no tasks, return `(0, ())`.
- If the dependencies contain a directed cycle, return `(-1, ())`.
- `completion_time` is the final task's end time under the deterministic dispatch policy above. It
  is not required to be the globally minimum possible completion time.

## Example

```python
durations = [2, 2, 3, 1]
dependencies = [(0, 2), (1, 2), (1, 3)]
worker_count = 2
```

Expected result:

```text
(
    5,
    (
        (0, 0, 0, 2),
        (1, 1, 0, 2),
        (2, 0, 2, 5),
        (3, 1, 2, 3),
    ),
)
```

## Run it

Implement `schedule_tasks` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py --list
python3 custom_practice/snowflake/parallel_schedule_limited_workers/run_tests.py --case cycle
```

The supplied starter intentionally raises `NotImplementedError` and contains no reference solution.

## Questions to clarify aloud before coding

1. Are task durations all equal, or does each task have its own duration?
2. Is the goal a deterministic feasible schedule or the globally shortest completion time?
3. Can a running task be preempted or moved to another worker?
4. What should happen when multiple ready tasks or workers are available simultaneously?
5. Can dependency pairs repeat, and how should a cycle be reported?

## Follow-ups to discuss after the base passes

1. What changes if the interviewer requires the exact minimum completion time?
2. What changes if every task has duration `1`?
3. How would worker-specific task capabilities change the contract?
4. How would task failure and retry affect dependency release?

