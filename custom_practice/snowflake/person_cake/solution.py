from typing import Optional, Sequence


EMPTY = 0
PERSON = 1
CAKE = 2


def min_person_cake_distance(cells: Sequence[int]) -> int:
    """Return the smallest distance between any person and any cake.

    The one-dimensional row contains only:
    - 0 for an empty position
    - 1 for a person
    - 2 for a cake

    Distance between two positions is the difference of their indices. Return
    -1 when the row holds no person or no cake.
    """
    best: Optional[int] = None
    last_person: Optional[int] = None
    last_cake: Optional[int] = None

    for index, cell in enumerate(cells):
        if cell == PERSON:
            last_person = index
            if last_cake is not None:
                distance = index - last_cake
                if best is None or distance < best:
                    best = distance
        elif cell == CAKE:
            last_cake = index
            if last_person is not None:
                distance = index - last_person
                if best is None or distance < best:
                    best = distance

    return -1 if best is None else best
