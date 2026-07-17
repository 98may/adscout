# AdScout: your ads-industry radar

**Author:** Ayan Mao · **Date:** Jul 16, 2026 · **Self link:** go/adscout · **Repo:** `[FILL — repo link]`

> **AdScout — watches every ads blog, so your team doesn't have to.**

---

## Three questions first

1. **Did you know the industry already runs end-to-end, self-tuning ads model pipelines?**
   Meta's REA autonomously drives the whole experiment loop — generates hypotheses, launches training, debugs failures, iterates. Claimed 2× model accuracy and 5× engineering output *(claimed by Meta, tier-2 eng blog, Mar 2026)*.

2. **Did you know most web traffic is no longer human?**
   57.4% of HTTP requests are now bot/agent-initiated (Cloudflare, Jun 2026). "Bots don't click on ads" — impression-based value chains are eroding under our feet.

3. **Did you know ChatGPT ads went from $60 CPM to CPC bidding in ten weeks — and now shows ads in ~50% of US responses?**
   Nobody, including OpenAI, knows how to price a single-slot AI answer yet. Price discovery is happening live, in production.

If you knew all three — you spend serious time reading. If not: **that reading is a part-time job nobody on the team has. AdScout does it as a skill.** Each answer above is one query, with sources and evidence grades attached.

---

## What it is

An ads-intelligence skill: a weekly crawler ingests external sources (Meta / Kuaishou / Pinterest / ByteDance eng blogs, papers, AI-era ads news — English **and** Chinese), grades every article by **evidence tier** (1 = paper → 4 = speculation), and answers questions by comparing findings against **our own capability inventory** — producing opportunity briefs for real gaps, strategic signals for industry shifts, and *silence* when nothing clears the bar.

## How it works

```
RSS / arXiv / manual URL → crawl.py → corpus/ (markdown + evidence tiers)
                                          │  weekly auto-update, zero maintenance
        your question ──► thin skill (a pointer, ~15 lines) ──► reads corpus fresh
                                          │
                          gap check vs internal_capabilities.yaml
                                          ▼
                     briefs / signals / digest — only what scores ≥7/10
```

- **Install once, never update:** the skill ships without the corpus — it's a pointer, not a package. The crawler updates the corpus; every question reads the latest.
- **Anti-hallucination by construction:** answers only from corpus + inventory; tier 3–4 sources cap confidence; no first-party source → it says so instead of bluffing.
- **Anti-noise by construction:** below-threshold weeks return *"Silence below threshold is a feature, not a failure."*

## Usage examples

| Command | What you get | |
|---|---|---|
| `[ai_ads]` | AI-era spotlight: how AI is rewriting ads teams' work and the ad market itself | `[FILL — screenshot 11:18:57]` |
| `[source]` | Whole corpus, newest first, tier/track badges | `[FILL — screenshot 11:31:24]` |
| `[newsfeed]` | Live crawl → new articles arrive **already gap-analyzed** | `[FILL — screenshot]` |
| free-form Q | e.g. *"What have Meta and Kuaishou shipped on RL in ads ranking, and what applies to us?"* → 3 briefs with next steps | `[FILL — screenshot]` |

## TODO / next

- **Subscribe:** push threshold-passing digests to a group chat / email (webhook step already stubbed) — get pinged only when something matters, no skill install needed.
- **Team-owned inventory:** each team maintains its own `internal_capabilities.yaml` slice with go/ + code links; briefs then point at the exact doc to review.
- **Optimize the merged use case** (below).

## If merged with Xiaochen Yang's internal-docs skill → **AdScout 360**

*Every modeling idea checked three ways:*

1. **Do we have it?** (our inventory)
2. **Does a sister team have it?** (her internal corpus → the brief becomes *"reuse — talk to team X, here's their go/ link"*, the cheapest possible next step)
3. **Does anybody in the industry?** (AdScout's external corpus)

Neither skill can do the three-way check alone. Merge plan + a ready-to-run merge prompt: `MERGE-PROPOSAL.md` in the repo.

---

*All corpus content is public articles; the demo inventory is fictional. Internal slices live only internally.*
