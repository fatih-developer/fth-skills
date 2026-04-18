# Turborepo + Coolify Deploy Playbook

## Sorunun Kökü

Turborepo monorepo'larda Coolify Docker build'i başarısız olur çünkü:
- Docker build context monorepo root'u
- Ama uygulama subdirectory'ye işaret ediyor
- Shared packages (`@myapp/ui`, `@myapp/shared`, `@myapp/db`) build edilmeden önce
  uygulama bundle'ı onları import etmeye çalışıyor

## Doğru Dockerfile Yapısı

### Pattern 1: Turbo Prune (Önerilen)

```dockerfile
FROM oven/bun:1 AS base

# 1. Turbo prune — sadece bu app için gerekli package'ları kopyala
FROM base AS pruner
WORKDIR /app
RUN bunx turbo@latest -- --version  # veya global turbo
COPY . .
RUN bunx turbo prune --scope=@myapp/api --docker

# 2. Dependency install
FROM base AS installer
WORKDIR /app
COPY --from=pruner /app/out/json/ .
COPY --from=pruner /app/out/bun.lockb ./bun.lockb
RUN bun install --frozen-lockfile

# 3. Build — shared packages önce, app sonra
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

### Pattern 2: Explicit Build Order (Turbo olmadan)

```dockerfile
FROM oven/bun:1 AS base
WORKDIR /app

# Tüm package.json'ları kopyala (layer cache için)
COPY package.json bun.lockb turbo.json ./
COPY apps/api/package.json ./apps/api/
COPY packages/shared/package.json ./packages/shared/
COPY packages/db/package.json ./packages/db/

RUN bun install --frozen-lockfile

# Shared packages ÖNCE build et
COPY packages/shared ./packages/shared
RUN cd packages/shared && bun run build

COPY packages/db ./packages/db
RUN cd packages/db && bun run build

# Ana app en son
COPY apps/api ./apps/api
RUN cd apps/api && bun run build

CMD ["bun", "apps/api/dist/index.js"]
```

## Coolify'da Docker Build Context Ayarı

Coolify Dashboard → Application → Configuration:

```
Base Directory: /          ← monorepo root (önemli!)
Dockerfile Location: apps/api/Dockerfile
Build Context: /           ← yine root
```

Eğer Coolify subdirectory'yi build context olarak kullanıyorsa shared package'lar görünmez.

## Sık Karşılaşılan Hatalar ve Çözümleri

### Hata: `Cannot find module '@myapp/shared'`
**Neden:** Shared package build edilmemiş veya node_modules'a symlink yok.
**Çözüm:** Pattern 1 veya 2'yi uygula. `turbo build --filter=@myapp/api...` trailing `...` önemli — dependency'leri de build eder.

### Hata: `tsconfig.json not found` veya `paths` resolve edilemiyor
**Neden:** TypeScript path alias'lar (`@shared/*`) Dockerfile içinde çözülemiyor.
**Çözüm:**
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
Ve Dockerfile'da `tsconfig.base.json`'ı da kopyala.

### Hata: `bun install` sonrası workspace symlink'ler yok
**Neden:** `bun install --frozen-lockfile` workspace package'ları `node_modules` altına link etmiyor.
**Çözüm:**
```dockerfile
RUN bun install --frozen-lockfile
# Workspace symlink'leri kontrol et
RUN ls -la node_modules/@myapp/
```
Eğer yoksa: `bun install` (frozen olmadan) veya Pattern 1'e geç.

### Hata: Coolify her deploy'da full rebuild yapıyor, cache yok
**Çözüm:** Dockerfile'ın başına layer cache buster ekle:
```dockerfile
ARG BUILDKIT_INLINE_CACHE=1
```
Ve Coolify → Application → Build Cache: Enabled.

## Verify: Başarılı Build Göstergesi

```bash
# Log'larda şunları ara
grep -E "(successfully built|BUILD SUCCESS|✓ Built)" build.log

# Veya image'ı local test et
docker build -f apps/api/Dockerfile . --target runner -t test-build
docker run --rm test-build bun --version
```

## turbo.json Pipeline Yapısı

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],  // ^ = dependency'leri önce build et
      "outputs": ["dist/**", ".next/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

`"^build"` kritik — Turborepo'ya dependency graph'ı takip etmesini söyler.
