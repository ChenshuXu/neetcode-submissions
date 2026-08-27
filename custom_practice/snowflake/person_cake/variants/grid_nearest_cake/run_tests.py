from pathlib import Path
import sys
from typing import Dict, Sequence, Tuple


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import Position, nearest_cake_distances  # noqa: E402
from test_cases import TEST_CASES, randomized_test_cases  # noqa: E402


def run_candidate(
    grid: Sequence[Sequence[int]],
) -> Tuple[Tuple[Position, int], ...]:
    distances: Dict[Position, int] = nearest_cake_distances(grid)
    return tuple(sorted(distances.items()))


def show_input(case: Case) -> str:
    grid = case.args[0]
    if not grid:
        return "grid=[]"

    lines = ["grid=["]
    lines.extend(f"    {list(row)!r}," for row in grid)
    lines.append("]")
    return "\n".join(lines)


def run_randomized_tests(seed_count: int = 1000) -> int:
    for case in randomized_test_cases(seed_count):
        try:
            actual = run_candidate(*case.args)
        except Exception as error:
            print(f"Randomized differential test failed: {case.name}")
            print(show_input(case))
            print(f"Expected: {case.expected!r}")
            print(f"Actual: raised {type(error).__name__}: {error}")
            return 1

        if actual != case.expected:
            print(f"Randomized differential test failed: {case.name}")
            print(show_input(case))
            print(f"Expected: {case.expected!r}")
            print(f"Actual:   {actual!r}")
            return 1

    print(f"Randomized differential test: {seed_count}/{seed_count} passed")
    return 0


if __name__ == "__main__":
    visible_status = run_cli(
        run_candidate,
        TEST_CASES,
        format_input=show_input,
        argv=None,
    )

    if visible_status != 0:
        raise SystemExit(visible_status)

    if "--list" in sys.argv or "--case" in sys.argv:
        raise SystemExit(visible_status)

    raise SystemExit(run_randomized_tests())
