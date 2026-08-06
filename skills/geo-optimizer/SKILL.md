---
name: geo-optimizer
description: Analyze, implement, and verify technical SEO, GEO, AEO, AI-search visibility, citation-readiness, AI-question coverage, and repeatable visibility measurement for web projects. Use when creating a new website or web application; when the user asks to improve or measure visibility in ChatGPT Search, generative/AI answer engines, Google, Bing, SEO, GEO, or AEO; or when a code or content change may materially affect crawling, indexing, metadata, structured data, answer extraction, internal linking, analytics, or search-visible content. Do not invoke for unrelated changes that cannot affect public discovery or search presentation.
---

# AI GEO Optimizer

**CRITICAL LANGUAGE RULE:** The instructions in this skill are written in English, but you MUST respond in the language of the user's request. All outputs, explanations, candidates, categories, and findings must be delivered in the user's language unless otherwise specified.

Improve a web project's discoverability in AI answer engines and conventional search without promising rankings, citations, traffic, or inclusion.

## Operating rules

- Inspect the repository before asking questions. Infer the framework, rendering model, routes, content system, deployment clues, and existing search configuration.
- Ask only for missing facts that materially change implementation, such as target audience, market, language, product positioning, verified claims, or production URL.
- Never invent prices, testimonials, credentials, statistics, locations, legal claims, customer counts, or product capabilities.
- Preserve existing architecture, conventions, and unrelated user changes. Read and follow repository instructions.
- Treat AI visibility as an extension of sound technical SEO, useful content, entity clarity, and external credibility—not as a separate ranking trick.
- Optimize the full path from crawl eligibility to answer extraction, citation or mention, referral/exposure, and verified conversion. Keep those outcomes distinct.
- Avoid keyword stuffing, hidden text, doorway pages, fake FAQs, fabricated citations, schema spam, crawler cloaking, or instructions aimed at manipulating an AI model.
- Do not claim success merely because files were added. Verify observable behavior.

## Required current-source gate

Before every implementation:

1. Identify the search and AI platforms relevant to the request.
2. Search and open their current official webmaster, crawler, structured-data, or publisher documentation.
3. Prefer primary sources. Record the access date and the rules that affect the implementation.
4. Distinguish confirmed platform requirements from general best practices and inferences.
5. Do not copy stale bot names, IP ranges, directives, submission endpoints, or unsupported files from memory.

If official sources cannot be reached, continue only with platform-neutral improvements. Mark platform-specific work as unverified and leave exact follow-up checks. Do not describe the platform-specific portion as complete.

## Workflow

### 1. Establish scope

- Determine whether the project is new, existing, or a targeted change.
- For a new public web project, include the search foundation automatically.
- For later changes, run this workflow only when public discovery, indexing, presentation, or answer extraction may be affected.
- Establish target audiences, regions, languages, conversion goals, and representative user questions from available evidence.
- Build a compact natural-language AI question map across applicable definition, how-to, comparison, alternative, recommendation, trust, commercial, local, and branded intents.

### 2. Audit before editing

Read [references/implementation-guide.md](references/implementation-guide.md) before auditing or implementing.

- Inspect public routes, rendering behavior, robots controls, HTTP headers, sitemap generation, canonical handling, redirects, status codes, metadata, structured data, internal links, and content accessibility.
- Identify whether critical content exists in initial HTML or requires client-side execution.
- Check whether CDN, WAF, authentication, rate limiting, or environment configuration can block legitimate crawlers.
- Review entity, trust, authorship, freshness, source attribution, and answer-extraction signals.
- Establish a platform-by-query AI visibility baseline only when the actual platforms can be queried. Otherwise preserve the query set and mark the baseline unavailable.
- Classify every material finding as `Critical`, `High`, `Medium`, or `Low`. Do not calculate a numeric score.
- Separate observed defects from opportunities and external promotion ideas.

### 3. Plan the smallest complete change

- Prioritize crawl/index blockers and misleading signals before content expansion.
- Reuse framework-native metadata, sitemap, robots, routing, and structured-data facilities.
- Map each proposed page or section to a distinct user intent. Avoid near-duplicate pages.
- Prefer strengthening a coherent topic cluster and first-party evidence over publishing many generic pages.
- Explain any business fact that needs confirmation before coding it.
- Keep backlink and external-visibility work as an ethical action plan; do not contact people, create accounts, publish externally, or purchase links unless the user separately authorizes those actions.

### 4. Implement

Apply relevant changes across these layers:

- **Discovery:** robots rules, sitemap, indexability, canonical URLs, redirects, status codes, crawlable internal links, and crawler access.
- **Search presentation:** titles, descriptions, language/locale signals, social metadata when useful, and consistent public URLs.
- **Entity and structured data:** accurate JSON-LD that matches visible page content and the page's actual type.
- **Answer readiness:** focused headings, concise direct answers, comparison data, definitions, steps, dates, authorship, sources, and clear update signals where appropriate.
- **Extractable knowledge:** self-contained passages that retain the named subject, scope, conditions, date, evidence, and necessary context when quoted alone.
- **Content coverage:** intent-led landing pages, guides, FAQs only when genuine, and internal links connecting related questions to product or service pages.
- **Trust:** transparent organization, contact, policy, author, methodology, and evidence pages appropriate to the site.
- **External visibility plan:** relevant publications, directories, partnerships, expert contributions, digital PR, reference-worthy assets, and unlinked brand-mention opportunities. Never recommend spam or paid-link schemes as organic authority.
- **Measurement:** project-supported analytics for AI referrals, branded demand, citations or mentions gathered through controlled runs, and business conversions. Never invent a visibility rate from one answer.

Implement only what the repository and verified business information support.

### 5. Verify locally

- Run the narrowest relevant formatter, lint, type-check, unit tests, build, and framework route/static generation checks.
- Inspect generated or served HTML—not only source components—for titles, canonical links, robots directives, headings, structured data, and crawlable content.
- Validate JSON-LD syntax and ensure it matches visible claims.
- Confirm robots and sitemap routes return the intended content and URLs.
- Exercise redirects, missing pages, and important public routes where feasible.
- Use `scripts/audit_url.py` against a local or preview server when HTTP access is available.

### 6. Verify live when possible

- If a production or preview URL is available, inspect the live response, final URL, rendered content, robots file, sitemap, headers, and structured data.
- Check for deployment-only blocks such as WAF challenges, authentication, `noindex`, incorrect hostnames, or stale caches.
- Check that staging, preview, mirror, and legacy hosts are intentionally protected or consolidated and do not publish duplicate canonical entities or stale facts.
- Do not make live verification a prerequisite when no live URL exists. Complete local verification and provide a precise post-deployment checklist instead.

### 7. Report

Read [references/report-template.md](references/report-template.md) before presenting the result.

Always deliver:

- A concise summary of code and content changes.
- A GEO/SEO audit and verification report using only `Critical`, `High`, `Medium`, and `Low` priorities.
- Content opportunities and representative target-user questions.
- The AI question map, visibility baseline when directly observable, and a repeatable measurement plan separating rank, mention, citation, referral, and conversion.
- A backlink and external-visibility action plan.
- A post-deployment checklist, including any live-only or officially unverified checks.
- Exact tests run, results, and limitations.

State explicitly that crawler access and optimization enable eligibility and improve clarity but do not guarantee indexing, ranking, recommendation, or citation.

## Live audit helper

Run:

```bash
python3 scripts/audit_url.py https://example.com
```

Use `--json` for machine-readable output. Treat its results as evidence for basic HTTP and HTML checks, not as a replacement for platform tools, rendered-page inspection, or current official documentation.
