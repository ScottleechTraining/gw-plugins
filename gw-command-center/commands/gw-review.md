---
name: gw-review
model: claude-opus-5
description: "Build and open a single local HTML contact sheet of every pending carousel (SHIP / POLISH / KILL per topic), then apply the pasted gw-review-result string: ship flips ready_to_ship, polish records a note, kill moves the folder to the terminal killed/ folder (never rescanned, no restore)."
---

# GW Review - Carousel approval contact sheet

Scott reviews every pending carousel in one local page instead of opening
folders. Radios pick SHIP / POLISH / KILL per topic, the page compiles a
`gw-review-result:` string, and pasting that string back applies every
decision. No server, no upload, all local.

## Paths

- **Deliverables:** `C:/Claude Projects/Gridiron Warrior/Deliverables/`
- **Builder module:** `scripts.gwqueue.build_review_page`
- **Review page:** `C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/review.html`
- **State file:** `C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json`
- **Killed:** `C:/Claude Projects/Gridiron Warrior/Deliverables/killed/` (terminal, never rescanned, no restore)

## Step 1: Build the page

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.build_review_page
```

Reads `queue-state.json`, selects every topic where a carousel exists AND
(`carousel_needs_polish` is true OR the topic is untriaged in `_inbox`/`ready`
and not yet `ready_to_ship`), and writes `review.html`. It never mutates
`queue-state.json`. Expected output: `Wrote .../review.html (N topic(s) pending review)`.

## Step 2: Open it

```bash
start "" "C:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/review.html"
```

Tell Scott:

```
Review page open. For each carousel: SHIP / POLISH / KILL.
POLISH note is optional. When done, hit Copy and paste the
gw-review-result string back to me.
```

Then STOP and wait for Scott to paste the string. Do not proceed without it.

## Step 3: Apply a pasted gw-review-result string

The pasted string looks like:

```
gw-review-result: ship=[slug1,slug2] polish=[slug3:"note",slug4] kill=[slug5]
```

`polish` entries may carry an optional `:"note"` suffix (double-quoted, may
contain commas and `\"` escapes). Any bucket may be empty.

Apply it with the applier module. It mirrors `/gw-ship` for ship (moves
`_inbox` topics into `ready/`, flips `ready_to_ship`, clears polish flags),
records the polish note on the topic entry, and kills by moving the folder to
the terminal `killed/` folder, trimming its renderable assets on arrival
(slides/, carousel and social-pack html, loose images; every .md plus
captions/ and lead-magnet/ are kept, per the 2026-08-01 archive diet). Pass
the whole pasted line, `gw-review-result:` prefix included, as ONE argument:

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.apply_review "PASTED_STRING"
```

Quoting rule for Git Bash: use SINGLE quotes around the string if any polish
note carries `\"` escapes (double quotes strip the backslashes before python
sees them). If quoting gets awkward, skip it entirely: write the pasted line
to a temp file and feed it on stdin, which the module reads when no argument
is given:

```bash
python -m scripts.gwqueue.apply_review < path/to/result.txt
```

The module prints one action line per decision (`ship` / `polish` / `kill`,
or `SKIP` with a reason). Parser and apply logic live in
`scripts/gwqueue/apply_review.py` with tests in
`scripts/gwqueue/tests/test_apply_review.py`. Do not re-inline this logic as
a bash heredoc: on Windows Git Bash the heredoc mangled the backslash-heavy
polish regex into an invalid pattern, which is exactly the crash the module
replaced.

## Step 4: Render, sync shipped topics to Drive, re-scan, rebuild the page

Ships and kills moved folders on disk. Render/split (idempotent), then sync
EACH shipped slug so ready/ topics land on Drive immediately, then refresh:

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.render_carousel
python -m scripts.gwqueue.split_captions
# one per shipped slug:
python -m scripts.gwqueue.sync_to_drive --slug "EXACT_SLUG"
python -m scripts.gwqueue.scan_folders
python -m scripts.gwqueue.build_review_page
```

The final rebuild keeps review.html matched to the fresh state. Without it
the page keeps showing topics that were just applied; a shipped carousel
stayed on the sheet this way on 2026-07-29. The rebuild must run AFTER
scan_folders, never inside the applier: killed topics keep their stale stage
in queue-state.json until the scan drops them. Tell Scott to refresh the
page in his browser if he still has it open.

Print a summary:

```
Applied review:
  ship:   <n>  (moved to ready/, synced to Drive - post from phone anytime)
  polish: <n>  (stay in _inbox with notes recorded on the topic)
  kill:   <n>  (moved to killed/ - terminal, never rescanned, no restore)
```

If a Drive sync fails, say so plainly; the topic stays in ready/ with
`ready_to_ship: true` and the next /gw-queue run retries it. Polish topics go
back to the carousel builder with their `polish_note`.

**Restyle notes.** The review page has a style dropdown per row. When it is
used with POLISH, the note arrives as `restyle: <Pack Name>` (optionally
followed by `. <free text>`). That is a rebuild order, not a copy tweak:
`/gw-carousel-batch` picks these topics up and rebuilds the carousel in the
named pack. The pack came from a dropdown of valid names, so it counts as
confirmed - do not re-ask. After applying the string, if any polish note
starts with `restyle:`, tell the user those topics are queued for a rebuild
and that running `/gw-carousel-batch` will do it now.

**Cover notes.** A polish note starting with `cover:` means the COVER only:
the body slides are fine but slide 1 does not stop the thumb. `/gw-carousel-batch`
rebuilds slide 1 per the note using the ig-carousel skill's
`references/cover-treatments.md` (e.g. `cover: try torn paste-up` or
`cover: weak photo, use the huddle shot with spotlight`). Same follow-up:
tell the user cover rebuilds are queued for `/gw-carousel-batch`.

## Step 5: Commit (optional, ask first)

If Scott wants it committed:

```bash
cd "C:/Claude Projects"
git add -A
git commit -m "review: apply carousel decisions (<n> ship, <n> polish, <n> kill)"
```

## Voice

Mechanical status output. Any recommendation stays in Scott's tone: short,
direct, no em-dashes.
