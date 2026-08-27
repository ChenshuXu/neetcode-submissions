from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="single course",
        args=(1, (), (5,), 1),
        expected=5,
    ),
    Case(
        name="parallel courses iii sample with enough workers",
        args=(3, ((1, 3), (2, 3)), (3, 2, 5), 2),
        expected=8,
    ),
    Case(
        name="one worker serializes every course",
        args=(3, ((1, 3), (2, 3)), (3, 2, 5), 1),
        expected=10,
    ),
    Case(
        name="limited workers require exact load balancing",
        args=(3, (), (3, 2, 4), 2),
        expected=5,
    ),
    Case(
        name="greedy task id order is not optimal",
        args=(4, ((1, 4),), (1, 4, 4, 5), 2),
        expected=8,
    ),
    Case(
        name="dependency chain cannot run in parallel",
        args=(3, ((1, 2), (2, 3)), (3, 2, 4), 2),
        expected=9,
    ),
    Case(
        name="three workers still require partitioning",
        args=(4, (), (6, 5, 4, 3), 3),
        expected=7,
    ),
    Case(
        name="fan in waits for every prerequisite",
        args=(4, ((1, 3), (2, 3), (3, 4)), (2, 3, 4, 5), 3),
        expected=12,
    ),
    Case(
        name="parallel courses iii second sample with enough workers",
        args=(
            5,
            ((1, 5), (2, 5), (3, 5), (3, 4), (4, 5)),
            (1, 2, 3, 4, 5),
            5,
        ),
        expected=12,
    ),
]
