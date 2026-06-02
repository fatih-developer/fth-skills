# Multi-Agent Patterns

Use these patterns only when a single agent is not enough.

Default to one agent unless the separation of responsibilities is clearly useful.

## Coordinator / Specialist / Reviewer

Use when the task benefits from separated planning, execution, and critique.

- `Coordinator`: decomposes the task and routes work
- `Specialist`: performs the main domain work
- `Reviewer`: critiques quality, safety, or correctness

## Researcher / Synthesizer / Critic

Use when the task involves large information gathering followed by writing or decision support.

- `Researcher`: gathers inputs and evidence
- `Synthesizer`: builds the main output
- `Critic`: stress-tests weak assumptions and missed risks

## Multi-Agent Guardrails

- each agent should have a narrow role
- define handoff inputs and outputs
- define who can escalate to the user
- avoid duplicate responsibilities
- add a reviewer when the cost of silent error is high

## When Not To Use Multi-Agent

Avoid it when:

- the task is short and well-bounded
- the overhead exceeds the benefit
- the output can be produced and reviewed reliably by one well-scoped agent
