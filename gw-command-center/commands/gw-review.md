---
name: gw-review
description: "Build and open a single local HTML contact sheet of every pending carousel (SHIP / POLISH / KILL per topic), then apply the pasted gw-review-result string: ship flips ready_to_ship, polish records a note, kill moves the folder to trash-review."
---

# GW Review - Carousel approval contact sheet

Scott reviews every pending carousel in one local page instead of opening
folders. Radios pick SHIP / POLISH / KILL per topic, the page compiles a
`gw-review-result:` string, and pasting that string back applies every
decision. No server, no upload, all local.

## Paths

- **Deliverables:** `D:/Claude Projects/Gridiron Warrior/Deliverables/`
- **Builder module:** `scripts.gwqueue.build_review_page`
- **Review page:** `D:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/review.html`
- **State file:** `D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json`
- **Trash:** `D:/Claude Projects/Gridiron Warrior/Deliverables/trash-review/`

## Step 1: Build the page

```bash
cd "D:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.build_review_page
```

Reads `queue-state.json`, selects every topic where a carousel exists AND
(`carousel_needs_polish` is true OR the topic is untriaged in `_inbox`/`ready`
and not yet `ready_to_ship`), and writes `review.html`. It never mutates
`queue-state.json`. Expected output: `Wrote .../review.html (N topic(s) pending review)`.

## Step 2: Open it

```bash
start "" "D:/Claude Projects/Gridiron Warrior/Deliverables/_system/review/review.html"
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

Parse the three buckets. `polish` entries may carry an optional
`:"note"` suffix (double-quoted, may contain commas, so split on the bracket
structure not naively on commas). Any bucket may be empty.

Apply each bucket with the SAME mechanisms the existing commands use. Run this
one script (it mirrors `/gw-ship` for ship, records the polish note, and mirrors
the `/gw-triage` kill convention by moving to `trash-review/`):

```bash
python - "$RESULT_STRING" <<'PY'
import json, re, shutil, sys, pathlib
raw = sys.argv[1]

DELIV = pathlib.Path("D:/Claude Projects/Gridiron Warrior/Deliverables")
STATE = DELIV / "queue-state.json"
TRASH = DELIV / "trash-review"

def bucket(name):
    m = re.search(name + r"=\[(.*?)\](?=\s+\w+=\[|\s*$)", raw)
    return m.group(1).strip() if m else ""

# ship / kill: plain comma-separated slugs
ship = [s.strip() for s in bucket("ship").split(",") if s.strip()]
kill = [s.strip() for s in bucket("kill").split(",") if s.strip()]

# polish: slug or slug:"note", note may contain commas -> parse with a regex
polish = {}
for m in re.finditer(r'([^,\[\]]+?)(?::"((?:[^"\\]|\\.)*)")?(?=,|$)', bucket("polish")):
    slug = m.group(1).strip()
    if not slug:
        continue
    polish[slug] = (m.group(2) or "").replace('\\"', '"')

data = json.loads(STATE.read_text(encoding="utf-8"))
topics = {t["slug"]: t for t in data["topics"]}
actions = []

# SHIP: mirror /gw-ship (ready_to_ship=True) and clear the polish flag
for slug in ship:
    t = topics.get(slug)
    if not t:
        actions.append(f"SKIP ship {slug} (not in state)"); continue
    t["ready_to_ship"] = True
    t["carousel_needs_polish"] = False
    actions.append(f"ship {slug} -> ready_to_ship=true")

# POLISH: keep the flag, stash the note on the topic entry
for slug, note in polish.items():
    t = topics.get(slug)
    if not t:
        actions.append(f"SKIP polish {slug} (not in state)"); continue
    t["carousel_needs_polish"] = True
    if note:
        t["polish_note"] = note
    actions.append(f"polish {slug}" + (f' -> "{note}"' if note else ""))

# KILL: move folder to trash-review/ (mirror /gw-triage's kill, non-destructive)
TRASH.mkdir(parents=True, exist_ok=True)
for slug in kill:
    t = topics.get(slug)
    if not t:
        actions.append(f"SKIP kill {slug} (not in state)"); continue
    src = DELIV / t["folder"]
    if not src.exists():
        actions.append(f"SKIP kill {slug} (folder gone)"); continue
    dst = TRASH / src.name
    # dedup collision the way trash-review already does (suffix)
    if dst.exists():
        dst = TRASH / (src.name + "__review")
    shutil.move(str(src), str(dst))
    t["stage"] = "trash-review"
    actions.append(f"kill {slug} -> trash-review/{dst.name}")

STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n".join(actions) if actions else "no decisions to apply")
PY
```

Pass the pasted string as `$RESULT_STRING` (the whole line, including the
`gw-review-result:` prefix - the regex ignores the prefix).

## Step 4: Re-scan and report

Kills moved folders on disk, so refresh the queue:

```bash
cd "D:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.scan_folders
```

Print a summary:

```
Applied review:
  ship:   <n>  (ready_to_ship flipped - run /gw-queue to push to Drive)
  polish: <n>  (notes recorded on the topic)
  kill:   <n>  (moved to trash-review/)
```

Then recommend: shipped topics need `/gw-queue` to sync to Drive; polish topics
go back to the carousel builder with their `polish_note`.

## Step 5: Commit (optional, ask first)

If Scott wants it committed:

```bash
cd "D:/Claude Projects"
git add -A
git commit -m "review: apply carousel decisions (<n> ship, <n> polish, <n> kill)"
```

## Voice

Mechanical status output. Any recommendation stays in Scott's tone: short,
direct, no em-dashes.
