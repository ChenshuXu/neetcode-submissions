from pathlib import Path
import sys
from typing import Sequence


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import RepeatedQueryIndex, lower_bound  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def run_candidate(
    values: Sequence[int],
    targets: Sequence[int],
) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    lower_bound_results = []
    for target in targets:
        lower_bound_results.append(lower_bound(values, target))

    index = RepeatedQueryIndex(values)
    query_results = []
    for target in targets:
        query_results.append(index.query(target))

    return tuple(lower_bound_results), tuple(query_results)


def show_input(case: Case) -> str:
    values, targets = case.args
    return f"values={values!r}\ntargets={targets!r}"


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
        )
    )

