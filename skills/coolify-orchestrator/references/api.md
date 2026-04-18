# Coolify REST API Reference

For direct API use when MCP is not installed.

Base URL: `$COOLIFY_BASE_URL/api/v1`
Auth: `Authorization: Bearer $COOLIFY_ACCESS_TOKEN`

## Quick Reference

### General

| Operation | Method | Endpoint |
|-------|--------|----------|
| API version | GET | `/version` |
| Health check | GET | `/healthcheck` |

### Servers

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/servers` |
| Detail | GET | `/servers/{uuid}` |
| Resources | GET | `/servers/{uuid}/resources` |
| Domains | GET | `/servers/{uuid}/domains` |
| Validate | POST | `/servers/{uuid}/validate` |

### Projects

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/projects` |
| Detail | GET | `/projects/{uuid}` |
| Create | POST | `/projects` |
| Update | PATCH | `/projects/{uuid}` |
| Delete | DELETE | `/projects/{uuid}` |

### Environments

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/projects/{uuid}/environments` |
| Detail | GET | `/projects/{uuid}/environments/{name}` |
| Create | POST | `/environments` |
| Delete | DELETE | `/environments/{uuid}` |

### Applications

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/applications` |
| Detail | GET | `/applications/{uuid}` |
| Create | POST | `/applications` |
| Update | PATCH | `/applications/{uuid}` |
| Delete | DELETE | `/applications/{uuid}` |
| Logs | GET | `/applications/{uuid}/logs` |
| Start | POST | `/applications/{uuid}/start` |
| Stop | POST | `/applications/{uuid}/stop` |
| Restart | POST | `/applications/{uuid}/restart` |
| Deploy | POST | `/applications/{uuid}/deploy` |

### Env Vars (Application)

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/applications/{uuid}/envs` |
| Add | POST | `/applications/{uuid}/envs` |
| Update | PATCH | `/applications/{uuid}/envs/{env_uuid}` |
| Delete | DELETE | `/applications/{uuid}/envs/{env_uuid}` |
| Bulk update | PUT | `/applications/{uuid}/envs/bulk` |

### Databases

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/databases` |
| Detail | GET | `/databases/{uuid}` |
| Create | POST | `/databases` |
| Delete | DELETE | `/databases/{uuid}` |
| Start | POST | `/databases/{uuid}/start` |
| Stop | POST | `/databases/{uuid}/stop` |
| Restart | POST | `/databases/{uuid}/restart` |

Database type values: `standalone-postgresql`, `standalone-mysql`, `standalone-mariadb`,
`standalone-mongodb`, `standalone-redis`, `standalone-keydb`, `standalone-clickhouse`,
`standalone-dragonfly`

### Services

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/services` |
| Detail | GET | `/services/{uuid}` |
| Create | POST | `/services` |
| Delete | DELETE | `/services/{uuid}` |
| Start | POST | `/services/{uuid}/start` |
| Stop | POST | `/services/{uuid}/stop` |
| Restart | POST | `/services/{uuid}/restart` |

### Deployments

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/deployments` |
| Detail | GET | `/deployments/{uuid}` |
| Logs | GET | `/deployments/{uuid}/logs` |
| Cancel | POST | `/deployments/{uuid}/cancel` |
| List for application | GET | `/applications/{uuid}/deployments` |

### Private Keys

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/security/keys` |
| Detail | GET | `/security/keys/{uuid}` |
| Create | POST | `/security/keys` |
| Update | PATCH | `/security/keys/{uuid}` |
| Delete | DELETE | `/security/keys/{uuid}` |

### Teams

| Operation | Method | Endpoint |
|-------|--------|----------|
| List | GET | `/teams` |
| Detail | GET | `/teams/{id}` |
| Members | GET | `/teams/{id}/members` |
| Current team | GET | `/teams/current` |

---

## Basic curl Wrapper

Shell function to avoid repetitive typing:

```bash
coolify() {
  local METHOD="${1:-GET}"
  local ENDPOINT="$2"
  local DATA="${3:-}"
  
  ARGS=(-s -X "$METHOD" \
    -H "Authorization: Bearer $COOLIFY_ACCESS_TOKEN" \
    -H "Content-Type: application/json")
  
  [ -n "$DATA" ] && ARGS+=(-d "$DATA")
  
  curl "${ARGS[@]}" "$COOLIFY_BASE_URL/api/v1$ENDPOINT"
}

# Usage:
coolify GET /applications | jq '.[] | {uuid, name, status}'
coolify POST "/applications/$APP_UUID/restart"
coolify POST /projects '{"name":"my-project"}'
```

## Error Codes

| Code | Meaning | Solution |
|-----|-------|-------|
| 401 | Invalid token | Check token, regenerate |
| 403 | Insufficient permission | Check token permission level |
| 404 | Resource not found | Verify UUID |
| 422 | Validation error | Check request body |
| 500 | Coolify server error | Check Coolify logs |

## Useful jq Filters

```bash
# List all applications (uuid + name + status)
curl ... /applications | jq '.[] | {uuid, name, status: .status}'

# Find unhealthy applications
curl ... /applications | jq '.[] | select(.status | contains("unhealthy"))'

# Find application with a specific name
curl ... /applications | jq '.[] | select(.name == "my-app")'

# Get DB connection URL
curl ... /databases/$DB_UUID | jq '{internal: .internal_db_url, external: .external_db_url}'
```
