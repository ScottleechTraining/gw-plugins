---
name: gw-ship
description: "Ship a Deliverables topic in one atomic step: move it to ready/ (if still in _inbox), flip ready_to_ship, render slides, split captions, and sync it to Google Drive immediately. After this command the topic IS on Drive - no separate /gw-queue run needed. The folder contract: ready/ only ever contains approved, Drive-synced topics."
---

# GW Ship — Approve + move + sync, one step

The folder contract (non-negotiable): a topic is only allowed into `ready/`
at the moment it is approved AND synced to Drive. Fix-me work stays in
`_inbox`. `/gw-ship` is the only door into `ready/`, and it does everything
in one shot so the folder itself is the truth.

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
p = pathlib.Path('D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
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

## Step 3: Move to ready/ (if in _inbox)

```bash
python -c "
import json, pathlib, shutil
slug = 'EXACT_SLUG'
DEL = pathlib.Path('D:/Claude Projects/Gridiron Warrior/Deliverables')
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

```bash
cd "D:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.render_carousel
python -m scripts.gwqueue.split_captions
```

## Step 5: Sync THIS topic to Drive

```bash
cd "D:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.sync_to_drive --slug "EXACT_SLUG"
```

## Step 6: Rescan and confirm

```bash
cd "D:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.scan_folders
```

Confirm to Scott:

```
Shipped <slug>: in ready/, on Drive. Post from your phone whenever.
```

If the Drive sync fails (auth, network), say so plainly and leave the topic in
ready/ with `ready_to_ship: true` - the next /gw-queue run will retry the sync.
That is the only allowed state where a ready/ topic is briefly not on Drive.
