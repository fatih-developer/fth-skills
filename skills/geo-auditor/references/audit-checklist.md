# Public Website Audit Checklist

Use only checks supported by public evidence. Mark anything else `Unavailable`; do not convert tool limitations into site failures.

## Contents

1. Scope and sampling
2. Official platform rules
3. Crawl and index eligibility
4. URL and internationalization
5. Search presentation and structured data
6. Content and answer readiness
7. Entity, trust, and safety
8. External credibility
9. Contradiction and freshness review
10. AI question map and visibility sampling
11. Measurement model
12. Evidence and priority tests

## 1. Scope and sampling

Record:

- Domain, canonical host if observable, audit date, markets, and languages.
- User goal: brand discovery, category visibility, citations, leads, ecommerce, local discovery, or comparison.
- Sampled page groups and why each represents the site.
- Pages or data that could not be reached.

Use representative sampling:

- Small site: homepage plus every important public page when practical.
- Medium/large site: homepage, conversion route, two or three important category/use-case pages, two informational pages, trust/about/policy, and representative locale variants.
- Focused request: audit only the named page plus its discovery and trust dependencies.

Never call a sample a complete crawl.

## 2. Official platform rules

For each requested platform capture:

- Official source URL and access date.
- Search-purpose crawler or fetcher behavior.
- Training-purpose controls when separately documented.
- Relevant robots, sitemap, metadata, structured-data, or publisher guidance.
- Whether a recommendation is required, recommended, optional, experimental, or merely inferred.

Do not treat `llms.txt`, AI-specific meta tags, content signals, Markdown negotiation, IndexNow, feeds, or proprietary files as universal requirements. Verify current platform support and describe their status precisely.

## 3. Crawl and index eligibility

Check when observable:

- Root `robots.txt` exists, parses coherently, declares intended sitemap locations, and does not block desired public search/citation agents.
- Training controls do not accidentally block search-purpose agents when the owner wants AI-search visibility.
- Important public pages are not blocked by robots, `noindex`, authentication, consent walls, or WAF challenges.
- Private, account, upload, admin, query, history, and internal-search routes are not promoted in public sitemaps.
- Sitemaps return usable content and contain canonical, indexable URLs from the intended host.
- Representative sitemap URLs resolve successfully and do not redirect unnecessarily.
- Public navigation exposes descriptive links to important pages.

Remember:

- Robots directives express crawler preferences; they are not authentication or data security.
- A failed audit fetch proves only that the auditor could not fetch it unless the returned response establishes a site failure.
- Sitemap submission supports discovery but does not guarantee indexing.

## 4. URL and internationalization

Check:

- One preferred HTTPS host and consistent URL conventions.
- Old and duplicate routes redirect to the current equivalent or have an intentional canonical strategy.
- Canonical targets match the page's actual language, intent, and index state.
- Localized pages communicate equivalent approved product facts.
- Language and direction are correct, especially for Arabic and other RTL locales.
- Hreflang annotations are reciprocal and use valid locale codes when actual HTML evidence is available.
- Language selectors use crawlable links and do not force geolocation-based redirects that hide alternatives.
- Slugs, breadcrumbs, titles, headings, and body copy do not mix languages accidentally.

Search for legacy indexed URLs and cached snippets, but label them `Indexed/cached` until live behavior is confirmed.

## 5. Search presentation and structured data

On representative pages check, when observable:

- Descriptive page-specific title and useful description.
- Clear H1 and coherent visible heading hierarchy.
- Stable canonical URL.
- Appropriate robots meta and response headers.
- Social metadata where sharing presentation matters.
- Structured data that matches visible content and the page/entity type.
- Organization identity and stable identifiers.
- Accurate author, reviewer, publication/modification dates, price, availability, rating, and policy facts.
- No schema for invisible FAQs, invented reviews, unsupported claims, or unrelated entities.

Do not report missing JSON-LD unless page source or a structured-data inspection proves it is absent.

## 6. Content and answer readiness

For each target intent assess:

- Does the page answer the main question in the opening section?
- Is the answer concise enough to extract yet supported by detail?
- Can the key passage stand alone while retaining the named subject, scope, conditions, date, and source context?
- Does it define terms and conditions that change the answer?
- Does it cite primary sources for changing or consequential facts?
- Does it show unique value beyond generic summaries?
- Are comparisons fair, scoped, dated, and evidenced?
- Are limitations and uncertainty visible near claims?
- Is the next action relevant and crawlably linked?
- Does the site cover a coherent topic cluster across definition, task, comparison, trust, and decision intents without thin keyword variants?

Map opportunities with:

- Representative user question.
- Search/answer intent.
- Existing route or new page brief.
- Unique evidence or first-party value required.
- Internal link source and conversion destination.

## 7. Entity, trust, and safety

Determine whether public evidence clearly establishes:

- Brand and legal operator.
- Product/service definition and intended audience.
- Supported regions, languages, channels, and limitations.
- Contact and support routes.
- Privacy, terms, refunds/cancellations where applicable, and data handling.
- Author/editor/reviewer identity or accountable role.
- Methodology, corrections process, research status, and update cadence.
- Safe-use warnings for consequential decisions.

Check consistency across visible pages, policies, FAQ, about, pricing, product facts, and structured data. Do not infer legal compliance from the existence of a policy page.

## 8. External credibility

Search for:

- Independent editorial mentions.
- Relevant professional or industry directories.
- Partner and integration pages.
- Expert quotes, research citations, podcasts, interviews, conference pages, and community resources.
- Reviews whose identity and context are visible.
- Unlinked brand mentions or inaccurate listings.

Assess relevance, independence, factual accuracy, recency, and likely referral quality. Do not fabricate backlink counts or recommend irrelevant high-volume placements.

Useful earned-visibility assets include:

- Original research and transparent methodology.
- Public datasets or benchmark summaries with clear licensing and limitations.
- Calculators, checklists, templates, and diagnostic tools.
- Expert guides, glossaries, comparison frameworks, and incident explainers.
- Integration documentation and partner case studies.

## 9. Contradiction and freshness review

Compare:

- Homepage versus pricing and checkout status.
- FAQ versus policies and product facts.
- Locale variants versus canonical language facts.
- Current pages versus legacy indexed routes.
- Visible claims versus structured data.
- Publication/update dates versus time-sensitive statements.
- Product availability versus calls to action.
- Methodology versus published accuracy or performance claims.

For every expiring claim recommend an owner, source of truth, expiry trigger, and verification route.

Also check public staging, preview, mirror, and legacy hosts discovered through links, search results, certificates, or redirects. Confirm their intended role when possible. An indexable staging host with duplicate or stale facts remains a finding even when it is not the production domain.

## 10. AI question map and visibility sampling

Create only applicable query groups:

- Definition: “What is X?”
- Task/how-to: “How do I accomplish Y?”
- Comparison: “X versus Y for this use case?”
- Alternative: “What are alternatives to X?”
- Recommendation: “Which product/service fits these constraints?”
- Trust: “Is X safe, accurate, compliant, or evidence-based?”
- Commercial: pricing, availability, compatibility, refunds, and limits.
- Local: service plus location and real decision constraints.
- Branded: product facts, operator, policies, and support.

For directly observable AI answers record:

| Field | Required observation |
|---|---|
| Platform/query | Exact platform and prompt wording |
| Context | Date, locale/market, login or personalization state when known |
| Brand | Mentioned, omitted, or misidentified |
| Citation | Exact cited URL and whether it is canonical/current |
| Accuracy | Correct, stale, contradictory, or unverifiable facts |
| Competitors | Relevant alternatives named in the same answer |

Do not simulate a platform answer with an ordinary web search. Do not convert one run into a percentage. If direct access is unavailable, deliver the query set as a measurement plan.

## 11. Measurement model

Keep metrics distinct:

- SEO discovery: index coverage, impressions, rank, CTR, organic sessions.
- AI visibility: sampled mention presence, citation presence, cited URL quality, factual accuracy, competitor inclusion, and share of observed citations across a controlled run set.
- Exposure proxies: branded search demand, direct visits, assisted conversions, and qualified referral growth.
- Business outcome: signup, lead, purchase, workflow import, or another verified conversion.

Record query set, platform, market, date, repetition count, and collection method so later runs are comparable. Treat model outputs as variable samples. Never infer business value from mention presence alone.

## 12. Evidence and priority tests

Use this evidence vocabulary:

| Label | Meaning |
|---|---|
| Observed | Current page/response evidence was directly inspected |
| Indexed/cached | Search engine or cached representation; live state not proven |
| Official rule | Current first-party platform documentation |
| Inference | Reasoned conclusion from multiple facts; label it explicitly |
| Unavailable | The audit could not establish the fact |

Before assigning a priority ask:

1. Is the finding confirmed rather than merely unavailable?
2. How many important page groups or users are affected?
3. Does it block discovery, misstate core facts, weaken trust, or only refine presentation?
4. Can the claim be tied to a sampled URL and evidence label?
5. Does the recommended action have an observable acceptance check?

Never use a numeric score. Never hide uncertainty to make the report look complete.
