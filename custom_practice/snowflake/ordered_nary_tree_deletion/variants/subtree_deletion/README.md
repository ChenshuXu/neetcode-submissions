# Separate Variant — Delete Entire N-ary Subtrees

Delete every listed node and its entire subtree. This is deliberately different from child promotion:
descendants of a deleted node do not survive.

- If the root survives, return `[root]`.
- If the root is deleted, return `[]`.
- Node values are unique, and mutation is allowed.

Implement `delete_subtrees` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/variants/subtree_deletion/run_tests.py
```
