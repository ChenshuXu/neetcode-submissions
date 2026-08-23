from typing import List, Optional

from models import Node


def delete_node(root: Optional[Node], target: int) -> List[Node]:
    """Delete target and promote its children while preserving their order.

    Return a list of roots:
    - [] for an empty tree or when deleting the only node
    - [root] when the original root remains
    - the deleted root's children when target is the root

    Node values are unique. If target is absent, return the original tree as [root].
    You may mutate the supplied tree.
    """
    if root is None:
        return []

    if root.val == target:
        return root.children
    
    def dfs(node):
        new_children = []
        for child in node.children:
            if child.val != target:
                new_children.append(child)
                dfs(child)
            else:
                new_children.extend(child.children)
        node.children = new_children
    dfs(root)
    return [root]