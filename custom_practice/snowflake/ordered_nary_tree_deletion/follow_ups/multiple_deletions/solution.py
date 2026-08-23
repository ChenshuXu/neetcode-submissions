from typing import List, Optional

from custom_practice.snowflake.ordered_nary_tree_deletion.models import Node


def delete_nodes(
    root: Optional[Node],
    to_delete: List[int],
) -> List[Node]:
    """Delete all listed nodes and return the ordered surviving forest.

    Deleted nodes promote their processed children. Parent and child nodes may
    both be deleted. Node values are unique, and mutation is allowed.
    """
    if root is None:
        return []

    def dfs(node) -> List[Node]:
        """Return the ordered roots that replace this subtree after deletion.

        If ``node`` survives, return ``[node]``. If it is deleted, return its
        surviving child roots so the caller can promote them into its own
        children list. The returned list may be empty.
        """
        new_children = []
        for child in node.children:
            # A deleted child may contribute multiple promoted descendants.
            new_children.extend(dfs(child))

        # Rebuild the child list only after every child subtree is processed.
        node.children = new_children
        if node.val in to_delete:
            # Removing this node promotes its surviving children in place.
            return new_children
        return [node]

    return dfs(root)
