# Structure Selection

Use the least expensive structure that makes the task unambiguous.

## Decision table

| Prompt shape | Default structure | Reason |
|---|---|---|
| One short action | Compact natural sentence | Lowest overhead |
| One action with a few constraints | Short sentence plus constraint line | Keeps relationships clear |
| Multiple requirements or deliverables | Markdown sections and bullets | Efficient and readable |
| Long but one-shot task | Compact Markdown | XML adds control without a staged benefit |
| Staged research or build workflow | Shallow XML with `active_stage` | Enforces boundaries and prevents premature work |
| Reusable context plus changing step | Stable XML prefix plus small active-stage block | Supports reuse and consistent control |
| Strict machine-consumed output | Required JSON/XML schema | Use only when the consumer requires parsing |
| Verbatim editing, translation, legal text, code, or logs | Preserve original blocks | Rewriting can corrupt evidence or meaning |

Length is a signal, not the deciding rule. A long single task can remain Markdown; a short but stateful workflow can justify XML.

## Compact Markdown pattern

```text
Task: <single objective>

Scope:
- <required topic>
- <required topic>

Constraints:
- <limit or exclusion>

Deliver:
- <output>

Answer in <language> for <audience>.
```

## Shallow XML pattern

```xml
<project>
Reusable context.
</project>

<active_stage id="1">
  <task>Current objective.</task>
  <deliver>Required outputs.</deliver>
  <exclude>Work reserved for later stages.</exclude>
</active_stage>

<rule>
Complete only active_stage.
</rule>
```

Do not repeat the full stage catalog in every call. Keep stable context identical when caching or reuse is available.

## Candidate policy

Generate candidates according to the task:

1. Always retain the original as the fidelity baseline.
2. Generate compact Turkish for substantial Turkish prompts.
3. Generate compact English when the text will be sent downstream and translation is safe.
4. Generate XML only when stage or boundary control exists.
5. Generate JSON only when a program must consume the result.

Avoid fixed replacement dictionaries. Tokenization depends on full substrings, encoding, punctuation, and context; replacing isolated words can increase tokens and reduce clarity.
