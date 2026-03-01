#!/usr/bin/env bash

echo "--- AŞAMA 1: Proje Keşfi ---"

echo "1. Genel yapı"
find . -maxdepth 3 -type f | grep -v node_modules | grep -v .git | grep -v dist | sort

echo "2. Dil ve framework tespiti"
find . -name "package.json" -not -path "*/node_modules/*" | head -5
find . -name "*.toml" -o -name "*.yaml" -o -name "*.yml" -o -name "requirements.txt" \
       -o -name "go.mod" -o -name "Cargo.toml" -o -name "pom.xml" | grep -v node_modules

echo "3. Satır sayısı ve dil dağılımı"
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" \
       -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.cs" \) \
       -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" \
  | xargs wc -l 2>/dev/null | sort -rn | head -30

echo "4. Git geçmişi (varsa)"
git log --oneline --since="3 months ago" | wc -l
git log --format='%an' | sort | uniq -c | sort -rn | head -5
git shortlog -sn --since="6 months ago" | head -5

echo "5. Bağımlılıklar"
cat package.json 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    deps = {**d.get('dependencies',{}), **d.get('devDependencies',{})}
    print(f'Toplam bağımlılık: {len(deps)}')
    for k,v in list(deps.items())[:20]: print(f'  {k}: {v}')
except Exception as e:
    pass
" 2>/dev/null

echo "6. Test dosyaları"
find . -type f \( -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" \) \
       -not -path "*/node_modules/*" | wc -l

echo "7. Ortam ve konfigürasyon"
ls -la .env* Dockerfile* docker-compose* 2>/dev/null
