# Platform Calibration Guide

Platform-agnostic prompts are the default. Apply calibration only when the user specifies a target model.

## Image Generation Models

### Flux (1.1 / Pro / Dev)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 100-500 tokens (descriptive natural language) |
| Aspect ratio syntax | `aspect_ratio: 9:16` (API) or specify in prompt |
| Negative prompt | Supported via `negative_prompt:` parameter |
| Style keywords | Prefers natural language descriptions over tags |
| Strength | Photorealism, text rendering, complex compositions |
| UGC-specific tips | Excels at natural skin textures. Use "raw smartphone photo" and "unedited" for UGC authenticity. Avoid "8k" or "cinematic" which push toward polish. |

**Flux UGC template adjustments:**
- Add: "shot on iPhone, slight lens distortion, natural color temperature"
- Avoid: quality boosters like "masterpiece", "best quality", "award-winning"

---

### Midjourney (v6 / v6.1)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 60-300 tokens (concise, keyword-rich) |
| Aspect ratio syntax | `--ar 9:16` |
| Negative prompt | `--no text, logos, watermarks` |
| Style keywords | `--style raw` (critical for UGC — disables Midjourney's aesthetic beautification) |
| Strength | Artistic interpretation, stylistic consistency |
| UGC-specific tips | ALWAYS use `--style raw`. Without it, outputs default to polished/artistic. Add `--s 50` or lower to reduce stylization. |

**Midjourney UGC template adjustments:**
- Always append: `--style raw --ar 9:16 --no text, logos, watermarks, studio lighting, beauty filter`
- Use `--s 0` to `--s 100` range for maximum authenticity
- Avoid: aesthetic keywords (ethereal, dreamy, magical)

---

### DALL-E 3

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 100-400 tokens (natural language) |
| Aspect ratio syntax | `size: 1024x1792` (portrait) |
| Negative prompt | Embed in prompt text: "Do not include any text, logos, or watermarks" |
| Style keywords | `style: natural` via API |
| Strength | Instruction following, text rendering |
| UGC-specific tips | DALL-E tends to beautify. Counter with explicit "imperfect" descriptors: "slightly out of focus background", "not perfectly centered", "natural imperfections visible". |

**DALL-E 3 UGC template adjustments:**
- Add explicit instruction: "This should look like a real smartphone photo, not a professional studio image"
- Counter-beautification: "asymmetric composition, slight motion blur, visible smartphone camera artifacts"

---

### Ideogram (v2 / v3)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 50-300 tokens |
| Aspect ratio syntax | Selectable in UI, or specify in prompt |
| Negative prompt | Supported via parameter |
| Style keywords | "Photo" style preset for realism |
| Strength | Text rendering, graphic design |
| UGC-specific tips | Best for UGC that includes product packaging with readable text. Less suited for pure character work. |

---

## Video Generation Models

### Kling (2.6 / 2.1)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 50-200 tokens (concise, action-focused) |
| Duration | 5s or 10s (per clip) |
| Aspect ratio | 9:16 vertical supported |
| Motion control | Supports camera motion presets |
| Strength | Human motion, facial expressions, lip sync |
| UGC-specific tips | Best-in-class for natural human movement. Specify "subtle handheld shake" explicitly. Keep prompts action-focused rather than descriptive. |

**Kling UGC template adjustments:**
- Lead with action: "A person holds up a product and speaks to camera"
- Motion: "Natural handheld camera movement, not stabilized, slight shake"
- Expression: Be specific — "slight smile forming, eyebrows raised briefly" not "happy expression"

---

### Google Veo (3 / 2)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 100-300 tokens (descriptive) |
| Duration | Up to 8s (Veo 3) |
| Aspect ratio | 9:16 supported |
| Motion control | Described in prompt |
| Strength | Cinematic quality, physics, complex scenes |
| UGC-specific tips | Veo defaults to high production quality. Actively counter with "amateur footage", "smartphone quality", "non-professional". Specify imperfections. |

**Veo UGC template adjustments:**
- Counter-polish: "Recorded on smartphone, not color-graded, natural white balance"
- Audio: Veo 3 supports audio — specify "ambient room noise, no background music"
- Reduce cinematic tendency: Avoid "dramatic", "epic", "beautiful" — use "natural", "casual", "everyday"

---

### Runway (Gen-3 Alpha / Gen-4)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 50-200 tokens |
| Duration | 5-10s |
| Aspect ratio | Vertical supported |
| Motion control | Motion brush, camera controls |
| Strength | Consistent motion, creative control |
| UGC-specific tips | Good for controlled transitions. The motion brush feature helps direct specific product interactions. |

---

### Pika (2.0)

| Parameter | Value |
|-----------|-------|
| Optimal prompt length | 50-150 tokens (brief) |
| Duration | 3-5s |
| Aspect ratio | Vertical supported |
| Motion control | Limited camera controls |
| Strength | Quick iterations, simple motions |
| UGC-specific tips | Best for simple, single-action UGC clips. Keep prompts short and focused on one action per generation. |

---

## Cross-Platform Prompt Adaptation Rules

When adapting a platform-agnostic prompt to a specific model:

1. **Adjust length:** Trim for Kling/Pika, expand for Flux/Veo
2. **Syntax conversion:** Add model-specific parameters (--ar, --style, etc.)
3. **Counter-beautification:** Models that default to polish (Veo, DALL-E, Midjourney without --style raw) need explicit "imperfection" descriptors
4. **Preserve identity:** Never shorten the character description during adaptation
5. **Negative prompt format:** Convert between parameter-based (Flux, MJ) and in-prompt (DALL-E) negative approaches

## Quick Reference: UGC Authenticity Keywords

Use these across all platforms:

**Positive (use):**
```
smartphone camera, handheld footage, natural lighting, unedited photo,
raw photography, everyday setting, casual style, authentic, relatable,
slight lens distortion, ambient noise, room tone, natural skin texture,
visible pores, asymmetric composition, genuine expression, unrehearsed
```

**Negative (avoid in prompt AND add to negatives):**
```
studio lighting, professional camera, cinematic, color graded, 4K film,
beauty filter, retouched, airbrushed, perfect skin, symmetrical composition,
bokeh wall, dramatic lighting, golden ratio, award-winning photography,
editorial, high fashion, magazine cover
```
