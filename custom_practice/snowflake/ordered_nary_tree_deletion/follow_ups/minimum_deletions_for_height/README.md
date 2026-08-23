# Follow-up 3 — Minimum Deletions for Maximum Height

Return any minimum-size list of node values whose deletion makes the tree height at most
`max_height`.

- The root cannot be deleted.
- Height counts nodes.
- Deleting a node costs one operation and promotes its children.
- Node values are unique.
- Do not mutate the tree.

Implement `minimum_deletions_for_height` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/minimum_deletions_for_height/run_tests.py
```

The visible trees are intentionally small. The harness applies your returned set, checks the resulting
height, and brute-forces the true minimum count. Different optimal deletion sets are accepted.
