---
name: gw-carousel-batch
description: "Batch-build IG carousel HTML for multiple content packs in parallel. Run bare (no arguments) to discover every content pack still waiting on a carousel and get a recommended style pack per topic. Central photo assignment, ~5 subagents per wave, mandatory render-and-eyeball verification of every cover before done."
model: claude-opus-5
---

# /gw-carousel-batch — Parallel IG Carousel Builds

Orchestrates many carousel builds at once. Photo assignment is centralized so no two carousels share a hero. Every cover is rendered and eyeballed before the batch is called done. Each subagent runs the canonical `ig-carousel` skill.

## 1. Input

Two ways in:

**A. Explicit list.** A list of content-pack folders (from `Deliverables/ready/` or `Deliverables/_inbox/`) or slugs, plus the style pack chosen for each carousel.

**B. No arguments — discovery mode.** This is the standing "what's waiting on a carousel" entry point (Louis runs it bare, see `Deliverables/LOUIS-NOTE.md`). Two kinds of waiting work:

1. **New builds:** scan `Deliverables/_inbox/` and `Deliverables/ready/` for every topic folder that has a `*content-pack*.md` but no `*-carousel.html`. For each, recommend a style pack: read the "Pack selection quick-reference" table in the ig-carousel skill's `references/style-packs.md` and match the pack's title/hook keywords against it. Present one table (slug, title hook, recommended pack, why) and wait for confirmation or swaps before building.
2. **Restyle rebuilds:** topics in `queue-state.json` where `carousel_needs_polish` is true and `polish_note` starts with `restyle: <Pack Name>`. The pack was chosen from the review page's dropdown, so it is already confirmed - include these in the batch without asking, rebuild the carousel HTML in the named pack from the topic's content pack, and clear nothing yourself (the next /gw-review pass re-judges the rebuilt carousel; SHIP there clears the polish flag).
3. **Cover rebuilds:** topics where `carousel_needs_polish` is true and `polish_note` starts with `cover:`. Rebuild ONLY slide 1 per the note (new treatment and/or photo from the ig-carousel skill's `references/cover-treatments.md`); body slides stay untouched.

If nothing is waiting in any bucket, say so and stop.

Pack rules for both modes:

- Attended and a pack is missing or unclear: recommend one from the quick-reference table and ask to confirm. Never build on a guess.
- If invoked unattended (no human to answer), skip any carousel without a confirmed pack and record it in the skipped list. Do not guess a pack.

## 2. Photo assignment (centrally, FIRST)

Before spawning any agents:

1. List available photos in `C:\IMAGES\Football` and `C:\IMAGES\Gym`.
2. Pick one hero photo per carousel, matched to the topic.
3. Never assign the same photo to two carousels in the batch.
4. Record the full assignment table (slug, style pack, content-pack path, assigned photo path) before anything is spawned. This table is the source of truth for the whole run.

## 3. Spawn subagents in waves of ~5

Each subagent builds ONE carousel using the `ig-carousel` skill. Spawn with `model: sonnet` set explicitly on every agent (never inherit).

Give each subagent:
- the content-pack path
- the chosen style pack
- the chosen cover treatment (from the ig-carousel skill's `references/cover-treatments.md` quick-reference, matched to the topic and the photo's character; Type Plate is the fallback when the photo can't carry a treatment)
- the assigned hero photo path
- the instruction to prepare the hero as a brightened ~230KB JPEG (quality ~80, resized to slide dimensions), never a PNG
- the instruction to kill any server or browser process it starts, even on failure

## 4. Verify after each wave

When a wave finishes:

1. Render every produced carousel's slides to PNG, respecting the headless quirks documented in the `ig-carousel` skill's "Known traps" section (`--headless=new`, kill stray processes, unique `--user-data-dir`, `127.0.0.1`, fresh port, window sized to exact slide width).
2. LOOK at every cover image (Read the PNG files). Judge the cover FIRST and on one question: would it stop a coach's thumb in a feed full of workout clips? Layout-correct but flat goes back with a stronger treatment or better photo, same as a broken one.
3. Any dark or blank hero, clipped text, broken layout, or flat cover goes back for a fix in the next wave.

Do not report done on trust. A file passing a portability or lint check can still render wrong.

## 5. Output

A summary table:

| Slug | Style pack | Photo used | Verified | Path |
|------|-----------|------------|----------|------|

Plus the list of anything skipped and why.
