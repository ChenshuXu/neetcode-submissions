# Dasher Payout API — staged follow-ups

Open this file only after the base visible suite is green. Take one coding card
at a time. The cards are reconstructed from multiple public payout-family
reports; they are not claimed to be one verbatim DoorDash sequence.

## Card 1 — Peak-pay windows (coding)

Add one or more half-open peak windows. Every active delivery-minute inside at
least one peak window pays `2x` the base rate; outside all windows it pays the
base rate. A window may begin or end inside a delivery. Adjacent and overlapping
windows are allowed, but multipliers do not stack above `2x` in this practice
contract.

Keep the original base call usable and add focused tests for:

- no overlap with a window;
- a window strictly inside one delivery;
- a delivery strictly inside one window;
- a boundary that exactly touches a delivery endpoint;
- two overlapping deliveries crossing both sides of a window;
- adjacent or overlapping peak windows.

Use this worked expectation, but write the test yourself:

    deliveries: [0, 10), [5, 15)
    peak:       [8, 12)
    payout:     7.80

After implementation, answer:

- Why does your boundary convention avoid double-counting at `t = 10`?
- What changes if the rate windows come from another service?

## Card 2 — Event-timeline input (coding)

The upstream service now returns events shaped as `(order_id, timestamp,
action)`. Actions are `PICKED_UP`, `DELIVERED`, and `CANCELLED`. A pickup opens
an order interval; one terminal action closes it.

For this deterministic practice variant:

- events may be unsorted;
- exact duplicate events are ignored;
- a conflicting second pickup or second terminal action is invalid;
- a terminal event without a pickup is invalid;
- an unfinished pickup is invalid when payout is finalized.

Convert valid events into paid intervals, then reuse the payout core. Add tests
for a normal order, two overlapping orders, shuffled input, an exact duplicate,
an orphan terminal event, and an unfinished order.

After implementation, say which rules above were provided and which you would
have to clarify in a real interview.

## Card 3A — Fixed cancellation compensation (coding alternative)

Use this card instead of Card 3B.

A cancelled delivery earns a fixed `$2.00` only when it was active for at least
five whole minutes. The compensation is not multiplied by peak pay. Do not use
a field named `completed_at` to represent cancellation without discussing the
model mismatch.

Add tests just below, exactly at, and just above the five-minute threshold, plus
one duplicate-cancellation/idempotency test at the service boundary.

## Card 3B — Cancellation closes the interval (coding alternative)

Use this card instead of Card 3A.

Treat cancellation as a terminal action like delivery completion. Pay the
normal duration-based amount through the half-open cancellation boundary. Add
tests for zero-length, normal, overlapping, and peak-window cancellation.

These two cancellation cards represent different reported variants. Never
silently combine them.

## Card 4 — Slow or unavailable upstream (90-second discussion)

Assume the delivery dependency has a `300 ms` total request deadline for this
rehearsal and sometimes returns a named transient timeout.

Explain:

- which errors are retryable;
- maximum attempts and how all attempts stay inside one total deadline;
- where exponential backoff and jitter belong;
- what the caller receives after exhaustion;
- where circuit breaking and latency metrics live;
- why you would not implement the networking stack inside the pure payout core.

The `300 ms` number is a practice assumption, not recovered DoorDash wording.

## Card 5 — Actually issue the payout (90-second discussion)

The endpoint changes from calculating a number to issuing money.

Explain:

- why recalculation is safe to retry but issuing payment is not automatically
  safe;
- the idempotency key and where its request/result record is persisted;
- what a repeated request returns;
- how an outbox or durable queue prevents commit/publish gaps;
- when a message reaches a DLQ;
- whether the caller sees `completed`, `pending`, or an error.

Do not answer with "exactly once." State the dedupe and replay mechanism.

## Card 6 — Large and out-of-order stream (90-second discussion)

The upstream history no longer fits comfortably in one response.

Explain two separate contracts:

1. chronological events: incremental state, partitioned by `dasher_id`;
2. late/out-of-order events: stable event IDs, allowed lateness, watermark,
   buffering, and adjustment after finalization.

State the time/space cost for an unsorted finite batch and for a chronological
stream. Name what must be persisted so a restart does not double pay.

## Closing lines to rehearse

    The invariant is that every paid active-delivery minute contributes exactly once.

    I have the base behavior green; I will isolate the new rate policy rather than rewrite the endpoint shell.

    Calculation is retryable. Issuing money needs an idempotency key and durable result before I retry it.

    For late events, I need an allowed-lateness contract before I can say when a payout is final.
