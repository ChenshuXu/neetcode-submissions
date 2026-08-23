from pathlib import Path
import sys


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli  # noqa: E402
from solution import delete_from_parent_array  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(run_cli(delete_from_parent_array, TEST_CASES))
