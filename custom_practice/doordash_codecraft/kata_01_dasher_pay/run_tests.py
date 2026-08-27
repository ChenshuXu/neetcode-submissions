"""Run the visible and post-clock Dasher Payout API suites."""

import argparse
import unittest


SUITES = {
    "visible": ("test_dasher_pay",),
    "held-back": ("interviewer_checks",),
    "all": ("test_dasher_pay", "interviewer_checks"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("suite", choices=tuple(SUITES), nargs="?", default="visible")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()

    for module_name in SUITES[args.suite]:
        suite.addTests(loader.loadTestsFromName(module_name))

    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
