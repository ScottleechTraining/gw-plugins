---
name: gw-screenshot-ingest
model: sonnet
description: "Daily screenshot ingest - OCR + classify + file Screenshots/inbox"
---

# /gw-screenshot-ingest — Daily Screenshot Sweep

Fires daily. Processes any images sitting in the GW vault's screenshot inbox.

## Steps

### 1. Read the inbox

Path: `C:\Claude Projects\Gridiron Warrior\External Library\Screenshots\inbox\`

List all `.png`, `.jpg`, `.jpeg`, `.PNG`, `.JPG`, `.JPEG` files.

If empty: report "Inbox empty, no-op" and exit (no commit).

### 2. For each image

- **Read** via the multi-modal Read tool (this OCRs)
- **Classify** the dominant domain: `coaching` | `business` | `ai` | `personal-skip`
  - coaching: S&C, football, weight room, programming, recovery, mobility, speed, contact prep, athletic performance
  - business: marketing, sales pages, copywriting, sponsorships, pricing, course launches, lead gen, content systems
  - ai: AI tools, prompts, Claude/GPT, automation, agent design, MCP, no-code
  - personal-skip: memes, off-topic, personal photos, low-quality
- **Slug** the topic (kebab-case, 4-8 words max) from the image content
- **Skip-tier:** if `personal-skip`, just delete or move the original to `archive/2026-MM/` — write no note
- **Otherwise:** write a markdown note at `External Library\Screenshots\processed\YYYY-MM-DD-[slug].md`:

```markdown
# [Topic title]

**Source:** [Instagram / Twitter / web / unknown]
**Captured:** YYYY-MM-DD
**Domain:** [coaching|business|ai]
**File:** YYYY-MM-DD-[slug].[ext]

## OCR text
[Full OCR'd text from the image]

## Description
[1-2 sentences describing what the image contains]

## Why Scott likely saved this
[1-2 sentences on the GW angle / coaching application]

## Tags
#[domain] #[content-idea OR other relevant]

## Linked wiki pages
- [[concepts/...]] (only if a real match exists; otherwise omit this section)

## Usage
[1 sentence on when Scott should pull this up]
```

- **Rename + move** the original image to `External Library\Screenshots\processed\YYYY-MM-DD-[slug].[ext]` (same slug as the note)

### 3. Append to wiki log

```
2026-MM-DD /gw-screenshot-ingest: N processed (coaching: X, business: Y, ai: Z, skipped: K)
```

### 4. Do NOT commit

The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing files and the wiki/log.md line.

### 5. Print the completion marker (ALWAYS last)

As the very last line of your output, print EXACTLY:

```
GW-DONE: screenshot-ingest
```

Print it whether you processed screenshots or the inbox was empty (clean no-op). The only time it must NOT appear is if you crashed before finishing. `run_job.py` validates on this marker — without it the gate is recorded `failed (artifact_invalid)` and rerun, even though exit code was 0.

## Notes

- This extends `/gw-daily` screenshot logic into a standalone, scheduler-callable skill.
- Keep the flat `processed/` folder structure (don't split by `coaching/business/ai` subfolders — current practice has all notes in one folder with domain in frontmatter).
- Don't move originals to a separate `archive/` folder — rename them to match the note slug and leave them next to the note in `processed/`.
- Idempotent: re-running on an empty inbox is a clean no-op.
