#!/usr/bin/env bash

echo "--- AŞAMA 2: Derin Analiz ---"

echo "### 2.1 Mimari Analiz"
# Klasör yapısı mantığı
find . -maxdepth 2 -type d | grep -v node_modules | grep -v .git | grep -v dist | sort

# Büyük dosyalar
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" \) \
       -not -path "*/node_modules/*" \
  | xargs wc -l 2>/dev/null | sort -rn | head -15

# Circular dependency ipucu
grep -r "from '\.\./" --include="*.ts" -l | head -10
grep -r "import.*from" --include="*.ts" . \
     -not -path "*/node_modules/*" | grep -c "\.\."

echo "### 2.2 Kod Kalitesi Analiz"
# TODO sayisi
grep -r "TODO\|FIXME\|HACK\|XXX\|TEMP\|BUG" \
     --include="*.ts" --include="*.js" --include="*.py" \
     -not -path "*/node_modules/*" | wc -l

# TODO detaylari
grep -rn "TODO\|FIXME\|HACK" \
     --include="*.ts" --include="*.js" --include="*.py" \
     -not -path "*/node_modules/*" | head -20

# any kullanimi
grep -r ": any" --include="*.ts" -not -path "*/node_modules/*" | wc -l
grep -r "as any" --include="*.ts" -not -path "*/node_modules/*" | wc -l

# console.log kontrolu
grep -rn "console\.log" --include="*.ts" --include="*.js" \
     -not -path "*/node_modules/*" -not -path "*test*" -not -path "*spec*" | wc -l

# Tekrar eden kod bloğu ipucu
grep -r "^function\|^const.*=.*=>" --include="*.ts" --include="*.js" \
     -not -path "*/node_modules/*" | awk -F: '{print $2}' | sort | uniq -d | head -10

# Error handling
grep -rn "try {" --include="*.ts" --include="*.py" \
     -not -path "*/node_modules/*" | wc -l
grep -rn "catch" --include="*.ts" --include="*.py" \
     -not -path "*/node_modules/*" | wc -l

echo "### 2.3 Güvenlik Analiz"
# Hardcoded secret
grep -rn "password\s*=\s*['\"]" --include="*.ts" --include="*.js" --include="*.py" \
     -not -path "*/node_modules/*" -not -path "*test*" | head -10
grep -rn "api_key\s*=\s*['\"]" --include="*.ts" --include="*.js" \
     -not -path "*/node_modules/*" | head -10

# .env commited mi?
git ls-files | grep "\.env$" 2>/dev/null

# SQL injection
grep -rn "query\s*=.*\$\{" --include="*.ts" --include="*.js" \
     -not -path "*/node_modules/*" | head -10
grep -rn "f\"SELECT\|f'SELECT" --include="*.py" | head -10

# Güvensiz paketler
cat package.json 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    deps = d.get('dependencies',{})
    risky = ['lodash','axios','express','moment']
    for r in risky:
        if r in deps: print(f'{r}: {deps[r]}')
except Exception as e:
    pass
" 2>/dev/null

# Auth middleware kontrolü
find . -name "*.ts" -not -path "*/node_modules/*" | \
  xargs grep -l "middleware\|auth\|guard\|jwt" 2>/dev/null | head -5

echo "### 2.4 Performans Analiz"
# N+1 sorgu riski
grep -rn "forEach\|for.*of\|map(" --include="*.ts" -A2 \
     -not -path "*/node_modules/*" | grep -B1 "await.*find\|await.*query" | head -10

# Buyuk bundle riski
cat package.json 2>/dev/null | python3 -c "
import json,sys
try:
    d=json.load(sys.stdin)
    deps=d.get('dependencies',{})
    heavy=['moment','lodash','chart.js','three','@mui/material']
    for h in heavy:
        if h in deps: print(f'⚠️  Ağır paket: {h} {deps[h]}')
except Exception as e:
    pass
" 2>/dev/null

# Caching kullanımı
grep -rn "cache\|redis\|memcache" --include="*.ts" --include="*.py" \
     -not -path "*/node_modules/*" -i | wc -l

# Async doğru kullanımı
grep -rn "async function\|async (" --include="*.ts" \
     -not -path "*/node_modules/*" | wc -l

echo "### 2.5 Test Analiz"
# Test dosyalari ve test sayisi
find . -type f \( -name "*.test.ts" -o -name "*.spec.ts" -o -name "*.test.js" \
       -o -name "*_test.py" -o -name "test_*.py" \) \
       -not -path "*/node_modules/*"

# Test runner konfigürasyonu
cat jest.config.* 2>/dev/null | head -20
cat vitest.config.* 2>/dev/null | head -20
cat pytest.ini 2>/dev/null | head -10

echo "### 2.6 API Tespiti"
# REST endpoint tespiti
grep -rn "\.get\(\|\.post\(\|\.put\(\|\.patch\(\|\.delete\(" \
     --include="*.ts" --include="*.js" \
     -not -path "*/node_modules/*" | grep -v "//.*\." | head -50

# FastAPI/Django route
grep -rn "@app\.\|@router\.\|@.*route" --include="*.py" | head -30

# GraphQL
find . -name "*.graphql" -o -name "*.gql" | head -5
grep -rn "type Query\|type Mutation" --include="*.ts" --include="*.graphql" \
     -not -path "*/node_modules/*" | head -20

# Swagger/OpenAPI
find . -name "swagger*" -o -name "openapi*" | grep -v node_modules
