# Dasher Payout API — guided custom practice

This package is a runnable reconstruction for DoorDash Code Craft preparation.
It is not DoorDash-owned material and is not claimed to reproduce one verbatim
prompt.

For a true cold run, open only `COLD_PROMPT.md`, `dasher_pay.py`, and
`test_dasher_pay.py`. Do not open `FOLLOW_UPS.md`, `INTERVIEWER_PACKET.md`, or
`interviewer_checks.py` until the base version is green or time is called.

## What the reports actually recover

Repeated public reports support this base shape:

- an endpoint-like payout operation receives a `dasher_id`;
- a supplied or mocked upstream dependency returns delivery activity;
- pay is sometimes stated as `$0.30` per active delivery-minute;
- concurrent deliveries multiply the rate by the active-delivery count;
- the result must run, and the candidate may need to write their own tests;
- discussion commonly moves to timeline boundaries and upstream latency or
  unavailability.

One close-match report frames the work as extracting payout logic from a
monolith into a new payment microservice. Presentation varies from a blank file
or `Main` plus zero/few examples to a light supplied model/client scaffold. In
all modes, clarify whether the upstream must be exercised through a mock client
rather than bypassed with direct fixture input. One report had no functional
extension at all; the remaining time went to timeline edge cases and upstream
latency.

The exact input model, interval convention, partial-minute rule, error schema,
and framework requirement vary or remain unrecovered. The deterministic choices
in this package are rehearsal assumptions. Ask about them before coding.

## Candidate prompt

Build an endpoint-like service method:

    PayoutService.get_payout(dasher_id)

The injected `DeliveryClient` returns deliveries associated with that dasher.
DoorDash pays `0.30` dollars for each active delivery-minute. If two deliveries
are active during the same minute, that minute earns twice the base amount.

Return the total amount and the number of completed deliveries included in the
calculation. The result must run locally and be covered by meaningful tests.

You may add private helpers or small abstractions, but the supplied public
models and service method are the starting contract.

## Before coding

Ask only questions that change the implementation:

- Are activity intervals half-open, and are timestamps aligned to whole
  minutes?
- Which statuses are paid? What happens to invalid or unfinished records?
- Does a blank `dasher_id` fail before the upstream call?
- How should an upstream dependency failure appear to this service's caller?
- Is an endpoint-like class enough, or is a real HTTP framework required?
- Are tests supplied, and must the final program run from a `main` or test
  command?

Do not open `INTERVIEWER_PACKET.md` until you have asked or written down these
questions.

## Run

From this directory:

    python3 run_tests.py visible

Expected starter state: four tests are discovered and fail because
`get_payout` is intentionally unimplemented.

After time is called:

    python3 run_tests.py held-back

To rerun both suites after implementing the base contract:

    python3 run_tests.py all

## Sixty-minute sequence

| Time | Required outcome |
|---:|---|
| `0–5` | Restate the contract and resolve interval, status, dependency, and runnable-test semantics |
| `5–9` | Name one service boundary, one pure calculation boundary, and the first four tests |
| `9–28` | Make one real request produce one real response |
| `28–40` | Add validation, upstream-error mapping, and candidate-written boundary tests |
| `40–49` | Take exactly one coding follow-up from `FOLLOW_UPS.md` |
| `49–54` | Refactor only what the follow-up proved necessary and rerun tests |
| `54–60` | State complexity, unimplemented production work, and retry/idempotency boundary |

If the happy path is not running by minute 30, collapse speculative structure
instead of adding a framework, repository, factory, or circuit breaker.

## Base deliverable

By minute 40, aim for:

- a stable response using `Decimal`, not binary floating point;
- request validation before the upstream call;
- completed-delivery payout behind an injected `DeliveryClient`;
- explicit invalid-interval behavior;
- stable mapping of the named upstream failure;
- at least two candidate-written tests beyond the supplied suite.

When the base suite is green, say:

    The base behavior and failure semantics are green. I am ready for one follow-up.

Then open `FOLLOW_UPS.md` or ask an interviewer to release one card. The deck
covers every recovered extension family without claiming that all of them
appear in one interview.

## Cold-practice integrity

`dasher_pay.py` deliberately retains `NotImplementedError`. A temporary
reference implementation is used only for package and Notion-card verification
and is removed afterward. Passing reference tests proves the contract is
coherent; it does not prove cold, no-AI readiness. Readiness requires a timed
attempt in a fresh `attempts/` directory.
