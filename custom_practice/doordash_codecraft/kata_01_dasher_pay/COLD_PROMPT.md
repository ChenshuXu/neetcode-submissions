# Cold prompt: Dasher Payout API

Build the supplied endpoint-like method:

    PayoutService.get_payout(dasher_id)

The injected DeliveryClient returns deliveries for the requested dasher.
DoorDash pays 0.30 dollars for each active delivery-minute. Concurrent active
deliveries each earn the rate. Return a stable PayoutResponse.

The implementation must run locally and include meaningful tests. The prompt
is intentionally underspecified. Clarify any ambiguity that would change your
implementation before coding.

Run the visible suite with:

    python3 -m unittest -v

During a cold run, do not open README.md, INTERVIEWER_PACKET.md, or
interviewer_checks.py. Ask the interviewer for clarification and for one
follow-up after the base suite is green.

