from copy import deepcopy
from pathlib import Path
import sys

REPOSITORY_ROOT = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "custom_practice" / "__init__.py").is_file()
)
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from custom_practice.runner import run_cli
from solution import build_rule, evaluate_rules
from test_cases import TEST_CASES


class SelectedExpensesRule:
    """Test-only extension: a rule unknown to the candidate's factory."""
    rule_id = "external_review"

    def evaluate(self, expenses):
        return [e["expense_id"] for e in expenses if e["vendor_name"] == "ReviewCo"]


def run_case(specs, expenses, extension=False, repeat=False):
    before = deepcopy((specs, expenses))
    rules = [build_rule(spec) for spec in specs]
    if extension:
        rules.append(SelectedExpensesRule())
    actual = evaluate_rules(rules, expenses)
    if repeat:
        assert evaluate_rules(rules, []) == {}, "Rule state leaked into an empty batch"
        assert evaluate_rules(rules, expenses) == actual, "Rule state leaked between calls"
    assert (specs, expenses) == before, "Input was mutated"
    return actual


if __name__ == "__main__":
    raise SystemExit(run_cli(run_case, TEST_CASES))
