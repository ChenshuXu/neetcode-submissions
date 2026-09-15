"""Rippling Q001 — Expense Rule Engine

Description
-----------
Build a corporate credit-card policy checker. Given a list of rules and a
batch of expenses, return the IDs of every rule violated by each expense.
Adding a new rule implementation must not require changing evaluate_rules.

Each expense is a dictionary; amounts are integer dollars and other fields are strings:
    expense_id: unique expense ID
    trip_id: the business trip this expense belongs to
    amount_usd: nonnegative integer USD amount, e.g. 75
    expense_type: expense category, e.g. "meal", "airfare", "lodging"
    vendor_type: merchant category, e.g. "restaurant", "airline", "hotel"
    vendor_name: merchant name

Stage 1: Individual policies
    restaurant_75: restaurant expenses cannot exceed $75 each.
    no_airfare: airfare expenses are prohibited.
    no_entertainment: entertainment expenses are prohibited.
    single_250: no individual expense can exceed $250.

Stage 2: Trip policies
    trip_2000: all expenses in one trip cannot total more than $2000.
    meals_200: expenses with expense_type == "meal" in one trip cannot
               total more than $200.

Stage 3: Create rules from configuration
    build_rule constructs rules from valid configurations.
    Confirm input guarantees verbally before coding; no input validation
    or HTTP server is required.

Interfaces
----------
    build_rule(spec) -> rule object
    evaluate_rules(rules, expenses) -> {expense_id: [violated_rule_id, ...]}

Each rule object exposes rule_id and evaluate(expenses) -> list[str], which
returns unique IDs of violating expenses. Choose your own rule classes.
The examples below create rule objects from configuration dictionaries:
    rules = [build_rule(spec) for spec in specs]
    result = evaluate_rules(rules, expenses)

Practice contract
-----------------
- Confirm verbally: inputs are valid dictionaries; required keys
  exist, rule kinds and filter fields are supported, optional field/value
  appear together, and amounts and limits are nonnegative integer dollars. No runtime input validation is required.
- All expense fields exist; expense IDs and rule IDs are unique per call.
- Amounts and limits are integer dollars. Equality with a limit passes.
- Matching is exact and case-sensitive. Allowed filter fields are
  expense_type, vendor_type and vendor_name.
- ban rejects matching expenses. max_amount checks each matching expense.
  trip_total sums matching expenses separately for each trip_id.
- Amount rules may omit field/value to include all expenses.
- Return every expense ID, including compliant expenses with [].
  List violated rule IDs in input rule order; report all violations.
- An exceeded trip limit marks ALL matching expenses in that trip,
  not just the last expense. Nonmatching expenses are not marked.
- Expenses rejected by another rule still contribute to trip totals.
- Do not mutate inputs or retain batch totals between evaluations.
- Empty expenses return {}; empty rules give [] for every expense.

Example 1 — Individual checks and exact boundary (Stage 1)
--------------------------------------------------------
Input:
    specs = [
        {"rule_id": "restaurant_75", "kind": "max_amount",
         "limit_usd": 75, "field": "vendor_type", "value": "restaurant"},
        {"rule_id": "no_airfare", "kind": "ban",
         "field": "expense_type", "value": "airfare"},
        {"rule_id": "single_250", "kind": "max_amount", "limit_usd": 250},
    ]
    expenses = [
        {"expense_id": "e1", "trip_id": "t1", "amount_usd": 75,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Cafe"},
        {"expense_id": "e2", "trip_id": "t1", "amount_usd": 300,
         "expense_type": "airfare", "vendor_type": "airline", "vendor_name": "AirCo"},
    ]
Output:
    {"e1": [], "e2": ["no_airfare", "single_250"]}
Explanation:
    e1 equals the restaurant cap and passes. e2 violates both the airfare
    ban and the individual cap; it does not match the restaurant filter.

Example 2 — Multiple rules and filtered trip aggregation (Stage 2)
----------------------------------------------------------------
Input:
    specs = [
        {"rule_id": "restaurant_75", "kind": "max_amount",
         "limit_usd": 75, "field": "vendor_type", "value": "restaurant"},
        {"rule_id": "meals_200", "kind": "trip_total",
         "limit_usd": 200, "field": "expense_type", "value": "meal"},
    ]
    expenses = [
        {"expense_id": "e1", "trip_id": "t1", "amount_usd": 120,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Cafe"},
        {"expense_id": "e2", "trip_id": "t1", "amount_usd": 100,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Diner"},
        {"expense_id": "e3", "trip_id": "t1", "amount_usd": 180,
         "expense_type": "lodging", "vendor_type": "hotel", "vendor_name": "Hotel"},
    ]
Output:
    {"e1": ["restaurant_75", "meals_200"],
     "e2": ["restaurant_75", "meals_200"],
     "e3": []}
Explanation:
    Both restaurant expenses exceed $75. Their meal total is $220, so both
    receive meals_200. The hotel expense is excluded from this meal rule.

Example 3 — Empty batch
-----------------------
Input:
    specs = []
    expenses = []
Output:
    {}

These examples, interfaces and output conventions are local practice choices
based on the reported Corporate Credit Card variant, not a verbatim official
prompt. See README.md for source boundaries and the full Stage 3 contract.
Implementation below covers all three stages.
"""


from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rule:
    rule_id: str
    field: str | None = None
    value: str | None = None

    def matches(self, expense):
        # 判断这笔费用是否属于规则的适用范围，不代表它已经违规。
        # 没有指定过滤字段时，规则适用于所有费用。
        if self.field is None:
            return True

        # 例如 field="vendor_type", value="restaurant"，只匹配餐厅费用。
        if expense[self.field] == self.value:
            return True

        # 字段值不匹配，这条规则不适用于该费用。
        return False

    def evaluate(self, expenses):
        raise NotImplementedError("Each rule type implements its own evaluation")


class BanRule(Rule):
    def evaluate(self, expenses):
        violations = []
        for expense in expenses:
            if self.matches(expense):
                violations.append(expense["expense_id"])
        return violations


@dataclass
class MaxAmountRule(Rule):
    limit_usd: int = 0

    def evaluate(self, expenses):
        violations = []
        for expense in expenses:
            if self.matches(expense):
                amount = expense["amount_usd"]
                if amount > self.limit_usd:
                    violations.append(expense["expense_id"])
        return violations


@dataclass
class TripTotalRule(Rule):
    limit_usd: int = 0

    def evaluate(self, expenses):
        # Totals belong to this batch, so reusing the rule cannot leak state.
        totals = {}
        for expense in expenses:
            if self.matches(expense):
                trip_id = expense["trip_id"]
                amount = expense["amount_usd"]
                totals[trip_id] = totals.get(trip_id, 0) + amount

        # Report every matching expense after the complete trip total is known.
        violations = []
        for expense in expenses:
            if self.matches(expense):
                if totals[expense["trip_id"]] > self.limit_usd:
                    violations.append(expense["expense_id"])
        return violations


def build_rule(spec: dict):
    """Create a rule from a valid configuration, as confirmed with the interviewer."""
    rule_id = spec["rule_id"]
    kind = spec["kind"]
    field = spec.get("field")
    value = spec.get("value")

    if kind == "ban":
        return BanRule(rule_id, field, value)

    limit_usd = spec["limit_usd"]
    if kind == "max_amount":
        return MaxAmountRule(rule_id, field, value, limit_usd)
    return TripTotalRule(rule_id, field, value, limit_usd)


def evaluate_rules(rules: list, expenses: list[dict]) -> dict[str, list[str]]:
    """Collect all violations in rule order without knowing concrete rule types.

    For R built-in rules, E expenses and V returned violations:
    time O(R * E + E + V), space O(E + V), assuming bounded-length amounts.
    """
    result = {}
    for expense in expenses:
        result[expense["expense_id"]] = []

    for rule in rules:
        for expense_id in rule.evaluate(expenses):
            result[expense_id].append(rule.rule_id)
    return result


if __name__ == "__main__":
    # 1. Exact limit passes; report every violated rule in rule order.
    rules = [
        build_rule({"rule_id": "restaurant_75", "kind": "max_amount",
                    "limit_usd": 75, "field": "vendor_type", "value": "restaurant"}),
        build_rule({"rule_id": "no_airfare", "kind": "ban",
                    "field": "expense_type", "value": "airfare"}),
        build_rule({"rule_id": "single_250", "kind": "max_amount", "limit_usd": 250}),
    ]
    expenses = [
        {"expense_id": "e1", "trip_id": "t1", "amount_usd": 75,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Cafe"},
        {"expense_id": "e2", "trip_id": "t1", "amount_usd": 76,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Diner"},
        {"expense_id": "e3", "trip_id": "t1", "amount_usd": 300,
         "expense_type": "airfare", "vendor_type": "airline", "vendor_name": "AirCo"},
    ]
    print(evaluate_rules(rules, expenses))
    # {'e1': [], 'e2': ['restaurant_75'], 'e3': ['no_airfare', 'single_250']}

    # 2. Empty inputs.
    print(evaluate_rules(rules, []))  # {}
    print(evaluate_rules([], expenses))  # {'e1': [], 'e2': [], 'e3': []}

    # 3. Attribute a meal-total violation to both meals, not the hotel or another trip.
    meal_rule = build_rule({"rule_id": "meals_200", "kind": "trip_total",
                            "limit_usd": 200, "field": "expense_type", "value": "meal"})
    trip_expenses = [
        {"expense_id": "m1", "trip_id": "t1", "amount_usd": 120,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Cafe"},
        {"expense_id": "m2", "trip_id": "t2", "amount_usd": 200,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Diner"},
        {"expense_id": "h1", "trip_id": "t1", "amount_usd": 500,
         "expense_type": "lodging", "vendor_type": "hotel", "vendor_name": "Hotel"},
        {"expense_id": "m3", "trip_id": "t1", "amount_usd": 100,
         "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Cafe"},
    ]
    print(evaluate_rules([meal_rule], trip_expenses))
    # {'m1': ['meals_200'], 'm2': [], 'h1': [], 'm3': ['meals_200']}

    # 4. Reuse the same rule with a new batch; previous totals must not carry over.
    print(evaluate_rules([meal_rule], trip_expenses[:1]))  # {'m1': []}
