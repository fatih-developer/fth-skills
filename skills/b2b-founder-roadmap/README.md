# b2b-founder-roadmap

An execution-oriented B2B founder skill for technical founders and solo
developers.

It guides a business through:

`Business Context → Problem → Research → Validation → Positioning → Offer →
Distribution → Sales → Metrics → Pricing → Retention → Growth`

The skill does not blindly move forward. It finds the current bottleneck,
executes the work it can, evaluates evidence, and uses `PASS / PARTIAL / FAIL`
stage gates.

## Install

Place the skill folder in the skills directory used by your agent environment.

Core file:

```text
b2b-founder-roadmap/
└── SKILL.md
```

Recommended project state:

```text
marketing/
└── ROADMAP_STATE.md
```

Copy `ROADMAP_STATE.template.md` into the project's `marketing/` directory when
initializing manually.

## Example usage

```text
$b2b-founder-roadmap start

APIHeart için B2B go-to-market sürecini başlat.
```

Continue later:

```text
$b2b-founder-roadmap continue
```

Inspect current position:

```text
$b2b-founder-roadmap status
```

Re-evaluate after major product/market changes:

```text
$b2b-founder-roadmap reassess
```

Restart only the current stage:

```text
$b2b-founder-roadmap restart-stage
```

## Design principles

- Customer first. Code second.
- Evidence over opinion.
- Payment/commitment over compliments.
- Outcome over features.
- One bottleneck at a time.
- Adaptive gates instead of universal vanity thresholds.
- GTM-aware funnels: product-led, founder-led, sales-led, or hybrid.
- Every meaningful stage leaves an artifact.
