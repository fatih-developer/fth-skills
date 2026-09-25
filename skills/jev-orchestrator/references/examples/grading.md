# Example: Semantic Grading

Expected concept:

```text
MVCC lets transactions observe appropriate row versions/snapshots and reduces conventional reader/writer blocking.
```

User answer:

```text
Readers can see different row versions without blocking writers.
```

Possible Choice:

```text
How complete is the answer?
- incorrect
- partial
- correct
- fully_correct
```

Atomic concept checks can also use Noul:

```text
Does the answer express multiple row versions?
Does it express reduced reader/writer blocking?
Does it express snapshot/transaction visibility?
```

Application code maps the semantic result into its own grading/scheduling system.
