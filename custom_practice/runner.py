from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass, field
from pprint import pformat
from typing import Any, Callable, Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Case:
    """One visible test case for a function-style interview problem."""

    name: str
    expected: Any
    args: Tuple[Any, ...] = ()
    kwargs: dict = field(default_factory=dict)


def _default_input(case: Case) -> str:
    parts = []
    if case.args:
        parts.append("args=" + pformat(case.args, width=88, sort_dicts=False))
    if case.kwargs:
        parts.append("kwargs=" + pformat(case.kwargs, width=88, sort_dicts=False))
    return "\n".join(parts) if parts else "(no arguments)"


def _default_value(value: Any) -> str:
    return pformat(value, width=88, sort_dicts=False)


def run_cli(
    candidate: Callable[..., Any],
    cases: Iterable[Case],
    *,
    format_input: Optional[Callable[[Case], str]] = None,
    format_value: Optional[Callable[[Any], str]] = None,
    argv: Optional[Sequence[str]] = None,
) -> int:
    """Run visible cases and print LeetCode-like input/expected/actual output."""

    parser = argparse.ArgumentParser(description="Run visible custom-practice cases.")
    parser.add_argument(
        "--case",
        help="Run only cases whose names contain this text (case-insensitive).",
    )
    parser.add_argument("--list", action="store_true", help="List case names and exit.")
    options = parser.parse_args(argv)

    all_cases: List[Case] = list(cases)
    if options.list:
        for index, case in enumerate(all_cases, start=1):
            print(f"{index}. {case.name}")
        return 0

    selected = all_cases
    if options.case:
        needle = options.case.lower()
        selected = [case for case in all_cases if needle in case.name.lower()]
        if not selected:
            parser.error(f"no case name contains {options.case!r}")

    show_input = format_input or _default_input
    show_value = format_value or _default_value
    passed = 0

    print(f"Running {len(selected)} visible case(s)\n")
    for index, case in enumerate(selected, start=1):
        print(f"[{index}/{len(selected)}] {case.name}")
        print(f"  Input:    {show_input(case)}")
        print(f"  Expected: {show_value(case.expected)}")

        error: Optional[Exception] = None
        actual: Any = None
        try:
            actual = candidate(
                *copy.deepcopy(case.args),
                **copy.deepcopy(case.kwargs),
            )
        except Exception as exc:  # Show the failing case instead of hiding it.
            error = exc

        if error is not None:
            print(f"  Actual:   raised {type(error).__name__}: {error}")
            print("  Result:   FAIL\n")
            continue

        print(f"  Actual:   {show_value(actual)}")
        if actual == case.expected:
            passed += 1
            print("  Result:   PASS\n")
        else:
            print("  Result:   FAIL\n")

    failed = len(selected) - passed
    print(f"Summary: {passed} passed, {failed} failed, {len(selected)} total")
    return 0 if failed == 0 else 1
