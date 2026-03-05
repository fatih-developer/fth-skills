---
name: ecosystem-database
description: Comprehensive map and workflows for the Database domain. Triggers when users ask to "design a database", "optimize query", "schema architecture", "database ecosystem", or migrate data.
---

# 🗄️ Database Domain Ecosystem

Welcome to the `database` domain ecosystem. This directory contains specialized agentic skills for database schema design, query optimization, data migration, and security (SQL & NoSQL).

> **For Orchestrator Agents (`task-decomposer`, `parallel-planner`):**
> When asked to plan a database-related task, you **MUST** consult the workflows below. Do not hallucinate steps; map your plan strictly to these available skills in the order defined.

---

## 🔄 Standard Workflows & Handoffs

### 1. New Schema Design Flow

When the user asks to "design a database", "create tables", or "model the data", execute these skills sequentially:

1. `@schema-architect` -> Creates the ERDs, tables, relationships, and normalizes the models.
2. `@access-policy-designer` -> Designs Row-Level Security (RLS) or application-level access controls.
3. `@seed-data-generator` -> Generates realistic, varied placeholder data for development and testing.

### 2. Performance Optimization Flow

When the user asks to "fix a slow query", "optimize the database", or "why is the DB lagging":

1. `@query-explainer` -> Analyzes the execution plans (e.g., `EXPLAIN ANALYZE`) to locate bottlenecks.
2. `@index-advisor` -> Recommends optimal covering indexes, composites, or partition keys to solve the bottleneck.
3. `@query-budget-enforcer` -> Sets up mechanisms to detect and alert on N+1 queries or heavy reads in the future.

### 3. Database Evolution Flow

When the user asks to "update the database", "change a table", or "migrate data":

1. `@schema-diff-analyzer` -> Compares the old schema and new schema to detect potential data loss or locks.
2. `@migration-strategist` -> Designs the zero-downtime migration scripts (up/down) and backfill jobs.

### 4. Compliance & Observability Flow

When the user asks about "data privacy", "GDPR", or "where does this data go":

1. `@data-masker` -> Identifies PII (Personally Identifiable Information) and designs obfuscation/encryption strategies.
2. `@data-lineage-tracer` -> Maps how data flows from ingestion to the data warehouse.

---

## 🧠 Core Philosophy

Database design is focused on data integrity, scalable reads/writes, and strict security constraints. Every skill in this domain is programmed to defend against data corruption and insecure data exposure. Never prioritize feature delivery over data safety.

---

## 🚀 Installation & Orchestration Instructions

As an AI Agent reading this ecosystem file, you must **actively guide** the user to install the missing skills for the selected workflow.

If the user wants to execute the **New Schema Design Flow**, you must execute or instruct the user to execute the following terminal commands:

```bash
skills install schema-architect
skills install access-policy-designer
skills install seed-data-generator
```

**Execution Rule:**
Do not attempt to perform the tasks of these skills yourself. Your job is to install them and hand off the execution to the appropriate skill, or instruct the user to trigger the newly installed skills in order.
