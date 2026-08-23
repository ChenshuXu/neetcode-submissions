from custom_practice.runner import Case


TEST_CASES = [
    Case(name="empty forest", args=([], []), expected=[]),
    Case(
        name="delete nothing",
        args=([-1, 0, 0, 1, 1], []),
        expected=[-1, 0, 0, 1, 1],
    ),
    Case(
        name="delete internal parent",
        args=([-1, 0, 0, 1, 1], [1]),
        expected=[-1, -2, 0, 0, 0],
    ),
    Case(
        name="delete root",
        args=([-1, 0, 0, 1], [0]),
        expected=[-2, -1, -1, 1],
    ),
    Case(
        name="delete root and one child",
        args=([-1, 0, 0, 1], [0, 1]),
        expected=[-2, -2, -1, -1],
    ),
    Case(
        name="delete consecutive ancestors in a chain",
        args=([-1, 0, 1, 2, 3], [1, 2]),
        expected=[-1, -2, -2, 0, 3],
    ),
    Case(
        name="delete every node",
        args=([-1, 0, 1], [0, 1, 2]),
        expected=[-2, -2, -2],
    ),
    Case(
        name="forest with two roots",
        args=([-1, -1, 0, 1, 2], [0]),
        expected=[-2, -1, -1, 1, 2],
    ),
]
