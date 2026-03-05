---
name: ecosystem-mobile
description: Comprehensive map and workflows for the Mobile domain. Triggers when users ask to "design a mobile app", "mobile architecture", "audit the app before launch", "prepare for release", or "view the mobile ecosystem".
---

# 📱 Mobile Domain Ecosystem

Welcome to the `mobile` domain ecosystem. This directory contains specialized agentic skills for React Native, Flutter, and Native iOS/Android app development, auditing, and deployment.

> **For Orchestrator Agents (`task-decomposer`, `parallel-planner`):**
> When asked to plan a mobile-related task, you **MUST** consult the workflows below. Do not hallucinate steps; map your plan strictly to these available skills in the order defined.

---

## 🔄 Standard Workflows & Handoffs

### 1. The Pre-Release Audit Flow

When the user asks to "audit the app before launch", "check if the app is ready", or "review our mobile app quality", execute these skills sequentially:

1. `@accessibility-enforcer` -> Ensures ADA/WCAG compliance, touch targets, and contrast.
2. `@mobile-perf-auditor` -> Analyzes bundle size, memory leaks, and frame drops.
3. `@mobile-security-auditor` -> Checks for exposed API keys, insecure storage, and network payloads.

### 2. The Production Deployment Flow

When the user asks to "deploy the app to the stores", "prepare for release", or "ship to production":

1. **[Execute Pre-Release Audit Flow First]**
2. `@app-store-reviewer` -> Validates metadata, privacy policy, and store guidelines to prevent rejection.
3. `@release-orchestrator` -> Manages versioning, build artifacts, testflight/alpha rollout, and release notes.

### 3. The New Feature Architect Flow

When the user asks to "build a new feature" that involves complex mobile constraints:

- If it requires deep linking/routing: use `@deep-link-architect`
- If it requires push notifications: use `@push-notification-planner`
- If it requires offline capabilities/local database: use `@offline-sync-designer`
- If it requires a new user flow/tutorial: use `@onboarding-designer`
  _(Note: These can run in parallel via `parallel-planner` depending on the feature scope.)_

### 4. Post-Launch Monitoring Flow

When the user asks to "investigate app issues", "fix crashes", or "analyze user complaints":

1. `@crash-analyst` -> Analyzes stack traces, symbolication, and user sessions.
2. _(Handoff based on conclusion)_ -> If it was a performance issue, handoff to `@mobile-perf-auditor`.

---

## 🧠 Core Philosophy

Mobile development is constrained by app store guidelines, device resources (battery/memory), and unreliable networks. Every skill in this domain is programmed to defend against these constraints. Never prioritize feature delivery over performance or security in a mobile environment.

---

## 🚀 Installation & Orchestration Instructions

As an AI Agent reading this ecosystem file, you must **actively guide** the user to install the missing skills for the selected workflow.

To install **all skills** within this ecosystem at once, you must execute or instruct the user to execute the provided installation script:

```bash
python skills/ecosystem-mobile/scripts/install_all.py
```

**Execution Rule:**
Do not attempt to perform the tasks of these skills yourself. Your job is to install them and hand off the execution to the appropriate skill, or instruct the user to trigger the newly installed skills in order.
