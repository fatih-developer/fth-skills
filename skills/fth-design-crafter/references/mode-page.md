# PAGE Mode — Page Strategy and Structure

Design a page or screen on top of the system in `DESIGN.md`. If no `DESIGN.md` exists, run FOUNDATIONS and SPEC first or state that the page uses provisional tokens.

## Step 1 — Essential questions

Ask or infer:

1. **Page type:** landing, dashboard, e-commerce, blog, portfolio, pricing, about, other.
2. **Primary goal:** sell, inform, convert, onboard, operate, profile, other.
3. **Audience:** developers, consumers, B2B buyers, internal staff, other.

## Step 2 — Page strategy summary

```
## Page Strategy Summary
- Page type:
- Page goal:
- Primary audience:
- Primary message: the one thing this page must communicate
- Primary CTA: the main action (or "none" for purely informational pages)
```

## Step 3 — Section architecture

Build sections from the visitor's questions in the order they ask them. Include a section only if it answers a real question with real content. Do not default to hero + logo strip + three feature cards + testimonials + pricing + FAQ.

Example for a **landing page** of a shipment-tracking product:

```
1. Hero — the concrete offer ("track every shipment from one screen") + primary CTA + a real product view
2. How it works — the 3 actual steps of the product flow
3. Proof — supplied customer quotes or measured results only; omit if none exist
4. Pricing or next step — only if the business publishes prices
5. Questions — real objections from sales or support, not filler
```

Example for a **dashboard**:

```
1. Navigation shell — sidebar or top bar
2. Primary status — the few numbers the user acts on today
3. Primary data view — main table or chart
4. Secondary panels — detail, filters, activity
5. Action bar — bulk actions, exports
```

## Step 4 — Rule check

Check the page against `references/page-rules.md` and record the result:

| Rule | Status | Notes |
|---|---|---|
| One primary message | | |
| No hero slider | | |
| Structure chosen by content | | |
| Mobile-first | | |
| Performance targets (LCP < 2.5s, INP < 200ms, CLS < 0.1) | | |
| Accessibility baseline | | |
| Functional motion only | | |
| Tokens only (no hardcoded colors, no gradients) | | |

## Step 5 — Optional enhancements

Only after the base is solid, and only with a stated benefit: scrollytelling for guided narratives, 3D/WebGL with a fallback, personalization as an enhancement layer, lightweight meaningful video.

## Page type matrix

| Page type | Primary focus | Key adaptation |
|---|---|---|
| Landing | Conversion, one message | Hero and CTA placement are critical |
| Dashboard / admin | Task efficiency | Dense but organized; hierarchy by importance |
| E-commerce | Product decision | Product, price, variants, delivery info, purchase control first |
| Blog / article | Reading | Typography first, minimal chrome |
| Portfolio | Work | Visual first, clean layout, work before bio |
| Pricing | Comparison | Table or up to three plan cards; clear CTA per plan |
| About / contact | Trust | People, story, clear contact channels |
| Error / empty states | Recovery | Plain message and the next action |

Per-type modulation details and worked examples: `references/page-rules.md` and `references/page-examples.md`.

## Forbidden defaults

Unless explicitly justified:

- Hero sliders and auto-rotating carousels
- Several competing primary CTAs in one focal area
- Decorative-only animation; missing reduced-motion fallback
- Decorative gradients, glow, glassmorphism
- Invented logos, testimonials, metrics, or customer counts
- Desktop-first layout logic; touch targets under 44×44px
- Text below 4.5:1 contrast
- Dense text walls without structure; heavy WebGL on simple pages

## Exception policy

A forbidden default may be broken only when you explain why it is necessary, the concrete benefit, and why it does not harm clarity, performance, or accessibility. If you cannot, keep the default rule.
