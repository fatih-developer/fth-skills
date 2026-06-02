# Workflow Templates

Use these templates when the user needs a staged process rather than a single prompt.

## Default Workflow

```text
Research -> Analyze -> Generate -> Review -> Refine
```

Use this when the task needs discovery, synthesis, drafting, quality control, and iteration.

## Fast Draft Workflow

```text
Understand -> Generate -> Check
```

Use this for low-risk and low-ambiguity tasks.

## Coding Workflow

```text
Inspect -> Plan -> Edit -> Validate -> Summarize
```

Use this for coding agents and implementation prompts.

## Evaluation Workflow

```text
Detect Type -> Score -> Find Weaknesses -> Revise -> Re-score
```

Use this for prompt critique and optimization loops.

## Agent Workflow

```text
Intake -> Decide -> Use Tools -> Verify -> Escalate or Deliver
```

Use this when the prompt defines an autonomous or semi-autonomous agent.

## Workflow Rules

When building a workflow:

1. define entry conditions
2. define exit conditions for each stage
3. define where human approval is required
4. define what happens when information is missing
5. define quality gates before delivery
