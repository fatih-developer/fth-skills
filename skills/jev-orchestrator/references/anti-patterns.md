# Anti-Patterns

## Jev as text generator

Bad: `Write a friendly refund email.`

Use the LLM to generate text. Jev may first classify refund reason, tone, or escalation need.

## Jev for arithmetic

Bad: `Compute a weighted average from detector scores.`

Use code.

## Jev for dates

Bad: `Is this subscription 37 days overdue?`

Compute dates in code.

## Replacing deterministic validation

If a parser, schema validator, regex, or exact rule already solves the problem reliably, keep it deterministic.

## Giant multi-purpose judgment

Bad:

```text
Decide whether this is risky, urgent, fraudulent, and write the explanation.
```

Split into atomic judgments, then use the LLM only for prose.

## Sole security enforcement

Bad:

```text
Jev says safe -> execute privileged/destructive action.
```

Use permissions, policy, allowlists, sandboxing, approvals, and other deterministic controls.

## Excessive state

Do not send unrelated conversation history, secrets, tokens, full profiles, or irrelevant files.

## Asking permission to use Jev

If Jev is connected and the bounded semantic decision is reversible/appropriate, invoke it directly.

## Recommending instead of executing

Bad: `This would be a great Jev use case.`

Correct: invoke Jev, consume the result, continue the task.

## Treating typed output as truth

Typed output prevents schema drift; it does not guarantee semantic correctness. Evaluate real accuracy.
