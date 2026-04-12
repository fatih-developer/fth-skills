# REVIEW_RUBRIC — 12-Category Scoring Guide

Use this rubric to review existing or generated web pages. Score each category 1–5, classify issues, and issue a final recommendation.

**Scoring scale:**
- 1 = poor (major problems, nearly unusable)
- 2 = weak (noticeable issues, usable but frustrating)
- 3 = acceptable (adequate, some weaknesses)
- 4 = strong (good quality, minor improvements possible)
- 5 = excellent (best-in-class, no meaningful improvements needed)

---

## 1. Message Clarity

**Question:** Does the page communicate one dominant message quickly and clearly?

**Score guidance:**
- 1: Confusing, fragmented, or no discernible primary message
- 3: Understandable but not sharply focused; user must work to understand the point
- 5: Immediate, clear, memorable primary message; user gets it within 1–2 seconds

**What to look for:**
- Strong H1 that states the core value
- Concise supporting copy (1–2 sentences max)
- One dominant promise or intent
- No above-the-fold message conflict (no multiple equally-weighted headlines)

**Per-type guidance:**
- **Landing:** Value proposition must be in the hero H1
- **Dashboard:** "What do I need to know right now?" answered at top
- **E-commerce:** Product name + key benefit in product hero
- **Blog:** Article headline must be specific enough to promise a clear read

---

## 2. Hero Focus

**Question:** Is the hero area focused, readable, and free from competing priorities?

**Score guidance:**
- 1: Cluttered, multi-message, or slider/carousel-based hero
- 3: Workable hero but some visual competition or distraction
- 5: Highly focused hero with clear hierarchy — one H1, one CTA, one visual anchor

**What to look for:**
- No hero slider or auto-rotating carousel (automatic failure on this rule)
- One main CTA
- Readable content without competing visual weights
- Meaningful visual anchor (not decorative stock photo unless intentional)
- No excessive badge/sticker/decoration layering

**Per-type guidance:**
- **Dashboard:** No hero section at all — hero area shows KPI summary cards
- **E-commerce:** Product image is the hero — gallery with thumbnails is OK, carousel is not
- **Blog:** Featured article headline and image — single, not a list

---

## 3. CTA Clarity

**Question:** Is the main action obvious, easy to understand, and well-placed?

**Score guidance:**
- 1: Unclear, competing, or missing primary CTA; user doesn't know what to do
- 3: CTA exists but lacks prominence, clarity in copy, or optimal placement
- 5: CTA is obvious, well-placed, and aligned to page goal; copy is actionable and clear

**What to look for:**
- One primary CTA in the hero area
- Readable CTA copy (not "Click Here" — instead "Start Free Trial", "Get Started", "Shop Now")
- Good placement: hero, above-fold, and repeated at end
- No competing equal-priority CTAs (secondary CTAs OK but visually subordinate)
- CTA above the fold on mobile

**Per-type guidance:**
- **Landing:** Hero CTA + final section CTA; CTA copy must match the page's primary goal
- **Dashboard:** No marketing CTA — primary actions are filter, export, add, view
- **E-commerce:** "Add to Cart" or "Buy Now" prominent; "View Details" subordinate
- **Pricing:** CTA per plan card — "Get Started" buttons clearly associated with plan

---

## 4. Modular Structure

**Question:** Is content organized into scan-friendly modules rather than long undifferentiated sections?

**Score guidance:**
- 1: Dense wall-like content or weak/nonexistent structure; impossible to scan
- 3: Some modularity but inconsistent grouping; user must work to find information
- 5: Strong modular layout with clear content chunking; information finds itself

**What to look for:**
- Card clusters, bento grids, or clearly delineated sections
- Semantic section boundaries (header per section)
- Grouped related information (features together, testimonials together, specs together)
- No long uninterrupted walls of text
- Section headers that preview content (not generic "Features", but "What Makes Us Different")

**Per-type guidance:**
- **Dashboard:** Modular cards for KPIs, tables with clear headers, filter panels separate from data
- **E-commerce:** Product grid, category cards, cart summary in sidebar/module
- **Blog:** Sidebar modules, related posts, author bio — all modular; article body is intentionally linear

---

## 5. Visual Hierarchy

**Question:** Is importance communicated clearly through size, spacing, contrast, and layout?

**Score guidance:**
- 1: Everything feels equally loud or equally weak; no clear reading order
- 3: Hierarchy exists but is inconsistent or partially broken; some sections compete
- 5: Obvious, smooth, intentional hierarchy throughout; the page guides the eye naturally

**What to look for:**
- Larger blocks for primary content (hero > secondary sections)
- Smaller, subordinate treatment for supporting content
- Strong heading contrast (H1 clearly larger than H2, H2 clearly larger than H3)
- Disciplined use of emphasis (bold, color, size — not all at once)
- White space used to breathe around important elements

**Per-type guidance:**
- **Dashboard:** Primary metrics largest, secondary metrics smaller, tertiary in collapsed sections
- **E-commerce:** Product image largest, price prominent (large, bold), features secondary, reviews tertiary
- **Blog:** Article title largest, deck/st excerpt smaller, body text comfortable 16–18px

---

## 6. Mobile Usability

**Question:** Does the page work naturally on mobile-first assumptions?

**Score guidance:**
- 1: Desktop-first compression, crowded layout, broken flow, horizontal scroll
- 3: Usable but not optimized; some awkwardness or information loss on small screens
- 5: Strong mobile flow with excellent prioritization; page feels designed for mobile

**What to look for:**
- Content stacked vertically (single column or adaptive grid)
- Hierarchy preserved on small screens (primary content still dominant)
- Readable text sizing without horizontal scroll
- Practical scroll sequence (most important at top)
- No content hidden behind non-obvious interactions on mobile

**Per-type guidance:**
- **Dashboard:** Simplified mobile view — KPIs visible, full table accessible via scroll or expandable row
- **E-commerce:** Product images swipeable, cart accessible, checkout single-column
- **Blog:** Article readable without zooming; sidebar stacks below content

---

## 7. Touch Comfort

**Question:** Are interactive controls easy to tap and comfortably spaced on touch devices?

**Score guidance:**
- 1: Dense, error-prone tap targets; user frequently misses or hits wrong targets
- 3: Mostly usable but inconsistent; some interactions feel cramped or too close
- 5: Comfortable, thumb-friendly interaction throughout; no precision tapping required

**What to look for:**
- Minimum 44×44 px touch targets where relevant
- Enough spacing between buttons, links, and other interactive elements
- Obvious active/tap states (button depresses, link highlights)
- Primary CTA easily reachable with thumb (bottom third of screen on mobile)
- No dense clusters of links or buttons without spacing

**Per-type guidance:**
- **Dashboard:** Filter controls thumb-friendly; table rows have enough vertical padding; action buttons in thumb zone
- **E-commerce:** "Add to Cart" large and thumb-accessible; quantity stepper with clear +/− targets

---

## 8. Performance Safety

**Question:** Is the page likely to remain fast and stable across devices and networks?

**Score guidance:**
- 1: Obvious performance risks — heavy hero media, excessive dependencies, layout shifts likely
- 3: Acceptable but somewhat heavy; may load slowly on constrained devices
- 5: Clearly performance-aware and technically lean; targets likely met

**What to look for:**
- Limited above-the-fold media weight (hero image < 200KB if possible)
- No unnecessary heavy slider/carousels libraries
- Restrained third-party usage (analytics, chat widgets — all non-blocking if used)
- Responsive images with `srcset`; lazy loading for below-fold images
- No render-blocking resources in `<head>`
- Likely support for LCP < 2.5s, INP < 200ms, CLS < 0.1

**Per-type guidance:**
- **Dashboard:** Data tables virtualized if > 100 rows; pagination or infinite scroll
- **E-commerce:** Product images WebP, lazy-loaded; no full-page re-renders on filter change
- **Blog:** Single hero image optimized; font loading non-blocking

---

## 9. Accessibility Quality

**Question:** Does the page preserve accessibility fundamentals?

**Score guidance:**
- 1: Major accessibility failures; keyboard inaccessible, poor contrast, no semantic structure
- 3: Basic accessibility present but incomplete; some issues with focus, contrast, or semantics
- 5: Strong accessibility support; WCAG 2.1 AA minimum, good keyboard nav, proper semantics

**What to look for:**
- Semantic HTML structure (headings in order, landmarks `<main>`, `<nav>`, `<header>`, `<footer>`)
- Keyboard accessibility (all interactive elements reachable via Tab, logical focus order)
- Visible focus styles (clear focus ring, not only color change)
- Readable contrast (4.5:1 for normal text, 3:1 for large text — verify with tools)
- Meaningful alt text for informative images; empty alt for decorative images
- `prefers-reduced-motion` respected for motion
- Form labels associated with inputs (not just placeholder as label)

**Per-type guidance:**
- **Dashboard:** Data tables have proper `<th scope>`; filter inputs have labels; sort controls keyboard-accessible
- **E-commerce:** Product images have alt; form inputs have labels; cart quantity stepper keyboard-accessible

---

## 10. Motion Usefulness

**Question:** Is motion functional rather than decorative? Is reduced-motion respected?

**Score guidance:**
- 1: Distracting, purposeless, or excessive motion; no reduced-motion fallback
- 3: Mixed quality; some useful motion but some gratuitous; reduced-motion not verified
- 5: Restrained, purposeful motion that improves usability without distraction

**What to look for:**
- Motion serves a purpose (feedback, state change confirmation, guided attention)
- No constant looping distractions or competing animations
- No aggressive parallax without functional value
- Micro-interactions present for key actions (hover, focus, tap feedback)
- `prefers-reduced-motion` media query respected
- No motion that harms readability

**Per-type guidance:**
- **Dashboard:** Smooth sort/filter transitions; loading skeletons; collapse/expand animations — all brief and functional
- **E-commerce:** Cart add confirmation animation; checkout step transitions; image gallery transitions

---

## 11. Visual Consistency

**Question:** Does the interface feel coherent across typography, spacing, components, and styling?

**Score guidance:**
- 1: Inconsistent and fragmented UI language; mixed patterns, conflicting styles
- 3: Generally coherent with some drift; recognizable pattern library but small inconsistencies
- 5: Strong and consistent design language; every element feels like it belongs to the same system

**What to look for:**
- Consistent spacing rhythm (same increments used throughout)
- Consistent radius behavior (all cards have similar rounding, buttons share radius)
- Stable typography scale (no arbitrary font sizes)
- Coherent card and section patterns (cards look like cards throughout)
- Consistent color usage (primary action color same everywhere, secondary everywhere else)
- No style drift between sections (FAQ section looks different from Pricing section for no reason)

**Per-type guidance:**
- **Dashboard:** Consistent card styles across all widget types; data table rows consistent
- **E-commerce:** Product cards consistent across grid and related products; checkout steps consistent
- **Blog:** Article typography consistent; sidebar consistent with main content

---

## 12. Advanced Effects Justification

**Question:** Are premium effects (3D, WebGL, video backgrounds, scrollytelling, AI personalization) actually justified?

**Score guidance:**
- 1: Advanced effects are gimmicky, harmful to performance, or break accessibility
- 3: Partially justified but not fully controlled; some benefit but some cost
- 5: Clearly valuable, well-contained, performance-aware, and accessibility-conscious

**What to look for:**
- **Scrollytelling:** Only for guided narrative (product launches, brand stories, data stories) — not for FAQ or simple landing
- **3D/WebGL:** Only when it adds explanatory or emotional value; performance acceptable; mobile fallback exists
- **Video background:** Only if meaningful and lightweight; contrast-safe; non-disruptive autoplay
- **AI personalization:** Only as enhancement layer; default page understandable without AI; core navigation unchanged

**For each advanced effect used, verify:**
1. It has a clear functional purpose (not decoration)
2. Performance impact is acceptable (measure or estimate)
3. Fallback behavior exists for unsupported browsers/devices
4. Mobile experience remains usable
5. Reduced-motion users can opt out

---

## Issue Classification Reference

### Critical — Immediate Action Required

Damages **clarity, usability, accessibility, performance, or conversion path**.

Examples:
- Hero slider hiding primary value
- Unreadable contrast in hero section (below 3:1 for large text)
- Primary CTA missing or unclear
- Broken mobile flow (horizontal scroll, content truncated)
- No keyboard accessibility on primary actions
- CLS-causing layout shifts (images without dimensions, ads injecting content)
- Form submission with no error feedback
- Empty state that looks broken (not intentionally empty)

### Important — Address in Short Term

Weakens quality but does **not fully break** the page.

Examples:
- Inconsistent spacing system (some sections 16px gap, others 24px)
- Weak hierarchy in secondary sections (everything looks same size)
- Unnecessary media weight slowing load
- Mixed card radius patterns on same page
- Missing focus states on secondary interactive elements
- Loading states absent on async interactions

### Nice to Improve — Polish and Refinement

Polish opportunities that don't affect core usability.

Examples:
- Better proof ordering (testimonials could be more relevant)
- Cleaner CTA wording ("Get Started" could be "Start Your Free Trial")
- Stronger section transitions (subtle dividers or whitespace between sections)
- Tighter typography rhythm (line-height slightly loose on body text)
- Color contrast could be improved from 4.5:1 to 5:1

---

## Final Recommendation Logic

| Recommendation | Condition |
|----------------|-----------|
| **approve** | No critical issues. Page is clear, usable, accessible, and performance-safe. Minor improvements OK. |
| **revise** | No structural failure. Important issues meaningfully weaken effectiveness. Fixable without full redesign. |
| **redesign** | Structurally confused hero strategy, broken content architecture, poor mobile experience, or systemic accessibility/performance problems. |

**Never recommend approve if:**
- Any critical issue exists
- Accessibility score ≤ 2
- Performance safety score ≤ 2
- Hero section uses a slider/carousel

**Recommend redesign if:**
- Structural layout is fundamentally wrong
- Mobile experience requires significant compression
- Performance problems are systemic (not fixable with optimizations alone)
- Accessibility problems are pervasive (not isolated to one section)
