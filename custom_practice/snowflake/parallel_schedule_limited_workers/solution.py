from typing import Sequence


ScheduleEntry = tuple[int, int, int, int]


def schedule_tasks(
    durations: Sequence[int],
    dependencies: Sequence[tuple[int, int]],
    worker_count: int,
) -> tuple[int, tuple[ScheduleEntry, ...]]:
    """Return the completion time and deterministic limited-worker schedule."""
    raise NotImplementedError("Implement schedule_tasks")
