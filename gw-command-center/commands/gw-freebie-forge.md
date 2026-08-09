---
name: gw-freebie-forge
model: claude-opus-5
description: "Generate a lead magnet from a brief or content source. Interactive Toolbox-standard HTML is the default format; one-page PDF only when the teaching is list-shaped. Dedup gate against site tools + freebie ledger is mandatory. Funnels into Insiders, a course, or Summit."
---

# /gw-freebie-forge [brief-or-content-path] — Lead Magnet Producer

Takes any brief, transcript, or content source. Produces one-page, printable lead magnet that funnels readers into the right paid offer. Coach-direct. Scott's voice. No commit. No autonomous distribution.

Deliver one freebie plus the Step 6 report. Every teaching point in it must change what a coach does; template sections are limits, not slots to fill. Do not build a second variant, a companion asset, or a promo post.

## Accepted input: $ARGUMENTS

The user provides a file path. Typical inputs:
- A Film Study brief at `Research/Film Study/YYYY-MM-DD-<slug>-film-study-brief.md`
- A `/gw-research` brief at `Research/NotebookLM/<slug>-brief.md`
- A Voice Corpus transcript
- Any markdown file with coaching content

If empty, abort with: "Provide a source file path. Example: `/gw-freebie-forge \"C:\\Claude Projects\\Gridiron Warrior\\Research\\Film Study\\2026-05-25-deceleration-film-study-brief.md\"`."

## Vault paths

- **Voice rules:** `C:\Claude Projects\CLAUDE.md`
- **Output:** `C:\Claude Projects\Gridiron Warrior\Deliverables\<topic-slug>-freebie.md`
- **Wiki for product targeting:** `C:\Claude Projects\Gridiron Warrior\wiki\` (read entities/Insiders, entities/GW-2-0, entities/Contact-Prep, entities/Scores-and-Stops, entities/Summit to pick the right CTA)
- **Voice check guard:** `C:\Claude Projects\Gridiron Warrior\scripts\voice_check.py`

## CREATION RULES (2026-07-06, Scott-approved - these outrank everything below)

Scott killed an entire wave of repetitive cheat-sheet freebies and three PDFs that
duplicated live site tools. These rules exist so that never happens again. They are
written for whichever model runs this command - no session memory required.

**Rule 0 - THE DEDUP GATE. Run it before creating anything.**
Check, in order:
1. `C:\Claude Projects\websites\scottleechtraining.com\tools\index.html` - the Toolbox
   inventory (interactive tools: program audit, high/low CNS planner, training age sort,
   missed lifts tree, session conductor, floor clock, sled load calculator, tri-set timer,
   8-week team talks, hamstring resource, GPS for football).
2. `C:\Claude Projects\Gridiron Warrior\Deliverables\_system\review\freebie-state.json` -
   the freebie ledger. `killed` means dead: never rebuild without Scott explicitly reviving it.
3. `Deliverables\projects\insiders-vault\VAULT-MANIFEST.md` - what members already have.
If the job is already done by a site tool, DO NOT build a shadow PDF of it. Output a short
funnel asset pointing at the live tool instead (or say so and stop). A static copy of an
interactive tool undercuts the tool.

**Rule 1 - THE FORMAT LADDER. Interactive is the default, flat must be earned.**
Default format: a single-file interactive HTML tool at the Toolbox standard (below) or the
Vault interactive template (`Deliverables\_templates\_interactive_template.html`).
A one-page PDF/md cheat sheet is allowed ONLY when the teaching is genuinely list-shaped
(reference card, phase comparison, checklist) or Scott asked for that format by name.
Posters are dead - Scott has killed every poster variant. Do not produce them.

**Rule 2 - KNOWLEDGE-BACKED, NEVER FROM MEMORY.**
Any threshold, percentage, rep rule, or protocol in the freebie must trace to a wiki concept
page, a Voice Corpus source, or a dated NotebookLM brief. If the number is not written down
somewhere in the vault, query NotebookLM and write the brief first (pattern:
`websites\scottleechtraining.com\tools\_plans\brief-*.md`).

**Rule 3 - THE FRESHNESS TEST.**
Before building, answer in one line: what does this teach that no existing freebie or tool
teaches? If the honest answer is "same teaching, new wrapper," stop and say so. A variation
of an existing asset must name what is new (new audience like feeder programs, new season
phase, new interaction) or it does not get built.

**Rule 4 - THE TOOLBOX STANDARD (for interactive builds).**
- Single self-contained index.html, vanilla JS, no framework, no build step.
- Non-trivial logic as pure functions with a module.exports guard for headless tests; ship a `?demo=` URL hook.
- State in localStorage only, key pattern `gw-{tool}-{purpose}`.
- Lead capture: fetch() POST to `https://app.kit.com/forms/9647774/subscriptions` (shared free-rack gate; `tb_email`/`tb_unlocked` localStorage).
- Printable `@media print` view; sign-off "Keep the Fire Burning. - Leech" + Insiders CTA.
- Design tokens: --ink:#1a2742, --gold:#c0902f, --steel:#5b6472, --line:#d1d5db, stoplight --high:#dc2626 / --low:#10b981 / --amber:#f59e0b; fonts Oswald + Anton; navy .hero header; back-breadcrumb to /tools/.
- For Toolbox builds, never use the legacy `_shared/gw-tools.css` black/stoplight system - deprecated here. (Insiders deep-dive pages under /tools/ still reuse it via /gw-advanced-scouting; that is a different surface.)

**Rule 5 - EVERY FREEBIE ENTERS THE LEDGER.**
New freebies are pending until Scott reviews them on freebies.html
(`python -m scripts.gwqueue.build_freebie_review_page` regenerates it). Nothing ships,
uploads, or enters the Vault without his approval.

## Steps

### Step 1 — Read the source

Read the file at `$ARGUMENTS`. Extract: topic, the 3-5 strongest teaching points, the single most coach-direct quote or line, any specific stat or example.

If the source is a Film Study brief, the "Bottom-line takeaways" section is the obvious source. If it's a longer brief or transcript, distill.

### Step 2 — Read voice rules

Read `C:\Claude Projects\CLAUDE.md`. Internalize:
- Short sentences. Active verbs. Plain language.
- **No em-dashes. Not one.**
- Banned words: delve, tapestry, vibrant, transformative, unlock, leverage (as verb), game-changer, revolutionary, groundbreaking, seamless, robust, utilize, synergy, holistic, empower, journey, curated, cutting-edge, innovative, best-in-class, dive into, unpack, explore, elevate, reimagine, supercharge, fluff
- Tough love. Coach in the trenches.
- Sign off: `Keep the Fire Burning,` / `Leech`

### Step 3 — Pick the CTA target

Read the wiki entity pages to decide where this freebie funnels. Priority order:

1. **Insiders ($1 first month trial)** — default. Always works. Use unless a course is a clearly better fit.
2. **Contact Prep ($87)** — if the topic is physicality, tackling, partner drills, violence-as-skill, OL/DL.
3. **Scores and Stops ($97)** — if the topic is agility, space creation, closing space, decision-making.
4. **Gridiron Warrior 2.0 ($197)** — if the topic is summer programming, full-team S&C, season-long programs.

Decide one. Name it in Step 6 report so Scott knows the funnel direction.

### Step 4 — Write the freebie

Interactive HTML is the default per Rule 1. Use the markdown template below only when Rule 1's list-shaped exception applies or Scott named the format. Interactive builds follow Rule 4 and land at `Deliverables\projects\insiders-vault\incoming\<topic-slug>\index.html`.

Markdown-path structure (one page, printable to PDF):

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

# [Hook headline: bold coaching truth, under 60 chars]

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

## [Next step: direct, urgency-flavored CTA line]

[2-3 sentences pitching the funnel target picked in Step 3. Include the price or trial offer. Include a link placeholder Scott can swap in. Specific to the offer:

- Insiders: "$1 for the first month. Cancel anytime. [LINK]"
- Contact Prep: "$87. 60+ videos. Three-phase progression. [LINK]"
- Scores and Stops: "$97. Agility drills for creating and closing space. [LINK]"
- GW 2.0: "$197. Win the summer. Win the season. [LINK]"]

Keep the Fire Burning,

Leech

*Scott Leech | URI Strength & Conditioning | Gridiron Warrior*
*scottleechtraining.com*
```

Write to `C:\Claude Projects\Gridiron Warrior\Deliverables\<topic-slug>-freebie.md`. If same-day same-topic file exists, append `-2`, `-3` like the other forges.

### Step 5 — Voice check

If `scripts\voice_check.py` exists, run it against the produced freebie:

```bash
python "C:\Claude Projects\Gridiron Warrior\scripts\voice_check.py" "C:\Claude Projects\Gridiron Warrior\Deliverables\<topic-slug>-freebie.md"
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
- **Markdown-path output only** — for the Rule 1 exception path, Scott (or a downstream tool) handles PDF rendering. Don't embed images, don't use tables, don't use anything that breaks plain pandoc/markdown-to-PDF rendering.
