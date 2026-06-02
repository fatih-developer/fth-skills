# MCP Templates

Use these templates when the user wants MCP-oriented prompt assets.

V1 scope:

- system prompt guidance
- tool description guidance
- approval rules
- workflow rules
- evaluation checks
- config scaffolds

Do not claim runtime compatibility unless the user names the target MCP environment and explicitly requests a concrete adaptation.

## MCP Package Skeleton

```text
Package Goal:
[what the assistant should accomplish]

System Prompt Guidance:
- [role]
- [behavior rules]
- [safety and refusal rules]

Tool Description Guidance:
- [tool name]: [purpose, when to use, when not to use]

Approval Policy:
- require human approval for [high-risk actions]

Workflow Rules:
- [how to reason about tools, uncertainty, and handoff]

Evaluation Checks:
- [how to review output quality and safety]

Config Scaffold:
- transport: [placeholder]
- tools: [placeholder]
- permissions: [placeholder]
```

## Tool Description Pattern

```text
Tool:
[name]

Use when:
- [valid use case]

Do not use when:
- [invalid or risky case]

Inputs:
- [required fields]

Failure handling:
- [what the assistant should do]
```

## Approval Rules Pattern

Always specify approval gates for:

- destructive file changes
- external side effects
- payments or purchases
- credential use
- sensitive data access
- irreversible operations

## MCP Safety Notes

- prefer least privilege
- avoid hidden autonomy
- define refusal conditions
- define fallback behavior when tools fail or return incomplete results
