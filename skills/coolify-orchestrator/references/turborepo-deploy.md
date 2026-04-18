# Turborepo + Coolify Deploy Playbook

## Root Cause

In Turborepo monorepos, Coolify Docker build fails because:
- Docker build context is the monorepo root
- But the application points to a subdirectory
- The application bundle tries to import shared packages (`@myapp/ui`, `@myapp/shared`, `@myapp/db`) before they are built

## Correct Dockerfile Structure

### Pattern 1: Turbo Prune (Recommended)

```dockerfile
FROM oven/bun:1 AS base

# 1. Turbo prune — copy only packages required for this app
FROM base AS pruner
WORKDIR /app
RUN bunx turbo@latest -- --version  # or global turbo
COPY . .
RUN bunx turbo prune --scope=@myapp/api --docker

# 2. Dependency install
FROM base AS installer
WORKDIR /app
COPY --from=pruner /app/out/json/ .
COPY --from=pruner /app/out/bun.lockb ./bun.lockb
RUN bun install --frozen-lockfile

# 3. Build — shared packages first, app next
FROM base AS builder
WORKDIR /app
COPY --from=installer /app/node_modules ./node_modules
COPY --from=pruner /app/out/full/ .
RUN bunx turbo build --filter=@myapp/api...

# 4. Runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/apps/api/dist ./dist
COPY --from=builder /app/apps/api/package.json .
CMD ["bun", "dist/index.js"]
```

### Pattern 2: Explicit Build Order (Without Turbo)

```dockerfile
FROM oven/bun:1 AS base
WORKDIR /app

# Copy all package.jsons (for layer cache)
COPY package.json bun.lockb turbo.json ./
COPY apps/api/package.json ./apps/api/
COPY packages/shared/package.json ./packages/shared/
COPY packages/db/package.json ./packages/db/

RUN bun install --frozen-lockfile

# Build shared packages FIRST
COPY packages/shared ./packages/shared
RUN cd packages/shared && bun run build

COPY packages/db ./packages/db
RUN cd packages/db && bun run build

# Main app last
COPY apps/api ./apps/api
RUN cd apps/api && bun run build

CMD ["bun", "apps/api/dist/index.js"]
```

## Docker Build Context Setting in Coolify

Coolify Dashboard → Application → Configuration:

```
Base Directory: /          ← monorepo root (important!)
Dockerfile Location: apps/api/Dockerfile
Build Context: /           ← again root
```

If Coolify uses the subdirectory as the build context, shared packages will not be visible.

## Common Errors and Solutions

### Error: `Cannot find module '@myapp/shared'`
**Cause:** Shared package is not built or there's no symlink to node_modules.
**Solution:** Apply Pattern 1 or 2. The trailing `...` in `turbo build --filter=@myapp/api...` is important — it also builds dependencies.

### Error: `tsconfig.json not found` or `paths` cannot be resolved
**Cause:** TypeScript path aliases (`@shared/*`) cannot be resolved inside Dockerfile.
**Solution:**
```json
// apps/api/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "paths": {
      "@myapp/shared": ["../../packages/shared/src/index.ts"]
    }
  }
}
```
And also copy `tsconfig.base.json` in the Dockerfile.

### Error: No workspace symlinks after `bun install`
**Cause:** `bun install --frozen-lockfile` doesn't link workspace packages under `node_modules`.
**Solution:**
```dockerfile
RUN bun install --frozen-lockfile
# Verify workspace symlinks
RUN ls -la node_modules/@myapp/
```
If not present: `bun install` (without frozen) or switch to Pattern 1.

### Error: Coolify does full rebuild on every deploy, no cache
**Solution:** Add layer cache buster at the top of the Dockerfile:
```dockerfile
ARG BUILDKIT_INLINE_CACHE=1
```
And Coolify → Application → Build Cache: Enabled.

## Verify: Successful Build Indicator

```bash
# Search for these in logs
grep -E "(successfully built|BUILD SUCCESS|✓ Built)" build.log

# Or locally test the image
docker build -f apps/api/Dockerfile . --target runner -t test-build
docker run --rm test-build bun --version
```

## turbo.json Pipeline Structure

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],  // ^ = build dependencies first
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

`"^build"` is critical — it tells Turborepo to follow the dependency graph.
