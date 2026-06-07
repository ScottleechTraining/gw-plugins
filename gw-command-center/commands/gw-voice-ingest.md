---
name: gw-voice-ingest
description: "Process voice notes from Pocket - transcribe, verbatim file, wikilink"
---

# /gw-voice-ingest — Voice Note Processing

Processes voice notes from `Voice Corpus\_pocket-inbox\`. These are Scott's first-person voice — PRESERVE VERBATIM.

## Steps

### 1. Find files in inbox

```bash
ls "D:\Claude Projects\Gridiron Warrior\Voice Corpus\_pocket-inbox\"
```

Filter to: `.mp3`, `.m4a`, `.wav`, `.ogg`, `.txt`, `.md`. Skip `.processed/` subfolder.

### 2. Per file

**If audio:**
- Transcribe via Whisper (OpenAI API) or fallback (flag if no transcription service available)
- If transcription fails, write a stub note flagging for Scott

**If transcript text:**
- Read as-is

### 3. Parse + write

Extract topic from first 1-2 sentences. Slug kebab-case. Date the file by recording time (file mtime) or today if unknown.

Write to `Voice Corpus\Voice Notes\YYYY-MM-DD-[topic-slug].md`:

```markdown
---
title: "[Topic from first sentence, max 60 chars]"
tags: [voice-note, scott-original, <domain>]
type: voice-note
source: pocket
voice: scott-original
recorded: YYYY-MM-DD
topic: [topic-slug]
duration: <if audio, in seconds>
---

# [Topic]

<VERBATIM transcript. Do NOT polish. Do NOT smooth. Do NOT rewrite.>

## Concepts mentioned

<light-touch wikilinks where Scott explicitly names a concept (e.g. "Insiders", "Contact Prep", "violence is a skill") — do not force linkage>
```

### 4. Move original

Move source file to `Voice Corpus\_pocket-inbox\.processed\YYYY-MM\<original-filename>`. Mkdir if missing.

### 5. Append to log

```
2026-MM-DD /gw-voice-ingest: N voice notes processed
```

Do NOT run `git commit`. The `gw-daily-closeout` job commits all approved daily-output paths once, after the morning digest, via `scripts/git_safe_commit.py`. This skill's job ends at writing files and the wiki/log.md line.

### 6. Print the completion marker (ALWAYS last)

As the very last line of your output, print EXACTLY:

```
GW-DONE: voice-ingest
```

Print it whether you processed notes or there were none to process. The only time it must NOT appear is if you crashed before finishing. `run_job.py` validates on this marker — without it the gate is recorded `failed (artifact_invalid)` and rerun, even though exit code was 0.

## Critical rules

- **VERBATIM PRESERVATION.** This is Scott's voice corpus. If Scott says "and uh you know like the thing about it is" — you keep that. The rough edges ARE the voice signal.
- Do NOT add commentary, interpretation, or "summary" to the body. Just the transcript.
- Concept wikilinks are light-touch — only when Scott explicitly names something.
- If transcription fails: stub with `transcription_status: failed` and flag in `/gw-daily` report.

## Open question for Scott

What audio export format does Pocket produce? Confirm `.m4a` (most likely) or other. Update file extension filter if different.
