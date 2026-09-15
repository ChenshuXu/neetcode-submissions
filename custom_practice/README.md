# Custom Coding Practice

Local interview exercises use Python's standard library. Each exercise README owns its
contract, practice assumptions, and follow-ups. Read it before changing code or tests.

## Find an exercise

| Area | Entry point |
| --- | --- |
| Lyft Stateful fetch_n | [Q004 practice](lyft/fetch_n/README.md) |
| Rippling Task Scheduler | [Q058 practice](rippling/task_scheduler/README.md) |
| Rippling File System | [Q003 practice](rippling/file_system/README.md) |
| Rippling Delivery Payment | [Q048 practice](rippling/delivery_payment/README.md) |
| Rippling Food Delivery OOD | [Q010 practice](rippling/food_delivery_ood/README.md) |
| Rippling Expense Rule Engine | [Q001 practice](rippling/expense_rule_engine/README.md) |
| Snowflake | [Company index](snowflake/README.md) |
| Stripe | [Company index](stripe/README.md) and [OA map](stripe/oa_question_map/README.md) |
| Microsoft | [Question bank](microsoft_screen_custom_bank/README.md) |
| DoorDash Dasher Pay | [Kata](doordash_codecraft/kata_01_dasher_pay/README.md) |
| DoorDash Bootstrap | [Kata](doordash_codecraft/kata_02_bootstrap/README.md) |
| DoorDash Validate Cart | [Kata](doordash_codecraft/kata_03_validate_cart/README.md) |

Company exercises live under `custom_practice/<company>/`. Extensions live inside the
base problem's `follow_ups/`; related problems with different contracts live in `variants/`.
The existing Microsoft and DoorDash folders retain their names.

## Run an existing exercise

From the repository root, use the target exercise's runner, for example:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py --list
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py --case middle
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py
```

Runners using [runner.py](runner.py) support `--list` and case-insensitive `--case`
substring filtering. They print inputs, expected/actual values, and a summary, and exit
nonzero on failure. `--list` checks discovery without executing the candidate.
These scripts also work from their exercise directory or VS Code's **Run Python File**.

Some exercises use different entry points. The Microsoft bank takes a problem name:

```bash
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py --list-problems
python3 custom_practice/microsoft_screen_custom_bank/run_tests.py tagged_sequence_assembly
```

DoorDash katas use standalone Python files with inline checks; run the selected file:

```bash
python3 custom_practice/doordash_codecraft/kata_01_dasher_pay/dasher_pay.py
```

Use each kata README for its base and follow-up requirements. There is no DoorDash Go
module in this checkout.

Intentional `NotImplementedError` starters fail until implemented. Check the current file
rather than relying on an old completion summary. Passing visible tests verifies those
cases; it does not measure unaided interview readiness.

## Create an exercise

Follow the [template instructions](_template/README.md); keep the candidate blank when
creating a practice starter. Put visible contract cases in `test_cases.py` and any tree,
graph, or operation-replay adapter in the exercise's `run_tests.py`.

The shared runner deep-copies case arguments before each call so in-place solutions cannot
pollute later cases. Reuse it for new function-style packs. DoorDash's standalone snapshots
keep their existing inline checks.
