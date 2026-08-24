import collections
from typing import Dict, Sequence, Tuple


Position = Tuple[int, int]


def closest_bathroom_distances(grid: Sequence[str]) -> Dict[Position, int]:
    """Return each desk position's distance to its nearest bathroom.

    The grid is rectangular and contains only:
    - "B" for a bathroom
    - "D" for a desk
    - "." for an empty position

    Positions use zero-indexed (row, column) coordinates. If the grid contains
    desks but no bathroom, map every desk to -1. Return an empty dictionary for
    an empty grid or a grid with no desks.
    """
    if not grid:
        return {}
    # bfs with level, start with all bathroom
    # when meet a desk, this is the shortest distance
    result = {} # Position -> int
    bathrooms = []

    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "D":
                result[(r, c)] = -1
            elif grid[r][c] == "B":
                bathrooms.append((r, c))

    step = 0
    queue = collections.deque()
    for pos in bathrooms:
        queue.append(pos)

    visited = set(bathrooms)
    directions = [
        [1,0],[0,1],[-1,0],[0,-1]
    ]
    while queue:
        step += 1
        for _ in range(len(queue)):
            pos = queue.popleft()
            for dr, dc in directions:
                new_r = pos[0] + dr
                new_c = pos[1] + dc

                if not (0 <= new_r < rows and 0 <= new_c < cols):
                    continue
                if (new_r, new_c) in visited:
                    continue

                visited.add((new_r, new_c))
                # this is the desk, save the distance
                if (new_r, new_c) in result:
                    result[(new_r, new_c)] = step
                queue.append((new_r, new_c))

    return result 
