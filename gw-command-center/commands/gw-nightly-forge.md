---
name: gw-nightly-forge
description: "Overnight content production run. Reads the nightly picks list, runs the full Content Forge for each pick, lands everything in Deliverables/_inbox/ for morning triage. Unattended: no questions, no publishing, no carousel HTML. Prints GW-DONE: nightly-forge for the job validator."
---

# /gw-nightly-forge — overnight content production run

You are running unattended at night inside the GW vault (cwd is `Gridiron Warrior/`). Scott is asleep. Produce-then-retire is the contract: build everything on tonight's pick list at full quality, and Scott triages in the morning. Do NOT ask questions. Do NOT publish anything anywhere. Output goes to the Deliverables inbox only.

## Steps

1. Read `Deliverables/_inbox/_nightly-forge-picks.md`.
   - If it says NO PICKS TONIGHT, print the completion marker (step 4) and stop.

2. For EACH pick, run the full Content Forge process exactly as defined in the `/gw-content-forge` command (same vault paths, same Second Brain cross-referencing, same voice rules from `CLAUDE.md` at the repo root: short sentences, active verbs, no em-dashes, banned words list, sign-off `Keep the Fire Burning, / Leech`). Produce the standard pack: 2 Twitter threads, 2 IG carousels (slide plans / copy only), 1 email, saved to `Deliverables/_inbox/[slug]/[slug]-content-pack.md`. Every pack ends with the required PULLED FROM THE BRAIN block (see the content-forge command) so morning triage shows exactly which wiki pages each pack is built on.

3. Wiki ingest per the standard Content Forge contract (summary stub if the topic is new).

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
