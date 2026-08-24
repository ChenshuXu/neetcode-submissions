from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty input",
        args=((), (-3, 0, 7)),
        expected=(
            (0, 0, 0),
            ((-1, 0), (-1, 0), (-1, 0)),
        ),
    ),
    Case(
        name="duplicates and insertion boundaries",
        args=((1, 2, 2, 2, 5), (0, 1, 2, 3, 5, 6)),
        expected=(
            (0, 0, 1, 4, 4, 5),
            ((-1, 0), (0, 1), (1, 3), (-1, 0), (4, 1), (-1, 0)),
        ),
    ),
    Case(
        name="all values are duplicates",
        args=((4, 4, 4, 4), (3, 4, 5, 4)),
        expected=(
            (0, 0, 4, 0),
            ((-1, 0), (0, 4), (-1, 0), (0, 4)),
        ),
    ),
    Case(
        name="negative values and a missing middle target",
        args=((-8, -3, -3, 0, 7, 7, 10), (-9, -3, -1, 0, 7, 11)),
        expected=(
            (0, 1, 3, 3, 4, 7),
            ((-1, 0), (1, 2), (-1, 0), (3, 1), (4, 2), (-1, 0)),
        ),
    ),
    Case(
        name="single value",
        args=((6,), (5, 6, 7, 6)),
        expected=(
            (0, 0, 1, 0),
            ((-1, 0), (0, 1), (-1, 0), (0, 1)),
        ),
    ),
    Case(
        name="many repeated queries reuse one index",
        args=((1, 1, 2, 4, 4, 4, 9), (4, 4, 4, 2, 8, 1, 9, 4)),
        expected=(
            (3, 3, 3, 2, 6, 0, 6, 3),
            ((3, 3), (3, 3), (3, 3), (2, 1), (-1, 0), (0, 2), (6, 1), (3, 3)),
        ),
    ),
]

