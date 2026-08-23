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
from solution import BoundedEventFrequency  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


Operation = Tuple[Any, ...]


def run_candidate(
    window_seconds: int,
    operations: Sequence[Operation],
) -> Tuple[Any, ...]:
    tracker = BoundedEventFrequency(window_seconds)
    outputs = []

    for operation in operations:
        name = operation[0]
        if name == "record" and len(operation) == 3:
            tracker.record(operation[1], operation[2])
        elif name == "most_frequent" and len(operation) == 2:
            outputs.append(tracker.most_frequent(operation[1]))
        else:
            raise ValueError(f"invalid operation: {operation!r}")

    return tuple(outputs)


def show_input(case: Case) -> str:
    window_seconds, operations = case.args
    lines = [f"window_seconds={window_seconds}", "operations:"]
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
