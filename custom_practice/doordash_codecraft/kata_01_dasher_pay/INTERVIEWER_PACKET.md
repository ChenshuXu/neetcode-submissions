# Kata 1 interviewer packet

Candidate: do not read this during a cold run. A friend or Codex can use it to
answer clarification questions and release one follow-up.

## Base-contract answers

- Implement an endpoint-like service method; no HTTP framework is required.
- A blank or whitespace-only dasher ID is invalid, and the upstream client
  should not be called.
- Only COMPLETED deliveries count in the base version.
- Base inputs are aligned to whole minutes. Treat intervals as half-open:
  accepted_at is included and completed_at is excluded.
- A completed delivery must have completed_at strictly after accepted_at.
- ACTIVE and CANCELLED records are ignored in the base version.
- The amount must use Decimal and be represented to cents.
- A DeliveryClientError must become a stable PayoutUnavailableError while
  preserving the original exception as its cause.
- The supplied visible tests may be read and extended. The final suite must run
  locally.

## Interviewer pressure cues

Use at most one cue before minute 30:

- What is the smallest slice you can make run first?
- Which rule in your current code is hardest to test?
- You have ten minutes until the happy-path milestone. What will you cut?

Do not prescribe an algorithm, helper, or class hierarchy.

## Follow-up card A: peak pay

Use for the guided run.

Add a single peak-pay window. Every active delivery-minute inside the half-open
peak window pays twice the base rate; minutes outside it use the normal rate.
The window may partially overlap a delivery. Keep the original public method
usable and add focused boundary tests.

After implementation ask:

- Why did you put this rule at that boundary?
- What changes if peak windows come from a remote pricing service?

## Follow-up card B: cancellation

Use for one cold run.

A cancelled delivery earns a fixed 2.00-dollar compensation only when it was
active for at least five whole minutes before cancellation. The record's
completed_at field carries the cancellation time for this extension. Do not
pay active unfinished records. Add the smallest coherent model or policy change
and tests.

After implementation ask:

- What naming or model change avoids treating cancellation time as completion?
- How would you prevent issuing the same compensation twice?

## Follow-up card C: upstream degradation

Use when implementation time is already tight.

The delivery service now has a 300 ms deadline and occasional transient
timeouts. Do not implement networking infrastructure. Explain in under
90 seconds:

- which errors, if any, are retryable;
- the total deadline and maximum attempts;
- why calculation is safe to retry but actual payment issuance may not be;
- what the caller receives when the dependency remains unavailable.

## Post-clock held-back check

Run only after time is called:

    python3 -m unittest -v interviewer_checks.py
