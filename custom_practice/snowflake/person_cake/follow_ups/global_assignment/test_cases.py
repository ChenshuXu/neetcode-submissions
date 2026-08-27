import itertools
import random
from typing import Iterator, Optional, Sequence

from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="no people",
        args=([], [1, 5]),
        expected=0,
    ),
    Case(
        name="no people and no cakes",
        args=([], []),
        expected=0,
    ),
    Case(
        name="more people than cakes",
        args=([0, 3, 9], [1, 4]),
        expected=-1,
    ),
    Case(
        name="people but no cakes",
        args=([2], []),
        expected=-1,
    ),
    Case(
        name="one person one cake",
        args=([4], [9]),
        expected=5,
    ),
    Case(
        name="person already on a cake",
        args=([4], [4]),
        expected=0,
    ),
    Case(
        name="nearest-first order fails",
        args=([4, 0], [3, 5]),
        expected=4,
    ),
    Case(
        name="two people must not share one cake",
        args=([0, 1], [1, 10]),
        expected=10,
    ),
    Case(
        name="spare cake is left unused",
        args=([0, 10], [1, 5, 11]),
        expected=2,
    ),
    Case(
        name="duplicate positions",
        args=([2, 2, 2], [2, 2, 8]),
        expected=6,
    ),
    Case(
        name="negative positions",
        args=([-5, 0, 5], [-6, 1, 6]),
        expected=3,
    ),
    Case(
        name="crossing assignment is never needed",
        args=([1, 2, 3], [3, 2, 1]),
        expected=0,
    ),
    Case(
        name="unsorted input",
        args=([9, 1, 5], [6, 0, 4]),
        expected=5,
    ),
    Case(
        name="all cakes on one side",
        args=([0, 1, 2], [10, 11, 12]),
        expected=30,
    ),
]


def expected_total_distance(
    people: Sequence[int],
    cakes: Sequence[int],
) -> int:
    """Return a small-input oracle result by enumerating every assignment."""

    if not people:
        return 0
    if len(people) > len(cakes):
        return -1

    best: Optional[int] = None
    for chosen in itertools.permutations(cakes, len(people)):
        total = sum(abs(person - cake) for person, cake in zip(people, chosen))
        if best is None or total < best:
            best = total

    return best if best is not None else -1


def randomized_test_cases(seed_count: int = 400) -> Iterator[Case]:
    """Yield reproducible small position lists for differential testing."""

    for seed in range(seed_count):
        random_generator = random.Random(seed)
        person_count = random_generator.randint(0, 4)
        cake_count = random_generator.randint(0, 5)

        people = [random_generator.randint(-8, 8) for _ in range(person_count)]
        cakes = [random_generator.randint(-8, 8) for _ in range(cake_count)]

        yield Case(
            name=f"random seed {seed}",
            args=(people, cakes),
            expected=expected_total_distance(people, cakes),
        )
