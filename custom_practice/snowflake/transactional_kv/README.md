# Snowflake Custom — Transactional Key-Value Store

This is a runnable cold-practice contract derived from repeated Snowflake coding-screen reports.
The strongest public descriptions expose `get`, `put`, `begin`, `commit`, `rollback`, and nested
transaction tests. The current Snowflake prep plan also includes `delete`, so this exercise keeps
the reported core and adds `delete` as the first deterministic follow-up.

This is not a verbatim copy of one private prompt. Details that the reports do not fix consistently
are stated explicitly below so the visible tests have one unambiguous answer.

## Evidence boundary

- A 2025-05 screen report exposed `get/put/begin/commit/rollback` plus nested tests.
- A 2025-06 two-round report paired LC212 with a transactional KV question.
- A 2025-12 report again described transactional KV with nested transactions.
- The candidate reports do not establish one universal concurrency contract. Thread safety is a
  discussion follow-up here, not part of the implementation.

## Contract

Implement `TransactionalKV` in `solution.py`:

```python
class TransactionalKV:
    def get(self, key: str) -> Optional[int]:
        ...

    def put(self, key: str, value: int) -> None:
        ...

    def delete(self, key: str) -> None:
        ...

    def begin(self) -> None:
        ...

    def commit(self) -> bool:
        ...

    def rollback(self) -> bool:
        ...
```

Rules:

- Keys are strings. Values are integers; `None` is reserved for a missing key.
- With no active transaction, `put` and `delete` modify committed state immediately.
- `begin` opens a new transaction. Transactions may be nested.
- Reads see the most recent change from the innermost active transaction, then its parents, then
  committed state.
- `commit` closes only the innermost transaction.
  - If a parent transaction exists, merge the changes into that parent.
  - Otherwise, apply the changes to committed state.
- `rollback` discards only the innermost transaction.
- `commit` and `rollback` return `False` when no transaction is active; otherwise they return
  `True`.
- Deleting a missing key is a no-op, but a deletion inside a transaction must still hide an older
  value until that transaction is committed or rolled back.

## Mental model

Think of the store as one permanent dictionary plus a stack of temporary change layers:

```text
top / innermost transaction    {"a": 3}
parent transaction             {"a": 2, "b": 4}
committed state                {"a": 1}
```

Each transaction layer contains only the keys changed in that transaction. A layer does not need a
full copy of the database. `get` searches from the top layer downward, so the visible value of `a`
above is `3`, while the visible value of `b` is `4`.

A deletion needs a private sentinel such as `DELETED`; it cannot use `None` if the contract is later
extended to allow `None` as a real value. Conceptually, a layer might look like this:

```text
{"a": DELETED, "b": 4}
```

The important invariant is:

> For each key, its visible value is determined by the first layer containing that key when we scan
> from the innermost transaction toward committed state.

## What each function does

### `__init__()`

- Creates an empty committed key-value dictionary.
- Creates an empty transaction stack.
- After initialization, there is no active transaction.

### `get(key)`

- Returns the value currently visible to the caller.
- Checks active transactions from innermost to outermost, then checks committed state.
- If the first matching change is a deletion, returns `None` immediately; it must not continue and
  accidentally reveal an older value.
- Returns `None` when the key does not exist. The integer `0` is a valid value and must not be
  mistaken for a missing key.
- Does not modify any state.

### `put(key, value)`

- With an active transaction, records or replaces `key` only in the innermost transaction layer.
- With no active transaction, writes directly to committed state.
- A later `put` for the same key in the same layer replaces that layer's earlier `put` or deletion.
- Returns nothing.

### `delete(key)`

- With an active transaction, records a deletion in the innermost layer so `get` cannot fall through
  to an older value in a parent layer or committed state.
- With no active transaction, removes the key directly from committed state.
- Deleting a currently missing key has no visible effect and must not raise an error.
- A later `put` for the same key in the same transaction makes the new value visible again.
- Returns nothing.

### `begin()`

- Pushes one new empty change layer onto the transaction stack.
- The new layer becomes the innermost active transaction.
- Existing values remain visible until this new layer overwrites or deletes them.
- Returns nothing.

### `commit()`

- Returns `False` and changes nothing when there is no active transaction.
- Otherwise, removes the innermost transaction and returns `True`.
- If a parent transaction still exists, merges every child change into that parent. For the same
  key, the child's change wins.
- If there is no parent, applies the changes to committed state.
- Therefore, committing an inner transaction is not yet globally permanent: an outer rollback can
  still discard the merged changes.

### `rollback()`

- Returns `False` and changes nothing when there is no active transaction.
- Otherwise, discards only the innermost transaction layer and returns `True`.
- The parent transaction, if any, becomes visible again exactly as it was before the child began.
- It never directly changes the parent layer or committed state.

## Worked examples

### Example 1: direct writes without a transaction

```text
put("a", 1)    # committed = {"a": 1}
get("a")       -> 1
put("a", 0)    # zero is a valid stored value
get("a")       -> 0
delete("a")    # committed = {}
get("a")       -> None
commit()        -> False   # there is no transaction to commit
```

### Example 2: rollback restores both an overwritten key and a missing key

```text
put("a", 1)    # committed = {"a": 1}
begin()         # transactions = [{}]
put("a", 2)    # transactions = [{"a": 2}]
put("b", 3)    # transactions = [{"a": 2, "b": 3}]
get("a")       -> 2
get("b")       -> 3
rollback()      -> True
get("a")       -> 1       # old committed value is visible again
get("b")       -> None    # b existed only in the discarded transaction
```

### Example 3: an inner commit can still be undone by an outer rollback

```text
put("a", 1)    # committed = {"a": 1}
begin()         # outer = {}
put("a", 2)    # outer = {"a": 2}
begin()         # inner = {}
put("a", 3)    # inner = {"a": 3}
put("b", 4)    # inner = {"a": 3, "b": 4}
commit()        -> True
                 # inner is merged into outer
                 # outer = {"a": 3, "b": 4}
                 # committed is still {"a": 1}
get("a")       -> 3
get("b")       -> 4
rollback()      -> True
get("a")       -> 1       # outer, including the merged child, was discarded
get("b")       -> None
```

### Example 4: deletion must hide older layers

```text
put("x", 7)    # committed = {"x": 7}
begin()
delete("x")    # transaction = {"x": DELETED}
get("x")       -> None    # do not fall through and return 7
begin()
put("x", 9)
get("x")       -> 9
rollback()      -> True
get("x")       -> None    # parent's deletion is visible again
rollback()      -> True
get("x")       -> 7       # committed value is visible again
```

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/snowflake/transactional_kv/run_tests.py
```

Useful options:

```bash
python3 custom_practice/snowflake/transactional_kv/run_tests.py --list
python3 custom_practice/snowflake/transactional_kv/run_tests.py --case "outer rollback"
```

The runner creates a fresh store for every case and records output only for `get`, `commit`, and
`rollback` operations.

## Interview target

Use the Snowflake execution budget:

- 0–5 minutes: clarify nested-commit behavior, missing-value semantics, and no-transaction errors.
- 5–8 minutes: state the representation and invariants.
- 8–28 minutes: finish a runnable implementation.
- 28–35 minutes: run at least the basic, rollback, nested-commit, and delete tests.
- 35–45 minutes: discuss complexity and one concurrency extension.

A delta-layer solution can achieve:

- `begin`, `put`, `delete`, `rollback`: `O(1)`
- `get`: `O(d)`, where `d` is active transaction depth
- `commit`: `O(c)`, where `c` is the number of keys changed in the committed layer
- space: `O(c_total)` across uncommitted changes

## Follow-ups to discuss after the base passes

1. Make `get` independent of transaction depth using a materialized view plus undo logs.
2. Support `None` as a legitimate stored value without confusing it with a missing key.
3. Give each client or thread its own transaction stack and define visibility of uncommitted writes.
4. Add conflict detection or snapshot isolation instead of serializing every operation with one lock.
5. Persist committed state with a write-ahead log and recovery procedure.
