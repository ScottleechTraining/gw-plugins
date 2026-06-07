---
description: "Generate a one-page PDF-ready lead magnet from a brief or content source. Funnels into Insiders, a course, or Summit."
---

# /gw-freebie-forge [brief-or-content-path] — Lead Magnet Producer

Takes any brief, transcript, or content source. Produces one-page, printable lead magnet that funnels readers into the right paid offer. Coach-direct. Scott's voice. No commit. No autonomous distribution.

## Accepted input: $ARGUMENTS

The user provides a file path. Typical inputs:
- A Film Study brief at `Research/Film Study/YYYY-MM-DD-<slug>-film-study-brief.md`
- A `/gw-research` brief at `Research/NotebookLM/<slug>-brief.md`
- A Voice Corpus transcript
- Any markdown file with coaching content

If empty, abort with: "Provide a source file path. Example: `/gw-freebie-forge \"D:\\Claude Projects\\Gridiron Warrior\\Research\\Film Study\\2026-05-25-deceleration-film-study-brief.md\"`."

## Vault paths

- **Voice rules:** `D:\Claude Projects\CLAUDE.md`
- **Output:** `D:\Claude Projects\Gridiron Warrior\Deliverables\<topic-slug>-freebie.md`
- **Wiki for product targeting:** `D:\Claude Projects\Gridiron Warrior\wiki\` (read entities/Insiders, entities/GW-2-0, entities/Contact-Prep, entities/Scores-and-Stops, entities/Summit to pick the right CTA)
- **Voice check guard:** `D:\Claude Projects\Gridiron Warrior\scripts\voice_check.py`

## Steps

### Step 1 — Read the source

Read the file at `$ARGUMENTS`. Extract: topic, the 3-5 strongest teaching points, the single most coach-direct quote or line, any specific stat or example.

If the source is a Film Study brief, the "Bottom-line takeaways" section is the obvious source. If it's a longer brief or transcript, distill.

### Step 2 — Read voice rules

Read `D:\Claude Projects\CLAUDE.md`. Internalize:
- Short sentences. Active verbs. Plain language.
- **No em-dashes. Not one.**
- Banned words: delve, tapestry, vibrant, transformative, unlock, leverage (as verb), game-changer, revolutionary, groundbreaking, seamless, robust, utilize, synergy, holistic, empower, journey, curated, cutting-edge, innovative, best-in-class, dive into, unpack, explore, elevate, reimagine, supercharge, fluff
- Tough love. Coach in the trenches.
- Sign off: `Keep the Fire Burning,` / `Leech`

### Step 3 — Pick the CTA target

Read the wiki entity pages to decide where this freebie funnels. Priority order:

1. **Insiders ($1 first month trial)** — default. Always works. Use unless a course is a clearly better fit.
2. **Contact Prep ($87)** — if the topic is physicality, tackling, partner drills, violence-as-skill, OL/DL.
3. **Scores and Stops ($104)** — if the topic is agility, space creation, closing space, decision-making.
4. **Gridiron Warrior 2.0 ($197)** — if the topic is summer programming, full-team S&C, season-long programs.
5. **Summit ($199, July 18)** — if the topic ties to an upcoming Summit speaker or angle, AND today's date is before July 18.

Decide one. Name it in Step 6 report so Scott knows the funnel direction.

### Step 4 — Write the freebie

One page. Printable to PDF. Structure:

```markdown
---
title: "[Hook headline]"
topic: "[original topic from source]"
topic_slug: [slug]
date: YYYY-MM-DD
source: [absolute path to $ARGUMENTS]
funnel_cta: [Insiders | Contact Prep | Scores and Stops | GW 2.0 | Summit]
pipeline: gw-freebie-forge
---

# [Hook headline — bold coaching truth, under 60 chars]

[Coach,]

[Opening hook: 2-3 short sentences. The pain point or the lie most coaches believe. Direct. No throat-clearing.]

## [Teaching section header — short, declarative]

[3-5 teaching points. Each one is:
- A bold bolded line (the principle)
- 2-3 short sentences underneath (the how / the why / a quick example)
No bullet salad. Read like a coach talking to a coach after practice.]

**[Point 1 principle]**

[2-3 sentences.]

**[Point 2 principle]**

[2-3 sentences.]

**[Point 3 principle]**

[2-3 sentences.]

(4 and 5 only if the source supports them. Don't pad.)

## What this means for your program

[Single short paragraph. 3-4 sentences. The "so what" for a high school or college coach reading this Monday morning.]

## [Next step — direct, urgency-flavored CTA line]

[2-3 sentences pitching the funnel target picked in Step 3. Include the price or trial offer. Include a link placeholder Scott can swap in. Specific to the offer:

- Insiders: "$1 for the first month. Cancel anytime. [LINK]"
- Contact Prep: "$87. 60+ videos. Three-phase progression. [LINK]"
- Scores and Stops: "$104. Agility drills for creating and closing space. [LINK]"
- GW 2.0: "$197. Win the summer. Win the season. [LINK]"
- Summit: "July 18 at URI. Six Super Bowl rings on the keynote card. [LINK]"]

Keep the Fire Burning,

Leech

*Scott Leech | URI Strength & Conditioning | Gridiron Warrior*
*scottleechtraining.com*
```

Write to `D:\Claude Projects\Gridiron Warrior\Deliverables\<topic-slug>-freebie.md`. If same-day same-topic file exists, append `-2`, `-3` like the other forges.

### Step 5 — Voice check

If `scripts\voice_check.py` exists, run it against the produced freebie:

```bash
python "D:\Claude Projects\Gridiron Warrior\scripts\voice_check.py" "D:\Claude Projects\Gridiron Warrior\Deliverables\<topic-slug>-freebie.md"
```

If voice_check returns non-zero (banned words, em-dashes, or other violations), rewrite the offending sections and re-run. Loop max twice. If still failing, surface the voice_check output to Scott and stop.

### Step 6 — Report to Scott

Tell him:
1. Output file path
2. The funnel target picked (with one-line rationale)
3. The hook headline
4. Voice check result (clean | rewrote N times | failed)
5. One-line description of the strongest teaching point in the freebie

## Hard rules — what this command MUST NOT do

- Do NOT publish the freebie anywhere (no Substack post, no Kit upload, no IG, no email send)
- Do NOT commit the file
- Do NOT email anyone
- Do NOT auto-invoke any other production skill
- Do NOT use em-dashes
- Do NOT use any banned word
- Do NOT sign off as "Scott" — sign off "Leech" only

## Notes

- **Standalone-invokable:** runs fine outside the Film Study chain. Scott can point it at any brief, transcript, voice note, or content source.
- **One-page constraint is real.** If the source has 8 teaching points, pick the 3-5 strongest. A freebie that runs to two pages defeats the purpose.
- **CTA is mandatory.** A freebie without a funnel is a fact sheet. The whole point is conversion. If no CTA target fits, default to Insiders.
- **Plain markdown output** — Scott (or a downstream tool) handles PDF rendering. Don't embed images, don't use tables, don't use anything that breaks plain pandoc/markdown-to-PDF rendering.
