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
from solution import TaskExecutor  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


Operation = Tuple[Any, ...]


def run_candidate(operations: Sequence[Operation]) -> Tuple[Any, ...]:
    executor = TaskExecutor()
    outputs = []

    for operation in operations:
        name = operation[0]
        if name == "add" and len(operation) == 4:
            executor.add_task(operation[1], operation[2], operation[3])
        elif name == "cancel" and len(operation) == 2:
            outputs.append(executor.cancel_task(operation[1]))
        elif name == "execute" and len(operation) == 1:
            outputs.append(executor.execute_task())
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
