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
from solution import MultiRuleRateLimiter  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


Rule = tuple[int, int]
Request = tuple[str, int]


def run_candidate(
    rules: Sequence[Rule],
    requests: Sequence[Request],
) -> tuple[bool, ...]:
    limiter = MultiRuleRateLimiter(rules)
    outputs = []

    for key, timestamp in requests:
        outputs.append(limiter.allow(key, timestamp))

    return tuple(outputs)


def show_input(case: Case) -> str:
    rules, requests = case.args
    lines = [f"rules={rules!r}", "requests:"]
    lines.extend(f"    allow{request!r}" for request in requests)
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            run_candidate,
            TEST_CASES,
            format_input=show_input,
        )
    )
