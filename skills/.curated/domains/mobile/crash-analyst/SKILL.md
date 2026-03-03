---
name: crash-analyst
description: Parse and analyze crash reports from tools like Crashlytics or Sentry. Interpret iOS symbolication and Android ProGuard/R8 mappings, trace stack execution to find the root cause, and propose code-level fixes.
---

# Crash Analyst Protocol

A stack trace is a map to a bug, but on mobile, that map is often written in an obfuscated language. This skill interprets raw crash data (Crashlytics, Sentry, Bugsnag), identifies the true origin of the crash (which is often hidden deep in the trace), and provides actionable fixes.

**Core principle:** The top line of a stack trace is rarely the root cause. Follow the execution path.

---

## Workflow

```
1. Validate the Crash Report (Is it symbolicated? Is it complete?)
2. Isolate the Core Exception type and the Failing Thread
3. Trace the Stack (Find the highest point of *user* code)
4. Correlate with OS/Device/App Version context
5. Provide Root Cause and Mitigation
```

---

## Step 1: Report Validation
Before debugging, check if the report is readable.
- **Android:** If the trace is full of `a.b.c()`, it is obfuscated. The developer needs to upload their ProGuard/R8 `mapping.txt` to their crash reporter.
- **iOS:** If the trace is hex addresses (e.g., `0x00000001bcdefg`), it is unsymbolicated. The developer needs to upload the `.dSYM` file.
- If the trace is unreadable, stop the analysis and instruct the developer on how to symbolicate it.

## Step 2: Exception Isolation
Identify the type of crash:
- **NullPointerException (NPE) / Fatal signal 11 (SIGSEGV):** Trying to access memory that doesn't exist.
- **OutOfMemoryError (OOM) / EXC_RESOURCE:** The app used too much RAM. The stack trace here is usually useless because the crash happened at the last *straw*, not the root memory leak.
- **IllegalStateException / Swift Runtime Failure:** Framework rules were broken (e.g., modifying UI from a background thread).
- **ANR (Application Not Responding):** The main thread was blocked for > 5 seconds (Android) or watchdogs killed the app (iOS).

## Step 3: Stack Tracing
Ignore the OS framework lines at the very top (e.g., `android.app.ActivityThread.main` or `CoreFoundation`). 
- Scan down the stack trace until you find the first package name or namespace that belongs to the *app developer's code*. That is the injection point.

## Step 4: Contextual Correlation
Look at the metadata:
- Did this only happen on iOS 15? (Likely an API deprecation/availability issue).
- Did this only happen on Samsung devices? (Vendor-specific OS changes).
- Is it happening in the background? (Background execution limits).

## Step 5: Root Cause & Fix
Translate the stack trace into plain English and provide the code block to fix it.

---

## Output Format

```markdown
# 💥 Crash Analysis Report

## 🔍 Incident Summary
- **Exception:** `[e.g., java.lang.NullPointerException]`
- **Reason:** `[e.g., Attempt to invoke virtual method 'int java.lang.String.length()' on a null object reference]`
- **Affected OS/Devices:** `[e.g., Android 12+, All Manufacturers]`

## 🧵 Stack Trace Breakdown
The crash occurred in the `[Thread Name]` thread. 
The origin point in your code is:
`com.myapp.utils.FormatHelper.formatNames(FormatHelper.kt:42)`

*Trace path:*
1. User clicked the "Save Profile" button (`ProfileFragment.kt:112`)
2. Formatter tried to parse the middle name.
3. The DB returns null instead of an empty string for missing middle names.
4. Calling `.length` on this null value caused the NPE.

## 🛠 Actionable Fix

### Fix: Safecall / Optional Chaining
Your `formatNames` function assumes the `middleName` parameter string will always be present. You must check for nullability.

**Code Fix:**
```kotlin
// Before (Crashing):
fun formatNames(first: String, middle: String, last: String) {
    if (middle.length > 0) { ... }
}

// After (Safe):
fun formatNames(first: String, middle: String?, last: String) {
    if (!middle.isNullOrEmpty()) { ... }
}
```
```

---

## When to Skip
- The User is asking about backend server crashes (use a standard backend debug skill).

---

## Guardrails
- **OOM Warnings:** If the exception is an OutOfMemoryError, immediately warn the user that the stack trace provided is likely misleading and they need to use a memory profiler (like Android Studio Profiler or Xcode Allocations) to find the actual leak.
- **Background vs Foreground:** Always check the app state. A crash that says "Cannot execute background task" means the OS killed the app for taking too long, not necessarily a logic error in the code itself.

---

## References
See `references/EXAMPLES.md` for a worked case.
