# Examples

## Example — Chat App Notifications

**User Request:** 
"I am building a chat app. I need to send a push notification when someone gets a new message. If they click it, it should go to that exact chat. Also, how do I stop it from showing the notification if they currently have that specific chat open on their screen right now?"

**Skill Response:**

```markdown
# 🔔 Push Notification Strategy Plan

## 🎯 Use Case & Goal
**Type:** Transactional
**Description:** Alerting users of new incoming direct messages.

## 🗣 Permission Request Strategy
- **When to Ask:** Right after the user completes onboarding or sends their first message to someone.
- **Soft Prompt Copy:** "Want to know when your friends reply? Enable notifications to get instant alerts."

## 📦 Payload Architecture (FCM/Data-Only Approach)
*Since this is a chat app, we strongly recommend sending a **data-only** payload. This gives your app full control over whether to display a notification or not.*

```json
{
  "message": {
    "token": "DEVICE_TOKEN",
    "android": { "priority": "high" },
    "apns": {
      "payload": {
        "aps": { "content-available": 1 }
      }
    },
    "data": {
      "type": "NEW_MESSAGE",
      "chatId": "CHAT_987",
      "senderName": "Jane Doe",
      "snippet": "Hey, where are we meeting?",
      "route": "/chat/CHAT_987"
    }
  }
}
```

## 🛤 Handling & Routing Logic

### Problem: Suppressing Notifications for Active Chats
Because we are using a **data-only** payload, the OS will NOT automatically show a banner. Your app code must decide what to do.

1. **App in Background / Killed:** 
   - A background headless task (e.g., `messaging().setBackgroundMessageHandler` in React Native Firebase) wakes up, reads the data, and manually creates a local notification using a library like Notifee or the standard native NotificationManager.
   - When tapped, the app boots and reads the initial notification `route`, navigating directly to `/chat/CHAT_987`.

2. **App in Foreground:** 
   - The active screen component listens for incoming FCM messages.
   - **Logic Check:** 
     - If `currentRoute.params.chatId === incomingData.chatId` -> Do nothing (or play a soft 'pop' sound and render the new message in the UI).
     - If `currentRoute.params.chatId !== incomingData.chatId` -> Show an in-app Toast component ("New message from Jane Doe"). Do not show a system banner.

## 📊 Analytics & Tracking
To measure success, track these specific custom events:
- `push_prompt_conversion_rate` (Accepted / Shown)
- `push_opened_chat` (Tracks how many active sessions start from deep-linked pushes).
```
