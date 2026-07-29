---
name: gw-freebie-apply
model: sonnet
description: "Apply a pasted gw-freebie-result string from freebies.html. approve marks a freebie eligible for the Vault, edit flags it (with a note) for the fix batch, kill retires it: standalone .md files move to killed/_freebies/, PDFs inside topic folders just get marked killed in the sidecar. Mechanical parse and apply, no judgment."
---

# GW Freebie Apply - Apply pasted freebie-review decisions

Scott reviews every freebie candidate in `freebies.html`, picks APPROVE /
EDIT / KILL per item, and copies a `gw-freebie-result:` string. This command
parses it and writes decisions to the sidecar `freebie-state.json` and moves
killed standalone `.md` files. Page: `scripts.gwqueue.build_freebie_review_page`
(that is the contract this mirrors; the page only READS the sidecar, applying
is this command's job).

## Paths

- **Deliverables:** `C:/Claude Projects/Gridiron Warrior/Deliverables/`
- **Sidecar state:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/freebie-state.json`
- **Freebies page:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/freebies.html`
- **Killed freebies:** `C:/Claude Projects/Gridiron Warrior/Deliverables/killed/_freebies/`

## Input: the pasted string

```
gw-freebie-result: approve=[id1,id2] edit=[id3:"note",id4] kill=[id5]
```

Three buckets. `approve` and `kill` are plain comma-separated ids. `edit`
entries may carry an optional `:"note"` suffix (double-quoted, may contain
commas, so parse on the bracket structure, not naively on commas). Any bucket
may be empty. Each id is the freebie's stable id from the page: its path
relative to `Deliverables/`, extension dropped, slashes replaced with `__`
(e.g. `ready__hell-week__hell-week-freebie`). If the string is not prefixed
`gw-freebie-result:` or is missing any of the three buckets, report
"malformed freebie-result string" with what you got and STOP. Do not guess.

## Verdict semantics

- **approve**: sidecar `status = "approved"`. Eligible for Vault/delivery.
- **edit**: sidecar `status = "edit"` plus `note`. The fix batch picks it up
  with the note. If no note was given, still set status `edit` with empty note.
- **kill**: sidecar `status = "killed"`. If the freebie is a standalone `.md`
  (id contains no `lead-magnet` segment and the resolved file ends in `.md`),
  MOVE the file to `killed/_freebies/`. PDFs/XLSX inside topic folders are NOT
  moved (they live beside their pack); they are only marked killed in the
  sidecar so the page mutes them.

## Step 1: Parse and apply

Apply it with the applier module. Pass the whole pasted line,
`gw-freebie-result:` prefix included, as ONE argument:

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.apply_freebie "PASTED_STRING"
```

Quoting rule for Git Bash: use SINGLE quotes around the string if any edit
note carries `\"` escapes (double quotes strip the backslashes before python
sees them). If quoting gets awkward, skip it entirely: write the pasted line
to a temp file and feed it on stdin, which the module reads when no argument
is given:

```bash
python -m scripts.gwqueue.apply_freebie < path/to/result.txt
```

The module prints one action line per decision (`approve` / `edit` / `kill`).
A missing bucket exits with a `MALFORMED:` line, and a corrupt sidecar stops
it cold (the sidecar is the full decision history; it is never silently
reset). Report either error and STOP. Parser and apply logic live in
`scripts/gwqueue/apply_freebie.py` with tests in
`scripts/gwqueue/tests/test_apply_freebie.py`. Do not re-inline this logic as
a bash heredoc: on Windows Git Bash the heredoc mangles the backslash-heavy
note regex into an invalid pattern, which is exactly the crash the gw-review
module replaced.

## Step 2: Rebuild the page

Decided items re-render muted with their status badge so Scott can change his
mind later.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.build_freebie_review_page
```

## Step 3: Report

One table, exactly what was applied:

| verdict | id | result |
|---|---|---|
| approve | ... | eligible for Vault |
| edit | ... | flagged for fix batch (note) |
| kill | ... | moved to killed/_freebies/ OR marked killed in place |

Note any `kill ... (file gone)` lines so a mistyped or already-moved id is
visible, not silent.

## Voice

Mechanical status output. Any recommendation stays in Scott's tone: short,
direct, no em-dashes.
