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
from solution import schedule_tasks  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def show_input(case: Case) -> str:
    durations, dependencies, worker_count = case.args
    return (
        f"durations={durations!r}\n"
        f"dependencies={dependencies!r}\n"
        f"worker_count={worker_count!r}"
    )


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            schedule_tasks,
            TEST_CASES,
            format_input=show_input,
        )
    )

