"""Run from the repository root or this directory; supports --list / --case."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runner import run_cli
from solution import BillingSystem
from test_cases import CASES


def replay(operations):
    billing = BillingSystem()
    results = []
    for method, args in operations:
        try:
            result = getattr(billing, method)(*args)
        except (ValueError, KeyError) as error:
            results.append(type(error).__name__)
        else:
            if method == "get_total_cost":
                results.append(result)
    return results


if __name__ == "__main__":
    raise SystemExit(run_cli(replay, CASES))
