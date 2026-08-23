from custom_practice.ordered_nary_tree_deletion.models import t
from custom_practice.runner import Case


TEST_CASES = [
    Case(name="empty tree", args=(None, []), expected=()),
    Case(
        name="delete nothing",
        args=(t(1, t(2), t(3)), []),
        expected=(t(1, t(2), t(3)),),
    ),
    Case(
        name="delete root and return an ordered forest",
        args=(t(1, t(2, t(4)), t(3, t(5))), [1]),
        expected=(t(2, t(4)), t(3, t(5))),
    ),
    Case(
        name="delete every node",
        args=(t(1, t(2), t(3)), [1, 2, 3]),
        expected=(),
    ),
    Case(
        name="delete a parent and its child",
        args=(t(1, t(2, t(3, t(4)), t(5)), t(6)), [2, 3]),
        expected=(t(1, t(4), t(5), t(6)),),
    ),
    Case(
        name="delete several siblings",
        args=(t(1, t(2, t(5)), t(3), t(4, t(6), t(7)), t(8)), [2, 4]),
        expected=(t(1, t(5), t(3), t(6), t(7), t(8)),),
    ),
    Case(
        name="delete a chain of consecutive ancestors",
        args=(t(1, t(2, t(3, t(4, t(5))), t(6)), t(7)), [2, 3, 4]),
        expected=(t(1, t(5), t(6), t(7)),),
    ),
    Case(
        name="ignore values that are absent",
        args=(t(1, t(2), t(3, t(4))), [99, 100]),
        expected=(t(1, t(2), t(3, t(4))),),
    ),
]
