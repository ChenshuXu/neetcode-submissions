from custom_practice.ordered_nary_tree_deletion.models import t
from custom_practice.runner import Case


TEST_CASES = [
    Case(name="empty tree", args=(None, 1), expected=0),
    Case(name="root only", args=(t(1), 1), expected=0),
    Case(
        name="tree already fits",
        args=(t(1, t(2), t(3)), 2),
        expected=0,
    ),
    Case(
        name="chain needs two promotions",
        args=(t(1, t(2, t(3, t(4)))), 2),
        expected=2,
    ),
    Case(
        name="one branching child is too tall",
        args=(t(1, t(2, t(4), t(5)), t(3)), 2),
        expected=1,
    ),
    Case(
        name="one branch exceeds height by one",
        args=(t(1, t(2, t(4, t(6))), t(3, t(5))), 3),
        expected=1,
    ),
    Case(
        name="max height one requires deleting every non-root node",
        args=(t(1, t(2, t(4)), t(3, t(5))), 1),
        expected=4,
    ),
]
