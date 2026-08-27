"""Run only the candidate-visible Validate Cart tests."""

from pathlib import Path
import unittest


if __name__ == "__main__":
    package_dir = Path(__file__).resolve().parent
    suite = unittest.defaultTestLoader.discover(
        str(package_dir),
        pattern="test_validate_cart.py",
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
