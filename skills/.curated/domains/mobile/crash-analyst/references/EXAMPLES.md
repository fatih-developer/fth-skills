# Examples

## Example — iOS React Native Unsymbolicated Crash

**User Request:** 
"My React Native app is crashing on TestFlight for some users when they open the settings tab. Crashlytics just gives me this:
Fatal Exception: RCTFatalException: Unhandled JS Exception: TypeError: undefined is not an object (evaluating 'route.params.userId')
0 CoreFoundation 0x1a2b3c4d5e __exceptionPreprocess + 220
1 libobjc.A.dylib 0x8f7e6d5c4b objc_exception_throw + 60
2 MyApp 0x1029384756 RCTFatal + 668
3 MyApp 0x1029385678 -[RCTExceptionsManager reportFatal:stack:exceptionId:extraDataAsJSON:] + 500"

**Skill Response:**

```markdown
# 💥 Crash Analysis Report

## 🔍 Incident Summary
- **Exception:** `RCTFatalException: Unhandled JS Exception: TypeError`
- **Reason:** `undefined is not an object (evaluating 'route.params.userId')`
- **Affected Scope:** React Native Javascript Thread

## 🧵 Stack Trace Breakdown
The native stack trace you provided (CoreFoundation, libobjc) is actually a "wrapper" crash. React Native caught a Javascript error, couldn't handle it smoothly, and threw a fatal native Objective-C exception (`RCTFatal`) to deliberately crash the app.

The true root cause is inside your Javascript code, specifically on the Settings screen.
The error: `undefined is not an object (evaluating 'route.params.userId')` means you are trying to read `userId` from `route.params`, but `route.params` itself is `undefined`.

*Why is this happening only in TestFlight?*
Because in development (Metro bundler running), React Native shows a Redbox error screen that doesn't crash the app immediately. In a release build (TestFlight), all unhandled JS errors become fatal native crashes.

## 🛠 Actionable Fix

### Fix: Optional Chaining on Route Params
You are assuming that the Settings screen always receives navigation parameters. If a user navigates to Settings directly (e.g., from a bottom tab bar) without explicitly passing params, `route.params` is undefined.

**Code Fix:**
Navigate to your Settings screen component and update how you access the `userId`:

```javascript
// Before (Crashing):
const SettingsScreen = ({ route }) => {
  const userId = route.params.userId; // Crashes if params is undefined
  // ...
}

// After (Safe):
const SettingsScreen = ({ route }) => {
  // Use optional chaining (?.) and provide a fallback if needed
  const userId = route.params?.userId || null; 
  // ...
}
```

*Note: To prevent the native stack trace from hiding the JS error location in the future, ensure you have uploaded your React Native Source Maps to Crashlytics during the iOS build phase.*
```
