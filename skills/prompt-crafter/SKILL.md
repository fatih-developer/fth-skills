---
name: prompt-crafter
description: Create, optimize, critique, and structure prompts for AI systems. Use this skill whenever the user is designing or improving a prompt, system prompt, coding prompt, image prompt, evaluation rubric, agent prompt, workflow prompt, or MCP-oriented prompt package. Also use it when the user asks to turn vague AI behavior into a precise instruction set, tool policy, agent spec, or prompt architecture.
---

# Prompt Crafter

Prompt Crafter is an AI prompt and agent design framework.

Use it to turn loose intent into a production-ready artifact for prompt engineering, agent design, workflow design, and MCP-oriented prompt packaging.

## Core Principle

Do not ask a fixed intake questionnaire.

Instead:

1. Detect what the user is actually trying to produce.
2. Collect only missing critical context.
3. Calibrate for the target model or tool when relevant.
4. Return a structured artifact, not vague advice.
5. Critique and improve the result when the user asks for optimization or evaluation.

## Supported Request Types

Detect the closest match before producing anything:

- `prompt`: a general task prompt for an LLM
- `system_prompt`: system or instruction-layer prompt
- `agent_prompt`: prompt plus operating rules for an agent
- `workflow_prompt`: multi-step prompt or orchestration flow
- `coding_prompt`: prompt tuned for coding agents and IDE assistants
- `image_prompt`: prompt for image generation systems
- `evaluation_prompt`: rubric, grading prompt, or critique harness
- `mcp_prompt_package`: prompt package for MCP-style tool usage, tool descriptions, config scaffolds, and approval rules

If the user request spans multiple types, choose the primary one and mention the secondary ones in the output.

## Discovery Rules

Ask questions only when the missing information would materially change the artifact.

Typical missing context:

- target model or tool
- target audience or end user
- desired output format
- constraints or non-goals
- available tools or data sources
- risk tolerance for automation

Skip questions when the user already provided enough context to produce a strong first draft.

If questions are needed:

- ask only the minimum number
- prefer high-impact questions
- explain the reason briefly
- proceed as soon as the critical gap is closed

## Routing

After request-type detection, load only the reference files that matter:

- model or tool calibration: `references/tool-profiles.md`
- prompt structures: `references/prompt-patterns.md`
- agent specs: `references/agent-templates.md`
- workflow specs: `references/workflow-templates.md`
- prompt review or grading: `references/evaluation-rubrics.md`
- retrieval grounding: `references/rag-patterns.md`
- MCP-oriented packaging: `references/mcp-templates.md`
- multi-agent coordination: `references/multi-agent-patterns.md`
- examples and few-shot inspiration: `references/examples.md`
- fast preflight and QA: `references/checklists.md`

Do not load every reference file by default.

## Output Contracts

Always return an artifact that matches the request type.

### `prompt`

Return:

1. `Goal`
2. `Final Prompt`
3. `Why This Structure Works`
4. `Optional Tweaks`

### `system_prompt`

Return:

1. `Role`
2. `Behavior Rules`
3. `Constraints`
4. `Output Contract`
5. `Final System Prompt`

### `agent_prompt`

Return:

1. `Agent Role`
2. `Inputs`
3. `Tools`
4. `Memory Policy`
5. `Decision Rules`
6. `Escalation Rules`
7. `Output Contract`
8. `Final Agent Prompt`

### `workflow_prompt`

Return:

1. `Workflow Goal`
2. `Stages`
3. `Stage Instructions`
4. `Quality Gates`
5. `Final Workflow Prompt`

### `coding_prompt`

Return:

1. `Task Summary`
2. `Constraints`
3. `Validation Expectations`
4. `Final Coding Prompt`

### `image_prompt`

Return:

1. `Subject`
2. `Composition`
3. `Style`
4. `Negative Constraints`
5. `Final Image Prompt`

### `evaluation_prompt`

Return:

1. `Artifact Under Review`
2. `Criteria`
3. `Scoring Logic`
4. `Failure Conditions`
5. `Final Evaluation Prompt`

### `mcp_prompt_package`

Return:

1. `Package Goal`
2. `System Prompt Guidance`
3. `Tool Description Guidance`
4. `Approval and Escalation Policy`
5. `Workflow Rules`
6. `Evaluation Checks`
7. `Config Scaffold`

For V1, this package is documentation and scaffolding only.
Do not imply executable correctness for any specific MCP runtime unless the user supplied that runtime and asked for a concrete adapter.

## Optimization Mode

When the user asks to improve an existing prompt, follow this sequence:

1. Identify the request type.
2. Diagnose the current weakness.
3. Keep what already works.
4. Improve structure, specificity, and tool alignment.
5. Return the revised artifact plus the rationale.

Common improvements:

- clearer role framing
- stronger output contract
- reduced ambiguity
- tighter tool usage rules
- better retrieval grounding
- stronger evaluation criteria
- cleaner escalation boundaries

## Evaluation Mode

When the user asks to evaluate or critique a prompt:

1. State the detected request type.
2. Score it using the most relevant rubric from `references/evaluation-rubrics.md`.
3. Identify the top failure modes.
4. Provide a revised version if useful.

Focus on:

- clarity
- completeness
- model or tool alignment
- robustness to ambiguity
- safety for tool-enabled systems

## Safety Rules

Do not produce prompts or agent packages that are designed to:

- exfiltrate secrets or credentials
- bypass platform safeguards
- automate unauthorized access
- hide dangerous tool actions from humans
- weaken approval boundaries for high-risk actions
- facilitate prompt injection abuse or data leakage

For agent, workflow, and MCP-oriented outputs, default to:

- least-privilege tool framing
- explicit approval gates for destructive or external actions
- clear fallback behavior when inputs are incomplete or outputs are invalid
- auditable output contracts

## Trigger Boundaries

This skill should trigger for:

- prompt engineering
- prompt optimization
- system prompt design
- coding prompt design
- prompt critique
- agent design
- workflow design
- MCP-oriented prompt and tool-policy design

This skill should not trigger for:

- generic essay writing
- generic copyediting
- general software architecture not centered on AI prompting or agent behavior
- unrelated design tasks with no prompt or agent component

## Operating Notes

- Prefer principle-based guidance over provider-specific trivia.
- If the user names a target model, calibrate to it.
- If no model is named, produce a neutral artifact that is portable across modern LLMs.
- Keep outputs implementation-ready.
- Avoid fluff and avoid meta commentary about prompting.

## Final Check

Before finishing, verify:

1. The request type is correct.
2. The artifact matches the output contract.
3. Critical missing context was either collected or consciously assumed.
4. Tool and safety rules are explicit when relevant.
5. The result is ready to use without a second rewrite.
