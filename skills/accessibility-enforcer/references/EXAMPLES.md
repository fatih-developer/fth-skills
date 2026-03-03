# Examples

## Example — Form Validation Error Message

**User Request:** 
"I'm building a login form in React Native. If the user enters the wrong password, the border turns red and a small '!' icon appears next to the input. We don't have text space for an error message. Is this okay?"

**Skill Response:**

```markdown
# ♿ Accessibility Audit Report

**Component / View:** Login Form Password Input

## 🚨 Critical VoiceOver/TalkBack Issues
*Issues blocking screen reader users from using the feature.*

1. **Visual-Only Error Indicators**
   - **Problem:** Color alone is not sufficient to convey meaning (WCAG 1.4.1). A colorblind user cannot see the red border, and a VoiceOver/TalkBack user cannot 'see' the red border or the '!' icon unless it is specifically announced. They will not know their password was rejected.
   - **Fix:** You must provide an audible error announcement explicitly linked to the input state, and you should provide a text-based error message (even a visually hidden one) instead of relying purely on an icon and color.

## ⚠️ UX / Interaction Warnings

1. **Focus Management on Error**
   - **Problem:** After a failed login attempt, if focus remains on the 'Submit' button, the user might not realize the input above them changed to an error state.
   - **Mitigation:** Move screen reader focus to the input field or an error summary component when the error occurs.

## 💡 Code Implementation

```javascript
// Before (Inaccessible):
<View style={{ borderColor: isError ? 'red' : 'gray' }}>
  <TextInput secureTextEntry onChangeText={setPassword} />
  {isError && <Icon name="exclamation" />}
</View>
<Button title="Login" onPress={submit} />

// After (Accessible):
// Note: We use accessibilityState to indicate the error to screen readers, 
// and accessibilityHint to explain what to do. The icon is hidden from SR.

<View style={{ borderColor: isError ? 'red' : 'gray' }}>
  <TextInput 
    secureTextEntry 
    onChangeText={setPassword}
    accessibilityLabel="Password"
    accessibilityState={{ error: isError }}
    accessibilityHint={isError ? "Incorrect password. Please try again." : ""}
  />
  {isError && (
    <Icon 
      name="exclamation" 
      accessible={false} // purely visual, SR gets the state from TextInput
      importantForAccessibility="no" 
    />
  )}
</View>
```
```
