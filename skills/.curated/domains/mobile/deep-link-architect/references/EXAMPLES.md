# Examples

## Example — Profile Sharing Links

**User Request:** 
"I want users to be able to share their profiles via a link like `https://fatihunal.dev/profile/123`. If someone clicks this on their phone, it should open my React Native app directly to that profile. If they don't have the app, it should just go to the website. How do I set this up for both iOS and Android?"

**Skill Response:**

```markdown
# 🔗 Deep Link Architecture Plan

**Domain:** `https://fatihunal.dev`
**Routing Paths:** `/profile/*`

## 🍎 iOS Universal Links

### 1. Hosted File (`apple-app-site-association`)
```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAMID.com.fatihunal.app",
        "paths": [ "/profile/*" ]
      }
    ]
  }
}
```
*Host this at: `https://fatihunal.dev/.well-known/apple-app-site-association`. **Ensure there is no `.json` extension and the Content-Type header is `application/json`.***

### 2. Xcode Entitlements
1. Open up your Xcode workspace.
2. Go to the Signing & Capabilities tab.
3. Add the Associated Domains capability.
4. Add: `applinks:fatihunal.dev`

## 🤖 Android App Links

### 1. Hosted File (`assetlinks.json`)
```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.fatihunal.app",
    "sha256_cert_fingerprints": ["YOUR_APP_SHA256_FINGERPRINT"]
  }
}]
```
*Host this at: `https://fatihunal.dev/.well-known/assetlinks.json`*

### 2. Android Manifest (`AndroidManifest.xml`)
Add this intent filter inside your `<activity>` block (usually `MainActivity`):
```xml
<intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="fatihunal.dev" android:pathPrefix="/profile/" />
</intent-filter>
```

## 🔄 In-App Routing Strategy (React Navigation)
Update your Navigation Container's linking prop to catch the URL and parse the ID:

```javascript
const linking = {
  prefixes: ['https://fatihunal.dev', 'fatihapp://'],
  config: {
    screens: {
      ProfileFlow: {
        path: 'profile/:id',
        parse: {
          id: (id) => `${id}`,
        },
      },
    },
  },
};

// <NavigationContainer linking={linking}>
```

## 🛡 Fallback & Target Testing
- **Fallback:** If the app is not installed, the OS opens standard Safari/Chrome to `https://fatihunal.dev/profile/123`. Your web team must ensure the website handles this route gracefully (perhaps showing the profile and a "Download App" banner).
- **Test iOS:** `xcrun simctl openurl booted "https://fatihunal.dev/profile/123"`
- **Test Android:** `adb shell am start -W -a android.intent.action.VIEW -d "https://fatihunal.dev/profile/123" com.fatihunal.app`
```
