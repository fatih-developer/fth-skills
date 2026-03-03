---
name: push-notification-planner
description: Plan end-to-end push notification strategies using APNs and FCM. Design payloads, define permission request timing, architect silent pushes vs. rich notifications, and structure analytics tracking.
---

# Push Notification Planner Protocol

Implementing push notifications correctly involves much more than asking for permission on launch and wiring up Firebase Cloud Messaging (FCM). It requires empathy for the user's attention, right-timed permission requests, robust payload design, and proper routing when the app is in foreground, background, or killed state.

**Core principle:** A push notification must be timely, personal, and actionable. Unprompted "We miss you" pushes are spam.

---

## Workflow

```
1. Define the business goal for the notifications
2. Design the permission request strategy (When and How to ask)
3. Architect the payload structures (Data vs. Notification)
4. Plan handling logic (Foreground vs. Background/Killed)
5. Define key metrics to track success
```

---

## Step 1: Goal Definition
Categorize the type of push needed:
- **Transactional:** Order updates, messages received, friend requests. (High value to user).
- **Engagement/Marketing:** Newsletters, promotions, "Check out this feature." (High risk of opt-out).
- **Silent (Data-only):** Background sync triggers, badge icon updates (No UI shown to user).

## Step 2: Permission Strategy
**Never** ask for push permissions on app launch. 
- Design a "Pre-permission" or "Soft prompt" flow. Explain *why* the user needs notifications before triggering the native OS dialogue.
- Choose the trigger moment: e.g., Right after the user makes their first purchase ("Want to track your order?").

## Step 3: Payload Architecture
Distinguish between Apple Push Notification service (APNs) and Firebase Cloud Messaging (FCM) structures. 
- **Notification Payload:** Handled automatically by the system (shows the banner). Less flexible.
- **Data Payload:** Handled entirely by your code. Required for silent pushes or complex routing. Must be processed in a background service (Android) or `didReceiveRemoteNotification` (iOS).

## Step 4: Routing & Interaction
Define what happens when the user clicks the notification.
- Does it deep link to a specific screen? 
- Does it have action buttons ("Reply", "Mark as Read")? 
- What happens if the notification arrives while the app is already open (Foreground)? Often, you should display an in-app toast instead of a system banner.

---

## Output Format

```markdown
# 🔔 Push Notification Strategy Plan

## 🎯 Use Case & Goal
**Type:** [Transactional / Marketing / Silent]
**Description:** [What are we telling the user?]

## 🗣 Permission Request Strategy
- **When to Ask:** [E.g., After submitting the first order]
- **Soft Prompt Copy:** "Enable notifications so we can tell you the minute your food arrives."
- **Fallback:** If they decline the native prompt, allow them to enable it later in app Settings.

## 📦 Payload Architecture (FCM Example)
```json
{
  "message": {
    "token": "DEVICE_REGISTRATION_TOKEN",
    // Use 'notification' block for standard alerts
    "notification": {
      "title": "Your order is arriving!",
      "body": "Driver is 2 minutes away."
    },
    // Use 'data' block for deep-linking and silent processing
    "data": {
      "type": "ORDER_UPDATE",
      "orderId": "12345",
      "route": "/orders/12345/tracking"
    }
  }
}
```

## 🛤 Handling & Routing Logic
- **App in Background / Killed:** System displays banner. Upon tapping, read `data.route` and navigate to `/orders/12345/tracking`.
- **App in Foreground:** Silent to system banner. App intercepts data payload and shows an in-app Toast: "Order is 2 mins away [View]".

## 📊 Analytics & Tracking
To measure success, track these specific custom events:
- `push_prompt_shown`
- `push_prompt_accepted` / `push_prompt_declined`
- `push_received` (if measurable)
- `push_opened`
```

---

## When to Skip
- The User is asking about backend server architecture for millions of concurrent socket connections (this skill is focused on the mobile push client & strategy).

---

## Guardrails
- **No Launch Prompts:** Always correct developers who try to shove the `requestPermissions()` call inside `useEffect` or `viewDidLoad` on the main screen.
- **FCM 'notification' vs 'data':** Explain the critical difference between these two payload types. A `notification` block in FCM when the app is backgrounded will NOT wake up your JavaScript/App logic until the user taps it. You must use `data` only if you need to run background logic immediately upon receipt.

---

## References
See `references/EXAMPLES.md` for a worked case.
