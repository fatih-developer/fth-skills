# Examples — Multi-Brain Experts

---

## Example 1: API Authentication Design

**Request:** "Design authentication for our public REST API."

```markdown
## 🧠 Expert Panel

**Selected Experts:** Security Architect, DX Advocate, Backend Architect
**Why these 3:** Auth requires security-first design, developer ergonomics for API consumers, and solid backend architecture.

**🔒 Security Architect:**
Use OAuth 2.0 with PKCE for third-party access and short-lived JWTs (15min) with
refresh token rotation for first-party clients. Never expose long-lived secrets
in client-side code. Implement rate limiting per API key.

**🛠️ DX Advocate:**
Provide API keys for server-to-server simplicity with clear documentation.
Support both Bearer tokens and API keys — let developers choose based on their
use case. Include a sandbox environment with test credentials.

**⚙️ Backend Architect:**
Centralize auth in an API gateway or middleware layer — don't scatter auth checks
across services. Use a claims-based model so downstream services get pre-validated
context. Plan for multi-tenancy from the start.

---

## ⚖️ Consensus
OAuth 2.0 + PKCE for interactive flows, API keys for server-to-server (Security +
DX). Centralize in middleware with claims propagation (Backend). Sandbox environment
for developer onboarding (DX).

---

## 💻 Code
[Full implementation: auth middleware, JWT validation, API key management, example
client integration]
```

---

## Example 2: Database Selection for SaaS

**Request:** "Which database should I use for a multi-tenant SaaS app?"

```markdown
## 🧠 Expert Panel

**Selected Experts:** Data Engineer, Cost Analyst, Performance Engineer
**Why these 3:** Database selection requires schema expertise, cost projections at scale, and query performance analysis.

**🗄️ Data Engineer:**
PostgreSQL with Row-Level Security for tenant isolation. Schema-per-tenant adds
complexity without proportional benefit until 1000+ tenants. Use partitioning
for large tables and UUIDv7 for distributed-friendly primary keys.

**💰 Cost Analyst:**
Managed PostgreSQL (RDS/Cloud SQL) at $200-400/month covers most early-stage SaaS.
Aurora Serverless for unpredictable workloads but watch I/O costs. Avoid DynamoDB
unless your access patterns are well-defined — costs surprise at scale.

**⚡ Performance Engineer:**
Index tenant_id on every table. Use connection pooling (PgBouncer) from day one.
Prepared statements + query plan caching give 3-5x improvement on repeated queries.
Plan read replicas for analytics workloads.

---

## ⚖️ Consensus
PostgreSQL with RLS, managed hosting, connection pooling from day one. UUIDv7 keys
for future scalability. Budget $300/month initially with Aurora Serverless as the
scale-up path.
```
