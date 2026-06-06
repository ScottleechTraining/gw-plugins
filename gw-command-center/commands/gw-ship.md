# GW Ship — Mark a topic ready for Drive sync

Flip `ready_to_ship: true` on a topic so the next `/gw-queue` run pushes its
slides and captions to Google Drive. Until this flag is true, the topic stays
local-only — slides and captions are rendered/split locally so you can preview
them, but nothing leaves the laptop.

## Usage: $ARGUMENTS

Format: `<topic-slug-substring>`

Examples:
- `/gw-ship speed-work`
- `/gw-ship tri-set-structure-summer-install`
- `/gw-ship gassers`

## Step 1: Find the topic

```bash
python -c "
import json, pathlib, sys
slug_query = 'REPLACE_ME'
p = pathlib.Path('D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
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
p = pathlib.Path('D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
topic = next(t for t in data['topics'] if t['slug'] == slug)
topic['ready_to_ship'] = True
p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'Marked {slug} ready_to_ship=true')
"
```

## Step 3: Confirm and offer next action

```
Marked <slug> ready_to_ship=true.
Next /gw-queue run will push slides + captions to Drive.
Run /gw-queue now to push immediately.
```
