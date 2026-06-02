# RAG Patterns

Use these patterns when the prompt depends on retrieved context.

## Retrieval First

Use when the system should ground the answer in external or indexed material before generating.

Rules:

- search before guessing
- cite or name the source set when possible
- distinguish retrieved facts from inference
- say when retrieval was insufficient

## Grounded Generation

Use when the model must write only from the provided materials.

Rules:

- prioritize source fidelity over creativity
- refuse to invent unsupported details
- summarize conflicts explicitly
- mark unknowns rather than smoothing them over

## Retrieval-Aware Output Contract

Good retrieval prompts often specify:

- what to retrieve
- how many sources to use
- what to do with conflicting evidence
- how to report uncertainty
- what to do if no relevant source is found
