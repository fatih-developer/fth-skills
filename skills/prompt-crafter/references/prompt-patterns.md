# Prompt Patterns

Use these patterns as building blocks, not rigid templates.

## Standard Prompt

Best for straightforward generation tasks.

Template:

```text
Goal:
[what to produce]

Context:
[relevant background]

Constraints:
[scope, tone, exclusions]

Output:
[exact format]
```

## System Prompt

Best for durable behavior shaping.

Template:

```text
You are [role].

Your job is to:
- [responsibility 1]
- [responsibility 2]

Rules:
- [behavior rule]
- [safety or scope rule]

Output contract:
- [format or schema]
```

## Rewrite And Improve

Best for prompt optimization.

Template:

```text
Analyze the prompt below for ambiguity, missing constraints, and output weakness.
Preserve the original goal.
Return:
1. weaknesses
2. revised prompt
3. rationale
```

## Few-Shot Prompt

Best when output style or structure matters more than broad reasoning freedom.

Use:

- one to three examples
- examples that reflect the exact target style
- examples that show edge behavior if needed

## Structured Output Prompt

Best when the result feeds another system.

Template:

```text
Return the output in this exact structure:
[schema, fields, or headings]

If information is missing, say:
[fallback behavior]
```

## Tool-Enabled Prompt

Best for agents and MCP-oriented systems.

Template:

```text
Goal:
[task]

Available tools:
- [tool name]: [when to use]

Rules:
- do not use tools unless needed
- ask for approval before [high-risk action]
- if tool results conflict, explain uncertainty

Output:
[required format]
```

## Evaluation Prompt

Best for reviewing output quality.

Template:

```text
Evaluate the artifact against:
- clarity
- completeness
- correctness
- safety

Return:
1. score by criterion
2. strongest parts
3. highest-risk issues
4. improved version
```
