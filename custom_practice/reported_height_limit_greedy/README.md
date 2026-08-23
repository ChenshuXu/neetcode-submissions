# Snowflake Reported Follow-up — Height Limit Greedy

Return any minimum-size list of node values whose deletion makes an ordered N-ary tree's height at
most `max_height`.

- The root cannot be deleted.
- Height counts nodes: an empty tree has height `0`, and a leaf has height `1`.
- Deleting one node costs one operation and promotes its children to its parent in order.
- Node values are unique.
- Do not mutate the input tree.
- Different minimum-size deletion sets are accepted.

## Evidence boundary

The public Snowflake report confirms this question family: delete N-ary nodes, reconnect their
children to the parent, calculate the resulting height, then use postorder/greedy for a height limit.
The exact API and edge-case contract were not fully published, so the bullets above are explicit
practice assumptions.

Source: [1Point3Acres 1173123](https://www.1point3acres.com/bbs/thread-1173123-1-1.html)

This is the same mathematical target as `followup_3_minimum_deletions_for_height`, but this folder is
a fresh blank attempt specifically for the reported linear-time greedy. It does not replace the
completed DP version.

## Example

```text
root = 1[2[3[5], 4[6]], 7]
max_height = 3
```

Deleting node `2` promotes `3` and `4` to the root:

```text
1[3[5], 4[6], 7]
```

The resulting height is `3`, and one deletion is optimal.

## Target approach

Let `limit = max_height - 1`, the maximum allowed height below the undeletable root.

Use postorder DFS. For each non-root node, return the effective height that replaces it in its
parent after all chosen deletions in that subtree:

1. Process every child and take the maximum returned child height.
2. Keeping the current node would make the effective height `1 + max_child_height`.
3. If that exceeds `limit`, delete the current node. Its children are promoted, so return
   `max_child_height` without adding one.
4. Otherwise keep the node and return `1 + max_child_height`.

Why the greedy step is safe: whenever keeping the current node violates the limit, every valid
solution must pay for at least one deletion in that replacement subtree. Deleting the current node
costs exactly one and shortens every path through it, so choosing the highest such node is never
worse than spending that operation lower in the subtree.

Target complexity: `O(n)` time and `O(h)` recursion space, plus the returned deletion list.

## Run it

Implement `minimum_deletions_for_height` in `solution.py`, then run:

```bash
python3 custom_practice/reported_height_limit_greedy/run_tests.py
```

Useful options:

```bash
python3 custom_practice/reported_height_limit_greedy/run_tests.py --list
python3 custom_practice/reported_height_limit_greedy/run_tests.py --case ancestor
```

The visible trees are intentionally small. The harness checks that the input was not mutated,
applies the returned deletion set, verifies the final height, and brute-forces the true minimum
count. It therefore accepts different correct optimal sets.
