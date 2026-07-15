---
name: gw-queue
model: sonnet
description: "Refresh queue-state.json by scanning the Deliverables folder tree, optionally trigger Drive sync for ready_to_ship topics, and print a 'what's new in inbox' report. Auto-deploys the dashboard via Netlify CLI when state changes."
---

# GW Queue — Refresh queue-state.json and report inbox status

Scan the Deliverables folder tree, refresh `queue-state.json`, optionally trigger
Drive sync for ready topics that need it, and print a "what's new in inbox"
report.

## Paths

- **Deliverables:** `C:/Claude Projects/Gridiron Warrior/Deliverables/`
- **Scanner module:** `scripts.gwqueue.scan_folders`
- **State file:** `C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json`
- **Dashboard state copy:** `C:/Claude Projects/websites/scottleechtraining.com/tools/queue/queue-state.json` (Phase 9+)

## Step 0: Apply any pending stage mutations from dashboard exports

Phase 11 adds an `apply_state.py` script. Until then, this step is a no-op.

If `scripts/gwqueue/apply_state.py` exists, run it:

```bash
cd "C:/Claude Projects/Gridiron Warrior"
if [ -f "scripts/gwqueue/apply_state.py" ]; then
  python -m scripts.gwqueue.apply_state
else
  echo "apply_state.py not yet implemented (Phase 11); skipping"
fi
```

## Step 1: Capture the prior state for diff

Read the current `queue-state.json` (BEFORE re-scanning) to capture the slugs in `_inbox` so we can detect new arrivals.

```bash
python -c "
import json, pathlib
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
if p.exists():
    data = json.loads(p.read_text(encoding='utf-8'))
    inbox_slugs = sorted([t['slug'] for t in data.get('topics', []) if t.get('stage') == '_inbox'])
    print('PRIOR_INBOX:', ','.join(inbox_slugs))
else:
    print('PRIOR_INBOX:')
"
```

Remember this list (call it `prior_inbox`).

## Step 2: Run the scanner

```bash
cd "C:/Claude Projects/Gridiron Warrior"
python -m scripts.gwqueue.scan_folders
```

Expected output: `Scanned N topics. Wrote .../queue-state.json.`

## Step 3: Render carousel slides + split captions (skipped until Phase 6+7)

```bash
cd "C:/Claude Projects/Gridiron Warrior"
if [ -f "scripts/gwqueue/render_carousel.py" ]; then
  python -m scripts.gwqueue.render_carousel
else
  echo "render_carousel.py not yet implemented (Phase 6); skipping slide rendering"
fi

if [ -f "scripts/gwqueue/split_captions.py" ]; then
  python -m scripts.gwqueue.split_captions
else
  echo "split_captions.py not yet implemented (Phase 7); skipping caption split"
fi
```

## Step 4: Drive sync (skipped until Phase 8)

```bash
cd "C:/Claude Projects/Gridiron Warrior"
if [ -f "scripts/gwqueue/sync_to_drive.py" ]; then
  python -m scripts.gwqueue.sync_to_drive
  # Re-run scanner to pick up drive_folder_id updates
  python -m scripts.gwqueue.scan_folders
else
  echo "sync_to_drive.py not yet implemented (Phase 8); skipping Drive sync"
fi
```

## Step 4.5: Retire topics Scott dragged to `used` on Drive (Drive -> local)

The contract: when Scott drags a topic folder into the `used` subfolder under
`GW Posting Queue` on Drive (or trashes it), that retires the topic locally.

```bash
cd "C:/Claude Projects/Gridiron Warrior"
if [ -f "scripts/gwqueue/retire_from_drive.py" ]; then
  python -m scripts.gwqueue.retire_from_drive
  # Re-scan to reflect the archived stage changes in queue-state.json
  python -m scripts.gwqueue.scan_folders
fi
```

## Step 5: Read fresh state and build the report

```bash
python -c "
import json, pathlib
p = pathlib.Path('C:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
topics = data['topics']

by_stage = {}
for t in topics:
    by_stage.setdefault(t['stage'], []).append(t)

print()
print('=' * 50)
print(f\"GW Queue refreshed - {data['generated'][:19].replace('T', ' ')}\")
print('=' * 50)

# Inbox section
inbox = by_stage.get('_inbox', [])
print()
print(f'Inbox: {len(inbox)} untriaged')
for t in inbox:
    print(f\"  - {t['slug']}\")

# Ready section ranked by squeeze
ready = by_stage.get('ready', [])
def squeeze_count(t):
    return sum(1 for c in t['channels'].values() if c.get('state') in ('posted', 'skip'))
ready.sort(key=lambda t: (-squeeze_count(t), t.get('last_activity', '')))

print()
print(f'Ready: {len(ready)} topics')
print('  Up Next (most-squeezed first):')
for t in ready[:5]:
    settled = squeeze_count(t)
    total = len(t['channels'])
    polish = ' [needs polish]' if t.get('carousel_needs_polish') else ''
    print(f\"    - {t['slug']} ({settled}/{total}{polish})\")

# Cold and archived counts
print()
print(f\"Cold storage: {len(by_stage.get('cold-storage', []))} topics\")
print(f\"Archived: {len(by_stage.get('archived', []))} topics\")
print()
"
```

## Step 6: Identify new inbox topics

Compare current inbox slugs against `prior_inbox` from Step 1. Any new slug in inbox now that wasn't there before is a new arrival worth flagging.

If new inbox topics exist, print:
```
NEW IN INBOX (since last /gw-queue):
  - <slug-1>
  - <slug-2>

Run /gw-triage to sort.
```

## Step 7: Recommend next action

- If inbox is non-empty: "Run `/gw-triage` to sort inbox topics."
- If any ready topic has no channels posted in 14+ days (compare `last_activity` to today): print a "stale ready topics" callout.
- If everything is clean: "Queue is healthy. Open the dashboard to post: https://scottleechtraining.com/tools/queue/"

## Step 8: Auto-deploy the dashboard via Netlify CLI

The scottleechtraining.com site is deployed via Netlify CLI (API drops), NOT from git. So a `git push` does NOT trigger a redeploy. Use the Netlify CLI directly to push the local dashboard mirror live.

The CLI is already authenticated (`netlify status` to confirm). The site is linked to `scott-leech-training`.

Detect whether anything in the dashboard folder changed since the last deploy. If yes, deploy. If no, no-op.

> This autonomous `netlify deploy --prod` is the documented exception to the "nothing ships autonomously" rule (blessed by Scott 2026-07-14, audit 2026-07-14 finding P3). It only publishes the internal queue dashboard, which sits behind the queue-auth edge gate; it never touches public marketing pages.

```bash
cd "C:/Claude Projects/websites/scottleechtraining.com/tools/queue"

# Check if anything in the dashboard folder changed in the last 5 minutes
# (proxy for "did /gw-queue update the mirror?")
recent_changes=$(find . -type f -mmin -5 -not -path "./.*" 2>/dev/null | head -3)

if [ -z "$recent_changes" ]; then
  echo "No dashboard changes to deploy."
else
  echo "Dashboard changed. Deploying via Netlify CLI..."
  cd "C:/Claude Projects/websites/scottleechtraining.com"
  netlify deploy --prod --dir=. 2>&1 | tail -8
  echo ""
  echo "Deployed. Live dashboard should reflect changes within ~15s."
fi
```

This step ALWAYS runs after Steps 0-7, even if no Drive sync happened, because thumbnail or caption changes might still need to deploy.

**Note on git:** the scanner-mirrored files (`websites/scottleechtraining.com/tools/queue/queue-state.json`, `thumbs/`, `captions/`) DO end up in your git working tree as modified, but you don't need to commit them — the deploy is via CLI, not git. You can commit them separately when you next want to push a "checkpoint" to GitHub.

## Voice

Output should follow Scott's voice rules from `C:/Claude Projects/CLAUDE.md` when applicable. No em-dashes. Short. Direct. The status report itself is mechanical, not voice-driven — but any recommendations or warnings stay in Scott's tone (e.g., "Inbox is backing up. Triage tonight." beats "Your inbox has unaddressed items.").
