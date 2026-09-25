# Decision Matrix

| Problem shape | Runtime | Reason |
|---|---|---|
| Exact business rule | Code | Deterministic/testable |
| Arithmetic / counting | Code | Exact computation |
| Date/time comparison | Code | Exact computation |
| Exact lookup | Code / DB | No semantic inference |
| Permission enforcement | Code | Security boundary |
| One semantic option from a known set | Jev Choice | Bounded semantic selection |
| Whether a semantic condition holds | Jev Noul | Binary semantic judgment |
| Degree on an ordered semantic rubric | Jev Score | Bounded grading |
| Intent classification | Jev | Semantic decision |
| Tool/model/agent routing | Jev + Code | Jev judges; code executes |
| RAG relevance | Jev | Semantic evidence judgment |
| Human-review need | Jev + Code | Semantic escalation signal |
| Free-form explanation | LLM | Generative output |
| Rewrite / summary | LLM | Generative output |
| Brainstorming | LLM | Open-ended output |
| Complex open reasoning | Strong LLM | Open-ended reasoning |
| High-impact security decision | Code + verified evidence + human if needed | Jev cannot be sole enforcement |

## Strong Jev candidate

```text
semantic understanding required
AND bounded answer space
AND result is consumed by code
AND decision is useful to the active workflow
```

## Common migration targets

LLM prompts like:

```text
Return one of: bug, feature, billing, other.
```

```text
Return JSON: { relevant: true|false }.
```

```text
Rate quality as low/medium/high.
```

```text
Decide whether human review is needed.
```

These are strong Jev candidates.
