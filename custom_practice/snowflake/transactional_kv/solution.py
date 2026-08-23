from typing import Optional


class TransactionalKV:
    """In-memory key-value store with nested transactions."""

    def __init__(self) -> None:
        """Initialize an empty store with no active transactions."""
        pass

    def get(self, key: str) -> Optional[int]:
        """Return the currently visible value, or None when the key is missing."""
        raise NotImplementedError("Implement get in solution.py")

    def put(self, key: str, value: int) -> None:
        """Write a value in the current transaction or directly to committed state."""
        raise NotImplementedError("Implement put in solution.py")

    def delete(self, key: str) -> None:
        """Hide or remove a key in the current visible state."""
        raise NotImplementedError("Implement delete in solution.py")

    def begin(self) -> None:
        """Open a new, possibly nested transaction."""
        raise NotImplementedError("Implement begin in solution.py")

    def commit(self) -> bool:
        """Commit the innermost transaction, returning False if none is active."""
        raise NotImplementedError("Implement commit in solution.py")

    def rollback(self) -> bool:
        """Discard the innermost transaction, returning False if none is active."""
        raise NotImplementedError("Implement rollback in solution.py")
