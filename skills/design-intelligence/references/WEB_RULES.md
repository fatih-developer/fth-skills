# WEB_RULES — Design Intelligence Rule Set

Comprehensive design rules for generating and reviewing web interfaces. Rules apply to all page types; per-type adaptations are noted where they diverge.

**Core priority order:** clarity → task completion → performance → accessibility → visual hierarchy.

---

## 1. One Primary Message Rule

Every page must communicate one dominant message above the fold.

**Required structure:**
- 1 clear H1
- 1 supporting sentence or short paragraph
- 1 primary CTA
- 1 visual anchor (image, illustration, short video, product preview, or meaningful graphic)

**Do not** place multiple competing messages in the hero area.

**Per-type modulation:**
- **Landing:** Product or value proposition = primary message
- **Dashboard:** Primary KPIs = primary message (not a marketing headline)
- **E-commerce:** Product name + key benefit = primary message
- **Blog:** Article headline = primary message
- **Portfolio:** Work title or personal brand = primary message

---

## 2. No Hero Slider Rule

Do not use auto-rotating hero sliders, homepage carousels, or multi-slide banner systems for primary messaging.

**Why:** weak focus, poor scanability, worse performance, lower content visibility, users concentrate on the first item only.

**Preferred alternatives:**
- Static high-impact hero
- Modular featured cards
- Scrollytelling section
- Thumbnail-driven content gallery
- Segmented hero with visible choices
- Product image gallery with thumbnails (e-commerce)

**Per-type modulation:**
- **Dashboard:** Never appropriate — data is primary
- **E-commerce:** Product gallery with thumbnails is OK; auto-rotating carousel is not
- **Blog:** Not applicable — hero is typically a single featured post

---

## 3. Modular Layout Rule

Use modular content architecture by default. Chunk content into meaningful units.

**Preferred patterns:**
- Bento grid
- Card-based sections
- Feature clusters
- Modular stats + media + text blocks
- Content blocks with clear semantic separation

**Do not** produce long uninterrupted sections of content.

**Per-type modulation:**
- **Dashboard:** Strongly encouraged — dense data must be chunked into cards, tables, and panels
- **E-commerce:** Product grid, category cards, cart summary module
- **Blog:** Article body is linear; sidebar modules, related posts, and author bio are modular
- **Pricing:** Comparison table or bento grid of plan cards

---

## 4. Hierarchy by Size Rule

Use space and block size to signal importance.

**Examples:**
- Primary content → larger grid area
- Secondary content → smaller cards
- Supporting items → grouped blocks
- CTA prominence → controlled by hierarchy, not visual noise

**Do not** make all blocks equally loud.

**Per-type modulation:**
- **Dashboard:** Critical — KPI cards large, secondary data small, tertiary actions in footer/toolbar
- **E-commerce:** Product image large, price prominent, features secondary, reviews tertiary
- **Landing:** Hero section largest, feature grid medium, testimonials compact

---

## 5. Controlled Asymmetry Rule

Asymmetry is allowed and often preferred, but only when structure remains readable.

**Allowed:**
- Uneven card sizes
- Offset compositions
- Organic flow
- Visual rhythm through modular variation

**Not allowed:**
- Random layout
- Broken reading order
- Decorative chaos without hierarchy

**The result should feel dynamic, not confusing.**

---

## 6. Grid Standard

Use a 12-column layout system for desktop by default. Collapse to simpler structures on tablet and mobile.

**Recommended approach:**
- Desktop: 12-column grid
- Tablet: reduced modular grid (6-column or adaptive)
- Mobile: single-column or simple stacked flow

**Per-type modulation:**
- **Dashboard:** Data tables may need 12-col for complex grids; sidebar may collapse to icons
- **E-commerce:** Product grid: 4-col desktop, 2-col tablet, 1-col mobile
- **Pricing:** 3-col plan cards desktop, 1-col stack mobile

---

## 7. Consistent Spacing Rule

Spacing must be systematic and reusable.

**Preferred behavior:**
- Consistent gutters between cards
- Consistent section spacing
- Clear distinction between internal padding and external spacing

**Visual standard:**
- Medium-to-generous spacing
- Enough breathing room for scanning
- Avoid cramped compositions

**Suggested scale:** 4px base unit — 4, 8, 12, 16, 24, 32, 48, 64, 96px increments.

---

## 8. Rounded Interface Rule

Use soft corners where appropriate for a modern, approachable feel.

**Suitable for:**
- Cards
- Media containers
- Buttons
- Feature modules
- Dashboard-like homepage blocks

**Do not** mix too many corner styles within one page. Pick one radius strategy and apply it consistently.

**Per-type modulation:**
- **Dashboard:** Slightly rounded cards, rounded buttons — approachable but professional
- **E-commerce:** Heavily rounded product cards, softer cart items
- **Blog:** Minimal rounding — readable, content-first

---

## 9. Mobile-First Construction Rule

Design for mobile first, then enhance upward.

**Workflow:**
1. Define essential content and actions for small screens
2. Ensure tap comfort and scroll flow
3. Expand complexity only for larger screens

**Do not** design desktop-first and compress it later.

**Per-type modulation:**
- **E-commerce:** Critical — mobile commerce dominates; checkout must be single-column flow
- **Dashboard:** Mobile dashboard is typically a simplified KPI view; full data interaction is desktop
- **Blog:** Mobile-first typography, readable at any width

---

## 10. Thumb-Friendly Interaction Rule

Critical actions must be easy to reach and easy to tap on mobile.

**Required:**
- Touch targets at least 44×44 px
- Enough spacing between interactive elements
- Obvious tap states
- Avoid dense clusters of links or buttons

**Primary CTA** must remain accessible without precision tapping.

**Per-type modulation:**
- **Dashboard:** Primary actions (filter, export, add) must be thumb-reachable in mobile view
- **E-commerce:** "Add to cart" prominent and large; checkout button thumb-friendly

---

## 11. Progressive Enhancement Rule

Base experience must work on constrained devices and networks. Enhance only after the core page is solid.

**Enhancements may include:**
- Richer motion
- Larger media
- Advanced hover effects
- 3D or WebGL elements
- Dynamic personalization

**The page must remain usable without those extras.**

---

## 12. Performance Before Decoration Rule

Do not add visual features that significantly hurt load speed or interaction speed.

**Target:**
- LCP under 2.5s
- INP under 200ms
- CLS under 0.1

**Per-type modulation:**
- **Landing:** Above-the-fold media must be lightweight; hero image optimized
- **Dashboard:** Data fetching strategy matters; pagination or virtualization for large tables
- **E-commerce:** Product images must be WebP, lazy-loaded, responsive

---

## 13. Media Discipline Rule

Above-the-fold media must be intentional and optimized.

**Avoid:**
- Multiple heavy hero assets
- Oversized background videos with no functional value
- Unnecessary preload of non-critical visuals
- Decorative media that delays first useful paint

**Use:**
- Optimized images (WebP/AVIF, correct sizing)
- Short lightweight video only when justified
- Lazy loading for non-critical assets
- Responsive image delivery (`srcset`)

**Per-type modulation:**
- **Landing:** Hero visual is critical — keep it lightweight
- **Dashboard:** Charts and data visualizations are the "media" — optimize for render speed
- **E-commerce:** Product photography is the product — high quality but optimized

---

## 14. Lightweight Frontend Rule

Keep the page technically lean.

**Avoid:**
- Unnecessary third-party plugins
- Redundant JS dependencies
- Oversized animation libraries for simple tasks
- Duplicated rendering logic

**Prefer:**
- Semantic HTML
- Efficient CSS
- Minimal JS for essential interactions
- Progressive loading

---

## 15. Functional Motion Rule

Animation must serve a clear purpose.

**Valid purposes:**
- Guide attention
- Explain transition
- Confirm interaction
- Reveal hierarchy
- Support storytelling
- Improve perceived responsiveness

**Invalid purpose:** decoration only.

**Motion must never compete with core content.**

---

## 16. Micro-Interaction Rule

Important user actions must produce immediate, visible feedback.

**Expected patterns:**
- Hover and focus states
- Pressed states on buttons
- Loading states
- Form validation feedback
- Success and error confirmation
- Skeletons or progress indicators during wait states

**The interface should feel responsive and alive.**

**Per-type modulation:**
- **Dashboard:** Loading skeletons for data tables; filter feedback; sort state changes
- **E-commerce:** Cart add confirmation; quantity update; checkout flow step indicators

---

## 17. Motion Restraint Rule

Use motion with moderation.

**Avoid:**
- Constant looping distractions
- Multiple competing animations
- Aggressive parallax without purpose
- Motion that harms readability
- High-motion experiences without reduced-motion fallback

**Support reduced motion preferences** whenever possible (`prefers-reduced-motion`).

---

## 18. Typography as Structure Rule

Typography must carry hierarchy, not just decoration.

**Required:**
- Strong heading contrast
- Readable body text (16px minimum for body)
- Predictable scale system
- Clear distinction between headline, support text, labels, and metadata

**Avoid arbitrary size jumps.** Use a consistent type scale (e.g., 12/14/16/18/20/24/32/40/48/64px).

**Per-type modulation:**
- **Blog:** Typography is the product — use a proven readable combination (e.g., Merriweather + system-ui)
- **Dashboard:** Dense but readable — labels smaller, values larger, monospace for data

---

## 19. Scan-Friendly Copy Rule

Write for scanning, not only for reading.

**Preferred:**
- Concise headlines
- Short supporting paragraphs
- Grouped information
- Bullets or cards when information density is high
- Visible key facts and benefits

**Avoid long dense text walls** unless the page specifically requires editorial reading.

---

## 20. Expressive Typography with Restraint Rule

Large, bold, or expressive typography is acceptable when:
- it improves emphasis
- it supports brand tone
- it does not break readability
- it does not overload mobile layouts

**Variable fonts** are preferred when they improve performance and responsive behavior.

---

## 21. Human-Centered Aesthetic Rule

The interface should feel warm, intentional, and approachable.

**Preferred qualities:**
- Soft depth (shadows, subtle gradients)
- Clean surfaces
- Balanced contrast
- Modern but human character
- Subtle texture or tactility where useful

**Avoid extremes:**
- Sterile flatness
- Chaotic overstimulation
- Novelty for its own sake

---

## 22. Controlled Density Rule

High information density is acceptable only when clearly organized.

**When content is dense:**
- Separate it into modules
- Use visual grouping
- Preserve whitespace
- Prioritize primary actions and primary facts
- Avoid dumping all content into one continuous container

**Per-type modulation:**
- **Dashboard:** High density is expected and appropriate — chunk into KPI cards, data tables, filter panels
- **Landing:** Low density — each section breathes, hero is spacious

---

## 23. Scrollytelling Rule

Use scrollytelling only when the page needs guided narrative progression.

**Best use cases:**
- Product storytelling
- Launch pages
- Feature reveals
- Brand narratives
- Data storytelling

**Do not use** scrollytelling for simple informational pages that need fast direct access.

---

## 24. 3D / WebGL Rule

3D, WebGL, and immersive interaction are optional premium patterns, not defaults.

**Use only when:**
- They support the brand or story materially
- They add real explanatory or emotional value
- Performance remains acceptable
- Fallback behavior exists
- Mobile experience remains usable

**Do not use 3D merely to look advanced.**

---

## 25. Video Background Rule

Background video is allowed only when it strengthens meaning and remains lightweight.

**It must not:**
- Block content clarity
- Reduce text contrast
- Slow first rendering significantly
- Autoplay in a disruptive way

**Prefer** short, optimized, silent loops if used at all.

---

## 26. Personalization Is an Enhancement Rule

AI-driven personalization must enhance the experience, not replace structural clarity.

**Safe uses:**
- Adaptive content ordering
- Contextual recommendations
- Dynamic support blocks
- Readability and accessibility improvements
- Seasonal or contextual asset updates

**Unsafe uses:**
- Changing core navigation unpredictably
- Hiding essential actions
- Making first-time experience confusing

**The default version of the page must still be understandable without AI.**

---

## 27. Accessibility Is Mandatory Rule

All outputs must preserve accessibility as a baseline, not as an afterthought.

**Minimum expectations:**
- Semantic heading order (h1 → h2 → h3, no skips)
- Keyboard accessibility (all interactive elements reachable via Tab)
- Visible focus styles (clear ring on focused elements)
- Sufficient contrast (4.5:1 for normal text, 3:1 for large text)
- Meaningful alt text where needed
- Reduced motion support (`prefers-reduced-motion`)
- Readable text sizing (respect user zoom, minimum 16px for body)
- Non-color-only feedback (icons + color, not color alone)

**A visually modern page is unacceptable if it weakens accessibility.**

---

## 28. Error & Empty State Rule

Every interactive flow must handle error and empty states gracefully.

**Error state must have:**
- Friendly, actionable message
- Clear indication of what went wrong
- Recovery path or retry mechanism
- No technical jargon visible to users

**Empty state must have:**
- Helpful message explaining the empty state
- Clear CTA to populate the state (e.g., "Add your first product")
- Visual that doesn't look broken

**Per-type modulation:**
- **Dashboard:** Empty data table ≠ broken table — show "No data matches your filters" with clear action
- **E-commerce:** Empty cart — show friendly message with CTA to continue shopping
- **Blog:** No posts found — suggest categories or show featured content

---

## 29. Form Behavior Rule

Forms must be designed with progressive disclosure and immediate feedback.

**Principles:**
- Show only the minimum required fields initially
- Reveal additional fields only when needed
- Validate on blur, not just on submit
- Show inline error messages close to the field
- Disable submit while processing; show loading state
- Provide clear success confirmation on submit

**Per-type modulation:**
- **Dashboard:** Filter forms should update results immediately (no submit button needed)
- **E-commerce:** Checkout forms should auto-fill where possible; address validation feedback
- **Contact/About:** Simple form — name, email, message; CAPTCHA only if absolutely necessary

---

## 30. Navigation Clarity Rule

Navigation must always be predictable and findable.

**Principles:**
- Primary navigation is always visible on desktop (top bar or left sidebar)
- On mobile, hamburger menu is acceptable but must reveal full navigation
- Current page is indicated (active state)
- Breadcrumbs used when depth > 2 levels
- Mobile nav opens via tap, not hover
- Nav items are labeled with plain language, not jargon

**Per-type modulation:**
- **Dashboard:** Persistent sidebar or top bar; mobile may use bottom tab bar for key actions
- **Landing:** Top nav with CTA; scrolling may hide nav (smart sticky behavior)
- **Blog:** Simple top nav; category dropdown; search icon; mobile hamburger
