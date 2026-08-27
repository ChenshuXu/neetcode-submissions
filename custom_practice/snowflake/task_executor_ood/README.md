# Snowflake Custom — Task Executor OOD

Runnable cold-practice contract for Snowflake `[P1-07]`. Public interview reports fix only the base
API — `addTask(taskId, priority, timestamp)` plus `executeTask()`, with the same task ID allowed to
appear more than once — and explicitly leave the selection rule and the version semantics for the
candidate to define. This exercise freezes one deterministic contract so it can be implemented and
tested under interview conditions.

This is not a verbatim copy of one private prompt. `cancel` is included because the archived
follow-up list for this family names cancellation and stale heap entries together; concurrency,
worker crash / no-loss retry, and multiple priority queues are left as discussion follow-ups because
no single reported round establishes them as one continuous line of questioning.

## Contract

Implement `TaskExecutor` in `solution.py`:

```python
class TaskExecutor:
    def add_task(self, task_id: str, priority: int, timestamp: int) -> None:
        ...

    def cancel_task(self, task_id: str) -> bool:
        ...

    def execute_task(self) -> Optional[str]:
        ...
```

Rules:

- `task_id` is a non-empty string. `priority` is an integer where **a larger number is more
  urgent**. `timestamp` is a non-negative integer submission time. Inputs satisfy these
  constraints, so input validation is not required.
- A task is **pending** from the moment it is added until it is executed or cancelled.
- **Latest version wins.** Adding a `task_id` that is already pending replaces that pending task
  outright: the new priority and timestamp are the only ones that count, even when the new priority
  is *lower*. One `task_id` never has two pending entries.
- Adding a `task_id` that was already executed or cancelled creates a fresh pending task. There is
  no memory of the finished one.
- `execute_task()` removes and returns the `task_id` of the pending task with the highest priority.
  Ties break by smaller `timestamp` first (earlier submission wins), then by smaller `task_id`
  lexicographically, so the result is fully deterministic.
- `execute_task()` returns `None` when nothing is pending.
- Execution is **non-preemptive in the caller's hands**: this class hands out one task per call and
  keeps no running state. A task is gone from the executor the moment it is returned.
- `cancel_task(task_id)` removes that task from the pending set and returns `True`. It returns
  `False` when the task is not pending, including when it was never added or was already executed.
- Timestamps may repeat and may arrive out of order. They order tasks; they do not gate execution.

Example:

```text
ex.add_task("build", 5, 10)
ex.add_task("test", 5, 20)
ex.add_task("deploy", 9, 30)

ex.execute_task()          -> "deploy"   # highest priority
ex.add_task("build", 1, 40)              # same ID, new version: priority drops to 1
ex.execute_task()          -> "test"     # the stale priority-5 build entry must not win
ex.cancel_task("build")    -> True
ex.execute_task()          -> None
```

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/task_executor_ood/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/task_executor_ood/run_tests.py --list
python3 custom_practice/snowflake/task_executor_ood/run_tests.py --case stale
```

The runner creates a fresh executor for every case and records output only for `execute_task` and
`cancel_task`. `solution.py` holds the worked solution; for a cold attempt, copy it aside and stub
the three method bodies back to `raise NotImplementedError` before starting the timer.

## Interview target

45 minutes for the base, matching the plan entry.

- 0–5 minutes: clarify priority direction, what a repeated ID means, the tie rule, whether
  `execute_task` blocks or returns `None` on empty, and whether cancel affects a task already
  handed out.
- 5–10 minutes: state the representation and the invariant — the heap may hold stale entries, the
  dictionary is the only authority on what is pending.
- 10–35 minutes: implement all three methods.
- 35–45 minutes: run empty, priority-order, both tie levels, re-add-higher, re-add-lower,
  cancel-then-re-add, and stale-drain tests.
- 45–60 minutes: take the follow-ups below.

Let `p` be the number of pending tasks and `n` the total number of `add_task` calls.
`add_task` is `O(log n)`, `cancel_task` is `O(1)`, and `execute_task` is amortized `O(log n)`
because every heap entry is pushed once and popped once. Heap space is `O(n)` rather than `O(p)`,
which is the price of lazy deletion — say that out loud rather than claiming `O(p)`.

## Follow-ups to discuss after the base passes

1. Stale entries make the heap grow with total adds, not pending tasks. When would you switch to an
   indexed heap with real `decrease-key` / `delete`, and what does that cost in code complexity?
2. Multiple priority queues — one per class of work — instead of one comparison key. How is
   starvation of the low-priority queue prevented, and how does aging change the ordering key?
3. Concurrency: which operations need mutual exclusion, and where does a single global lock become
   the bottleneck once many workers call `execute_task` at once?
4. Worker crash with no task loss. What has to be recorded before a task is handed to a worker,
   how is a lease or heartbeat used to detect the crash, and what makes retry idempotent?
5. Persistence and recovery: what does the executor write down so a restart rebuilds the same
   pending set, and how are stale entries dropped during recovery?
6. What changes when a task must not run before its timestamp — a scheduled-time queue rather than
   a submission-time tiebreaker?
