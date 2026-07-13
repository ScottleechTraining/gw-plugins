---
name: gw-review
model: opus
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

Parse the three buckets. `polish` entries may carry an optional
`:"note"` suffix (double-quoted, may contain commas, so split on the bracket
structure not naively on commas). Any bucket may be empty.

Apply each bucket with the SAME mechanisms the existing commands use. Run this
one script (it mirrors `/gw-ship` for ship, records the polish note, and kills
by moving the folder to the terminal `killed/` folder):

```bash
python - "$RESULT_STRING" <<'PY'
import json, re, shutil, sys, pathlib
raw = sys.argv[1]

DELIV = pathlib.Path("C:/Claude Projects/Gridiron Warrior/Deliverables")
STATE = DELIV / "queue-state.json"
KILLED = DELIV / "killed"

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

# SHIP: mirror /gw-ship atomically - move _inbox topics into ready/, flip the
# flag, clear any polish note. Folder contract: ready/ only holds approved,
# Drive-synced topics (the per-slug Drive sync runs right after this script).
for slug in ship:
    t = topics.get(slug)
    if not t:
        actions.append(f"SKIP ship {slug} (not in state)"); continue
    if t["stage"] == "_inbox":
        src = DELIV / t["folder"]
        dst = DELIV / "ready" / src.name
        if dst.exists():
            actions.append(f"SKIP ship {slug} (ready/{src.name} already exists)"); continue
        shutil.move(str(src), str(dst))
        t["stage"] = "ready"
        t["folder"] = f"ready/{src.name}"
    t["ready_to_ship"] = True
    t["carousel_needs_polish"] = False
    t["polish_note"] = None
    actions.append(f"ship {slug} -> ready/, ready_to_ship=true")

# POLISH: keep the flag, stash the note on the topic entry
for slug, note in polish.items():
    t = topics.get(slug)
    if not t:
        actions.append(f"SKIP polish {slug} (not in state)"); continue
    t["carousel_needs_polish"] = True
    if note:
        t["polish_note"] = note
    actions.append(f"polish {slug}" + (f' -> "{note}"' if note else ""))

# KILL: move folder to the terminal killed/ folder. killed/ is never scanned,
# so the entry drops out of state on the next scan (no stage write needed, no
# restore path). This is a one-way door - to run the idea again, start fresh
# through the forge (per the novelty rules).
KILLED.mkdir(parents=True, exist_ok=True)
for slug in kill:
    t = topics.get(slug)
    if not t:
        actions.append(f"SKIP kill {slug} (not in state)"); continue
    src = DELIV / t["folder"]
    if not src.exists():
        actions.append(f"SKIP kill {slug} (folder gone)"); continue
    dst = KILLED / src.name
    # dedup collision (suffix)
    if dst.exists():
        dst = KILLED / (src.name + "__review")
    shutil.move(str(src), str(dst))
    actions.append(f"kill {slug} -> killed/{dst.name}")

STATE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n".join(actions) if actions else "no decisions to apply")
PY
```

Pass the pasted string as `$RESULT_STRING` (the whole line, including the
`gw-review-result:` prefix - the regex ignores the prefix).

## Step 4: Render, sync shipped topics to Drive, re-scan

Ships and kills moved folders on disk. Render/split (idempotent), then sync
EACH shipped slug so ready/ topics land on Drive immediately, then refresh:

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.render_carousel
python -m scripts.gwqueue.split_captions
# one per shipped slug:
python -m scripts.gwqueue.sync_to_drive --slug "EXACT_SLUG"
python -m scripts.gwqueue.scan_folders
```

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
