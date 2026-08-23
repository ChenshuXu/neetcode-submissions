# Stripe-style Custom — Join Two Datasets

This runnable exercise reconstructs the four-part Stripe dataset-join family. The public evidence
establishes CSV headers, a named join field, inner/left join behavior, one-to-many matches, numeric
`order` sorting, and a late `skipUnmatched` parameter. The exact Part 4 wording is not public, so this
practice defines `skip_unmatched=True` as inner-join behavior and `False` as left-join behavior.

## Contract

Implement:

```python
def join_data_set(
    field_name: str,
    customer_file: Sequence[str],
    processor_file: Sequence[str],
    skip_unmatched: bool,
) -> List[str]:
    ...
```

- Both files are non-empty and their first row is a comma-separated header.
- Fields contain no escaped commas; headers are unique within each file.
- Both headers contain `field_name` and a numeric `order` column.
- The output header is every customer column followed by every processor column.
- A customer row with `k` processor matches emits `k` rows.
- With `skip_unmatched=False`, an unmatched customer emits one row with empty processor fields.
- With `skip_unmatched=True`, unmatched customers are omitted.
- Sort data rows by numeric customer `order`, then numeric processor `order`; an unmatched processor
  portion sorts after matched rows for the same customer order.
- Preserve source order when all sort keys tie.

## Related LeetCode

[LC 175 — Combine Two Tables](https://leetcode.com/problems/combine-two-tables/) practices the
left-join core, but not CSV parsing, one-to-many expansion, the Boolean mode, or stable numeric sorting.

## Run

```bash
python3 custom_practice/stripe_join_two_datasets/run_tests.py
```

Use `--list` or `--case one-to-many` to select cases.
