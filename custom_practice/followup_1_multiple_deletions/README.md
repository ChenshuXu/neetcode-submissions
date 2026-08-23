# Follow-up 1 — Multiple Ordered N-ary Deletions

Generalize the base problem from one `target` to `to_delete: List[int]`.

- Apply all deletions as one set.
- A deleted node promotes its processed children.
- Parent and child nodes may both be deleted.
- Preserve the exact left-to-right order.
- Return the resulting forest as `List[Node]`.

Implement `delete_nodes` in `solution.py`, then run:

```bash
python3 custom_practice/followup_1_multiple_deletions/run_tests.py
```

The visible cases are in `test_cases.py`. Use `t(value, *children)` to add another tree.
