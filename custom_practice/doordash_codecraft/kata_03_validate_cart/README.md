# Kata 3 — Inventory / Validate Cart

This optional 30-minute mini-kata practices business-rule validation and the
boundary between a read-only inventory snapshot and a real inventory
reservation. It is lower-frequency than the Dasher Pay and Bootstrap task
families and should not replace either primary cold rep.

The canonical template is intentionally unsolved. Work in a fresh attempt:

```bash
cd "/Users/Newton/Documents/job search/neetcode-submissions/custom_practice/doordash_codecraft"
python3 new_attempt.py validate-cart cold-validate-cart-01
cd attempts/cold-validate-cart-01
python3 run_tests.py
```

## Files

- `COLD_PROMPT.md`: candidate-visible contract and example.
- `validate_cart.py`: models plus the intentional `NotImplementedError`.
- `test_validate_cart.py`: nine visible rule and ordering tests.
- `run_tests.py`: runs only candidate-visible tests.
- `INTERVIEWER_PACKET.md`: clarification answers and three follow-up cards.
- `interviewer_checks.py`: held-back checks to run only after time is called.

## Training target

- By minute 5: confirm duplicate semantics, all-errors versus fail-fast, stable
  ordering, and whether validation mutates inventory.
- By minute 15: happy path plus quantity, duplicate, and lookup rules run.
- By minute 23: min/max/inventory rules and stable error order run.
- By minute 27: add one candidate-written adversarial test.
- By minute 30: state complexity and take one reservation/concurrency
  follow-up without pretending snapshot validation prevents overselling.

After the clock, run:

```bash
python3 -m unittest -v interviewer_checks.py
```

Reference implementations may be used temporarily for harness verification,
but must not be retained in this starter or in generated attempts.
