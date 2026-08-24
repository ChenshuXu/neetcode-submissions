from typing import Optional


class TransactionalKV:
    """In-memory key-value store with nested transactions."""

    def __init__(self) -> None:
        """Create an empty committed store with no active transaction layers."""
        pass

    def get(self, key: str) -> Optional[int]:
        """Return the newest visible value across transaction layers, or None."""
        raise NotImplementedError("Implement get in solution.py")

    def put(self, key: str, value: int) -> None:
        """Write to the innermost transaction, or committed state if none exists."""
        raise NotImplementedError("Implement put in solution.py")

    def delete(self, key: str) -> None:
        """Hide a key in the innermost transaction, or remove it if none exists."""
        raise NotImplementedError("Implement delete in solution.py")

    def begin(self) -> None:
        """Push a new empty transaction layer, which may be nested."""
        raise NotImplementedError("Implement begin in solution.py")

    def commit(self) -> bool:
        """Merge the innermost layer downward; return False if none is active."""
        raise NotImplementedError("Implement commit in solution.py")

    def rollback(self) -> bool:
        """Discard only the innermost layer; return False if none is active."""
        raise NotImplementedError("Implement rollback in solution.py")
