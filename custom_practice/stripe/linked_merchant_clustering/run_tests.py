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
from solution import linked_merchants  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


def show_input(case: Case) -> str:
    lines = []
    for day_number, batch in enumerate(case.args, start=1):
        lines.append(f"day{day_number}=[")
        lines.extend(f"    {record!r}," for record in batch)
        lines.append("]")
    return "\n".join(lines)


def show_output(value: object) -> str:
    if isinstance(value, list):
        return "\n            ".join(repr(line) for line in value)
    return repr(value)


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            linked_merchants,
            TEST_CASES,
            format_input=show_input,
            format_value=show_output,
        )
    )
