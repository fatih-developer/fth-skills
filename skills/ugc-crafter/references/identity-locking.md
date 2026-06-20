# Identity Locking Protocol

Ensuring character consistency across multiple AI-generated scenes.

## The Problem

AI image and video models generate each frame independently. Without precise, repeated character descriptions, the same "person" will look different across scenes — breaking the illusion of authentic UGC content.

## Identity Card Format

For every character, build this card BEFORE writing any prompt:

```
IDENTITY CARD
─────────────────────────────────────────
ID:             [unique identifier, e.g., "talent-A"]
Gender:         [male / female / non-binary]
Age Range:      [e.g., late 20s, mid-30s]

FACE
  Jaw:          [round / square / oval / heart / angular]
  Forehead:     [narrow / broad / high / low]
  Nose:         [straight / slightly upturned / broad / narrow / prominent bridge]
  Eyes:         [shape + color, e.g., "almond-shaped, dark brown"]
  Brows:        [thick / thin / arched / straight / bushy]
  Lips:         [full / thin / wide / cupid's bow]
  Distinctive:  [dimples, moles, freckles, scar, etc.]

SKIN
  Tone:         [Fitzpatrick I-VI or descriptive: fair, light olive, medium brown, deep brown]
  Texture:      [smooth, visible pores, light acne scarring, freckled]
  Condition:    [sun-kissed, pale winter skin, natural glow]

HAIR
  Length:       [descriptive: chin-length, shoulder-length, buzz cut, waist-length]
  Style:        [straight, wavy, curly, coily, messy bun, slicked back, loose ponytail]
  Color:        [specific: warm chestnut brown, platinum blonde, jet black with subtle highlights]
  Texture:      [fine, thick, coarse, silky]

BUILD
  Height:       [range: short, average height, tall — avoid exact measurements]
  Type:         [slim, athletic, average, stocky, curvy, lean]
  Posture:      [upright, slightly slouched, relaxed]

OUTFIT
  Top:          [exact description: "oversized heather gray crewneck sweatshirt"]
  Bottom:       [exact description: "high-waisted medium wash straight-leg jeans"]
  Footwear:     [if visible: "white canvas sneakers, slightly worn"]
  Layer:        [jacket, cardigan, if applicable]
  Fit:          [loose, fitted, oversized, cropped]

ACCESSORIES
  Primary:      [glasses, watch, necklace — anything that should appear in every scene]
  Secondary:    [items that may appear in some scenes]

DISTINGUISHING
  Mannerisms:   [how they hold things, dominant hand, posture habits]
  Voice energy: [calm, energetic, soft-spoken — for video prompt direction]
─────────────────────────────────────────
```

## Usage Rules

### Rule 1: Embed Completely, Every Time

The full Identity Card description must appear in EVERY prompt for that character. Never abbreviate, paraphrase, or use shorthand like "same character as before."

**Why:** Each generation is independent. The model has no memory. Shorthand = inconsistency.

### Rule 2: Lock Outfit Across Scenes

Unless the archetype demands a wardrobe change (GRWM), the character wears the exact same outfit in every scene. Describe it identically every time.

**Exception:** Day-in-Life archetype may include one wardrobe change (morning → evening). Document both outfits in the card.

### Rule 3: Consistent Lighting Descriptors

The same character under different lighting looks different. Keep lighting consistent across scenes, or if it changes (indoor → outdoor), adjust skin tone descriptors to match.

### Rule 4: Anchor with Accessories

Consistent accessories (a specific watch, pair of glasses, ring) help reinforce identity even when the face varies slightly between generations.

### Rule 5: Face Description Priority Order

When token limits force trimming, prioritize in this order:
1. Jaw shape + eye shape + eye color (most impactful for recognition)
2. Skin tone + hair color + hair length
3. Nose profile + brows
4. Lips + distinctive marks
5. Build + posture

Never trim categories 1-2.

## Multi-Character Scenes

When a scene includes multiple characters:

1. Assign each character a unique ID (talent-A, talent-B)
2. Create separate Identity Cards for each
3. In the prompt, describe each character in a separate paragraph
4. Use spatial anchoring: "On the left, [talent-A description]... On the right, [talent-B description]..."
5. Ensure contrasting features between characters (different hair color, different outfit color) to help the model distinguish them

## Consistency Testing

After generating prompts for a multi-scene set, perform this quick check:

- [ ] Is the same face structure described in every scene?
- [ ] Is the exact same outfit described (word for word)?
- [ ] Are accessories mentioned consistently?
- [ ] If lighting changes between scenes, is this intentional and noted?
- [ ] Are no new physical features introduced mid-sequence?
- [ ] Is the character's dominant hand consistent?

If any check fails, revise before outputting.
