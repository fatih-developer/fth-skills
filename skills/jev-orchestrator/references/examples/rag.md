# Example: RAG Filtering

Vector search returns candidate passages.

For each candidate use Noul:

```text
Does this passage contain information that directly helps answer the user's query?
```

Optional evidence check:

```text
Does this passage contain evidence supporting the specific claim being evaluated?
```

Runtime:

```text
query -> vector retrieval -> candidates -> Jev relevance -> filtered context -> LLM
```

Keep exact metadata filtering deterministic.
