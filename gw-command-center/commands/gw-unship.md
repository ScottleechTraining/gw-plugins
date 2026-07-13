---
name: gw-unship
model: sonnet
description: "Take a Deliverables topic OFF the Drive sync list. Flips `ready_to_ship: false` so future /gw-queue runs skip syncing it. Existing Drive folder is not deleted automatically (manual cleanup if needed)."
---

# GW Unship — Take a topic OFF the Drive sync list

Flip `ready_to_ship: false`. Future /gw-queue runs will skip Drive sync for
this topic. Existing Drive folder is NOT deleted automatically (manual cleanup
if needed).

## Usage: $ARGUMENTS

Format: `<topic-slug-substring>`

Examples:
- `/gw-unship speed-work`
- `/gw-unship gassers`

## Step 1: Find the topic

```bash
python -c "
import json, pathlib, sys
slug_query = 'REPLACE_ME'
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
matches = [t for t in data['topics'] if slug_query.lower() in t['slug'].lower() and t['stage'] == 'ready']
if not matches:
    print(f'No ready topic matches \"{slug_query}\". Run /gw-queue to refresh.')
    sys.exit(1)
if len(matches) > 1:
    print('Multiple matches:')
    for t in matches:
        print(f'  - {t[\"slug\"]}')
    sys.exit(1)
print(matches[0]['slug'])
"
```

If no match or multiple matches, stop and report. Otherwise, continue with the matched slug.

## Step 2: Flip the flag

```bash
python -c "
import json, pathlib
slug = 'EXACT_SLUG'
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
topic = next(t for t in data['topics'] if t['slug'] == slug)
topic['ready_to_ship'] = False
p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Marked {slug} ready_to_ship=false')
"
```

## Step 3: Confirm and offer next action

```
Marked <slug> ready_to_ship=false.
Drive sync will skip this topic going forward.
Note: existing files at GW Posting Queue/<slug>/ on Drive are NOT auto-deleted.
```
