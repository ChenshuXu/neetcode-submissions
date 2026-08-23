from custom_practice.ordered_nary_tree_deletion.models import t
from custom_practice.runner import Case


TEST_CASES = [
    Case(name="empty tree", args=(None, 1), expected=0),
    Case(name="root only", args=(t(1), 1), expected=0),
    Case(
        name="tree already fits",
        args=(t(1, t(2, t(4)), t(3, t(5))), 3),
        expected=0,
    ),
    Case(
        name="one deletion has multiple optimal positions",
        args=(t(1, t(2, t(3, t(4)))), 3),
        expected=1,
    ),
    Case(
        name="delete the shared ancestor instead of both branches",
        args=(
            t(
                1,
                t(2, t(3, t(5)), t(4, t(6))),
                t(7),
            ),
            3,
        ),
        expected=1,
    ),
    Case(
        name="chain requires repeated promotions",
        args=(t(1, t(2, t(3, t(4, t(5))))), 2),
        expected=3,
    ),
    Case(
        name="independent tall root branches",
        args=(
            t(
                1,
                t(2, t(4, t(6))),
                t(3, t(5, t(7))),
            ),
            2,
        ),
        expected=4,
    ),
    Case(
        name="max height one deletes every non-root node",
        args=(t(1, t(2, t(4)), t(3, t(5))), 1),
        expected=4,
    ),
]
