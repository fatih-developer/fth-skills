# Implementation Guide

Use this guide as a framework-neutral checklist. Verify platform-specific behavior against current official sources before applying it.

## Contents

1. Evidence and priority rules
2. Discovery and indexability
3. Rendering and extractability
4. Metadata and URL signals
5. Structured data and entities
6. Content and answer readiness
7. AI question map and visibility measurement
8. Trust and external visibility
9. Change-impact rules
10. Verification matrix

## 1. Evidence and priority rules

Classify findings by user and discovery impact:

| Priority | Meaning | Typical examples |
|---|---|---|
| Critical | Broad discovery is blocked or public content is unavailable | Site-wide `noindex`, crawler blocked, 5xx public routes, authentication wall |
| High | Important pages are undiscoverable, misleading, duplicated, or technically invalid | Missing sitemap coverage, wrong canonical, client-only critical content, invalid product claims in schema |
| Medium | Relevance, extraction, or trust is materially weaker | Generic titles, weak internal links, unclear authorship, missing intent coverage |
| Low | Useful refinement with limited immediate impact | Secondary social metadata, minor wording, optional enrichment |

Attach evidence to every finding: file path, route, HTTP response, generated HTML, log observation, official rule, or clearly labeled inference.

## 2. Discovery and indexability

Check:

- Public pages return intentional `2xx`, `3xx`, `4xx`, or `5xx` statuses.
- Redirects resolve in one logical hop where practical.
- Important pages are reachable through crawlable anchor links.
- `robots.txt` reflects current business intent and current official crawler names.
- Meta robots and `X-Robots-Tag` do not conflict with the intended index state.
- XML sitemap URLs are canonical, indexable, absolute, current, and successful.
- Sitemap indexes are used when scale requires them.
- Parameter, filter, staging, preview, account, and internal-search URLs are controlled intentionally.
- Staging, preview, mirror, and legacy hosts do not expose indexable duplicate entities, sitemaps, schema, or stale product facts; use access control plus `noindex` where appropriate rather than relying on robots alone.
- Canonical tags do not point important pages to unrelated or non-indexable URLs.
- CDN/WAF rules allow intended verified crawlers without opening unsafe broad bypasses.

For ChatGPT Search, verify OpenAI's current crawler documentation on every run. As a historical baseline only, OpenAI documented `OAI-SearchBot` for search visibility and treated it independently from `GPTBot` training controls. Never assume names, versions, IP ranges, or behavior remain unchanged.

## 3. Rendering and extractability

Check the served response and, when different, the rendered page:

- Primary topic, main copy, essential links, and factual answers appear without user interaction.
- JavaScript errors, consent layers, hydration failures, or infinite loading do not hide critical content.
- Server rendering, static generation, or reliable dynamic rendering matches the framework's supported patterns.
- Navigation uses semantic anchors for public destinations.
- Images that carry meaning have useful alt text; decorative images do not add noise.
- Videos and interactive tools have text context, labels, or transcripts when appropriate.
- Important information is not available only inside images, canvas, private APIs, or inaccessible downloads.

## 4. Metadata and URL signals

For every important page, check:

- One descriptive, intent-aligned title.
- A useful description that does not make unsupported claims.
- One stable canonical URL using the intended host and protocol.
- Correct language and locale signals.
- Consistent trailing-slash, casing, and query-parameter behavior.
- Meaningful headings with one clear page topic; do not enforce arbitrary heading counts.
- Social metadata only where sharing presentation matters.
- Dates accurately distinguish publication from modification.

Avoid boilerplate metadata across unrelated routes. Generate framework-native metadata close to route data when possible.

## 5. Structured data and entities

Use structured data only when it represents visible, accurate content and a recognized page/entity type.

Commonly relevant types include:

- `Organization` or a more specific organization type.
- `WebSite` and `WebPage`.
- `Product`, `Offer`, or `Service` when the page truly provides those details.
- `Article`, `BlogPosting`, or another appropriate creative work.
- `BreadcrumbList` for visible hierarchical navigation.
- `FAQPage` only for genuine visible question-and-answer content and only where current platform guidance supports it.

Check stable entity identifiers, consistent names, canonical URLs, logos, contact details, authors, dates, currencies, availability, and relationships. Validate JSON syntax and semantic accuracy. Never add reviews, ratings, prices, or availability that the business has not verified.

## 6. Content and answer readiness

Build around user intent, not keyword variants:

1. Identify the user's actual decision or task.
2. Give a concise direct answer near the relevant heading.
3. Make the answer block self-contained: repeat the named subject and retain necessary scope, conditions, date, and source context.
4. Add necessary evidence, conditions, comparisons, steps, or examples.
5. Connect the answer to the appropriate product, service, tool, or next action.
6. Cite primary sources for changing or high-stakes facts.

Useful content formats include definitions, how-to guides, comparisons, calculators, original data, transparent pricing, compatibility tables, methodology pages, case studies, and troubleshooting guides. Use FAQs only when questions are genuinely frequent and not already answered cleanly elsewhere.

Build semantic authority with a coherent cluster that covers the user's journey—definition, task, comparison, evidence, trust, and decision—without producing thin keyword variants. Prefer original benchmarks, calculators, templates, datasets, screenshots, reproducible examples, and transparent methodology over generic summaries.

For each opportunity, specify:

- Representative user question.
- Search intent.
- Recommended page or existing route.
- Unique value the site can truthfully provide.
- Evidence or business input required.
- Conversion path and internal links.

## 7. AI question map and visibility measurement

Build a small, durable query manifest from applicable groups:

- Definition and explanation.
- How-to and troubleshooting.
- Comparison and alternatives.
- Recommendation under explicit constraints.
- Trust, evidence, safety, privacy, or methodology.
- Pricing, availability, compatibility, limits, and refunds.
- Local service and location intent.
- Branded product and operator facts.

When direct platform access exists, record exact query, platform, date, market/locale, brand mention, cited URL, factual accuracy, competitors, and relevant context. Repeat important prompts under consistent conditions before describing a trend. Never use ordinary web search as a substitute for an actual ChatGPT, Gemini, Copilot, Claude, or Perplexity answer.

Keep measurement layers separate:

| Layer | Examples |
|---|---|
| Discovery | index coverage, impressions, rank, CTR |
| AI visibility | controlled mention/citation observations, cited URL, accuracy, competitor inclusion |
| Exposure/referral | AI referral sessions, branded search, direct visits, assisted conversions |
| Business | qualified leads, signups, purchases, imports, retained users |

Store the query set and collection conditions in a project-native location only when that helps repeat measurement. Instrument referral and conversion events only when the repository and user authorization support them. Do not claim that exposure caused conversion without suitable evidence.

## 8. Trust and external visibility

Evaluate whether a reader and an answer engine can establish:

- Who operates the site.
- How to contact them.
- What the product or service actually does.
- Which markets and languages it serves.
- Who authored or reviewed important content.
- When and how factual content was updated.
- What evidence supports comparisons, outcomes, or claims.
- Which policies apply to users and purchases.

Create an external-visibility plan based on relevance and earned value:

- Publish reference-worthy original resources.
- Contribute expertise to legitimate industry publications.
- Seek accurate inclusion in relevant directories and partner pages.
- Turn genuine integrations and partnerships into co-marketing opportunities.
- Find and correct unlinked or inaccurate brand mentions.
- Use digital PR for real data, launches, or expert commentary.

Reject bulk directory spam, private blog networks, hidden sponsorships, fake reviews, automated outreach spam, and links purchased to manipulate rankings.

## 9. Change-impact rules

Re-run a focused audit when changes affect:

- Routing, domains, protocols, redirects, middleware, proxies, CDN, or deployment.
- Authentication or authorization around public routes.
- Page rendering, layouts, navigation, headings, or core content.
- Metadata, canonical logic, localization, pagination, or filters.
- Robots directives, HTTP headers, sitemap generation, feeds, or structured data.
- Product names, pricing, availability, organization details, authors, policies, or claims.

Skip a dedicated GEO/SEO pass for isolated internal refactors, private admin features, tests, or backend changes with no public response, URL, content, or performance impact. Record the reason when impact is genuinely ambiguous.

## 10. Verification matrix

| Layer | Local evidence | Live evidence when available |
|---|---|---|
| Code quality | Formatter, lint, types, tests | Not applicable |
| Build/render | Successful build; generated or served HTML | Final HTML/rendered page |
| Discovery | Robots and sitemap route tests | Public status, content, and headers |
| Metadata | Route/component tests; HTML inspection | Canonical host and deployed metadata |
| Structured data | JSON parse and semantic review | Live extraction/validator where available |
| Content | Visible copy, headings, links | No consent/auth/rendering obstruction |
| Platform access | Current official rules documented | Bot/WAF/log or webmaster-tool evidence |

If no live URL exists, convert the right-hand column into the post-deployment checklist.
