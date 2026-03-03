# Examples

## Example — Conversation History Compression

### Input (long)
```
User: Hi! I want to build a rate limiter in Python.
Assistant: Hi! Sure, I can help. Rate limiters can use several algorithms...
[... 40 messages, algorithm discussion, 3 different attempts ...]
User: OK, let's use sliding window.
Assistant: Great choice! Sliding window has these advantages...
User: Got it, thanks.
```

### Output (compressed)
```
CONTEXT COMPRESSOR
Type    : Conversation history
Before  : ~800 words
After   : ~220 words
Saving  : ~72% reduction

[CONVERSATION SUMMARY — 40 messages -> 5 items]
Context: Python rate limiter implementation
Decisions:
  - Sliding window algorithm chosen (token bucket and fixed window tried, rejected)
  - No external dependencies (pure Python)
  - Must be thread-safe
Current status: Algorithm chosen, implementation not started
Pending: FastAPI middleware vs standalone decorator — not decided
```
