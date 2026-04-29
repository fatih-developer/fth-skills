# Skill Comparison Report: Coolify Orchestration

**Goal:** Compare the local `coolify-orchestrator` skill with the external `ajmcclary/coolify-manager` to determine the best approach for managing Coolify infrastructure.

## Skill Metadata
- **Local Skill:** `coolify-orchestrator` (h:\Project\fth-skills\skills\coolify-orchestrator)
- **External Skill:** `coolify-manager` (https://skills.sh/ajmcclary/coolify-manager/coolify-manager)
- **External Security Audit:** ❌ Trust Hub: FAIL | ❌ Snyk: FAIL | ✅ Socket: PASS

## Skill Comparison

| Dimension | [Local coolify-orchestrator] | [ajmcclary coolify-manager] | Winner |
|-----------|-----------|-----------|--------|
| **Primary Mechanism** | Native MCP / Direct REST API | Custom third-party CLI wrapper | **Local** (No extra CLI dependency) |
| **Ecosystem Focus** | Modern TS (Next.js, Bun, Hono, Turbo) | Heavily WordPress / PHP focused | **Local** (Modern Stack) |
| **Scope & Generality** | 9/10 - "Multi-tenant env vars, Turborepo builds, DB provisioning" | 5/10 - "Fix .htaccess, test REST API, PHP limits" | **Local** |
| **Technical Depth** | 9/10 - "HTTP probes, deployment monitoring loops, Docker context checks" | 4/10 - "Run `coolify app logs` or `sed -i`" | **Local** |
| **Decision Intelligence** | 9/10 - Structured Playbooks (TURBO-DEPLOY, PROVISIONING, etc.) | 6/10 - Basic flowchart for site availability | **Local** |
| **Security Practices** | 9/10 - "Never show API token / Mask env vars / Approval for destructive ops" | 2/10 - Failed Trust Hub & Snyk / Blind `sed` & `echo` | **Local** |
| **Error Handling** | 8/10 - "If failed → analyze logs, check /health endpoint loops" | 5/10 - Focuses solely on .htaccess 500 errors | **Local** |
| **Documentation** | 9/10 - Highly modular (`references/` structure) | 6/10 - Monolithic structure | **Local** |
| **Freshness** | 10/10 - Supports native MCP natively | 4/10 - Security audit failures | **Local** |
| **Overall Score** | **89/100** | **44/100** | **Local coolify-orchestrator** |

*(Note: Dimensions ORM Compatibility, Output Quality, and Monitoring were marked N/A due to the operational nature of both skills).*

## Recommendation: KEEP LOCAL (VERDICT: BUILD FROM SCRATCH / REJECT EXTERNAL)

**Why to reject `ajmcclary/coolify-manager`:**
1. **Security Flags:** It has overtly failed Snyk and Trust Hub verification.
2. **Dependency Overhead:** It relies on installing an overarching `scripts/install_coolify_cli.sh` wrapper, mutating the user's `PATH`. Our `coolify-orchestrator` relies natively on MCP or zero-dependency REST API requests (`curl`).
3. **Very Niche Focus:** The external skill is overwhelmingly fixated on standard WordPress (PHP) troubleshooting (modifying `.htaccess`, REST APIs). It lacks knowledge about multi-container modern deployments (Turborepo, Bun, Next.js).

**Conclusion:**
There are no useful attributes from the external skill to adapt into our codebase. The local `coolify-orchestrator` is significantly superior in terms of architecture, security constraints, integration with MCP, and targeted playbooks.
