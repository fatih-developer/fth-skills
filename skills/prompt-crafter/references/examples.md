# Examples

## Example 1: System Prompt For A Coding Agent

Request:

```text
Create a system prompt for a coding agent that should inspect a repo, make minimal edits, run targeted validation, and summarize risks clearly.
```

Expected shape:

- role
- operating rules
- edit boundaries
- validation expectations
- final system prompt

## Example 2: Prompt Optimization

Request:

```text
Improve this prompt for Claude Code: "fix my app and make it production ready"
```

Expected shape:

- weaknesses
- revised coding prompt
- assumptions
- optional follow-up questions

## Example 3: Agent Spec

Request:

```text
Design an agent prompt for a support bot that can answer billing questions, use internal knowledge tools, and escalate risky issues to a human.
```

Expected shape:

- agent role
- allowed tools
- escalation rules
- output contract
- final agent prompt

## Example 4: MCP-Oriented Package

Request:

```text
Create an MCP-style prompt package for a research assistant that can search documents, summarize findings, and require approval before sending emails.
```

Expected shape:

- system prompt guidance
- tool description guidance
- approval policy
- workflow rules
- config scaffold
