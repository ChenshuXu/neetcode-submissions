import heapq
from typing import Optional


class TaskExecutor:
    """Priority task queue where re-adding a task ID replaces its pending version."""

    def __init__(self) -> None:
        """Initialize an empty executor."""
        # Lazy-deletion heap of (-priority, timestamp, task_id, version).
        # Entries are never removed on cancel or re-add; they are skipped on the way out.
        self.heap = []

        # task_id -> version of its one pending entry.
        # This dict, not the heap, is the authority on what is still pending.
        self.pending = {}

        # Monotonic counter, so a re-added task never reuses a version that an
        # older heap entry still carries.
        self.next_version = 0

    def add_task(self, task_id: str, priority: int, timestamp: int) -> None:
        """Add a pending task, replacing any pending version of the same ID."""
        version = self.next_version
        self.next_version += 1

        # Overwriting the dict entry is what invalidates the previous version:
        # its heap entry now carries a version no longer recorded as pending.
        self.pending[task_id] = version
        heapq.heappush(self.heap, (-priority, timestamp, task_id, version))

    def cancel_task(self, task_id: str) -> bool:
        """Drop a pending task; return whether it was pending."""
        if task_id not in self.pending:
            return False

        del self.pending[task_id]
        return True

    def execute_task(self) -> Optional[str]:
        """Remove and return the most urgent pending task ID, or None if there is none."""
        while self.heap:
            _, _, task_id, version = heapq.heappop(self.heap)

            # Skip stale entries: cancelled tasks and superseded versions.
            if self.pending.get(task_id) != version:
                continue

            del self.pending[task_id]
            return task_id

        return None
