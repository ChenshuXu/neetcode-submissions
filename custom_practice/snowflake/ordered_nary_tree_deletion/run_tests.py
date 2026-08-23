from pathlib import Path
import sys
from typing import Any


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import Case, run_cli  # noqa: E402
from models import (  # noqa: E402
    ForestSpec,
    TreeSpec,
    build_tree,
    forest_to_spec,
    format_forest,
    format_tree,
)
from solution import delete_node  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def run_candidate(root_spec: TreeSpec, target: int) -> ForestSpec:
    root = build_tree(root_spec)
    forest = delete_node(root, target)
    if not isinstance(forest, list):
        raise TypeError("delete_node must return list[Node]")
    return forest_to_spec(forest)


def show_input(case: Case) -> str:
    root_spec, target = case.args
    return f"root={format_tree(root_spec)}, target={target}"


def show_value(value: Any) -> str:
    return format_forest(value)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
            format_value=show_value,
        )
    )
