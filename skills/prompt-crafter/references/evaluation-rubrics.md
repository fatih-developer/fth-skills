# Evaluation Rubrics

Use these rubrics when reviewing prompts, agents, workflows, or MCP-oriented packages.

## Prompt Quality

Check:

- `Clarity`: is the request unambiguous?
- `Completeness`: are role, task, constraints, and output shape present?
- `Model Alignment`: is the prompt suited to the target model or tool?
- `Robustness`: does it handle ambiguity, missing input, or edge cases?

## Agent Quality

Check:

- `Role Precision`: is the agent's job crisp?
- `Tool Discipline`: are tool permissions and usage rules clear?
- `Escalation`: does it know when to stop and ask?
- `Safety`: are risky actions bounded?
- `Output Contract`: can another system or user reliably consume the result?

## Workflow Quality

Check:

- `Stage Logic`: do steps follow a sensible order?
- `Decision Gates`: are critical checkpoints explicit?
- `Failure Handling`: does the workflow define what happens on uncertainty or invalid outputs?
- `Efficiency`: is the workflow right-sized for the task?

## MCP-Oriented Package Quality

Check:

- `System Behavior`: is the assistant behavior well-bounded?
- `Tool Guidance`: are tool descriptions clear and least-privilege?
- `Approval Rules`: are high-risk actions gated?
- `Config Clarity`: is the scaffold understandable and internally consistent?
- `Auditability`: can a human inspect what the system is expected to do?

## Suggested Verdicts

- `Strong`: immediately usable with minor or no edits
- `Usable With Edits`: good core, but gaps remain
- `Weak`: the artifact is likely to misfire, drift, or create risk

## Common Failure Modes

- vague role definition
- missing constraints
- missing output contract
- no escalation rules
- excessive prompt length without structure
- unsafe tool autonomy
- unsupported claims about execution behavior
