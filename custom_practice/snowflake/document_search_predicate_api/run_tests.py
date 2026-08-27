from pathlib import Path
import sys
from typing import Any, Sequence, Tuple


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import DocumentStore  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


Operation = Tuple[Any, ...]


def run_candidate(operations: Sequence[Operation]) -> Tuple[Any, ...]:
    store = DocumentStore()
    outputs = []

    for operation in operations:
        name = operation[0]
        if name == "insert" and len(operation) == 3:
            store.insert_doc(operation[1], operation[2])
        elif name == "delete" and len(operation) == 2:
            outputs.append(store.delete_doc(operation[1]))
        elif name == "search" and len(operation) == 2:
            outputs.append(tuple(store.search(operation[1])))
        else:
            raise ValueError(f"invalid operation: {operation!r}")

    return tuple(outputs)


def show_input(case: Case) -> str:
    (operations,) = case.args
    lines = ["operations:"]
    lines.extend(f"    {operation!r}" for operation in operations)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
        )
    )
