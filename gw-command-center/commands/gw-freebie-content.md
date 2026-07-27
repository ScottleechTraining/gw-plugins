---
name: gw-freebie-content
model: sonnet
description: "Scott's voice-edit layer for interactive freebies. extract mode pulls every coach-facing string out of a freebie's index.html into an editable CONTENT.md; apply mode maps Scott's edited CONTENT.md back into the HTML, runs voice check + smoke test, and rebuilds the review page. Runs BEFORE any freebie is promoted to the Vault or committed."
---

# /gw-freebie-content <freebie-folder> [extract|apply]

Scott approves a freebie on freebies.html, but the words inside it are a
draft until he has passed through them. This command gives him an editable
markdown surface so he never has to touch HTML or JS.

The lifecycle: forge builds `index.html` -> **extract** writes `CONTENT.md`
beside it -> Scott edits CONTENT.md in Obsidian (or anywhere) -> **apply**
maps his words back into index.html -> voice check + smoke test -> review
page rebuild -> only then is the freebie ready for Vault promote / commit.

## Input

`$ARGUMENTS`: a freebie folder (contains `index.html`) plus optional mode.
If the folder is a bare slug, resolve it under
`C:/Claude Projects/Gridiron Warrior/Deliverables/` (search `projects/**/incoming/`
and `ready/`). If mode is omitted: `extract` when no CONTENT.md exists,
`apply` when one does.

## Mode: extract

1. Read `index.html`.
2. Write `CONTENT.md` in the same folder containing EVERY coach-facing string:
   hero title/subtitle, intro paragraphs, input labels and hints, button
   labels, result headers, all JS-generated message strings (start notes,
   schedule notes, calibration notes), every drill/exercise name and
   description, every table row of programming numbers, trace/fine-print,
   gate copy, footer CTAs, sign-off.
3. Structure: `##` section per page region, `###` per repeated item (drill,
   week), `**Field:**` per single string. Headings and bold labels are the
   map back into the HTML; say so at the top of the file.
4. Frontmatter MUST include `knowledge_sources:` listing the vault files the
   teaching traces to (from the forge trace note or the source brief), and a
   line flagging any numbers that are forge-written ranges rather than
   vault-sourced, so Scott knows exactly what to scrutinize.
5. Where the JS interpolates values (week counts, day counts), show `N` in
   the template string and note it.
6. Report the path and tell Scott: edit anything, keep the headings, then say
   "apply my freebie edits to <slug>".

## Mode: apply

1. Read `CONTENT.md` and `index.html`.
2. For each field, if Scott's text differs from what is in the HTML/JS,
   Edit the HTML to match. Preserve interpolation: where the template shows
   `N`, keep the JS expression that produces the number. Escape quotes
   properly inside JS strings. Never alter logic, only strings.
3. If Scott changed programming numbers (sets/holds/reps/week labels), update
   the data arrays (e.g. `WEEK_LADDER`), not just display text.
4. Voice check: `python "C:/Claude Projects/Gridiron Warrior/scripts/voice_check.py" <index.html>`
   if the script accepts HTML; otherwise scan the changed strings yourself for
   em-dashes and banned words. Scott's own words win over the banned list;
   flag, do not silently rewrite him.
5. Smoke test: if the file has a `module.exports` guard, run its pure logic
   under node (or the existing test pattern) to confirm nothing broke.
6. Set `status: scott-edited` in CONTENT.md frontmatter, then rebuild the
   review page: `cd "C:/Claude Projects/Gridiron Warrior" && python -m scripts.gwqueue.build_freebie_review_page`.
7. Report a short diff summary: which fields changed, voice check result,
   smoke test result. The freebie is now ready for promote/commit (which is
   still a separate, Scott-triggered step).

## Hard rules

- Do NOT commit, publish, upload, or promote to the Vault. This command only
  edits the freebie in place.
- Do NOT rewrite Scott's edits back toward the draft. His words are final;
  only flag genuine mechanical problems (broken quote escaping, em-dashes).
- Do NOT touch logic, styling, the Kit gate wiring, or localStorage keys.
- CONTENT.md stays beside index.html permanently as the provenance + edit
  record. Do not delete it after apply.
