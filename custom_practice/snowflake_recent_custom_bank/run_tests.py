from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli  # noqa: E402
import solution  # noqa: E402
from test_cases import TEST_CASES  # noqa: E402


PROBLEMS = {
    "single_query_revenue": solution.maximize_single_query_type,
    "horizontal_pod_autoscaler": solution.final_pod_counts,
    "string_xor": solution.minimum_string_xor,
    "database_configuration": solution.subtree_pairability,
    "string_patterns": solution.count_constrained_strings,
    "acl_inheritance": solution.resolve_acl,
    "distributed_nary_count": solution.count_distributed_nodes,
    "http_retry_backoff": solution.execute_with_retry,
    "result_cache_invalidation": solution.run_result_cache,
    "sql_table_extraction": solution.extract_sql_tables,
    "redundant_parentheses": solution.has_redundant_parentheses,
    "sessionization": solution.sessionize_events,
    "preaggregate_three_tables": solution.summarize_accounts,
    "census_nl2sql": solution.answer_census_question,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one Snowflake recent custom drill.")
    parser.add_argument("problem", nargs="?", choices=sorted(PROBLEMS))
    parser.add_argument("--list-problems", action="store_true")
    known, remaining = parser.parse_known_args()

    if known.list_problems:
        for name in sorted(PROBLEMS):
            print(name)
        return 0
    if known.problem is None:
        parser.error("choose a problem or use --list-problems")

    return run_cli(PROBLEMS[known.problem], TEST_CASES[known.problem], argv=remaining)


if __name__ == "__main__":
    raise SystemExit(main())
