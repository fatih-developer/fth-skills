---
name: mobile-security-auditor
description: "Audit mobile app security against the OWASP Mobile Top 10: insecure storage, weak transport and certificate pinning, hardcoded secrets, and missing runtime protections, with remediation code. Use when the user asks for a mobile security review, before a release, or after finding exposed keys or tokens in an app."
---

# Mobile Security Auditor Protocol

Mobile apps run in hostile, untrusted environments (the user's device). Unlike a web server tucked behind a firewall, a mobile app can be decompiled, memory-dumped, and its network traffic intercepted by anyone holding the physical device. This skill enforces hard security boundaries on the client.

**Core principle:** Assume the device is compromised. Never trust the client. Never store secrets in plaintext.

---

## Workflow

```
1. Analyze the requested feature / current implementation
2. Check against OWASP Mobile Top 10 vulnerabilities
3. Audit Data at Rest (Storage Security)
4. Audit Data in Transit (Network Security)
5. Audit Runtime Defenses (Reverse Engineering/Tampering)
```

---

## Step 1: Implementation Analysis
Understand what the app is doing:
- Storing an API token or password?
- Communicating with a backend over HTTPS?
- Handling financials, PII, or health data?

## Step 2: OWASP Mobile Top 10
Cross-reference the implementation with common flaws:
- M1: Improper Platform Usage (Misusing Keychain, Intents).
- M2: Insecure Data Storage (Storing tokens in `AsyncStorage` or `UserDefaults`).
- M3: Insecure Communication (No certificate pinning, HTTP traffic).
- M4: Insecure Authentication (Relying purely on device ID).
- M5: Insufficient Cryptography (Using weak algorithms like MD5/SHA1).

## Step 3: Data at Rest (Storage)
How is data saved on the device?
- **Rule:** Never store JWTs, API keys, or passwords in unencrypted `SharedPreferences` (Android), `UserDefaults` (iOS), or React Native `AsyncStorage`.
- **Solution:** Always use the iOS **Keychain** and Android **Keystore / EncryptedSharedPreferences** (via libraries like `expo-secure-store` or `react-native-keychain`).

## Step 4: Data in Transit (Network)
HTTPS is not enough to stop a Man-in-the-Middle (MitM) attack if the user installs a rogue root certificate on their device (using tools like Charles Proxy).
- **Solution:** For high-security apps (banks, health), implement **Certificate Pinning** or **Public Key Pinning**. Hardcode the server's public key hash in the app so it only trusts that specific certificate.

## Step 5: Runtime Defenses
How do you stop a user from tampering with your app logic?
- **Obfuscation:** ProGuard / R8 for Android.
- **Root/Jailbreak Detection:** Check if the OS is compromised (e.g., checking for Cydia/Magisk paths). Warn the user or lock the app.
- **Anti-Debugging / Anti-Tampering:** iOS `ptrace` checks, Android SafetyNet / Play Integrity API.

---

## Output Format

````markdown
# 🛡️ Mobile Security Audit Report

**Feature/Area:** [e.g., User Authentication Token Storage]

## 🚨 Critical Security Vulnerabilities
*Must be fixed before release to prevent data breaches.*

1. **[Vulnerability, e.g., Insecure Data Storage (OWASP M2)]**
   - **Threat:** [E.g., Storing the JWT in `AsyncStorage` means any rooted device or malicious app with root access can read the token in plaintext from the app's data folder.]
   - **Remediation:** [E.g., Migrate storage to the hardware-backed Android Keystore and iOS Keychain utilizing `react-native-keychain`.]

## ⚠️ Medium-Risk Warnings
*Best practices that should be implemented.*

1. **[Risk, e.g., Insecure Communication (MitM Vulnerability)]**
   - **Threat:** [E.g., Users on public Wi-Fi could have their traffic intercepted if they are tricked into installing a rogue profile.]
   - **Mitigation:** [E.g., Implement strict Certificate Pinning for the `/login` endpoint.]

## 💡 Code Implementation

```javascript/swift/kotlin
// Insecure Pattern (DO NOT DO THIS):
await AsyncStorage.setItem('userToken', token);

// Secure Pattern:
import * as Keychain from 'react-native-keychain';
await Keychain.setGenericPassword('user', token);
```
````

---

## When to Skip
- The user is asking about server-side SQL injection or backend Kubernetes security (this skill focuses on the mobile client).

---

## Guardrails
- **Hardcoded Secrets:** Explicitly warn developers against hardcoding API Secrets or third-party paid keys directly into the app source code, even if obfuscated. Strings can always be extracted. Route calls through a secure backend proxy instead.
- **Root Detection Bypass:** Remind developers that client-side Jailbreak/Root detection is an arms race and can be bypassed. It is a defense-in-depth layer, not a silver bullet.

---

## References
See `references/EXAMPLES.md` for a worked case.

## 🔗 Next Steps & Handoffs

<!-- BEGIN GENERATED: handoffs (generated from the ecosystem workflow map by build_ecosystems.py — do not edit by hand) -->
**Ecosystem:** `@ecosystem-mobile` — Mobile App Domain.

**Workflows:**
- **Pre-Release Audit Flow** (`mobile-pre-release-audit`, step 3 of 3): last step → once it passes, complete the workflow and report the outcome.

**Direct handoffs:**
- `@auth-flow-designer` — Findings involve token storage or backend auth design.

**Handoff contract:** pass results to the next skill through an inline *Handoff* block in your reply with the fields `skill`, `workflow`, `created_at`, `inputs`, `summary`, and `next` (the handoff contract of `@ecosystem-mobile`). If a next skill is not installed, continue with its step from the ecosystem map, or install it with `npx skills add fatih-developer/fth-skills --skill <name>` after the user agrees.
<!-- END GENERATED: handoffs -->
