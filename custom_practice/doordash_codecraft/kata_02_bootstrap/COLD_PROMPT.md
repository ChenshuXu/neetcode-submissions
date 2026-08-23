# Cold prompt: Bootstrap Aggregator API

Implement the supplied endpoint-like method:

    BootstrapService.get_bootstrap(user_id)

UserClient resolves the public user ID to core user data and a consumer ID.
AddressClient, PaymentClient, and OrderClient accept that consumer ID. Assemble
one stable BootstrapResponse.

Some dependencies may be required and others may be optional. The
implementation must define observable failure and partial-response behavior,
run locally, and include meaningful tests. Clarify any ambiguity that would
change your implementation before coding.

Run the visible suite with:

    python3 -m unittest -v

During a cold run, do not open README.md, INTERVIEWER_PACKET.md, or
interviewer_checks.py. Ask the interviewer for clarification and for one
follow-up after the base suite is green.

