from pathlib import Path
import sys
from typing import Sequence, Tuple


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli  # noqa: E402
from solution import CardValidator  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def run_candidate(operations: Sequence[Tuple[str, str]]) -> tuple:
    validator = CardValidator()
    output = []
    for operation, value in operations:
        if operation == "classify":
            output.append(validator.classify(value))
        elif operation == "count_redacted":
            output.append(validator.count_redacted(value))
        elif operation == "repair_one_digit":
            output.append(tuple(validator.repair_one_digit(value)))
        else:
            raise ValueError(f"unknown operation: {operation}")
    return tuple(output)


if __name__ == "__main__":
    raise SystemExit(run_cli(run_candidate, TEST_CASES))
