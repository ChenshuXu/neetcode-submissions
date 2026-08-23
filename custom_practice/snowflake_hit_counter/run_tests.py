from pathlib import Path
import sys
from typing import Any, Sequence, Tuple


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import Case, run_cli  # noqa: E402
from solution import HitCounter  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


Operation = Tuple[Any, ...]


def run_candidate(operations: Sequence[Operation]) -> Tuple[int, ...]:
    counter = HitCounter()
    outputs = []

    for operation in operations:
        name = operation[0]
        if name == "hit" and len(operation) == 2:
            counter.hit(operation[1])
        elif name == "getHits" and len(operation) == 2:
            outputs.append(counter.getHits(operation[1]))
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
