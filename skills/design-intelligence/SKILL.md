---
name: design-intelligence
description: 'Design and review web interfaces with trend-aware, performance-conscious, accessible rules. Triggers on design a page, build UI, review my site, audit this page, create a landing page, check my dashboard.'
---

# design-intelligence

AI-powered web design skill that guides both **generation** and **review** of web interfaces. Works for any framework (HTML/CSS, React, Vue, Svelte, Next.js, Nuxt, etc.).

---

## Modes

This skill operates in two modes. Identify the request type and apply the corresponding instructions.

### GENERATE Mode

**Trigger:** User wants to design, build, create, or scaffold a web page or UI.

**Approach:**
1. Ask the 3 essential questions (or infer from context)
2. Produce a Page Strategy Summary
3. Define Section Architecture
4. Apply UX Rule Check from `references/WEB_RULES.md`
5. Flag optional enhancements (only after base is solid)

### REVIEW Mode

**Trigger:** User wants to review, audit, critique, or check an existing page or design.

**Approach:**
1. Score each of the 12 rubric categories (1-5)
2. Classify issues: Critical / Important / Nice to Improve
3. Issue final recommendation: **approve** / **revise** / **redesign**
4. Reference `references/REVIEW_RUBRIC.md` for detailed category guidance

---

## Decision Tree

```
User request
    │
    ├─ "tasarla / oluştur / build / create" → GENERATE Mode
    │       └─ What page type? (landing, dashboard, e-commerce, blog, portfolio, pricing, about)
    │
    └─ "incele / audit / review / kontrol et / eleştir" → REVIEW Mode
            └─ Is this a live URL or code/snippet?
                    ├─ Live URL → navigate, snapshot, score
                    └─ Code/snippet → analyze directly
```

---

## GENERATE Mode Instructions

### Step 1 — Essential Questions

If not already clear, ask or infer:

1. **Page type:** landing / dashboard / e-commerce / blog / portfolio / pricing / about / other
2. **Primary goal:** sell / inform / convert / onboard / dashboard / profile / other
3. **Target audience:** developers / consumers / B2B / internal / other

### Step 2 — Page Strategy Summary

Output:

```
## Page Strategy Summary
- Page type: [type]
- Page goal: [what the page must accomplish]
- Primary audience: [who uses this page]
- Primary message: [the one thing this page must communicate]
- Primary CTA: [the main action — can be "none" for purely informational pages]
```

### Step 3 — Section Architecture

List ordered sections for the page type. Example for **landing page**:

```
1. Hero — single message + primary CTA
2. Trust indicators — logos, stats, social proof
3. Feature bento grid — modular card cluster
4. Results or stats — measurable impact
5. Testimonial or proof — human evidence
6. FAQ — objection handling
7. Final CTA — last conversion push
```

Example for **dashboard**:

```
1. Navigation shell — sidebar or top bar
2. KPI cards — top-level metrics
3. Primary data view — main table/chart
4. Secondary panels — detail, filters, activity
5. Action bar — bulk actions, exports
```

### Step 4 — UX Rule Check

Confirm each rule is satisfied. Reference `references/WEB_RULES.md` for the full rule text.

| Rule | Status | Notes |
|------|--------|-------|
| One Primary Message | ✅ | |
| No Hero Slider | ✅ | |
| Modular Layout | ✅ | |
| Mobile-First | ⚠️ | Side nav collapses to hamburger on mobile |
| Performance Targets | ✅ | LCP < 2.5s, INP < 200ms, CLS < 0.1 |
| Accessibility Baseline | ✅ | Semantic HTML, focus states, contrast |
| Functional Motion Only | ✅ | |
| Forbidden Defaults | ✅ | No slider, no carousel, no decoration-only animation |

### Step 5 — Optional Enhancements

Only after the base solution is solid. Apply `references/WEB_RULES.md` Section "Advanced Effects":

- **scrollytelling** — only for guided narrative (product launches, brand stories)
- **3D/WebGL** — only when it adds real explanatory value + has fallback
- **AI personalization** — only as enhancement layer, never as structural replacement
- **video background** — only if meaningful + lightweight + contrast-safe

---

## REVIEW Mode Instructions

### Step 1 — Gather Information

- **Live URL:** Navigate, take snapshot, analyze
- **Code snippet:** Read directly, identify framework and structure
- **Image:** Describe visually, identify layout patterns

### Step 2 — Score 12 Categories

Score each category **1-5** and record justification:

| # | Category | Score (1-5) | Justification |
|---|----------|-------------|---------------|
| 1 | Message Clarity | | |
| 2 | Hero Focus | | |
| 3 | CTA Clarity | | |
| 4 | Modular Structure | | |
| 5 | Visual Hierarchy | | |
| 6 | Mobile Usability | | |
| 7 | Touch Comfort | | |
| 8 | Performance Safety | | |
| 9 | Accessibility Quality | | |
| 10 | Motion Usefulness | | |
| 11 | Visual Consistency | | |
| 12 | Advanced Effects Justification | | |

Reference `references/REVIEW_RUBRIC.md` for detailed scoring guidance per category.

### Step 3 — Issue Classification

Classify every issue into one of three tiers:

**Critical** — damages clarity, usability, accessibility, performance, or conversion path:
- Hero slider hiding primary value
- Unreadable contrast in hero
- Primary CTA unclear or missing
- Broken mobile flow
- No keyboard accessibility
- CLS-causing layout shifts

**Important** — weakens quality without breaking the page:
- Inconsistent spacing system
- Weak hierarchy in secondary sections
- Unnecessary media weight
- Mixed card patterns

**Nice to Improve** — polish opportunities:
- Better proof ordering
- Cleaner CTA wording
- Tighter typography rhythm

### Step 4 — Final Recommendation

```
## Final Recommendation: [approve / revise / redesign]

[approve] — No critical issues, page is clear and usable
[revise] — No structural failure, but important issues weaken effectiveness
[redesign] — Structurally confused, hero strategy broken, mobile poor, systemic problems
```

---

## Page Type Matrix

Rules adapt based on page type. The default rules in `references/WEB_RULES.md` apply to all types. This matrix highlights per-type emphasis.

| Page Type | Primary Focus | Key Adaptation |
|-----------|--------------|---------------|
| **Landing page** | Conversion, single message | Hero is critical, CTA placement paramount |
| **Dashboard / Admin** | Data density, task efficiency | High information density OK, hierarchy by importance |
| **E-commerce** | Product discovery, conversion | Product hero, gallery, clear pricing, CTA priority |
| **Blog / Article** | Readability, content first | Typography-first, minimal chrome, distraction-free |
| **Portfolio** | Work showcase, personality | Visual-first, project cards, clean layout |
| **SaaS Pricing** | Plan comparison, decision support | Table or grid layout, feature clarity, CTA per plan |
| **About / Contact** | Trust, human connection | Team, story, clear contact channels |
| **Error / Empty states** | Clarity, next action | Friendly message, clear CTA, recovery path |

### Per-Type Rule Modulations

**Dashboard / Admin panel:**
- Rule 1 (One Primary Message): Relaxed — data density is expected, but primary KPIs must be immediately visible
- Rule 3 (Modular Layout): Strongly encouraged — dense data must be chunked into cards/tables/panels
- Rule 4 (Hierarchy by Size): Critical — larger blocks for primary metrics, smaller for secondary

**E-commerce product page:**
- Rule 1 (One Primary Message): Product = hero, single product focus
- Rule 9 (Mobile-First): Critical — mobile commerce dominates
- Rule 2 (No Hero Slider): Product gallery is OK (thumbnails/video), carousel is not

**Blog / Article:**
- Rule 1 (One Primary Message): Article headline = primary message
- Rule 18 (Typography as Structure): Critical — readability is the product
- Rule 3 (Modular Layout): Article body is linear, sidebar/modules are modular

---

## Forbidden Defaults

Unless explicitly justified and explainable, these are **never acceptable**:

- Hero sliders / auto-rotating carousels
- Multiple competing primary CTAs in the same focal area
- Decorative-only animation
- Desktop-first layout logic
- Random asymmetry or broken reading order
- Dense text walls without modular structure
- Heavy WebGL on basic pages
- AI-driven navigation changes that reduce predictability
- Unreachable touch targets under 44×44 px on mobile
- Content that breaks below 4.5:1 contrast ratio
- Pages without reduced-motion fallback

---

## Exception Policy

A forbidden default **may be broken** only if the agent:
1. Explains why the exception is necessary
2. Describes the concrete benefit it creates
3. Confirms it does not harm clarity, performance, or accessibility

If that explanation cannot be made convincingly, **keep the default rule**.

---

## Quick Reference

**GENERATE workflow:**
```
1. Identify page type → 2. Ask essential questions → 3. Page Strategy Summary
→ 4. Section Architecture → 5. UX Rule Check → 6. Optional Enhancements
```

**REVIEW workflow:**
```
1. Gather info (URL or code) → 2. Score 12 categories (1-5)
→ 3. Classify issues → 4. Final recommendation (approve/revise/redesign)
```

**Core reading:**
- `references/WEB_RULES.md` — 27+ rules with per-type adaptations
- `references/REVIEW_RUBRIC.md` — 12 scoring categories with detailed guidance
- `references/EXAMPLES.md` — concrete examples per page type
