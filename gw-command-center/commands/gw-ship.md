---
name: gw-ship
model: sonnet
description: "Ship a Deliverables topic in one atomic step: move it to ready/ (if still in _inbox), flip ready_to_ship, render slides, split captions, and sync it to Google Drive immediately. After this command the topic IS on Drive - no separate /gw-queue run needed. The folder contract: ready/ only ever contains approved, Drive-synced topics."
---

# GW Ship — Approve + move + sync, one step

The folder contract (non-negotiable): shipping approves a topic, moves it into
`ready/`, and immediately attempts Drive sync. Fix-me work stays in `_inbox`.
`/gw-ship` and SHIP decisions in `/gw-review` share the approval path for
new-format carousels. A local approval is not proof of a successful upload.

## Usage: $ARGUMENTS

Format: `<topic-slug-substring>` (one or more, space-separated)

Examples:
- `/gw-ship speed-work`
- `/gw-ship gassers hell-week power-clean`

## Step 1: Find each topic

Match the substring against `queue-state.json` topics in stage `_inbox` OR
`ready` (case-insensitive). If no match or multiple matches for a substring,
stop and report that substring; process the rest.

```bash
python -c "
import json, pathlib, sys
slug_query = 'REPLACE_ME'
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
matches = [t for t in data['topics'] if slug_query.lower() in t['slug'].lower() and t['stage'] in ('_inbox', 'ready')]
if not matches:
    print(f'No _inbox/ready topic matches \"{slug_query}\". Run /gw-queue to refresh.')
    sys.exit(1)
if len(matches) > 1:
    print('Multiple matches:')
    for t in matches:
        print(f'  - {t[\"slug\"]} ({t[\"stage\"]})')
    sys.exit(1)
print(matches[0]['slug'], matches[0]['stage'], matches[0]['folder'])
"
```

## Step 2: Guard — do not ship broken work

If the topic has `carousel_missing: true`, stop: "No carousel built yet."
If `carousel_needs_polish: true`, warn Scott and ask before proceeding (the
HTML still has an empty photo placeholder slot).

**New-format branch:** detect the explicit schema marker and follow
[copy-record.md](../skills/ig-carousel/references/copy-record.md), including its
capability gate. No marker means the legacy path below, unchanged. Never remove
a marker, migrate a legacy deck, or downgrade a marked topic when helpers are
missing. Report that topic and continue other eligible topics.

For new-format topics, prepare the selected variant and stage its exact outputs
for review first. A general ship request does not approve newly generated or
changed outputs:

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.render_carousel
python -m scripts.gwqueue.split_captions
python -m scripts.gwqueue.carousel_package review TOPIC
```

Replace TOPIC with the resolved topic folder and EXACT_SLUG with its unique slug.
The `review TOPIC` CLI invokes `stage_review` to snapshot exact current outputs
in `carousel-review.json`, NOT approval. `validate TOPIC` is read-only and cannot
substitute for staging review. For multiple topics, prepare all intended outputs
before snapshotting/approving any so a later broad render pass cannot stale an
earlier receipt. Stop that topic on any failure.

The CLI prints a Review token. Preserve that exact SHA256 token with this topic's
paired outputs; do not regenerate or replace it after Scott's review.

SHOW the rendered deck, its paired caption, and that token to Scott and obtain
approval, or honor his explicit approval of those exact unchanged outputs and
their retained token. Only then run:

```bash
python -m scripts.gwqueue.apply_review "gw-review-result: ship=[EXACT_SLUG] polish=[] kill=[] review=[EXACT_SLUG:SHA256TOKEN]"
```

Replace SHA256TOKEN with the original printed Review token shown with the paired
outputs. Preserve one matching review entry per managed SHIP in a batch; legacy
paste format remains unchanged and requires no token.

The applier refuses managed SHIP for a missing/mismatched review token or if
source HTML, PNGs, or caption changed since the snapshot. A stale-review block
requires current outputs to be staged, shown with their new token, and approved
again; never refresh the snapshot or regenerate a token to replay an old approval.
On success it seals `carousel-package.json` and handles approval/state/move.
State POLISH invalidates managed approvals and sets `ready_to_ship=false`.
After success, skip Steps 3 and 4 and continue at Step 5. Never run the legacy
state-edit snippet for a marked topic or create the receipt manually. An action
reroll must be reviewed again before this approval.

## Step 3: Move to ready/ (if in _inbox)

Legacy topics only. New-format topics use the applier above.

```bash
python -c "
import json, pathlib, shutil
slug = 'EXACT_SLUG'
DEL = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables')
p = DEL / 'queue-state.json'
data = json.loads(p.read_text(encoding='utf-8'))
topic = next(t for t in data['topics'] if t['slug'] == slug)
src = DEL / topic['folder']
if topic['stage'] == '_inbox':
    dst = DEL / 'ready' / src.name
    if dst.exists():
        raise SystemExit(f'ready/{src.name} already exists - resolve manually')
    shutil.move(str(src), str(dst))
    topic['stage'] = 'ready'
    topic['folder'] = f'ready/{src.name}'
topic['ready_to_ship'] = True
topic['polish_note'] = None
p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'{slug}: stage=ready, ready_to_ship=true')
"
```

## Step 4: Render slides + split captions (idempotent)

Legacy-only post-approval preparation. In mixed batches, prepare legacy outputs
before the new-format approval phase too, and skip this broad pass afterward so
sealed outputs do not change.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.render_carousel
python -m scripts.gwqueue.split_captions
```

## Step 5: Sync THIS topic to Drive

Sync enforces the current new-format approval receipt. Missing or stale approval
must fail before upload; changed copy/caption/renders need preparation and renewed
approval, not an unmanaged retry. Legacy sync remains on its existing path.

Managed preflight checks render provenance and runs before remote calls. The
sync helper uploads the approved slide set, then removes surplus remote PNGs
only from that managed slide folder. It leaves non-PNG files and legacy folders
alone; do not replace this with broad or manual cleanup.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.sync_to_drive --slug "EXACT_SLUG"
```

## Step 6: Rescan and confirm

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.scan_folders
```

Confirm to Scott:

```
Shipped <slug>: in ready/, on Drive. Post from your phone whenever.
```

If the Drive sync fails (auth, network), say so plainly and leave the topic in
ready/ with `ready_to_ship: true` - the next /gw-queue run will retry the sync.
That is the only allowed state where a ready/ topic is briefly not on Drive.
