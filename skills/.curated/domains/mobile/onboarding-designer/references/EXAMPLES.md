# Examples

## Example — Fitness Tracking App

**User Request:** 
"I am building a new fitness tracker app. Right now, when they open the app, I show 3 splash screens explaining the app. Then I pop the Location permission (to track runs), the HealthKit permission (to read heart rate), and the Push Notification permission. Then they have to create an account. A lot of beta testers are dropping off. How can I fix this?"

**Skill Response:**

```markdown
# 🚀 Onboarding & First-Run Experience Plan

Your current flow suffers from "Permission Fatigue" and high friction. Users are being asked to give up highly sensitive data (Health, Location) and create an account before they have seen any value from the app.

## 🎯 The "Aha!" Moment
**Goal:** The user should see the beautifully designed dashboard and map interface before committing to a login.
**Time to Value:** Under 15 seconds.

## 🚦 Registration Strategy
**Flow: Deferred Login with Guest Exploration**
- Scrap the 3 splash screens. Nobody reads them.
- Drop the user directly onto the main Dashboard (Empty State).
- Allow them to poke around the UI. When they press the giant "Start Run" button for the first time, *then* prompt them to create an account to save their run data.

## 🔐 Permission Sequencing (Double Opt-In)
You must delay all permissions until contextually relevant, and use a "Soft Prompt" first.

| Permission | When to Ask (Soft Prompt) | Rationale User Copy |
|---|---|---|
| Location (When In Use) | After account creation, when they press "Start Run". | "We need your GPS to map your route and calculate your pace accurately." |
| HealthKit (Heart Rate) | After completing their first run, on the summary screen. | "Connect Apple Health to overlay your heart rate data onto this run summary." |
| Push Notifications | At the end of week 1, if they haven't run in 3 days. | "Want a gentle nudge to meet your weekly goal? Enable reminders." |

## 🪹 Empty State Design
**Screen:** Main Dashboard
**Visual:** A faded, blurred-out map with a pulsing blue dot in the center.
**Text:** "Ready to hit the pavement? Your stats will appear here."
**Action (CTA):** A massive, unmissable "Start First Run" button.

## 🪝 Day 1-3 Retention Loop
- **Day 1 Trigger:** If they downloaded the app but didn't run: Send an in-app message (if opened) or simple email: "Just a 10-minute walk counts! Here’s how to start tracking your daily steps."
- **Day 3 Trigger:** If they completed a run: Introduce the "Milestones" feature. "You ran 3 miles this week. Check out the Milestones tab to set a monthly goal."
```
