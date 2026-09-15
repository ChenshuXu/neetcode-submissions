# Agent workflow audit — 2026-09-05

Scope: this checkout's instruction files, skill files, workflow entry points, template,
and shared runner. The initial working tree was clean. Hidden and ignored file discovery
found no repository AGENTS.md, SKILL.md/skill.md, agent configuration, or CI workflow.
Global skills and the user's Codex configuration were not modified.

## Findings and changes

| Finding | Resolution |
| --- | --- |
| No repository instruction entry point | Added a 39-line AGENTS.md with task boundaries, context routing, and verification scope. |
| Practice README duplicated company navigation, commands, and historical status | Reduced it from 177 to 64 lines; contracts remain in exercise READMEs. |
| README advertised a missing DoorDash Go module and a generic runner workflow | Removed the dead route and documented the existing standalone Python checks. |
| Hint requests and intentional starters need different handling from implementation | Made the requested mode explicit; completion means fulfilling that mode. |
| Whole-repository test success would be misleading for unfinished practice stubs | Documented target checks, discovery-only checks, and when shared changes need broader coverage. |
| No local skill to optimize | Reused the existing template/README workflow; did not create a duplicate skill. |
| No API harness or model configuration in this repository | No model, reasoning, async-tool, or permission settings introduced. |

## Official guidance and application

- [GPT-6 Astra model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra):
  inspected on the audit date. Applied its guidance on follow-through, conflicting
  instructions, concise communication, and proportional verification. Routine choices
  can proceed within scope; a hint-only request retains its learning boundary.
  Delegation is workload-dependent; this small practice workflow has no blanket mandate.
- [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md):
  used the standard root entry point. Kept repository guidance local rather than copying
  global memory instructions or adding an override file.
- [Build skills](https://learn.chatgpt.com/docs/build-skills): used on-demand context and
  explicit skill scope. A reusable skill requires a SKILL.md with name and description;
  a second copy of this repository's short workflow would add another authority to maintain.

These are repository design choices informed by the guidance, not an official optimal
prompt or a guarantee of maximum model performance.

## Verification and limits

- All relative links in AGENTS.md and the revised practice README resolve.
- Tree runner: discovery, filtered case (1/1), full suite (7/7), and discovery from its own
  exercise directory passed. Microsoft bank discovery and the Dasher Pay inline check passed.
- Static scope review: hints remain answer-limited; requested implementation proceeds to
  relevant checks; shared changes require caller inspection; docs do not require a full suite.
- No solution, test, runner, or template implementation changed. No new testing framework,
  CI job, or global skill override was needed. Diff whitespace checks passed.
- This is document and command validation, not a behavioral model evaluation. No before/after
  token, latency, or solution-quality benchmark was performed. Global skill interactions and
  instruction loading in a fresh Codex session were not end-to-end tested.
