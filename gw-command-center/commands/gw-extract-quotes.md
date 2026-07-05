---
name: gw-extract-quotes
model: sonnet
description: "Pull teaching moments and Scott-voice quotes from a podcast, Film Study, or webinar transcript and write them to wiki/extracted/. Builds the second brain of Scott's voice corpus over time so future content can reuse his real lines. Accepts a transcript file path, speaker/topic reference, or nothing (lists 10 most recent transcripts)."
---

# GW Extract Quotes — Transcript → Wiki Quote Extraction

Pull teaching moments and Scott-voice quotes from a podcast, Film Study, or webinar transcript and write them to `wiki\extracted\`. This builds the second brain of Scott's voice corpus over time so future content can reuse his real lines.

## Source: $ARGUMENTS

The user provides one of:
- A file path to a transcript (`.docx`, `.txt`, `.md`) — usually under `Voice Corpus\` or `raw-sources\`
- A speaker or topic reference (e.g., "Murdock podcast", "the latest Film Study") — find the matching transcript file
- Nothing — in which case, list the 10 most recent transcript files in `Voice Corpus\Podcast Transcripts\` and `Voice Corpus\Course Transcripts\` and ask which to extract

## Vault Paths

- **Transcript sources:** `D:/Claude Projects/Gridiron Warrior/Voice Corpus/`, `D:/Claude Projects/Gridiron Warrior/raw-sources/`
- **Output:** `D:/Claude Projects/Gridiron Warrior/wiki/extracted/`
- **Voice rules:** `D:/Claude Projects/CLAUDE.md`
- **Wiki log:** `D:/Claude Projects/Gridiron Warrior/wiki/log.md`

## Step 1: Read the Transcript

If `.docx`, use the `docx` skill to extract text. If `.md` or `.txt`, read directly.

Identify the speaker(s). For podcasts, Scott is one of multiple speakers — extract HIS quotes specifically, not the guest's (unless the guest says something Scott explicitly endorses or builds on).

## Step 2: Apply the Voice Filter

Read voice rules from `CLAUDE.md`. The quotes you extract must match Scott's voice signature:

**KEEP quotes that have:**
- Short sentences, active verbs, plain language
- A teachable principle (not just commentary)
- Tough-love framing or coach-in-the-trenches tone
- A signature phrase (see CLAUDE.md "Signature Phrases" list) or one that fits the pattern
- Specific examples — names of players, schools, drills, numbers
- A pop culture reference, story moment, or analogy

**SKIP:**
- Filler ("yeah, totally," "for sure," "right")
- Pleasantries and intros
- Banned words (delve, leverage, unlock, etc. — full list in CLAUDE.md)
- Anything with em-dashes (Scott's hard rule)
- Generic motivational lines that don't teach anything

## Step 3: Categorize What You Pull

Sort extracted material into three categories:

1. **Teaching moments** — passages where Scott explains a concept or principle. 2-5 sentences each. These become the bones of future content packs and Substacks.
2. **Quotable lines** — single-sentence punchy lines. These become Instagram quote-cards, Twitter hook tweets, email subject lines.
3. **Signature phrases (new)** — any line that has the pattern of Scott's known signature phrases but isn't on the existing list. Flag these so they can be added to CLAUDE.md.

Aim for: 5-10 teaching moments, 8-15 quotable lines, 0-3 signature candidates per transcript.

## Step 4: Write the Extract Page

Path: `wiki/extracted/[source-slug]-quotes.md`

`[source-slug]` rule: speaker-last-name + episode/topic descriptor, kebab-case. Examples:
- `Gridiron Warrior Podcast - Mike Serricchio.docx` → `serricchio-podcast-quotes.md`
- `Weekly Film Study - 2026-05-07-jumps-by-force-vector.txt` → `film-study-jumps-by-force-vector-quotes.md`

```markdown
---
title: Quote Extract — [Source Title]
type: extracted
source: [relative path to source file]
speaker: Scott Leech
date_recorded: [YYYY-MM-DD if known from source]
date_extracted: [YYYY-MM-DD today]
tags: [infer 2-3 tags: topic + format (podcast/film-study/webinar)]
pipeline: gw-extract-quotes
---

# Quote Extract: [Source Title]

**Source:** `[relative path]`
**Speaker:** Scott Leech
**Recorded:** [YYYY-MM-DD or "unknown"]
**Extracted:** [YYYY-MM-DD]

## Teaching Moments

### [Short topic label]

> [Multi-sentence passage in Scott's voice. Preserve his exact words. No em-dashes.]

**Why it's useful:** [1 sentence — what kind of content this fuels: email hook, carousel teaching slide, Substack section opener]

---

(repeat for each teaching moment, 5-10 total)

## Quotable Lines

> [Single sentence quote]

> [Single sentence quote]

(repeat — 8-15 total. Format as standalone blockquotes for easy copy-paste.)

## Signature Phrase Candidates

- "[exact phrase]" — [why it fits the pattern of his existing signatures]
- (only if any are flagged in Step 3. Otherwise omit this section.)

## Concepts Touched

- [[concepts/[slug]]] — if Scott references an existing wiki concept
- (flag new ones to back-fill)

## Entities Touched

- [[entities/[slug]]] — people, schools, products mentioned
```

## Step 5: Update Wiki Log

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] extract | [source-slug] — [N teaching moments, M quotable lines] via gw-extract-quotes
```

## Step 6: Flag Signature Candidates

If Step 3 found any new signature phrase candidates, surface them in the report. Scott can decide whether to add them to CLAUDE.md's "Signature Phrases" list.

## Step 7: Report

Tell Scott:
1. Extract file path
2. Counts: N teaching moments, M quotable lines, X signature candidates
3. The strongest single quote pulled — paste it inline so Scott can verify it
4. Any wiki concepts that got referenced but don't have pages yet (back-fill candidates)
5. If a signature candidate was flagged, prompt: "Add `[phrase]` to CLAUDE.md signature phrases? Y/N"

## Error Handling

- If `.docx` extraction fails, note the error and ask Scott to manually paste a section.
- If the transcript appears to be entirely a guest speaking (Scott silent), report: "This transcript reads as primarily [Guest Name]'s voice. Skip Scott-voice extraction, or extract the guest's quotes separately?"
- If the source has zero usable quotes after voice filtering, don't write an empty file — report "No quotes met the voice filter" and stop.
