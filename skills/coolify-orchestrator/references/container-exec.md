# Container Exec / SSH Fallback

## When To Use

Situations where Coolify API is insufficient:
- Editing a file inside a container (config, .env, cert)
- Reading application logs as files (disk log, not stdout)
- Clearing Bun/node_modules cache
- Running database migration manually
- In-container process debugging

## Access Strategy (Try in order)

### Strategy 1: Coolify Web Terminal (Without MCP, easiest)

Coolify Dashboard → Application/Service → "Terminal" tab → select container → enter command.

If this is insufficient or automation is needed, proceed to Strategy 2.

### Strategy 2: SSH + Docker Exec

```bash
# 1. Connect to server
ssh -i ~/.ssh/coolify_key user@coolify-server-ip

# 2. List running containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 3. Find the relevant container (by service name)
docker ps | grep <service-name>

# 4. Enter container
docker exec -it <container-name> sh
# If bash exists:
docker exec -it <container-name> bash
# For Bun container:
docker exec -it <container-name> /bin/sh
```

### How to find container name?

Coolify generally generates container names like this:
- `<project-name>-<service-name>-1`
- `coolify-<uuid>-<service>-1`

```bash
# Search by UUID
docker ps | grep <coolify-app-uuid>

# Search by service name
docker ps | grep -i "acme-api"
```

---

## Common In-Container Operations

### File Viewing and Editing

```bash
# Read config file
docker exec <container> cat /app/.env

# Edit file (with vi)
docker exec -it <container> vi /app/config.json

# Replace line with sed (doesn't require interactive session)
docker exec <container> \
  sed -i 's/OLD_VALUE/NEW_VALUE/g' /app/config.json
```

### Clearing Bun Cache

```bash
docker exec <container> bun pm cache rm

# Delete node_modules and reinstall
docker exec <container> sh -c "rm -rf node_modules && bun install"
```

### Database Migration

```bash
# Drizzle migration
docker exec <container> bunx drizzle-kit push

# Or migration script
docker exec <container> bun run db:migrate
```

### Reading Log File

```bash
# Container log (stdout/stderr)
docker logs <container> --tail 200 -f

# Log file on disk
docker exec <container> tail -f /var/log/app/error.log
```

### Process and Resource Checking

```bash
# CPU/Memory usage
docker stats <container> --no-stream

# In-container processes
docker exec <container> ps aux

# Check listening ports
docker exec <container> ss -tlnp
```

---

## Coolify Bun/Node Application: File Paths

| Content | Path |
|--------|-----|
| Application code | `/app/` |
| node_modules | `/app/node_modules/` |
| .env file | `/app/.env` (if exists) |
| Bun binary | `/usr/local/bin/bun` |
| Build output | `/app/dist/` |

## Coolify Next.js: File Paths

| Content | Path |
|--------|-----|
| Application | `/app/` |
| .next build | `/app/.next/` |
| Static files | `/app/public/` |

---

## Copying Files from Outside the Container

```bash
# Copy from container to server
docker cp <container>:/app/config.json /tmp/config.json

# Edit
nano /tmp/config.json

# Copy back
docker cp /tmp/config.json <container>:/app/config.json

# Application can reload if restart is not required
# If needed:
docker restart <container>
# or via Coolify API:
curl -X POST -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

---

## If No SSH Access to Server Available

Some operations can be performed via Coolify's API:

```bash
# Application logs (stdout)
curl -s \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/logs?lines=500"

# Service restart
curl -s -X POST \
  -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
  "$COOLIFY_BASE_URL/api/v1/applications/$APP_UUID/restart"
```

SSH is required for file editing. If there is no SSH access:
1. Tell the user to use the Coolify web terminal
2. Or pass config via env var (environment-based config instead of file)

---

## Post-Operation

Checklist after an in-container change:

```
[ ] Change applied correctly (verify with cat)
[ ] Service restarted (if needed)
[ ] Health check passed
[ ] No errors in log
```

If it can be reloaded without requiring a restart (e.g., Hono reload signal):
```bash
docker exec <container> kill -HUP 1  # Graceful reload with SIGHUP
```
