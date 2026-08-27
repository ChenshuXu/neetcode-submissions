# Kata 2 interviewer packet

Candidate: do not read this during a cold run. A friend or Codex can use it to
answer clarification questions and release one follow-up.

## Evidence boundary

Public reports repeatedly support supplied clients/classes, a user-to-consumer
lookup followed by response aggregation, runnable tests, and explicit
hard-versus-soft failure reasoning. Address and payment are the strongest
repeated downstreams; orders, configuration, and credit aggregation appear in
additional reports. Timeout/retry, partial response, and possible parallelism
are recurring discussion themes.

This kata's exact Python models, exception hierarchy, warning order, required
payment rule, and retry/deadline parameters are deterministic training choices.
They are not claimed to be a verbatim DoorDash prompt. Keep that boundary clear
when answering the candidate.

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
- No recent orders, including a missing orders resource, is normal: return an
  empty tuple without a warning.
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

Once user lookup yields consumer_id, payment, address, and recent orders may be
fetched concurrently because all three depend only on that resolved ID. Payment
remains required; address and orders remain optional. Preserve deterministic
response and warning behavior independent of completion order. Use only Python
standard-library primitives. Enforce one total request deadline even if a call
hangs; do not merely place a separate full timeout on each future.

After implementation ask:

- Why is user lookup not in the same concurrent batch?
- If required payment fails, what happens to optional work already in flight?
- What cleans up unfinished work when the total deadline expires, and can a
  Python thread actually be force-killed?

## Follow-up card B: bounded retry

Use for one cold run.

The payment dependency may raise a transient ClientTimeoutError. Add an
injected retry policy with a configurable maximum retry count; set it to one in
the drill, while explaining that a public relay mentions up to three retries
and that the production count is a policy choice. Retry ClientTimeoutError
only. Do not retry ClientNotFoundError or other permanent failures. Use
exponential backoff, leave a jitter seam, and inject sleep/clock behavior so
tests remain fast and deterministic. Every attempt and backoff must fit inside
the total request deadline.

After implementation ask:

- Why is this retry safe for a read but not automatically safe for a charge?
- How can synchronized retries amplify an outage, and what do jitter and a
  retry budget change?
- Where is the total request deadline checked before another attempt or sleep?

## Follow-up card C: policy change

Use when the base implementation overfits to one hard/soft matrix.

For a limited guest experience, payment becomes optional. Change the design so
required versus optional behavior can be configured without duplicating the
entire orchestration path. Do not build a general workflow engine.

After implementation ask:

- What is the smallest abstraction that represents this policy?
- Which behavior remains explicit rather than hidden in a generic helper?

## Follow-up card D: response transformation

Add an AccountConfigClient as another optional consumer-scoped dependency. Its
response includes gift cards with remaining_balance_cents. Add account config
and total remaining gift-card balance to the stable bootstrap response. A
missing config is normal; an unavailable config produces one stable warning.
Do not leak upstream DTOs directly into the public response.

After implementation ask:

- Where should the gift-card sum live so orchestration and transformation stay
  separately testable?
- What should happen with a negative balance, duplicate card ID, or an upstream
  schema change? Clarify rather than inventing behavior.

## Follow-up card E: endpoint mapping

Wrap the service with a thin endpoint adapter. Use this training map unless the
candidate asks to change it:

- blank request -> 400;
- missing required user -> 404;
- required dependency unavailable -> 503;
- core response with optional failures -> 200 plus stable warnings;
- unexpected programming error -> 500 and no internal exception text in the
  response.

After implementation ask why a partial 200 is better than a blanket 500 for
mobile bootstrap, and when a supposedly optional field would become core
enough to change that answer.

## Follow-up card F: production discussion gauntlet

This is verbal; do not ask the candidate to implement a production platform in
the remaining minutes. Pick three, then ask for the trade-off and failure mode:

- load balancer plus stateless horizontal scaling;
- per-dependency timeout, bulkhead, and bounded worker pool;
- circuit breaker behavior for required versus optional dependencies;
- rate limiting and backpressure at the aggregator boundary;
- cache key, TTL, invalidation, and stale-on-error policy;
- duplicate request coalescing and idempotency boundaries;
- bounded async work and cancellation after the caller disconnects;
- correlation ID plus per-dependency latency/error/timeout/retry metrics;
- partial-response rate and warning cardinality as first-class signals.

The complete answer-free rotation and acceptance checks are in
FOLLOW_UP_DRILLS.md.

## Post-clock held-back check

Run only after time is called:

    python3 -m unittest -v interviewer_checks.py
