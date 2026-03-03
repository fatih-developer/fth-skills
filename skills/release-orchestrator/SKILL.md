---
name: release-orchestrator
description: Manage the mobile release lifecycle. Produce version bumps, changelog generation, TestFlight/Internal Track submission strategies, and staged rollout plans. Focuses on release management decisions, not CI/CD pipeline setup.
---

# Release Orchestrator Protocol

Shipping a mobile application is not just about uploading a binary. It involves version management, clear communication through changelogs, safe testing deployment, and strategic rollout planning to mitigate the impact of unforeseen bugs.

**Core principle:** A release is a controlled experiment, not a single 'launch' event.

---

## Workflow

```
1. Determine release type (Major, Minor, Patch, Hotfix)
2. Generate semantic version bump
3. Compile user-facing and internal changelogs
4. Define pre-production testing track (TestFlight / Play Console Internal)
5. Create a staged rollout plan for production
```

---

## Step 1: Release Categorization
Analyze the changes to determine the impact:
- **Major:** High impact. Large UX overhauls, core architecture changes, new monetization flows.
- **Minor:** Features added but backward compatible.
- **Patch:** Bug fixes, performance improvements.
- **Hotfix:** Critical, out-of-band failure correction (crashes, business logic breaks).

## Step 2: Version Generation
Based on semantic versioning (`MAJOR.MINOR.PATCH`):
- Increment the correct segment.
- Note any build number increment requirements for internal tracks.

## Step 3: Changelogs
Create two versions from the raw commit data or feature list:
- **Internal/Developer:** Technical specifics, PR numbers, API changes.
- **User-Facing (Store Notes):** Benefits, not features. Accessible language. Example: Instead of "Refactored CoreData schema," say "Improved app load times so you can get to your data faster."

## Step 4: Testing Tracks
Advise on the immediate next step before production:
- **iOS:** TestFlight Internal vs. External testing. Usually start with 1-2 days Internal.
- **Android:** Internal Testing track vs. Closed Beta vs. Open Beta.

## Step 5: Rollout Strategy
Design a phased release plan based on the release impact (Step 1). A typical patch might roll out faster than a major feature change.
- *Example:* Day 1 (1%), Day 2 (5%), Day 3 (20%), Day 5 (50%), Day 7 (100%).
- State specific monitoring metrics for each phase.

---

## Output Format

```markdown
# 🚀 Release Orchestration Plan

## 📦 Version Info
- **Type:** [Major/Minor/Patch/Hotfix]
- **Previous Version:** [X.Y.Z]
- **New Version:** [A.B.C]

## 📝 Changelogs

### 📣 User-Facing (Store Update Notes)
- [Bullet point translating technical fix to user benefit]

### 🛠 Internal (For QA/Stakeholders)
- [Bullet point of technical changes]

## 🧪 Pre-Production Strategy
- **Track:** [e.g., TestFlight External Testing]
- **Duration:** [X days]
- **Focus Areas for QA/Beta Users:** [Specific areas changed]

## 📈 Staged Rollout Plan
*Halt rollout if crash-free sessions drop below [Target%]*

| Day | Percentage | Monitoring Focus |
|---|---|---|
| 1 | 1% | Fatal crashes |
| 2 | 5% | Server load |
| 4 | 20% | User feedback on new feature |
| 7 | 100% | Full availability |
```

---

## When to Skip
- The user is asking how to configure Fastlane or GitHub Actions (that is CI/CD infrastructure, not release orchestration).
- The changes are non-production (e.g., updating a README).

---

## Guardrails
- **Never advise a 100% Day-1 rollout** unless it is a critical hotfix that resolves a store-blocking issue or 100% crash loop.
- **User-centric notes:** Force user-facing changelogs away from jargon.
- **Store nuances:** Remember iOS TestFlight external testing requires a basic, shorter Apple review. Plan for that delay.

---

## References
See `references/EXAMPLES.md` for a worked case.

---

## 🔗 Next Steps & Handoffs
If you are executing the **Production Deployment Flow** as defined in the Mobile ECOSYSTEM guide, this skill represents the final step of the release preparation. 

Once the app is live, the next logical skill in the lifecycle (Post-Launch Monitoring Flow) is:
- `@crash-analyst` (to monitor stability during rollout)
