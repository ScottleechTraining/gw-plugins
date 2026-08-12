---
name: gw-daily
model: claude-opus-5
description: "Evening ritual - pull cloud results, process screenshots + voice notes, report"
---

# /gw-daily — Scott's 8pm Evening Ritual

Run this every weekday evening when you fire up Claude Code. Catches up on everything from the day.

## Steps

### 1. Sync the vault Git repo

```bash
cd "C:\Claude Projects\Gridiron Warrior" && git pull --rebase
```

Report any conflicts. Do not auto-resolve — surface to Scott.

### 2. Sweep Screenshot Inbox

Run `/gw-screenshot-ingest`. It owns `External Library\Screenshots\inbox\` and carries the full OCR / classify / file spec; do not re-implement any of it here. If the inbox is empty it reports zero and exits fast.

From its output, take the counts for the report block: `N processed, M skipped, K skipped-personal`.

### 3. Sweep Voice Note Inbox

Run `/gw-voice-ingest`. It owns `Voice Corpus\_pocket-inbox\` and carries the full transcribe / verbatim-file / wikilink spec; do not re-implement any of it here. If the inbox is empty it reports zero and exits fast.

From its output, take the count for the report block: `N voice notes processed`.

### 4. Read Today's Daily Seed

Read `C:\Claude Projects\Gridiron Warrior\Deliverables\_daily-seeds\YYYY-MM-DD.md` (today's date) and present its content angles to Scott.

If file missing: report "No seed file today — `/gw-seed-writer` did not fire (laptop may have been closed). Want me to run it now?"

### 5. Surface Queue Status + Anomalies

Check:
- Queue depths: run `python "C:\Claude Projects\Gridiron Warrior\scripts\queue_status.py"` and use its counts. If any < 5: warn. Do NOT Read the `_topic-queue.md` files to count topics: they are UTF-16LE and a raw read shows them as empty.
- Any new error logs in `wiki\log.md`
- Pending `External Library\_promotion-candidates.md` items

### 6. Final Report Format

Use this exact format:

```
GW DAILY: YYYY-MM-DD
─────────────────────
GIT SYNC      : <ok / conflicts>
SCREENSHOTS   : N processed (coaching: X, business: Y, ai: Z), M personal-skipped
VOICE NOTES   : N processed
SEED FILE     : <present / missing>
QUEUES        : Business: N | AI: M | S&C: K  (warn if any < 5)
ATTENTION     : <bullet list of anything Scott should look at, or "nothing">

TODAY'S SEED ANGLES:
<paste the angles from today's seed file here, formatted for quick scan>
```

## Notes

- Keep each screenshot and voice note to one pass. Do not re-read or re-summarize items already filed.
- Deliver steps 1-6 and the report block. Do not draft content, run a forge, or fix anything you surface: name it under ATTENTION and stop.
- Do NOT auto-publish anything
- If anything is ambiguous, default to surfacing it for Scott rather than guessing
