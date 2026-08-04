---
name: turkish-prompt-compiler
description: Analyze, measure, and optimize substantial Turkish prompts without losing intent, constraints, terminology, or protected content. Use when the user explicitly asks for Turkish prompt token analysis, compression, translation, restructuring, or optimization, or when a long Turkish instruction will be forwarded to another model, API, agent, or repeated workflow. Do not use for ordinary Turkish conversation, short requests handled directly, or verbatim editing unless optimization is explicitly requested.
---

# Turkish Prompt Compiler

Optimize for downstream token efficiency and execution reliability. Do not treat English translation, Markdown, XML, or brevity as goals by themselves.

## Apply the correct boundary

- Recognize that the current user message has already consumed input tokens. Never claim that rewriting it reduces the current call's input usage.
- Optimize only text that will be reused, forwarded, stored as a prompt, or explicitly analyzed.
- Include the optimizer's own billable call when estimating net savings.
- Treat token counts as model- and encoding-specific. Never present character counts or estimates as exact token counts.
- Preserve the user's requested response language independently from the prompt's internal language.

## Run the workflow

1. Identify the target model or encoding, reuse count, destination, required output language, and whether the prompt is one-shot or staged.
2. Extract a semantic contract:
   - primary task;
   - required coverage;
   - constraints and exclusions;
   - deliverables;
   - named entities and terminology;
   - output language, format, depth, and audience.
3. Protect content that must remain exact:
   - code, SQL, commands, logs, URLs, file paths, JSON/XML, identifiers;
   - names, dates, numbers, units, thresholds, quotations, citations;
   - negations and scope terms such as `değil`, `hariç`, `yalnızca`, `en az`, and `en fazla`;
   - domain terms whose Turkish spelling carries meaning.
4. Select a structure using [structure-selection.md](references/structure-selection.md).
5. Generate only relevant candidates:
   - compact Turkish;
   - compact English control language with Turkish proper nouns and domain terms preserved;
   - shallow XML only for staged execution, scope boundaries, or machine-controlled workflows.
6. Measure the original and candidates with the target model's tokenizer. Use `scripts/count_tokens.cjs` when `tiktoken` is available.
7. Reject any candidate that changes the semantic contract, even when it is shorter.
8. Prefer the shortest surviving candidate only when the reduction is meaningful:
   - below 10%: retain the clearer version;
   - 10–20%: optimize only if fidelity is unambiguous;
   - above 20%: use the shorter candidate after validation.
9. Report input savings separately from expected output usage. Flag prompts whose requested output dominates total cost.

## Choose the prompt language

- Keep short prompts in Turkish; translation overhead and review risk usually outweigh savings.
- For long downstream prompts, compare compact Turkish against compact English rather than assuming English is cheaper.
- Preserve Turkish names and specialist terms when translation could alter retrieval, citation, legal meaning, or historical identity.
- Add one concise instruction such as `Answer in Turkish` when using English control language.
- Avoid word-by-word Turkish-English replacement. Rewrite the whole instruction coherently.

## Use XML selectively

- Use shallow XML when the workflow has an active stage, explicit inclusions/exclusions, reusable project context, or automated parsing.
- Keep the hierarchy flat. Prefer a few meaningful tags such as `<task>`, `<coverage>`, `<active_stage>`, `<deliver>`, `<exclude>`, and `<rule>`.
- Do not wrap every bullet or sentence in a tag.
- Do not use XML for a simple one-shot request solely because it is long.
- Compare equivalent plain and XML candidates. Attribute savings from reduced scope separately from XML tag overhead.
- For staged work, keep stable project context reusable and change only `<active_stage>`.

## Validate fidelity

Before selecting a candidate, verify all of the following:

- Every required topic appears.
- Every deliverable appears.
- Numbers, names, technologies, sources, regions, and alternatives remain intact.
- Optional preferences have not become requirements, or vice versa.
- No negation, exception, or scope boundary changed.
- The response language and audience remain explicit.
- Compression has not introduced ambiguous shorthand.

If any check fails, repair the candidate and recount it. If exact tokenizer access is unavailable, label counts as estimates or omit them; never fabricate precision.

## Calculate savings

Use:

```text
input_saving_rate = 1 - optimized_tokens / original_tokens
```

For repeated downstream use:

```text
net_tokens_saved =
  reuse_count * (original_tokens - optimized_tokens)
  - optimizer_billable_tokens
```

Do not claim total-call savings without considering output tokens:

```text
total_saving_rate =
  (original_input - optimized_input)
  / (original_input + expected_output)
```

## Present results

When the user asks for analysis, return:

1. A table containing original and candidate token counts by encoding.
2. Savings percentages.
3. The recommended optimized prompt.
4. A brief fidelity note.
5. A warning when output scope is the larger cost driver.

When the user asks only for an optimized prompt, return the optimized prompt without exposing intermediate candidates unless needed.

When optimizing silently for a downstream call, forward only the selected candidate and retain the semantic contract for validation.

## Token counter

Run:

```bash
node scripts/count_tokens.cjs --encoding o200k_base --file prompt.txt
node scripts/count_tokens.cjs --model <target-model> --file original.txt --file optimized.txt
```

The script emits JSON with character and token counts. If the installed `tiktoken` package does not recognize a model, use the explicitly verified encoding instead of guessing.
