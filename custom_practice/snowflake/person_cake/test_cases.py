import random
from typing import Iterator, Optional, Sequence

from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="empty row",
        args=([],),
        expected=-1,
    ),
    Case(
        name="no person",
        args=([0, 2, 0, 2],),
        expected=-1,
    ),
    Case(
        name="no cake",
        args=([1, 0, 1, 0],),
        expected=-1,
    ),
    Case(
        name="all empty",
        args=([0, 0, 0],),
        expected=-1,
    ),
    Case(
        name="single person",
        args=([1],),
        expected=-1,
    ),
    Case(
        name="adjacent person then cake",
        args=([1, 2],),
        expected=1,
    ),
    Case(
        name="adjacent cake then person",
        args=([2, 1],),
        expected=1,
    ),
    Case(
        name="cake before person with a gap",
        args=([2, 0, 0, 1],),
        expected=3,
    ),
    Case(
        name="two cakes tie around one person",
        args=([2, 0, 1, 0, 2],),
        expected=2,
    ),
    Case(
        name="best pair is not the first pair",
        args=([1, 0, 0, 0, 2, 0, 1, 2],),
        expected=1,
    ),
    Case(
        name="nearest cake is behind the person",
        args=([0, 2, 0, 1, 0, 0, 0, 2],),
        expected=2,
    ),
    Case(
        name="block of people then block of cakes",
        args=([1, 1, 1, 0, 2, 2],),
        expected=2,
    ),
    Case(
        name="alternating row",
        args=([1, 2, 1, 2, 1, 2],),
        expected=1,
    ),
    Case(
        name="best pair sits at the end of a long row",
        args=([1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],),
        expected=1,
    ),
    Case(
        name="many people share one cake",
        args=([1, 1, 0, 0, 2, 0, 0, 1, 1],),
        expected=3,
    ),
]


def expected_min_distance(cells: Sequence[int]) -> int:
    """Return a small-row oracle result by enumerating every person/cake pair."""

    people = [index for index, cell in enumerate(cells) if cell == 1]
    cakes = [index for index, cell in enumerate(cells) if cell == 2]

    best: Optional[int] = None
    for person in people:
        for cake in cakes:
            distance = abs(person - cake)
            if best is None or distance < best:
                best = distance

    return -1 if best is None else best


def randomized_test_cases(seed_count: int = 1000) -> Iterator[Case]:
    """Yield reproducible small rows for differential testing."""

    for seed in range(seed_count):
        random_generator = random.Random(seed)
        length = random_generator.randint(0, 12)
        cells = [random_generator.choice([0, 0, 1, 2]) for _ in range(length)]

        yield Case(
            name=f"random seed {seed}",
            args=(cells,),
            expected=expected_min_distance(cells),
        )
