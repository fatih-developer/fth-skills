# Expert Roles Pool

Available domain experts for dynamic selection. Pick the 3 most relevant per request.

---

## Technical Roles

| Role | Icon | Expertise | Trigger When |
|------|------|-----------|--------------|
| **Security Architect** | 🔒 | Auth, encryption, attack vectors, compliance | Auth, API security, data handling |
| **Performance Engineer** | ⚡ | Latency, throughput, caching, profiling | Database queries, API design, rendering |
| **Infrastructure Architect** | 🏗️ | Cloud, containers, CI/CD, scaling | Deployment, scaling, infrastructure decisions |
| **Data Engineer** | 🗄️ | Schema design, migrations, indexing, ETL | Database choices, data modeling, queries |
| **Frontend Architect** | 🎨 | Component design, state management, rendering | UI architecture, framework decisions |
| **Backend Architect** | ⚙️ | API design, service patterns, queue systems | Server architecture, microservices |
| **DevOps Engineer** | 🔄 | Pipelines, monitoring, observability, IaC | CI/CD, deployment, logging |
| **ML/AI Engineer** | 🤖 | Model selection, prompting, embeddings, RAG | AI integration, prompt engineering |

## User-Facing Roles

| Role | Icon | Expertise | Trigger When |
|------|------|-----------|--------------|
| **UX Designer** | 👤 | Usability, flow, accessibility, interaction | User flows, UI decisions, forms |
| **DX Advocate** | 🛠️ | API ergonomics, SDK design, docs, tooling | Developer-facing products, APIs, libraries |
| **Product Manager** | 📋 | Scope, priorities, user stories, ROI | Feature planning, scope decisions |
| **Growth Strategist** | 📈 | Acquisition, retention, conversion, SEO | Marketing, landing pages, funnels |

## Quality Roles

| Role | Icon | Expertise | Trigger When |
|------|------|-----------|--------------|
| **QA Strategist** | 🧪 | Test strategy, coverage, automation | Testing approaches, quality gates |
| **Accessibility Expert** | ♿ | WCAG, screen readers, keyboard nav | UI components, public-facing pages |
| **Cost Analyst** | 💰 | TCO, pricing models, resource optimization | Cloud costs, SaaS selection, scaling costs |
| **Compliance Officer** | 📜 | GDPR, SOC2, HIPAA, data residency | User data, cross-border, regulated industries |

---

## Selection Heuristics

1. **Match the primary domain** — at least 1 expert must directly address the core question.
2. **Create productive tension** — pick experts whose priorities naturally conflict (e.g., Security vs DX, Performance vs Maintainability).
3. **Cover different dimensions** — avoid 3 experts from the same category (e.g., don't pick 3 Technical roles if the question has user-facing implications).
4. **Fallback rule** — if no clear domain experts apply, fall back to base multi-brain (Creative / Pragmatic / Comprehensive).

## Combination Examples

| Request | Expert Combo | Reasoning |
|---------|-------------|-----------|
| "Design an auth system" | Security Architect + DX Advocate + Backend Architect | Security-first with dev ergonomics and architecture |
| "Choose a database" | Data Engineer + Cost Analyst + Performance Engineer | Data modeling + cost + speed tradeoffs |
| "Build a landing page" | UX Designer + Growth Strategist + Frontend Architect | User experience meets conversion meets implementation |
| "Set up CI/CD pipeline" | DevOps Engineer + Security Architect + DX Advocate | Automation + security scanning + developer velocity |
