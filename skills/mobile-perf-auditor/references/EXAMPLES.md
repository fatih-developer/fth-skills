# Examples

## Example — React Native FlatList Jank

**User Request:** 
"My React Native app has a FlatList that renders about 500 items (images and text). When I scroll fast on my older Android test device, it stutters terribly and shows blank white space before the items load. iOS is mostly fine. How do I fix this?"

**Skill Response:**

```markdown
# ⚡ Performance Audit Report

**Symptom:** UI Scroll Jank and Blank Item Rendering (FlatList)
**Environment:** React Native, Older Android Devices

## 🔍 Root Cause Analysis
Based on the symptoms, there are two distinct bottlenecks occurring simultaneously:
1. **Blank Space on Scroll:** This means the scroll speed is exceeding the `FlatList` render window. The JS thread cannot calculate and pass the UI updates over the bridge to the Native thread fast enough.
2. **Scroll Stuttering (Jank):** Heavy image decoding and layout calculations on older Android CPUs are blocking the main thread, causing frame drops below 60 FPS (taking longer than 16.6ms per frame).

## 🛠 Actionable Fix

### Fix 1: Implement FlatList Optimization Props
- **Current Pattern:** Likely using default `FlatList` props which aren't tuned for heavy image lists.
- **Proposed Pattern:** Optimize the render window, use `getItemLayout` to skip measurement, and implement `initialNumToRender`.

- **Code Example:**
  ```javascript
  <FlatList
    data={items}
    renderItem={renderItem}
    keyExtractor={item => item.id}
    // Optimizations:
    initialNumToRender={10} // Render enough to fill the screen
    maxToRenderPerBatch={5} // Reduce items rendered per frame
    windowSize={5} // Reduce memory by keeping fewer screens rendered
    removeClippedSubviews={true} // Unmount components off-screen (Great for Android)
    // CRITICAL: If items have fixed height, skip dynamic measurement
    getItemLayout={(data, index) => (
      {length: 120, offset: 120 * index, index}
    )}
  />
  ```

### Fix 2: Optimize Image Decoding (FastImage)
- **Current Pattern:** Using the standard React Native `<Image>` component, which has known memory and caching inefficiencies on Android for long lists.
- **Proposed Pattern:** Switch to `react-native-fast-image`. It uses Glide on Android, which handles aggressive caching, memory management, and background thread decoding much better than the default implementation.

## 📏 Measurement Strategy
*How to verify this worked:*
1. Open the dev menu and enable "Perf Monitor".
2. Scroll aggressively. Both the JS and UI numbers should stay near 60.
3. Check the memory usage in Android Studio Profiler. FastImage + `removeClippedSubviews` should keep the memory curve flat as you scroll down the 500 items, instead of constantly climbing.
```
