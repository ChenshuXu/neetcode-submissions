from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli  # noqa: E402
from solution import reconcile_payments  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(run_cli(reconcile_payments, TEST_CASES))
