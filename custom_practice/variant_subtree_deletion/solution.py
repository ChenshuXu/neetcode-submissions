from typing import List, Optional

from custom_practice.ordered_nary_tree_deletion.models import Node


def delete_subtrees(
    root: Optional[Node],
    to_delete: List[int],
) -> List[Node]:
    """Delete each listed node and its entire subtree.

    This is not child promotion. If the original root survives, return [root].
    If the root is deleted or the input is empty, return []. Node values are
    unique, and mutation is allowed.
    """

    raise NotImplementedError("Implement delete_subtrees in solution.py")
