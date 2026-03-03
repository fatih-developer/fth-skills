---
name: onboarding-designer
description: Design the first-run experience (FRE) for mobile apps. Sequence permission requests, define feature discovery flows, plan empty states, and create retention-focused day 1-3 scenarios.
---

# Onboarding Designer Protocol

You only get one chance to make a first impression. If a user downloads an app and is immediately hit with 3 native permission dialogs (Push, Location, Tracking) before they even know what the app does, they will delete it. This skill designs onboarding flows optimized for user retention and permission acceptance.

**Core principle:** Show value before asking for trust.

---

## Workflow

```
1. Map the required app permissions and account creation needs
2. Design the "Aha!" Moment (Value Proposition)
3. Sequence the Soft & Hard Permission Prompts
4. Design the Empty States (Day 0)
5. Plan the Day 1 to Day 3 Retention Hooks
```

---

## Step 1: Requirements Mapping
What does the app *absolutely need* to function?
- **Authentication:** Is an account required immediately, or can they browse as a guest? (Apple mandates guest mode if account isn't strictly necessary).
- **Permissions:** Location, Notifications, Camera, Photo Library, App Tracking Transparency (ATT).

## Step 2: Value Discovery
Instead of a stationary 4-page swipe carousel that no one reads, design progressive disclosure.
- Drop the user into the app as quickly as possible.
- Use tooltip overlays or guided tours only when the user touches a relevant feature.

## Step 3: Permission Sequencing (The Double-Opt-In)
Never trigger the OS-level permission dialog blindly.
- **The "Soft Prompt":** A custom UI screen explaining *why* you need the permission. (e.g., "We need your location to find nearby restaurants.")
- If they say "No" to the soft prompt, you save the real OS prompt for later.
- If they say "Yes", you trigger the OS prompt, and they are primed to accept.

## Step 4: Empty States
The moment after onboarding, the app is usually empty (no friends, no data, no history).
- **Do not show a blank screen.**
- Provide a clear, single Call-To-Action (CTA) pointing to the core value loop (e.g., "Add your first task", "Import your contacts").

## Step 5: Retention Hooks
Design the communication strategy to bring them back.
- **Day 1:** Did they complete the core action? If not, send a helpful local notification or email.
- **Day 3:** Introduce a power-user feature they haven't discovered yet.

---

## Output Format

```markdown
# 🚀 Onboarding & First-Run Experience Plan

## 🎯 The "Aha!" Moment
**Goal:** [What is the first thing the user should achieve to feel the app's value?]
**Time to Value:** [e.g., Under 60 seconds]

## 🚦 Registration Strategy
- **Flow:** [e.g., Deferred Login. Let users browse nearby restaurants without an account. Only ask for login when they click 'Order'.]

## 🔐 Permission Sequencing (Double Opt-In)
| Permission | When to Ask (Soft Prompt) | Rationale User Copy |
|---|---|---|
| Location (When In Use) | Upon tapping "Find near me" | "We need your location to show restaurants in your zip code." |
| Push Notifications | After placing the very first order | "Want to know when your food arrives? Enable notifications." |

## 🪹 Empty State Design
**Screen:** [e.g., 'My Orders' Tab]
**Visual:** [Illustration of an empty shopping bag]
**Text:** "You haven't ordered anything yet. Hungry?"
**Action (CTA):** [Button: "Browse Popular Places"]

## 🪝 Day 1-3 Retention Loop
- **Day 1 Trigger:** [If user generated an order: Do nothing. If not: "Still deciding? Here is a $5 promo code."]
- **Day 3 Trigger:** ["Did you know you can save your favorite meals for 1-tap ordering?"]
```

---

## When to Skip
- The user is asking about the visual UI design (colors, corner radius). This is a UX flow and behavioral design skill.

---

## Guardrails
- **Apple Guideline 5.1.1 (v):** Explicitly warn developers that Apple requires apps to provide "Sign in with Apple" if they use third-party social logins.
- **App Tracking Transparency (ATT):** If they use ads, remind them that the ATT prompt must be shown, but should ideally be preceded by a soft prompt explaining that tracking keeps the app free.

---

## References
See `references/EXAMPLES.md` for a worked case.
