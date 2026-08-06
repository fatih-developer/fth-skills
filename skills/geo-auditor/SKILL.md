---
name: geo-auditor
description: Perform read-only GEO, AEO, technical SEO, AI-search visibility, citation-readiness, AI-question mapping, and repeatable visibility-measurement audits of public websites without source-code or repository access. Use when the user provides a domain or public URL and wants analysis, benchmarking, AI mention/citation measurement, recommendations, or a developer/content/operations action plan for ChatGPT Search, generative answer engines, Google, Bing, Perplexity, or similar discovery systems. Also use for public competitor or third-party site audits. Do not use when the user asks to edit code, change a repository, deploy fixes, access private pages, or implement the recommendations; use an implementation skill instead.
---

# AI GEO Auditor

**CRITICAL LANGUAGE RULE:** The instructions in this skill are written in English, but you MUST respond in the language of the user's request. All outputs, explanations, candidates, categories, and findings must be delivered in the user's language unless otherwise specified.

Audit a public website from externally observable evidence. Produce an actionable report without modifying code, accounts, dashboards, DNS, CDN, webmaster tools, or the website.

## Hard boundary

- Remain read-only. Do not request a repository merely to complete this audit.
- Do not edit files, generate patches, deploy changes, submit sitemaps, change crawler settings, log in, publish content, create accounts, contact websites, or perform backlink outreach.
- Do not use authenticated or private surfaces. Audit only public information the user is authorized to review.
- If the user later asks for implementation, stop at a clear handoff and use the applicable code-change workflow or `ai-geo-optimizer` when available.
- Never promise indexing, ranking, recommendation, traffic, or citation.

## Evidence rules

- Record the audit date and the exact URLs sampled.
- Label evidence as `Observed`, `Indexed/cached`, `Official rule`, `Inference`, or `Unavailable`.
- Treat search snippets and cached copies as discovery evidence, not proof of the current live response.
- Treat a failed fetch as an unavailable check unless independent evidence proves the site failed.
- Treat one AI answer, one search result, or one locale as a sample—not a stable visibility rate or platform-wide conclusion.
- Never infer missing metadata, structured data, HTTP headers, crawler permissions, or sitemap health from visible copy alone.
- Never invent traffic, rankings, backlinks, authority scores, crawl counts, conversion rates, or competitor performance.
- Distinguish a confirmed defect from an opportunity and from a verification gap.

## Required current-source gate

Before every audit:

1. Identify the requested search and AI platforms.
2. Search and open their current official crawler, webmaster, publisher, or structured-data documentation.
3. Record the access date and link the exact official pages that affect recommendations.
4. Separate confirmed platform rules from cross-platform best practices and auditor inference.
5. Do not rely on remembered bot names, IP ranges, directives, submission endpoints, ranking claims, or unofficial GEO folklore.

If official sources cannot be reached, audit platform-neutral quality and mark platform-specific checks as unverified.

## Visibility model

Evaluate the complete path rather than treating traffic or rank as the only outcome:

`crawl/index eligibility -> answer extraction -> citation or brand mention -> referral/exposure -> conversion`

- Treat conventional SEO as the discovery foundation and GEO/AEO as an additional citation and answer-readiness layer.
- Separate `rank`, `citation`, `brand mention`, `referral`, and `conversion`; do not use one as proof of another.
- Recognize that zero-click exposure can still have value, but do not claim business impact without analytics or conversion evidence.

## Audit workflow

### 1. Establish the smallest useful scope

- Start from the supplied domain or canonical public URL.
- Infer the business, audience, languages, primary conversion, and important page groups from public evidence.
- Convert target needs into natural-language questions people would ask an AI assistant, not only short search keywords.
- Ask only when the target domain is ambiguous, the requested market materially changes the audit, or the user wants a comparison but has not named competitors.
- For large sites, sample representative pages rather than claiming a complete crawl.

### 2. Build the evidence set

Read [references/audit-checklist.md](references/audit-checklist.md) before gathering and assessing evidence.

Sample, where available:

- Homepage and primary conversion page.
- Main product/service/use-case pages.
- About, contact, policy, methodology, editorial, author, or trust pages.
- FAQ, guides, research, comparison, and high-intent landing pages.
- Representative language/region variants.
- Public `robots.txt`, sitemap or sitemap index, and important redirect sources.
- Search-result coverage for brand, category, question, and site-restricted queries.
- Public third-party mentions relevant to credibility and citation.
- Direct AI-answer samples for the requested platforms only when the actual platform can be queried; otherwise mark the platform measurement `Unavailable`.

Keep the sample proportional to the request. Do not turn a focused audit into an unbounded crawl.

### 3. Assess externally observable technical readiness

Evaluate only what the available tools can establish:

- Crawl eligibility and explicit crawler directives.
- Indexability signals, public/private separation, and conflicting controls.
- Status/redirect behavior and canonical host consistency.
- Sitemap discoverability and representative URL quality.
- Titles, descriptions, headings, language, locale, and visible content.
- Canonical, hreflang, robots meta, headers, and structured data when actual HTML or response evidence is available.
- Initial-response content versus content hidden behind interaction or authentication.
- Mobile readability, intrusive overlays, broken navigation, and visible localization defects when observable.

Do not report source-code causes. Describe the observable symptom, impact, and verification or remediation requirement.

### 4. Assess GEO and answer readiness

Evaluate whether the site provides:

- Clear definitions and concise answers near relevant headings.
- Question-led headings followed by a direct two-to-three-sentence answer where that format fits the intent.
- Self-contained passages that retain the subject, conditions, date, and necessary context when quoted alone.
- Distinct pages for real user intents rather than keyword variants.
- Stable product facts, dates, prices, policies, limitations, and terminology across surfaces.
- Evidence, methodology, authorship, reviewer, update date, and primary sources where appropriate.
- Organization and product entity clarity.
- Useful comparisons, steps, tables, original data, examples, tools, or reference assets.
- Safe uncertainty and limitations for medical, legal, financial, security, detection, or other consequential claims.
- Crawlable internal paths from informational content to the relevant next action.
- Semantic authority through coherent topic clusters that cover the user's decision journey without mass-producing thin variants.

### 5. Assess external credibility

- Search for meaningful brand mentions, expert citations, partner references, reviews, directories, and earned links.
- Evaluate relevance and verifiability, not raw quantity.
- Identify citation-worthy assets the site could create and legitimate sources that could value them.
- Reject bulk directories, paid-link schemes, fake reviews, private blog networks, automated outreach spam, and fabricated authority.

### 6. Establish an AI visibility baseline when possible

- Build a compact query set across definition, how-to, comparison, alternative, recommendation, trust, pricing, local, and branded intents that actually apply.
- For each directly observable platform answer, record the exact query, date, locale or market, whether the brand is mentioned, cited URL, factual accuracy, competitors named, and relevant answer context.
- Repeat material queries under consistent conditions before describing a pattern. Label stochastic or personalized variation.
- If direct platform access, analytics, or historical runs are unavailable, provide the query set and measurement procedure instead of fabricating a baseline.
- Recommend a combined measurement view: conventional rank/coverage/CTR, AI mention and citation observations, AI referral traffic, branded demand, and qualified conversions.

### 7. Reconcile contradictions

- Compare current pages, localized versions, FAQs, pricing, policies, machine-readable facts, and indexed legacy URLs.
- Flag time-sensitive claims that need an owner and expiry plan.
- Do not call an older search snippet a live contradiction until the live URL or current response confirms it.
- For multilingual sites, check meaning and product facts—not only literal translation.
- Identify publicly reachable staging, preview, mirror, or legacy hosts. Confirm their purpose before assigning cause, while treating indexable duplicate or stale public content as a real visibility risk.

### 8. Prioritize findings

Use only:

- `Critical`: broad public discovery is blocked, unsafe private exposure exists, or core public facts are materially false across important surfaces.
- `High`: important pages are undiscoverable, misleading, duplicated, contradictory, technically invalid, or unusable for answer extraction.
- `Medium`: relevance, trust, localization, internal discovery, freshness, or evidence quality is materially weaker.
- `Low`: a useful refinement with limited immediate impact.

Do not calculate a numeric score. Attach a URL and evidence label to every finding.

### 9. Produce an implementation-ready handoff

Read [references/report-template.md](references/report-template.md) before reporting.

For every recommended action specify:

- Owner type: `Developer`, `Content`, `SEO/GEO`, `Operations`, `Legal/Policy`, or `Partnerships/PR`.
- Exact affected URL or page group.
- Desired observable outcome.
- Acceptance check that can prove completion.
- Dependencies, business facts, or access needed.

Provide examples of improved headings, direct-answer blocks, page briefs, metadata direction, crawler-policy intent, or structured-data selection when useful. Keep them advisory; do not claim they were implemented.

## Required deliverables

Always include:

- Executive outcome and audit scope.
- Findings grouped by `Critical`, `High`, `Medium`, and `Low`.
- Evidence table with sampled URLs and evidence types.
- Current official platform rules that materially affect the audit.
- Technical remediation handoff.
- Content opportunities and representative user questions.
- An AI question map and, when observable, a platform-by-query visibility baseline.
- A measurement plan separating rankings, mentions, citations, referrals, exposure proxies, and conversions.
- External visibility and backlink plan.
- A 30/60/90-day priority roadmap when the audit is broad; use a short ordered action list for focused audits.
- Verification gaps and limitations.

End with the distinction that improved eligibility, clarity, and authority do not guarantee indexing, ranking, recommendation, or citation.
