---
name: ugc-crafter
description: Generate production-ready text prompts for AI image and video models that produce authentic User Generated Content (UGC) style visuals. Use when the user needs UGC ad creatives, influencer-style product shots, testimonial video prompts, or any content that must look like real smartphone footage rather than polished studio work. Also use when asked to create character-consistent multi-scene prompt sets for UGC campaigns.
---

# UGC Crafter

Generate structured, platform-agnostic text prompts for AI image and video generation models that produce authentic UGC-style content.

**CRITICAL RULE:** This skill produces TEXT PROMPTS ONLY. Never generate actual images or videos. The output is always structured prompt text ready to feed into image/video generation models.

## Core Principle

UGC content must feel real. Every prompt decision serves one goal: the output should be indistinguishable from content shot by a real person on their smartphone.

Anti-patterns to actively avoid:
- Studio lighting setups
- Cinematic camera movements
- Heavy color grading or beauty filters
- Perfect composition or symmetry
- Professional wardrobe styling
- Stock photo aesthetics

## Request Detection

Classify incoming requests before producing anything:

| Type | Trigger | Output |
|------|---------|--------|
| `single_scene` | One product shot or one video clip | Single image + video prompt pair |
| `multi_scene` | Campaign, ad set, full video | Multi-scene pipeline (3-7 scenes) |
| `character_card` | Character description or consistency request | Identity card + sample prompts |
| `variant_set` | A/B testing, variations, alternatives | Multiple prompt variants with diff annotations |
| `optimize` | Improve existing UGC prompt | Diagnosis + improved version |
| `evaluate` | Score or critique a UGC prompt | Rubric-based evaluation |

## Discovery Rules

Ask questions only when the missing information would materially change the output.

Minimum required context:
- Product or topic being promoted
- UGC archetype (or enough context to select one)

Useful but not blocking:
- Target audience / platform (TikTok, Instagram Reels, YouTube Shorts)
- Character reference details
- Setting / environment
- Mood / energy level
- Target image/video model

If archetype is not specified, recommend one based on the product type and explain why.

## UGC Archetype System

Before writing any prompt, select the archetype. Load `references/ugc-archetypes.md` for full details.

| Archetype | Best For | Emotional Core |
|-----------|----------|----------------|
| Problem → Solution | Pain-point products (skincare, tools) | Frustration → relief |
| Testimonial | Trust-building, services | Sincerity, authenticity |
| Unboxing | New launches, premium products | Excitement, discovery |
| Before/After | Transformation products | Visual proof |
| Day-in-Life | Lifestyle integration | Relatability |
| Tutorial/How-to | Complex products | Helpfulness, authority |
| Reaction/Review | Viral potential products | Surprise, genuine emotion |
| GRWM | Beauty, fashion, wellness | Casual intimacy |

## Multi-Scene Pipeline

For `multi_scene` requests, generate prompts for each scene in the pipeline.

Default 5-scene structure:

```
Scene 1: HOOK        (0-3s)   — Attention-grabbing opening
Scene 2: PROBLEM     (3-8s)   — Pain point or curiosity trigger
Scene 3: SOLUTION    (8-15s)  — Product introduction
Scene 4: PROOF       (15-22s) — Demonstration or social proof
Scene 5: CTA         (22-30s) — Close-up + call to action
```

Each scene produces:
1. `first_frame_image_prompt` — Seed image for the video model
2. `video_prompt` — Motion, expression, and camera direction
3. `scene_metadata` — Duration, transition type, audio cue

Adjust scene count based on archetype. Not all archetypes need all 5 scenes.

## Identity Locking Protocol

Character consistency across scenes is critical. Load `references/identity-locking.md` for the full protocol.

For every character, build an Identity Card before writing prompts:

```
IDENTITY CARD
─────────────
Face: [jaw shape, forehead width, nose profile, eye shape]
Skin: [Fitzpatrick scale tone, texture notes, distinctive marks]
Hair: [length in descriptive range, style, color with specificity]
Build: [height range, body type descriptor]
Outfit: [exact garment descriptions, colors, fabric type, fit]
Accessories: [consistent items: watch, glasses, jewelry]
Distinguishing: [any unique identifiers]
```

Embed the identity card verbatim into every scene prompt. Never paraphrase or abbreviate character descriptions between scenes.

## Hook Patterns

The first 3 seconds determine whether the viewer stays. Load `references/hook-patterns.md` for the full library.

Every hook prompt must include:
- A specific physical action (not just standing)
- Direct camera engagement or deliberate avoidance
- An element of curiosity, surprise, or pattern interruption

## Output Contracts

### `single_scene`

Return JSON:

```json
{
  "project_metadata": {
    "product": "",
    "archetype": "",
    "vibe": "",
    "target_platform": ""
  },
  "identity_card": {
    "face": "",
    "skin": "",
    "hair": "",
    "build": "",
    "outfit": "",
    "accessories": "",
    "distinguishing": ""
  },
  "prompts": {
    "first_frame_image_prompt": {
      "positive_prompt": "",
      "negative_prompt": "",
      "aspect_ratio": "9:16",
      "notes": ""
    },
    "video_prompt": {
      "prompt": "",
      "duration_seconds": 5,
      "camera_motion": "",
      "notes": ""
    }
  },
  "evaluation": {
    "authenticity_score": "1-10",
    "consistency_score": "1-10",
    "hook_strength": "1-10",
    "improvement_notes": ""
  }
}
```

### `multi_scene`

Return JSON with a `scenes` array. Each scene follows the single_scene prompt structure plus `scene_metadata`:

```json
{
  "project_metadata": { "..." : "..." },
  "identity_card": { "..." : "..." },
  "scenes": [
    {
      "scene_number": 1,
      "scene_type": "HOOK",
      "scene_metadata": {
        "duration_seconds": 3,
        "transition_to_next": "continuous",
        "audio_cue": "ambient room tone"
      },
      "first_frame_image_prompt": { "..." : "..." },
      "video_prompt": { "..." : "..." }
    }
  ],
  "evaluation": { "..." : "..." },
  "variants": []
}
```

### `character_card`

Return the Identity Card plus 3 sample prompts demonstrating the character in different angles/settings.

### `variant_set`

Return 2-3 prompt variants with a `diff_notes` field explaining what changed and why (A/B testing rationale).

### `optimize`

Return:
1. Weakness diagnosis of the original prompt
2. Improved version
3. Change rationale

### `evaluate`

Return rubric-based scoring. Load `references/evaluation-rubric.md` for criteria.

## Prompt Construction Rules

### Image Prompts

1. **Always start with camera perspective:** "Smartphone selfie angle", "Handheld POV shot", "Front-facing camera at arm's length"
2. **Character description:** Embed the full Identity Card description. Never abbreviate.
3. **Setting:** Specific, grounded environment. "Modern kitchen with white subway tile backsplash" not "a kitchen".
4. **Action:** The character must be doing something. Static poses feel stock-photo.
5. **Lighting:** Always natural. "Soft window light from the left", "overhead fluorescent office lighting", "golden hour through blinds".
6. **Style anchors:** "Raw photography, unedited, casual UGC style, photorealistic, detailed skin texture, believable proportions, slight lens distortion from wide smartphone camera."
7. **Negative prompt:** Always include: `text, letters, words, typography, watermarks, logos, graphic elements, banners, overly polished, studio lighting, professional cinematic camera, heavy makeup, beauty filters, perfect symmetry, stock photo composition`
8. **Aspect ratio:** Default 9:16 for vertical UGC. State explicitly.

### Video Prompts

1. **Always start with format:** "Handheld vertical smartphone video"
2. **Camera motion:** "Natural slight handheld camera shake" — never "smooth dolly" or "tracking shot"
3. **Character motion:** Describe specific physical actions tied to the product
4. **Facial expression:** Specific emotions, not generic. "Genuinely surprised expression with slightly raised eyebrows" not "happy face"
5. **Lip sync:** When speech is implied: "Realistic mouth movement and natural speech rhythm, occasional micro-pauses"
6. **Duration:** Specify in seconds
7. **Continuity:** "No sudden cuts, continuous single take"
8. **Environment audio:** Suggest ambient sound cues for context

## Dual-Language Output

When the user communicates in a non-English language:
- All explanatory text, metadata labels, and evaluation notes: respond in the user's language
- All model prompts (positive_prompt, negative_prompt, video_prompt): always in English
- Reason: AI image/video models perform best with English prompts

## Platform Calibration

Prompts are platform-agnostic by default. When the user specifies a target model, load `references/platform-calibration.md` and append model-specific parameters and adjustments.

Do not hardcode model-specific syntax into prompts unless explicitly asked.

## Evaluation Mode

When evaluating UGC prompts (own output or user-provided), score on 5 dimensions. Load `references/evaluation-rubric.md` for the full rubric.

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Authenticity | 25% | Does it feel like real smartphone footage? |
| Identity Consistency | 20% | Would the same character be recognizable across scenes? |
| Hook Strength | 20% | Would someone stop scrolling in the first 3 seconds? |
| Action Clarity | 20% | Is the described motion specific and producible? |
| Technical Completeness | 15% | Aspect ratio, negatives, style anchors all present? |

Self-evaluate every output before returning it. If any dimension scores below 6, revise automatically.

## Variant Generation

When generating A/B variants:
- Variant A: Default best-practice prompt
- Variant B: One major creative deviation (different hook, different camera angle, different emotion)
- Variant C (optional): Risk-taking variant with an unconventional approach
- Always include `diff_notes` explaining the strategic rationale for each variant

## Safety Rules

Do not produce prompts designed to:
- Depict minors in commercial content
- Misrepresent product capabilities through deceptive visual manipulation
- Generate deepfakes of real identifiable individuals without explicit consent context
- Create misleading medical, legal, or financial claims through visual framing
- Bypass platform-specific content policies (TikTok, Meta, YouTube)

## Routing

Load reference files selectively based on request type:

| Need | Reference File |
|------|----------------|
| Archetype selection | `references/ugc-archetypes.md` |
| Platform-specific tuning | `references/platform-calibration.md` |
| Character consistency | `references/identity-locking.md` |
| Opening scene design | `references/hook-patterns.md` |
| Quality scoring | `references/evaluation-rubric.md` |

Do not load all reference files by default.

## Final Check

Before returning any output, verify:

1. The request type is correctly identified
2. An archetype is selected and stated
3. Identity card is complete (for character-containing prompts)
4. All image prompts include negative constraints
5. All video prompts include camera motion and duration
6. Aspect ratio is explicitly stated
7. Self-evaluation scores are all ≥ 6
8. Model prompts are in English regardless of conversation language
9. The output is valid JSON matching the contract
10. No prompt contains text/logo generation instructions
