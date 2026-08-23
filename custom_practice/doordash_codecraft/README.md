# DoorDash Code Craft practice pack

This is a local, executable practice environment for Newton's Round 1. It is
based on the recurring public task families and the recruiter's stated rubric;
it is not DoorDash-owned material and is not claimed to reproduce an exact
interview question.

The package deliberately uses Python's standard library only. It needs no
account, subscription, network access, or package installation.

## Start here

Use Kata 1 first. Create a fresh attempt so the reviewed starter template stays
unchanged:

    cd "/Users/Newton/Documents/job search/neetcode-submissions/custom_practice/doordash_codecraft"
    python3 new_attempt.py dasher-pay guided-dasher-01
    cd attempts/guided-dasher-01
    python3 -m unittest -v

The first run should discover four tests and fail because the service method
is intentionally unimplemented. That is the correct starter state.

When it is time for the second kata:

    cd "/Users/Newton/Documents/job search/neetcode-submissions/custom_practice/doordash_codecraft"
    python3 new_attempt.py bootstrap guided-bootstrap-01
    cd attempts/guided-bootstrap-01
    python3 -m unittest -v

That first run should discover four tests and fail for the same reason.

## What to edit

- Edit only the files inside the newly created attempts folder.
- Kata 1: edit dasher_pay.py and add tests to test_dasher_pay.py.
- Kata 2: edit bootstrap.py and add tests to test_bootstrap.py.
- Treat kata_01_dasher_pay and kata_02_bootstrap as immutable templates.
- The visible tests are part of the supplied interview environment. You may
  add candidate-written tests to the existing test file.
- The interviewer_checks.py files are intentionally excluded from normal test
  discovery. Do not read or run them until time is called.
- Do not change an existing assertion just to make a failure disappear. If you
  believe the contract is wrong, state the disagreement before changing it.

## Practice modes

### Guided baseline

Message Codex:

    开始 DoorDash Kata 1 guided

Codex acts as the interviewer. Ask clarification questions in English. Start
the 60-minute clock only after Codex says the prompt is complete. During the
run, Codex should answer contract questions but should not write code or reveal
an implementation.

### Solo baseline

1. Create a fresh attempt with new_attempt.py.
2. Open only COLD_PROMPT.md, the starter file, and the visible tests.
3. Say your clarification questions out loud.
4. Open the canonical interviewer packet only to obtain the answers.
5. Start a 60-minute timer.
6. Record milestones in RUN_LOG.md.
7. Stop at 60 minutes, even if unfinished.

### Cold repetition

Create a new, uniquely named attempt with new_attempt.py. The command refuses
to overwrite earlier work and verifies that the canonical starter files still
match the reviewed hashes. Do not read the guided README, interviewer packet,
previous code, or solution notes. Ask Codex for an unseen follow-up only after
the base tests pass.

Example:

    python3 new_attempt.py dasher-pay cold-dasher-01

After time is called, run the held-back checks from inside the attempt:

    python3 -m unittest -v interviewer_checks.py

## Sixty-minute operating rhythm

| Time | Required outcome |
|---|---|
| 0–5 | Clarify contract, run/test expectation, and failure semantics |
| 5–9 | State the minimum model, service boundary, and first test |
| 9–28 | Produce the smallest runnable happy path |
| 28–40 | Add validation and high-value tests |
| 40–49 | Take one interviewer-selected follow-up |
| 49–54 | Refactor and rerun the full suite |
| 54–60 | Summarize coverage, limitations, and next production step |

If the happy path is not running by minute 30, remove speculative abstractions
and collapse to a smaller service implementation.

## No-AI baseline rules

The baseline should mimic the current default for DoorDash live interviews:

- no AI-generated code, chat assistance, or AI completion during the timed run;
- ordinary non-AI editor completion is fine;
- language or standard-library documentation only if the exact recruiter
  packet allows it;
- Codex may act as interviewer during the clock, but may answer only contract
  questions and release follow-ups, not implementation questions;
- after time is called, Codex may inspect the implementation, tests, terminal
  output, and RUN_LOG, then score the result.

The exact recruiter packet and interviewer's instructions override these
practice defaults.

## Readiness gate

Both cold katas must independently meet all of these:

- runnable happy path by minute 30;
- at least four meaningful tests passing by minute 42;
- at least two of those tests written by the candidate;
- one dependency-failure or partial-success behavior implemented;
- one follow-up handled without dismantling the base design;
- one relevant reliability or scalability tradeoff explained in under
  90 seconds;
- at least 75/100 on SCORECARD.md;
- no zero in working behavior, tests, or failure handling.

## Files

- kata_01_dasher_pay: light starter, closer to a blank service exercise.
- kata_02_bootstrap: supplied clients and models, closer to an existing-code
  aggregation exercise.
- new_attempt.py: creates a fresh, non-overwriting attempt and verifies the
  reviewed starter files before copying.
- attempts: all candidate edits and run logs belong here.
- SCORECARD.md: weighted post-run assessment.
- RUN_LOG_TEMPLATE.md: timestamps and self-assessment to copy for each run.
