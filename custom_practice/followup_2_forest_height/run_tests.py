from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.ordered_nary_tree_deletion.models import (  # noqa: E402
    ForestSpec,
    build_tree,
    format_forest,
)
from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import max_forest_depth  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def run_candidate(forest_spec: ForestSpec) -> int:
    roots = []
    for root_spec in forest_spec:
        root = build_tree(root_spec)
        if root is not None:
            roots.append(root)
    return max_forest_depth(roots)


def show_input(case: Case) -> str:
    (forest_spec,) = case.args
    return f"roots={format_forest(forest_spec)}"


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
        )
    )
