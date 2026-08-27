# Cold prompt: Dasher Payout API

Build the supplied endpoint-like method:

    PayoutService.get_payout(dasher_id)

The injected `DeliveryClient` returns delivery activity for the requested
dasher. The base rate is `0.30` dollars per active delivery-minute. Concurrent
active deliveries each earn that rate, so two active deliveries earn twice the
base rate during their overlap.

Return a stable `PayoutResponse`. The final result must run locally and include
meaningful tests. The prompt is intentionally underspecified: clarify every
ambiguity that would change the implementation before coding.

Run the visible suite with:

    python3 run_tests.py visible

During a cold run, do not open `README.md`, `FOLLOW_UPS.md`,
`INTERVIEWER_PACKET.md`, or `interviewer_checks.py`. Ask the interviewer for
clarification, then request exactly one follow-up after the base suite is green.
