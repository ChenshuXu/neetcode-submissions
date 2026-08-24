from typing import Sequence


def lower_bound(values: Sequence[int], target: int) -> int:
    """Return the first index whose value is at least target in O(log n) time."""
    # len(values) is the required answer when every value is smaller than target.
    target_index = len(values)
    left = 0
    right = len(values) - 1

    # Search the closed interval [left, right]. target_index stores the
    # earliest valid position found so far.
    while left <= right:
        mid = (left + right) // 2

        if values[mid] >= target:
            # mid qualifies, but duplicates or a smaller qualifying value may
            # exist to its left, so keep searching the left half.
            target_index = mid
            right = mid - 1
        else:
            left = mid + 1

    return target_index


class RepeatedQueryIndex:
    """Build an O(u)-space index for expected O(1) exact-value queries."""

    def __init__(self, values: Sequence[int]) -> None:
        # Keep one fixed-size summary per distinct value instead of storing all
        # occurrence indices: value -> [first_index, occurrence_count].
        self.data = {}
        for index, value in enumerate(values):
            if value not in self.data:
                # The first encounter permanently determines first_index.
                self.data[value] = [index, 1]
            else:
                self.data[value][1] += 1

    def query(self, target: int) -> tuple[int, int]:
        """Return (first_index, occurrence_count), or (-1, 0) when absent."""
        if target not in self.data:
            return (-1, 0)

        # Construction already computed the complete answer, so no scan or
        # binary search is needed for each repeated query.
        first_index, occurrence_count = self.data[target]
        return (first_index, occurrence_count)
