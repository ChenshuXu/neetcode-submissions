# Follow-up 4 — Parent-index Forest Deletion

The forest is encoded as a parent array:

```text
parent[node] = parent index
parent[node] = -1 for a root
```

Delete every index in `to_delete`. A survivor whose parent is deleted reconnects to its nearest
surviving ancestor; if none exists, it becomes a root. Mark deleted nodes with `-2`.

Implement `delete_from_parent_array` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/ordered_nary_tree_deletion/follow_ups/parent_index_forest/run_tests.py
```
