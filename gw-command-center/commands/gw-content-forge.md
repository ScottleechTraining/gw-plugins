---
name: gw-content-forge
description: "Scott Leech's content production engine. Two modes. TRANSCRIPT MODE: paste a transcript (podcast, Film Study, or Wildcat Webinar) and get the correct asset set for that content type, ready to schedule. CONTENT PACK MODE: give a topic, file path, or Second Brain reference and get a full content pack (3 Twitter threads, 2 Instagram carousels, 3 reel ideas, 1 email). All in Scott Leech's voice. Wiki-first, cross-domain integrated, queue-aware. Use when Scott pastes a transcript, says 'content forge', 'run the forge', 'make content from', or asks for Twitter threads, carousels, emails, or reels from any GW source or coaching topic."
---

# GW Content Forge

Gridiron Warrior's content production engine. One input. All the assets. Scott's voice every time. Wiki-first, cross-domain integrated, plugged into the queue dashboard.

## Accepted input: $ARGUMENTS

The user will provide one of:
- **A transcript** (pasted text, or a file path to a `.txt` / `.md` / `.docx`) → TRANSCRIPT MODE
- **A file path** to any vault source (brief, Film Study doc, pitch doc) → CONTENT PACK MODE
- **A topic name** (e.g., "contact prep", "box squats") → CONTENT PACK MODE; find the source files
- **A Second Brain reference** (e.g., "the contact prep transcript") → CONTENT PACK MODE
- **Nothing** — check `Research/NotebookLM/` for the most recently created brief → CONTENT PACK MODE

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
- If no brief exists and the topic warrants it, note in the final report that running `/gw-research [topic]` first would strengthen the content

NotebookLM is the knowledge fuel. Use it when it exists.

## Step 0.6: Sweep External Library for cross-domain reinforcement

The vault has three knowledge domains — S&C, Business, AI. Before drafting, sweep the External Library for material that could reinforce the content angle:

1. **Dewey saves** (`External Library/Twitter-Instagram Saves/`) — Grep for the topic across notes. A relevant Dewey save can supply a powerful quote, counter-example, or proof point.
2. **Business research briefs** (`External Library/BusinessDocuments/YYYY-MM-DD-*-brief.md`) — If the content is about coaching as a business, a recent business brief may have the exact framework.
3. **AI research briefs** (`External Library/AI/YYYY-MM-DD-*-brief.md`) — If the content is about AI tooling or workflow automation, pull from here.
4. **Voice corpus** (`Voice Corpus/Voice Notes/YYYY-MM-DD-*.md`) — HIGH PRIORITY. Scott's first-person voice notes are gold. If a recent voice note mentions this topic, the rough phrasing IS the seed of the content. Use verbatim quotes when possible.
5. **Daily seeds** (`Deliverables/_daily-seeds/`) — Check if a recent seed file already proposed an angle for this topic. If so, build on it rather than starting fresh.

When you find cross-domain material, name it explicitly in the final report:
> "Pulled from: wiki/concepts/contact-prep.md + Dewey save coach-murdock-2026-04-12.md + voice note 2026-05-09-physicality-vs-strength.md"

This is how the vault closes the loop — content is built from EVERYTHING that landed, not just what's in wiki/.

---

## Step 1: Determine Mode

Read the input and pick the mode:

**TRANSCRIPT MODE** — the user pasted a transcript, said "here's the transcript," or pointed at a `.txt` / `.md` / `.docx` that looks like a session recording. This is the daily post-session workflow. Go to Step 2A.

**CONTENT PACK MODE** — the user gave a topic keyword, a file path that is not a transcript, a Second Brain reference, or asked for content without source material. This is the research-driven creation workflow. Go to Step 2B.

When in doubt, ask: "Is this a transcript from a recorded session, or a topic you want me to build content around?"

---

## STEP 2A: TRANSCRIPT MODE

The highest-frequency task. Post-session, phone in hand, transcript ready.

### 2A.1: Identify Content Type

Ask (or infer from context):
- **Podcast** — 6 assets
- **Film Study** — 5 assets
- **Wildcat Webinar** — 6 assets (includes guest share message)

If the user doesn't specify, check the transcript for clues: guest intro = podcast or webinar, Scott solo presenting = Film Study.

### 2A.2: Read the Transcript

Read or accept the pasted transcript. Extract:
- The topic and the single sharpest coaching insight
- The strongest quote or moment (best hook candidate)
- Any product connection (Contact Prep, GW 2.0, Insiders, Summit)
- Guest name if applicable

### 2A.3: Voice Rules (apply to every asset)

Read voice rules from `D:/Claude Projects/CLAUDE.md` before writing.

- Short sentences. Active verbs. Plain language.
- **No em-dashes. Not one.**
- No banned words: fluff, delve, tapestry, vibrant, transformative, unlock, leverage (as verb), game-changer, revolutionary, groundbreaking, seamless, robust, utilize, synergy, holistic, empower, journey, curated, cutting-edge, innovative, best-in-class, dive into, unpack, explore, elevate, reimagine, supercharge
- Tough love. Coach in the trenches. Not a motivational poster.
- Sign off all emails: Keep the Fire Burning, / Leech

Write all assets in Scott's voice before outputting anything. Then output all at once.

---

### PODCAST (6 assets)

**Asset 1: YouTube Description**
- 2-3 sentence episode summary. Why a football coach needs to hear this.
- Timestamps: infer from transcript structure if not explicitly provided. Format: `0:00 Intro`, `2:30 [Topic]`, etc.
- 3-5 hashtags: `#footballcoach #strengthandconditioning #gridironwarrior` plus 1-2 topic-specific

**Asset 2: HelloAudio Description**
- 2-3 sentences. Episode number (if known), guest name, topic, why it matters.
- Plain. No hype.

**Asset 3: Email Announcement**
- Subject line: lowercase, 4-6 words, curiosity or tension (not the guest's name alone)
- Opens with "Coach," or jumps straight in
- 5-6 short paragraphs. Lead with the single best insight from the episode.
- Why a football coach needs to hear this specific conversation.
- CTA: listen to the episode. Soft Insiders CTA at the end if relevant.
- Sign off: Keep the Fire Burning, / Leech

**Asset 4: Twitter Thread**
- Tweet 1: Hook. Bold coaching truth or the episode's sharpest insight. Under 280 chars.
- Tweets 2-4: Teaching points from the episode. One per tweet. Specific. Under 280 chars each.
- Tweet 5: Link to episode. Soft CTA. Under 280 chars.

**Asset 5: Instagram Caption**
- First line is the hook. No setup.
- 3-4 short punchy sentences.
- CTA: "Comment PODCAST and I'll send you the link."
- Max 3 hashtags: `#footballcoach #strengthandconditioning #gridironwarrior`

**Asset 6: Show Notes**
- 3-4 bullet points. Key takeaways. Plain language. Coach-friendly.
- What the listener walks away knowing how to do.

---

### FILM STUDY (5 assets)

**Asset 1: YouTube Description**
- 2-3 sentences on the topic and why it matters right now in the training calendar.
- Timestamps inferred from transcript.
- Hashtags: `#footballcoach #filmStudy #gridironwarrior` plus topic-specific.

**Asset 2: Insiders Community Post**
- 2-3 sentences. Direct. Tells members exactly what they're getting and why it matters this week.
- Include the YouTube link placeholder: `[YOUTUBE LINK]`
- No fluff.

**Asset 3: Email Teaser to Full List**
- Subject line: leads with the best insight from the session, not "Film Study recap"
- 4-6 sentences. Leads with what Insiders coaches just learned.
- Non-members feel what they're missing.
- Ends with: "This is what Insiders coaches are learning every week. First month is $1. [LINK]"
- Sign off: Keep the Fire Burning, / Leech

**Asset 4: Twitter Thread**
- Tweet 1: Hook. Bold coaching truth pulled from the session. Under 280 chars.
- Tweets 2-4: Teaching points. One idea per tweet. Specific and usable. Under 280 chars.
- Tweet 5: Bridge to Insiders. "This is what we cover every week inside GW Insiders. First month is $1. [LINK]" Under 280 chars.

**Asset 5: Instagram Caption**
- First line is the hook.
- 3-4 sentences. Tease the content without giving it all away.
- CTA: "Comment INSIDERS and I'll send you the link."
- Max 3 hashtags.

---

### WILDCAT WEBINAR (6 assets)

**Asset 1: YouTube Description**
- Episode summary. Guest bio in 2 sentences (credentials, why coaches should care).
- Timestamps inferred from transcript.
- Hashtags: `#footballcoach #gridironwarrior` plus topic-specific.

**Asset 2: Insiders Community Post**
- 2-3 sentences. What members just got access to. Guest name and topic.
- YouTube link placeholder: `[YOUTUBE LINK]`

**Asset 3: Email Teaser to Full List**
- Subject line: guest name + what they taught. Curiosity angle.
- 4-6 sentences. Lead with the guest's best insight or most surprising point.
- Non-members feel the cost of not being inside.
- Ends with $1 trial CTA.
- Sign off: Keep the Fire Burning, / Leech

**Asset 4: Twitter Thread**
- Tweet 1: Hook. The guest's sharpest point or most provocative claim. Under 280 chars.
- Tweets 2-4: Teaching points from the session. Under 280 chars each.
- Tweet 5: CTA to Insiders. Under 280 chars.

**Asset 5: Instagram Caption**
- Lead with the guest's credibility or best quote.
- 3-4 sentences.
- CTA: "Comment INSIDERS and I'll send you the link."
- Max 3 hashtags.

**Asset 6: Guest Share Message**
- Short text Scott sends to the guest directly (text or DM format).
- Includes their clip link placeholder: `[CLIP LINK]`
- A caption the guest can copy/paste to share with their own network.
- Tone: one coach to another. Not a PR request. Handing them the finished product.
- 3-4 sentences max.

---

### 2A.4: Save TRANSCRIPT MODE Output

Save to: `D:/Claude Projects/Gridiron Warrior/Deliverables/_inbox/[CONTENT-TYPE]-[TOPIC-SLUG]/[CONTENT-TYPE]-[TOPIC-SLUG]-[YYYY-MM-DD].md`

Where `[CONTENT-TYPE]` is `podcast`, `film-study`, or `wildcat-webinar`. Creates the `_inbox/` folder if it doesn't exist.

Then jump to Step 4 (Wiki Update) and Step 5 (Report).

---

## STEP 2B: CONTENT PACK MODE

Research-driven. Topic or file in, full content pack out.

### 2B.1: Read the Source Material

If the user gave a file path, read it. If they gave a topic name, search:
1. `wiki/summaries/` for an existing Film Study or brief on this topic
2. `Research/NotebookLM/` for a matching brief
3. `Second Brain/` for matching markdown and docx files (match by filename keywords)
4. If multiple files match, read all and synthesize

Extract: the topic, the core principles/insights, the strongest quote, and any product connections.

### 2B.2: Cross-Reference the Second Brain

Grep `Second Brain/` for the topic keyword and close synonyms. Note which files matched and what Scott has said about this topic before.

This shapes the CTAs:
- If a course covers this topic (Contact Prep, GW 2.0, Scores and Stops) → point there
- If a Film Study exists → reference it and push Insiders
- No prior work found → default CTA is Insiders $1 trial

Note any new angles, updated positions, new quotes, or new evidence. These go in the content pack AND get flagged for wiki ingest in Step 4.

### 2B.3: Voice Rules

Same as TRANSCRIPT MODE (see Step 2A.3).

### 2B.4: Generate the Content Pack (7 assets)

**Asset 1: Twitter Thread #1 (Teaching Thread)**
- Tweet 1 (Hook): Bold coaching truth or provocative statement. Under 280 chars.
- Tweets 2-5 (Teaching): One clear point per tweet. Short sentences. Specific. Under 280 chars.
- Tweet 6 (Bridge): Connect the teaching to a real in-season or offseason scenario. Under 280 chars.
- Tweet 7 (CTA): Soft pitch to the relevant product. Under 280 chars.

**Asset 2: Twitter Thread #2 (Myth-Buster or Story Thread)**
- Tweet 1 (Hook): "Most coaches get [topic] wrong." or a story opener. Under 280 chars.
- Tweets 2-4: The myth, the reality, the evidence. Or story beats. Under 280 chars.
- Tweet 5: The lesson. Under 280 chars.
- Tweet 6 (CTA): Different angle than Thread #1. Push to course, podcast, or Summit. Under 280 chars.

**Asset 3: Twitter Thread #3 (Quick-Hit Practical Thread)**
- Tweet 1 (Hook): "Here are [3/5/7] things about [topic] most coaches never learn:" Under 280 chars.
- Tweets 2-N: One practical, usable point each. Numbered. Short. Under 280 chars.
- Final Tweet (CTA): Direct. Point to the most relevant offer. Under 280 chars.

**Asset 4: Instagram Carousel #1 (Teaching Carousel)**

Slide text:
- Slide 1 (Cover): Bold headline. Topic name. Hook question or statement.
- Slides 2-5 (Teaching): One point per slide. Header line (bold, short). 2-3 supporting sentences max.
- Slide 6 (Common Mistake): "The #1 mistake I see:" followed by the most impactful mistake.
- Slide 7 (CTA): Push to Insiders or relevant course.

Caption: Hook first line. 3-4 sentences. CTA: "Comment INSIDERS and I'll send you the link." Max 3 hashtags: `#footballcoach #strengthandconditioning #gridironwarrior`

**Asset 5: Instagram Carousel #2 (Quote or Myths vs. Reality)**

Choose whichever fits the source material better:
- *Option A (Quote Carousel):* Key quote on slide 1, why it matters on slides 2-4, CTA on slide 5.
- *Option B (Myths vs. Reality):* "What You Think vs. What Actually Works" format. 3 myths busted. CTA.

Caption: same rules as Asset 4.

**Asset 6: Reel Ideas (3 concepts)**

Three standalone reel concepts Scott can shoot in under 60 seconds. Format each as:
- **Hook (first 3 seconds):** Exact words to say to camera. Provocative. Stops the scroll.
- **Body (20-40 seconds):** What to demonstrate or say. One tight teaching point.
- **CTA (last 5 seconds):** What to say and where to point.

Concepts and structure only. Scott fills in the coaching specifics.

**Asset 7: Email Draft (Leech Letter style)**

- Subject: lowercase, 3-6 words, curiosity or tension
- Opens with "Coach," or jumps straight in
- 5-8 short paragraphs. One idea per paragraph. Many are one sentence.
- Structure: Problem → agitation → insight → CTA
- CTA points to the product the cross-reference found (or defaults to Insiders $1 trial)
- Ends with: Keep the Fire Burning, / Leech

### 2B.5: Save CONTENT PACK MODE Output

Save as: `D:/Claude Projects/Gridiron Warrior/Deliverables/_inbox/[TOPIC-SLUG]/[TOPIC-SLUG]-content-pack-[YYYY-MM-DD].md`

Create the `_inbox/[TOPIC-SLUG]/` folder if it doesn't exist. New content lands in `_inbox/` so Scott can triage it (Ready / Cold / Kill) before it enters the working set.

File structure:
```markdown
---
date: [YYYY-MM-DD]
topic: [TOPIC]
mode: content-pack
source_files: [list of files used]
wiki_refs: [list of wiki pages consulted]
second_brain_refs: [list of Second Brain files that matched]
external_refs: [list of External Library / Voice Corpus / Daily seed files used]
cta_rationale: [why these CTAs were chosen]
pipeline: gw-content-forge
---

# [TOPIC] — Content Pack

## Cross-Reference Summary
[2-3 sentences: what wiki and Second Brain pages were consulted, what angles already exist, what's new]

---
## Twitter Thread #1: [Title]
[thread]

---
## Twitter Thread #2: [Title]
[thread]

---
## Twitter Thread #3: [Title]
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
## Reel Ideas
### Reel 1: [Title]
[concept]

### Reel 2: [Title]
[concept]

### Reel 3: [Title]
[concept]

---
## Email Draft
**Subject:** [subject]
[body]

---
## PULLED FROM THE BRAIN
- [wiki page path] ([one clause: what it contributed to this pack])
- [wiki page path] ([one clause])
- [Voice Corpus file if used] ([one clause])

NEW TO THE BRAIN: [concept/summary page this run created, or "nothing new - fully covered by existing pages"]
```

The PULLED FROM THE BRAIN block is required in every pack, always the last section. It is the retrieval receipt: Scott approves packs in 60 seconds because he can see exactly what each one is built on. If the cross-reference genuinely found nothing, say so in the block ("no wiki matches - built from [source] only") - that is a signal the topic needs a research pass, not a section to omit.

---

## Step 3: Save (handled inside mode steps)

Both modes save into `Deliverables/_inbox/[TOPIC-SLUG]/`. The `_inbox/` lands new content for Scott to triage (Ready / Cold / Kill) before it enters the working set.

---

## Step 4: Update the Wiki (if source is new)

If the source contained coaching knowledge NOT already captured in a wiki summary page:

1. Write a summary page to `wiki/summaries/[topic-slug].md` using the standard summary format (title, source, date, key takeaways, concepts touched, entities touched)
2. Update any entity or concept pages in `wiki/` that this source touches
3. Add the new summary to `wiki/index.md` under the appropriate section
4. Append to `wiki/log.md`: `## [YYYY-MM-DD] ingest | [topic] — via gw-content-forge`
5. **Flag any new coaching concept** that appears repeatedly in this source and does NOT have a dedicated wiki concept page yet. Note it in the Step 5 report so it can be created.

If a wiki summary for this source already exists, skip this step but still check for new concepts.

---

## Step 5: Report to Scott

Tell him:
1. The content pack file path
2. Mode used (TRANSCRIPT or CONTENT PACK), and for TRANSCRIPT mode which content type (podcast / film-study / wildcat-webinar)
3. The PULLED FROM THE BRAIN block, verbatim
4. What cross-domain material was used (Dewey saves, voice notes, business briefs, daily seeds)
5. Which products/offers the CTAs point to and why
6. Whether a new wiki summary was created or an existing one was used
7. One line on the strongest piece in the pack

Keep it tight. Scott has 15 minutes.

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
