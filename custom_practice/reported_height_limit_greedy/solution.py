from typing import List, Optional

from custom_practice.ordered_nary_tree_deletion.models import Node


def minimum_deletions_for_height(
    root: Optional[Node],
    max_height: int,
) -> List[int]:
    """Return any minimum-size deletion set that makes height <= max_height.

    The root cannot be deleted. Deleting a node costs one operation and
    promotes its children to its parent. Height counts nodes, node values are
    unique, and the input tree must not be mutated. Assume max_height >= 1.

    The reported follow-up expects an O(n) postorder greedy solution.
    """
    raise NotImplementedError(
        "Implement minimum_deletions_for_height in solution.py"
    )
