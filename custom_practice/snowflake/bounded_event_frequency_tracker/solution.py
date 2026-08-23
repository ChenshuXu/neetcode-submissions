from typing import Optional


class BoundedEventFrequency:
    """Track the most frequent key in a bounded recent-time window."""

    def __init__(self, window_seconds: int) -> None:
        """Initialize any state needed for a positive-length window."""
        self.window_seconds = window_seconds

    def record(self, timestamp: int, key: str) -> None:
        """Record one event at a timestamp no earlier than previous calls."""
        raise NotImplementedError("Implement record in solution.py")

    def most_frequent(self, now: int) -> Optional[str]:
        """Return the most frequent active key, using lexicographic tie-breaking."""
        raise NotImplementedError("Implement most_frequent in solution.py")
