---
name: gw-film-study-brief
model: claude-opus-5
description: "Film Study full production chain - brief + wiki ingest + content pack + Substack + IG carousel + freebie. Manual invocation, no email, no commit."
---

# /gw-film-study-brief [topic] — Full Film Study Production Chain

Replaces the retired Sunday Film Study production stack ([retirement note](../../../docs/superpowers/cowork-tasks/_archive/2026-05-24-film-study-sunday-stack/README.md)). Scott invokes manually when he wants a full Film Study asset set.

**Every run produces the full chain:**

1. Research brief (corpus + NotebookLM, merged)
2. Wiki ingest (summary + concept stubs)
3. Content pack (`/gw-content-forge`)
4. Substack article draft (`/gw-substack-forge`)
5. IG carousel (`ig-carousel` skill)
6. Lead-magnet freebie (`/gw-freebie-forge`)

**What it does NOT do:** email, commit, publish, post, or schedule anything. Those stay manual. Scott reviews everything and ships what he wants to ship.

**Why the chain came back:** the 5/24 retirement killed the Sunday *autonomous scheduler*, not the production logic. The fragility risk that killed the Sunday run is mitigated here by manual invocation — Scott is at the terminal when the chain runs, so failures are visible and recoverable in-context, not silent 7am breakages.

Scope: deliver all six chain outputs and nothing past them. The floor is brief + wiki ingest (summary page, concept stubs, index line) + content pack + Substack draft + IG carousel + freebie, plus the status file and the one wiki/log.md line. A logged step failure is not permission to ship five. Do not invent artifacts the chain does not name, and do not re-run a step that already succeeded.

## Topic: $ARGUMENTS

The user provides a coaching topic as `$ARGUMENTS` (e.g., `"tri-set structure for high school football summer training"`).

If `$ARGUMENTS` is empty, fall through to Step 0 to pop a topic from the queue.

## Vault paths

- **Topic queue:** `C:\Claude Projects\Gridiron Warrior\Research\Film Study\_topic-queue.md`
- **Brief output:** `C:\Claude Projects\Gridiron Warrior\Research\Film Study\YYYY-MM-DD-<topic-slug>-film-study-brief.md`
- **Corpus query feedstock (from `/gw-everything-on`):** `C:\Claude Projects\Gridiron Warrior\Deliverables\_corpus-queries\YYYY-MM-DD-<topic-slug>.md`
- **Wiki log (append one line):** `C:\Claude Projects\Gridiron Warrior\wiki\log.md`
- **Wiki summary output:** `C:\Claude Projects\Gridiron Warrior\wiki\summaries\film-study-<topic-slug>.md`
- **Wiki concept stubs:** `C:\Claude Projects\Gridiron Warrior\wiki\concepts\<concept-slug>.md`
- **Wiki index:** `C:\Claude Projects\Gridiron Warrior\wiki\index.md`
- **Deliverables (content pack / Substack / carousel / freebie):** `C:\Claude Projects\Gridiron Warrior\Deliverables\`
- **Status file:** `C:\Claude Projects\Gridiron Warrior\scripts\health\film-study-brief-YYYY-MM-DD.status.json`

Slug rules: kebab-case, truncate to 50 chars, strip special chars.

## Preflight gate

Call it first:

```bash
python "C:\Claude Projects\Gridiron Warrior\scripts\preflight.py" --gate film-study-brief
```

- Exit code 0 → proceed.
- Exit code 10 → preflight wrote a `blocked` status file. Stop. Tell Scott the next action from the status file's `next_action` field.
- Any other non-zero → preflight bug. Surface the error to Scott and stop.

The `film-study-brief` gate is registered in `scripts/preflight-gates.json` and checks auth, NotebookLM MCP, network, the vault, and the four chain directories. This command is manual-only: no scheduled task, no `job-contracts.json` entry.

## Step 0 — Resolve topic (queue pop if no argument)

If `$ARGUMENTS` is non-empty: set `topic = $ARGUMENTS`, set `topic_source = "argument"`, skip to Step 1.

If `$ARGUMENTS` is empty:
1. Read `C:\Claude Projects\Gridiron Warrior\Research\Film Study\_topic-queue.md`.
2. Find the first non-placeholder line under `## Active Queue` (skip any line starting with `(placeholder` or empty bullets).
3. Parse line format: `- topic name [topic-slug]`. Extract both the human topic and the slug.
4. If a valid topic is found: set `topic = <parsed topic>`, set `topic_source = "queue"`, proceed to Step 1.
5. If queue is empty (no valid lines): **abort cleanly.** Print this exact message and stop:

   > Queue is empty and no topic was supplied. Either:
   >
   > 1. Add topics to `C:\Claude Projects\Gridiron Warrior\Research\Film Study\_topic-queue.md` under `## Active Queue`, then re-run `/gw-film-study-brief`.
   > 2. Or supply a topic directly: `/gw-film-study-brief "deceleration mechanics"`.
   >
   > No auto-pick — this command is demand-driven by design.

   Do NOT write a brief, do NOT write a status file, do NOT touch the wiki. Just stop.

## Step 1 — Corpus query

Invoke `/gw-everything-on <topic>`. This writes `Deliverables/_corpus-queries/YYYY-MM-DD-<topic-slug>.md` (or appends `-2` if a same-day run exists). Capture the resulting file path. You cite it in Step 3.

If the corpus query returns zero matches, continue anyway — the NotebookLM step may still produce material. Note the empty corpus result in the final brief.

## Step 2 — NotebookLM query against S&C Master Resource

```
mcp__notebooklm__notebook_list
```

Locate the notebook named `S&C Master Resource` (or closest match). Then:

```
mcp__notebooklm__notebook_query
  notebook_id: <S&C Master Resource id>
  query: <topic, expanded if needed for clarity>
```

Capture the response. If the notebook isn't found or the query fails, note the failure in the brief — do NOT fabricate NotebookLM content.

## Step 3 — Merge into one brief

Read the corpus-query output file from Step 1 (skim — do NOT inline the full file). Extract:
- The 3-5 themes from its **Themes** section.
- 6-12 best-signal excerpts from its **By Source** sections.

Combine with the NotebookLM response into a single brief at `Research/Film Study/YYYY-MM-DD-<topic-slug>-film-study-brief.md`.

Density: the counts in the template are ceilings, not targets. Keep a takeaway, theme, or excerpt only when it changes what Scott would teach on camera. Excerpts stay verbatim and short. No word-count target for any section, and no section gets padded to look full.

Use this structure:

```markdown
---
title: "Film Study Brief, [topic]"
type: film-study-brief
topic: "[topic]"
topic_slug: [topic-slug]
date: YYYY-MM-DD
topic_source: [argument|queue]
pipeline: gw-film-study-brief
corpus_query: [path to corpus-queries file]
notebooklm_notebook: "S&C Master Resource"
notebooklm_query: [literal query string sent]
---

# Film Study Brief, [Topic]

**Topic:** [topic]
**Date:** YYYY-MM-DD
**Sources:** GW corpus + NotebookLM S&C Master Resource

## Bottom-line takeaways

3-5 bullets. Coach-direct. Each bullet is a teaching point Scott could open a Film Study with — not a generic restatement of the topic.

## Themes from the corpus

3-5 short paragraphs lifted from the `/gw-everything-on` Themes section. One paragraph per theme. Each paragraph cites the corpus-query file path so Scott can drill in.

## NotebookLM: S&C Master Resource

Direct quote of the NotebookLM response. Preserve attribution / source citations if NotebookLM returned them. If NotebookLM failed or returned nothing useful, say so plainly.

## Best corpus excerpts

6-12 short excerpts (3-8 lines each). Each must include its source file path as a header. Do not paraphrase — quote verbatim.

#### `External Library\S-and-C\<file>.md`
> [excerpt]

(…etc.)

## Pre-recording outline

A loose outline Scott can use as a starting point for the Film Study recording itself. Hook, 3-4 teaching points, one drill demo suggestion, one coaching takeaway, one call to the room. Not a script.

## Chain artifacts produced

(Filled in at Step 10.)
```

## Step 4 — Append to wiki log

Append ONE line to `C:\Claude Projects\Gridiron Warrior\wiki\log.md`:

```
YYYY-MM-DD /gw-film-study-brief: [topic-slug] (corpus N, NL: ok|empty|failed, chain: pending)
```

The chain status is updated at Step 11. For now write `chain: pending`.

## Step 5 — Write initial status file

Write `C:\Claude Projects\Gridiron Warrior\scripts\health\film-study-brief-YYYY-MM-DD.status.json` with status `in_progress`:

```json
{
  "job": "film-study-brief",
  "status": "in_progress",
  "started": "<ISO timestamp>",
  "topic": "<topic>",
  "topic_source": "argument|queue",
  "brief_path": "<absolute path to brief>",
  "corpus_query_path": "<absolute path>",
  "notebooklm_result": "ok|empty|failed",
  "chain_steps": {
    "wiki_ingest": "pending",
    "content_pack": "pending",
    "substack": "pending",
    "carousel": "pending",
    "freebie": "pending"
  }
}
```

## Step 5.5 — Queue maintenance (only if topic came from queue)

If `topic_source == "queue"`:

1. Re-read `Research/Film Study/_topic-queue.md`.
2. Remove the consumed line from `## Active Queue`.
3. Append to `## Completed` with date prefix: `- YYYY-MM-DD - <topic name> [<topic-slug>]`.
4. Update the frontmatter `updated:` field to today's date.
5. Write the file back.

If `topic_source == "argument"`, skip this step entirely — queue not touched.

## Step 5.6 — Tick off any driving topic this film study covered

Read `Voice Corpus\_driving-topics.md`. Compare this film study's topic and brief against the
lines under `## Active`. These are Scott's drive-in talk prompts; the dashboard shows a rotating
five of them daily as the "Driving Conversations" board.

Move a topic to `## Covered` ONLY when the film study substantively covers it. Judge by meaning,
not by shared words. Cut the line out of Active and append it under `## Covered` in this shape:

```
- YYYY-MM-DD | <the topic line, verbatim> | [[film-study-<topic-slug>]]
```

Never reword a topic line, never delete one, and never move a topic the film study did not
cover. If nothing matched, leave the file untouched.

## Step 5.7 — Wiki auto-ingest

**Fact-density rule (2026-08-03):** pull EVERY number the source states (set counts, timelines, percentages, testing results, injury rates, loads) into the summary page, each with its context. Numbers are what makes a future page citable by AI answer engines; prose buries them. A summary with zero numbers from a numeric source is an incomplete ingest.

**Write the summary page** at `wiki/summaries/film-study-<topic-slug>.md`:

```markdown
---
title: "Film Study, [topic]"
type: film-study-summary
topic: "[topic]"
topic_slug: [topic-slug]
date: YYYY-MM-DD
source_brief: [absolute path to the brief]
external_origin: false
pipeline: gw-film-study-brief
---

# Film Study, [Topic]

**Source:** [link to brief file]
**Date:** YYYY-MM-DD

## Key takeaways

(Copy "Bottom-line takeaways" section from the brief verbatim.)

## Themes

(One-line per theme — pulled from the brief's "Themes from the corpus" section. Compress, do not copy full paragraphs.)

## Concept stubs created

(List of `wiki/concepts/<slug>.md` stubs created in this run. Blank if none.)

## Cross-links

(Any wiki entity or concept page already referenced in the brief — link to them here.)
```

**Create concept stubs.** Scan the brief's "Bottom-line takeaways" and "Themes from the corpus" sections for distinct coaching concepts. For each concept that does NOT already have a page in `wiki/concepts/`:

1. Slug the concept name (kebab-case).
2. Write `wiki/concepts/<concept-slug>.md`:

```markdown
---
title: "[Concept Name]"
type: concept
external_origin: false
origin: "Scott's own recorded Film Study on [topic] (YYYY-MM-DD); brief-sourced external components attributed inline"
source_brief: [absolute path to the brief]
date_created: YYYY-MM-DD
status: stub
---

# [Concept Name]

**Origin:** Film Study brief on [topic] ([YYYY-MM-DD](path-to-brief))

## What the brief said

(2-4 sentences pulled from the brief about this specific concept.)

## How Scott uses this in GW

*[TODO: Scott fills during weekly synthesis. Until filled, this concept is reference-only and NOT voice-input safe.]*

## Related

(Any cross-links to existing wiki entities or concepts.)
```

**Skip stub creation if a concept page already exists** — don't clobber. Note the existing page in the summary's "Cross-links" section instead.

**Update `wiki/index.md`.** Find or create a `## Film Study Briefs` section. Append a line:

```
- [Film Study, [topic]](summaries/film-study-<topic-slug>.md) (YYYY-MM-DD)
```

**Update the chain_steps in the status file:** set `wiki_ingest` to `"ok"` (or `"failed"` with `error` field if any step above broke).

## Step 6 — Content pack

Invoke `/gw-content-forge "<absolute path to brief>"`.

- On success: capture the output file path. Set `chain_steps.content_pack = "ok"` in status file, record path.
- On failure: set `chain_steps.content_pack = "failed"` with `error` and `next_action: "Re-run: /gw-content-forge \"<brief path>\""`. **Continue the chain.** Do not abort.

## Step 7 — Substack draft

Invoke `/gw-substack-forge "<absolute path to brief>"` (uses `gw-command-center:gw-substack-forge`).

- On success: capture output path. Set `chain_steps.substack = "ok"`, record path.
- On failure: log to status file with `next_action: "Re-run: /gw-substack-forge \"<brief path>\""`. **Continue.**

## Step 8 — IG carousel

Invoke the `ig-carousel` skill (`gw-command-center:ig-carousel`) against the brief. Save the HTML to `Deliverables/<topic-slug>-carousel.html`.

- On success: capture path. Set `chain_steps.carousel = "ok"`.
- On failure: log with `next_action`. **Continue.**

## Step 9 — Freebie

Invoke `/gw-freebie-forge "<absolute path to brief>"`.

- On success: capture path. Set `chain_steps.freebie = "ok"`.
- On failure: log with `next_action: "Re-run: /gw-freebie-forge \"<brief path>\""`. **Continue (this is the last step anyway).**

## Step 10 — Finalize status file + log line

**Update the status file** with final status:

- If all chain steps succeeded: `status: "complete"`.
- If any chain step failed: `status: "partial"`. Include `partial_failures: [list of failed step names]`.
- If the brief itself failed before reaching the chain: `status: "failed"`.

Add `ended: <ISO timestamp>` and all artifact paths under a `paths` block:

```json
{
  "paths": {
    "brief": "...",
    "wiki_summary": "...",
    "concept_stubs": ["..."],
    "content_pack": "...",
    "substack": "...",
    "carousel": "...",
    "freebie": "..."
  }
}
```

**Update the wiki log line** written in Step 4. Find the line you wrote and replace `chain: pending` with `chain: complete|partial` and append the partial-failures list if any:

```
YYYY-MM-DD /gw-film-study-brief: [topic-slug] (corpus N, NL: ok, chain: partial, failed: [substack, freebie])
```

**Update the brief's "Chain artifacts produced" section** with paths to every artifact (and failure notes for any partial).

## Step 11 — Report to Scott

Tell him, in this order:

1. **Topic + topic source** — `[topic] (from queue|from argument)`
2. **Brief path**
3. **Chain status** — complete | partial | failed
4. **Per-step status table:**
   - wiki ingest: ok / failed
   - content pack: ok (path) / failed (next_action)
   - Substack: ok (path) / failed (next_action)
   - carousel: ok (path) / failed (next_action)
   - freebie: ok (path) / failed (next_action)
5. **One-line teaching highlight** from the brief's "Bottom-line takeaways" — the single strongest line Scott should look at first.
6. **Reminder:** "Nothing was committed. Nothing was emailed. Review and ship what you want to ship."

Keep it tight. Scott has 15 minutes.

## Hard rules — what this command MUST and MUST NOT do

**MUST run, in order:**
- Brief (Steps 1-3)
- Wiki ingest (Step 5.7)
- Content pack (Step 6)
- Substack draft (Step 7)
- IG carousel (Step 8)
- Freebie (Step 9)

**MUST keep going on downstream failure.** A failed Substack-forge does not block the carousel. Each step independently logged. Scott re-invokes failing steps using the brief path.

**MUST NOT:**
- Email anyone. No SMTP. No pending-email JSON write. No Kit draft. Nothing.
- Commit, push, or call `git` on Scott's behalf.
- Publish to Substack. Post to IG. Send anything to Kit. Schedule any future run.
- Auto-pick a topic when the queue is empty (abort instead).
- Re-enable the retired Sunday cowork prompts (`gw-notebooklm-handshake`, `gw-film-study-pipeline-run`, `gw-film-study-weekly-batch-prep`). Those stay archived.
- Use em-dashes anywhere in produced content. Use any banned word from CLAUDE.md.

## Voice and tone (for the synthesis sections)

- Coach-direct. Short sentences. Plain language.
- No em-dashes. No banned words (see CLAUDE.md / AGENTS.md).
- Quote excerpts verbatim. Don't "clean up" voice transcripts.
- This is a research brief Scott will mine — clarity over polish.
- Downstream skills (content-forge, substack-forge, freebie-forge) enforce their own voice rules on their outputs. Don't second-guess them.

## Notes

- **Idempotent within a day** via the `-2`, `-3` convention. If a same-day brief exists, the new brief and all downstream artifacts get `-2` appended before the extension.
- **`Research/Film Study/` is for briefs only.** Not for content packs (that's `Deliverables/`), not for published material (that's `wiki/`), not for transcripts (that's `raw-sources/` or `Voice Corpus/`).
- **NotebookLM failure is NOT fatal.** Brief proceeds corpus-only. Wiki ingest proceeds. Chain proceeds. Status file records the NotebookLM gap.
- **The SOURCE decides `external_origin`, not a blanket default (fixed 2026-08-17 per Scott).** A Film Study is Scott's own recorded teaching, so pages built on his transcript are `external_origin: false`: his voice, voice-input safe. External material the brief blended in (NotebookLM sources, other coaches' numbers) gets INLINE attribution at point of use, never a page-level external flag. Only a pre-recording research-only run (no transcript exists, `TRANSCRIPT NOT YET RECORDED` status) is flagged `external_origin: true`, because that page is NotebookLM material with no Scott voice in it. Why this changed: the old default-external posture quarantined 13 summaries and 4 concept stubs of Scott's OWN camp system out of voice-safe input, and the "Scott flips at synthesis" step never happened; three surfaces grew hand-written workarounds instead. The "How Scott uses this in GW" block on concept stubs stays as TODO until filled.
- **Partial success is fine.** A run that produces brief + wiki + content pack + carousel + freebie but fails Substack is still a valuable run. Scott just re-invokes `/gw-substack-forge` against the brief path.
