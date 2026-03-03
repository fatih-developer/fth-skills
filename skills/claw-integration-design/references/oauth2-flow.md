# OAuth2 Integration Flow for Bot/Agent Access

This reference covers the recommended OAuth2 setup for third-party agent providers connecting to your application.

## When to Use OAuth2 vs API Keys

| Scenario                                            | Recommended Auth                 |
| --------------------------------------------------- | -------------------------------- |
| Internal bot / single organization                  | API Key (simpler)                |
| Third-party agent provider (e.g., OpenClaw, Zapier) | OAuth2 (standard)                |
| User grants an agent access to their own account    | OAuth2 Authorization Code + PKCE |

---

## Authorization Code Flow + PKCE (Recommended for Agents)

```
1. Bot redirects user to:
   GET /oauth/authorize
     ?response_type=code
     &client_id=<BOT_CLIENT_ID>
     &redirect_uri=<BOT_CALLBACK_URL>
     &scope=read:items write:captures
     &state=<RANDOM_STATE>
     &code_challenge=<PKCE_CHALLENGE>
     &code_challenge_method=S256

2. User logs in and approves scopes in your app's consent screen.

3. Your app redirects to:
   <BOT_CALLBACK_URL>?code=<AUTH_CODE>&state=<STATE>

4. Bot exchanges code for tokens:
   POST /oauth/token
     { grant_type: "authorization_code", code, redirect_uri, code_verifier }

5. Your app returns:
   { access_token, token_type: "bearer", expires_in: 3600, refresh_token }

6. Bot uses:
   Authorization: Bearer <access_token>
```

---

## Token Endpoints

### Issue Access Token

`POST /oauth/token`

```json
{
  "grant_type": "authorization_code",
  "code": "<auth_code>",
  "redirect_uri": "https://bot.example.com/callback",
  "client_id": "client_abc",
  "code_verifier": "<pkce_verifier>"
}
```

### Refresh Access Token

`POST /oauth/token`

```json
{
  "grant_type": "refresh_token",
  "refresh_token": "<refresh_token>",
  "client_id": "client_abc"
}
```

### Revoke Token

`POST /oauth/revoke`

```json
{ "token": "<access_token_or_refresh_token>" }
```

---

## Scope Consent Screen Guidelines

When presenting scopes to the user for approval, use clear human-readable descriptions:

| Scope            | User-facing label                                       |
| ---------------- | ------------------------------------------------------- |
| `read:items`     | View your tasks and notes                               |
| `write:captures` | Add items to your inbox (reviewed by you before saving) |
| `write:items`    | Create and edit tasks on your behalf                    |
| `write:links`    | Link records together                                   |
| `admin:audit`    | View action history                                     |

> Always list only the scopes the bot actually needs. Over-requesting scopes erodes user trust.

---

## Security Notes

- **PKCE is mandatory** — prevents authorization code interception attacks.
- **Short-lived access tokens** — 1 hour is the recommended default.
- **Rotate refresh tokens** on each use (refresh token rotation).
- **Revoke all tokens** when the user disconnects the bot integration from settings.
