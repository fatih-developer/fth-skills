# Examples

## Example — Minor Feature Update

**User Request:** 
"We are ready to release. Current version is 1.4.2. We added a new dark mode toggle, fixed a bug where the profile image wouldn't upload on Android 13, and updated the analytics SDK from v2 to v3. How should we roll this out?"

**Skill Response:**

```markdown
# 🚀 Release Orchestration Plan

## 📦 Version Info
- **Type:** Minor
- **Previous Version:** 1.4.2
- **New Version:** 1.5.0

## 📝 Changelogs

### 📣 User-Facing (Store Update Notes)
- 🌙 **Dark Mode is here!** You can now easily switch to a darker theme right from your profile settings. Perfect for late-night scrolling.
- 🐛 **Bug Fix:** Fixed an issue preventing some users from uploading a new profile picture.

### 🛠 Internal (For QA/Stakeholders)
- `Feature:` Implemented `ThemeContext` for dynamic dark mode switching.
- `Fix:` Addressed Android 13 scoped storage permission crash in image picker (`Media.Images`).
- `Tech Debt:` Bumped `AnalyticsProvider` SDK from v2.1 to v3.0 per deprecation warning.

## 🧪 Pre-Production Strategy
- **Track:** Internal Testing (Google Play) / TestFlight Internal (iOS)
- **Duration:** 2 Days
- **Focus Areas for QA/Beta Users:** Ensure analytics events still fire correctly with the v3 SDK (critical path). Test profile picture upload on both legacy Android and Android 13 devices. 

## 📈 Staged Rollout Plan
*Halt rollout if crash-free sessions drop below 99.5% or if analytics data drops unexpectedly.*

| Day | Percentage | Monitoring Focus |
|---|---|---|
| 1 | 1% | Monitor for any unexpected SDK v3 initialization crashes. |
| 2 | 5% | Check analytics dashboard to ensure event volume matches the 5% user cohort. |
| 4 | 20% | Evaluate engagement with the new Dark Mode toggle. |
| 6 | 50% | General stability check. |
| 7 | 100% | Full availability |
```
