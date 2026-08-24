from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty task set",
        args=((), (), 2),
        expected=(0, ()),
    ),
    Case(
        name="single task with extra workers",
        args=((5,), (), 3),
        expected=(5, ((0, 0, 0, 5),)),
    ),
    Case(
        name="dependency chain uses one worker at a time",
        args=((3, 2, 4), ((0, 1), (1, 2)), 2),
        expected=(
            9,
            (
                (0, 0, 0, 3),
                (1, 0, 3, 5),
                (2, 0, 5, 9),
            ),
        ),
    ),
    Case(
        name="worker limit delays an independent task",
        args=((3, 2, 4), (), 2),
        expected=(
            6,
            (
                (0, 0, 0, 3),
                (1, 1, 0, 2),
                (2, 1, 2, 6),
            ),
        ),
    ),
    Case(
        name="simultaneous completions release multiple tasks",
        args=((2, 2, 3, 1), ((0, 2), (1, 2), (1, 3)), 2),
        expected=(
            5,
            (
                (0, 0, 0, 2),
                (1, 1, 0, 2),
                (2, 0, 2, 5),
                (3, 1, 2, 3),
            ),
        ),
    ),
    Case(
        name="duplicate dependency does not block twice",
        args=((1, 2), ((0, 1), (0, 1)), 1),
        expected=(
            3,
            (
                (0, 0, 0, 1),
                (1, 0, 1, 3),
            ),
        ),
    ),
    Case(
        name="directed cycle",
        args=((1, 1), ((0, 1), (1, 0)), 2),
        expected=(-1, ()),
    ),
    Case(
        name="new lower id ready task beats an older ready task",
        args=((4, 1, 2, 3), ((1, 2),), 2),
        expected=(
            6,
            (
                (0, 0, 0, 4),
                (1, 1, 0, 1),
                (2, 1, 1, 3),
                (3, 1, 3, 6),
            ),
        ),
    ),
    Case(
        name="deterministic policy is not an optimality promise",
        args=((1, 4, 4, 5), ((0, 3),), 2),
        expected=(
            9,
            (
                (0, 0, 0, 1),
                (1, 1, 0, 4),
                (2, 0, 1, 5),
                (3, 1, 4, 9),
            ),
        ),
    ),
]

