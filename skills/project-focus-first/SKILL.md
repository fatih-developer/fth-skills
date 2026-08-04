---
name: project-focus-first
description: Force establishing and preserving the primary focus category before discussing any new project, product, web app, AI tool, business initiative, workflow, or job. Use when the user starts building, planning, evaluating, improving, or substantially changing something and the primary focus is not explicit. Do not proceed to features, tools, architecture, strategy, roadmap, or solutions until the user chooses one primary focus. Especially useful for non-technical users.
---

# Project Focus First

## Purpose

Establish one explicit **primary focus** before an assistant begins solving, designing, planning, evaluating, or implementing a new project.

The selected focus becomes the main decision filter for the rest of that project conversation. The assistant must not silently infer, replace, or change it.

This skill is a **hard gate**, not a general discovery questionnaire.

---

## Non-Negotiable Rule

When this skill is triggered and no primary focus has been explicitly established:

1. Ask the focus-category question.
2. Do not provide analysis, recommendations, features, tools, architecture, strategy, roadmap, implementation steps, or solutions.
3. Do not ask unrelated discovery questions.
4. Stop and wait for the user's answer.

The focus question must be the only substantive action in that response.

---

## Focus Categories

Use exactly these eight categories unless the user explicitly asks to revise the taxonomy:

1. **Ürün**
2. **Marketing / Büyüme**
3. **Mühendislik / Teknik**
4. **Araştırma / Keşif**
5. **Validasyon**
6. **Tasarım / Kullanıcı Deneyimi (UX)**
7. **Monetizasyon / İş Modeli**
8. **Operasyon / Sürdürülebilirlik**

### Category meanings

#### 1. Ürün
What should be built, for whom, which problem it solves, the value proposition, scope, MVP, user scenarios, and product priorities.

#### 2. Marketing / Büyüme
Positioning, messaging, target audience, acquisition channels, launch, conversion, retention, distribution, and growth loops.

#### 3. Mühendislik / Teknik
Architecture, technology choices, data model, APIs, integrations, security, performance, testing, deployment, scalability, and technical risks.

#### 4. Araştırma / Keşif
Understanding the problem space, users, market, competitors, technologies, uncertainties, opportunities, evidence, and research questions.

#### 5. Validasyon
Testing whether the problem, demand, proposed solution, willingness to use, or willingness to pay is real before committing significant resources.

#### 6. Tasarım / Kullanıcı Deneyimi (UX)
User journeys, information architecture, task flows, screens, interaction design, accessibility, usability, onboarding, and design systems.

#### 7. Monetizasyon / İş Modeli
Who pays, why they pay, pricing, revenue model, packaging, costs, margins, unit economics, sales motion, and business sustainability.

#### 8. Operasyon / Sürdürülebilirlik
How the product or process will be run, maintained, monitored, supported, documented, updated, governed, and kept reliable over time.

---

## Trigger Conditions

Trigger this skill when the user begins or substantially reframes any of the following:

- A new project
- A product or SaaS
- A web or mobile application
- An AI product, agent, assistant, automation, or tool
- A business idea or initiative
- A workflow, service, platform, internal system, or job to be designed
- A strategy whose main purpose is unclear
- A request to build, plan, improve, redesign, validate, monetize, launch, or scale something
- A direct technology or feature request for a project whose primary focus has not yet been established

Examples of trigger phrases include:

- “Bir web app geliştirmek istiyorum.”
- “Bir SaaS fikrim var.”
- “Bu AI ürününü nasıl yaparız?”
- “Yeni bir proje başlatalım.”
- “React mı Next.js mi kullanalım?” when the project focus is not already known
- “Bu ürünü geliştirelim.”

---

## Non-Trigger Conditions

Do not trigger this skill for a request that is clearly isolated and does not start or materially redirect a project, such as:

- Translation
- Rewriting or proofreading
- A simple factual question
- Solving a specific math problem
- Fixing a clearly scoped code error
- Explaining a single concept
- Summarizing supplied content
- Producing a narrowly specified standalone output
- Continuing the same project when its primary focus is already active

Do not ask the focus question merely because the user's request contains a technical term.

---

## Focus Gate Procedure

### Step 1: Detect project context

Determine whether the user is starting a new project or continuing an existing one.

A project is considered new when:

- It has a different purpose, target user, product, organization, or outcome.
- The user explicitly says they are starting something new.
- The current request cannot reasonably be treated as part of the active project.

Never carry the focus from one project into a different project automatically.

### Step 2: Check for an explicit primary focus

A focus is explicit when the user:

- Names one of the eight categories.
- Uses an unambiguous equivalent statement.
- Clearly distinguishes a primary and secondary focus.

Examples:

- “Ana odağımız validasyon.”
- “Önce ürün tarafını netleştirelim.”
- “Birincil odak teknik, ikincil odak operasyon.”

### Step 3: Apply the gate

If no explicit primary focus exists, ask the mandatory focus question and stop.

Use this default Turkish template:

> Bu çalışma için öncelikli odak noktamız hangisi?
>
> 1. Ürün  
> 2. Marketing / Büyüme  
> 3. Mühendislik / Teknik  
> 4. Araştırma / Keşif  
> 5. Validasyon  
> 6. Tasarım / Kullanıcı Deneyimi (UX)  
> 7. Monetizasyon / İş Modeli  
> 8. Operasyon / Sürdürülebilirlik  
>
> Bir numara veya kategori adıyla cevaplayabilirsin. Birden fazla alan önemliyse birini **ana odak**, diğerini **ikincil odak** olarak belirt.

Do not append recommendations, analysis, examples about the user's project, or a second question.

When the conversation language is not Turkish, translate the template while preserving the category meanings.

---

## Interpreting the User's Answer

### One category selected

Accept it immediately and activate it.

A brief acknowledgement is allowed:

> Ana odak: **Validasyon**

Then continue with the user's original request through that focus.

### Primary and secondary categories selected

Store both, but the primary category always controls prioritization.

Example state:

```text
PROJECT_CONTEXT: AI destekli eğitim uygulaması
PRIMARY_FOCUS: Ürün
SECONDARY_FOCUS: Tasarım / Kullanıcı Deneyimi (UX)
FOCUS_STATUS: active
```

### Multiple categories without priority

Ask only which one is primary:

> Bunlardan hangisi birincil odak olacak? Diğerini ikincil odak olarak koruyabiliriz.

Do not continue until one is selected.

### User says “Hepsi”

“Hepsi” is not a valid primary focus.

Reply:

> Hepsi proje için önemli olabilir; ancak kararları yönlendirebilmek için bir tanesini birincil odak olarak seçmemiz gerekiyor. Şu anda başarılması en kritik olan alan hangisi?

Then stop.

### Ambiguous answer

Do not silently map an ambiguous answer to a category.

Offer only the smallest distinction needed.

Example:

> Buradaki önceliğin hangisine daha yakın?
>
> - Ürünün doğru problemi çözmesi: **Ürün**
> - Kullanımın kolay ve anlaşılır olması: **Tasarım / UX**

Then stop.

### User refuses to choose

Explain the constraint once, briefly:

> Bu çalışma biçiminde çözüme geçmeden önce tek bir ana odak seçmemiz gerekiyor. En kritik sonucu belirleyen kategoriyi seçelim.

Do not proceed with the project solution.

---

## Persistent Focus State

Maintain the following conceptual state for each active project:

```text
PROJECT_CONTEXT: concise project identifier
PRIMARY_FOCUS: one of the eight categories
SECONDARY_FOCUS: optional category
FOCUS_STATUS: active | awaiting_selection
FOCUS_HISTORY: previous focus values, if changed
DEFERRED_TOPICS: relevant topics intentionally postponed
```

This state does not need to be shown in every response.

Do not claim that the state persists outside the capabilities of the current assistant environment. Within the available conversation or project context, use it consistently.

---

## Focus as a Decision Filter

Before each substantive response, silently evaluate:

1. Does this response directly advance the primary focus?
2. Is the proposed detail necessary at the current stage?
3. Is the assistant drifting into another category?
4. Should an off-focus topic be limited, deferred, or used only as supporting information?
5. What is the smallest meaningful next step under the active focus?

Prefer depth in the active focus over breadth across all categories.

---

## Behavior by Primary Focus

### Ürün
Prioritize:

- User and problem
- Value proposition
- Core use case
- Product boundaries
- MVP
- Feature prioritization
- Product roadmap

Keep technology discussion limited to what is required to make product decisions.

### Marketing / Büyüme
Prioritize:

- Audience
- Positioning
- Message
- Distribution
- Acquisition
- Conversion
- Retention
- Growth loops

Treat product or engineering details as supporting constraints only.

### Mühendislik / Teknik
Prioritize:

- Requirements
- Architecture
- Data model
- Integrations
- Security
- Performance
- Deployment
- Testing
- Technical risks

Do not expand the product scope unless technically necessary.

### Araştırma / Keşif
Prioritize:

- Unknowns
- Research questions
- Evidence
- Sources
- User and market understanding
- Competitors
- Technology landscape
- Opportunity areas

Avoid presenting unverified assumptions as final decisions.

### Validasyon
Prioritize:

- Riskiest assumption
- Testable hypothesis
- Cheapest meaningful experiment
- Success and failure criteria
- Real behavior and demand signals
- User feedback

Do not recommend substantial implementation before the critical assumptions are tested.

### Tasarım / Kullanıcı Deneyimi (UX)
Prioritize:

- User journey
- Task flow
- Information architecture
- Screens
- Interaction
- Accessibility
- Usability
- Onboarding

Do not place visual aesthetics above comprehension and task completion.

### Monetizasyon / İş Modeli
Prioritize:

- Payer
- Value exchanged
- Revenue model
- Pricing
- Packaging
- Costs
- Margins
- Unit economics
- Sales model

Do not create a broad feature list disconnected from willingness to pay.

### Operasyon / Sürdürülebilirlik
Prioritize:

- Ownership
- Maintenance
- Monitoring
- Support
- Documentation
- Data and content operations
- Reliability
- Cost control
- Governance
- Continuity

Evaluate the ongoing system, not only the initial build.

---

## Managing Off-Focus Requests

### The request supports the primary focus

Handle it, but explicitly connect it to the primary focus when useful.

Example:

> Ana odak validasyon olduğu için prototipi yalnızca talebi test edecek minimum kapsamda ele alacağım.

### The request is relevant but premature

Defer it without dismissing it.

Example:

> Bu konu önemli; ancak mevcut ana odağımız Ürün olduğu için ayrıntılı teknoloji seçimini ürün kapsamı netleştikten sonra ele almak daha doğru olur.

Add it conceptually to `DEFERRED_TOPICS`.

### The request would materially change the focus

Ask for an explicit focus decision:

> Bu istek çalışmanın odağını **Ürün**’den **Mühendislik / Teknik** alana taşıyor. Ana odağı değiştirelim mi, yoksa bunu mevcut ürün odağını destekleyen sınırlı bir teknik konu olarak mı ele alalım?

Do not change focus without the user's answer.

---

## Changing Focus

The user may change focus explicitly at any time.

Examples:

- “Şimdi teknik tarafa geçelim.”
- “Validasyon tamam; artık ürün odağıyla ilerleyelim.”
- “Önceliğimiz artık monetizasyon.”

Acknowledge the change briefly:

> Ana odak güncellendi: **Mühendislik / Teknik**

Store the previous focus in `FOCUS_HISTORY` and continue under the new focus.

Do not force the user to answer the full eight-category question when the new focus is already explicit.

---

## Non-Technical User Guidance

When the user is non-technical:

- Start from goals, users, inputs, outputs, and constraints.
- Avoid unnecessary jargon.
- Do not ask the user to choose technologies they cannot reasonably evaluate.
- Translate technical decisions into business or user consequences.
- Present technical options only after the focus is active and only when relevant.
- Make recommendations instead of transferring all technical decisions to the user.

Bad question:

> PostgreSQL mi MongoDB mi kullanmak istiyorsun?

Better question after the focus is active:

> Uygulamadaki bilgiler çoğunlukla düzenli kayıtlar mı olacak, yoksa belge ve serbest metin ağırlıklı mı?

---

## Forbidden Behavior Before Focus Selection

Before the primary focus is selected, do not say or do things such as:

- “React kullanalım.”
- “Önce MVP yapalım.”
- “Şu özellikler olmalı.”
- “Landing page hazırlayalım.”
- “Rakip analizi yapmalısın.”
- “Freemium model uygun olur.”
- “PostgreSQL seçelim.”
- “İşte yol haritası.”
- “Önce hedef kitleni belirle.”
- Produce code, schemas, prompts, plans, mockups, or implementation instructions

Each of these assumes a focus that the user has not chosen.

---

## Response-Length Rule

The focus-gate response must be concise.

Before selection:

- Show the eight categories.
- Explain how to answer in one sentence.
- Do not add project-specific analysis.

After selection, response depth may match the user's request.

---

## Priority and Conflict Handling

This skill controls project-flow behavior but does not override:

1. System instructions
2. Safety policies
3. Explicit higher-priority developer instructions
4. Tool requirements
5. Direct user constraints that do not conflict with the focus gate

When the user requests an immediately necessary safety, legal, medical, or security response, address the urgent issue first. Do not delay critical harm-prevention information merely to ask a focus category.

When a platform requires an action before questions can be asked, perform the required action and then apply this skill at the earliest valid point.

---

## Examples

### Example 1: New application

User:

> Yapay zekâ destekli bir eğitim uygulaması geliştirmek istiyorum.

Assistant:

> Bu çalışma için öncelikli odak noktamız hangisi?
>
> 1. Ürün  
> 2. Marketing / Büyüme  
> 3. Mühendislik / Teknik  
> 4. Araştırma / Keşif  
> 5. Validasyon  
> 6. Tasarım / Kullanıcı Deneyimi (UX)  
> 7. Monetizasyon / İş Modeli  
> 8. Operasyon / Sürdürülebilirlik  
>
> Bir numara veya kategori adıyla cevaplayabilirsin. Birden fazla alan önemliyse birini **ana odak**, diğerini **ikincil odak** olarak belirt.

Stop.

### Example 2: Premature technology request

User:

> Bir SaaS fikrim var. React mı Next.js mi kullanmalıyım?

Assistant asks the focus question. It does not compare React and Next.js yet.

### Example 3: Explicit focus in the first message

User:

> Bir iş takip uygulaması geliştireceğim. Öncelikle fikri doğrulamak istiyorum.

Assistant:

> Ana odak: **Validasyon**

Then answer the user's request through validation, without repeating the focus question.

### Example 4: Equal priorities

User:

> Ürün ve teknik birlikte önemli.

Assistant:

> İkisini de ele alabiliriz; ancak hangisi birincil odak olacak? Diğerini ikincil odak olarak koruyabiliriz.

Stop.

### Example 5: New project in the same conversation

The active project is an AI résumé tool with primary focus `Ürün`.

User:

> Şimdi de restoranlar için rezervasyon sistemi geliştirmek istiyorum.

Assistant treats this as a new project and asks the focus question again.

### Example 6: Isolated bug fix

User:

> Bu SQL sorgusundaki ORA-00904 hatasını düzelt.

Assistant does not trigger this skill. It handles the scoped bug.

---

## Internal Pre-Response Checklist

Before each project-related answer, verify:

- Is this a new project?
- Does this project have an explicit primary focus?
- Is the selection truly unambiguous?
- Did the user select multiple categories without priority?
- Is the response aligned with the primary focus?
- Am I expanding an off-focus topic unnecessarily?
- Does the user's latest request imply a focus change?
- Am I carrying a focus from a different project?
- Am I asking a non-technical user to make an unjustified technical choice?
- What is the smallest meaningful next step?

If the focus is missing, ask only the focus question and stop.

---

## Success Criteria

The skill is working correctly when:

1. Every new project receives an explicit primary focus.
2. No project solution is produced before focus selection.
3. The assistant does not silently infer a focus from weak signals.
4. The selected focus guides later decisions.
5. Off-focus topics are connected, limited, deferred, or escalated for a focus-change decision.
6. New projects do not inherit the previous project's focus.
7. Focus changes require explicit user intent.
8. Non-technical users are not burdened with premature technical choices.
9. Responses prioritize the active goal instead of covering every possible category.
10. The assistant advances the smallest meaningful next step under the active focus.
