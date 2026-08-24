from collections.abc import Callable
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

from custom_practice.runner import run_cli  # noqa: E402
from solution import resolve_all_acls  # noqa: E402
from test_cases import RAISES_VALUE_ERROR, TEST_CASES  # noqa: E402


def capture_value_error(candidate: Callable[..., Any]) -> Callable[..., Any]:
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        try:
            return candidate(*args, **kwargs)
        except ValueError:
            return RAISES_VALUE_ERROR

    return wrapped


if __name__ == "__main__":
    raise SystemExit(
        run_cli(
            capture_value_error(resolve_all_acls),
            TEST_CASES,
        )
    )
