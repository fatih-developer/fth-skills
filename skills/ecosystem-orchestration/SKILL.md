---
name: ecosystem-orchestration
description: Comprehensive map for multi-brain, orchestration, and agent governance. Triggers when users ask to "view the orchestration ecosystem", "how do agents work together?", "multi-brain workflows", or "give agents access".
---

# 🤖 Orchestration & Agentic Ecosystem

Welcome to the `orchestration` domain ecosystem. Unlike typical domains (which focus on specific tech stacks like frontend or databases), this meta-ecosystem defines the rules, workflows, and connectivity for **how AI autonomous agents interact, plan, recover from errors, and evaluate themselves and each other.**

> **For Orchestrator Agents (`task-decomposer`, `parallel-planner`):**
> This document is your internal operating manual. Use these workflows when structuring complex reasoning tasks, coordinating multiple AI models, or building secure entry points for external agentic integrations.

---

## 🔄 Standard Workflows & Handoffs

### 1. The Agent Connectivity Flow (The Foundation)

When the user asks to "integrate an LLM bot", "give an external agent access", or "design an AI pipeline into the app":

1. **`@claw-integration-design` -> (MANDATORY)** Designs the API endpoints, sets up `{action}:{resource}` OAuth scopes, and builds the generic `tools.json` manifest. **(This must always be the first step for agent connectivity).**
2. `@tool-selector` -> Analyzes the available tooling landscape (APIs, generic scripts) and selects the optimal set of actions for the incoming agent.
3. `@context-compressor` -> Steps in when agents retrieve massive payloads (logs, raw DB dumps) to compress the context window before it overwhelms the LLM.

### 2. Task Orchestration & Execution Flow

When given a large, ambiguous objective (e.g., "build an app", "migrate the server"):

1. `@task-decomposer` -> Breaks the massive goal into a step-by-step dependency graph.
2. `@parallel-planner` -> Analyzes the decomposed steps to find where tasks can be run concurrently (saving time and tokens).
3. `@memory-ledger` -> Used consistently throughout execution to maintain state across different sub-agents.
4. `@error-recovery` -> Automatically takes over if an executed step fails (retries, attempts alternate tools, or safely escalates to a human).

### 3. Multi-Brain (Consensus & Quality) Flow

When the user asks to "find the best approach", "debate these two libraries", or "give me a robust solution":

1. _Choose the synthesis model based on user intent:_
   - `@multi-brain` -> General 3-perspective synthesis.
   - `@multi-brain-experts` -> Specialized perspective synthesis based on strict domain personas (e.g., Security vs UX).
   - `@multi-brain-debate` -> Used when two distinct choices clash; forces a 2-round adversarial debate.
2. `@assumption-checker` -> Runs parallel to validate if the underlying facts driving the perspectives are hallucinated or real.
3. `@output-critic` -> Acts as the final tollgate to score the proposed synthesis before showing it to the user. (For advanced scoring structures, `@multi-brain-score` can be used).

### 4. Safety & Review Flow

When autonomous agents are operating on sensitive codebases or production databases:

1. `@checkpoint-guardian` -> A mandatory tollgate activated right before any destructive steps (e.g., Drop Table, Push to Main) are executed.
2. `@agent-reviewer` -> An oversight entity that retrospectively audits what the execution agents did, looking for logic holes or skipped steps.

---

## 🧠 Core Philosophy

Agentic orchestration is about **reliability, oversight, and fallback mechanisms**. Unlike standard script execution, agents can hallucinate or fail unexpectedly. Every skill in this ecosystem is designed to bound agent behavior within safe limits (`claw-integration`, `checkpoint-guardian`), ensure high-quality reasoning (`multi-brain`, `critic`), and provide resilient recovery (`error-recovery`). Never trust a single "one-shot" output for a complex scenario without decomposition and review.

---

## 🚀 Installation & Orchestration Instructions

As an AI Agent reading this ecosystem file, you must **actively guide** the user to install the missing skills for the selected workflow.

For example, if the user needs the **Task Orchestration & Execution Flow**, execute or instruct the user to execute:

```bash
skills install task-decomposer
skills install parallel-planner
skills install memory-ledger
```

**Execution Rule:**
Do not attempt to perform the tasks of these skills yourself. Your job is to install them and hand off the execution to the appropriate skill, or instruct the user to trigger the newly installed skills in order.
