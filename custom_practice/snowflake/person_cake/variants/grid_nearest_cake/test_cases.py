import random
from typing import Iterator, Optional, Sequence, Tuple

from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty grid",
        args=([],),
        expected=(),
    ),
    Case(
        name="grid with no columns",
        args=([[], []],),
        expected=(),
    ),
    Case(
        name="no people",
        args=([[0, 2, 0], [0, 0, 0]],),
        expected=(),
    ),
    Case(
        name="single person cell",
        args=([[1]],),
        expected=(((0, 0), -1),),
    ),
    Case(
        name="no cake anywhere",
        args=([[1, 0, 0], [0, 0, 1]],),
        expected=(((0, 0), -1), ((1, 2), -1)),
    ),
    Case(
        name="person next to a cake",
        args=([[1, 2]],),
        expected=(((0, 0), 1),),
    ),
    Case(
        name="two cakes choose the nearer one",
        args=(
            [
                [0, 0, 2, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [1, 0, 0, 0, 2],
            ],
        ),
        expected=(((1, 1), 2), ((3, 0), 4)),
    ),
    Case(
        name="equal-distance tie",
        args=(
            [
                [2, 0, 0, 0, 2],
                [0, 0, 1, 0, 0],
            ],
        ),
        expected=(((1, 2), 3),),
    ),
    Case(
        name="several people share one cake",
        args=(
            [
                [1, 0, 1],
                [0, 2, 0],
                [1, 0, 0],
            ],
        ),
        expected=(((0, 0), 2), ((0, 2), 2), ((2, 0), 2)),
    ),
    Case(
        name="search passes through other people",
        args=([[2, 1, 1]],),
        expected=(((0, 1), 1), ((0, 2), 2)),
    ),
    Case(
        name="single column with two cakes",
        args=([[2], [0], [1], [0], [2], [1]],),
        expected=(((2, 0), 2), ((5, 0), 1)),
    ),
    Case(
        name="opposite corners",
        args=(
            [
                [2, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
            ],
        ),
        expected=(((2, 3), 5),),
    ),
    Case(
        name="cake surrounded by people",
        args=(
            [
                [0, 1, 0],
                [1, 2, 1],
                [0, 1, 0],
            ],
        ),
        expected=(((0, 1), 1), ((1, 0), 1), ((1, 2), 1), ((2, 1), 1)),
    ),
]


def expected_distances(
    grid: Sequence[Sequence[int]],
) -> Tuple[Tuple[Tuple[int, int], int], ...]:
    """Return a small-grid oracle result by enumerating every cake.

    No cell blocks movement, so the shortest path length between two cells is
    their Manhattan distance.
    """

    people = []
    cakes = []

    for row, values in enumerate(grid):
        for column, value in enumerate(values):
            if value == 1:
                people.append((row, column))
            elif value == 2:
                cakes.append((row, column))

    expected = []
    for person_row, person_column in people:
        nearest: Optional[int] = None
        for cake_row, cake_column in cakes:
            distance = abs(person_row - cake_row) + abs(person_column - cake_column)
            if nearest is None or distance < nearest:
                nearest = distance

        expected.append(((person_row, person_column), -1 if nearest is None else nearest))

    return tuple(expected)


def randomized_test_cases(seed_count: int = 1000) -> Iterator[Case]:
    """Yield reproducible small grids for differential testing."""

    for seed in range(seed_count):
        random_generator = random.Random(seed)
        rows = random_generator.randint(0, 6)

        grid = []
        if rows > 0:
            columns = random_generator.randint(0, 6)
            for _ in range(rows):
                grid.append(
                    [random_generator.choice([0, 0, 0, 1, 2]) for _ in range(columns)]
                )

        yield Case(
            name=f"random seed {seed}",
            args=(grid,),
            expected=expected_distances(grid),
        )
