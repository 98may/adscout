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
             corpus/*.md  ◄── weekly GitHub Action auto-commit
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

**Use it as a skill:** clone this repo, open Claude Code inside it, and invoke `/adscout` — the project skill in `.claude/skills/adscout/` loads `SKILL.md` + `corpus/` + `internal_capabilities.yaml` and answers through the pipelines. The corpus *is* the knowledge: when the crawler adds a file, the very next question can cite it. No re-indexing, no re-configuration.

## Subscribe & distribute

**The skill ships without the corpus — it's a pointer, not a package.** The thin shell in `.claude/skills/adscout/` carries no knowledge; it resolves the repo (env var → cwd → `~/.adscout` clone/pull) at every invocation, so users install once and always get the latest corpus. Porting the same pattern to an internal monorepo or Gemini: see [PORTING.md](PORTING.md).

- **Today:** watch this repo — the GitHub Action crawls every Monday 08:00 UTC and auto-commits new articles.
- **Next sprint:** the commented-out webhook step in `.github/workflows/crawl.yml` pushes threshold-passing digests to a chat channel — subscribers get pinged **only when something matters**.
- **Later:** each team maintains its own `internal_capabilities.yaml` slice; opportunity briefs convert to experiment proposals one-click.

## Demo script (4 scenes)

1. **Hard answer** — `/adscout What have Meta and Kuaishou shipped recently on RL/generative models in ads ranking, and what applies to our auction?` → 3 briefs, tier badges, cross-language sources, verb-first next steps. (See `examples/hard-answer.md`.)
2. **Confidence downgrade** — `/adscout What modeling techniques does AppLovin Axon use?` → "No first-party sources available", tier-4 only, confidence capped at low. The skill refusing to bluff *is* the feature. (See `examples/low-confidence.md`.)
3. **Strategic signal** — `/adscout What does the ChatGPT ads pricing evolution tell us?` → "no industry consensus on pricing single-slot AI answers". Transform Internal Workflows is its body, AI Surface Monetization is its eyes. (See `examples/strategic-signal.md`.)
4. **Live ingest** — `python crawl.py --url <fresh article> --tier 2 --lang en --track modeling` (3 seconds), then immediately `/adscout` a question about the new article. Show the green weekly-crawl runs in the Actions tab as the standing subscription layer.

## Vision & theme mapping

- **Primary — Transform Internal Workflows:** competitive intelligence for a modeling team goes from ad-hoc link-sharing to a graded, gap-aware, auto-updating pipeline.
- **Secondary — AI Surface Monetization:** the `ai_era_ads` track watches how AI surfaces (ChatGPT ads, agent traffic) rewrite advertising economics — the strategic radar for any team monetizing an AI surface.
- **Roadmap sources:** WeChat official accounts (richest Chinese channel; no API — today handled via manual `--url` ingest of writeups), X/LinkedIn analyst commentary (API-restricted).

---

*`internal_capabilities.yaml` is fictional demo data. Nothing in this repo contains real internal information.*
