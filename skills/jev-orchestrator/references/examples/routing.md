# Example: Model / Tool / Agent Routing

Input:

```text
Compare the latest API pricing for these providers and update our cost model.
```

Possible independent Jev judgments:

```text
Choice: task class
- deterministic
- research
- coding
- writing
- mixed

Noul: requires current web research?
Noul: requires repository modification?
Noul: requires strong reasoning?
```

Batch independent judgments when supported.

Then deterministic orchestration maps signals to actual tools/models/agents.
