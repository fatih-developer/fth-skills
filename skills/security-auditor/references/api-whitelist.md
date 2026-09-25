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

---

## Extended Catalog

The detailed entries below were merged from the former `skill-security` skill. They use the same tiers as the summary above; when an entry appears in both, the stricter tier wins.

The following list defines the default services that skills (under `security-auditor` supervision) can send `HTTPS POST/GET` requests to without requiring any checkpoints (user approval).
Traffic to addresses outside this list is blocked or requires explicit user approval depending on the Trust score.

### Trusted Public Providers

#### Cloud and Infrastructure
- `*.amazonaws.com` (AWS APIs)
- `*.googleapis.com` (Google Cloud & Workspace API)
- `*.azure.com` (Azure Services)
- `*.cloudflare.com` (Cloudflare API)

#### AI and Language Models
- `api.anthropic.com` (Claude API)
- `api.openai.com` (OpenAI API)
- `api.gemini.google.com` (Google Gemini)
- `*.minimax.chat` (Minimax Open Source / Models)

#### VCS and Development Tools
- `api.github.com` (GitHub API)
- `gitlab.com/api/*` (GitLab API)
- `bitbucket.org/api/*` (Bitbucket API)

#### Database and Auth (BaaS)
- `*.supabase.co` (Supabase API)
- `*.firebaseio.com` (Firebase API)
- `*.auth0.com` (Auth0 Token Endpoints)

### Rule Set:
1. Only connections secured with **HTTPS** or **WSS** can be accepted in the whitelist.
2. HTTP (unencrypted) is never considered automatically trusted.
3. If you have custom servers specific to your project outside of these public addresses (e.g. servers in your own corporate network), you can easily add them to this list.
