# DoorDash Code Craft scorecard

This is a coaching rubric, not a claimed DoorDash official score sheet.

Record direct evidence from the code, test output, narration, and run log. Do
not award points for production improvements that were only named vaguely.

| Dimension | Max | Scoring anchor |
|---|---:|---|
| Working behavior and scope control | 15 | 15: runnable vertical slice on time; 8: late or incomplete edge behavior; 0: no meaningful runnable path |
| Requirement clarification and judgment | 10 | 10: clarified implementation-changing ambiguity and prioritized independently; 5: some useful questions; 0: silently guessed core contract |
| Maintainability and readability | 20 | 20: clear names, small cohesive units, low duplication; 10: understandable with notable friction; 0: unfinished or structurally opaque |
| Testability and tests | 15 | 15: injected dependencies plus meaningful happy, boundary, invalid, and failure tests; 8: only supplied/happy tests; 0: no runnable tests |
| Failure handling and API semantics | 15 | 15: stable required/optional behavior and correct exception mapping; 8: partial handling; 0: swallowed or undefined critical failures |
| API and OOP design | 10 | 10: coherent public contract and ownership boundaries; 5: workable but leaky; 0: no stable interface |
| Communication | 10 | 10: concise narration, checkpoints, and explicit tradeoffs; 5: understandable but intermittent; 0: silent or continuously rambling |
| Scalability follow-up | 5 | 5: one relevant, bounded improvement with a real tradeoff; 2: generic suggestion; 0: absent or incorrect |
| Total | 100 | Readiness target: 75 or higher |

## Required evidence

- First runnable happy path:
- First passing candidate-written test:
- Tests passing at minute 42:
- Failure behavior implemented:
- Follow-up attempted:
- Reliability or scalability explanation:
- Final test result:

## Decision

- Total:
- Core-zero check: PASS / FAIL
- Readiness: READY / TARGETED REPAIR / REPEAT COLD
- One highest-leverage repair:

