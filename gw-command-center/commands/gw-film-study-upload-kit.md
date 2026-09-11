---
name: gw-film-study-upload-kit
model: claude-opus-5
description: "Film Study upload kit - YouTube URL in, transcript filed + Thinkific post copy + wiki ingest out. Phone-to-YouTube phase 2 flow. No freebie link, no email, no commit, no posting."
---

# /gw-film-study-upload-kit <youtube-url> [topic] — Film Study Upload Kit

Phase 2 companion to `/gw-film-study-brief`. Scott films the weekly Film Study on his phone, uploads it to YouTube as **unlisted**, then runs this command with the URL. It pulls the transcript, files it in the Voice Corpus, writes the copy-paste upload kit (YouTube + Thinkific post), and runs the wiki ingest the locked cadence requires.

**By design (per Scott 2026-08-26): NO freebie link in the post copy.** Do not add one, do not suggest one in the output file.

**What it does NOT do:** post to Thinkific, publish anything on YouTube, email, commit, push, or schedule. Scott pastes the copy himself.

## Arguments: $ARGUMENTS

- First token: the YouTube URL (required — abort with usage message if missing).
- Rest: optional topic override.

## Paths

- **Transcript script:** `C:\Claude Projects\Gridiron Warrior\scripts\yt_transcript.py`
- **Transcript destination:** `C:\Claude Projects\Gridiron Warrior\Voice Corpus\Course Transcripts\Weekly Film Study\YYYY-MM-DD-<topic-slug>.md`
- **Upload kit output:** `Deliverables/<stage>/<topic-slug>/UPLOAD-KIT.md` (existing topic folder in `_inbox/` or `ready/`; create `_inbox/<topic-slug>/` if none exists)
- **Wiki summary:** `wiki/summaries/film-study-<topic-slug>.md`
- **Wiki log:** `wiki/log.md` (append one line)

Slug rules: kebab-case, truncate to 50 chars, strip special chars.

## Step 1 — Pull the transcript

```bash
python "C:\Claude Projects\Gridiron Warrior\scripts\yt_transcript.py" "<url>" "<scratchpad>/transcript.md"
```

The output has frontmatter (title, duration, upload_date) and `[MM:SS]` markers about once a minute. If the script exits with "No English subtitles found", tell Scott to wait a few minutes for YouTube auto-captions to finish processing and stop. Do not fabricate a transcript.

## Step 2 — Resolve the topic slug

1. If a topic argument was given: slug it. Done.
2. Else: match the video title against existing `wiki/summaries/film-study-*.md` pages and topic folders in `Deliverables/_inbox/` and `Deliverables/ready/`. A clear single match wins (this links the kit to the brief-chain artifacts already produced for that topic).
3. Else: derive the slug from the video title.
4. If the match is ambiguous (two plausible folders), ask Scott. He is at the terminal — this command is manual-only.

## Step 3 — File the transcript

Copy the transcript to `Voice Corpus\Course Transcripts\Weekly Film Study\YYYY-MM-DD-<topic-slug>.md` (date = today). Keep the script's frontmatter and add `topic_slug: <topic-slug>`. This is Scott's own recorded teaching: voice-input safe, immutable once filed.

## Step 4 — Write UPLOAD-KIT.md

Read the transcript. Write `UPLOAD-KIT.md` into the topic's Deliverables folder. Voice rules from CLAUDE.md apply in full: Scott's voice, short sentences, no em-dashes, no banned words.

Structure (follow the podcast upload-kit house style, e.g. `Deliverables/ready/podcast-cyrus-baetz/UPLOAD-KIT.md`):

```markdown
# Film Study Upload Kit — [topic] — YYYY-MM-DD

Video: <url> (UNLISTED — confirm before sharing)
Transcript: <voice corpus path>
Chapters read off the transcript's [MM:SS] markers. If the upload got trimmed, nudge every chapter by the same offset.

Copy-paste everything below.

---

## YOUTUBE (visibility: UNLISTED)

**Title:**
[Coach-facing title. The teaching claim, not the topic label.]

**Description:**
[2-4 sentences. What the Film Study teaches and who it is for.]

CHAPTERS
0:00 [chapter]
[3-8 chapters total, from the transcript's actual teaching beats]

---

## THINKIFIC — Weekly Film Study space

**Post title:**
[Same claim, community-facing.]

**Post body:**
[3-6 sentences in Scott's voice. What this week's Film Study covers, the one thing to steal from it, then the watch link. End with a question to the room to drive replies. NO freebie link.]

WATCH: <url>

[chapter list repeated]
```

## Step 5 — Wiki ingest

Follow the vault CLAUDE.md ingest workflow, with the fact-density rule (pull every number the transcript states):

1. If `wiki/summaries/film-study-<topic-slug>.md` exists from a pre-recording brief run: flip it to published state. Add the transcript path as source, set `external_origin: false` (Scott's own recorded teaching), refresh takeaways from what he ACTUALLY said on camera.
2. If no summary exists: create one per the ingest workflow (summary + index line).
3. Append one line to `wiki/log.md`:

```
YYYY-MM-DD /gw-film-study-upload-kit: [topic-slug] (transcript filed, kit written, summary: flipped|created, forge: ok|skipped-exists)
```

## Step 6 — Content pack (skip if the brief chain already made one)

- If a `*content-pack*.md` already exists in the topic's Deliverables folder (the `/gw-film-study-brief` chain produced it): skip. Log `forge: skipped-exists`.
- Else: invoke `/gw-content-forge "<transcript path>"` per the locked cadence rule (every transcript through Content Forge, every time).

## Step 7 — Report to Scott

1. Transcript path + duration.
2. UPLOAD-KIT.md path.
3. Wiki summary: flipped or created.
4. Content pack: path, or "already existed from brief chain".
5. Reminder: "Video stays unlisted. Paste the Thinkific post yourself. Nothing was committed or sent."

Keep it tight.

## Hard rules

- NO freebie link anywhere in the output. Scott's explicit call, 2026-08-26.
- No email, no Kit, no commit, no push, no posting to Thinkific or anywhere else.
- Never fabricate transcript content. Auto-captions missing = stop and say so.
- Auto-caption text is imperfect. Quote it for ingest, but never publish raw caption lines as polished copy without cleanup.
- No em-dashes. No banned words from CLAUDE.md.
