#!/usr/bin/env python3

import re
import os
from pathlib import Path

translations = {
    "webhook-architect": "Architects the provider side of the webhook infrastructure. Not only sends data but designs event schemas and robust delivery mechanisms.",
    "seed-data-generator": "Generates realistic test data preserving referential integrity. Reads schemas, foreign keys, and builds relationships.",
    "schema-diff-analyzer": "Detects schema differences between environments (dev vs staging vs prod). Generates actionable migration paths instead of just diff lists.",
    "schema-architect": "Derives the database schema from business requirements. Selects optimal normalization levels (1NF->3NF->BCNF) and prevents God tables.",
    "rate-limit-strategist": "Selects the optimal rate limiting strategy (sliding window, token bucket, leaky bucket) for per-user, per-IP, or global levels.",
    "query-explainer": "Translates execution plans (EXPLAIN ANALYZE) into human-readable language. Explains why Seq Scan is bad and when Hash Join is optimal.",
    "query-budget-enforcer": "Defines and enforces query resource limits. Detects which queries scan too many rows, inflate memory usage, or exceed execution budgets.",
    "protocol-selector": "Selects the most suitable API protocol (REST, GraphQL, gRPC) based on project requirements like latency, payload size, and real-time needs.",
    "mobile-security-auditor": "Evaluates mobile app security against the OWASP Mobile Top 10. Implements certificate pinning, secure storage, and reverse-engineering protections.",
    "migration-strategist": "Manages major schema changes with zero-downtime using the expand-contract pattern, rather than writing unstable from-scratch migrations.",
    "index-advisor": "Analyzes existing queries and schema to detect missing indexes. Suggests covering and composite indexes to optimize slow queries.",
    "data-masker": "Masks production data for test and development environments (Data Masking). Detects PII (email, SSN, credit cards) and obfuscates them safely.",
    "data-lineage-tracer": "Traces the data source (Data Lineage) of any column or table. Identifies views, triggers, stored procedures, and ETL pipelines involved.",
    "contract-first-designer": "Writes OpenAPI/AsyncAPI specifications before writing any code. Determines provider-consumer contracts and endpoint definitions early.",
    "changelog-generator": "Analyzes commit history, PR descriptions, and spec changes to automatically generate developer-friendly API changelogs.",
    "breaking-change-detector": "Compares two OpenAPI/API specification versions (V1 vs V2) to detect breaking changes and backward compatibility issues.",
    "auth-flow-designer": "Determines whether to use API keys, JWT, OAuth2, or mTLS. Designs token lifespans, refresh token strategies, and secure session management.",
    "api-observability-planner": "Architects which metrics to collect, how logs should be formatted, and how distributed tracing should be implemented across boundaries.",
    "api-mock-designer": "Designs realistic API mock servers. Goes beyond happy paths by designing stateful mocks (create order -> get order) for complex integrations.",
    "access-policy-designer": "Designs and implements row-level security (RLS), column-level masking, and role-based access control policies (RBAC/ABAC)."
}

for skill_name, eng_desc in translations.items():
    skill_dir = Path(f"skills/{skill_name}")
    if not skill_dir.exists():
        # Maybe inside .curated
        for d in Path("skills").rglob(skill_name):
            if d.is_dir():
                skill_dir = d
                break
    
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        # Replace the description in the YAML frontmatter
        new_text = re.sub(
            r'^(description:\s*)(.*?)(?=\n[A-Za-z_-]+:|\n---)', 
            lambda m: m.group(1) + eng_desc, 
            text, 
            flags=re.MULTILINE | re.DOTALL,
            count=1
        )
        skill_md.write_text(new_text, encoding="utf-8")
        print(f"Updated SKILL.md for {skill_name}")
    
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.exists():
        # Remove it so generate_openai_yaml.py can recreate it cleanly
        openai_yaml.unlink()

print("Translating completed. Use generate_openai_yaml.py to regenerate agents/openai.yaml files.")
