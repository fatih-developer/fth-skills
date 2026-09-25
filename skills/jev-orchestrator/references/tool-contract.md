# Jev Tool Contract

The skill assumes a connected TypeSafe/Jev MCP or equivalent tool exists.

Tool names and schemas may vary by host. Never invent a tool name when the host exposes a different schema.

## Discovery

If the Jev operations are visible, invoke them directly.

Otherwise:

1. inspect connected tools;
2. identify the TypeSafe/Jev integration;
3. find Choice, Noul, Score, or a generic typed-judgment operation;
4. call the matching operation.

Do not ask the user for setup details unless discovery/invocation proves the integration is unavailable.

## Conceptual request shape

The real tool schema is authoritative, but a request conceptually contains:

```json
{
  "state": {},
  "questions": [
    {
      "id": "route",
      "primitive": "choice",
      "instruction": "...",
      "options": ["...", "..."]
    }
  ]
}
```

## Response handling

Consume whatever the connected tool actually returns: selected option, probability/distribution, confidence, score, or equivalent typed result.

Do not hard-code conceptual example field names against a different real schema.

## Failure

If invocation fails:

```text
preserve deterministic state
-> project fallback
-> generative semantic judge when safe
-> human/manual review when necessary
```

Never expose credentials.

## Versioning

When model/version selection is exposed:
- follow project configuration;
- respect pinned production versions;
- record model version for evaluation where feasible.
