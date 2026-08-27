# Dasher Payout API — interviewer packet

Candidate: do not read this during a cold run. A friend or Codex can use it to
answer clarification questions, release one follow-up at a time, and evaluate
the resulting discussion.

## Evidence boundary

Use these labels consistently:

- **Recovered:** repeated public reports explicitly support the item.
- **Variant:** reported in at least one payout-family experience, but not a
  guaranteed part of every prompt.
- **Practice assumption:** fixed here only so the local tests are deterministic.
- **Unknown:** public evidence does not recover the exact interview rule.

The base rate, concurrent-delivery multiplier, mocked upstream data, runnable
code/tests, timeline boundaries, and upstream latency discussion are recovered.
Peak-rate windows, event timelines, cancellation, retry/idempotency, and
streaming appear across variants and follow-up discussions. Do not claim that
one candidate received all cards or that the card order is official.

A close-match report uses a monolith-to-microservice payment-service framing.
Other current reports vary between no scaffold/no tests, a blank `Main` with a
few examples, and light supplied classes. Treat those as presentation modes,
not different payout algorithms. One close-match candidate received no new
feature follow-up and used the remaining time on timeline edges and upstream
latency; do not force a coding extension if the mock interviewer instead asks
for deeper tests and production discussion.

## Base-contract answers

- **Practice assumption:** implement an endpoint-like service method; no HTTP
  framework is required.
- **Practice assumption:** a blank or whitespace-only dasher ID is invalid, and
  the upstream client must not be called.
- **Practice assumption:** only `COMPLETED` deliveries count in the base
  version. `ACTIVE` and `CANCELLED` records are ignored.
- **Practice assumption:** timestamps are aligned to whole minutes. Treat
  intervals as half-open: `accepted_at` is included and `completed_at` is
  excluded.
- **Practice assumption:** a completed delivery must have `completed_at`
  strictly after `accepted_at`.
- **Practice assumption:** use `Decimal` and return money to cents.
- **Practice assumption:** a `DeliveryClientError` becomes a stable
  `PayoutUnavailableError`, preserving the original exception as its cause.
- **Recovered format signal:** the final result and tests must run locally. The
  candidate may inspect and extend the visible tests.

If the candidate asks about partial minutes, answer: "For this base run, inputs
are whole-minute aligned. Tell me where you would isolate a different rounding
policy." Do not make them implement a rounding system before the happy path.

## What a strong base implementation says aloud

The candidate does not need a sweep line for the base version. Paying
`active_count * rate` over time is algebraically the same as adding each
completed delivery's duration once, including overlaps. A direct `O(D)` sum is
the smallest correct slice.

Accept either a direct sum or a correct sweep. If the candidate starts with a
minute-by-minute simulation or pairwise overlap comparisons, ask what input
duration or delivery count makes that work unnecessary.

Expected invariant:

> After processing the first `k` paid deliveries, `amount` equals the base rate
> times the sum of their active minutes, and `completed_delivery_count == k`.

## Interviewer pressure cues

Use at most one cue before minute 30:

- What is the smallest slice you can make run first?
- Which rule in your current code is hardest to test?
- You have ten minutes until the happy-path milestone. What will you cut?
- Does the overlap rule really require comparing deliveries pairwise?

Do not prescribe an algorithm, helper, or class hierarchy.

## Follow-up release protocol

The candidate should take one coding card in a 60-minute rep, then discuss two
production cards if time remains. `FOLLOW_UPS.md` contains the candidate-facing
wording. The sections below are the evaluation key.

### Card 1 — one or more peak-pay windows

**Recovered variant:** peak/double-pay windows and boundary splitting.

Expected insight: payout can only change at a delivery start/end or rate-window
start/end. Between adjacent sorted boundaries, active count and the rate
multiplier are constant. A boundary sweep avoids expanding every minute.

Practice assumptions:

- windows are half-open;
- being inside any peak window means `2x`, even if input windows overlap;
- adjacent and overlapping peak windows are allowed;
- round only the final total to cents.

High-value tests:

- delivery `[0, 10)`, peak `[3, 5)` -> `$3.60`;
- delivery `[0, 10)`, peak `[10, 20)` -> `$3.00`;
- deliveries `[0, 10)` and `[5, 15)`, peak `[8, 12)` -> `$7.80`;
- touching/overlapping peak windows do not stack above `2x` under this harness.

Ask after coding:

- Why is applying all deltas at one timestamp safe for half-open intervals?
- What fails if peak windows come from a remote pricing dependency?

### Card 2 — order-event timeline

**Recovered variant:** events carry order ID, timestamp, and action; public
reports name pickup/finish, and one report treats cancellation as a terminal
event. Exact duplicate and disorder semantics are not recovered.

Practice contract for this card:

- actions are `PICKED_UP`, `DELIVERED`, and `CANCELLED`;
- one pickup opens an interval; one terminal action closes it;
- input may be unsorted, so sort by `(timestamp, action_priority, order_id)`;
- an exact duplicate event is ignored; a second conflicting start or terminal
  action is invalid;
- a terminal event without a pickup and an unfinished pickup are invalid for
  this drill.

Expected invariant: the open-order map contains exactly the orders with one
accepted start and no terminal event among the processed canonical events.

Ask after coding:

- Which of the disorder/duplicate rules came from the prompt, and which did we
  choose for the harness?
- How would the design change if late events may arrive after payout closes?

### Card 3 — cancellation policy

**Variant:** reports expose both fixed cancellation compensation and a version
where cancellation is treated like fulfillment. Release exactly one policy;
do not combine them as if the interview contract were consistent.

Policy A for this harness:

- a cancelled delivery receives `$2.00` only after at least five whole active
  minutes;
- cancellation compensation is fixed and is not peak-multiplied;
- rename/generalize the terminal timestamp instead of pretending a cancellation
  time is a completion time.

Policy B for an alternate rep:

- cancellation closes the active interval exactly like delivery completion;
- it receives duration-based pay through the cancellation boundary.

Ask after coding:

- Where does this business policy live so a future rule does not rewrite the
  endpoint shell?
- How do you prevent the same cancellation from being paid twice?

### Card 4 — upstream latency and unavailability

**Recovered discussion:** latency/SLA, unavailable dependencies, bounded retry,
backoff with jitter, circuit breaking, and sometimes a DLQ or asynchronous
decoupling. Exact numbers are unknown.

Use a rehearsal-only `300 ms` total deadline. A strong 90-second answer should
cover:

1. validate before I/O;
2. retry only named transient failures while the total deadline still permits;
3. cap attempts and use exponential backoff with jitter outside the pure
   calculator;
4. map exhaustion to one stable service error;
5. count latency, attempts, exhaustion, and circuit state in observability;
6. avoid implementing a circuit breaker inside the interview method.

Do not accept "retry every exception" or an unbounded retry loop.

### Card 5 — calculation versus issuing payment

**Recovered discussion:** idempotent payment calls and message-queue
decoupling. Some reports also mention DLQ behavior.

Expected distinction:

- recalculating a deterministic payout is a read/compute operation and can be
  retried;
- issuing money is a side effect and requires an idempotency key such as
  `(dasher_id, payout_period)` plus a persisted request/result record;
- retries reuse the same key and return the stored result;
- an outbox or durable queue prevents a database commit and publish from
  diverging;
- poison/exhausted messages go to a DLQ for investigation, not silent replay.

Ask what the caller receives while an issuance is still pending and whether the
API is synchronous or asynchronous. There is no single recovered answer.

### Card 6 — large or out-of-order event stream

**Variant/follow-up:** scale and event-stream discussion is useful, but the
exact streaming API is not recovered.

Expected answer:

- if events are chronological, carry `previous_time`, `active_count`, current
  rate state, and accrued payout; each event is `O(1)` after ordering;
- if a finite batch is unsorted, sort boundaries in `O(E log E)`;
- if events can arrive late, define allowed lateness and a watermark, buffer the
  open window, and either correct a not-yet-final payout or post an adjustment;
- dedupe by stable event ID before mutating state;
- partition by `dasher_id` so one dasher's timeline is ordered by one consumer.

Do not accept "just use Kafka" without stating ordering, partition key,
dedupe, and finalization semantics.

## Final review checklist

- Base code runs from the documented command.
- At least four meaningful tests pass before a follow-up starts.
- Request validation happens before the upstream call.
- Money avoids binary floating point.
- Interval boundaries are stated, not inferred from code.
- Upstream errors have stable caller-facing semantics.
- The candidate separates payout calculation from payout issuance.
- Follow-up facts are labeled as recovered variants or practice assumptions.

## Post-clock held-back check

Run only after time is called:

    python3 run_tests.py held-back
