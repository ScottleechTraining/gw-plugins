---
name: gw-dewey-daily
model: sonnet
description: "Daily Dewey sheet check - classify new rows into S&C / Business / AI / Skip"
---

# /gw-dewey-daily — Daily Dewey Ingest with 3-Domain Classification

Fires daily. Reads the Dewey Google Sheet for new rows since last run. Classifies each row and writes notes to the appropriate domain subfolder.

## Inputs

- Dewey Sheet ID: `1G5hGEBd5oGWN4po1RV3dKNPW3cIJq9HI5lrVFf8784U`
- Last-run cursor: `External Library\Twitter-Instagram Saves\.dewey-cursor.txt` (last processed row ID; created on first run)

## Steps

### 1. Pull unprocessed rows

Run the helper at its real path (sources `~/.bashrc` for `DEWEY_SHEET_ID` + `GOOGLE_APPLICATION_CREDENTIALS`):

```bash
source ~/.bashrc
python "D:/Claude Projects/Skills/tools/dewey_ingest/dewey_ingest.py" list-unprocessed
```

Get rows with `Processed: FALSE` OR `Processed` not set. (Path note: the helper lives under `Skills/tools/`, not `tools/` — the `tools/` dir was removed in the 2026-05-12 cleanup.)

### 2. Classify each row

For each row, classify into ONE of:

| Tag | Criteria |
|---|---|
| `s-and-c` | S&C coaching, football, weight room, athletic performance, contact prep, programming, recovery, periodization, mobility, speed, agility — anything that goes in `wiki\concepts\` |
| `business` | Marketing, sales pages, email funnels, sponsorships, pricing, business operations, course launches, lead gen, copywriting, branding |
| `ai` | AI tools, prompts, Claude / GPT / Gemini, automation, agent design, MCP, no-code, AI-assisted content |
| `skip` | Off-topic, spam, duplicates, low quality, personal-only |

Use post caption + author + media OCR to decide. When ambiguous, prefer richer domain (a coach-business overlap → tag as `s-and-c` if it's tactically coaching, `business` if it's positioning/marketing).

### 3. Write notes

Follow existing `gw-dewey-ingest` SKILL.md schema for note format. Add a NEW required frontmatter field:

```yaml
domain: s-and-c | business | ai
```

File location pattern (NEW):
- `External Library\Twitter-Instagram Saves\<author>\[author]_[post_id].md` (existing pattern, KEEP)
- ALSO write a symlink-style reference file (just a note with a wikilink) to:
  - `External Library\Twitter-Instagram Saves\_by-domain\s-and-c\YYYY-MM-DD-[author]-[post_id].md`
  - `External Library\Twitter-Instagram Saves\_by-domain\business\YYYY-MM-DD-[author]-[post_id].md`
  - `External Library\Twitter-Instagram Saves\_by-domain\ai\YYYY-MM-DD-[author]-[post_id].md`
- (Skip-tier: no file written, just mark row Processed in sheet)

### 4. Update cursor + mark sheet

- Write last-processed row ID to `.dewey-cursor.txt`
- Mark rows `Processed: TRUE` in Dewey sheet

### 5. Append to log

Append a one-line summary to `wiki\log.md`:

```
2026-MM-DD /gw-dewey-daily: N rows processed (S&C: X, Business: Y, AI: Z, Skipped: K)
```

### 6. Do NOT commit

The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing files and the wiki/log.md line.

### 7. Print the completion marker (ALWAYS last)

As the very last line of your output, print EXACTLY:

```
GW-DONE: dewey-daily
```

Print it whether you processed rows or skipped gracefully (e.g. sheet unreachable, no new rows). The only time it must NOT appear is if you crashed before finishing. `run_job.py` validates on this marker — without it the gate is recorded `failed (artifact_invalid)` and rerun, even though exit code was 0. This is how the pipeline tells "ran to completion" apart from "bailed silently."

## Notes

- This extends, doesn't replace, `gw-dewey-ingest` skill
- If sheet is unreachable, report and skip — do not fail loudly
- Idempotent: re-running same day is safe
