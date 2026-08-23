# Kata 1 guided hints: Dasher Payout API

This file is for a guided or solo-learning run. For a true cold run, open only
COLD_PROMPT.md, dasher_pay.py, and test_dasher_pay.py.

## Candidate prompt

Build an endpoint-like service method:

    PayoutService.get_payout(dasher_id)

The injected DeliveryClient returns deliveries associated with that dasher.
DoorDash pays 0.30 dollars for each active delivery-minute. If two deliveries
are active during the same minute, that minute earns twice the base amount.

Return the total amount and the number of completed deliveries included in the
calculation.

Your result must run locally and be covered by meaningful tests. You may add
private helpers or small abstractions, but the supplied public models and
service method are the starting contract.

## Before coding

The prompt intentionally omits decisions that affect the implementation. Ask
the interviewer about:

- interval boundaries and partial minutes;
- which statuses count;
- invalid or incomplete records;
- upstream failures;
- whether a real HTTP framework is expected;
- whether the final program must run and which tests are supplied.

Do not open INTERVIEWER_PACKET.md until you have asked or written down your
questions.

## Run

    python3 -m unittest -v

Expected starter state: four tests are discovered and fail because
get_payout is not implemented.

## Deliverable

By minute 40, aim for:

- a stable response using Decimal, not binary floating point;
- input validation before the upstream call;
- a completed-delivery calculation;
- explicit invalid-interval behavior;
- stable mapping of upstream failure;
- at least two candidate-written tests beyond the supplied suite.

When the base suite is green, tell the interviewer:

    The happy path and base failure semantics are green. I am ready for the follow-up.
