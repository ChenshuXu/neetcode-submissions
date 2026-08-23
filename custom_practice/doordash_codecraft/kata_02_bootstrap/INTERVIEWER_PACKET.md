# Kata 2 interviewer packet

Candidate: do not read this during a cold run. A friend or Codex can use it to
answer clarification questions and release one follow-up.

## Base-contract answers

- Implement an endpoint-like service method; no HTTP framework is required.
- Validate a blank or whitespace-only user ID before calling any dependency.
- User is required. Missing user maps to UserNotFoundError; unavailable user
  service maps to BootstrapUnavailableError.
- Payment is required for this drill. Any missing or unavailable payment data
  makes the entire request unavailable.
- Address and recent orders are optional.
- A missing address is normal: return address=None without a warning.
- An unavailable or timed-out address returns address=None plus one stable
  address warning.
- No recent orders is normal: return an empty tuple without a warning.
- An unavailable order dependency returns an empty tuple plus one stable order
  warning.
- The base implementation may call dependencies sequentially.
- Preserve the original required-dependency exception as the cause of the
  stable service exception.

## Interviewer pressure cues

Use at most one cue before minute 30:

- Which dependency determines whether the remaining calls are possible?
- Point to the code that expresses the hard-versus-soft dependency decision.
- You have ten minutes until the test milestone. Which refactor can wait?

Do not prescribe a helper, concurrency primitive, or exception hierarchy.

## Follow-up card A: concurrent enrichment

Use for the guided run.

Once user and required payment data are available, address and recent orders
may be fetched concurrently. Preserve deterministic response and warning
behavior. Use only Python standard-library primitives. Explain how you would
enforce a total request deadline even if one optional call hangs.

After implementation ask:

- Why is user lookup not in the same concurrent batch?
- What cleans up unfinished work when the total deadline expires?

## Follow-up card B: bounded retry

Use for one cold run.

The payment dependency may return a transient ClientTimeoutError. Add at most
one retry for that error only. ClientNotFoundError and other permanent errors
must not be retried. Inject any sleep/backoff behavior so the unit tests remain
fast and deterministic.

After implementation ask:

- Why is this retry safe for a read but not automatically safe for a charge?
- Where would the total request deadline be enforced?

## Follow-up card C: policy change

Use when the base implementation overfits to one hard/soft matrix.

For a limited guest experience, payment becomes optional. Change the design so
required versus optional behavior can be configured without duplicating the
entire orchestration path. Do not build a general workflow engine.

After implementation ask:

- What is the smallest abstraction that represents this policy?
- Which behavior remains explicit rather than hidden in a generic helper?

## Post-clock held-back check

Run only after time is called:

    python3 -m unittest -v interviewer_checks.py
