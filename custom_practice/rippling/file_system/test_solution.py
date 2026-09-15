"""Verify the printed examples while keeping solution.py interview-style."""
import contextlib
import io
from pathlib import Path
import runpy


if __name__ == "__main__":
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        runpy.run_path(str(Path(__file__).with_name("solution.py")), run_name="__main__")
    expected = [
        "[]", "['a']", "hello", "hello world", "['d']", "['a', 'm', 'z']", "",
        "['d']", "['/a/b/c/d', '/other/d', '/other/d/d']", "['/other/d/d']", "[]",
        "['a', 'other', 'z']", "[]", "['/other/d', '/other/d/d']", "[]",
        "deep file", "True", "[]",
    ]
    actual = output.getvalue().splitlines()
    assert actual == expected, (actual, expected)
    print("All 18 printed results matched.")
