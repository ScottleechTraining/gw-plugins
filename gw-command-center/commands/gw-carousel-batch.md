---
name: gw-carousel-batch
description: "Batch-build IG carousel HTML for multiple content packs in parallel. Run bare (no arguments) to discover every content pack still waiting on a carousel; the style-pack recommendation is used without confirmation. Central photo assignment, ~5 subagents per wave, mandatory render-and-eyeball verification of every cover before done. Runs nightly at 3:00am as the gw-carousel-batch scheduled job, and on demand."
model: claude-opus-5
---

# /gw-carousel-batch — Parallel IG Carousel Builds

Orchestrates many carousel builds at once. Photo assignment is centralized so no two carousels share a hero. Every cover is rendered and eyeballed before the batch is called done. Each subagent runs the canonical `ig-carousel` skill.

## 1. Input

Two ways in:

**A. Explicit list.** A list of content-pack folders (from `Deliverables/ready/` or `Deliverables/_inbox/`) or slugs, plus the style pack chosen for each carousel.

**B. No arguments — discovery mode.** This is the standing "what's waiting on a carousel" entry point (Louis runs it bare, see `Deliverables/LOUIS-NOTE.md`). Three kinds of waiting work:

1. **New builds:** scan `Deliverables/_inbox/` and `Deliverables/ready/` for every topic folder that has a `*content-pack*.md` but no `*-carousel.html`. For each, recommend a style pack: read the "Pack selection quick-reference" table in the ig-carousel skill's `references/style-packs.md` and match the pack's title/hook keywords against it. Present one table (slug, title hook, recommended pack, why) and build on the recommendations immediately. Do not wait for confirmation (Scott 2026-08-12: the review page's restyle dropdown is the correction path, so a wrong pack costs one rebuild, not a blocked batch).
2. **Restyle rebuilds:** topics in `queue-state.json` where `carousel_needs_polish` is true and `polish_note` starts with `restyle: <Pack Name>`. The pack was chosen from the review page's dropdown, so it is already confirmed - include these in the batch without asking, rebuild the carousel HTML in the named pack from the topic's content pack, and clear nothing yourself (the next /gw-review pass re-judges the rebuilt carousel; SHIP there clears the polish flag).
3. **Cover rebuilds:** topics where `carousel_needs_polish` is true and `polish_note` starts with `cover:`. Rebuild ONLY slide 1 per the note (new treatment and/or photo from the ig-carousel skill's `references/cover-treatments.md`); body slides stay untouched.

If nothing is waiting in any bucket, say so, print the completion marker (section 6), and stop.

Pack rules for both modes:

- Explicit list mode: the pack Scott named wins.
- Otherwise the quick-reference recommendation IS the pack, attended or not. If no row clearly matches, pick the closest fit and flag that slug in the summary table so Scott knows to look at it at review.
- Two-row ties resolve by the photo-forward tiebreak in `references/style-packs.md` (photo pack wins), subject to its rotation guard: read `style_pack` off the last 6 built topics in `queue-state.json` first, and if neither Editorial Long-Form nor Mono Series is among them, suspend the tiebreak for this batch. Say which way the guard went in the assignment table.

Build the slugs in the assignment table and stop there. Do not restyle carousels nobody flagged, do not edit the source content packs, and do not leave a listed slug unbuilt.

## 2. Photo assignment (centrally, FIRST)

Before spawning any agents:

1. List available photos in `C:\IMAGES\Football` and `C:\IMAGES\Gym`.
2. Pick TWO photos per carousel, matched to the topic: a hero for the cover and a body photo for one body slide (photo floor, `references/style-packs.md`). Prefer a landscape body photo so it can carry a two-slide seamless spread. Mono Series carousels get a hero only.
3. Never assign the same photo to two carousels in the batch, hero or body.
4. Record the full assignment table (slug, style pack, content-pack path, hero photo path, body photo path) before anything is spawned. This table is the source of truth for the whole run.

## 3. Build (spawn subagents at 3+ carousels)

One or two carousels: build them yourself, no agents. Three or more: spawn one agent per carousel, at most 5 running at once, next wave after the current one verifies.

Each subagent builds ONE carousel using the `ig-carousel` skill. Spawn with `model: sonnet` set explicitly on every agent (never inherit).

Give each subagent:
- the content-pack path
- the chosen style pack
- the chosen cover treatment (from the ig-carousel skill's `references/cover-treatments.md` quick-reference, matched to the topic and the photo's character; Type Plate is the fallback when the photo can't carry a treatment)
- the assigned hero photo path AND the assigned body photo path
- the photo floor: the cover carries the hero and one body slide carries the body photo, each per the pack's own photo treatment and sizing in `references/style-packs.md` (Mono Series exempt: hero only). If the body photo is landscape, run it as a two-slide seamless spread per `references/seamless-image-spread.md`; otherwise a single photo slide. A build that drops the body photo is a bounce, not a fallback.
- the instruction to prepare every photo as a brightened ~230KB JPEG (quality ~80, resized to slide dimensions, pack treatment baked with Pillow), never a PNG
- the instruction to kill any server or browser process it starts, even on failure
- the copy-source rule: slide text comes from the pack's carousel "Slide Text" section ONLY. Pack meta sections (THE MESSAGE, PULLED FROM THE BRAIN, Cross-Reference Summary, frontmatter, cta_rationale) are triage receipts and NEVER appear on a slide or in a caption, ever (Scott 2026-08-26). If the pack's slide text itself fails an obvious message-gate check (cover promise never paid off in the body, an unexplained label or credit on a slide), the builder reports it back instead of building it broken.

## 4. Verify after each wave

When a wave finishes:

1. Render every produced carousel's slides to PNG, respecting the headless quirks documented in the `ig-carousel` skill's "Known traps" section (`--headless=new`, kill stray processes, unique `--user-data-dir`, `127.0.0.1`, fresh port, window sized to exact slide width).
2. LOOK at every cover image (Read the PNG files). Judge the cover FIRST and on one question: would it stop a coach's thumb in a feed full of workout clips? Layout-correct but flat goes back with a stronger treatment or better photo, same as a broken one.
3. Any dark or blank hero, clipped text, broken layout, or flat cover goes back for a fix in the next wave.
3b. Read the body photo slide as a PNG too. A missing body photo (any pack but Mono Series), text sitting on the photo's subject, or an empty spread slide goes back in the next wave.
4. Read the LAST slide and one body slide as text. If any pack meta leaked onto a slide (THE MESSAGE, PULLED FROM THE BRAIN, a cross-reference line, a bare source credit), the carousel goes back in the next wave and the pack gets flagged in the output; meta on a slide is a hard fail, not a style note.

Do not report done on trust. A file passing a portability or lint check can still render wrong.

## 5. Output

A summary table:

| Slug | Style pack | Hero photo | Body photo | Verified | Path |
|------|-----------|------------|------------|----------|------|

Plus the list of anything skipped and why.

## 6. Completion marker

At the end of EVERY run, including a nothing-waiting no-op, print exactly this on its own line so the scheduled-job validator can see it:

GW-DONE: carousel-batch
