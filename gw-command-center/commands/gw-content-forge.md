---
name: gw-content-forge
description: "Transform any source material into a full content pack - 2 Twitter threads, 2 Instagram carousel drafts, and 1 email draft in Scott Leech's voice. Accepts a file path, topic name, Second Brain reference, or nothing (defaults to most recent research brief). Use when Scott says 'content forge', 'run the forge', or wants social content from any GW source."
---

# GW Content Forge

Transform any source material into a full content pack: 2 Twitter threads, 2 Instagram carousel drafts, and 1 email draft. All in Scott Leech's voice.

## Accepted input: $ARGUMENTS

The user will provide one of these as $ARGUMENTS:
- **A file path** to any file in the vault (transcript, brief, Film Study doc, pitch doc, etc.)
- **A topic name** (e.g., "contact prep", "box squats") and you find the relevant files
- **A reference to a Second Brain file** (e.g., "the contact prep transcript", "the GW2 transcript")
- **Nothing** — in which case, check `Research/NotebookLM/` for the most recently created brief

## Vault Paths

- **Wiki:** `D:/Claude Projects/Gridiron Warrior/wiki/`
- **Wiki index:** `D:/Claude Projects/Gridiron Warrior/wiki/index.md`
- **Wiki summaries:** `D:/Claude Projects/Gridiron Warrior/wiki/summaries/`
- **Wiki log:** `D:/Claude Projects/Gridiron Warrior/wiki/log.md`
- **Wiki business domain:** `D:/Claude Projects/Gridiron Warrior/wiki/business/`
- **Wiki AI domain:** `D:/Claude Projects/Gridiron Warrior/wiki/ai/`
- **Second Brain:** `D:/Claude Projects/Gridiron Warrior/Second Brain/`
- **Research briefs (S&C):** `D:/Claude Projects/Gridiron Warrior/Research/NotebookLM/`
- **Business research briefs:** `D:/Claude Projects/Gridiron Warrior/External Library/BusinessDocuments/`
- **AI research briefs:** `D:/Claude Projects/Gridiron Warrior/External Library/AI/`
- **Dewey saves (Twitter + IG):** `D:/Claude Projects/Gridiron Warrior/External Library/Twitter-Instagram Saves/`
- **Voice corpus (Scott-original):** `D:/Claude Projects/Gridiron Warrior/Voice Corpus/Voice Notes/`
- **Daily content seeds:** `D:/Claude Projects/Gridiron Warrior/Deliverables/_daily-seeds/`
- **Deliverables output (new content lands here):** `D:/Claude Projects/Gridiron Warrior/Deliverables/_inbox/`
- **Voice rules:** `D:/Claude Projects/CLAUDE.md`

---

## Step 0: Read the Wiki First

Before touching the source material, read the wiki to understand what Scott already knows and has already said about this topic.

1. Read `wiki/index.md`
2. Find any entity, concept, or summary pages that match the topic
3. Read those pages — extract: what angles Scott has already covered, what products connect to this topic, what his stated position is, what quotes or phrases he's used before

This context shapes everything that follows. It prevents repeating angles he's already published and ensures CTAs point to the right product.

## Step 0.5: Check NotebookLM for Depth (if relevant)

If the topic is a coaching/S&C concept (not just a product pitch), check whether there is a matching research brief in `D:/Claude Projects/Gridiron Warrior/Research/NotebookLM/`.

- If a brief exists for this topic, read it and pull the strongest coaching insight or evidence point into the content pack
- If no brief exists and the topic warrants it, note in Step 6 report that running `/gw-research [topic]` first would strengthen the content

NotebookLM is the knowledge fuel. Use it when it exists.

## Step 0.6: Sweep External Library for cross-domain reinforcement

NEW (added 2026-05-13): The vault now has three knowledge domains — S&C, Business, AI. Before drafting, sweep the External Library for material that could reinforce the content angle:

1. **Dewey saves** (`External Library/Twitter-Instagram Saves/`) — Grep for the topic across notes. A relevant Dewey save can supply a powerful quote, counter-example, or proof point. Look for notes tagged with the topic or by authors Scott has called out.
2. **Business research briefs** (`External Library/BusinessDocuments/YYYY-MM-DD-*-brief.md`) — If the content is about coaching as a business (sponsor outreach, course launches, Insiders growth), a recent business brief may have the exact framework.
3. **AI research briefs** (`External Library/AI/YYYY-MM-DD-*-brief.md`) — If the content is about AI tooling or workflow automation, pull from here.
4. **Voice corpus** (`Voice Corpus/Voice Notes/YYYY-MM-DD-*.md`) — HIGH PRIORITY. Scott's first-person voice notes are gold. If a recent voice note mentions this topic, the rough phrasing IS the seed of the content. Use verbatim quotes when possible.
5. **Daily seeds** (`Deliverables/_daily-seeds/`) — Check if a recent seed file already proposed an angle for this topic. If so, build on it rather than starting fresh.

When you find cross-domain material, name it explicitly in Step 6 report:
> "Pulled from: wiki/concepts/contact-prep.md + Dewey save coach-murdock-2026-04-12.md + voice note 2026-05-09-physicality-vs-strength.md"

This is how the vault closes the loop — content is built from EVERYTHING that landed, not just what's in wiki/.

---

## Step 1: Read the Source Material

If the user gave a file path, read it. If they gave a topic name, search:
1. `wiki/summaries/` for an existing Film Study or brief on this topic
2. `Research/NotebookLM/` for a matching brief
3. `Second Brain/` for matching markdown and docx files (match by filename keywords)
4. If multiple files match, read all and synthesize

Extract: the topic, the core principles/insights, the strongest quote, and any product connections.

---

## Step 2: Cross-Reference

Check whether this source contains knowledge NOT already captured in the wiki.

Note any new angles, updated positions, new quotes, or new evidence. These go in the content pack AND get flagged for wiki ingest in Step 5.

If the source is a Film Study transcript and a wiki summary already exists for it, use the wiki summary as your primary reference — it's already distilled.

---

## Step 3: Write the Content Pack

Read voice rules from `D:/Claude Projects/CLAUDE.md` before writing.

- Short sentences. Active verbs. Plain language.
- **No em-dashes. Not one.**
- No banned words: delve, tapestry, vibrant, transformative, unlock, leverage, game-changer, revolutionary, groundbreaking, seamless, robust, utilize, synergy, holistic, empower, journey, curated, cutting-edge, innovative, best-in-class, dive into, unpack, explore, elevate, reimagine, supercharge
- Tough love. Coach in the trenches. Not a motivational poster.
- Sign off: Keep the Fire Burning, / Leech

### Asset 1: Twitter Thread #1 (Teaching Thread)

- **Tweet 1 (Hook):** Bold coaching truth or provocative statement. Under 280 chars.
- **Tweets 2-5 (Teaching):** One clear point per tweet. Short sentences. Specific.
- **Tweet 6 (Bridge):** Connect the teaching to a real in-season or offseason scenario.
- **Tweet 7 (CTA):** Soft pitch. Under 280 chars.

Every tweet must be under 280 characters.

### Asset 2: Twitter Thread #2 (Myth-Buster or Story Thread)

- **Tweet 1 (Hook):** "Most coaches get [topic] wrong." or a story opener.
- **Tweets 2-4:** The myth, the reality, the evidence. Or the story beats.
- **Tweet 5:** The lesson.
- **Tweet 6 (CTA):** Different angle than Thread #1. Push to course, podcast, or Summit based on wiki cross-reference.

### Asset 3: Instagram Carousel #1 (Teaching Carousel)

Write the text for each slide:
- **Slide 1 (Cover):** Bold headline. Topic name. Hook question or statement.
- **Slides 2-5 (Teaching):** One point per slide. Header line (bold, short). 2-3 supporting sentences max.
- **Slide 6 (Common Mistake):** "The #1 mistake I see:" followed by the most impactful mistake.
- **Slide 7 (CTA):** Push to Insiders or relevant course.

Write the **caption**: Hook first line. 3-4 sentences. CTA. Max 3 hashtags: #footballcoach #strengthandconditioning #gridironwarrior

### Asset 4: Instagram Carousel #2 (Quote or Myths vs. Reality)

**Option A (Quote Carousel):** Key quote on slide 1, why it matters on slides 2-4, CTA on slide 5.
**Option B (Myths vs. Reality):** "What You Think vs. What Actually Works" format, 3 myths busted, CTA.

Pick whichever fits the source material better. Write caption with same rules.

### Asset 5: Email Draft

Leech Letter style:
- Subject lines: lowercase, 3-6 words, curiosity or tension
- Opens with "Coach," or jumps straight in
- 5-8 short paragraphs. One idea per paragraph. Many are one sentence.
- Problem → agitation → insight → CTA
- CTA points to the product the wiki cross-reference found (or defaults to Insiders $1 trial)
- Ends with: Keep the Fire Burning, / Leech

---

## Step 4: Save to Deliverables

Save as: `D:/Claude Projects/Gridiron Warrior/Deliverables/_inbox/[TOPIC-SLUG]/[TOPIC-SLUG]-content-pack-[YYYY-MM-DD].md`

Create the `_inbox/[TOPIC-SLUG]/` folder if it does not yet exist. New content lands in `_inbox/` so Scott can triage it (Ready / Cold / Kill) before it enters the working set.

File structure:
```markdown
---
date: [YYYY-MM-DD]
topic: [TOPIC]
source_file: [filename(s) used as input]
wiki_refs: [list of wiki pages consulted]
pipeline: gw-content-forge
---

# [TOPIC] — Content Pack

## Wiki Cross-Reference
[2-3 sentences: what wiki pages were consulted, what angles already exist, what's new]

---
## Twitter Thread #1: [Title]
[thread]

---
## Twitter Thread #2: [Title]
[thread]

---
## Instagram Carousel #1: [Title]
### Slide Text
[slides]
### Caption
[caption]

---
## Instagram Carousel #2: [Title]
### Slide Text
[slides]
### Caption
[caption]

---
## Email Draft
**Subject:** [subject]
[body]
```

---

## Step 5: Update the Wiki (if source is new)

If the source contained coaching knowledge NOT already captured in a wiki summary page:

1. Write a summary page to `wiki/summaries/[topic-slug].md` using the standard summary format (title, source, date, key takeaways, concepts touched, entities touched)
2. Update any entity or concept pages in `wiki/` that this source touches
3. Add the new summary to `wiki/index.md` under the appropriate section
4. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | [topic] — via gw-content-forge`
5. **Flag any new coaching concept** that appears repeatedly in this source and does NOT have a dedicated wiki concept page yet. Note it in the Step 6 report so it can be created.

If a wiki summary for this source already exists, skip this step but still check step 5 for new concepts.

---

## Step 6: Report to Scott

Tell him:
1. The content pack file path
2. What the wiki cross-reference found (angles already covered, what's new)
3. Which products/offers the CTAs point to and why
4. Whether a new wiki summary was created or an existing one was used
5. One line on the strongest piece in the pack

Keep it tight. He has 15 minutes.

---

## After writing the content pack

The new topic now lives in `_inbox/`. Run `/gw-queue` to refresh state and surface it in the dashboard's Inbox view. Then run `/gw-triage` (or use the dashboard) to sort it into `ready/`, `cold-storage/`, or kill it.

This is the queue system's intake gate. Nothing reaches the working set without your explicit Ready/Cold/Kill decision.

---

## After writing the content pack — mark forge backlog entry

If the topic you just forged was suggested by a daily seed (i.e., it appears in `queue-state.json`'s `forge_backlog` array), mark the entry as `forged` so it stops showing in the dashboard's Backlog view.

```bash
python -c "
import json, pathlib, sys, re
new_slug = 'REPLACE_WITH_TOPIC_SLUG'  # e.g., 'stop-running-your-linemen'
p = pathlib.Path('D:/Claude Projects/Gridiron Warrior/Deliverables/queue-state.json')
data = json.loads(p.read_text(encoding='utf-8'))
backlog = data.get('forge_backlog', [])
hits = [e for e in backlog if e['slug'] == new_slug]
if hits:
    for h in hits:
        h['status'] = 'forged'
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Marked {len(hits)} backlog entry/entries as forged')
else:
    print(f'No backlog match for slug {new_slug} (this is normal if topic was a one-off)')
"
```

Then suggest running `/gw-queue` to refresh state and push to the dashboard.
