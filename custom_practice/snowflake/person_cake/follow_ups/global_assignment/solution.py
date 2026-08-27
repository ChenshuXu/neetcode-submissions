from typing import List, Sequence


UNREACHABLE = float("inf")


def min_total_assignment_distance(
    people: Sequence[int],
    cakes: Sequence[int],
) -> int:
    """Return the smallest total distance of a one-to-one person/cake assignment.

    `people` and `cakes` are positions on a line, in any order, possibly with
    repeats. Every person must receive exactly one cake, and every cake feeds at
    most one person. The cost of one pair is the difference of its positions,
    and the answer is the smallest achievable sum over all valid assignments.
    Return -1 when there are more people than cakes.
    """
    if not people:
        return 0
    if len(people) > len(cakes):
        return -1

    sorted_people = sorted(people)
    sorted_cakes = sorted(cakes)

    # best[matched] = smallest total distance after feeding the first `matched`
    # people using only the cakes considered so far.
    best: List[float] = [0.0] + [UNREACHABLE] * len(sorted_people)

    for cake in sorted_cakes:
        # Skipping this cake keeps every previous total unchanged; the loop
        # below overwrites an entry only when using this cake is cheaper.
        updated = list(best)
        for matched in range(1, len(sorted_people) + 1):
            if best[matched - 1] == UNREACHABLE:
                continue

            candidate = best[matched - 1] + abs(sorted_people[matched - 1] - cake)
            if candidate < updated[matched]:
                updated[matched] = candidate

        best = updated

    total = best[len(sorted_people)]
    return -1 if total == UNREACHABLE else int(total)
