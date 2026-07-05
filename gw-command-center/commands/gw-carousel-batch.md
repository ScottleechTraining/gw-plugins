---
name: gw-carousel-batch
description: "Batch-build IG carousel HTML for multiple content packs in parallel. Central photo assignment, ~5 subagents per wave, mandatory render-and-eyeball verification of every cover before done."
model: opus
---

# /gw-carousel-batch — Parallel IG Carousel Builds

Orchestrates many carousel builds at once. Photo assignment is centralized so no two carousels share a hero. Every cover is rendered and eyeballed before the batch is called done. Each subagent runs the canonical `ig-carousel` skill.

## 1. Input

Take a list of content-pack folders (from `Deliverables/ready/` or `Deliverables/_inbox/`) or slugs, plus the style pack Scott chose for each carousel.

- If a carousel is missing its style pack, ask which pack.
- If invoked unattended (no human to answer), skip any carousel without a chosen pack and record it in the skipped list. Do not guess a pack.

## 2. Photo assignment (centrally, FIRST)

Before spawning any agents:

1. List available photos in `D:\IMAGES\Football` and `D:\IMAGES\Gym`.
2. Pick one hero photo per carousel, matched to the topic.
3. Never assign the same photo to two carousels in the batch.
4. Record the full assignment table (slug, style pack, content-pack path, assigned photo path) before anything is spawned. This table is the source of truth for the whole run.

## 3. Spawn subagents in waves of ~5

Each subagent builds ONE carousel using the `ig-carousel` skill. Spawn with `model: sonnet` set explicitly on every agent (never inherit).

Give each subagent:
- the content-pack path
- the chosen style pack
- the assigned hero photo path
- the instruction to prepare the hero as a brightened ~230KB JPEG (quality ~80, resized to slide dimensions), never a PNG
- the instruction to kill any server or browser process it starts, even on failure

## 4. Verify after each wave

When a wave finishes:

1. Render every produced carousel's slides to PNG, respecting the headless quirks documented in the `ig-carousel` skill's "Known traps" section (`--headless=new`, kill stray processes, unique `--user-data-dir`, `127.0.0.1`, fresh port, window sized to exact slide width).
2. LOOK at every cover image (Read the PNG files).
3. Any dark or blank hero, clipped text, or broken layout goes back for a fix in the next wave.

Do not report done on trust. A file passing a portability or lint check can still render wrong.

## 5. Output

A summary table:

| Slug | Style pack | Photo used | Verified | Path |
|------|-----------|------------|----------|------|

Plus the list of anything skipped and why.
