---
name: mobile-perf-auditor
description: Evaluate mobile app performance holistically across cold start time, FPS drops, memory leaks, battery drain, and bundle size. Interpret profiling data and pinpoint platform-specific bottlenecks.
---

# Mobile Performance Auditor Protocol

Mobile devices have hard constraints on memory, CPU, and battery. What works fine on a fast developer machine or simulator might cause a crash or severe battery drain on a 4-year-old device. This skill analyzes performance metrics to find the root cause of sluggishness or resource exhaustion.

**Core principle:** Blaming the user's device is not an option. Find the bottleneck in the code.

---

## Workflow

```
1. Identify the performance symptom (e.g., slow start, UI stutter, OOM crashes)
2. Determine the context (iOS, Android, React Native, Platform context)
3. Request or analyze profiling data / metrics
4. Correlate metrics with common architectural anti-patterns
5. Propose a targeted, measurable fix
```

---

## Step 1: Symptom Identification
Categorize the user's complaint:
- **Cold Start:** Time from tapping the icon to the first meaningful interaction.
- **Jank/Stutter:** Framerate dropping below 60fps (or 120fps) during scrolling or animations.
- **Memory/OOM:** Out Of Memory crashes caused by leaks or large resource allocation.
- **Battery/Thermal:** Phone getting hot or draining battery due to non-stop background work or GPU overwork.
- **Bundle Size:** App takes too long to download or exceeds over-the-air limits.

## Step 2: Contextualize
Understand the environment: 
- Is this native (Swift/Kotlin) or cross-platform (React Native/Flutter)?
- Is the issue happening on all devices or specific older models?

## Step 3: Analyze Profiling Data
Ask for or analyze existing data from:
- **iOS:** Xcode Instruments (Time Profiler, Leaks, Allocations), MetricKit.
- **Android:** Android Studio Profiler (CPU, Memory, Network), Perfetto.
- **Cross-Platform:** React Native Performance Monitor, Flipper, Flutter DevTools.

## Step 4: Diagnosis
Identify common culprits based on data:
- *Cold start slow?* Heavy synchronous work on the main thread, parsing large JSON files on mount, instantiating too many singletons.
- *Scrolling jank?* Re-rendering heavy lists, calculating layout inside `onScroll`, heavy image decoding on the UI thread.
- *Memory leaks?* Retain cycles (iOS/Swift closures), forgotten listeners (Android contexts), large image caches not being cleared on memory warnings.

## Step 5: Actionable Mitigation
Provide a specific code-level or architecture-level fix. "Optimize your images" is not acceptable. "Use downsampling during image decode via `BitmapFactory.Options.inSampleSize` before loading into memory" is acceptable.

---

## Output Format

```markdown
# ⚡ Performance Audit Report

**Symptom:** [e.g., UI Scroll Jank on Android]
**Environment:** [e.g., React Native 0.72, Low-end Android devices]

## 🔍 Root Cause Analysis
Based on the provided metrics/context, the bottleneck appears to be:
[Detailed explanation of WHY this is happening. E.g., The JS thread is blocked during scroll because `setState` is being called excessively in the `onScroll` handler, causing a drop below 60FPS.]

## 🛠 Actionable Fix

### Fix 1: [Name of the fix, e.g., Debounce Scroll Events / Use Reanimated]
- **Current Pattern:** [What they are doing wrong]
- **Proposed Pattern:** [What they should do]
- **Code Example (if applicable):**
  ```javascript
  // Optimized code snippet
  ```

### Fix 2: [Secondary fix or long-term architecture change]
[Explanation]

## 📏 Measurement Strategy
*How to verify this worked:*
[E.g., "Run the React Native Performance Monitor. You should see the JS thread maintain 60FPS during aggressive scrolling, and the UI frame time should drop below 16ms."]
```

---

## When to Skip
- The user is asking about network API response times (that is backend latency, not mobile client performance).
- The user is asking about web browser performance (use a web/Lighthouse skill).

---

## Guardrails
- **Main Thread Rule:** Always prioritize freeing up the Main/UI thread. Never suggest solutions that move heavy work back to the main thread.
- **No Silver Bullets:** Do not blindly recommend caching or memoization without proving that re-computation is actually the bottleneck. Over-memoizing causes memory issues.

---

## References
See `references/EXAMPLES.md` for a worked case.

---

## 🔗 Next Steps & Handoffs
If you are executing the **Pre-Release Audit Flow** as defined in the Mobile ECOSYSTEM guide, and this performance audit passes, the next mandatory skill in the sequence is:
- `@mobile-security-auditor`

If you are executing the **Post-Launch Monitoring Flow** and have successfully optimized the app based on a crash/jank report, the flow concludes here or hands back to:
- `@crash-analyst` (to verify the fix in the next release)
