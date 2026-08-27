# Kata 3 interviewer packet

Candidate: do not read this during a cold run. A friend or Codex can use it to
answer clarification questions and release one follow-up.

## Base-contract answers

- Implement a plain validator; no HTTP framework is required.
- The recovered report names quantity, available inventory, and min/max rules.
  Duplicate semantics and exact output ordering are deterministic training
  choices rather than recovered prompt wording.
- Return all user-correctable errors in a stable typed schema.
- Preserve first-seen item order.
- Duplicate lines are invalid. Emit one error for that item and skip its later
  checks rather than silently merging quantities.
- Quantity must have exact runtime type `int` and be greater than zero; `bool`
  and `float` are invalid for this exercise.
- Minimum and maximum quantities are inclusive.
- A valid unique item can produce more than one business-rule error. Their
  order is minimum, maximum, then available inventory.
- The inventory input is a read-only snapshot. The base method must not mutate
  it and does not promise that stock remains available after it returns.

## Interviewer pressure cues

Use at most one cue before minute 15:

- What must you know about all lines before validating the first item?
- If duplicate lines are illegal, which quantity would you validate?
- How will a caller receive every fix in one response without nondeterminism?

Do not prescribe a helper, map layout, or loop structure.

## Follow-up card A: atomic reservation and idempotency

Use for the guided run.

Add an injected inventory gateway with an atomic operation shaped like:

```text
reserve(request_id, restaurant_id, quantities) -> reservation result
```

Pure validation still runs first. If it passes, call `reserve` once. The
snapshot may be stale, so an atomic reservation failure must become a stable
`INSUFFICIENT_INVENTORY` result. `request_id` is the idempotency key: repeating
the same request returns the original outcome and never decrements twice.

Ask:

- Which layer owns the compare-and-decrement transaction?
- What prevents two service instances from both accepting the last item?
- What is stored for an idempotency key, and for how long?

## Follow-up card B: timeout and cancellation

A successful reservation has a lease expiration. Confirming the order commits
it; cancellation releases it. Both confirm and release are idempotent. A
background worker may reclaim expired reservations, but correctness cannot
depend on the client successfully sending a cancellation.

Ask:

- What state transition prevents confirm and timeout release from both winning?
- Which clock and expiration field are authoritative?
- What does a retry receive after the reservation has already expired?

## Follow-up card C: hot SKU discussion

Do not implement distributed infrastructure. Explain in under 90 seconds:

- why a process-local lock is insufficient across service instances;
- when a database conditional update is enough;
- how per-SKU serialization, sharded counters, or queued admission trade exact
  real-time stock for throughput;
- why cache may reject early but must not be the final stock authority.

## Post-clock held-back check

Run only after time is called:

```bash
python3 -m unittest -v interviewer_checks.py
```
