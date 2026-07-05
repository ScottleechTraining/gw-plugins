---
name: gw-weekly-synthesis
model: opus
description: "Sunday synthesis - promote best vault material to wiki concepts, write weekly themes"
---

# /gw-weekly-synthesis — Sunday Weekly Synthesis Pass

Fires every Sunday. Reviews the week's vault deltas. Promotes the best material into wiki concept pages. Writes a themes-of-the-week summary.

## Hard guard

This skill's only write surface is `Gridiron Warrior/wiki/`. Check that path for dirt — not the whole tree. Scott routinely has unrelated WIP edits in the repo (scripts, config, drafts), and those should not block the weekly synthesis from updating the wiki.

Before reading or writing anything, run:

```bash
git -C "D:\Claude Projects" status --porcelain -- "Gridiron Warrior/wiki/"
```

If the output is not empty, STOP. Do not edit files. Do not stage files. Do not commit. Report:

```text
Weekly synthesis blocked because the wiki/ tree is already dirty.
Dirty paths under Gridiron Warrior/wiki/:
<paste the scoped git status --short output>

Next action: clean or commit the wiki/ changes, then rerun /gw-weekly-synthesis.
(Unrelated dirt elsewhere in the repo is fine — this check is scoped to wiki only.)
```

This command is allowed to update the wiki only from a clean wiki/ starting point.
Raw `git commit` is forbidden inside this command.

## Steps

### 1. Pull week's deltas

```bash
cd "D:\Claude Projects\Gridiron Warrior" && git log --since="7 days ago" --name-only --pretty=format: | sort -u
```

Filter to new content (Dewey notes, screenshots, voice notes, research briefs, daily seeds).

### Promotion criteria (the bar for ANY vault → wiki concept promotion)

These rules govern every promotion step below (Dewey saves, briefs, voice notes). A concept page is expensive to unwind, promotion is reversible only with git archaeology, so the bar is high and the default is "don't."

A vault item earns a wiki concept page ONLY when all of these hold:

1. **Provenance is clean.** It is either Scott's own teaching, OR external material with `external_origin: true` frontmatter AND the `Origin:` + `How Scott uses this in GW:` blocks per the vault schema in `Gridiron Warrior/CLAUDE.md`. External content with no attribution header does NOT promote, it stays in External Library. This is the contamination guardrail; do not launder someone else's framework into Scott's voice.
2. **It has weight.** It appeared in 2+ independent sources or sessions this week (a real pattern, not a one-off save), OR it is load-bearing for a current live offer (Insiders, Schools funnel, Summit, a course). One brief or one Dewey save alone is not enough, that is the rule Step 3 already encodes for briefs, and it holds for every source type.
3. **It is not a duplicate.** Search the wiki first (`wiki/index.md` plus the resolver in Step 4b). If a concept page already covers this, EXTEND that page, do not spawn a near-duplicate. A wiki with two pages on the same idea is worse than one tight page.

**Default when in doubt: leave it in the vault and note it as a candidate** in the Step 5 report ("candidate for promotion, needs a second source"). Under-promote. A missed promotion costs one line in next Sunday's report; a bad promotion costs git archaeology to undo. When the case for a page is anything short of clear, it does not get a page this week.

### 2. Score and rank Dewey saves

For each new Dewey note in the week:
- Score 1-10 on: clarity of teaching, originality, applicability to GW ICP, voice fit, completeness
- Top 5 of the week get promoted to proper wiki concept pages (in the right domain folder)
- Others stay in External Library as references

### 3. Weave research briefs into concept pages

For each new research brief (business, AI, S&C), check if a concept page already exists in the relevant wiki domain folder.

**If yes** → append (or extend) a `## Recent research` section with key findings + wikilink to the brief. Log as `Brief had matching concept → updated wiki/<domain>/<slug>.md` for the Step 5 summary.

**If no** → **do not create a wiki page.** Wiki pages are reserved for concepts with real synthesized content; one brief alone doesn't justify a page. Instead, requeue the topic so it can mature with more briefs:

- Read the brief's frontmatter. Topic slug comes from `topic:`. Topic name comes from `title:` with the trailing ` — Business Research Brief` / ` — AI Research Brief` / ` — S&C Research Brief` suffix stripped.
- Build the line: `- <topic name> [<topic-slug>]`
- Route by brief domain:
  - `business` → append under `## Active Queue` in `External Library\BusinessDocuments\_topic-queue.md`
  - `ai` → append under `## Active Queue` in `External Library\AI\_topic-queue.md`
  - `s&c` → no queue exists; skip the append (log only)
- **Idempotency:** before appending, grep both the `## Active Queue` and `## Completed` sections of the target queue file for `[<topic-slug>]`. If the slug is already present in either, skip the append — synthesis re-runs shouldn't duplicate. Log as `Brief already queued → no-op`.
- Otherwise log as `Brief had no matching concept → queued [<topic-slug>] in <domain>/_topic-queue.md`.

These routing decisions all feed Step 5's summary.

### 4. Promote voice notes into the graph

Voice notes are Scott-original content — highest-signal source in the vault. Every voice note must enter the wiki concept graph. Two paths: link to existing concept pages, or stub new ones.

For each new voice note from the past 7 days at `Voice Corpus\Voice Notes\YYYY-MM-DD-*.md`:

**4a. Parse `## Concepts mentioned` section.** Extract every `[[Concept]]` wikilink target (the text inside the brackets, before any `|` alias or `—` gloss).

**4b. For each concept, resolve its wiki page** using a multi-strategy resolver. Slug = lowercase concept name with spaces → hyphens. (e.g. `[[Weekly Film Study]]` → `weekly-film-study`.) Try in order, stop at first hit:

1. **Exact slug match** in `wiki\concepts\`, `wiki\business\`, `wiki\ai\`, `wiki\entities\` (in that order).
2. **`gw-` prefix match** in `wiki\entities\` (covers `[[Insiders]]` → `gw-insiders.md`, `[[Podcast]]` → `gw-podcast.md`).
3. **Frontmatter title match** — grep all wiki .md files for `title: "<exact concept name>"` (case-insensitive). This is the strongest signal when names diverge from filenames.
4. **Substring match on filename** across all four domain folders. Try the full slug first, then progressively drop the leading word and try again (e.g. `weekly-film-study` → also try `film-study` → also try `study`). Also try the slug with stopwords removed (`the`, `of`, `a`, `an`, `and`). A file matches if its name contains the candidate substring with at least 5 characters of overlap. If multiple files match, prefer the shortest filename. (Covers `[[DFY Programming]]` → `dfy-team-programming.md` via full slug, `[[Weekly Film Study]]` → `film-study-methodology.md` via dropped leading word.)

If all four strategies fail → treat as new concept and create stub per 4d.

**Log every resolution** in the weekly summary so Scott can spot misroutes:
```
- [[Insiders]] → wiki/entities/gw-insiders.md (matched via gw- prefix)
- [[Foo Bar]] → STUB created at wiki/concepts/foo-bar.md
```

**4c. If the concept page exists** → append (or extend an existing) `## Voice corpus` section at the bottom:

```
## Voice corpus
- 2026-05-13 — [[2026-05-13-personalized-education-and-application]] — Personalized education and application for Insiders
```

The gloss is the voice note's `title:` frontmatter. If a `## Voice corpus` section already exists, append the new bullet under it (don't duplicate the heading, don't duplicate an existing entry for the same voice note).

**4d. If the concept page does NOT exist** → create a stub. Infer domain folder from the voice note's `tags:` frontmatter:
- contains `business` → `wiki\business\<slug>.md`
- contains `ai` → `wiki\ai\<slug>.md`
- otherwise → `wiki\concepts\<slug>.md`

If multiple domain tags apply, prefer business > ai > default (business wins for the GW context).

Stub format:

```markdown
---
title: "<Concept Name>"
tags: [concept, stub, voice-corpus-origin]
created: <today YYYY-MM-DD>
status: stub
---

# <Concept Name>

Stub created from Scott's voice note on <date>. Expand as more material accumulates.

## Voice corpus
- <date> — [[<voice-note-slug>]] — <voice note title>
```

**4e. Identify 2-3 strongest themes** across the week's voice notes for the weekly summary report (carries forward to Step 5).

### 4.5. Expand stale stubs (wiki health)

The wiki's stub rate is the "wide but shallow" risk. This step burns it down 3-5 pages per week.

1. Read `wiki\system\wiki-health-report.md` (produced by `scripts/wiki_health.py`). Find the `## Stale stubs (oldest first)` list.
2. Pick 3-5 stubs, oldest first. Skip any stub whose topic has zero vault material (log it as `skipped - no sources yet` instead of padding a page with generic filler).
3. For each pick, expand the stub into a real concept page: the teaching, the evidence, the application (per the concept page convention in `Gridiron Warrior/CLAUDE.md`), plus wikilinks to related concept/entity pages. Source material from the vault only: Voice Corpus, wiki summaries, research briefs, course transcripts. Remove `stub` from the page's tags/status when done.
4. Update the page's one-line description in `wiki/index.md` if it changed, and log each expansion in `wiki/log.md`.
5. Carry the list of expanded pages forward to the Step 5 report.

### 5. Write weekly synthesis report

Save to `D:\Claude Projects\Gridiron Warrior\wiki\summaries\weekly-synthesis-YYYY-MM-DD.md`:

```markdown
---
title: "Weekly Synthesis — Week ending YYYY-MM-DD"
tags: [weekly-synthesis, summary]
date: YYYY-MM-DD
pipeline: gw-weekly-synthesis
---

# Weekly Synthesis — Week ending YYYY-MM-DD

## Themes of the week

<2-4 themes that recurred across multiple sources>

## What got promoted to wiki this week

- **Concept pages created**: <N>
- **Concept pages updated**: <N>
- **Top Dewey saves promoted**: <list with wikilinks>
- **Voice notes wikilinked from existing concepts**: <N links across M concept pages>
- **Voice-note-origin stubs created**: <list with wikilinks>
- **Stale stubs expanded to full pages**: <list with wikilinks, or "none">
- **Briefs queued for further research (no wiki page yet)**: <list of [topic-slug] → which queue, or "none">

## Voice corpus highlights

<2-3 strongest themes from Scott's voice notes>

## Content seed inventory

<which daily seeds got used vs. which sit unused>

## Recommended focus for next week

<1-3 specific suggestions: topics to research, content angles to pursue, Dewey gaps to fill>

## Queue health

- Business queue: <N remaining, recommend adding: ...>
- AI queue: <N remaining, recommend adding: ...>
```

### 6. Append to wiki log

```
2026-MM-DD /gw-weekly-synthesis: N promoted, M concepts updated, themes: X, Y, Z
```

Do not commit automatically. Leave the changes unstaged and report the exact file list.
If Scott explicitly asks for the commit later, use:

```bash
python "D:\Claude Projects\Gridiron Warrior\scripts\git_safe_commit.py" --paths "Gridiron Warrior/wiki" "Gridiron Warrior/External Library/BusinessDocuments/_topic-queue.md" "Gridiron Warrior/External Library/AI/_topic-queue.md" --message "synthesis: weekly synthesis week of YYYY-MM-DD"
```

### 7. Print the completion marker (ALWAYS last)

As the very last line of your output, print EXACTLY:

```
GW-DONE: weekly-synthesis
```

Print it once the synthesis report is written and the wiki log line is appended. The only time it must NOT appear is if you crashed or bailed before finishing the synthesis (e.g. could not read the vault). `run_job.py` validates on this marker — without it the gate is recorded `failed (artifact_invalid)` and rerun.

## Notes

- This is the cadence that keeps the wiki tight as the vault grows
- Without it, External Library bloats and concept pages go stale
- Output is a 1-page summary Scott reads on Sunday evening
