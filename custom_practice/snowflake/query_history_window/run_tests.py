from collections import defaultdict
from pathlib import Path
import random
import sys


REPOSITORY_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli  # noqa: E402
from solution import (  # noqa: E402
    WINDOW_SECONDS,
    QueryRecord,
    WindowSummary,
    find_peak_query_windows,
)
from test_cases import TEST_CASES  # noqa: E402


def brute_force(
    queries: tuple[QueryRecord, ...],
) -> list[WindowSummary]:
    records_by_warehouse = defaultdict(list)
    for record in queries:
        records_by_warehouse[record.warehouse_id].append(record)

    result = []
    for warehouse_id in sorted(records_by_warehouse):
        records = records_by_warehouse[warehouse_id]
        candidate_starts = set()
        for record in records:
            candidate_starts.add(record.start_time)

        best_summary = None
        for window_start in sorted(candidate_starts):
            window_end = window_start + WINDOW_SECONDS
            total_credits = 0
            credits_by_user = defaultdict(int)

            for record in records:
                if window_start <= record.start_time < window_end:
                    total_credits += record.credits_used
                    credits_by_user[record.user_id] += record.credits_used

            top_user_id = min(
                credits_by_user,
                key=lambda user_id: (-credits_by_user[user_id], user_id),
            )
            summary = WindowSummary(
                warehouse_id=warehouse_id,
                window_start=window_start,
                window_end=window_end,
                total_credits=total_credits,
                top_user_id=top_user_id,
                top_user_credits=credits_by_user[top_user_id],
            )

            if best_summary is None:
                best_summary = summary
            elif summary.total_credits > best_summary.total_credits:
                best_summary = summary

        result.append(best_summary)

    return result


def run_randomized_differential() -> bool:
    seed_count = 500
    random_source = random.Random(20260825)

    for seed in range(seed_count):
        query_count = random_source.randint(0, 24)
        queries = []

        for index in range(query_count):
            warehouse_number = random_source.randint(1, 3)
            user_number = random_source.randint(1, 4)
            start_time = random_source.randint(0, 4000)
            duration = random_source.randint(1, 3600)
            credits_used = random_source.randint(1, 20)

            record = QueryRecord(
                query_id=f"seed-{seed}-query-{index}",
                warehouse_id=f"wh-{warehouse_number}",
                user_id=f"user-{user_number}",
                start_time=start_time,
                end_time=start_time + duration,
                credits_used=credits_used,
            )
            queries.append(record)

        random_source.shuffle(queries)
        query_tuple = tuple(queries)
        expected = brute_force(query_tuple)
        actual = find_peak_query_windows(query_tuple)

        if actual != expected:
            print(f"Randomized differential seed {seed}: FAIL")
            print(f"Queries: {query_tuple!r}")
            print(f"Expected: {expected!r}")
            print(f"Actual: {actual!r}")
            return False

    print(f"Randomized differential: {seed_count} seeds passed")
    return True


if __name__ == "__main__":
    exit_code = run_cli(find_peak_query_windows, TEST_CASES)

    running_selected_case = "--case" in sys.argv
    listing_cases = "--list" in sys.argv
    if exit_code == 0 and not running_selected_case and not listing_cases:
        if not run_randomized_differential():
            exit_code = 1

    raise SystemExit(exit_code)
