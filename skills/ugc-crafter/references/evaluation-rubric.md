# UGC Prompt Evaluation Rubric

Score every generated prompt across 5 dimensions. Use this rubric for self-evaluation (built into every output) and for explicit evaluation requests.

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 9-10 | Exceptional — production-ready, no revisions needed |
| 7-8 | Strong — minor tweaks optional |
| 5-6 | Acceptable — usable but has clear improvement areas |
| 3-4 | Weak — needs significant revision before use |
| 1-2 | Failing — fundamentally flawed, do not use |

**Minimum passing threshold:** 6 per dimension, 7 overall average.

If any dimension scores below 6, auto-revise before returning the output.

---

## Dimension 1: Authenticity (25% weight)

Does the prompt reliably produce content that looks like real smartphone footage?

| Score | Criteria |
|-------|----------|
| 9-10 | Explicitly specifies smartphone camera, natural lighting, imperfections. Includes anti-polish descriptors. Would be mistaken for real footage. |
| 7-8 | Natural look described but missing 1-2 key authenticity markers (e.g., lens distortion, asymmetric composition). |
| 5-6 | Generally natural but includes terms that could push toward polish (e.g., "beautiful lighting", "stunning detail"). |
| 3-4 | Mixed signals — some UGC language but also cinematic/studio terms. |
| 1-2 | Reads like a stock photo or commercial production prompt. |

**Red flags (auto-deduct 2 points):**
- "Cinematic lighting" or "dramatic lighting"
- "Perfect composition" or "golden ratio"
- "8K" or "ultra HD" quality descriptors
- "Beauty filter" or "retouched"
- "Professional studio" anything

---

## Dimension 2: Identity Consistency (20% weight)

Would the character be recognizable across all scenes in the set?

| Score | Criteria |
|-------|----------|
| 9-10 | Full Identity Card embedded verbatim in every scene. Face, hair, skin, outfit, accessories all consistent. |
| 7-8 | Character described consistently but one minor detail varies (e.g., accessory mentioned in some scenes but not all). |
| 5-6 | Core features consistent but description is shortened or paraphrased between scenes. |
| 3-4 | Character described differently across scenes (different adjectives, missing details). |
| 1-2 | No consistent character description. Each scene could generate a different person. |

**Red flags (auto-deduct 2 points):**
- Outfit described differently between scenes
- Hair color or length changing
- Using "same person as before" instead of re-describing
- Missing Identity Card entirely

---

## Dimension 3: Hook Strength (20% weight)

Would the opening frame/scene make someone stop scrolling?

| Score | Criteria |
|-------|----------|
| 9-10 | Specific physical action, strong curiosity trigger, immediate visual interest. Follows a proven hook pattern. |
| 7-8 | Good opening but could be slightly more specific or attention-grabbing. |
| 5-6 | Opens with relevant content but lacks urgency or pattern interrupt. |
| 3-4 | Generic opening — character standing still, smiling at camera. |
| 1-2 | No hook strategy. Starts with a static establishing shot or fade-in. |

**Evaluation questions:**
- Is the character DOING something in the first frame?
- Is there a visual element that breaks the scrolling pattern?
- Would this create curiosity about what happens next?
- Does the hook match the selected archetype?

---

## Dimension 4: Action Clarity (20% weight)

Are the described motions specific enough for an AI model to reproduce?

| Score | Criteria |
|-------|----------|
| 9-10 | Every motion is specific and physical: body part, direction, speed, accompanying expression. |
| 7-8 | Most actions are clear but one action is vague (e.g., "interacts with product" without specifying how). |
| 5-6 | General actions described but lack physical specificity (e.g., "shows the product" instead of "holds product in right hand at shoulder height"). |
| 3-4 | Actions are abstract or emotional only (e.g., "excitedly presents the product"). |
| 1-2 | No specific actions. Character is described statically. |

**Specificity checklist:**
- [ ] Which hand holds the product?
- [ ] What is the other hand doing?
- [ ] Is the facial expression described beyond one word?
- [ ] Is camera distance/angle specified?
- [ ] Is the speed/tempo of motion indicated?
- [ ] Is the direction of gaze specified?

---

## Dimension 5: Technical Completeness (15% weight)

Are all structural requirements present?

| Score | Criteria |
|-------|----------|
| 9-10 | All elements present: positive prompt, negative prompt, aspect ratio, duration (video), camera motion (video), model notes. |
| 7-8 | All critical elements present, one optional element missing (e.g., model notes). |
| 5-6 | Missing one critical element (e.g., no negative prompt or no aspect ratio). |
| 3-4 | Missing multiple critical elements. |
| 1-2 | Unstructured text that cannot be directly fed to a model. |

**Required elements checklist:**

For image prompts:
- [ ] Positive prompt with camera perspective, character, setting, action, lighting, style anchors
- [ ] Negative prompt with text/logo/polish exclusions
- [ ] Aspect ratio specified (default 9:16)

For video prompts:
- [ ] Format specification (handheld vertical)
- [ ] Character motion with physical specificity
- [ ] Camera motion (handheld shake)
- [ ] Facial expression details
- [ ] Duration in seconds
- [ ] Continuity instruction (no cuts)

---

## Overall Score Calculation

```
Overall = (Authenticity × 0.25) + (Identity × 0.20) + (Hook × 0.20) + (Action × 0.20) + (Technical × 0.15)
```

| Overall Score | Verdict | Action |
|---------------|---------|--------|
| 8.0+ | PASS — Production Ready | Ship as-is |
| 7.0-7.9 | PASS — Minor Polish | Note improvement areas, ship |
| 6.0-6.9 | CONDITIONAL — Needs Revision | Auto-revise weak dimensions |
| Below 6.0 | FAIL — Major Rewrite | Do not return, rewrite completely |

---

## Variant Evaluation

When generating A/B variants, additionally score:

| Criterion | What to Check |
|-----------|---------------|
| **Differentiation** | Are variants meaningfully different, not just word swaps? |
| **Strategic Rationale** | Does each variant test a specific hypothesis? |
| **Risk Distribution** | Is there a safe variant AND a risk-taking variant? |
| **Shared Identity** | Do all variants use the same Identity Card? |

---

## Quick Evaluation Template

For inline self-evaluation in the output JSON:

```json
{
  "evaluation": {
    "authenticity_score": 8,
    "consistency_score": 9,
    "hook_strength": 7,
    "action_clarity": 8,
    "technical_completeness": 9,
    "overall_score": 8.15,
    "verdict": "PASS — Production Ready",
    "improvement_notes": "Hook could use a stronger curiosity trigger. Consider opening with the result visible before showing the process."
  }
}
```
