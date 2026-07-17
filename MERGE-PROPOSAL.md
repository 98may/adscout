# Merge proposal: AdScout × Xiaochen's internal modeling scout

Status: proposal — to be discussed with Xiaochen. Nothing here is committed to.

## Why merge (the one-paragraph pitch)

The two skills are the two halves of one question. Xiaochen's skill scouts
**inside Google**: what sister ads/modeling teams have shipped, designed, or
written up. AdScout scouts **outside**: what Meta/Kuaishou/Pinterest/the AI-era
market are shipping, evidence-graded. Merged, every finding gets the three-way
check that neither skill can do alone:

> external finding → do WE have it? → does a SISTER TEAM have it? → does NOBODY have it?

That upgrades the GAP classification with the cheapest possible next step:
when a sister team already built it, the brief says **"reuse — talk to team X,
here's their doc"** instead of "design an experiment". And it works in
reverse: an internal idea can be checked against the external corpus — *has
the industry already tried this and published results?*

## Merged architecture (minimal change to both)

```
corpus/            # external articles (this repo's crawler keeps it fresh)
corpus_internal/   # sister-team findings (Xiaochen's collector keeps it fresh)
                   # → lives ONLY in google3, never in the external repo
internal_capabilities.yaml   # still the only truth about OUR OWN team
SKILL.md           # one rulebook, one new frontmatter field, one new GAP class
```

- **Frontmatter:** add `origin: external | internal` to every corpus file.
  Internal files reuse the tier idea with internal meanings:
  1 = launched + measured, 2 = approved design doc, 3 = experiment/WIP,
  4 = brainstorm/meeting notes. `company:` becomes the team name; `source_url:`
  the go/ link.
- **GAP comparison gains one class:** `INTERNAL-ELSEWHERE` — a sister team has
  an equivalent. Produces a **reuse brief** (cheapest gap_type: next step is a
  conversation, not a build), citing their doc/code links.
- **Scope rules compose:** our own inventory is still `internal_capabilities.yaml`
  only; sister-team facts come only from `corpus_internal/`; external facts only
  from `corpus/`. Nothing is ever inferred across the boundary.
- **Both update loops keep running unchanged:** AdScout's weekly crawl CL +
  Xiaochen's internal collection cadence. Users still install a thin pointer
  shell once and never update it.

## How to proceed (suggested agenda for the chat with Xiaochen)

1. **Look at her skill's shape** — is it also instructions + a document corpus?
   (If yes, the merge is mostly mechanical — see the prompt below. If her
   knowledge lives in a different form, decide whether to export it into
   frontmattered markdown, which is the only format the merged rulebook needs.)
2. **Agree on the internal frontmatter mapping** — team, tier semantics above,
   go/ links, and who owns backfilling it.
3. **Agree on ownership & cadence** — she owns `corpus_internal/` + its
   collector; you own `corpus/` + crawler + the shared `SKILL.md` rulebook.
4. **Pick the merged name** (candidates: AdScout 360, ScoutNet, or keep
   AdScout with "internal lens") and the canonical google3 path.
5. **Run the merge prompt below in Gemini CLI** inside a directory containing
   both skills, review the diff together, land it internally.
6. **Confidentiality line:** the merged skill and `corpus_internal/` exist only
   in google3. This external repo keeps only the external half — that stays
   true even after the merge.

## The merge prompt (paste into Gemini CLI)

Fill the two `<...>` placeholders, run from an empty working directory.

```text
You are merging two AI-agent skills into one. Work step by step, and do not
invent content for either skill — everything you write must be derived from
the two inputs or from the explicit rules below.

INPUTS
- AdScout (external ads-industry intelligence skill):
  located at <ADSCOUT_ROOT, e.g. ~/.adscout or the google3 path>.
  Key files: SKILL.md (the full rulebook: evidence tiers 1-4, Pipeline A
  structured-extraction → GAP comparison vs internal_capabilities.yaml →
  opportunity briefs; Pipeline B strategic signals for track: ai_era_ads;
  digest mode with a ≥7/10 threshold and a fixed "silence" line; commands
  [newsfeed]/[ai_ads]/[source]; a confidence downgrade rule; a scope rule),
  corpus/ (frontmattered markdown articles), internal_capabilities.yaml,
  sources.yaml, crawl.py, examples/, PORTING.md.
- Xiaochen's internal modeling scout skill:
  located at <XIAOCHEN_SKILL_PATH>. First READ every file in it and produce a
  short written inventory: where its instructions live, where its knowledge
  lives, what format the knowledge is in, and what its update mechanism is.
  Show me this inventory and WAIT for my confirmation before writing anything.

GOAL
One merged skill ("AdScout 360" unless I say otherwise) with:
1. corpus/ (external, unchanged) and corpus_internal/ (Xiaochen's knowledge,
   converted to one markdown file per finding with frontmatter:
   title, source_url (go/ link), team, date, evidence_tier, origin: internal,
   track, full_text). Internal tier semantics: 1=launched+measured,
   2=approved design doc, 3=experiment/WIP, 4=brainstorm notes.
2. One merged SKILL.md rulebook that keeps EVERY existing AdScout rule
   verbatim in spirit, adds `origin: external|internal` handling, and extends
   the GAP comparison with one new class:
   INTERNAL-ELSEWHERE — a sister team has an equivalent (evidence: a
   corpus_internal/ file). It produces a REUSE brief: same schema as an
   opportunity brief, but gap_type: INTERNAL-ELSEWHERE, our_status cites the
   sister team's doc/code links, and suggested_next_step is a concrete
   conversation ("Contact <team> about <capability>, review <go/ link> first").
   Precedence when classifying: HAVE > INTERNAL-ELSEWHERE > PARTIAL > MISSING > N/A.
3. Composed scope rules — never violate any of these:
   - our own team's state comes ONLY from internal_capabilities.yaml;
   - sister-team facts come ONLY from corpus_internal/;
   - external industry facts come ONLY from corpus/;
   - anything else is labeled "not from corpus";
   - never fabricate entries in any of the three.
4. The [newsfeed], [ai_ads], [source] commands extended to cover both corpora
   ([source] shows an origin column; [newsfeed] also lists new internal
   findings if Xiaochen's collector added any).
5. A merged thin pointer shell (10-15 lines) that points at the single
   canonical root — no corpus content inside the shell.
6. examples/: regenerate hard-answer.md by actually running the merged rules
   over both corpora, so at least one brief demonstrates INTERNAL-ELSEWHERE;
   keep the other examples, updating only what the merge invalidates.

CONSTRAINTS
- No vector DB, no RAG framework, no embeddings: both corpora stay small
  enough to load whole into context. Retrieval is "read all files".
- All analysis rules live in SKILL.md as instructions; any code only does
  fetch/filter/dedupe/frontmatter/file IO.
- Do not weaken any anti-fabrication or confidence-cap rule while merging.
- corpus_internal/ content is Google-internal: the merged skill must never be
  synced to any external repo. Add this warning to the merged README.

ACCEPTANCE (verify yourself, show me the results)
- Every file in both corpora parses: frontmatter has all required fields
  including origin; grep finds no file missing evidence_tier, track, or origin.
- Ask the merged skill one question that should trigger INTERNAL-ELSEWHERE and
  confirm the reuse brief cites a real corpus_internal file.
- Ask one question with no relevant source in any corpus and confirm it
  refuses to answer from general knowledge.
- [source] lists both corpora, newest first, with an origin column.
```

## Form-answer implications

`submission-draft.md` has a "Variant B" section with the merged-story answers
(title/description/Q&A) ready if you two decide to submit jointly.
