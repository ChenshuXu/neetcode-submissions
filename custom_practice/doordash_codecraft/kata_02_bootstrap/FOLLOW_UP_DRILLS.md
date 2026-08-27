# Bootstrap Aggregator follow-up drill deck

This is an answer-free extension deck. Do not open it during a cold base run.
Use one implementation card per fresh attempt, then finish with three verbal
questions from the production gauntlet.

## Provenance labels

- **Recovered prompt element:** appears in a public report or in multiple
  corroborating reports.
- **Recovered follow-up theme:** the topic was reported, but no single exact
  universal contract was recovered.
- **Training rule:** a deterministic choice added so code and tests can have one
  answer. It is not claimed as DoorDash wording.

Recovered elements include supplied services/classes, user-to-consumer lookup,
payment/address aggregation, runnable tests, partial fields after some
dependency errors, and failure/retry discussion. Orders, account configuration,
gift-card aggregation, parallel calls, and production reliability topics appear
in additional reports. The base kata's exact response fields, required payment
rule, warning order, and exception classes are training rules.

Local evidence trail:

- `/Users/Newton/Documents/job search/projects/context/Interview/doordash/doordash-round-1-codecraft-preparation-plan-2026-08-18.md`
- `/Users/Newton/Documents/job search/projects/context/Interview/doordash/doordash-codecraft-research-refresh-2026-08-25.md`
- `/Users/Newton/Documents/job search/projects/context/Interview/doordash/doordash-xiaohongshu-interview-archive-2026-08-18/posts/6a323e09000000000d00bc00--DoorDash VO｜Bootstrap API 聚合接口设计.md`

## Card 1: remove duplication without hiding policy

Repeated client-call try/except blocks are growing. Refactor the base solution
so the hard/soft policy is still visible at the call site.

Acceptance checks:

- all base and held-back tests remain green;
- required failures preserve the original exception as `__cause__`;
- missing optional data and unavailable optional data remain different;
- warning order remains deterministic;
- the helper does not become a generic workflow engine.

## Card 2: concurrent downstream fan-out and total deadline

After user lookup returns `consumer_id`, fetch payment, address, and recent
orders concurrently with Python standard-library primitives. Payment remains
required; address and orders remain optional.

Acceptance checks:

- user lookup finishes before any consumer-scoped call starts;
- downstream completion order cannot change response or warning order;
- one total deadline bounds the fan-out, rather than granting each future a new
  full timeout;
- a required failure still fails the request and unfinished optional work is
  cancelled or drained deliberately;
- tests coordinate fakes with events/barriers instead of flaky wall-clock
  sleeps.

Explain afterward: why a running Python thread cannot be force-killed safely,
how the HTTP client's own timeout still matters, and when async I/O would be a
better fit than a thread pool.

## Card 3: transient-only retry with exponential backoff

Add an injected retry policy to one read-only dependency. In this drill use one
retry; a public relay mentions up to three retries, but the production count is
a policy choice.

Acceptance checks:

- retry `ClientTimeoutError` only;
- never retry `ClientNotFoundError` or a permanent dependency error;
- delay follows exponential backoff and has an injectable jitter seam;
- tests assert call count and requested delays without sleeping;
- no new attempt or sleep starts when it cannot fit inside the total deadline;
- the final stable error keeps the last dependency error as its cause.

Explain afterward: retry amplification, synchronized retry storms, retry
budgets, and why idempotent reads are safer to retry than payment side effects.

## Card 4: account config and response transformation

**Recovered prompt element:** some reports name account configuration; another
names preprocessing such as summing remaining gift-card balances.

Add an optional `AccountConfigClient`. Its DTO contains gift cards with
`remaining_balance_cents`. Return both stable config fields and
`gift_card_balance_cents` in the public response.

Training rules to clarify before coding:

- whether missing config is normal;
- whether unavailable config adds a warning;
- how duplicate card IDs, negative balances, and integer overflow are handled;
- whether config may be cached more aggressively than user-specific payment.

Keep DTO conversion in a pure function and write a test with at least three
cards, including a zero balance. Do not pass the upstream DTO through unchanged.

## Card 5: configurable guest-mode policy

For a limited guest experience, payment becomes optional. Make the
required-versus-optional choice configurable without duplicating the entire
orchestration method.

Acceptance checks:

- the normal policy still fails closed on payment;
- guest mode returns a partial response and warning on payment outage;
- user identity remains required in both modes;
- the smallest policy object is preferred over a general DAG/workflow engine;
- the response schema stays stable across policies.

## Card 6: HTTP and partial-response mapping

Add a thin endpoint adapter around the service. Use this training map:

- blank request -> 400;
- missing required user -> 404;
- required dependency unavailable -> 503;
- optional dependency failure with usable core response -> 200 plus warnings;
- unexpected bug -> 500 without internal exception text.

Acceptance checks:

- mapping tests assert public status/body, not private exception branches;
- a partial 200 names which field is unavailable without leaking stack traces;
- domain/service code does not import an HTTP framework;
- the adapter has one place that owns status mapping.

## Card 7: cache and duplicate suppression

This is a design-or-small-code follow-up. Define the key and staleness policy
before choosing a cache.

Questions to settle:

- whole-bootstrap cache or per-dependency caches;
- TTL and invalidation for address, payment, orders, and config;
- whether stale optional data may be served on dependency failure;
- whether required identity/payment may ever be stale;
- request coalescing for simultaneous misses on one user;
- authorization and PII boundaries in cache keys and logs.

If coding, implement only a small single-flight wrapper or TTL cache around one
fake dependency. Do not bolt a distributed cache onto the kata.

## Production discussion gauntlet

Answer three in no more than 90 seconds each:

1. Traffic grows 10x. Where do a load balancer and stateless horizontal scaling
   help, and which downstream bottleneck do they not fix?
2. A dependency is failing. How do timeout, bounded retry with jitter, circuit
   breaker, and bulkhead interact? In what order do they apply?
3. Where should rate limiting and backpressure live, and how do they prevent the
   aggregator from amplifying an outage?
4. What is safe to cache, for how long, and when may stale-on-error be used?
5. What does “async” improve, and why must concurrency, queues, and cancellation
   still be bounded?
6. Which metrics make partial success visible? Include per-dependency latency,
   timeout/error/retry counts, circuit state, total latency, and partial-response
   rate.
7. How do correlation IDs and structured warnings let support trace one mobile
   bootstrap request across fan-out calls?
8. How do request deduplication and idempotency differ? Which matters for reads,
   and which becomes critical if a downstream call has side effects?

## Suggested rotation

| Attempt | Implementation card | Verbal close |
|---|---|---|
| guided | Card 1 or 2 | gauntlet 1, 2, 6 |
| cold 1 | Card 3 | gauntlet 2, 5, 8 |
| cold 2 | Card 4 or 5 | gauntlet 3, 4, 7 |
| format hedge | Card 6 | explain 200 partial vs 503 hard failure |

One attempt passing visible or held-back tests is coverage evidence, not cold
no-AI readiness. Readiness still requires a timed runnable attempt with your own
tests, narration, complexity, and one implemented follow-up.
