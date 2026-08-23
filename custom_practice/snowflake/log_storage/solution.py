from typing import List


class LogSystem:
    """Store timestamped log IDs and retrieve them at a requested granularity."""

    def __init__(self) -> None:
        """Initialize the log store."""
        raise NotImplementedError("Implement LogSystem in solution.py")

    def put(self, log_id: int, timestamp: str) -> None:
        """Store one unique log ID and its fixed-width timestamp."""
        raise NotImplementedError("Implement put in solution.py")

    def retrieve(
        self,
        start: str,
        end: str,
        granularity: str,
    ) -> List[int]:
        """Return IDs in the inclusive range at the requested granularity."""
        raise NotImplementedError("Implement retrieve in solution.py")
