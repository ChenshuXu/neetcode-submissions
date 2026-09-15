"""Check the interview-style printed examples without changing solution.py."""
import ast
import contextlib
import io
from pathlib import Path
import runpy


if __name__ == "__main__":
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        runpy.run_path(str(Path(__file__).with_name("solution.py")), run_name="__main__")
    actual = [ast.literal_eval(line) for line in output.getvalue().splitlines()]
    expected = [
        0, (0, []), 70, 70, 0, 20, 0, 50, 50, 70, 0, 2,
        (2, [(20, 40)]), (2, [(30, 40)]), (0, []), 4, 0,
        (1, [(0, 10), (20, 30), (1430, 1440)]),
    ]
    assert actual == expected, (actual, expected)
    print("All 18 printed results matched.")
