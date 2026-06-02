# Agent Templates

Use these templates when the user is designing an agent rather than a one-shot prompt.

## Core Agent Spec

```text
Agent Role:
[what the agent is responsible for]

Inputs:
- [input type]

Available Tools:
- [tool]: [allowed usage]

Memory Policy:
- [what to remember]
- [what not to store]

Decision Rules:
- [how to choose next actions]

Escalation Rules:
- [when to ask the user or a human]

Output Contract:
- [final format]
```

## Research Agent

Use when the goal is gathering, comparing, and summarizing information.

- prioritize source quality
- separate facts from inference
- track uncertainty
- stop before acting on unverified claims

## Coding Agent

Use when the goal is repository work or implementation support.

- define read vs write boundaries
- specify validation expectations
- define how to report changed files and risk
- include rollback or fallback behavior when edits fail

## Reviewer Agent

Use when the goal is critique, QA, or hardening.

- review against explicit criteria
- identify failure modes
- separate must-fix issues from nice-to-have improvements
- avoid rewriting the whole artifact unless necessary

## Support Agent

Use when the goal is user assistance or operational guidance.

- optimize for clarity and next steps
- escalate when account, billing, legal, or sensitive actions are involved
- avoid pretending actions were taken when they were not

## Design Heuristics

Strong agent prompts usually define:

- the agent's job
- the boundaries of autonomy
- the conditions for escalation
- the output contract
- the failure and fallback behavior
