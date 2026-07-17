# AdScout

**AdScout: tracks what other ads teams are shipping and how the AI era is rewriting advertising — grades the evidence, and pings you only when it matters.**

## The problem

- English first-party ads-modeling sources are down to **~2 companies** that still publish real engineering detail (Meta, Pinterest).
- Chinese sources are rich but scattered across papers and WeChat writeups.
- Between them sits a thick layer of **speculation-sold-as-fact** marketing content.
- Meanwhile the AI era is restructuring the industry itself: agent traffic passed **57% of HTTP requests**, and AI surfaces are selling ads with **no settled pricing model** ($60 CPM → CPC within ten weeks on ChatGPT).

Keeping up is a part-time job nobody has. AdScout does it as a skill.

## Three design decisions

1. **Evidence tiers** — every source is graded 1–4 (paper / eng blog / press / speculation). Know the source's motive before you trust its numbers. Tier 3–4 findings can never carry high confidence.
2. **Event-driven, not calendar-driven** — digests include only items scoring ≥7/10. If nothing clears the bar, the output is *"No items met the threshold this period. Silence below threshold is a feature, not a failure."* Anti AI-slop by construction.
3. **Cross-language + dual-track** — Chinese and English sources feed two pipelines: **opportunity briefs** (modeling findings vs our capability inventory) and **strategic signals** (AI-era industry shifts). Transform Internal Workflows is its body; AI Surface Monetization is its eyes.

## Architecture

```
   RSS / arXiv API / --url manual ingest          (discovery: reliable)
                  │
                  ▼
             crawl.py ── full-text fetch          (best effort; degrades to
                  │                                full_text: pending, never fails)
                  ▼
             corpus/*.md  ◄── weekly crawl job auto-commit
                              (GitHub Action here; a scheduled CL job in google3)
   (frontmatter: tier, track, lang, company)
                  │
                  ▼            internal_capabilities.yaml
             SKILL.md  ◄──────  (sanitized inventory — the ONLY
                  │              source of truth about us)
      ┌───────────┴───────────┐
      ▼                       ▼
 Pipeline A: modeling    Pipeline B: ai_era_ads
 extract → GAP compare   strategic intelligence
 → opportunity briefs    → strategic signals
      └───────────┬───────────┘
                  ▼
        digest mode (≥7/10 only)
```

No vector DB, no RAG framework, no backend: ~15 markdown files fit in a single LLM context, so retrieval is "load all files". Every processing rule lives in `SKILL.md` as instructions; Python only fetches, filters, dedupes, and writes frontmatter.

## How to run

```bash
pip install -r requirements.txt

# crawl all sources in sources.yaml (idempotent, safe to re-run, never hard-fails)
python crawl.py

# ingest one article on the spot (the live-demo path)
python crawl.py --url <URL> --tier 2 --lang en --track modeling
```

**Use it as a skill (Google / Gemini — the target users):** follow [PORTING.md](PORTING.md) — copy the portable core into a google3 path, register the ~10-line thin shell wherever your team keeps Gemini skills, and point it at that path. Freshness is automatic: the weekly crawler CL lands, everyone reads head, the very next question can cite the new article. No re-indexing, no re-configuration, no skill updates ever.

This GitHub repo is the external dev/demo copy; it carries an equivalent thin shell for Claude Code (`.claude/skills/adscout/`) so the demo runs anywhere. The corpus *is* the knowledge in both worlds.

## Subscribe & distribute

**The skill ships without the corpus — it's a pointer, not a package.** The thin shell carries no knowledge; it reads the canonical corpus location at every invocation, so users install once and always get the latest corpus (in google3: reading head *is* the update mechanism; in this external copy: the shell does a best-effort `git pull`). See [PORTING.md](PORTING.md).

- **Today:** the weekly crawl job (Mondays 08:00 UTC — GitHub Action here, a scheduled CL job internally) auto-commits new articles; anyone with the skill installed asks "generate digest" and gets the latest week.
- **Next sprint:** the crawl job additionally pushes threshold-passing digests to a chat channel (see the commented-out webhook step in `.github/workflows/crawl.yml`) — subscribers get pinged **only when something matters**, no skill required.
- **Later:** each team maintains its own real `internal_capabilities.yaml` slice with `doc:`/`code:` links; opportunity briefs convert to experiment proposals one-click.

## Commands

| Command | What it does |
|---|---|
| `[newsfeed]` | Pulls fresh articles via the crawler, then briefs what matters: headline list of new items (newest first) + auto-generated opportunity briefs / strategic signals for anything scoring ≥7. |
| `[ai_ads]` | AI-era spotlight: two-chapter briefing — *AI rewriting how ads teams work* (Meta's self-improving REA/GEM pipeline) and *AI rewriting the ad market* (bots at 57.4% of requests, ChatGPT's $60 CPM → CPC price discovery). |
| `[source]` | The whole corpus, newest first: `date \| tier \| track \| company \| title \| full_text`, plus the feed registry and any pending re-fetch candidates. |

## Demo script (4 scenes, ~2 minutes)

1. **`[source]`** *(10 seconds)* — one table: 22 articles, 2 languages, 4 feeds, tier badges. "This corpus updates itself weekly; nobody maintains it."
2. **Hard answer** — ask: *"What have Meta and Kuaishou shipped recently on RL/generative models in ads ranking, and what applies to our auction?"* → 3 briefs with tier badges, a Chinese-language source, and next steps that point at go/-linked docs. (See `examples/hard-answer.md`.)
3. **`[ai_ads]`** — the theme moment: Meta's ads models now improve themselves end-to-end, while on the open web the majority of "viewers" are no longer human. Transform Internal Workflows is its body, AI Surface Monetization is its eyes.
4. **`[newsfeed]`** — the closer: live crawl on stage, new articles appear with scores, qualifying ones arrive **already briefed against our capability inventory**. "You didn't read the article. You got the gap analysis."

**Q&A pocket demos:** hallucination question → ask *"What modeling techniques does AppLovin Axon use?"* → "No first-party sources available", confidence capped at low — the skill refusing to bluff *is* the feature (`examples/low-confidence.md`). Reliability question → point at the AppLovin paywall article gracefully stored as `full_text: pending`, and the green weekly-crawl runs.

## Vision & theme mapping

- **Primary — Transform Internal Workflows:** competitive intelligence for a modeling team goes from ad-hoc link-sharing to a graded, gap-aware, auto-updating pipeline.
- **Secondary — AI Surface Monetization:** the `ai_era_ads` track watches how AI surfaces (ChatGPT ads, agent traffic) rewrite advertising economics — the strategic radar for any team monetizing an AI surface.
- **Roadmap sources:** WeChat official accounts (richest Chinese channel; no API — today handled via manual `--url` ingest of writeups), X/LinkedIn analyst commentary (API-restricted).

---

*`internal_capabilities.yaml` is fictional demo data. Nothing in this repo contains real internal information.*
