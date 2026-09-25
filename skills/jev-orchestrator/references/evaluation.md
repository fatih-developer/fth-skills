# Evaluation

A Jev integration is successful only when it improves the real workflow.

## Dataset

Use representative examples including:
- normal cases;
- ambiguous cases;
- edge cases;
- class imbalance;
- adversarial/misleading text where relevant;
- multilingual cases when applicable.

## Metrics

Classification/routing:
- accuracy
- per-class precision/recall
- confusion matrix
- wrong-route rate

Binary judgments:
- precision/recall
- false-positive rate
- false-negative rate
- calibration

Grading:
- agreement with human labels
- adjacent-grade errors
- severe overgrade/undergrade rates

Operational:
- P50/P95 latency
- cost per decision
- fallback rate
- strong-model call reduction
- human-review rate
- override rate

## Baselines

Compare against the current workflow, such as:
- generative LLM prompt-and-parse;
- rules-only logic;
- embedding similarity;
- human routing;
- production pipeline.

## Version data

Record when possible:

```text
jev_model_version
question_version
policy_version
timestamp
```

## Thresholds

Do not choose confidence thresholds by intuition alone. Evaluate coverage, error rate, fallback rate, cost, latency, and business consequence.
