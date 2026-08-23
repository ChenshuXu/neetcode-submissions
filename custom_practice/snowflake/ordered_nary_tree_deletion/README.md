# Snowflake Custom — Ordered N-ary Tree Deletion

This is a runnable practice contract derived from the reported Snowflake family. Details that were not
publicly fixed by the original report are made explicit here so the exercise has deterministic tests.

## Contract

You receive the root of an ordered N-ary tree and a unique integer `target`.

- Delete the node whose value equals `target`.
- If it has a parent, replace the deleted node in the parent's child list with the deleted node's
  children, preserving their order.
- If the root is deleted, its children become the returned forest roots, in order.
- If `target` is absent, return the unchanged tree.
- Return `list[Node]` for every input. An empty tree returns `[]`.
- Node values are unique. Mutating the input is allowed.

Example:

```text
root = 1[2, 3[5, 6], 4], target = 3
result = [1[2, 5, 6, 4]]
```

Aim for `O(n)` time. Be ready to explain the call-stack or explicit-stack space in terms of tree
height.

## Run it

Implement only `delete_node` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/run_tests.py
```

To add a test, edit `test_cases.py` and append another `Case`. Trees use the compact helper
`t(value, *children)`:

```python
Case(
    name="my case",
    args=(t(10, t(20), t(30, t(40))), 30),
    expected=(t(10, t(20), t(40)),),
)
```

The outer tuple in `expected` is the forest. A one-tree result therefore needs a trailing comma:
`(t(...),)`.
