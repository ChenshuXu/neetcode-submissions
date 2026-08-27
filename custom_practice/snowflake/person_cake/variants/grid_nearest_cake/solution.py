import collections
from typing import Dict, Sequence, Tuple


EMPTY = 0
PERSON = 1
CAKE = 2

Position = Tuple[int, int]


def nearest_cake_distances(grid: Sequence[Sequence[int]]) -> Dict[Position, int]:
    """Return each person's distance to the nearest cake on a rectangular grid.

    The grid contains only:
    - 0 for an empty cell
    - 1 for a person
    - 2 for a cake

    A step moves to a vertically or horizontally adjacent cell, and no cell
    blocks movement. Positions use zero-indexed (row, column) coordinates.
    Return one entry per person and no entry for any other cell. A person with
    no cake anywhere on the grid maps to -1. An empty grid, a grid with no
    columns, or a grid with no people returns an empty dictionary.
    """
    if not grid or not grid[0]:
        return {}

    rows = len(grid)
    columns = len(grid[0])

    distances: Dict[Position, int] = {}
    frontier: collections.deque = collections.deque()
    visited = set()

    for row in range(rows):
        for column in range(columns):
            value = grid[row][column]
            if value == PERSON:
                distances[(row, column)] = -1
            elif value == CAKE:
                frontier.append((row, column))
                visited.add((row, column))

    steps = 0
    while frontier:
        steps += 1
        for _ in range(len(frontier)):
            row, column = frontier.popleft()
            for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_delta
                next_column = column + column_delta

                if not (0 <= next_row < rows and 0 <= next_column < columns):
                    continue
                if (next_row, next_column) in visited:
                    continue

                visited.add((next_row, next_column))
                if (next_row, next_column) in distances:
                    distances[(next_row, next_column)] = steps
                frontier.append((next_row, next_column))

    return distances
