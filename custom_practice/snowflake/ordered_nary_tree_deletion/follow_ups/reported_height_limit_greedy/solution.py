from typing import List, Optional

from custom_practice.snowflake.ordered_nary_tree_deletion.models import Node


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
    if root is None:
        return []

    if max_height < 1:
        raise ValueError(
            "max_height must be at least 1 when root cannot be deleted"
        )

    # Values are unique, so they are safe dictionary keys even when Node
    # itself is an unhashable dataclass in the local practice.
    subtree_height = {}

    def get_height(node: Node) -> int:
        child_height = 0

        for child in node.children:
            child_height = max(child_height, get_height(child))

        subtree_height[node.val] = 1 + child_height
        return subtree_height[node.val]

    get_height(root)
    removed_values = []

    def choose(node: Node) -> None:
        if subtree_height[node.val] <= max_height - 1:
            return

        removed_values.append(node.val)

        for child in node.children:
            choose(child)

    for child in root.children:
        choose(child)

    return removed_values