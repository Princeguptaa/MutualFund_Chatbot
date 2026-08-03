# PRD: Mutual Fund FAQ Assistant (RAG-Powered, Facts-Only)

**Product Context:** Groww
**AMC in Scope:** SBI Mutual Fund (SBI Bluechip Fund, SBI Flexicap Fund, SBI Long Term Equity Fund, SBI Small Cap Fund)
**Document Owner:** Senior PM
**Status:** Draft v1
**Related Doc:** `problemstatement.md`

---

## 1. Executive Summary

Groww users repeatedly ask a small, predictable set of factual questions about mutual fund schemes — expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, and how to download statements. These questions have single, correct, publicly documented answers, yet today they are resolved through slow, inconsistent, or untrustworthy channels.

This PRD proposes a **RAG-powered, facts-only FAQ Assistant** that retrieves answers exclusively from official AMC/AMFI/SEBI sources, cites exactly one source per answer, and refuses any advisory or opinion-seeking query. The bet is narrow and deliberate: **trade broad conversational ability for verifiable, compliant, citation-backed accuracy** on a well-bounded set of factual intents.

---

## 2. Why This Product Would Work

**2.1 The query pattern is narrow and stable.**
Mutual fund facts (expense ratio, lock-in, exit load, minimum SIP, riskometer, benchmark) don't require reasoning or judgment — they require *lookup*. This is close to the ideal RAG use case: a small, well-structured, low-ambiguity corpus where retrieval quality directly determines answer quality, and where "I don't know, here's the source" is an acceptable and safe fallback.

**2.2 Compliance risk is reduced, not increased, by scoping down.**
Most AI assistants in the fintech space get into regulatory trouble by drifting into advice ("should I invest?"). By explicitly refusing advisory intents and anchoring every factual answer to a citation, this product is *more* conservative than a human support agent improvising an answer — which makes it easier to greenlight internally and defend externally.

**2.3 It reduces cost where cost is highest: repetitive, low-complexity support volume.**
Support and content teams don't need AI to handle nuanced escalations — they need relief from the long tail of "what's the exit load on X" tickets that consume agent time without requiring judgment. Deflecting even a fraction of this volume is a direct cost saving with low deployment risk.

**2.4 Trust is the actual product, not the chat interface.**
Retail investors already tolerate clunky UX if the information is verifiably correct. A visible citation on every answer is a trust mechanism, not a nice-to-have — it lets a skeptical user self-verify in one click, which is what separates this from both blog aggregators (no verifiability) and generic LLM chatbots (no grounding).

**2.5 It's a wedge, not a ceiling.**
Starting with one AMC and a handful of schemes keeps the corpus small enough to get retrieval accuracy right before scaling. The architecture (retrieval + citation + refusal-classification) generalizes cleanly to more AMCs, more schemes, and eventually more product surfaces — which is exactly why the brief ties this milestone to a follow-on challenge.

---

## 3. Market Landscape & Alternatives

| Alternative | What it does | Where it falls short |
|---|---|---|
| **AMC websites / factsheets / SID-KIM** | Authoritative source of truth | Dense, not searchable in natural language; users must know what a "riskometer" or "SID" even is |
| **Groww's existing help center / support chat** | Human or scripted support for account/factual queries | Slow (ticket queues), inconsistent phrasing across agents, doesn't scale with query volume, no built-in citation habit |
| **Competitor apps (e.g., ET Money, Kuvera, Zerodha Coin) assistants** | Some offer FAQ bots or fund-comparison tools | Comparison/recommendation features often blur into advisory territory; not consistently citation-first |
| **Generic LLM chatbots (ChatGPT, etc.)** | Conversational, flexible | No grounding in current official data, prone to hallucinated numbers (expense ratios, lock-ins), no source citation, no domain-specific refusal behavior |
| **Third-party finance blogs / aggregator sites** | Easy to read, SEO-optimized | Frequently outdated, sometimes wrong, monetization incentives can bias framing, not authoritative |
| **Community forums (Reddit, Quora, Telegram groups)** | Fast, informal answers | No accountability, high variance in accuracy, occasionally conflates fact with opinion |

**The gap this product fills:** nothing in the market combines (a) natural-language access, (b) grounding in official sources, (c) mandatory per-answer citation, and (d) a hard behavioral wall against advisory drift, in one place.

---

## 4. User Pain Points (With Anecdotes)

**4.1 "I didn't know ELSS had a lock-in until I tried to withdraw."**
A first-time investor puts money into an ELSS fund because a friend said "it saves tax." Two years later they try to redeem and discover a 3-year lock-in they never noticed in the KIM. They didn't misread anything — they never read it, because the information lived in a 40-page document they never opened.

**4.2 "I got charged an exit load I didn't expect."**
A user redeems units nine months after investing and sees a deduction they didn't budget for. When they search "exit load" in the app, they find a support article that's a year old and references an outdated slab. They open a support ticket; it takes two days to get a definitive answer that could have been a one-line lookup.

**4.3 "Support gave me a different answer than the website."**
A user asks two different support agents about the minimum SIP amount for the same fund on two different days and gets two slightly different answers — one agent quotes the number from memory, the other looks it up but reads an old cached page. Neither response includes a source link, so the user has no way to resolve the discrepancy themselves.

**4.4 "I just want the riskometer and benchmark, but I have to open three tabs."**
A user comparing schemes before investing has to separately open the factsheet, the SID, and the AMC's FAQ page to piece together riskometer classification, benchmark index, and category — a five-minute task for a fact that should take five seconds.

**4.5 "The support team is drowning in the same ten questions."**
From the content/support side: agents report that a large share of daily tickets are the same handful of factual questions repeated across thousands of users and hundreds of schemes. This isn't a knowledge problem for the team — they know the answers — it's a throughput problem.

**4.6 "I couldn't find how to download my capital gains statement, so I called support just for that."**
A user needing a capital-gains statement for tax filing can't locate the download flow through search or FAQ pages, and ends up making a support call for what should be a self-serve, one-step action.

---

## 5. Goals & Success Metrics

### 5.1 Primary Goal
Deflect repetitive factual mutual fund queries from human support/content channels into a self-serve, citation-backed assistant — without introducing advisory or compliance risk.

### 5.2 North Star Metric
**Verified Self-Resolution Rate** — % of factual MF queries fully answered by the assistant (correct fact + valid citation) without escalation to a human or the user re-searching elsewhere.

### 5.3 Supporting Metrics

| Metric | Target (MVP) | Why it matters |
|---|---|---|
| Citation accuracy rate | ≥ 98% of factual answers link to the *correct* source page | Core trust mechanism; a wrong citation is worse than no citation |
| Factual accuracy rate (human-audited sample) | ≥ 97% | Direct measure of the product's only real value proposition |
| Refusal precision (advisory queries correctly refused) | ≥ 95% | A missed refusal is a compliance incident, not just a UX miss |
| Refusal recall (facts wrongly refused) | ≤ 5% false-refusal rate | Over-refusing kills usefulness; needs to be tracked as a counter-metric to precision |
| PII rejection rate | 100% | Non-negotiable — any leakage is a hard failure, tracked as a guardrail metric, not a target to optimize |
| Median response latency | < 3 seconds | Keeps the experience feeling instant relative to opening a long document |
| Support ticket deflection (of in-scope categories) | ≥ 25% reduction within 60 days of pilot | Direct cost/efficiency signal for the business case |
| User-reported trust (post-answer "was this correct?" thumbs) | ≥ 90% positive | Leading indicator of whether citation-first design is working |

### 5.4 Guardrail Metrics (must not regress)
- Zero instances of stored/logged PII across the query pipeline
- Zero answers containing computed or compared returns/performance figures
- Zero advisory statements in facts-only responses (audited via sampled review)

---

## 6. Features to Build

### 6.1 Core Retrieval & Answering Engine (RAG)
- Ingestion pipeline for the curated 15–25 URL corpus (scheme pages, FAQ pages, AMFI/SEBI pages, and factsheet indices). Below is a verified starting list pulled directly from official domains (`sbimf.com`, `amfiindia.com`, `mutualfundssahihai.com`, `portal.amfiindia.com`) — confirm each is live and current before final ingestion, since AMC pages get renamed/restructured periodically:

  **Scheme pages (sbimf.com)**
  - SBI Large Cap Fund (formerly SBI Bluechip Fund) — scheme page: `https://www.sbimf.com/sbimf-scheme-details/sbi-large-cap-fund-(formerly-known-as-sbi-bluechip-fund)-43`
  - SBI Flexicap Fund — scheme page: `https://www.sbimf.com/sbimf-scheme-details/sbi-flexicap-fund-39`
  - SBI ELSS Tax Saver Fund (formerly SBI Long Term Equity Fund) — scheme page: `https://www.sbimf.com/sbimf-scheme-details/sbi-elss-tax-saver-fund-(formerly-known-as-sbi-long-term-equity-fund)-3`
  - SBI Small Cap Fund — scheme page: `https://www.sbimf.com/sbimf-scheme-details/sbi-small-cap-fund-329`

  **Factsheet Index (sbimf.com)**
  - Full factsheet index (use to pull current-month data): `https://www.sbimf.com/factsheets`

  **AMC FAQ / help / statements (sbimf.com)**
  - AMC FAQ page: `https://www.sbimf.com/faq`
  - Get Statement (Account / Capital Gain / Smart / Tax Statement): `https://online.sbimf.com/dashboard/statement-account`
  - Ways to Invest (statement access flow): `https://www.sbimf.com/ways-to-invest`
  - Grievance Redressal: `https://www.sbimf.com/grievance-redressal`
  - Contact Us (branch/toll-free/chatbot): `https://www.sbimf.com/contact-us`

  **AMFI / regulatory pages**
  - AMFI Risk-o-Meter disclosures (official, per-scheme): `https://www.amfiindia.com/online-center/risk-o-meter`
  - AMFI Investor Education — "What is a Riskometer": `https://www.mutualfundssahihai.com/en/how-riskometer-scheme-derived`
  - AMFI Investor Education — "What is Lock-in Period" (ELSS): `https://www.mutualfundssahihai.com/en/what-is-lock-in-period`

  Note: two of the four schemes have been renamed by the AMC (SBI Bluechip Fund → SBI Large Cap Fund; SBI Long Term Equity Fund → SBI ELSS Tax Saver Fund). The assistant's answers and citations should reference the current official name, with the former name recognized as a synonym at the retrieval/intent-matching layer so users searching either name get a correct, non-hallucinated match.
- Chunking strategy tuned for web pages
- Embedding + vector retrieval (top-k relevant chunks per query)
- Source-URL metadata attached to every retrieved chunk, carried through to the final answer
- Answer generation constrained to: ≤3 sentences, exactly one citation, mandatory "Last updated from sources: `<date>`" footer

### 6.2 Query Intent Classifier (Pre-Retrieval Gate)
- Classifies incoming query into: `factual` / `advisory-opinion` / `performance-comparison` / `PII-containing` / `out-of-corpus`
- Routes `factual` → retrieval pipeline
- Routes `advisory-opinion` and `performance-comparison` → standardized refusal template + educational link (no retrieval call needed)
- Routes `PII-containing` → immediate rejection, no storage, no forwarding to any downstream model call

### 6.3 Refusal & Redirection Templates
- Polite, consistent refusal copy for advisory/opinion queries
- Distinct copy for performance/return questions (redirect to official factsheet link only)
- Distinct copy for PII detection (explains why, does not echo back the detected PII)

### 6.4 Minimal Chat UI
- Welcome message + 3 example questions
- Persistent disclaimer: "Facts-only. No investment advice."
- Per-answer citation link rendered as a clickable source
- Per-answer "Last updated" footer

### 6.5 Corpus Freshness & Admin Tooling (internal-facing)
- Source registry mapping each URL to a "last verified" timestamp
- Lightweight re-crawl/refresh job to catch factsheet updates (factsheets are typically refreshed monthly)
- Alerting when a source URL 404s or content structure changes materially (broken citation risk)

### 6.6 Privacy & Safety Layer
- PII pattern detection (PAN, Aadhaar, account numbers, OTP formats, emails, phone numbers) at the input layer, before any query reaches retrieval or generation
- No conversation logging of raw user input where PII patterns are detected; only sanitized/aggregate analytics retained

### 6.7 Analytics & Feedback Loop
- Per-answer thumbs up/down feedback capture (no PII attached)
- Query-category tagging for support-team visibility into what's being deflected
- Weekly accuracy sampling workflow for human audit of citation correctness

---

## 7. Edge Cases

| Edge Case | Handling Approach |
|---|---|
| Query mixes a factual ask with an advisory ask (e.g., "what's the exit load, and should I sell now?") | Answer the factual part only; explicitly decline the advisory part with the standard refusal + educational link, in the same response |
| Ambiguous scheme reference (e.g., user says "the flexicap fund" without naming the AMC, or confuses similarly named schemes) | Ask a single disambiguating question listing the in-scope scheme names, rather than guessing |
| Retrieved sources conflict (e.g., a cached factsheet vs. a newer one) | Prefer the most recently dated source; if dates are unclear or conflict is unresolved, respond with "unable to confirm from current sources" rather than picking one silently |
| No relevant chunk retrieved (query outside corpus, e.g., a different AMC or scheme not in scope) | Respond that this scheme/AMC isn't in the assistant's current coverage, with a link to the official AMC/AMFI site to look it up directly |
| User pastes PAN, Aadhaar, account number, email, or phone number | Immediately reject with a standard message; do not store, echo, or forward the input downstream |
| User asks for performance/returns ("what were the 5-year returns?") | Refuse computation/comparison; provide a link to the official factsheet only |
| Adversarial prompt attempting to extract advice via reframing ("hypothetically, if you were an advisor...") | Refusal classifier treats reframed advisory intent the same as direct advisory intent — no exception for hypothetical framing |
| Source page structure changes or link breaks (404) | Flagged by the freshness-monitoring job; assistant should not surface a broken citation — falls back to "unable to confirm" until the source registry is updated |
| Non-English or code-mixed query (e.g., Hinglish) | MVP: best-effort intent classification; if confidence is low, ask for clarification in English rather than guessing and risking a wrong factual answer |
| Very short or one-word queries (e.g., "SIP?") | Prompt for the specific scheme name before answering, since minimum SIP is scheme-specific |
| User asks the same factual question repeatedly, seemingly testing consistency | Answer should be deterministic — same query, same scheme, same day should yield the same fact and same citation |

---

## 8. Phases of Implementation

### Phase 0 — Foundations (Corpus & Infra)
- Finalize AMC and scheme scope (SBI Mutual Fund; the 4 named schemes)
- Curate and validate the 15–25 source URL list (factsheets, KIM/SID, FAQ, AMFI/SEBI pages, statement-download guides)
- Stand up ingestion, chunking, and embedding pipeline
- Build the source registry with last-verified timestamps

### Phase 1 — MVP (Facts-Only Prototype)
- Implement core retrieval + citation-constrained answer generation for the 7 core fact categories (expense ratio, exit load, minimum SIP, ELSS lock-in, riskometer, benchmark, statement download)
- Implement query intent classifier and refusal templates (advisory, performance, PII)
- Ship minimal UI (welcome message, 3 example questions, disclaimer, citation rendering)
- Internal dogfooding with the support/content team as first users

### Phase 2 — Hardening & Pilot
- Expand edge-case handling (ambiguous scheme references, conflicting sources, no-match fallback)
- Add feedback capture (thumbs up/down) and weekly human-audit sampling for accuracy
- Limited beta rollout to a small user segment within the Groww app (e.g., a "Fund FAQs" entry point on scheme pages)
- Track support ticket deflection and citation accuracy against MVP targets

### Phase 3 — Scale Within Scope
- Add remaining schemes / a second AMC if Phase 2 metrics hold (citation accuracy, refusal precision, deflection rate)
- Automate corpus freshness monitoring (scheduled re-crawl, broken-link alerts)
- Tighten latency and reliability for full in-app exposure (not just a beta cohort)

### Phase 4 — Broader Rollout (Beyond This Milestone)
- Multi-AMC corpus expansion
- Deeper in-app integration (e.g., surfaced directly on fund detail pages, not just a standalone chat entry point)
- Feed learnings (retrieval quality, refusal edge cases, corpus maintenance overhead) into the next milestone/challenge referenced in the original brief

---

## 9. Go-To-Market Plan

### 9.1 Internal Soft Launch (Support & Content Teams)
Launch first as an internal co-pilot for the support/content team, not directly to end users. This validates factual accuracy and citation quality against real query volume with a forgiving audience, and builds an initial base of human-reviewed Q&A pairs.

### 9.2 Limited User Beta
Introduce a "Fund FAQs" entry point on scheme detail pages for a small, opt-in user segment. Frame it explicitly as facts-only from day one (disclaimer visible before first use) to set correct expectations and avoid users mistaking it for a recommendation tool.

### 9.3 Feedback-Driven Iteration
Use thumbs up/down feedback and weekly accuracy audits from the beta to fix retrieval gaps and refine refusal boundaries before wider exposure. No marketing push until citation accuracy and refusal precision targets are consistently met.

### 9.4 In-App Rollout
Expand the entry point to all users on the in-scope SBI Mutual Fund scheme pages, plus a discoverable link from the general help/support section. Communicate the launch through in-app notification and a short help-center article — not a broad marketing campaign, since scope is intentionally narrow at this stage.

### 9.5 Positioning
Position as **"verified answers, not opinions"** — the differentiator against both generic chat assistants (no grounding) and static FAQ pages (not conversational). Messaging should lean on the citation-first design as the trust hook, not on breadth of capability.

### 9.6 Expansion Trigger
Only after deflection, accuracy, and trust metrics hold at the single-AMC scale should marketing or broader rollout scale up — tied to the AMC/scheme expansion in Phase 3–4, keeping GTM paced to what the corpus and refusal system can actually support reliably.

---

## 10. Open Risks Carried Into Build

- Corpus maintenance overhead (source pages change without notice) is an ongoing operational cost, not a one-time setup task
- Refusal classifier quality is the single biggest compliance-risk lever in this product — false negatives here matter more than any other metric
- Success is bounded by scope discipline: the temptation to add "helpful" performance or comparison features will directly undermine the compliance posture that makes this product viable in the first place
