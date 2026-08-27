# Kata 2 guided hints: Bootstrap Aggregator API

This file is for a guided or solo-learning run. For a true cold run, open only
COLD_PROMPT.md, bootstrap.py, and test_bootstrap.py.

The starter covers the recurring aggregation core. `FOLLOW_UP_DRILLS.md`
contains the answer-free extension deck for the remaining reported and
plausible follow-ups. Open it only after the base attempt or let the interviewer
release one card at a time.

## Candidate prompt

Implement:

    BootstrapService.get_bootstrap(user_id)

The UserClient resolves the public user ID to a consumer ID and core user
record. AddressClient, PaymentClient, and OrderClient use that consumer ID.
Return one stable BootstrapResponse.

Some dependencies are required and others are optional. The method must define
observable behavior for missing resources, downstream failures, and partial
responses. Start sequentially; optimize only when the base behavior is clear
and tested.

## Before coding

Ask the interviewer:

- which dependencies are required versus optional;
- whether missing and unavailable mean the same thing;
- how partial data should be represented;
- whether warnings belong in the response;
- whether calls must be parallel;
- which exceptions are considered transient;
- whether a real HTTP endpoint is required.

Do not open INTERVIEWER_PACKET.md until you have asked or written down your
questions.

## Run

    python3 -m unittest -v

Expected starter state: four tests are discovered and fail because
get_bootstrap is not implemented.

## Deliverable

By minute 40, aim for:

- request validation before any dependency call;
- user lookup before consumer-scoped calls;
- required user and payment semantics;
- optional address and order partial-success semantics;
- deterministic warnings;
- at least two candidate-written tests beyond the supplied suite.

When the base suite is green, tell the interviewer:

    The base aggregation and failure matrix are green. I am ready for the follow-up.

## Follow-up rotation

Do not try to implement every production concern in one 60-minute run. Across
fresh attempts, rotate through:

1. remove duplicated error-handling code without hiding the hard/soft matrix;
2. concurrent downstream fan-out plus a total deadline;
3. transient-only retry with bounded exponential backoff;
4. account-config or gift-card response transformation;
5. configurable guest-mode policy;
6. HTTP status and partial-response mapping.

After each implementation follow-up, take the production discussion gauntlet
in `FOLLOW_UP_DRILLS.md` verbally. That deck covers retry amplification, load
balancing, horizontal scaling, circuit breaking, rate limiting, caching,
deduplication, bounded async work, and observability.
