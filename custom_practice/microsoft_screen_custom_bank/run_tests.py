from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Callable, Sequence, Tuple


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli  # noqa: E402
import solution  # noqa: E402
from test_cases import RAISES_VALUE_ERROR, TEST_CASES  # noqa: E402


def capture_value_error(candidate: Callable[..., Any]) -> Callable[..., Any]:
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return candidate(*args, **kwargs)
        except ValueError:
            return RAISES_VALUE_ERROR

    return wrapped


def run_user_movie_operations(
    operations: Sequence[Tuple[str, ...]],
) -> Tuple[Tuple[str, ...], ...]:
    index = solution.UserMovieIndex()
    outputs = []

    for operation in operations:
        name = operation[0]
        if name == "add":
            _, user_id, movie_id = operation
            index.add(user_id, movie_id)
        elif name == "movies_for_user":
            _, user_id = operation
            outputs.append(tuple(index.movies_for_user(user_id)))
        elif name == "users_for_movie":
            _, movie_id = operation
            outputs.append(tuple(index.users_for_movie(movie_id)))
        else:
            raise ValueError(f"unsupported operation: {name}")

    return tuple(outputs)


PROBLEMS = {
    "tagged_sequence_assembly": capture_value_error(solution.assemble_tagged_sequences),
    "bidirectional_movie_index": run_user_movie_operations,
    "extensible_calculator": capture_value_error(solution.evaluate_expression),
    "find_work_schedules": capture_value_error(solution.find_work_schedules),
    "shortest_weighted_string": capture_value_error(solution.shortest_weighted_string),
    "two_minimum_values": capture_value_error(solution.two_minimum_values),
    "distinct_nonempty_subsequences": solution.distinct_nonempty_subsequences,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run one Microsoft screen custom drill.",
        allow_abbrev=False,
    )
    parser.add_argument("problem", nargs="?", choices=sorted(PROBLEMS))
    parser.add_argument("--list-problems", action="store_true")
    known, remaining = parser.parse_known_args()

    if known.list_problems:
        for name in sorted(PROBLEMS):
            print(name)
        return 0
    if known.problem is None:
        parser.error("choose a problem or use --list-problems")

    return run_cli(PROBLEMS[known.problem], TEST_CASES[known.problem], argv=remaining)


if __name__ == "__main__":
    raise SystemExit(main())
