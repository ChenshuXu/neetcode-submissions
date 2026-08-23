from custom_practice.runner import Case
from models import t


TEST_CASES = [
    Case(
        name="empty tree",
        args=(None, 1),
        expected=(),
    ),
    Case(
        name="target is absent",
        args=(t(1, t(2), t(3)), 99),
        expected=(t(1, t(2), t(3)),),
    ),
    Case(
        name="delete a leaf",
        args=(t(1, t(2), t(3), t(4)), 3),
        expected=(t(1, t(2), t(4)),),
    ),
    Case(
        name="delete middle child and promote children in place",
        args=(t(1, t(2), t(3, t(5), t(6)), t(4)), 3),
        expected=(t(1, t(2), t(5), t(6), t(4)),),
    ),
    Case(
        name="delete a deeper internal node",
        args=(t(1, t(2, t(3, t(4), t(5)), t(6)), t(7)), 3),
        expected=(t(1, t(2, t(4), t(5), t(6)), t(7)),),
    ),
    Case(
        name="delete root and return its children as a forest",
        args=(t(1, t(2, t(4)), t(3, t(5), t(6))), 1),
        expected=(t(2, t(4)), t(3, t(5), t(6))),
    ),
    Case(
        name="delete the only node",
        args=(t(1), 1),
        expected=(),
    ),
]
