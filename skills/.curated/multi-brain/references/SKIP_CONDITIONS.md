# Skip Conditions

Decision matrix for when to bypass the multi-brain brainstorm process.

---

## Skip — Respond Directly

| Condition | Example |
|-----------|---------|
| Single factual answer | "How do I reverse a string in Python?" |
| User explicitly requests brevity | "Just tell me quickly…" |
| Simple transformation task | Translation, reformatting, spell-check |
| User has already decided | "I chose Option A. Implement it." |
| Trivial configuration | "Add this env variable" |
| Follow-up on a previous brainstorm | User said "go with B" after a prior session |

## Use Brainstorm

| Condition | Example |
|-----------|---------|
| Multiple valid approaches exist | "How should I structure this API?" |
| Decision has significant consequences | "Which database should I use?" |
| Request involves trade-offs | "Monorepo or polyrepo?" |
| Analysis or research is needed | "Compare these frameworks" |
| Complex implementation | "Build a notification system" |
| Strategy or planning | "How should I approach this migration?" |
| Ambiguity in requirements | "I need something fast and flexible" |

## Edge Cases

- **"Implement X"** without specifying approach → **Use brainstorm** (multiple architectures possible).
- **"Implement X using Y"** with specific approach → **Skip** (user has decided).
- **"What do you think about X?"** → **Use brainstorm** (opinion with reasoning requested).
- **Quick question during active implementation** → **Skip** (maintain flow, don't interrupt with 3 perspectives on a variable name).
