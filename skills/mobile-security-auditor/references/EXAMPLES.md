# Examples

## Example — Secure Token Storage in React Native

**User Request:** 
"I am building a React Native app that connects to my backend. When the user logs in, I receive a JWT token. I need to keep them logged in across sessions, so I'm saving it using `AsyncStorage.setItem('token', jwt)`. For security, I'm hiding my Stripe Secret Key in my `.env` file and using `react-native-dotenv` to access it. Is this secure enough for production?"

**Skill Response:**

```markdown
# 🛡️ Mobile Security Audit Report

**Feature/Area:** Authentication Storage and Secret Management

## 🚨 Critical Security Vulnerabilities
*Must be fixed before release to prevent data breaches.*

1. **Insecure Data Storage (OWASP M2)**
   - **Threat:** You are storing the JWT in `AsyncStorage`. `AsyncStorage` on Android writes plain text XML/JSON files to the app's local directory. If a user's device is rooted, or if there is a backup vulnerability, attackers can read your `token` in plain text and hijack the user's session indefinitely.
   - **Remediation:** Remove `AsyncStorage` for credentials. You must use the hardware-backed OS secure storage (Keychain on iOS, Keystore on Android). Use a library like `react-native-keychain` or `expo-secure-store`.

2. **Client-Side Secret Exposure (OWASP M1/M9)**
   - **Threat:** You mentioned hiding a Stripe Secret Key in a `.env` file and reading it in React Native. **`.env` files in mobile apps are NOT secure.** React Native bundles all environment variables into the final Javascript bundle (`index.android.bundle`). Anyone can unzip your `.apk`/`.ipa`, open the bundle in a text editor, and find your Stripe Secret Key, giving them full access to your Stripe account.
   - **Remediation:** NEVER put secret keys (Stripe, AWS, Database credentials) in a mobile app. You must move the Stripe integration logic to your backend server. The mobile app should only call your backend, and your backend securely talks to Stripe.

## ⚠️ Medium-Risk Warnings

1. **Token Expiration & Refresh Logic**
   - **Threat:** If the JWT never expires, a stolen token is a permanent compromise.
   - **Mitigation:** Ensure your backend issues short-lived JWTs (e.g., 15 minutes) and a long-lived Refresh Token. Store BOTH in the secure Keychain.

## 💡 Code Implementation

### Fixing the Token Storage

```javascript
// ❌ Insecure Pattern (Delete this):
import AsyncStorage from '@react-native-async-storage/async-storage';
await AsyncStorage.setItem('token', jwt);

// ✅ Secure Pattern (Use this):
import * as Keychain from 'react-native-keychain';

// Save the token securely
await Keychain.setGenericPassword('auth_token', jwt, {
  service: 'com.myapp.auth'
});

// Retrieve the token securely on next launch
const credentials = await Keychain.getGenericPassword({
  service: 'com.myapp.auth'
});
if (credentials) {
  console.log('Successfully retrieved token');
  const token = credentials.password;
}
```
```
