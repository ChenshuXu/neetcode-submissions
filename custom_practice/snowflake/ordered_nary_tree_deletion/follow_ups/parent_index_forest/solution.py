from typing import List


def delete_from_parent_array(
    parent: List[int],
    to_delete: List[int],
) -> List[int]:
    """Delete indices and reconnect survivors to nearest surviving ancestors.

    parent[node] is the parent index, -1 marks a root, and -2 must mark a
    deleted node in the returned array. The input is a valid forest.
    """

    raise NotImplementedError("Implement delete_from_parent_array in solution.py")
