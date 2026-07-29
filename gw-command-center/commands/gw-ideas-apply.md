---
name: gw-ideas-apply
model: sonnet
description: "Apply a pasted gw-ideas-result string from ideas.html to the forge backlog. forge queues /gw-content-forge on the slug now, top bumps its score so the nightly picker takes it first, skip retires it with a recorded skip_reason. Mechanical parse and apply, no judgment."
---

# GW Ideas Apply - Apply pasted ideas-queue decisions

Scott reviews the forge backlog in `ideas.html`, picks FORGE NOW / TOP / SKIP
per idea, and copies a `gw-ideas-result:` string. This command parses that
string and mutates `queue-state.json`'s `forge_backlog`. Page:
`scripts.gwqueue.build_ideas_page` (that is the contract this mirrors).

## Paths

- **Deliverables:** `C:/Claude Projects/Gridiron Warrior/Deliverables/`
- **State file:** `C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json`
- **Ideas page:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/ideas.html`

## Input: the pasted string

```
gw-ideas-result: forge=[slug1,slug2] top=[slug3] skip=[slug4,slug5]
```

Three buckets, each a plain comma-separated list of backlog slugs. Any bucket
may be empty (`forge=[]`). Slugs never carry a note here (unlike gw-review's
polish). If the string does not contain all three `name=[...]` buckets, or is
not prefixed `gw-ideas-result:`, report "malformed ideas-result string" with
what you got and STOP. Do not guess.

## Verdict semantics

- **forge**: run `/gw-content-forge` on the slug immediately. This does NOT
  change the backlog entry's status; the next scan auto-marks it `forged` once
  the topic folder exists (see `scan_folders._process_forge_backlog`).
- **top**: bump the entry so tonight's picker takes it first. Set
  `score` to `"N/20"` where N = max(current N, 18). Leave status `pending`.
- **skip**: set `status = "skipped"` and record a `skip_reason`. House rule:
  every skip carries a reason (the ideas page lists skipped-with-reason entries
  for a human override). For a manual SKIP, use the reason Scott gives; if none,
  write `skip_reason = "manual skip from ideas review"`.

## Step 1: Apply the top and skip buckets to state

Apply it with the applier module. Pass the whole pasted line,
`gw-ideas-result:` prefix included, as the FIRST argument. If Scott gave a
spoken skip reason, pass it as the second argument; otherwise leave it off
and every skip records `manual skip from ideas review`.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.apply_ideas "PASTED_STRING" "OPTIONAL_SKIP_REASON"
```

Slugs never carry quotes or escapes, so double quotes are safe here. With no
arguments the module reads the result string from stdin (the default skip
reason applies). It prints one action line per decision (`top` / `skip`;
`forge` entries are only echoed, forging happens in Step 2) and exits with a
`MALFORMED:` line if any bucket is missing - report that and STOP. Parser and
apply logic live in `scripts/gwqueue/apply_ideas.py` with tests in
`scripts/gwqueue/tests/test_apply_ideas.py`. Do not re-inline this logic as a
bash heredoc: on Windows Git Bash heredocs mangle backslash-heavy regexes
into invalid patterns, which is exactly the crash the gw-review module
replaced.

## Step 2: Forge the forge bucket

For EACH slug in `forge=[...]` that exists in the backlog, run
`/gw-content-forge` on it now (one invocation per slug, using the backlog
entry's title/angle as the topic). If the bucket is empty, skip this step.

## Step 3: Re-scan

The scan auto-marks any freshly forged slug as `forged` and refreshes the
ideas page.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.scan_folders
python -m scripts.gwqueue.build_ideas_page
```

## Step 4: Report

One table, exactly what was applied:

| verdict | slug | result |
|---|---|---|
| forge | ... | forged now via /gw-content-forge |
| top | ... | score raised to N/20 |
| skip | ... | skipped, reason recorded |

Note any `SKIP ... (not in backlog)` lines the script emitted so a mistyped
slug is visible, not silent.

## Voice

Mechanical status output. Any recommendation stays in Scott's tone: short,
direct, no em-dashes.
