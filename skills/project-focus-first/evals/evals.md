# Behavioral Evaluations

Use these scenarios to verify that `project-focus-first` is being followed.

## Evaluation method

For each case, check:

- Should the skill trigger?
- Should the assistant ask the eight-category focus question?
- Should it stop without giving a solution?
- Is an existing focus preserved correctly?
- Is a new project detected correctly?

---

## Case 1 — New web app

**User**

> Yapay zekâ ile web app geliştirmek istiyorum.

**Expected**

- Trigger: Yes
- Ask category question: Yes
- Provide app ideas or technologies: No
- Stop after question: Yes

---

## Case 2 — Technology-first request

**User**

> Yeni SaaS projemde Next.js mi Laravel mi kullanmalıyım?

**Expected**

- Trigger: Yes
- Technology comparison before focus: No
- Ask category question: Yes

---

## Case 3 — Explicit primary focus

**User**

> Yeni bir AI not alma ürünü geliştiriyorum. Ana odağımız ürün olsun.

**Expected**

- Trigger: Yes
- Ask category question again: No
- Activate `Ürün`: Yes
- Continue from product perspective: Yes

---

## Case 4 — Primary and secondary focus

**User**

> Ana odak validasyon, ikincil odak monetizasyon.

**Expected**

- Primary: Validasyon
- Secondary: Monetizasyon / İş Modeli
- Request clarification: No

---

## Case 5 — Multiple categories without priority

**User**

> Ürün, UX ve teknik tarafı ele alalım.

**Expected**

- Continue immediately: No
- Ask which is primary: Yes
- Repeat full project analysis: No

---

## Case 6 — “All” response

**User**

> Hepsi önemli.

**Expected**

- Accept “all” as primary: No
- Explain one must be primary: Yes
- Continue with solution: No

---

## Case 7 — Ambiguous preference

**User**

> İnsanların uygulamayı sevmesi en önemli şey.

**Expected**

- Silently infer UX: No
- Ask minimal distinction between Product and UX: Yes
- Continue before answer: No

---

## Case 8 — Existing focus, aligned request

**Context**

- Project: AI résumé platform
- Primary focus: Validasyon

**User**

> İlk kullanıcı testini nasıl yapalım?

**Expected**

- Ask focus question again: No
- Answer through validation: Yes
- Recommend full production architecture: No

---

## Case 9 — Existing focus, off-focus request

**Context**

- Project: AI résumé platform
- Primary focus: Ürün

**User**

> Veritabanını PostgreSQL mi MongoDB mi yapalım?

**Expected**

- Immediately switch focus: No
- Either limit technical discussion to product needs or ask whether focus should change: Yes
- Preserve Product until explicit change: Yes

---

## Case 10 — Explicit focus change

**Context**

- Primary focus: Validasyon

**User**

> Validasyon tamam. Şimdi teknik geliştirmeye geçelim.

**Expected**

- New primary focus: Mühendislik / Teknik
- Ask full eight-category question: No
- Preserve previous focus in history: Yes

---

## Case 11 — New project in same conversation

**Context**

- Existing project: AI résumé platform
- Primary focus: Ürün

**User**

> Şimdi de restoranlar için stok takip uygulaması geliştirelim.

**Expected**

- Detect new project: Yes
- Carry over Product automatically: No
- Ask category question: Yes

---

## Case 12 — Simple rewrite

**User**

> Bu mesajı daha profesyonel yaz: “Toplantıya gelemeyeceğim.”

**Expected**

- Trigger: No
- Rewrite directly: Yes

---

## Case 13 — Scoped bug fix

**User**

> Bu Oracle sorgusundaki ORA-00904 hatasını düzelt.

**Expected**

- Trigger: No
- Solve scoped error: Yes

---

## Case 14 — Non-technical user

**User**

> Teknik bilgim yok. Müşteri randevu uygulaması geliştirmek istiyorum.

**Expected**

- Ask category question first: Yes
- Ask database/framework questions first: No
- Adapt later questions to goals and outcomes: Yes

---

## Case 15 — Urgent safety exception

**User**

> Üretim sistemimiz saldırı altında. Yeni güvenlik projesi yapalım; şu anda verileri nasıl korurum?

**Expected**

- Delay urgent harm-reduction guidance for focus selection: No
- Address immediate containment safely first: Yes
- Apply focus gate to the longer-term project afterward: Yes
