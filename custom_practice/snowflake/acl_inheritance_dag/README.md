# Snowflake Custom — ACL Inheritance on a DAG

This is a runnable cold-practice reconstruction of a reported Snowflake coding-screen family. The
recoverable interview evidence identifies the core task as propagating `ALLOW` and `DENY` permissions
through a DAG. It does not expose the complete original API, output format, or conflict rules.

This package therefore fixes one deterministic practice contract below. The function signature,
global deny-wins rule, sorted output, and whole-graph cycle validation are practice assumptions, not
claims about verbatim interview wording.

## Contract

Implement `resolve_all_acls` in `solution.py`:

```python
def resolve_all_acls(
    node_count: int,
    edges: Sequence[tuple[int, int]],
    local_allow: Mapping[int, Iterable[str]],
    local_deny: Mapping[int, Iterable[str]],
) -> list[list[str]]:
    ...
```

Nodes are numbered from `0` through `node_count - 1`. Each edge `(parent, child)` means that the
child inherits ACL rules from the parent. A node may have multiple parents.

For every node, consider the node itself and every ancestor that can reach it:

- A permission is effectively allowed if at least one node in that inheritance scope allows it and
  no node in the scope denies it.
- A deny anywhere in the scope overrides every allow for the same permission, including a local
  allow on the child.
- A permission with no allow in the scope is not returned.
- Missing mapping entries mean that the node has no local rules of that type.
- Duplicate permissions and duplicate edges do not change the result.
- Return one list per node in node-ID order. Sort each node's effective permissions
  lexicographically.
- If `node_count == 0`, return `[]`.
- The node IDs appearing in edges and ACL mappings are guaranteed to be valid.
- If the graph contains any directed cycle, including a self-loop, raise `ValueError`.

## Example

```text
edges = [(0, 1), (0, 2), (1, 3), (2, 3)]

local_allow = {
    0: ["read"],
    1: ["write"],
    2: ["share"],
    3: ["admin"],
}

local_deny = {
    2: ["write"],
    3: ["read"],
}

resolve_all_acls(...) -> [
    ["read"],
    ["read", "write"],
    ["read", "share"],
    ["admin", "share"],
]
```

Node `3` receives `write` from one parent and a denial of `write` through the other parent, so
`write` is denied. Its local denial also removes the inherited `read` permission.

## Run it

Implement only `resolve_all_acls` in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/acl_inheritance_dag/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/acl_inheritance_dag/run_tests.py --list
python3 custom_practice/snowflake/acl_inheritance_dag/run_tests.py --case diamond
python3 custom_practice/snowflake/acl_inheritance_dag/run_tests.py --case cycle
```

The supplied starter intentionally raises `NotImplementedError` and contains no reference solution.

## Interview target

- 0–5 minutes: clarify edge direction, multiple-parent conflicts, local-versus-inherited precedence,
  default behavior, duplicate edges, and whether acyclicity is guaranteed.
- 5–10 minutes: state the graph representation, propagation order, invariant, and complexity.
- 10–30 minutes: implement permission propagation and cycle detection.
- 30–40 minutes: test the empty graph, a chain, a diamond, multiple roots, duplicate edges, a local
  allow blocked by an inherited deny, and a cycle.

Let `V` be the number of nodes, `E` the number of distinct edges, and `P` the number of distinct
permission names. A set-based topological solution may take `O((V + E) * P)` propagation time,
plus the cost of sorting the returned permissions, and `O(E + V * P)` space. State the tighter cost
of the representation you actually implement.

## Follow-ups to discuss after the base passes

These are practice variants from the broader problem family; the archive does not establish that
they were all asked in the same interview:

1. Return the effective permissions for only one target node.
2. Support an iterative implementation when the inheritance graph is extremely deep.
3. Recompute only affected descendants after one node's local ACL changes.
4. Replace permission sets with bitsets when the permission universe is fixed and small.
5. Explain how the contract changes if a local rule overrides inherited rules instead of deny
   winning globally.
