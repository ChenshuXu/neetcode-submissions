from custom_practice.snowflake.ordered_nary_tree_deletion.models import t
from custom_practice.runner import Case


TEST_CASES = [
    Case(name="empty tree", args=(None, []), expected=()),
    Case(
        name="delete nothing",
        args=(t(1, t(2), t(3)), []),
        expected=(t(1, t(2), t(3)),),
    ),
    Case(
        name="delete a leaf subtree",
        args=(t(1, t(2), t(3), t(4)), [3]),
        expected=(t(1, t(2), t(4)),),
    ),
    Case(
        name="delete an internal node and all descendants",
        args=(t(1, t(2, t(5), t(6)), t(3), t(4)), [2]),
        expected=(t(1, t(3), t(4)),),
    ),
    Case(
        name="delete the root subtree",
        args=(t(1, t(2), t(3)), [1]),
        expected=(),
    ),
    Case(
        name="delete multiple disjoint subtrees",
        args=(t(1, t(2, t(5)), t(3), t(4, t(6), t(7)), t(8)), [2, 4]),
        expected=(t(1, t(3), t(8)),),
    ),
    Case(
        name="deleting a parent makes descendant deletion irrelevant",
        args=(t(1, t(2, t(3, t(4)), t(5)), t(6)), [2, 3]),
        expected=(t(1, t(6)),),
    ),
    Case(
        name="ignore values that are absent",
        args=(t(1, t(2), t(3)), [99]),
        expected=(t(1, t(2), t(3)),),
    ),
]
