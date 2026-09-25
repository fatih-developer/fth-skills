# Handoff Contract

<!-- Generated from scripts/templates/ecosystem/handoff-contract.md by scripts/build_ecosystems.py. Edit the template, not the copies. -->

Every skill in an fth-skills ecosystem passes its result to the next skill in the same shape, so a workflow can continue even when steps run in different sessions, agents, or fallback mode.

## Where results go

- **File mode:** when the user wants artifacts, or the skill is running as a step of an ecosystem workflow, write the skill's machine-readable output to the path shown in the ecosystem catalog (for example `docs/api-report/contract-designer-output.json`) and a human-readable report next to it.
- **Inline mode:** for a quick question outside a workflow, do not create files. End the reply with a fenced `json` block titled *Handoff* that uses the same fields.

## Envelope

```json
{
  "skill": "contract-first-designer",
  "schema_version": 1,
  "workflow": "api-design",
  "created_at": "2026-09-25T12:00:00Z",
  "mode": "skill",
  "inputs": ["openapi.yaml"],
  "summary": "Contract for orders and payments, 12 endpoints, RFC 7807 errors.",
  "outputs": {},
  "next": ["api-mock-designer", "sdk-scaffolder"]
}
```

| Field | Meaning |
|---|---|
| `skill` | Skill that produced the result. |
| `schema_version` | Envelope version; currently `1`. |
| `workflow` | Workflow id from `workflows.json`, or `null` when run on its own. |
| `created_at` | ISO 8601 timestamp. |
| `mode` | `skill` when the real skill ran, `fallback` when the orchestrator performed the step itself. |
| `inputs` | Files or artifacts that were read. |
| `summary` | One or two sentences a human can scan. |
| `outputs` | Skill-specific structured data (the fields each skill documents). |
| `next` | Suggested next skills, taken from the workflow map. |

## Rules for the receiving skill

1. Look for the previous step's artifact first; read it instead of re-deriving the same facts.
2. Treat it as input to verify, not as ground truth: re-check anything that drives a destructive or irreversible action.
3. If the artifact is missing or `mode` is `fallback`, say so and proceed with what is available.
4. Never put secrets, tokens, or raw personal data into an artifact; reference their location instead.
5. Do not overwrite another skill's artifact; write your own.
