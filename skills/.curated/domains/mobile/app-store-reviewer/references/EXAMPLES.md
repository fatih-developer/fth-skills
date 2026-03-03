# Examples

## Example — Preemptive Review of a Social App

**User Request:** 
"I'm ready to submit my new iOS social app. Users can post text and images. They have to sign up with Apple or Google. I added a premium tier for $5/mo using Stripe to remove ads. The title is 'Chatter - Best Free Social Network'. Any issues?"

**Skill Response:**

```markdown
# 📋 Store Review Readiness Report

**Target Platform(s):** App Store (iOS)

## 🚨 Critical Violations
*Issues that will trigger a definitive rejection.*

1. **In-App Purchases for Digital Features**
   - **Guideline:** Apple 3.1.1 (In-App Purchase)
   - **Finding:** You are using Stripe to unlock a premium tier (removing ads) within the app. Digital goods and features must use Apple's native In-App Purchase system.
   - **Fix:** Remove Stripe integration for this feature and implement StoreKit for the $5/mo subscription.

2. **Sign-In with Apple Requirement**
   - **Guideline:** Apple 4.8 (Sign in with Apple)
   - **Finding:** Apps that use third-party or social login service (like Google) must also offer Sign in with Apple as an equivalent option.
   - **Fix:** Ensure "Sign in with Apple" is implemented and visibly equal to the Google login button.

3. **User-Generated Content (UGC) Controls**
   - **Guideline:** Apple 1.2 (User Generated Content)
   - **Finding:** Social apps allowing user posts and images require specific UGC safety features. You did not mention these.
   - **Fix:** Ensure you have: 1) A way to filter objectionable material, 2) A mechanism to report offensive content/users, 3) The ability to block abusive users, 4) Published contact info so users can reach you.

## ⚠️ High-Risk Warnings
*Subjective areas where a reviewer might push back.*

1. **Metadata Pricing Claims**
   - **Guideline:** Apple 2.3.1 (Hidden or Non-Obvious Features) / General Metadata Rules
   - **Finding:** Your title includes the word "Free" ('Chatter - Best Free Social Network'). Apple frequently rejects apps that include price information (like "Free" or "Discount") in the app name or subtitle.
   - **Mitigation:** Change the title to just "Chatter - Social Network" and highlight the free aspect in the promotional text or description instead.

## 💡 Metadata Optimization
*Suggestions for better conversion and ASO.*

- **Subtitle:** Make sure you use the remaining characters in the subtitle for strong keywords (e.g., "Connect with friends globally").
- **Screenshots:** Ensure the first three screenshots clearly show the core UI of posting and viewing images.

## Next Steps
Before submitting to App Store Connect, you **must** replace Stripe with StoreKit for the subscription, verify your UGC reporting flow is functional, and remove the word "Free" from your app title.
```
