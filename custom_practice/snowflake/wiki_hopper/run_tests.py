from collections.abc import Mapping, Sequence
from pathlib import Path
import sys


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import find_shortest_path  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def run_candidate(
    graph: Mapping[str, Sequence[str]],
    start_page: str,
    target_page: str,
) -> list[str]:
    def get_linked_pages(page: str) -> Sequence[str]:
        return graph.get(page, ())

    return find_shortest_path(start_page, target_page, get_linked_pages)


def show_input(case: Case) -> str:
    graph, start_page, target_page = case.args
    return (
        f"graph={graph!r}\n"
        f"start_page={start_page!r}\n"
        f"target_page={target_page!r}"
    )


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
        )
    )
