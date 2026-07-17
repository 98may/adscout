# AC BuildAI Hackathon — submission draft (AdScout)

> Reference for filling the form yourself. `[FILL]` = only you know it.
> Form: https://docs.google.com/forms/d/e/1FAIpQLSddPd90sE33AmqBEtWlovuN0vm4oCYCBp-ATLsw2FwQB-nrog/viewform

---

**1. Email** *(required)*
`[FILL — your corp email]`

**2. Theme** *(required, single choice)*
**Transform Internal Workflows** ← pick this one.
(If asked in Q&A why not AI Surface Monetization: "Transform Internal Workflows is its body, AI Surface Monetization is its eyes — the `ai_era_ads` track watches how AI surfaces sell ads, but the product itself transforms how a modeling team does competitive intelligence.")

**3. Link to the 3-minute video** *(optional)*
`[FILL — record + upload, then paste link]`
Suggested structure (matches the form's "1 min overview + 2 min demo"):
- 0:00–1:00 overview: the problem (2 companies still blog, Chinese sources scattered, speculation sold as fact, AI era rewriting the industry) + the three design decisions (evidence tiers / silence below threshold / dual-track)
- 1:00–1:10 `[source]` — one table: 22 articles, 2 languages, 4 self-updating feeds
- 1:10–1:50 hard answer — *"What have Meta and Kuaishou shipped recently on RL/generative models in ads ranking, and what applies to our auction?"* → 3 briefs, tier badges, a Chinese source, go/-linked next steps
- 1:50–2:20 `[ai_ads]` — the theme moment: Meta's models improve themselves end-to-end; on the open web most "viewers" are no longer human (bots 57.4%); ChatGPT ads went $60 CPM → CPC in ten weeks
- 2:20–3:00 `[newsfeed]` — live crawl on stage; new articles land **already briefed against our capability inventory**. Closer line: *"You didn't read the article. You got the gap analysis. And if nothing matters this week, it says so — silence below threshold is a feature, not a failure."*

**4. Link to the presentation slide** *(optional)*
`[FILL — use their template, share with judges' email]`
Slide skeleton if useful: 1) problem, 2) what AdScout is (architecture ASCII from README), 3) evidence tiers + GAP comparison (one real brief as the visual), 4) demo, 5) distribution & vision (google3 port, digest webhook, per-team inventory slices).

**5. Prototype Title** *(required, short & catchy)*
Primary suggestion:
> **AdScout: your ads-industry radar — graded evidence, gap-aware briefs, pings only when it matters**

Shorter alternatives:
- "AdScout — competitive intelligence for ads teams, as a skill"
- "AdScout: reads the ads industry so your team doesn't have to"

**6. Prototype Description** *(required, 2–3 sentences)*
> AdScout is an ads-intelligence skill that monitors external sources (engineering blogs, papers, industry news — English and Chinese), grades every finding by evidence tier, and compares it against a team-owned capability inventory to produce only two high-signal outputs: opportunity briefs for modeling gaps and strategic signals for AI-era industry shifts. A weekly crawler keeps the corpus fresh with zero user maintenance — teammates install the skill once and every question or digest reflects the latest articles; if nothing clears the relevance threshold, it says so instead of padding. It turns competitive intelligence from ad-hoc link-sharing into a graded, gap-aware, auto-updating workflow.

**7. Team Lead ldap(s)** *(required, max 2)*
`[FILL]`

**8. Team Member ldap(s)** *(required, max 8 incl. leads)*
`[FILL]`

**9. PAG(s)** *(required, single choice)*
`[FILL — your PAG; options: ACEs / APaS / AViD & YT Ads / BAM / CE / Consumer / Merchant / Payments / SAGE / Other]`

**10. Live Q&A POC** *(required, one ldap)*
`[FILL]`

**11. Will you be joining live on GVC?** *(required)*
`[FILL — Yes/No]`

**12. Primary Team Location** *(required)*
`[FILL]`

---

## Variant B — if merged with Xiaochen's internal modeling scout

Use these instead of Q5/Q6 if you two decide to submit jointly (see
`MERGE-PROPOSAL.md` for the merge plan; discussion pending — not committed).

**5B. Prototype Title**
> **AdScout 360: every modeling idea checked three ways — do we have it, does a sister team have it, does anybody?**

Alternatives: "AdScout 360 — inside-and-outside intelligence for ads modeling teams"; "ScoutNet: one radar for the industry and the org".

**6B. Prototype Description**
> AdScout 360 merges two scouts into one skill: an external radar that crawls industry sources (Meta/Kuaishou/Pinterest engineering blogs, papers, AI-era ads news — English and Chinese, evidence-graded tier 1–4) and an internal radar over sister ads teams' launched systems and design docs. Every finding gets a three-way gap check — our team's inventory, sister teams' work, the outside world — so the output is the cheapest true next step: reuse a sister team's system (with the go/ link), close a real gap, or skip what everyone already has. Both corpora update automatically (weekly crawl CL + internal collection); teammates install a pointer skill once and never maintain anything.

**Extra Q&A ammo for the merged story:**
- **"What's genuinely new vs two separate skills?"** — The `INTERNAL-ELSEWHERE` class: an external finding that a sister team already built produces a *reuse brief* ("talk to team X, review go/... first") instead of a build proposal. Neither skill can produce that alone, and reuse is the cheapest action a brief can recommend.
- **"Does the external repo see internal data?"** — No. `corpus_internal/` and the merged skill live only in google3; the external repo keeps only the external half.
- Team fields (Q7/Q8/Q10) gain Xiaochen's ldap; everything else unchanged.

## Likely Q&A ammo (from the build)

- **"Why no RAG/vector DB?"** — The corpus is ~20 markdown files; it fits in one model context. Retrieval is "load all files". Zero infra, zero staleness, and the evidence-tier frontmatter does more for answer quality than embeddings would.
- **"How do users stay current without updating anything?"** — The skill ships without the corpus; it's a pointer, not a package. Internally the pointer is a google3 path: the weekly crawler lands a CL, everyone reads head. Install once, never update.
- **"How do you stop it from hallucinating our internal state?"** — `internal_capabilities.yaml` is the only source of truth about us; anything not in it = "no information in inventory". Capabilities carry go/doc and code links, so briefs point at the exact doc to review.
- **"What breaks if a fetch fails?"** — Nothing: the crawler degrades to storing the summary with `full_text: pending` and always exits 0. The AppLovin paywall article in the corpus is the live example — and it doubles as the confidence-downgrade demo.
- **Numbers to quote:** 22 articles in corpus (15 curated seeds + 7 the crawler found itself in week one), 4 source feeds, 2 languages, evidence tiers 1–4, built end-to-end in ~3 hours.
