---
description: Evening ritual — pull cloud results, process screenshots + voice notes, report
---

# /gw-daily — Scott's 8pm Evening Ritual

Run this every weekday evening when you fire up Claude Code. Catches up on everything from the day.

## Steps

### 1. Sync the vault Git repo

```bash
cd "D:\Claude Projects\Gridiron Warrior" && git pull --rebase
```

Report any conflicts. Do not auto-resolve — surface to Scott.

### 2. Sweep Screenshot Inbox

Check `D:\Claude Projects\Gridiron Warrior\External Library\Screenshots\inbox\` for new images.

For each image:
- OCR via Read tool (multi-modal)
- Classify as: `coaching` / `business` / `ai` / `personal-skip`
- If not personal-skip:
  - Write a markdown note in `External Library\Screenshots\processed\[domain]\YYYY-MM-DD-HHMMSS-[slug].md`
  - Note includes: source frontmatter (`type: screenshot`, `captured: <date>`, `domain: <coaching|business|ai>`, `wiki_links: [...]`), OCR'd text, GW relevance ("Could feed:" suggestions), wikilinks where matches exist
  - Move original image to `External Library\Screenshots\archive\YYYY-MM\` (mkdir if missing)
- If personal-skip: move to archive without writing a note

Report counts: `N processed, M skipped, K skipped-personal`.

### 3. Sweep Voice Note Inbox

Check `D:\Claude Projects\Gridiron Warrior\Voice Corpus\_pocket-inbox\` for new files.

For each file:
- If audio (.mp3, .m4a, .wav, .ogg): transcribe via best available method (Whisper API if configured; otherwise flag for Scott)
- If transcript (.txt, .md): read as-is
- Extract topic from first 1-2 sentences, slug it kebab-case
- Write to `Voice Corpus\Voice Notes\YYYY-MM-DD-[topic-slug].md`
  - Frontmatter: `type: voice-note`, `source: pocket`, `voice: scott-original`, `recorded: <date>`, `topic: <slug>`, `tags: [voice-note, scott-original, <domain>]`
  - Body: VERBATIM transcript. Do not polish, smooth, or rewrite.
  - Below transcript add `## Concepts mentioned` with detected wikilinks (optional, light touch)
- Move original to `Voice Corpus\_pocket-inbox\.processed\YYYY-MM\` (mkdir if missing)

Report count: `N voice notes processed`.

### 4. Read Today's Daily Seed

Read `D:\Claude Projects\Gridiron Warrior\Deliverables\_daily-seeds\YYYY-MM-DD.md` (today's date) and present its content angles to Scott.

If file missing: report "No seed file today — `/gw-seed-writer` did not fire (laptop may have been closed). Want me to run it now?"

### 5. Surface Queue Status + Anomalies

Check:
- `External Library\BusinessDocuments\_topic-queue.md` — count active topics. If < 5: warn.
- `External Library\AI\_topic-queue.md` — count active topics. If < 5: warn.
- Any new error logs in `wiki\log.md`
- Pending `External Library\_promotion-candidates.md` items

### 6. Final Report Format

Use this exact format:

```
GW DAILY — YYYY-MM-DD
─────────────────────
GIT SYNC      : <ok / conflicts>
SCREENSHOTS   : N processed (coaching: X, business: Y, ai: Z), M personal-skipped
VOICE NOTES   : N processed
SEED FILE     : <present / missing>
QUEUES        : Business: N | AI: M  (warn if either < 5)
ATTENTION     : <bullet list of anything Scott should look at, or "nothing">

TODAY'S SEED ANGLES:
<paste the angles from today's seed file here, formatted for quick scan>
```

## Notes

- This command should complete in under 5 minutes
- Do NOT auto-publish anything
- If anything is ambiguous, default to surfacing it for Scott rather than guessing
