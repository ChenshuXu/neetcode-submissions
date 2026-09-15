# Rippling Q001 — Expense Rule Engine

Python custom practice · implemented solution · visible tests.

练习顺序：读 Stage 1 → 在 `solution.py` 自己设计并实现 → 跑 stage1 → 再加 Stage 2、3。
这是 Financial Product R1 的准备题，不代表已确认会考这题。规则建模、可扩展性、正确性和自测是练习重点。

## Evidence boundary

依据现有 [Q001 prep](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-prep-2026-09-15.md>) 与 [evidence ledger](</Users/Newton/Documents/job search/projects/context/Interview/rippling/rippling-financial-product-interview-evidence-2026-09-15.md>)：

- S-W1-036 的评论提供 Corporate Credit Card 完整变体：六条规则、字符串 maps、候选人选择返回类型，以及未来通过 API 创建规则。
- 本轮按 Newton 要求简化：金额与上限使用整数美元，其他字段仍为字符串；不练习金额字符串解析或小数处理。
- S-W3-008 明确要求新增 Rule 实现即可扩展，不修改核心执行逻辑。
- 本练习自行确定：阶段顺序、Python 接口、配置 schema、返回顺序、聚合违规归属、meal 编码和输入合法性保证。它们是可执行的训练约定，不是原帖逐字题干。
- And/Or、Add/Multiply、DSL 仅在另一来源的候选人方案讨论中出现，不作为这道练习的强制要求。

## Stage 1 — Individual expense policies

Build a corporate credit-card rules engine. Given rules and expenses, return every
expense and the IDs of all rules it violates. Companies must be able to introduce
new rule implementations without changing the core evaluator.

Implement these four policies:

| Rule ID | Policy |
| --- | --- |
| restaurant_75 | An expense with vendor_type = restaurant cannot exceed USD 75. |
| no_airfare | Expenses with expense_type = airfare are prohibited. |
| no_entertainment | Expenses with expense_type = entertainment are prohibited. |
| single_250 | No individual expense can exceed USD 250. |

Input expenses are dictionaries: amounts are integer dollars; other fields are strings:

```python
expenses = [
    {"expense_id": "e1", "trip_id": "t1", "amount_usd": 75,
     "expense_type": "meal", "vendor_type": "restaurant", "vendor_name": "Cafe"},
    {"expense_id": "e2", "trip_id": "t1", "amount_usd": 300,
     "expense_type": "airfare", "vendor_type": "airline", "vendor_name": "AirCo"},
]
# With the four rules in the table's order:
# {"e1": [], "e2": ["no_airfare", "single_250"]}
```

### Candidate API

```python
build_rule(spec: dict) -> rule_object
evaluate_rules(rules: list, expenses: list[dict]) -> dict[str, list[str]]
```

You choose the classes and internal data model. For the harness, each rule object
exposes `rule_id: str` and `evaluate(expenses) -> list[str]`, returning unique IDs of
violating expenses in that batch. The evaluator must also accept a test-provided
rule with that interface; it is not created by `build_rule`.

The factory constructs these configuration types in Stage 1:

```python
{"rule_id": "no_airfare", "kind": "ban", "field": "expense_type", "value": "airfare"}
{"rule_id": "single_250", "kind": "max_amount", "limit_usd": 250}
{"rule_id": "restaurant_75", "kind": "max_amount", "limit_usd": 75,
 "field": "vendor_type", "value": "restaurant"}
```

### Fixed practice contract

- All expense fields shown above exist. Expense IDs and rule IDs are unique within each call.
- Amounts and limits are nonnegative integer dollars. No refunds, currency conversion, or malformed expense data in this exercise.
- Compare and sum money exactly. An amount equal to its limit passes; strictly greater fails.
- Matching is exact and case-sensitive. Filter fields are expense_type, vendor_type, or vendor_name.
- A ban rejects every matching expense, including a zero-dollar expense.
- Amount rules optionally filter by one field/value pair. Without a filter they apply to every expense.
- Return every expense ID, including compliant expenses with an empty list. Violation IDs follow input rule order. Dictionary key order is not graded.
- Evaluate every rule independently; do not stop at the first violation.
- Do not mutate expenses or configurations. Rule objects may be reused across batches; one call must not affect another.
- Empty expenses return `{}`; empty rules produce an empty violation list for each expense.
- Each call contains the complete relevant batch. No database, network, or cross-call trip accumulation is required.

## Stage 2 — Trip aggregation

Add two policies while keeping all Stage 1 behavior working:

| Rule ID | Policy |
| --- | --- |
| trip_2000 | The sum of all expenses within a trip cannot exceed USD 2000. |
| meals_200 | The sum of meal expenses within a trip cannot exceed USD 200. |

```python
{"rule_id": "trip_2000", "kind": "trip_total", "limit_usd": 2000}
{"rule_id": "meals_200", "kind": "trip_total", "limit_usd": 200,
 "field": "expense_type", "value": "meal"}
```

For this practice, meals mean `expense_type == "meal"`, independently of vendor type.
Group by trip_id, even when expenses for different trips are interleaved.
A trip_total filter restricts both the summed expenses and the reported violations.
If a group exceeds its cap, report that rule on **every matching expense in that trip**,
including earlier and zero-dollar expenses. Do not report only the expense that crosses
the limit. An expense that fails another rule still contributes its full amount.

Example: t1 has meal e1 = 100, lodging e2 = 999, meal e3 = 101.
With only meals_200, return `{"e1": ["meals_200"], "e2": [], "e3": ["meals_200"]}`.

## Stage 3 — Create rules from configuration

Implement `build_rule` to create ban, max_amount and trip_total rules from the
configuration dictionaries above. No HTTP server is required.

Before coding, verbally confirm that inputs are valid: required keys exist,
rule IDs are nonempty and unique, rule kinds and filter fields are supported,
optional field/value appear together, and amounts and limits are nonnegative integer
dollars. No runtime input checks are needed.

New rule types may require a factory change, but must not require changing
`evaluate_rules`. New configurations of existing types require no code change.

## Run

From the neetcode-submissions repository root:

```bash
python3 custom_practice/rippling/expense_rule_engine/run_tests.py --list
python3 custom_practice/rippling/expense_rule_engine/run_tests.py --case stage1
python3 custom_practice/rippling/expense_rule_engine/run_tests.py --case stage2
python3 custom_practice/rippling/expense_rule_engine/run_tests.py --case stage3
python3 custom_practice/rippling/expense_rule_engine/run_tests.py
```

You can also run `python3 run_tests.py --case stage1` from this folder. Test names,
inputs and expected results are visible in [test_cases.py](test_cases.py).
The implementation covers all three stages. Run all visible cases to check it.

## Finish the practice

- Explain the rule interface and the chosen output before coding.
- Write one normal and one boundary example of your own.
- Keep earlier stages passing when you add a requirement.
- State time and space complexity in terms of expenses, rules and returned violations.
- Explain what changes when a new rule type arrives.

Optional discussion after the tested stages: how would a very large batch change your
design; how would you return one trip-level violation instead of one per expense;
what contract would incremental expense updates require? These are local practice
extensions, not confirmed additional interview questions. The solution is implemented in solution.py.
