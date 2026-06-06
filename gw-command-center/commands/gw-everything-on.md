---
description: On-demand corpus search — pull every relevant snippet from across the GW archive on one topic into a single reference doc
---

# /gw-everything-on [topic] — Corpus Mining

Scans Scott's entire GW corpus (briefs, voice notes, X bookmarks, Pocket inbox, screenshots OCR, wiki, NotebookLM master notebooks) for everything relevant to one topic and writes it to a single reference doc. Use it when prepping a Film Study, Substack article, Leech Letter, or any output where the differentiator is weaving in material Scott has already saved.

**This is NOT a daily pipeline.** It runs on demand. Scott invokes when he needs depth on a topic. Output is feedstock for human synthesis, not publish-ready content.

## Examples

- `/gw-everything-on GPS for film study insiders`
- `/gw-everything-on deceleration`
- `/gw-everything-on NIL spend hamstring tech`
- `/gw-everything-on Insiders 90-day onboarding`

## WIKI CONTAMINATION GUARD (HARD RULE)

This skill READS the wiki but NEVER writes to it. Output goes ONLY to `Deliverables\_corpus-queries\`. Promotion of corpus-query insights into the wiki happens manually during Scott's Sunday `/gw-weekly-synthesis` review. Do not break this wall.

## Output target

Write ONE file: `D:\Claude Projects\Gridiron Warrior\Deliverables\_corpus-queries\YYYY-MM-DD-[topic-slug].md`

Slug rules: kebab-case the topic, truncate to 40 chars, no special chars. "GPS for film study insiders" → `gps-for-film-study-insiders`.

If the file already exists for today on the same topic, append a `-2` suffix (or `-3`, etc) — never overwrite a prior run on the same day.

## Steps

### 1. Expand the topic into a query set

Take Scott's topic argument and generate 3-7 search terms covering synonyms, related concepts, and brand-specific vocabulary. Examples:

- Topic `GPS` → `["GPS", "satellite tracking", "load monitoring", "wearable", "Catapult", "Polar", "Plyomat", "velocity"]`
- Topic `deceleration` → `["deceleration", "force absorption", "braking", "eccentric", "landing mechanics", "stopping"]`
- Topic `Insiders onboarding` → `["onboarding", "first 90 days", "retention", "quick win", "new member", "Insiders welcome"]`

Use Scott's voice vocabulary when expanding (his wiki has terms like "violence is a skill", "stimulate not annihilate", "August is coming" — these matter).

### 2. Scan sources in this order

For each source, glob the directory then grep for any of the query terms (case-insensitive, multiline mode where useful). Read matching files. Skip files larger than 50KB unless they contain a direct keyword match — in those, grep for the matches and pull surrounding context (3-5 lines on each side) rather than reading the whole file.

| # | Source | Path | Notes |
|---|---|---|---|
| 1 | AI briefs | `External Library\AI\*.md` | Daily AI research briefs |
| 2 | Business briefs | `External Library\BusinessDocuments\*.md` | Daily Business briefs |
| 3 | S&C briefs | `External Library\S-and-C\*.md` | Daily S&C briefs + the 7 migrated NotebookLM deep-dives |
| 4 | Dewey saves | `External Library\Twitter-Instagram Saves\_by-domain\` | S&C, Business, AI subfolders |
| 5 | Screenshots OCR | `External Library\Screenshots\processed\` | OCR'd content |
| 6 | Voice notes | `Voice Corpus\Voice Notes\` and `Voice Corpus\_pocket-inbox\.processed\` | Transcripts |
| 7 | Daily seeds | `Deliverables\_daily-seeds\*.md` | Past content angles |
| 8 | Wiki | `wiki\` | Scott's IP — concepts, summaries, quotes, frameworks |
| 9 | NotebookLM master notebooks | via `mcp__notebooklm__*` | Query the topic-relevant master notebook (e.g. "S&C Master Resource" for S&C-flavored topics). Use `mcp__notebooklm__notebook_list` to find candidates, then `mcp__notebooklm__notebook_query` against the most-relevant one. Optional — skip if no obvious match. |

### 3. Read budget guidance

**No hard cap, but be efficient:**
- Aim to finish in under 10 minutes wall-clock.
- Default depth: read top 30-50 highest-signal matches.
- For each source, if you've already pulled 8-10 relevant excerpts, move on — diminishing returns.
- Quote excerpts liberally but tag every quote with its source file path so Scott can trace.

### 4. Synthesize themes BEFORE listing extracts

Before dumping source-by-source quotes, write a short synthesis section that identifies 3-5 themes Claude saw across the corpus. This is the highest-leverage part of the doc — it's what makes corpus mining different from a grep dump. Themes should be coach-direct phrases ("the AD math nobody wants to do") not generic ("financial considerations").

### 5. Write the brief in this structure

```markdown
---
title: "Everything on [topic] — Corpus Query"
type: corpus-query
topic: "[original topic argument]"
topic_slug: [topic-slug]
date: YYYY-MM-DD
query_terms: [list of expanded search terms]
sources_scanned: [list of source dirs hit]
match_count: N
pipeline: gw-everything-on
---

# Everything on [Topic]

**Query:** [original topic argument]
**Expanded terms:** [comma-separated]
**Date:** YYYY-MM-DD

## Themes

3-5 short headed paragraphs. Each theme = one observation Claude formed across multiple sources. Lead with the insight, then list 2-4 source citations as inline references.

### Theme 1 — [short, coach-direct phrase]
[1-3 sentences of synthesis.] (Sources: `path/file.md`, `path/other.md`)

### Theme 2 — ...

## By Source

### Briefs (AI / Business / S&C)
For each matching brief, quote the relevant 1-3 paragraphs with the source path as a header.

#### `External Library\S-and-C\2026-04-30-weight-room-culture-brief.md`
> [excerpt]

### Voice Notes
For each matching transcript, quote the relevant passage.

#### `Voice Corpus\Voice Notes\2026-05-17-kevin-norbord-force-plate-pitch.md`
> [excerpt]

### Dewey Saves (X / Instagram)
Quote the post + the author + the date.

### Screenshots
Quote the OCR'd content.

### Daily Seeds
Quote the relevant angle blocks.

### Wiki
Quote the relevant concept pages or framework summaries.

### NotebookLM Master Notebook (if queried)
Summarize what the notebook returned.

## Suggested Next Moves

3-5 bullets. Concrete content angles or production moves this corpus suggests:
- "Film Study angle: ..."
- "Leech Letter hook: ..."
- "Insiders post: ..."
- "Substack article spine: ..."

## Footer

- Total matches: N
- Sources with hits: A / B / C / ...
- Sources empty: D / E
- Time spent: X minutes wall-clock
```

### 6. Empty result handling

If after scanning all sources there are zero or near-zero matches:

- Still write the file at the standard path.
- Frontmatter `match_count: 0`.
- Body: "No substantive material found for [topic] across the GW corpus. Sources scanned: [list]. Suggest broadening the topic to [2-3 related terms] or kicking off a `/gw-research [topic]` or `/gw-sc-research` run to build coverage."
- Do NOT fabricate excerpts.

### 7. Append to wiki log

```
YYYY-MM-DD /gw-everything-on: [topic-slug] (N matches across M sources)
```

### 8. Commit

```bash
cd "D:\Claude Projects\Gridiron Warrior" && git add "Deliverables/_corpus-queries/" "wiki/log.md" && git commit -m "corpus: query YYYY-MM-DD ([topic-slug], N matches)"
```

## Voice and tone (for the synthesis sections)

- Coach-direct. Short sentences. Plain language.
- No em-dashes. No banned words (see CLAUDE.md).
- This is a research brief Scott will mine — clarity over polish.
- Quote excerpts verbatim. Do NOT paraphrase or "clean up" voice note transcripts — preserve the raw register.

## Integration with other skills (3-tier policy)

Other skills decide whether to pull from this skill's output before generating their own content:

| Tier | Default | Skills | Behavior |
|---|---|---|---|
| 1 — Always pull corpus | ON | `gw-film-study-pipeline` | Film Studies invoke `/gw-everything-on [topic]` before any content production. Output becomes the research feedstock. |
| 2 — Opt-in flag | OFF (Scott or skill toggles) | `gw-substack-forge`, `gw-content-forge` (content pack mode) | Long-form content can pull corpus when topic depth matters. |
| 3 — Never pull | OFF (no flag) | `leech-letter-editor`, `ig-carousel`, `gw-content-forge` (transcript mode) | Voice purity / speed beats corpus depth. |

**Principle:** Corpus pull adds depth and cross-reference. It costs voice purity and speed. Use where depth is the product. Skip where voice (Letters) or speed (daily tweets, carousels) is the product. This is ALSO a wiki-contamination guard — without tiering, external research bleeds into every output published under Scott's name.

## Notes

- **Idempotent within a day**: re-running on the same topic same day appends `-2`, `-3` rather than overwriting.
- **Output is feedstock, not publishable**: never present this as polished content. It's a research brief for Scott to mine.
- **Master notebook queries are conditional**: only run if topic-relevance is obvious. Don't burn NotebookLM auth on a query that local files already answered.
- **Path tracing matters**: every excerpt needs its source file path. Scott traces back to context constantly.
