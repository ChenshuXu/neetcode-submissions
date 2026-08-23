from typing import List, Optional

from custom_practice.ordered_nary_tree_deletion.models import Node


def minimum_deletions_for_height(
    root: Optional[Node],
    max_height: int,
) -> List[int]:
    """Return a minimum-size deletion set that makes height <= max_height.

    The root cannot be deleted. Height counts nodes. Deleting a non-root node
    costs one operation and promotes its children to its parent. Node values are
    unique. Assume max_height >= 1. Do not mutate the tree.

    Any valid minimum-size set is accepted by the test harness.
    """
    if root is None:
        return []

    memo = {}

    def min_cost(node: Node, height_budget: int) -> int:
        key = (id(node), height_budget)
        if key in memo:
            return memo[key]

        delete_cost = 1 + sum(
            min_cost(child, height_budget) for child in node.children
        )

        if height_budget == 0:
            memo[key] = delete_cost
            return delete_cost

        keep_cost = sum(
            min_cost(child, height_budget - 1) for child in node.children
        )
        memo[key] = min(keep_cost, delete_cost)
        return memo[key]

    removed = []

    def collect(node: Node, height_budget: int) -> None:
        delete_cost = 1 + sum(
            min_cost(child, height_budget) for child in node.children
        )
        keep_cost = (
            sum(
                min_cost(child, height_budget - 1)
                for child in node.children
            )
            if height_budget > 0
            else float("inf")
        )

        if keep_cost <= delete_cost:
            for child in node.children:
                collect(child, height_budget - 1)
        else:
            removed.append(node.val)
            for child in node.children:
                collect(child, height_budget)

    child_budget = max_height - 1
    for child in root.children:
        collect(child, child_budget)

    return removed
