# Trust Matrix — Authorization & Confidence Levels

## Complete Authorization Map

Defines which operations are allowed, which require checkpoints, and which are forbidden for each confidence tier.

---

## TRUSTED (80-100)

```
FILESYSTEM
  ✓  Read          : free within defined scope
  ✓  Write         : free within defined scope
  ⚠️  Delete        : checkpoint (irreversible)
  ✓  Execute       : whitelisted commands only
  🚫 System dirs   : /etc /sys /proc — forbidden

NETWORK
  ✓  HTTPS GET     : whitelisted domains
  ✓  HTTPS POST    : whitelisted domains
  ✓  WebSocket     : whitelisted domains
  ⚠️  New domain    : approval on first use
  🚫 HTTP (clear)  : forbidden
  🚫 Raw socket    : forbidden

EXECUTION
  ✓  Bash (allowed): safe commands only
  ✓  Python/Node   : inside sandbox
  ⚠️  New process   : checkpoint
  🚫 eval/exec     : forbidden
  🚫 System service: forbidden

SKILL CHAIN
  ✓  Can trigger 60+ trust skills
  ⚠️  40-59 trust   : checkpoint
  🚫 0-39 trust    : cannot trigger

DATA
  ✓  Read user data
  ✓  Write to output
  ⚠️  Process PII   : masking mandatory
  🚫 3rd party PII : forbidden (no sharing)
```

---

## NORMAL (60-79)

```
FILESYSTEM
  ✓  Read          : working directory + tmp
  ⚠️  Write         : /tmp and project output dir only
  ⚠️  Delete        : checkpoint + rollback plan needed
  🚫 Execute       : strictly forbidden

NETWORK
  ✓  HTTPS GET     : safe domains only
  ⚠️  HTTPS POST    : checkpoint on payload logic
  🚫 WebSocket     : forbidden
  🚫 HTTP (clear)  : forbidden
  🚫 Raw socket    : forbidden

EXECUTION
  ✓  Python/Node   : strictly inside sandbox, no network
  🚫 Bash          : forbidden
  🚫 eval/exec     : forbidden

SKILL CHAIN
  ✓  Can trigger 80+ trust skills
  ⚠️  60-79 trust   : checkpoint
  🚫 0-59 trust    : cannot trigger

DATA
  ✓  Read non-sensitive data
  ⚠️  Write         : draft outputs only
  🚫 PII           : forbidden to read or touch
```

---

## SUSPICIOUS (0-59)

All operations are forbidden except requesting review from the user via the orchestrator.
