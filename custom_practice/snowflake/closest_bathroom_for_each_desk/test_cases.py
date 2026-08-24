import random
from typing import Iterator, Sequence, Tuple

from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty grid",
        args=([],),
        expected=(),
    ),
    Case(
        name="no desks",
        args=(["..B", "..."],),
        expected=(),
    ),
    Case(
        name="one adjacent bathroom",
        args=(["DB"],),
        expected=(((0, 0), 1),),
    ),
    Case(
        name="multiple bathrooms choose the nearest",
        args=(
            [
                "..B..",
                ".D...",
                ".....",
                "D...B",
            ],
        ),
        expected=(
            ((1, 1), 2),
            ((3, 0), 4),
        ),
    ),
    Case(
        name="multiple desks may share one bathroom",
        args=(
            [
                "D.D",
                ".B.",
                "D..",
            ],
        ),
        expected=(
            ((0, 0), 2),
            ((0, 2), 2),
            ((2, 0), 2),
        ),
    ),
    Case(
        name="equal-distance tie",
        args=(
            [
                "B...B",
                "..D..",
            ],
        ),
        expected=(((1, 2), 3),),
    ),
    Case(
        name="no bathroom",
        args=(
            [
                "D..",
                "..D",
            ],
        ),
        expected=(
            ((0, 0), -1),
            ((1, 2), -1),
        ),
    ),
    Case(
        name="bathroom and desk at opposite corners",
        args=(
            [
                "B...",
                "....",
                "...D",
            ],
        ),
        expected=(((2, 3), 5),),
    ),
    Case(
        name="single bathroom cell",
        args=(["B"],),
        expected=(),
    ),
    Case(
        name="single desk cell",
        args=(["D"],),
        expected=(((0, 0), -1),),
    ),
    Case(
        name="search continues through a desk",
        args=(["BDD"],),
        expected=(
            ((0, 1), 1),
            ((0, 2), 2),
        ),
    ),
    Case(
        name="single column with multiple bathrooms",
        args=(
            [
                "B",
                ".",
                "D",
                ".",
                "B",
                "D",
            ],
        ),
        expected=(
            ((2, 0), 2),
            ((5, 0), 1),
        ),
    ),
    Case(
        name="bathroom surrounded by desks",
        args=(
            [
                ".D.",
                "DBD",
                ".D.",
            ],
        ),
        expected=(
            ((0, 1), 1),
            ((1, 0), 1),
            ((1, 2), 1),
            ((2, 1), 1),
        ),
    ),
]


def expected_distances(grid: Sequence[str]) -> Tuple[Tuple[Tuple[int, int], int], ...]:
    """Return a small-grid oracle result by enumerating every bathroom."""

    desks = []
    bathrooms = []

    for row, values in enumerate(grid):
        for column, value in enumerate(values):
            if value == "D":
                desks.append((row, column))
            elif value == "B":
                bathrooms.append((row, column))

    expected = []
    for desk_row, desk_column in desks:
        if not bathrooms:
            expected.append(((desk_row, desk_column), -1))
            continue

        nearest_distance = None
        for bathroom_row, bathroom_column in bathrooms:
            row_distance = abs(desk_row - bathroom_row)
            column_distance = abs(desk_column - bathroom_column)
            distance = row_distance + column_distance

            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance

        expected.append(((desk_row, desk_column), nearest_distance))

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
                row = ""
                for _ in range(columns):
                    row += random_generator.choice("BD...")
                grid.append(row)

        yield Case(
            name=f"random seed {seed}",
            args=(grid,),
            expected=expected_distances(grid),
        )
