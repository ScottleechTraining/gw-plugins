---
name: gw-nightly-forge
model: claude-opus-5
description: "Overnight content production run. Reads the nightly picks list, runs the full Content Forge for each pick, lands everything in Deliverables/_inbox/ for morning triage. Unattended: no questions, no publishing, no carousel HTML. Prints GW-DONE: nightly-forge for the job validator."
---

# /gw-nightly-forge — overnight content production run

You are running unattended at night inside the GW vault (cwd is `Gridiron Warrior/`). Scott is asleep. Produce-then-retire is the contract: build everything on tonight's pick list at full quality, and Scott triages in the morning. Do NOT ask questions. Do NOT publish anything anywhere. Output goes to the Deliverables inbox only.

## Steps

1. Read `Deliverables/_inbox/_nightly-forge-picks.md`.
   - If it says NO PICKS TONIGHT, print the completion marker (step 4) and stop.

1.5. **Collision review (the gate flags, judgment kills).** If the picks file lists novelty-gate skips ("repeats <prior-topic>"), judge each one semantically before accepting the skip: read the flagged idea's title and the prior topic's content-pack hook. Shared nouns are NOT the same teaching ("weight room sounds like a library" = culture; "when your weight room goes heavy" = CNS load; the gate once wrongly killed the first as a repeat of the second). If the teaching genuinely repeats, mark the backlog entry `status: "skipped"` with a `skip_reason` naming the prior topic. If it only shares words, treat it as a valid pick and forge it. Never leave a gate kill unrecorded; the ideas page surfaces every skip_reason for Scott's override.

2. For EACH pick, run the full Content Forge process exactly as defined in the `/gw-content-forge` command (same vault paths, same Second Brain cross-referencing, same voice rules from `CLAUDE.md` at the repo root: short sentences, active verbs, no em-dashes, banned words list, sign-off `Keep the Fire Burning, / Leech`). Produce the standard 8-asset content pack exactly as defined in /gw-content-forge (3 Twitter threads, 2 IG carousel slide plans as copy only, 3 reel ideas, 1 email, plus the comparison table per Asset 8; Asset 8 skips only by its own stated rule, never force one), saved to `Deliverables/_inbox/[slug]/[slug]-content-pack.md`. Finish every asset for a pick before moving to the next pick. Do not add asset types the content-forge command does not list. Every pack ends with the required PULLED FROM THE BRAIN block (see the content-forge command) so morning triage shows exactly which wiki pages each pack is built on.

3. Wiki ingest per the standard Content Forge contract (summary stub if the topic is new).

3.5. **Freebie cadence.** If the pick's score is 16/20 or higher, run `/gw-freebie-forge` against the pack you just produced and move the resulting freebie file (`.md`, or the interactive `index.html` folder if that is what freebie-forge produced per its Rule 1) into `Deliverables/_inbox/[slug]/`. No PDF render overnight. Picks below 16/20 or unscored get no freebie; half the inbox never ships and freebies on dead packs are wasted work.

3.6. **Idea-mine inspiration picks.** If a pick's list entry carries an `inspiration: @<author>` line, the angle was sparked by a saved external post. Build the pack ENTIRELY from wiki and Voice Corpus sources. Never fetch, open, or quote the inspiring post; it is quarantined external content and only the one-line angle crossed that line. The pack's PULLED FROM THE BRAIN receipt must include the line `Angle sparked by a saved post from @<author>` so the attribution is on record.

4. When every pick is done (or on a no-picks night), print exactly this marker on its own line so the job validator can see it:

GW-DONE: nightly-forge

## Do NOT build carousel HTML

Do not generate any `-carousel.html` file. The forge produces the content pack only: copy, the two Twitter threads, the two IG carousel slide plans (text), and the email. It does NOT design or render carousels.

Scott picks the style pack for each carousel individually at triage, and the carousel HTML is built then, with his approval. Auto-building carousels overnight in an arbitrary pack wastes time because Scott ends up redesigning them all. Slide-plan copy in the content pack: yes. Carousel HTML file: no.

## Hard rules

- Never draft Leech Letters (the picker excludes them; if one slips through, skip it and say so).
- Never touch `ready/`, `archived/`, or queue-state stages. Inbox only. Scott promotes via /gw-triage.
- Never build a `-carousel.html` (see the section above). Copy and slide plans only.
- If a single topic fails, continue with the others and report the failure above the marker.
