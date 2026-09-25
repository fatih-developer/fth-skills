# Example: Classification

Input:

```text
I was charged twice this month and need the duplicate payment refunded.
```

Use Jev Choice:

```text
Which support route best matches this request?
- billing
- technical
- account
- security
- general
- no_match
```

Runtime:

```text
request -> Jev Choice -> billing -> code routes to billing workflow
```

Do not use a generative LLM merely to return the label as JSON when Jev can produce the typed decision directly.
