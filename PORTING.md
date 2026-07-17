# Porting AdScout to an internal repo (google3) / Gemini

AdScout's design rule for distribution: **the skill ships without the corpus —
it's a pointer, not a package.** A skill that bundles the corpus is a snapshot
that goes stale on day one. The skill is a thin instruction shell pointing at
one canonical corpus location; whatever keeps that location fresh (GitHub
Action, internal cron job) is the whole update story. Users install once and
never touch it again.

## What to copy (the portable core — no platform bindings anywhere)

| File | Role |
|---|---|
| `SKILL.md` | All analysis rules. Pure markdown instructions — model- and tool-agnostic. |
| `corpus/` | The knowledge. One markdown file per article, frontmatter-tagged. |
| `internal_capabilities.yaml` | Capability inventory for GAP comparison. |
| `sources.yaml` | Source registry for the crawler. |
| `crawl.py` | Fetch/filter/dedupe/file-IO only (deps: feedparser, requests, beautifulsoup4, pyyaml). |
| `examples/` | Worked examples — useful as few-shot references and for onboarding. |

Do NOT copy `.claude/` (Claude Code-specific shell) or `.github/` (GitHub
Actions) — those are per-platform delivery mechanisms you replace below.

## The thin shell template (~10 lines, adapt per platform)

```
You are AdScout, an ads intelligence analyst.

The AdScout corpus root is: <CORPUS_ROOT>

On every invocation:
1. Load <CORPUS_ROOT>/SKILL.md — it contains ALL analysis rules; follow it exactly.
2. Load every file in <CORPUS_ROOT>/corpus/ and <CORPUS_ROOT>/internal_capabilities.yaml.
3. Answer through the pipelines defined in SKILL.md (modeling briefs,
   ai_era_ads strategic signals, digest mode, confidence downgrade, scope rule).
```

- **google3:** replace `<CORPUS_ROOT>` with the absolute monorepo path (e.g.
  `//experimental/<your-team>/adscout`). **Delete any pull/clone logic** — in a
  monorepo everyone reads head, so freshness is automatic the moment the
  weekly crawler CL lands. Register this shell text wherever your team keeps
  Gemini skills (GEMINI.md, extension context, or the internal skill registry).
- **Gemini CLI (external):** the same text works as a `GEMINI.md` /extension
  context file; keep a `git pull` step if the corpus lives in a git clone.
- **Claude Code (external):** already implemented in
  `.claude/skills/adscout/SKILL.md` (env var → cwd repo → `~/.adscout`
  clone/pull, never blocks on sync failure).

## Update mechanics, side by side

| | GitHub world (this repo) | google3 world |
|---|---|---|
| Corpus production | Action, Mondays 08:00 UTC, auto-commit | scheduled job runs `crawl.py`, submits a CL |
| User freshness | thin shell runs `git pull` at invocation | free — everyone reads head |
| Skill updates | symlink/clone follows the repo | shell text rarely changes; rules SKILL.md updates land as CLs |

`crawl.py`'s discovery layer (RSS/arXiv fetching) may need rewriting against
internal fetch/egress infrastructure; the processing contract (frontmatter
schema, dedupe by source_url, degrade-to-pending, exit 0 always) is the part
to preserve. All analysis logic is in SKILL.md, which needs zero changes.

## The inventory caveat

Everything in `corpus/` is public articles, and `internal_capabilities.yaml`
here is **fictional demo data**. Once inside google3, teams should maintain
their own real inventory slice — at that point the file contains real internal
information and must live only in the internal repo. Never sync it back to
GitHub.
