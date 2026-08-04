---
name: gw-skill-tune
model: claude-opus-5
description: "Self-improvement loop for content skills. ANALYZE mode (run by /gw-weekly-synthesis, read-only): harvest the week's free grading signals (kills, polish notes, voice-gate failures, seed usage) into concrete SKILL.md diff proposals. APPLY mode (Scott pastes approval from the Sunday report): make the approved edits in the plugin folder and ship them."
---

# /gw-skill-tune — Skill self-improvement loop

Scott never grades anything. The grades already exist as byproducts of decisions
he makes anyway: KILL clicks, POLISH notes, voice-gate FAILs, seeds he ignores.
This command harvests them weekly into proposed skill edits. He approves or
rejects from the Sunday synthesis email. That is his entire involvement.

Two modes. `/gw-skill-tune` or `/gw-skill-tune analyze` = ANALYZE.
`/gw-skill-tune apply <numbers> from <report date>` = APPLY.

## Tunable targets (allowlist — never propose edits outside it)

- `plugins/gw-command-center/commands/gw-content-forge.md`
- `plugins/gw-command-center/skills/gw-substack-forge/SKILL.md`
- `plugins/gw-command-center/commands/gw-seed-writer.md`
- `plugins/gw-command-center/commands/gw-triage.md`
- `plugins/gw-command-center/skills/ig-carousel/SKILL.md` (+ its `references/`)
- `plugins/gw-command-center/commands/gw-carousel-batch.md`

**Never tunable:** `kit-guardrails` (safety rail), `gw-voice-gate` (executable
form of Scott's voice rules — those change only when Scott changes CLAUDE.md),
and this command itself.

## ANALYZE mode (read-only — writes NOTHING; output is returned to the caller)

Called by `/gw-weekly-synthesis` Step 4.7, or standalone. When standalone, print
the proposals section instead of handing it to the report.

### 1. Harvest the week's signals

All paths under `C:/Claude Projects/Gridiron Warrior/Deliverables/` unless noted.

| Signal | Where | What it grades |
|---|---|---|
| Kills | Git history, NOT folder mtimes (the 2026-08-01 archive diet touched every `killed/` folder): `git -C "C:/Claude Projects" log --since="8 days ago" --diff-filter=A --name-only -- "Gridiron Warrior/Deliverables/killed"`. Also check `git status` for uncommitted moves out of `_inbox/` and resolve each slug to `ready/` (ship) or `killed/` (kill) before counting. | Topic/angle selection by the producing skill |
| Polish notes | `queue-state.json` — `topics` is a LIST of dicts; iterate it for `polish_note` set (incl. `restyle:` / `cover:` prefixes) | The specific weakness Scott named, with his own words |
| Voice-gate FAILs | `_system/voice-gate-log.md` lines from the last 7 days | Which producing skill keeps breaking which voice rule |
| Seed usage | The "Content seed inventory" from the current synthesis run (or last week's report when standalone) | gw-seed-writer angle quality |
| Restyle patterns | Polish notes starting `restyle:` — count per style pack | ig-carousel pack selection guidance |

Attribute each signal to its producing skill via the topic's content pack
frontmatter or folder provenance. Unattributable signals are dropped, not guessed.

### 2. Find patterns worth a proposal

A proposal requires the same weight rule as wiki promotion: the pattern must
appear **2+ independent times this week**, OR once this week AND in last week's
tune section (read the previous `wiki/summaries/weekly-synthesis-*.md`).
One-off events are noted as "watching" lines, not proposals. **Zero proposals
is a normal, good outcome.** Never invent a proposal to fill the section.

### 3. Check against history

Read the tune sections of the last 4 weekly synthesis reports:
- A proposal Scott already REJECTED does not come back unless new evidence is
  materially different. Cite the rejection instead.
- For proposals APPLIED in prior weeks, report the scoreboard: this week's
  kill / polish / gate-FAIL counts for that skill vs. the week before the edit.
  Counts are small and noisy — report them honestly, no victory laps.

### 4. Emit the proposals section

Hand this block to the synthesis report (or print it standalone):

```markdown
## Skill tune proposals

<per applied-last-week edit: one scoreboard line, e.g.
"gw-seed-writer edit from 08-02: seeds used 2/3 this week vs 0/3 prior. Keeping it.">

### Proposal 1 — <target file, one-line summary>
- **Evidence:** <the 2+ concrete signals, quoted — Scott's polish note text, kill slugs, gate-log lines>
- **Change:** exact old text → new text (a real diff, not a vibe)
- **Risk:** one line — what this could over-correct

<repeat per proposal. If none:>
No skill tune proposals this week. Watching: <one-off signals, or "nothing">.
```

And give the synthesis "Your moves" section one paste-ready block:

```
/gw-skill-tune apply 1,3 from YYYY-MM-DD   (or: apply none, reject 2 because ___)
```

## APPLY mode (runs only from Scott's explicit approval)

1. Read the named report at `Gridiron Warrior/wiki/summaries/weekly-synthesis-<date>.md`,
   locate the approved proposal numbers.
2. Make exactly those edits in the plugin folder. Nothing beyond the approved diffs.
3. Record rejections: append one line per rejected proposal (with Scott's reason
   if given) to the report's tune section, so Step 3 of future ANALYZE runs sees it.
4. Ship per the standard plugin edit flow: bump `plugin.json` version (patch),
   `claude plugin validate gw-command-center`, marketplace update + reinstall,
   commit + push the plugins repo. `/gw-plugin-ship` is the reference ritual.
5. Print a summary: files touched, old → new version, proposals applied/rejected.

## Voice

Mechanical status output. Evidence quotes Scott verbatim. No em-dashes.
