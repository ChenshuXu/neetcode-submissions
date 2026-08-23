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

The critical nested behavior is:

```text
put("a", 1)
begin()
put("a", 2)
begin()
put("a", 3)
commit()       -> True
get("a")      -> 3
rollback()     -> True
get("a")      -> 1
```

The inner commit is not globally permanent. It remains part of the parent transaction, so the outer
rollback must still undo it.

## Run it

Implement only the class in `solution.py`, then run:

```bash
python3 custom_practice/transactional_kv/run_tests.py
```

Useful options:

```bash
python3 custom_practice/transactional_kv/run_tests.py --list
python3 custom_practice/transactional_kv/run_tests.py --case "outer rollback"
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
