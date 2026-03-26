# API Whitelist

This file defines the trusted external endpoints that skills may call without triggering a K3/K4 escalation.

## Always-Allowed Domains

```text
api.openai.com
api.anthropic.com
api.github.com
registry.npmjs.org
pypi.org
hub.docker.com
```

## Conditionally-Allowed (Requires skill-level declaration)

```text
*.supabase.co           # Supabase hosted databases
*.googleapis.com        # Google Cloud APIs
*.amazonaws.com         # AWS APIs
*.azure.com             # Microsoft Azure APIs
api.stripe.com          # Payment processing (high-risk — always checkpoint)
```

## Always-Blocked (Blacklist)

```text
*.onion                 # Tor hidden services
*.ru (dynamic content)  # High-risk TLD for C2
pastebin.com            # Common malware staging host
requestbin.com          # Exfiltration risk
webhook.site            # Exfiltration risk
```

## Rules for Adding a New Domain

1. Justify the business need explicitly in SKILL.md
2. Must use HTTPS (no HTTP allowed)
3. SSL certificate must be valid (verify=True enforced)
4. Timeout must be declared (recommended: 30s max)
5. Response must be schema-validated before use
