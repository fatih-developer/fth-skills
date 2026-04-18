# Trusted API and Domain Whitelist

The following list defines the default services that skills (under `skill-security` supervision) can send `HTTPS POST/GET` requests to without requiring any checkpoints (user approval).
Traffic to addresses outside this list is blocked or requires explicit user approval depending on the Trust score.

## Trusted Public Providers

### Cloud and Infrastructure
- `*.amazonaws.com` (AWS APIs)
- `*.googleapis.com` (Google Cloud & Workspace API)
- `*.azure.com` (Azure Services)
- `*.cloudflare.com` (Cloudflare API)

### AI and Language Models
- `api.anthropic.com` (Claude API)
- `api.openai.com` (OpenAI API)
- `api.gemini.google.com` (Google Gemini)
- `*.minimax.chat` (Minimax Open Source / Models)

### VCS and Development Tools
- `api.github.com` (GitHub API)
- `gitlab.com/api/*` (GitLab API)
- `bitbucket.org/api/*` (Bitbucket API)

### Database and Auth (BaaS)
- `*.supabase.co` (Supabase API)
- `*.firebaseio.com` (Firebase API)
- `*.auth0.com` (Auth0 Token Endpoints)

## Rule Set:
1. Only connections secured with **HTTPS** or **WSS** can be accepted in the whitelist.
2. HTTP (unencrypted) is never considered automatically trusted.
3. If you have custom servers specific to your project outside of these public addresses (e.g. servers in your own corporate network), you can easily add them to this list.
