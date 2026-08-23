from collections import deque
from typing import List

from custom_practice.snowflake.ordered_nary_tree_deletion.models import Node


def max_forest_depth(roots: List[Node]) -> int:
    """Return the maximum node-counted height across all forest roots.

    An empty forest has height 0, and a leaf has height 1. Do not mutate the
    forest.
    """
    queue = deque(roots)
    depth = 0

    while queue:
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()

            for child in node.children:
                queue.append(child)

        depth += 1

    return depth
