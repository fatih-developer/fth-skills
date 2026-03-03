---
name: app-store-reviewer
description: Analyze App Store and Play Store rejection reasons, detect guideline violations before submission, and optimize metadata (title, screenshots, description) for store review policies.
---

# App Store Reviewer Protocol

The submission process is critical. A rejection costs days. This skill acts as a preemptive store reviewer. It evaluates app metadata, features, and submission history against Apple's App Store Review Guidelines and Google Play Developer Policies.

**Core principle:** Find the rejection before the real reviewer does. 

---

## Workflow

```
1. Identify target platform (iOS, Android, or both)
2. Analyze provided metadata and feature list
3. Cross-reference with current store guidelines
4. Flag violations (Critical, Warning, Optimization)
5. Generate submission readiness report
```

---

## Step 1: Platform Context
Determine if the review is for the App Store (iOS), Play Store (Android), or both. Their policies differ significantly (e.g., Apple's strictness on in-app purchases vs. Google's focus on permissions).

## Step 2: Input Analysis
Review the user's provided inputs:
- App Title & Subtitle
- Promotional Text & Description
- Keywords (iOS)
- Screenshots & Video descriptions
- Core features and permissions requested (e.g., location, camera)
- In-App Purchase (IAP) structures

## Step 3: Guideline Verification
Check against common rejection reasons:
- **iOS Top Rejections:** 2.1 Performance (Crashes/Bugs), 2.3.3 Accurate Metadata, 3.1.1 In-App Purchase logic, 4.0 Design (Spam/Copycats), 5.1.1 Data Collection and Storage (Privacy).
- **Android Top Rejections:** Broken Functionality, Inappropriate Content, Misleading Claims, Improper Use of Permissions, Sign-in Wall without Guest Mode (in some cases).

## Step 4: Issue Categorization
Categorize findings into:
- **[CRITICAL]** Will definitely cause a rejection. Must fix.
- **[WARNING]** High risk of rejection depending on reviewer interpretation.
- **[OPTIMIZATION]** Safe, but metadata could be improved for ASO (App Store Optimization) or clarity.

## Step 5: Output Generation
Create a structured report detailing the findings, quoting the specific guideline violated, and providing an actionable fix.

---

## Output Format

```markdown
# 📋 Store Review Readiness Report

**Target Platform(s):** [App Store / Google Play]

## 🚨 Critical Violations
*Issues that will trigger a definitive rejection.*

1. **[Violation Area]** (e.g., In-App Purchases)
   - **Guideline:** [Quote or reference the guideline, e.g., Apple 3.1.1]
   - **Finding:** [Explain what is wrong, e.g., "Using Stripe for digital goods instead of IAP."]
   - **Fix:** [Actionable solution]

## ⚠️ High-Risk Warnings
*Subjective areas where a reviewer might push back.*

1. **[Risk Area]** (e.g., Privacy / Permissions)
   - **Guideline:** [Reference]
   - **Finding:** [Explanation]
   - **Mitigation:** [How to reduce the risk]

## 💡 Metadata Optimization
*Suggestions for better conversion and ASO.*

- **Title/Subtitle:** [Suggestion]
- **Screenshots:** [Suggestion]
- **Description:** [Suggestion]

## Next Steps
[Summary of what the developer must do before hitting "Submit"]
```

---

## When to Skip
- The task is purely code formatting or UI design with no store-facing implications.
- The user is asking about marketing strategy outside the store listing.

---

## Guardrails
- **Quote the Rules:** Always back up a rejection risk with a specific guideline number or concept (e.g., "Guideline 5.1.1" or "Play Console Spam Policy").
- **No Guarantees:** Explicitly state that fixing these issues does not guarantee approval, as human reviewers vary.
- **Platform Specificity:** Do not apply Apple rules to Google (like 30-character title limits, which differs between stores).

---

## References
See `references/EXAMPLES.md` for a worked case.
