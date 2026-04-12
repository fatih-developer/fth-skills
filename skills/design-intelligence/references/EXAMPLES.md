# EXAMPLES — design-intelligence by Page Type

Concrete examples showing how the rules apply per page type. Each example includes strategy summary, section architecture, and key rule applications.

---

## 1. Landing Page

**Example: SaaS Analytics Product**

### Page Strategy Summary
- **Page type:** Landing page
- **Page goal:** Convert visitors to free trial signups
- **Primary audience:** Developers and small team leads evaluating analytics tools
- **Primary message:** "Understand your production issues before your users notice them"
- **Primary CTA:** "Start free trial — no credit card required"

### Section Architecture
```
1. Hero — single message + primary CTA (above fold)
2. Trust bar — logos of known customers (Stripe, Vercel, Linear)
3. Problem statement — why current tools fail (short copy + illustration)
4. Feature bento — 6-card modular grid (error tracking, performance, uptime, logs, alerts, integrations)
5. Metrics proof — 3 large stat blocks ("99.9% uptime", "50ms avg alert latency", "10M events/day")
6. Testimonials — 2 quotes from known users
7. Code snippet — real diagnostic output example (shows value immediately)
8. FAQ — 5 common objections
9. Final CTA — repeat hero CTA with confidence builder
```

### Key Rule Applications
- **Rule 1 (One Primary Message):** Hero H1 = "Understand your production issues before your users notice them" — single, specific, no competing claims
- **Rule 2 (No Hero Slider):** Static hero with illustration; no auto-rotation
- **Rule 3 (Modular Layout):** Feature bento grid with 6 cards, each self-contained
- **Rule 12 (Performance):** Hero illustration is SVG, not raster image; code snippet is syntax-highlighted text
- **Rule 15 (Functional Motion):** Subtle fade-in on scroll for bento cards; no looping animations
- **Rule 27 (Accessibility):** All interactive elements keyboard-accessible; focus states visible; contrast verified

---

## 2. Dashboard / Admin Panel

**Example: B2B SaaS Analytics Dashboard**

### Page Strategy Summary
- **Page type:** Dashboard
- **Page goal:** Let engineering teams monitor production health and diagnose issues
- **Primary audience:** Backend engineers, SREs, engineering managers
- **Primary message:** "Here is what you need to know about your production systems right now"
- **Primary CTA:** None for marketing; primary actions are "Add alert", "View service", "Export report"

### Section Architecture
```
1. Top navigation bar — logo, service selector, user avatar
2. KPI summary row — 4 cards (Error rate, Latency p99, Uptime, Active alerts)
3. Primary chart area — time-series graph (last 24h default, selectable)
4. Service health table — sortable, filterable, with status indicators
5. Recent alerts panel — last 5 alerts with severity, service, and timestamp
6. Quick actions bar — "Create alert", "View logs", "Export PDF"
```

### Key Rule Applications
- **Rule 1 (One Primary Message):** Relaxed — dashboard's "message" is 4 KPIs at top (data density expected)
- **Rule 3 (Modular Layout):** 4 KPI cards, chart, table, alerts panel — each clearly delineated
- **Rule 4 (Hierarchy by Size):** KPI cards largest, chart medium, table full-width below
- **Rule 9 (Mobile-First):** KPIs stack vertically on mobile; table becomes horizontal scroll or card list
- **Rule 16 (Micro-Interaction):** Table rows highlight on hover; sort icons animate; filter panel slides in
- **Rule 22 (Controlled Density):** High density is appropriate — but each card/panel is self-contained with whitespace

---

## 3. E-commerce Product Page

**Example: Premium Headphones Product Page**

### Page Strategy Summary
- **Page type:** E-commerce product page
- **Page goal:** Convert product view to add-to-cart action
- **Primary audience:** Music professionals and audiophiles comparing wireless headphones
- **Primary message:** "Studio-grade wireless headphones with 40-hour battery"
- **Primary CTA:** "Add to cart — $349"

### Section Architecture
```
1. Product gallery — large main image + 4 thumbnail strip (color variants)
2. Product info column — name, price, short description, rating (4.8★)
3. Variant selector — color swatches + size guide link
4. Add to cart CTA — large, prominent, sticky on scroll
5. Feature highlights — 4 icons with short copy (battery, driver, ANC, connectivity)
6. Technical specs accordion — expandable table
7. Reviews summary — average rating, distribution bar chart, top 3 reviews
8. Related products carousel — "Customers also viewed"
```

### Key Rule Applications
- **Rule 1 (Primary Message):** Product name + benefit headline = primary message; price is visible but secondary
- **Rule 2 (No Hero Slider):** Image gallery with thumbnails is OK (not a carousel); thumbnails are clickable, not auto-advancing
- **Rule 9 (Mobile-First):** Gallery becomes swipeable on mobile; sticky "Add to cart" bar at bottom
- **Rule 10 (Thumb-Friendly):** "Add to cart" button is 48px tall on mobile; variant selector swatches are 44×44px
- **Rule 16 (Micro-Interaction):** Cart button shows checkmark + "Added!" on tap; quantity updates with +/− buttons
- **Rule 18 (Typography):** Product name largest, price prominent, specs in readable table

---

## 4. Blog / Article

**Example: Technical Blog Post**

### Page Strategy Summary
- **Page type:** Blog article
- **Page goal:** Help engineers understand and implement connection pooling
- **Primary audience:** Backend engineers working with PostgreSQL
- **Primary message:** "Connection pooling in Postgres: a practical guide to PgBouncer"
- **Primary CTA:** None (purely informational); secondary: "Subscribe to the newsletter"

### Section Architecture
```
1. Article header — headline, author avatar + name, date, reading time, category tag
2. Hero illustration — abstract diagram of connection pooling architecture
3. Deck/st excerpt — 2-sentence summary below headline
4. Article body — linear reading flow, H2/H3 hierarchy, code blocks, callout boxes
5. Author bio box — small card at end with avatar and social links
6. Related posts — 3 cards (same category)
7. Newsletter signup — single-field email form below related posts
```

### Key Rule Applications
- **Rule 1 (Primary Message):** Article headline is the primary message — specific, not generic
- **Rule 3 (Modular Layout):** Article body is intentionally linear (readability); sidebar = newsletter + related posts = modular
- **Rule 18 (Typography as Structure):** Merriweather for article body (serif, readable), system-ui for UI chrome; H2 clearly larger than body
- **Rule 19 (Scan-Friendly Copy):** H2 headings are descriptive (not "Introduction" but "What is PgBouncer and When Do You Need It")
- **Rule 22 (Controlled Density):** Low density — article body is comfortable reading with generous line-height (1.7)
- **Rule 27 (Accessibility):** Code blocks have `aria-label`; copy-paste is not the only way to access code

---

## 5. Portfolio

**Example: Freelance Designer Portfolio Page**

### Page Strategy Summary
- **Page type:** Portfolio
- **Page goal:** Get potential clients to request a project consultation
- **Primary audience:** Startup founders and product managers looking for design work
- **Primary message:** "I design interfaces that work as good as they look"
- **Primary CTA:** "Work with me →"

### Section Architecture
```
1. Hero — full-viewport, large name, tagline, single CTA
2. Selected work — 4 project cards (large image + project name + type + year)
3. About blurb — 2-paragraph personal story + headshot
4. Services offered — 3 cards (Product design, Design systems, UX audit)
5. Client logos — 6 logos in a row (muted/grayscale)
6. Contact strip — email + LinkedIn + Calendly link
```

### Key Rule Applications
- **Rule 1 (Primary Message):** Hero tagline is one sentence; no competing message in hero
- **Rule 3 (Modular Layout):** 4 project cards are equal-sized bento grid; each is self-contained
- **Rule 21 (Human-Centered Aesthetic):** Warm typography, personal photo, personality-driven — not sterile corporate
- **Rule 25 (Video Background):** Not used — hero is a bold typographic treatment or single large image
- **Rule 26 (Personalization):** Not applicable — no AI personalization needed

---

## 6. SaaS Pricing Page

**Example: Developer Tool Pricing Page**

### Page Strategy Summary
- **Page type:** SaaS pricing
- **Page goal:** Help visitors choose a plan and convert to signup
- **Primary audience:** Developers evaluating pricing for personal or team use
- **Primary message:** "Simple pricing. No surprises. Start free, scale as you grow."
- **Primary CTA:** Plan-specific ("Start with Pro", "Start with Team")

### Section Architecture
```
1. Page header — H1 + subheadline (simple, no fluff)
2. Toggle — Monthly / Annual billing (annual shows % savings)
3. Plan cards — 3 plans side by side (Free / Pro / Team)
   - Each card: plan name, price, target user, feature list, CTA button
4. Feature comparison table — full breakdown below cards (collapsible on mobile)
5. FAQ — 6 common questions about pricing, limits, upgrades
6. Migration note — "Already paying for X? We'll match and migrate you in 5 minutes."
7. Final CTA — "Still unsure? Book a 15-min call."
```

### Key Rule Applications
- **Rule 1 (Primary Message):** "Simple pricing" is the promise — no hidden fees, no feature confusion
- **Rule 3 (Modular Layout):** 3 plan cards are equal-width bento-style; feature table below is separate module
- **Rule 4 (Hierarchy by Size):** Pro plan card is slightly elevated or highlighted as "most popular"; Free and Team are equal
- **Rule 9 (Mobile-First):** Plan cards stack vertically on mobile; comparison table collapses to accordion
- **Rule 16 (Micro-Interaction):** Toggle animates price change; hover on plan card elevates it slightly
- **Rule 18 (Typography):** Plan names bold and large; price is the second largest element; feature text is small but readable

---

## 7. About / Contact

**Example: Small Agency About & Contact Page**

### Page Strategy Summary
- **Page type:** About / Contact
- **Page goal:** Build trust and get prospective clients to reach out
- **Primary audience:** Business owners and marketing leads evaluating an agency
- **Primary message:** "We're a small team that does serious work with serious clients"
- **Primary CTA:** "Send us a message" or "Book a call"

### Section Architecture
```
1. About hero — full-width team photo or office shot + headline
2. Our story — 2-paragraph origin story (why we exist)
3. Values — 3 cards (How we work, What we believe, What we're proud of)
4. Team section — 3-4 team member cards (photo, name, role, short bio)
5. Social proof — 2-3 client logos + 1 testimonial quote
6. Contact section — email, address, phone + embedded contact form OR Calendly embed
```

### Key Rule Applications
- **Rule 1 (Primary Message):** "Small team, serious work" is the headline — sets expectation accurately
- **Rule 3 (Modular Layout):** Team cards are modular; values are modular; contact is its own section
- **Rule 21 (Human-Centered Aesthetic):** Team photos are real (not stock); story is specific to this agency
- **Rule 26 (Personalization):** Contact form or Calendly is functional and simple — no AI chatbot needed
- **Rule 27 (Accessibility):** Contact form labels all filled; phone number is clickable `tel:` link; map embed has alt text
