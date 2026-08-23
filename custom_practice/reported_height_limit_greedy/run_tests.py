from itertools import combinations
from pathlib import Path
import sys
from typing import List, Optional, Set


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.ordered_nary_tree_deletion.models import (  # noqa: E402
    Node,
    TreeSpec,
    build_tree,
    forest_to_spec,
    format_tree,
)
from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import minimum_deletions_for_height  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def delete_nodes_reference(
    root: Optional[Node],
    to_delete: Set[int],
) -> List[Node]:
    if root is None:
        return []

    def dfs(node: Node) -> List[Node]:
        new_children = []
        for child in node.children:
            new_children.extend(dfs(child))
        node.children = new_children
        return new_children if node.val in to_delete else [node]

    return dfs(root)


def max_forest_depth_reference(roots: List[Node]) -> int:
    def depth(node: Node) -> int:
        return 1 + max((depth(child) for child in node.children), default=0)

    return max((depth(root) for root in roots), default=0)


def collect_values(root: Optional[Node]) -> List[int]:
    if root is None:
        return []

    values = [root.val]
    for child in root.children:
        values.extend(collect_values(child))
    return values


def brute_force_minimum(root_spec: TreeSpec, max_height: int) -> int:
    root = build_tree(root_spec)
    if root is None:
        return 0

    candidates = collect_values(root)[1:]
    for size in range(len(candidates) + 1):
        for selected in combinations(candidates, size):
            forest = delete_nodes_reference(
                build_tree(root_spec),
                set(selected),
            )
            if max_forest_depth_reference(forest) <= max_height:
                return size

    raise AssertionError("no valid deletion set found")


def run_candidate(root_spec: TreeSpec, max_height: int) -> int:
    root = build_tree(root_spec)
    removed = minimum_deletions_for_height(root, max_height)

    if not isinstance(removed, list):
        raise TypeError("minimum_deletions_for_height must return list[int]")
    if len(removed) != len(set(removed)):
        raise AssertionError("returned deletion values must be unique")

    values = set(collect_values(build_tree(root_spec)))
    if root is not None and root.val in removed:
        raise AssertionError("the original root cannot be deleted")

    unknown = set(removed) - values
    if unknown:
        raise AssertionError(f"unknown deletion values: {sorted(unknown)}")

    if root is not None and forest_to_spec([root])[0] != root_spec:
        raise AssertionError("minimum_deletions_for_height must not mutate the tree")

    forest = delete_nodes_reference(build_tree(root_spec), set(removed))
    actual_height = max_forest_depth_reference(forest)
    if actual_height > max_height:
        raise AssertionError(
            f"resulting height is {actual_height}, expected <= {max_height}"
        )

    minimum_count = brute_force_minimum(root_spec, max_height)
    if len(removed) != minimum_count:
        raise AssertionError(
            f"used {len(removed)} deletions, but the minimum is {minimum_count}"
        )

    return len(removed)


def show_input(case: Case) -> str:
    root_spec, max_height = case.args
    return f"root={format_tree(root_spec)}, max_height={max_height}"


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
        )
    )
