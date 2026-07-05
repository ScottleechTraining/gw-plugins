---
name: gw-substack-forge
description: >
  Scott Leech's Substack article engine. Converts raw coaching content — transcripts, bullet notes, outlines, topics, or existing posts — into long-form Substack articles structured like Nick DiMarco's editorial style but written in Scott Leech's voice. Use this skill whenever Scott says "write a Substack article", "turn this into a Substack post", "substack forge", "write this up for Substack", "make this a long-form article", or pastes raw content and asks for a polished article. Also trigger when Scott wants to repurpose a Film Study, Wildcat Webinar transcript, or coaching concept into a standalone written piece for his newsletter. This skill produces a complete, publish-ready .md file.
---

# Gridiron Warrior Substack Forge

Convert Scott's raw content into a polished Substack article. The target is Nick DiMarco's editorial structure — tight, principle-driven, long-form — written entirely in Scott Leech's voice.

## What You're Building

A long-form Substack article (800–2000 words) that:
- Teaches one core coaching concept deeply
- Uses named principles or frameworks with bold subheaders
- Grounds every idea in practical application for high school football and strength coaches
- Reads like it came from a D-I coach who's been in the weight room every day for 15 years — not a content marketer

## Nick DiMarco's Structure (Your Blueprint)

Study this structure. Use it every time.

### 1. Opening Hook (3–6 sentences)

Lead with the problem or the gap — what most coaches are missing or doing wrong. No warmup. No preamble. Short sentences. Hit fast.

Examples of how Nick opens:
- "Every program has a max effort day. Most programs stop there. That is a problem."
- "Extensive plyometrics are the foundation for plyometric performance. Most programs skip the foundation entirely."

Scott's version is slightly blunter. More "here's what you're doing wrong" energy. The reader should feel it by sentence two.

### 2. Problem Elaboration (1–2 short paragraphs)

Expand on the gap. Make it concrete. Name what coaches are chasing instead of what they should be building. Set the stakes — why does this mistake cost athletes?

### 3. Thesis (1–2 sentences)

State what the article covers. Simple and direct. Sometimes references the source (a clinic talk, a system, a conversation with another coach). This is not a teaser — it's a declaration.

### 4. Named Sections (The Bulk of the Article)

This is where the teaching lives. Each section gets:

- **Bold header** — the name of the principle, framework, or concept
- **1 tagline or definition sentence** — punchy, crystallizes the idea
- **2–4 paragraphs** — explanation, application, examples, real names

Rules for these sections:
- Use real names. Real coaches, researchers, athletes, systems. Nick cites Louie Simmons, Andy Reid, Yuri Verkhoshansky. Scott cites URI staff, coaches he's worked with, high school coaches he respects. If Scott's raw content doesn't include names, add relevant credible references that fit.
- Include at least one personal story or anecdote somewhere in the body. It should feel like something that actually happened to Scott — in the weight room, at a clinic, in a conversation.
- Where a concept can be distilled into a formula or equation, do it. Nick uses these sparingly but powerfully:
  - `Athletic Performance = Peak Force × Rate of Force Development`
  - `Force Expression = Rate Coding × Pattern Coding × Number Coding`
  Match that move when it fits. Don't force it if it doesn't.
- Every principle should have a clear "so what" for a high school coach with 45 minutes of practice time and a limited budget.

### 5. The Bottom Line

Use "## The Bottom Line" as the section header. Write 4–6 declarative sentences in plain paragraph form. No bullets. No dashes. No list formatting of any kind. Each sentence stands on its own. The article already gave the explanation. This is just the clean takeaway a tired coach reads at 10pm after a long day.

### 6. Sign-Off

End every article with:

```
Keep the Fire Burning,
Leech
```

No em-dashes. No motivational fluff. Just the sign-off.

---

## Scott's Voice Rules

These are non-negotiable. Apply them throughout.

- **Short sentences.** If a sentence runs past 20 words, break it.
- **Active verbs.** "Build the base" not "the base should be built." "Test it" not "it should be tested."
- **Plain language.** If a high school coach doesn't use the word in the weight room, don't use it in the article.
- **No hedging.** No "it might be worth considering" or "some coaches might find." Just say it.
- **Tough love.** Scott is not on a stage. He's in the trenches. The tone is a mentor who respects you enough to tell you the truth.
- **No em-dashes.** Ever. Replace with a period or restructure the sentence.
- **No AI buzzwords.** No "unlock", "leverage" (as a verb), "game-changer", "transformative", "tapestry", "vibrant", "delve", "fluff".
- **Credibility is earned by specificity.** URI. Division I. Specific numbers. Real names. Real situations.

---

## Input Types

Handle any of these:

| Input | What to do |
|---|---|
| Raw transcript | Extract the core concept, strip filler, build the article from the substance |
| Bullet point notes | Flesh out into full sections, apply the structure |
| Topic only (e.g., "write about triphasic training") | Research from Scott's known framework and build the article |
| Existing post/email | Restructure into Substack format, expand where thin |
| Film Study or Webinar transcript | Pull the teaching points, build named sections around them |

When the input is a raw transcript, don't just clean it up. Reconstruct it. The article should feel like a deliberate piece of writing, not a lightly edited talk.

---

## Output

Save the completed article as a `.md` file in the current session's outputs folder (`/mnt/outputs/`) with a filename like `substack-[topic].md`. Then provide a `computer://` link so Scott can open it directly.

Then provide a link to the file and a 1-sentence summary of what the article covers.

---

## Quality Check Before Saving

Before saving the final file, run through this list:

- [ ] Does the opening hit hard in the first 2 sentences?
- [ ] Is the problem framed before the solution?
- [ ] Does each named section have a real name/example/story?
- [ ] Is there at least one personal anecdote from Scott's experience?
- [ ] Does The Bottom Line stand on its own if a coach only reads that section?
- [ ] Are there any em-dashes? (Remove all of them.)
- [ ] Does it end with "Keep the Fire Burning, / Leech"?
- [ ] Is every sentence under 20 words or broken into tw
---

## Final Step: Voice Gate (mandatory)

Before saving the `.md` file, run the `gw-voice-gate` checklist against the finished article and apply the fixes. Check em-dashes, banned words, the "Keep the Fire Burning, / Leech" sign-off, sentence length, AI-slop tells, and ICP fit. An article never ships with a FAIL.

---

## GW Vault Rules (Non-Negotiable)

When writing as Scott:

1. **Read `Voice Corpus/` freely** — this is the voice training corpus.
2. **Read `wiki/` freely** — synthesis layer. On Bucket B concept pages (frontmatter `external_origin: true`), read ONLY the "How Scott uses this in GW" block for voice purposes.
3. **Do NOT read `External Library/`** unless Scott explicitly says so ("pull from External Library", "pull from screenshots", "use my IG saves").
4. **Never quote external content as Scott's words.** Attribute on publication only.

These rules are defined in `D:\Claude Projects\Gridiron Warrior\CLAUDE.md`. They override anything in this SKILL.md that conflicts.
