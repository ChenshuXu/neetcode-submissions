class HitCounter:
    """Count hits in the inclusive 300-second window ending at each query."""

    def __init__(self) -> None:
        """Initialize the counter."""
        raise NotImplementedError("Implement HitCounter in solution.py")

    def hit(self, timestamp: int) -> None:
        """Record one hit at a monotonically nondecreasing timestamp."""
        raise NotImplementedError("Implement hit in solution.py")

    def getHits(self, timestamp: int) -> int:
        """Return hits whose timestamps are in [timestamp - 299, timestamp]."""
        raise NotImplementedError("Implement getHits in solution.py")
